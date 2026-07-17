import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_external_ids(
        self, bank_connection_id: uuid.UUID, external_ids: Sequence[str]
    ) -> dict[str, Transaction]:
        if not external_ids:
            return {}
        result = await self.session.execute(
            select(Transaction).where(
                Transaction.bank_connection_id == bank_connection_id,
                Transaction.external_transaction_id.in_(external_ids),
                Transaction.deleted_at.is_(None),
            )
        )
        return {transaction.external_transaction_id: transaction for transaction in result.scalars()}

    def add(self, transaction: Transaction) -> None:
        self.session.add(transaction)

    async def list_for_user(
        self,
        user_id: uuid.UUID,
        bank_connection_id: uuid.UUID | None,
        limit: int,
        offset: int,
    ) -> list[Transaction]:
        query = select(Transaction).where(
            Transaction.user_id == user_id, Transaction.deleted_at.is_(None)
        )
        if bank_connection_id:
            query = query.where(Transaction.bank_connection_id == bank_connection_id)
        result = await self.session.execute(
            query.order_by(Transaction.occurred_at.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars())
