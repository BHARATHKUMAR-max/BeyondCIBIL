from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction
from app.models.user import User
from app.repositories.bank_connection import BankConnectionRepository
from app.repositories.transaction import TransactionRepository
from app.services.transactions.contracts import TransactionSource


class TransactionFetchError(Exception):
    """Raised when a transaction fetch cannot be completed safely."""


class TransactionFetchService:
    def __init__(self, session: AsyncSession, source: TransactionSource) -> None:
        self.session = session
        self.source = source
        self.connections = BankConnectionRepository(session)
        self.transactions = TransactionRepository(session)

    async def sync(self, user: User, bank_connection_id: uuid.UUID) -> tuple[int, int]:
        connection = await self.connections.get_for_user(bank_connection_id, user.id)
        if not connection or connection.connection_status != "active":
            raise TransactionFetchError("Active bank connection not found")

        source_transactions = await self.source.fetch_transactions(connection, connection.last_synced_at)
        existing = await self.transactions.get_by_external_ids(
            connection.id, [item.external_transaction_id for item in source_transactions]
        )
        created = 0
        updated = 0
        for item in source_transactions:
            transaction = existing.get(item.external_transaction_id)
            if transaction is None:
                transaction = Transaction(
                    user_id=user.id,
                    bank_connection_id=connection.id,
                    external_transaction_id=item.external_transaction_id,
                    amount=item.amount,
                    currency=item.currency,
                    transaction_type=item.transaction_type,
                    category=item.category,
                    merchant_name=item.merchant_name,
                    description=item.description,
                    occurred_at=item.occurred_at,
                )
                self.transactions.add(transaction)
                created += 1
            else:
                transaction.amount = item.amount
                transaction.currency = item.currency
                transaction.transaction_type = item.transaction_type
                transaction.category = item.category
                transaction.merchant_name = item.merchant_name
                transaction.description = item.description
                transaction.occurred_at = item.occurred_at
                updated += 1
        connection.last_synced_at = datetime.now(UTC)
        await self.session.commit()
        return created, updated

    async def list_transactions(
        self,
        user: User,
        bank_connection_id: uuid.UUID | None,
        limit: int,
        offset: int,
    ) -> list[Transaction]:
        return await self.transactions.list_for_user(user.id, bank_connection_id, limit, offset)
