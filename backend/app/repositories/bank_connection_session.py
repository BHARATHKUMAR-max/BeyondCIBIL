import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bank_connection_session import BankConnectionSession


class BankConnectionSessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def add(self, connection_session: BankConnectionSession) -> None:
        self.session.add(connection_session)

    async def get_for_user(self, session_id: uuid.UUID, user_id: uuid.UUID) -> BankConnectionSession | None:
        result = await self.session.execute(
            select(BankConnectionSession)
            .where(
                BankConnectionSession.id == session_id,
                BankConnectionSession.user_id == user_id,
                BankConnectionSession.deleted_at.is_(None),
            )
            .with_for_update()
        )
        return result.scalar_one_or_none()

    @staticmethod
    def is_expired(connection_session: BankConnectionSession) -> bool:
        return connection_session.expires_at <= datetime.now(UTC)
