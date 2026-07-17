from datetime import UTC, datetime
from decimal import Decimal

from app.models.bank_connection import BankConnection
from app.services.transactions.contracts import SourceTransaction


class MockTransactionSource:
    """Static representative transactions for hackathon development only."""

    async def fetch_transactions(
        self, connection: BankConnection, since: datetime | None = None
    ) -> list[SourceTransaction]:
        account_key = str(connection.id)[:8]
        transactions = [
            SourceTransaction(
                external_transaction_id=f"mock-{account_key}-salary-jul",
                amount=Decimal("85000.00"),
                currency="INR",
                transaction_type="credit",
                category="income",
                merchant_name="Acme Technologies Pvt Ltd",
                description="Monthly salary credit",
                occurred_at=datetime(2026, 7, 1, 5, 30, tzinfo=UTC),
            ),
            SourceTransaction(
                external_transaction_id=f"mock-{account_key}-rent-jul",
                amount=Decimal("22000.00"),
                currency="INR",
                transaction_type="debit",
                category="housing",
                merchant_name="Greenwood Residences",
                description="Monthly rent payment",
                occurred_at=datetime(2026, 7, 5, 4, 15, tzinfo=UTC),
            ),
            SourceTransaction(
                external_transaction_id=f"mock-{account_key}-groceries-jul",
                amount=Decimal("1840.50"),
                currency="INR",
                transaction_type="debit",
                category="groceries",
                merchant_name="FreshMart",
                description="UPI grocery payment",
                occurred_at=datetime(2026, 7, 10, 13, 20, tzinfo=UTC),
            ),
        ]
        if since is None:
            return transactions
        return [transaction for transaction in transactions if transaction.occurred_at > since]
