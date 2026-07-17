from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field


class FinancialSummary(BaseModel):
    """Summary of user's financial behavior metrics."""

    total_transactions: int
    total_credits: Decimal
    total_debits: Decimal
    average_monthly_income: Decimal
    average_monthly_spending: Decimal
    savings_rate: Decimal = Field(description="Savings as percentage of income")
    active_banks: int
    period_start: datetime
    period_end: datetime


class CreditScoreBreakdown(BaseModel):
    """Components contributing to the alternative credit score."""

    income_stability: Decimal = Field(description="Score based on income consistency")
    spending_patterns: Decimal = Field(description="Score based on spending behavior")
    account_activity: Decimal = Field(description="Score based on transaction frequency")
    payment_consistency: Decimal = Field(description="Score based on regular payments")
    overall_score: Decimal = Field(description="Final ACS score (0-1000)")


class Prediction(BaseModel):
    """Historical prediction record."""

    id: str
    model_name: str
    model_version: str
    prediction_type: str
    prediction: dict[str, Any]
    confidence: float | None
    calculated_at: datetime


class DashboardResponse(BaseModel):
    """Complete dashboard data for a user."""

    user_id: str
    credit_score: CreditScoreBreakdown
    financial_summary: FinancialSummary
    recent_predictions: list[Prediction]
    active_recommendations: int
    last_updated: datetime
