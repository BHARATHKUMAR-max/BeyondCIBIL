"""Feature engineering for ML pipeline."""

import logging
from typing import Any

import numpy as np
import pandas as pd

from app.ml.config import ml_config
from app.ml.constants import (
    BEHAVIOUR_FEATURES,
    DEBT_FEATURES,
    EXPENSE_FEATURES,
    INCOME_FEATURES,
)
from app.ml.utils import (
    calculate_growth_rate,
    calculate_percentile_rank,
    calculate_volatility,
    safe_divide,
    safe_mean,
    safe_std,
)

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Engineers features from transaction data."""

    def __init__(self, config: Any = ml_config):
        """Initialize feature engineer with configuration."""
        self.config = config

    def engineer_features(self, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """Engineer all features for each customer."""
        logger.info("Engineering features for all customers")

        customer_ids = transactions_df["customer_id"].unique()
        feature_rows = []

        for customer_id in customer_ids:
            customer_transactions = transactions_df[transactions_df["customer_id"] == customer_id].copy()
            
            if len(customer_transactions) < self.config.min_transactions_for_features:
                logger.warning(f"Skipping customer {customer_id}: insufficient transactions")
                continue

            features = self._engineer_customer_features(customer_transactions, customer_id)
            feature_rows.append(features)

        feature_df = pd.DataFrame(feature_rows)
        logger.info(f"Engineered features for {len(feature_df)} customers")
        return feature_df

    def _engineer_customer_features(self, df: pd.DataFrame, customer_id: str) -> dict[str, float]:
        """Engineer features for a single customer."""
        df = df.copy()
        df["transaction_date"] = pd.to_datetime(df["transaction_date"])
        df = df.sort_values("transaction_date")

        features = {"customer_id": customer_id}

        # Income Features
        income_features = self._engineer_income_features(df)
        features.update(income_features)

        # Expense Features
        expense_features = self._engineer_expense_features(df)
        features.update(expense_features)

        # Behaviour Features
        behaviour_features = self._engineer_behaviour_features(df)
        features.update(behaviour_features)

        # Debt Features
        debt_features = self._engineer_debt_features(df)
        features.update(debt_features)

        return features

    def _engineer_income_features(self, df: pd.DataFrame) -> dict[str, float]:
        """Engineer income-related features."""
        credit_transactions = df[df["transaction_type"] == "Credit"]
        salary_transactions = df[df["category"] == "Salary"]

        features = {}

        # average_monthly_income
        if len(credit_transactions) > 0:
            total_income = credit_transactions["amount"].sum()
            date_range_days = (df["transaction_date"].max() - df["transaction_date"].min()).days
            if date_range_days > 0:
                features["average_monthly_income"] = (total_income / date_range_days) * 30
            else:
                features["average_monthly_income"] = total_income
        else:
            features["average_monthly_income"] = 0.0

        # income_variance
        if len(credit_transactions) > 1:
            features["income_variance"] = safe_std(credit_transactions["amount"])
        else:
            features["income_variance"] = 0.0

        # salary_consistency
        if len(salary_transactions) > 1:
            salary_amounts = salary_transactions["amount"]
            features["salary_consistency"] = 1.0 - (safe_std(salary_amounts) / safe_mean(salary_amounts))
        else:
            features["salary_consistency"] = 0.0

        # income_growth
        if len(credit_transactions) > 1:
            credit_transactions = credit_transactions.sort_values("transaction_date")
            first_income = credit_transactions.iloc[0]["amount"]
            last_income = credit_transactions.iloc[-1]["amount"]
            features["income_growth"] = calculate_growth_rate(last_income, first_income)
        else:
            features["income_growth"] = 0.0

        return features

    def _engineer_expense_features(self, df: pd.DataFrame) -> dict[str, float]:
        """Engineer expense-related features."""
        debit_transactions = df[df["transaction_type"] == "Debit"]
        total_income = df[df["transaction_type"] == "Credit"]["amount"].sum()

        features = {}

        # monthly_expense
        if len(debit_transactions) > 0:
            total_expense = debit_transactions["amount"].sum()
            date_range_days = (df["transaction_date"].max() - df["transaction_date"].min()).days
            if date_range_days > 0:
                features["monthly_expense"] = (total_expense / date_range_days) * 30
            else:
                features["monthly_expense"] = total_expense
        else:
            features["monthly_expense"] = 0.0

        # savings_ratio
        if total_income > 0:
            features["savings_ratio"] = safe_divide(total_income - debit_transactions["amount"].sum(), total_income)
        else:
            features["savings_ratio"] = 0.0

        # expense_ratio
        if total_income > 0:
            features["expense_ratio"] = safe_divide(debit_transactions["amount"].sum(), total_income)
        else:
            features["expense_ratio"] = 0.0

        # Category-specific ratios
        categories = ["Grocery", "Shopping", "Travel", "Healthcare", "Entertainment", "Insurance", "Utility", "Tax"]
        category_ratios = {
            "grocery_ratio": "Grocery",
            "shopping_ratio": "Shopping",
            "travel_ratio": "Travel",
            "healthcare_ratio": "Healthcare",
            "entertainment_ratio": "Entertainment",
            "insurance_ratio": "Insurance",
            "utility_ratio": "Utility",
            "tax_ratio": "Tax",
        }

        for feature_name, category in category_ratios.items():
            category_transactions = debit_transactions[debit_transactions["category"] == category]
            if total_income > 0:
                features[feature_name] = safe_divide(category_transactions["amount"].sum(), total_income)
            else:
                features[feature_name] = 0.0

        return features

    def _engineer_behaviour_features(self, df: pd.DataFrame) -> dict[str, float]:
        """Engineer behaviour-related features."""
        features = {}

        # transaction_frequency
        date_range_days = (df["transaction_date"].max() - df["transaction_date"].min()).days
        if date_range_days > 0:
            features["transaction_frequency"] = len(df) / date_range_days
        else:
            features["transaction_frequency"] = 0.0

        # average_transaction_value
        if len(df) > 0:
            features["average_transaction_value"] = safe_mean(df["amount"])
        else:
            features["average_transaction_value"] = 0.0

        # digital_payment_ratio
        digital_modes = ["UPI", "NEFT", "IMPS", "Card"]
        digital_transactions = df[df["payment_mode"].isin(digital_modes)]
        if len(df) > 0:
            features["digital_payment_ratio"] = len(digital_transactions) / len(df)
        else:
            features["digital_payment_ratio"] = 0.0

        # cash_withdrawal_ratio
        cash_transactions = df[df["payment_mode"] == "Cash"]
        if len(df) > 0:
            features["cash_withdrawal_ratio"] = len(cash_transactions) / len(df)
        else:
            features["cash_withdrawal_ratio"] = 0.0

        # recurring_payment_ratio
        recurring_transactions = df[df["is_recurring"] == True]
        if len(df) > 0:
            features["recurring_payment_ratio"] = len(recurring_transactions) / len(df)
        else:
            features["recurring_payment_ratio"] = 0.0

        # expense_volatility
        debit_transactions = df[df["transaction_type"] == "Debit"]
        if len(debit_transactions) > 1:
            features["expense_volatility"] = calculate_volatility(debit_transactions["amount"])
        else:
            features["expense_volatility"] = 0.0

        # balance_volatility
        if len(df) > 1:
            features["balance_volatility"] = calculate_volatility(df["balance_after"])
        else:
            features["balance_volatility"] = 0.0

        # minimum_balance
        if len(df) > 0:
            features["minimum_balance"] = df["balance_after"].min()
        else:
            features["minimum_balance"] = 0.0

        # maximum_balance
        if len(df) > 0:
            features["maximum_balance"] = df["balance_after"].max()
        else:
            features["maximum_balance"] = 0.0

        # average_balance
        if len(df) > 0:
            features["average_balance"] = safe_mean(df["balance_after"])
        else:
            features["average_balance"] = 0.0

        return features

    def _engineer_debt_features(self, df: pd.DataFrame) -> dict[str, float]:
        """Engineer debt-related features."""
        debit_transactions = df[df["transaction_type"] == "Debit"]
        total_income = df[df["transaction_type"] == "Credit"]["amount"].sum()

        features = {}

        # emi_ratio
        emi_transactions = debit_transactions[debit_transactions["category"] == "EMI"]
        if total_income > 0:
            features["emi_ratio"] = safe_divide(emi_transactions["amount"].sum(), total_income)
        else:
            features["emi_ratio"] = 0.0

        # debt_to_income_ratio
        debt_transactions = debit_transactions[debit_transactions["category"].isin(["EMI", "Loan"])]
        if total_income > 0:
            features["debt_to_income_ratio"] = safe_divide(debt_transactions["amount"].sum(), total_income)
        else:
            features["debt_to_income_ratio"] = 0.0

        # overdraft_frequency
        overdraft_transactions = debit_transactions[debit_transactions["balance_after"] < 0]
        if len(debit_transactions) > 0:
            features["overdraft_frequency"] = len(overdraft_transactions) / len(debit_transactions)
        else:
            features["overdraft_frequency"] = 0.0

        # missed_emi_count
        # Assuming EMI transactions should be monthly, we count gaps > 45 days between EMIs
        if len(emi_transactions) > 1:
            emi_transactions = emi_transactions.sort_values("transaction_date")
            emi_gaps = emi_transactions["transaction_date"].diff().dt.days
            missed_emi = (emi_gaps > 45).sum()
            features["missed_emi_count"] = missed_emi
        else:
            features["missed_emi_count"] = 0.0

        return features

    def get_feature_importance(self, feature_df: pd.DataFrame) -> dict[str, float]:
        """Calculate feature importance based on variance."""
        feature_cols = [col for col in feature_df.columns if col != "customer_id"]
        importance = {}

        for col in feature_cols:
            if col in feature_df.columns:
                variance = feature_df[col].var()
                importance[col] = variance if not pd.isna(variance) else 0.0

        # Normalize importance scores
        total_importance = sum(importance.values())
        if total_importance > 0:
            importance = {k: v / total_importance for k, v in importance.items()}

        return importance

    def select_features(
        self, feature_df: pd.DataFrame, top_n: int = 20, method: str = "variance"
    ) -> list[str]:
        """Select top features based on importance."""
        if method == "variance":
            importance = self.get_feature_importance(feature_df)
            sorted_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)
            return [feat for feat, _ in sorted_features[:top_n]]
        else:
            # Default to all feature names
            return INCOME_FEATURES + EXPENSE_FEATURES + BEHAVIOUR_FEATURES + DEBT_FEATURES
