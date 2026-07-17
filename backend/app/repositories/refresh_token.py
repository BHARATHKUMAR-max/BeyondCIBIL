import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def add(self, refresh_token: RefreshToken) -> None:
        self.session.add(refresh_token)

    async def get_active_by_token_id(self, token_id: uuid.UUID) -> RefreshToken | None:
        result = await self.session.execute(
            select(RefreshToken)
            .where(
                RefreshToken.token_id == token_id,
                RefreshToken.revoked_at.is_(None),
                RefreshToken.expires_at > datetime.now(UTC),
            )
            .with_for_update()
        )
        return result.scalar_one_or_none()

    def revoke(self, refresh_token: RefreshToken) -> None:
        refresh_token.revoked_at = datetime.now(UTC)
