from dataclasses import replace
from typing import Iterable

from app.schemas.preprocessing import CleanTransaction


class CategorizationService:
    """Deterministic, inspectable transaction categorization with no ML dependency."""

    _rules: tuple[tuple[str, tuple[str, ...]], ...] = (
        ("income", ("salary", "payroll", "interest", "refund")),
        ("housing", ("rent", "landlord", "housing", "maintenance")),
        ("groceries", ("grocery", "supermarket", "freshmart", "mart")),
        ("food_and_dining", ("restaurant", "cafe", "swiggy", "zomato", "food")),
        ("transport", ("uber", "ola", "metro", "fuel", "petrol", "diesel")),
        ("utilities", ("electricity", "water", "gas", "broadband", "mobile recharge")),
        ("healthcare", ("pharmacy", "hospital", "clinic", "medical")),
        ("shopping", ("amazon", "flipkart", "retail", "store")),
        ("finance", ("emi", "loan", "insurance", "credit card")),
    )

    def categorize(self, transactions: Iterable[CleanTransaction]) -> list[CleanTransaction]:
        return [self.categorize_one(transaction) for transaction in transactions]

    def categorize_one(self, transaction: CleanTransaction) -> CleanTransaction:
        if transaction.category and transaction.category not in {"unknown", "uncategorized"}:
            return transaction
        search_text = f"{transaction.merchant_name} {transaction.description}".lower()
        for category, keywords in self._rules:
            if any(keyword in search_text for keyword in keywords):
                return replace(transaction, category=category)
        return replace(transaction, category="uncategorized")
