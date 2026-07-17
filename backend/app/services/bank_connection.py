from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bank_connection import BankConnection
from app.models.bank_connection_session import BankConnectionSession
from app.models.user import User
from app.repositories.bank_connection import BankConnectionRepository
from app.repositories.bank_connection_session import BankConnectionSessionRepository
from app.services.banking.contracts import BankConnector, BankProviderError, SupportedBank


class BankConnectionFlowError(Exception):
    """Raised when a user attempts an invalid connection-flow transition."""


class BankConnectionService:
    def __init__(self, session: AsyncSession, connector: BankConnector) -> None:
        self.session = session
        self.connector = connector
        self.connections = BankConnectionRepository(session)
        self.flow_sessions = BankConnectionSessionRepository(session)

    def list_banks(self) -> list[SupportedBank]:
        return self.connector.list_supported_banks()

    async def start(self, user: User, bank_code: str) -> BankConnectionSession:
        if bank_code not in {bank.code for bank in self.connector.list_supported_banks()}:
            raise BankConnectionFlowError("Unsupported bank")
        flow_session = BankConnectionSession(
            user_id=user.id,
            bank_code=bank_code,
            provider_reference=str(uuid.uuid4()),
            status="auth_required",
            expires_at=datetime.now(UTC) + timedelta(minutes=15),
        )
        self.flow_sessions.add(flow_session)
        await self.session.commit()
        await self.session.refresh(flow_session)
        return flow_session

    async def authenticate(self, user: User, session_id: uuid.UUID, customer_id: str, password: str) -> BankConnectionSession:
        flow_session = await self._active_session(session_id, user.id, "auth_required")
        try:
            challenge = self.connector.authenticate(flow_session.bank_code, customer_id, password)
        except BankProviderError as exc:
            flow_session.status = "failed"
            await self.session.commit()
            raise BankConnectionFlowError(str(exc)) from exc
        flow_session.provider_reference = challenge.provider_reference
        flow_session.customer_id = customer_id
        flow_session.status = "otp_pending"
        await self.session.commit()
        await self.session.refresh(flow_session)
        return flow_session

    async def verify_otp(self, user: User, session_id: uuid.UUID, otp: str) -> BankConnectionSession:
        flow_session = await self._active_session(session_id, user.id, "otp_pending")
        try:
            self.connector.verify_otp(flow_session.provider_reference, otp)
        except BankProviderError as exc:
            raise BankConnectionFlowError(str(exc)) from exc
        flow_session.status = "consent_required"
        await self.session.commit()
        await self.session.refresh(flow_session)
        return flow_session

    async def grant_consent(self, user: User, session_id: uuid.UUID) -> BankConnectionSession:
        flow_session = await self._active_session(session_id, user.id, "consent_required")
        try:
            account = self.connector.connect_account(flow_session.provider_reference)
        except BankProviderError as exc:
            raise BankConnectionFlowError(str(exc)) from exc
        connection = BankConnection(
            user_id=user.id,
            provider="mock",
            external_account_id=account.external_account_id,
            institution_name=account.institution_name,
            account_name=account.account_name,
            account_mask=account.account_mask,
            currency=account.currency,
            connection_status="active",
            last_synced_at=None,
        )
        self.connections.add(connection)
        await self.session.flush()
        flow_session.bank_connection_id = connection.id
        flow_session.consented_at = datetime.now(UTC)
        flow_session.status = "completed"
        await self.session.commit()
        await self.session.refresh(flow_session)
        return flow_session

    async def list_connections(self, user: User) -> list[BankConnection]:
        return await self.connections.list_for_user(user.id)

    async def _active_session(self, session_id: uuid.UUID, user_id: uuid.UUID, expected_status: str) -> BankConnectionSession:
        flow_session = await self.flow_sessions.get_for_user(session_id, user_id)
        if not flow_session:
            raise BankConnectionFlowError("Connection session not found")
        if self.flow_sessions.is_expired(flow_session):
            flow_session.status = "expired"
            await self.session.commit()
            raise BankConnectionFlowError("Connection session has expired")
        if flow_session.status != expected_status:
            raise BankConnectionFlowError("Invalid connection-flow state")
        return flow_session
