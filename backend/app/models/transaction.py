from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.bank_connection import BankConnection
    from app.models.feature_vector import FeatureVector
    from app.models.user import User


class Transaction(BaseModel):
    __tablename__ = "transactions"
    __table_args__ = (
        CheckConstraint("amount >= 0", name="ck_transactions_nonnegative_amount"),
        CheckConstraint("transaction_type IN ('credit', 'debit')", name="ck_transactions_type"),
        Index("ix_transactions_user_occurred", "user_id", "occurred_at"),
        Index("ix_transactions_connection_external", "bank_connection_id", "external_transaction_id", unique=True),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    bank_connection_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("bank_connections.id", ondelete="RESTRICT"), nullable=False)
    external_transaction_id: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, server_default="INR")
    transaction_type: Mapped[str] = mapped_column(String(10), nullable=False)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    merchant_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    user: Mapped["User"] = relationship(back_populates="transactions")
    bank_connection: Mapped["BankConnection"] = relationship(back_populates="transactions")
    feature_vectors: Mapped[list["FeatureVector"]] = relationship(back_populates="transaction")
