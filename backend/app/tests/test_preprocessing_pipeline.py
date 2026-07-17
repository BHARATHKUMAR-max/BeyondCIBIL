from decimal import Decimal

from app.schemas.preprocessing import RawTransaction
from app.services.preprocessing_service import PreprocessingService


def test_pipeline_cleans_deduplicates_categorizes_and_prepares_features() -> None:
    records = [
        RawTransaction("txn-1", "1250.50", None, "debit", "10/07/2026", "UPI FRESHMART", "weekly groceries"),
        RawTransaction("txn-1", "1250.50", "INR", "debit", "10/07/2026", "UPI FRESHMART"),
        RawTransaction("txn-2", 85000, "inr", "credit", "2026-07-01T05:30:00Z", "ACME PAYROLL"),
        RawTransaction("txn-3", None, "INR", "debit", "2026-07-12", "Unknown"),
    ]

    result = PreprocessingService().process(records)

    assert len(result.transactions) == 2
    assert len(result.rejected) == 1
    assert result.transactions[0].merchant_name == "Freshmart"
    assert result.transactions[0].category == "groceries"
    assert result.features.total_debits == Decimal("1250.50")
    assert result.features.total_credits == Decimal("85000.00")


def test_pipeline_marks_large_debit_as_outlier() -> None:
    records = [
        RawTransaction(f"txn-{index}", amount, "INR", "debit", f"2026-07-{index:02d}", "Merchant")
        for index, amount in enumerate((100, 110, 120, 130, 5000), start=1)
    ]

    result = PreprocessingService().process(records)

    assert result.features.outlier_count == 1
    assert any(transaction.amount == Decimal("5000.00") and transaction.is_outlier for transaction in result.transactions)
