from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.prediction_history import PredictionHistory
    from app.models.user import User


class AlternativeCreditScore(BaseModel):
    __tablename__ = "alternative_credit_scores"
    __table_args__ = (
        CheckConstraint("score BETWEEN 0 AND 1000", name="ck_alternative_credit_scores_range"),
        Index("ix_alternative_scores_user_calculated", "user_id", "calculated_at"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    score: Mapped[Decimal] = mapped_column(Numeric(7, 2), nullable=False)
    model_version: Mapped[str] = mapped_column(String(100), nullable=False)
    score_components: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    user: Mapped["User"] = relationship(back_populates="alternative_credit_scores")
    prediction_history: Mapped[list["PredictionHistory"]] = relationship(back_populates="alternative_credit_score")
