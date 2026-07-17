from __future__ import annotations

import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    TokenValidationError,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.repositories.refresh_token import RefreshTokenRepository
from app.repositories.user import UserRepository
from app.schemas.auth import TokenResponse


class AuthenticationError(Exception):
    """Raised when supplied credentials or tokens are not valid."""


class EmailAlreadyRegisteredError(Exception):
    """Raised when an email address is already assigned to a user."""


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)
        self.refresh_tokens = RefreshTokenRepository(session)

    async def register(self, email: str, password: str, full_name: str | None) -> User:
        normalized_email = email.lower()
        if await self.users.get_by_email(normalized_email):
            raise EmailAlreadyRegisteredError
        user = User(email=normalized_email, password_hash=hash_password(password), full_name=full_name)
        self.users.add(user)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise EmailAlreadyRegisteredError from exc
        await self.session.refresh(user)
        return user

    async def login(self, email: str, password: str) -> TokenResponse:
        user = await self.users.get_by_email(email.lower())
        if not user or not user.is_active or not verify_password(password, user.password_hash):
            raise AuthenticationError
        return await self._issue_token_pair(user.id)

    async def refresh(self, encoded_token: str) -> TokenResponse:
        payload = self._decode_refresh_token(encoded_token)
        user_id, token_id = self._token_identifiers(payload)
        stored_token = await self.refresh_tokens.get_active_by_token_id(token_id)
        if not stored_token or stored_token.user_id != user_id:
            raise AuthenticationError
        self.refresh_tokens.revoke(stored_token)
        tokens = await self._issue_token_pair(user_id, commit=False)
        await self.session.commit()
        return tokens

    async def logout(self, encoded_token: str) -> None:
        payload = self._decode_refresh_token(encoded_token)
        user_id, token_id = self._token_identifiers(payload)
        stored_token = await self.refresh_tokens.get_active_by_token_id(token_id)
        if not stored_token or stored_token.user_id != user_id:
            raise AuthenticationError
        self.refresh_tokens.revoke(stored_token)
        await self.session.commit()

    async def _issue_token_pair(self, user_id: uuid.UUID, commit: bool = True) -> TokenResponse:
        token_id = uuid.uuid4()
        refresh_token, expires_at = create_refresh_token(user_id, token_id)
        self.refresh_tokens.add(
            RefreshToken(token_id=token_id, user_id=user_id, expires_at=expires_at)
        )
        if commit:
            await self.session.commit()
        return TokenResponse(access_token=create_access_token(user_id), refresh_token=refresh_token)

    @staticmethod
    def _token_identifiers(payload: dict[str, object]) -> tuple[uuid.UUID, uuid.UUID]:
        try:
            return uuid.UUID(str(payload["sub"])), uuid.UUID(str(payload["jti"]))
        except (KeyError, ValueError) as exc:
            raise AuthenticationError from exc

    @staticmethod
    def _decode_refresh_token(encoded_token: str) -> dict[str, object]:
        try:
            return decode_token(encoded_token, expected_type="refresh")
        except TokenValidationError as exc:
            raise AuthenticationError from exc
