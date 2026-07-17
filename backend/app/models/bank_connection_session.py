from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.bank_connection import BankConnection
    from app.models.user import User


class BankConnectionSession(BaseModel):
    """Persistent state for a provider-agnostic bank connection flow."""

    __tablename__ = "bank_connection_sessions"
    __table_args__ = (
        CheckConstraint(
            "status IN ('auth_required', 'otp_pending', 'consent_required', 'completed', 'failed', 'expired')",
            name="ck_bank_connection_sessions_status",
        ),
        Index("ix_bank_connection_sessions_user_status", "user_id", "status"),
        Index("ix_bank_connection_sessions_reference", "provider_reference", unique=True),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    bank_code: Mapped[str] = mapped_column(String(100), nullable=False)
    provider_reference: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, server_default="auth_required")
    customer_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    consented_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    bank_connection_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("bank_connections.id", ondelete="SET NULL"), nullable=True, unique=True
    )
    provider_payload: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    user: Mapped["User"] = relationship()
    bank_connection: Mapped["BankConnection | None"] = relationship()
