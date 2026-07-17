from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.alternative_credit_score import AlternativeCreditScore
    from app.models.recommendation import Recommendation
    from app.models.user import User


class PredictionHistory(BaseModel):
    __tablename__ = "prediction_history"
    __table_args__ = (
        CheckConstraint("confidence IS NULL OR confidence BETWEEN 0 AND 1", name="ck_prediction_history_confidence"),
        Index("ix_prediction_history_user_created", "user_id", "created_at"),
        Index("ix_prediction_history_model", "model_name", "model_version"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    alternative_credit_score_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("alternative_credit_scores.id", ondelete="SET NULL"), nullable=True)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    model_version: Mapped[str] = mapped_column(String(100), nullable=False)
    prediction_type: Mapped[str] = mapped_column(String(100), nullable=False)
    input_snapshot: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    prediction: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 4), nullable=True)
    user: Mapped["User"] = relationship(back_populates="prediction_history")
    alternative_credit_score: Mapped["AlternativeCreditScore | None"] = relationship(back_populates="prediction_history")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="prediction")
