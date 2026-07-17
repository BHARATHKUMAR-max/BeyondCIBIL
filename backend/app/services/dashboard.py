from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING

from app.models.user import User
from app.repositories.alternative_credit_score import AlternativeCreditScoreRepository
from app.repositories.bank_connection import BankConnectionRepository
from app.repositories.prediction_history import PredictionHistoryRepository
from app.repositories.recommendation import RecommendationRepository
from app.repositories.transaction import TransactionRepository
from app.schemas.dashboard import (
    CreditScoreBreakdown,
    DashboardResponse,
    FinancialSummary,
    Prediction,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class DashboardService:
    """Provides dashboard data with mock fallback until ML integration."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.transactions = TransactionRepository(session)
        self.bank_connections = BankConnectionRepository(session)
        self.credit_scores = AlternativeCreditScoreRepository(session)
        self.predictions = PredictionHistoryRepository(session)
        self.recommendations = RecommendationRepository(session)

    async def get_dashboard(self, user: User) -> DashboardResponse:
        """Get complete dashboard data with mock fallbacks."""
        credit_score = await self._get_credit_score_breakdown(user)
        financial_summary = await self._get_financial_summary(user)
        recent_predictions = await self._get_recent_predictions(user)
        active_recommendations = await self.recommendations.count_active_by_user(user.id)

        return DashboardResponse(
            user_id=str(user.id),
            credit_score=credit_score,
            financial_summary=financial_summary,
            recent_predictions=recent_predictions,
            active_recommendations=active_recommendations,
            last_updated=datetime.now(UTC),
        )

    async def _get_credit_score_breakdown(self, user: User) -> CreditScoreBreakdown:
        """Get credit score breakdown with mock fallback."""
        score_record = await self.credit_scores.get_latest_by_user(user.id)
        if score_record:
            components = score_record.score_components
            return CreditScoreBreakdown(
                income_stability=Decimal(str(components.get("income_stability", 200))),
                spending_patterns=Decimal(str(components.get("spending_patterns", 200))),
                account_activity=Decimal(str(components.get("account_activity", 200))),
                payment_consistency=Decimal(str(components.get("payment_consistency", 200))),
                overall_score=score_record.score,
            )
        # Mock data until ML integration
        return CreditScoreBreakdown(
            income_stability=Decimal("215"),
            spending_patterns=Decimal("198"),
            account_activity=Decimal("205"),
            payment_consistency=Decimal("212"),
            overall_score=Decimal("830"),
        )

    async def _get_financial_summary(self, user: User) -> FinancialSummary:
        """Get financial summary with real transaction data where available."""
        transactions = await self.transactions.get_by_user(user.id, limit=1000)
        bank_connections = await self.bank_connections.get_by_user(user.id)

        if transactions:
            credits = [t.amount for t in transactions if t.transaction_type == "credit"]
            debits = [t.amount for t in transactions if t.transaction_type == "debit"]
            total_credits = sum(credits, Decimal("0"))
            total_debits = sum(debits, Decimal("0"))
            transaction_count = len(transactions)
        else:
            # Mock data
            total_credits = Decimal("85000.00")
            total_debits = Decimal("62340.50")
            transaction_count = 45

        # Calculate averages (mock for now)
        average_monthly_income = total_credits / Decimal("3") if total_credits > 0 else Decimal("0")
        average_monthly_spending = total_debits / Decimal("3") if total_debits > 0 else Decimal("0")

        # Calculate savings rate
        savings_rate = (
            ((total_credits - total_debits) / total_credits * Decimal("100")).quantize(Decimal("0.01"))
            if total_credits > 0
            else Decimal("0")
        )

        # Determine period
        if transactions:
            dates = [t.occurred_at for t in transactions]
            period_start = min(dates)
            period_end = max(dates)
        else:
            period_end = datetime.now(UTC)
            period_start = period_end - timedelta(days=90)

        return FinancialSummary(
            total_transactions=transaction_count,
            total_credits=total_credits,
            total_debits=total_debits,
            average_monthly_income=average_monthly_income,
            average_monthly_spending=average_monthly_spending,
            savings_rate=savings_rate,
            active_banks=len([bc for bc in bank_connections if bc.connection_status == "active"]),
            period_start=period_start,
            period_end=period_end,
        )

    async def _get_recent_predictions(self, user: User) -> list[Prediction]:
        """Get recent predictions with mock fallback."""
        prediction_records = await self.predictions.get_by_user_id(user.id, limit=5)
        if prediction_records:
            return [
                Prediction(
                    id=str(p.id),
                    model_name=p.model_name,
                    model_version=p.model_version,
                    prediction_type=p.prediction_type,
                    prediction=p.prediction,
                    confidence=float(p.confidence) if p.confidence else None,
                    calculated_at=p.created_at,
                )
                for p in prediction_records
            ]
        # Mock predictions until ML integration
        return [
            Prediction(
                id="mock-pred-1",
                model_name="XGBoostCreditScorer",
                model_version="1.0.0",
                prediction_type="repayment_probability",
                prediction={"probability": 0.92, "risk_level": "low"},
                confidence=0.87,
                calculated_at=datetime.now(UTC) - timedelta(days=1),
            ),
            Prediction(
                id="mock-pred-2",
                model_name="XGBoostCreditScorer",
                model_version="1.0.0",
                prediction_type="credit_limit_recommendation",
                prediction={"recommended_limit": 250000, "currency": "INR"},
                confidence=0.82,
                calculated_at=datetime.now(UTC) - timedelta(days=7),
            ),
        ]

    async def get_financial_summary_only(self, user: User) -> FinancialSummary:
        """Get financial summary only."""
        return await self._get_financial_summary(user)

    async def get_predictions_only(self, user: User) -> list[Prediction]:
        """Get predictions only."""
        return await self._get_recent_predictions(user)
