from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.alternative_credit_score import AlternativeCreditScore
    from app.models.bank_connection import BankConnection
    from app.models.feature_vector import FeatureVector
    from app.models.prediction_history import PredictionHistory
    from app.models.recommendation import Recommendation
    from app.models.refresh_token import RefreshToken
    from app.models.transaction import Transaction


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    bank_connections: Mapped[list["BankConnection"]] = relationship(back_populates="user")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")
    feature_vectors: Mapped[list["FeatureVector"]] = relationship(back_populates="user")
    alternative_credit_scores: Mapped[list["AlternativeCreditScore"]] = relationship(back_populates="user")
    prediction_history: Mapped[list["PredictionHistory"]] = relationship(back_populates="user")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="user")
