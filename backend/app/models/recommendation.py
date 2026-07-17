from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.prediction_history import PredictionHistory
    from app.models.user import User


class Recommendation(BaseModel):
    __tablename__ = "recommendations"
    __table_args__ = (
        CheckConstraint("priority BETWEEN 1 AND 5", name="ck_recommendations_priority"),
        CheckConstraint("status IN ('active', 'dismissed', 'completed', 'expired')", name="ck_recommendations_status"),
        Index("ix_recommendations_user_status", "user_id", "status"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    prediction_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("prediction_history.id", ondelete="SET NULL"), nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=False)
    action_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, server_default="3")
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="active")
    metadata_json: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSONB, nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    user: Mapped["User"] = relationship(back_populates="recommendations")
    prediction: Mapped["PredictionHistory | None"] = relationship(back_populates="recommendations")
