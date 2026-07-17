from __future__ import annotations

from collections import defaultdict
from dataclasses import replace
from decimal import Decimal
from statistics import median
from typing import Iterable

from app.schemas.preprocessing import (
    CleanTransaction,
    PreprocessingResult,
    ProcessingFeatures,
    RawTransaction,
)
from app.services.categorization_service import CategorizationService
from app.services.cleaning_service import CleaningService


class PreprocessingService:
    """Orchestrates cleaning, categorization, validation, outlier marking, and feature preparation."""

    def __init__(
        self,
        cleaning_service: CleaningService | None = None,
        categorization_service: CategorizationService | None = None,
    ) -> None:
        self.cleaning_service = cleaning_service or CleaningService()
        self.categorization_service = categorization_service or CategorizationService()

    def process(self, records: Iterable[RawTransaction]) -> PreprocessingResult:
        cleaned, rejected = self.cleaning_service.clean(records)
        categorized = self.categorization_service.categorize(cleaned)
        validated, validation_rejections = self._validate(categorized)
        enriched = self._mark_outliers(validated)
        features = self.prepare_features(enriched)
        return PreprocessingResult(
            transactions=enriched,
            rejected=[*rejected, *validation_rejections],
            features=features,
            metadata={
                "accepted_count": len(enriched),
                "rejected_count": len(rejected) + len(validation_rejections),
                "outlier_count": sum(transaction.is_outlier for transaction in enriched),
            },
        )

    @staticmethod
    def _validate(transactions: list[CleanTransaction]) -> tuple[list[CleanTransaction], list]:
        # Cleaning performs field validation. This explicit stage is kept as the contract boundary
        # for future business validation rules without altering upstream services.
        return transactions, []

    def _mark_outliers(self, transactions: list[CleanTransaction]) -> list[CleanTransaction]:
        amounts_by_type: dict[str, list[Decimal]] = defaultdict(list)
        for transaction in transactions:
            amounts_by_type[transaction.transaction_type].append(transaction.amount)

        outlier_amounts: dict[str, set[Decimal]] = {}
        for transaction_type, amounts in amounts_by_type.items():
            if len(amounts) < 4:
                outlier_amounts[transaction_type] = set()
                continue
            center = median(amounts)
            deviations = [abs(amount - center) for amount in amounts]
            mad = median(deviations)
            if mad == 0:
                outlier_amounts[transaction_type] = set()
                continue
            outlier_amounts[transaction_type] = {
                amount for amount in amounts if Decimal("0.6745") * abs(amount - center) / mad > Decimal("3.5")
            }
        return [
            replace(transaction, is_outlier=transaction.amount in outlier_amounts[transaction.transaction_type])
            for transaction in transactions
        ]

    @staticmethod
    def prepare_features(transactions: list[CleanTransaction]) -> ProcessingFeatures:
        credits = [transaction.amount for transaction in transactions if transaction.transaction_type == "credit"]
        debits = [transaction.amount for transaction in transactions if transaction.transaction_type == "debit"]
        category_debits: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))
        for transaction in transactions:
            if transaction.transaction_type == "debit" and not transaction.is_outlier:
                category_debits[transaction.category or "uncategorized"] += transaction.amount
        ordered_dates = sorted(transaction.occurred_at for transaction in transactions)
        return ProcessingFeatures(
            transaction_count=len(transactions),
            credit_count=len(credits),
            debit_count=len(debits),
            total_credits=sum(credits, Decimal("0.00")),
            total_debits=sum(debits, Decimal("0.00")),
            average_debit=(sum(debits, Decimal("0.00")) / len(debits)).quantize(Decimal("0.01")) if debits else Decimal("0.00"),
            outlier_count=sum(transaction.is_outlier for transaction in transactions),
            category_debits=dict(category_debits),
            first_transaction_at=ordered_dates[0] if ordered_dates else None,
            last_transaction_at=ordered_dates[-1] if ordered_dates else None,
            active_days=len({transaction.occurred_at.date() for transaction in transactions}),
        )
