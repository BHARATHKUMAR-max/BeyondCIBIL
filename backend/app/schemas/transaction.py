from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    bank_connection_id: UUID
    external_transaction_id: str
    amount: Decimal
    currency: str
    transaction_type: str
    category: str | None
    merchant_name: str | None
    description: str | None
    occurred_at: datetime


class TransactionSyncResponse(BaseModel):
    created: int
    updated: int
