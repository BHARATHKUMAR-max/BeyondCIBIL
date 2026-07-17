from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, ForeignKey, Index, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.user import User


class FeatureVector(BaseModel):
    __tablename__ = "feature_vectors"
    __table_args__ = (
        Index("ix_feature_vectors_user_version", "user_id", "feature_version"),
        Index("ix_feature_vectors_transaction", "transaction_id"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    transaction_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("transactions.id", ondelete="SET NULL"), nullable=True)
    feature_version: Mapped[str] = mapped_column(String(100), nullable=False)
    features: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    period_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    period_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    user: Mapped["User"] = relationship(back_populates="feature_vectors")
    transaction: Mapped["Transaction | None"] = relationship(back_populates="feature_vectors")
