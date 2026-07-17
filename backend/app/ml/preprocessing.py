"""Data preprocessing for ML pipeline."""

import logging
from typing import Any

import numpy as np
import pandas as pd

from app.ml.config import ml_config
from app.ml.constants import (
    CATEGORIES,
    DEFAULT_NUMERIC_VALUE,
    DEFAULT_STRING_VALUE,
    PAYMENT_MODES,
    TRANSACTION_TYPES,
)
from app.ml.utils import parse_date

logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Preprocesses and cleans transaction data."""

    def __init__(self, config: Any = ml_config):
        """Initialize preprocessor with configuration."""
        self.config = config

    def clean_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess transactions dataframe."""
        logger.info("Cleaning transactions data")
        df_cleaned = df.copy()

        # Convert date column to datetime
        df_cleaned["transaction_date"] = pd.to_datetime(df_cleaned["transaction_date"], errors="coerce")

        # Handle missing values
        df_cleaned = self._handle_missing_values(df_cleaned)

        # Normalize transaction types
        df_cleaned["transaction_type"] = df_cleaned["transaction_type"].str.strip().str.title()
        df_cleaned["transaction_type"] = df_cleaned["transaction_type"].apply(
            lambda x: x if x in TRANSACTION_TYPES else "Debit"
        )

        # Normalize payment modes
        df_cleaned["payment_mode"] = df_cleaned["payment_mode"].str.strip().str.title()
        df_cleaned["payment_mode"] = df_cleaned["payment_mode"].apply(
            lambda x: x if x in PAYMENT_MODES else DEFAULT_STRING_VALUE
        )

        # Normalize categories
        df_cleaned["category"] = df_cleaned["category"].str.strip().str.title()
        df_cleaned["category"] = df_cleaned["category"].apply(
            lambda x: x if x in CATEGORIES else DEFAULT_STRING_VALUE
        )

        # Normalize merchant names
        df_cleaned["merchant"] = df_cleaned["merchant"].str.strip().str.title()

        # Normalize location
        df_cleaned["location"] = df_cleaned["location"].str.strip().str.title()

        # Normalize description
        df_cleaned["description"] = df_cleaned["description"].str.strip()

        # Convert is_recurring to boolean
        df_cleaned["is_recurring"] = df_cleaned["is_recurring"].astype(bool)

        # Remove duplicates
        initial_count = len(df_cleaned)
        df_cleaned = df_cleaned.drop_duplicates(subset=["transaction_id"])
        duplicates_removed = initial_count - len(df_cleaned)
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate transactions")

        # Sort by date
        df_cleaned = df_cleaned.sort_values("transaction_date")

        # Reset index
        df_cleaned = df_cleaned.reset_index(drop=True)

        logger.info(f"Cleaned transactions: {len(df_cleaned)} records")
        return df_cleaned

    def clean_customers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess customers dataframe."""
        logger.info("Cleaning customers data")
        df_cleaned = df.copy()

        # Convert date column to datetime
        if "registration_date" in df_cleaned.columns:
            df_cleaned["registration_date"] = pd.to_datetime(df_cleaned["registration_date"], errors="coerce")

        # Handle missing values
        df_cleaned = self._handle_missing_values(df_cleaned)

        # Normalize string columns
        string_columns = ["name", "email", "phone", "address"]
        for col in string_columns:
            if col in df_cleaned.columns:
                df_cleaned[col] = df_cleaned[col].str.strip()

        # Remove duplicates
        initial_count = len(df_cleaned)
        df_cleaned = df_cleaned.drop_duplicates(subset=["customer_id"])
        duplicates_removed = initial_count - len(df_cleaned)
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate customers")

        logger.info(f"Cleaned customers: {len(df_cleaned)} records")
        return df_cleaned

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in dataframe."""
        df_cleaned = df.copy()

        # For numeric columns, fill with default value
        numeric_columns = df_cleaned.select_dtypes(include=[np.number]).columns
        df_cleaned[numeric_columns] = df_cleaned[numeric_columns].fillna(DEFAULT_NUMERIC_VALUE)

        # For string columns, fill with default value
        string_columns = df_cleaned.select_dtypes(include=["object"]).columns
        df_cleaned[string_columns] = df_cleaned[string_columns].fillna(DEFAULT_STRING_VALUE)

        return df_cleaned

    def filter_by_date_range(
        self, df: pd.DataFrame, start_date: str | None = None, end_date: str | None = None
    ) -> pd.DataFrame:
        """Filter transactions by date range."""
        if start_date is None and end_date is None:
            return df

        df_filtered = df.copy()
        df_filtered["transaction_date"] = pd.to_datetime(df_filtered["transaction_date"])

        if start_date:
            start_dt = pd.to_datetime(start_date)
            df_filtered = df_filtered[df_filtered["transaction_date"] >= start_dt]

        if end_date:
            end_dt = pd.to_datetime(end_date)
            df_filtered = df_filtered[df_filtered["transaction_date"] <= end_dt]

        logger.info(f"Filtered to {len(df_filtered)} transactions in date range")
        return df_filtered

    def filter_by_customer(self, df: pd.DataFrame, customer_ids: list[str]) -> pd.DataFrame:
        """Filter transactions by customer IDs."""
        df_filtered = df[df["customer_id"].isin(customer_ids)]
        logger.info(f"Filtered to {len(df_filtered)} transactions for {len(customer_ids)} customers")
        return df_filtered

    def remove_outliers(self, df: pd.DataFrame, column: str = "amount", method: str = "iqr") -> pd.DataFrame:
        """Remove outliers from specified column."""
        df_cleaned = df.copy()

        if method == "iqr":
            q1 = df_cleaned[column].quantile(0.25)
            q3 = df_cleaned[column].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            df_cleaned = df_cleaned[(df_cleaned[column] >= lower_bound) & (df_cleaned[column] <= upper_bound)]
        elif method == "zscore":
            mean = df_cleaned[column].mean()
            std = df_cleaned[column].std()
            z_scores = np.abs((df_cleaned[column] - mean) / std)
            df_cleaned = df_cleaned[z_scores < 3]

        outliers_removed = len(df) - len(df_cleaned)
        if outliers_removed > 0:
            logger.info(f"Removed {outliers_removed} outliers from {column}")

        return df_cleaned

    def aggregate_by_customer(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate transactions by customer."""
        agg_df = (
            df.groupby("customer_id")
            .agg(
                transaction_count=("transaction_id", "count"),
                total_credits=("amount", lambda x: x[df.loc[x.index, "transaction_type"] == "Credit"].sum()),
                total_debits=("amount", lambda x: x[df.loc[x.index, "transaction_type"] == "Debit"].sum()),
                avg_transaction_amount=("amount", "mean"),
                max_transaction_amount=("amount", "max"),
                min_transaction_amount=("amount", "min"),
                first_transaction=("transaction_date", "min"),
                last_transaction=("transaction_date", "max"),
            )
            .reset_index()
        )

        logger.info(f"Aggregated to {len(agg_df)} customers")
        return agg_df

    def add_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add temporal features to transactions."""
        df_enhanced = df.copy()
        df_enhanced["transaction_date"] = pd.to_datetime(df_enhanced["transaction_date"])

        df_enhanced["year"] = df_enhanced["transaction_date"].dt.year
        df_enhanced["month"] = df_enhanced["transaction_date"].dt.month
        df_enhanced["day"] = df_enhanced["transaction_date"].dt.day
        df_enhanced["day_of_week"] = df_enhanced["transaction_date"].dt.dayofweek
        df_enhanced["is_weekend"] = df_enhanced["day_of_week"].isin([5, 6]).astype(int)
        df_enhanced["is_month_start"] = df_enhanced["day"] <= 5
        df_enhanced["is_month_end"] = df_enhanced["day"] >= 25

        logger.info("Added temporal features")
        return df_enhanced
