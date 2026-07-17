"""Constants for the ML pipeline."""

# Feature categories
INCOME_FEATURES = [
    "average_monthly_income",
    "income_variance",
    "salary_consistency",
    "income_growth",
]

EXPENSE_FEATURES = [
    "monthly_expense",
    "savings_ratio",
    "expense_ratio",
    "grocery_ratio",
    "shopping_ratio",
    "travel_ratio",
    "healthcare_ratio",
    "entertainment_ratio",
    "insurance_ratio",
    "utility_ratio",
    "tax_ratio",
]

BEHAVIOUR_FEATURES = [
    "transaction_frequency",
    "average_transaction_value",
    "digital_payment_ratio",
    "cash_withdrawal_ratio",
    "recurring_payment_ratio",
    "expense_volatility",
    "balance_volatility",
    "minimum_balance",
    "maximum_balance",
    "average_balance",
]

DEBT_FEATURES = [
    "emi_ratio",
    "debt_to_income_ratio",
    "overdraft_frequency",
    "missed_emi_count",
]

# All feature names combined
FEATURE_NAMES = INCOME_FEATURES + EXPENSE_FEATURES + BEHAVIOUR_FEATURES + DEBT_FEATURES

# Transaction types
TRANSACTION_TYPES = ["Credit", "Debit"]

# Payment modes
PAYMENT_MODES = ["NEFT", "UPI", "IMPS", "Cash", "Card", "Cheque"]

# Categories
CATEGORIES = [
    "Salary",
    "EMI",
    "UPI",
    "Shopping",
    "Food",
    "Fuel",
    "Tax",
    "Grocery",
    "Travel",
    "Healthcare",
    "Entertainment",
    "Insurance",
    "Utility",
    "Transfer",
    "Withdrawal",
]

# Date format for parsing
DATE_FORMAT = "%Y-%m-%d"

# Default values for missing data
DEFAULT_NUMERIC_VALUE = 0.0
DEFAULT_STRING_VALUE = "unknown"

# Validation error messages
ERROR_DUPLICATE_TRANSACTIONS = "Duplicate transactions found"
ERROR_MISSING_VALUES = "Missing values detected"
ERROR_INVALID_DATES = "Invalid date format detected"
ERROR_INVALID_AMOUNTS = "Invalid transaction amounts detected"
ERROR_INVALID_CUSTOMER_IDS = "Invalid customer IDs detected"
