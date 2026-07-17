from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Protocol

from app.models.bank_connection import BankConnection


@dataclass(frozen=True)
class SourceTransaction:
    external_transaction_id: str
    amount: Decimal
    currency: str
    transaction_type: str
    occurred_at: datetime
    category: str | None = None
    merchant_name: str | None = None
    description: str | None = None


class TransactionSource(Protocol):
    """Port for mock data and future Account Aggregator transaction APIs."""

    async def fetch_transactions(
        self, connection: BankConnection, since: datetime | None = None
    ) -> list[SourceTransaction]: ...
