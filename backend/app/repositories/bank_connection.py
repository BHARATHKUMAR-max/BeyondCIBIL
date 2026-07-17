import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bank_connection import BankConnection


class BankConnectionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def add(self, connection: BankConnection) -> None:
        self.session.add(connection)

    async def list_for_user(self, user_id: uuid.UUID) -> list[BankConnection]:
        result = await self.session.execute(
            select(BankConnection)
            .where(BankConnection.user_id == user_id, BankConnection.deleted_at.is_(None))
            .order_by(BankConnection.created_at.desc())
        )
        return list(result.scalars())

    async def get_for_user(self, connection_id: uuid.UUID, user_id: uuid.UUID) -> BankConnection | None:
        result = await self.session.execute(
            select(BankConnection).where(
                BankConnection.id == connection_id,
                BankConnection.user_id == user_id,
                BankConnection.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()
