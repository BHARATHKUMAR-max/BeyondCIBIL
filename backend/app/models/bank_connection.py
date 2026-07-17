from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.user import User


class BankConnection(BaseModel):
    __tablename__ = "bank_connections"
    __table_args__ = (
        CheckConstraint("connection_status IN ('active', 'pending', 'error', 'revoked')", name="ck_bank_connections_status"),
        Index("ix_bank_connections_user_status", "user_id", "connection_status"),
        Index("ix_bank_connections_provider_external", "provider", "external_account_id", unique=True),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    external_account_id: Mapped[str] = mapped_column(String(255), nullable=False)
    institution_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    account_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    account_mask: Mapped[str | None] = mapped_column(String(8), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, server_default="INR")
    connection_status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="pending")
    access_token_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    user: Mapped["User"] = relationship(back_populates="bank_connections")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="bank_connection")
