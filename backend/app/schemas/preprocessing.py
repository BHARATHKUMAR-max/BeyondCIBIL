from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class RawTransaction:
    """Provider-neutral transaction input accepted by the preprocessing pipeline."""

    external_transaction_id: str | None
    amount: Decimal | float | int | str | None
    currency: str | None
    transaction_type: str | None
    occurred_at: datetime | str | None
    merchant_name: str | None = None
    description: str | None = None
    category: str | None = None


@dataclass(frozen=True)
class CleanTransaction:
    external_transaction_id: str
    amount: Decimal
    currency: str
    transaction_type: str
    occurred_at: datetime
    merchant_name: str
    description: str
    category: str | None
    is_outlier: bool = False


@dataclass(frozen=True)
class RejectedTransaction:
    index: int
    reason: str


@dataclass(frozen=True)
class ProcessingFeatures:
    transaction_count: int
    credit_count: int
    debit_count: int
    total_credits: Decimal
    total_debits: Decimal
    average_debit: Decimal
    outlier_count: int
    category_debits: dict[str, Decimal]
    first_transaction_at: datetime | None
    last_transaction_at: datetime | None
    active_days: int


@dataclass(frozen=True)
class PreprocessingResult:
    transactions: list[CleanTransaction]
    rejected: list[RejectedTransaction]
    features: ProcessingFeatures
    metadata: dict[str, int] = field(default_factory=dict)
