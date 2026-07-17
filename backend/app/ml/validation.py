"""Data validation for ML pipeline datasets."""

import logging
from typing import Any

import pandas as pd

from app.ml.config import ml_config
from app.ml.constants import (
    ERROR_DUPLICATE_TRANSACTIONS,
    ERROR_INVALID_AMOUNTS,
    ERROR_INVALID_CUSTOMER_IDS,
    ERROR_INVALID_DATES,
    ERROR_MISSING_VALUES,
)
from app.ml.schemas import ValidationResult
from app.ml.utils import parse_date, validate_uuid

logger = logging.getLogger(__name__)


class DataValidator:
    """Validates dataset integrity and quality."""

    def __init__(self, config: Any = ml_config):
        """Initialize validator with configuration."""
        self.config = config

    def validate_transactions(self, df: pd.DataFrame) -> ValidationResult:
        """Validate transactions dataset."""
        errors = []
        warnings = []

        if df.empty:
            errors.append("Transactions dataframe is empty")
            return ValidationResult(is_valid=False, error_count=1, errors=errors)

        # Check required columns
        required_columns = [
            "transaction_id",
            "customer_id",
            "transaction_date",
            "amount",
            "transaction_type",
            "category",
            "merchant",
            "payment_mode",
            "balance_after",
            "description",
            "location",
            "is_recurring",
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {missing_columns}")
            return ValidationResult(is_valid=False, error_count=len(errors), errors=errors)

        # Check for duplicates
        duplicate_count = df.duplicated(subset=["transaction_id"]).sum()
        if duplicate_count > 0:
            errors.append(f"{ERROR_DUPLICATE_TRANSACTIONS}: {duplicate_count} duplicate transaction_id(s)")

        # Check for missing values
        missing_ratio = df.isnull().sum() / len(df)
        high_missing = missing_ratio[missing_ratio > self.config.max_missing_ratio]
        if not high_missing.empty:
            errors.append(f"{ERROR_MISSING_VALUES}: Columns with >{self.config.max_missing_ratio:.0%} missing: {high_missing.index.tolist()}")

        # Validate transaction amounts (allow negative for debits)
        invalid_amounts = df[
            (df["amount"].abs() < self.config.min_transaction_amount) | (df["amount"].abs() > self.config.max_transaction_amount)
        ]
        if not invalid_amounts.empty:
            errors.append(f"{ERROR_INVALID_AMOUNTS}: {len(invalid_amounts)} transactions with invalid amounts")

        # Validate dates
        invalid_dates = df[~df["transaction_date"].apply(lambda x: parse_date(str(x)) is not None)]
        if not invalid_dates.empty:
            errors.append(f"{ERROR_INVALID_DATES}: {len(invalid_dates)} transactions with invalid dates")

        # Validate customer IDs
        invalid_customer_ids = df[~df["customer_id"].apply(validate_uuid)]
        if not invalid_customer_ids.empty:
            errors.append(f"{ERROR_INVALID_CUSTOMER_IDS}: {len(invalid_customer_ids)} transactions with invalid customer IDs")

        # Validate transaction types
        invalid_types = df[~df["transaction_type"].isin(["Credit", "Debit"])]
        if not invalid_types.empty:
            warnings.append(f"{len(invalid_types)} transactions with invalid transaction_type")

        # Validate balance_after
        negative_balance = df[df["balance_after"] < 0]
        if not negative_balance.empty:
            warnings.append(f"{len(negative_balance)} transactions with negative balance_after")

        is_valid = len(errors) == 0
        return ValidationResult(
            is_valid=is_valid,
            error_count=len(errors),
            errors=errors,
            warnings=warnings,
        )

    def validate_customers(self, df: pd.DataFrame) -> ValidationResult:
        """Validate customers dataset."""
        errors = []
        warnings = []

        if df.empty:
            errors.append("Customers dataframe is empty")
            return ValidationResult(is_valid=False, error_count=1, errors=errors)

        # Check required columns (adapted to actual dataset structure)
        required_columns = ["customer_id"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {missing_columns}")
            return ValidationResult(is_valid=False, error_count=len(errors), errors=errors)

        # Check for duplicates
        duplicate_count = df.duplicated(subset=["customer_id"]).sum()
        if duplicate_count > 0:
            errors.append(f"Duplicate customer_id(s): {duplicate_count}")

        # Check for missing values
        missing_ratio = df.isnull().sum() / len(df)
        high_missing = missing_ratio[missing_ratio > self.config.max_missing_ratio]
        if not high_missing.empty:
            errors.append(f"Columns with >{self.config.max_missing_ratio:.0%} missing: {high_missing.index.tolist()}")

        # Validate customer IDs
        invalid_customer_ids = df[~df["customer_id"].apply(validate_uuid)]
        if not invalid_customer_ids.empty:
            errors.append(f"Invalid customer IDs: {len(invalid_customer_ids)}")

        # Validate email format (basic check)
        if "email" in df.columns:
            invalid_emails = df[~df["email"].str.contains("@", na=False)]
            if not invalid_emails.empty:
                warnings.append(f"Potentially invalid email addresses: {len(invalid_emails)}")

        # Validate dates
        if "registration_date" in df.columns:
            invalid_dates = df[~df["registration_date"].apply(lambda x: parse_date(str(x)) is not None)]
            if not invalid_dates.empty:
                errors.append(f"Invalid registration dates: {len(invalid_dates)}")

        is_valid = len(errors) == 0
        return ValidationResult(
            is_valid=is_valid,
            error_count=len(errors),
            errors=errors,
            warnings=warnings,
        )

    def validate_features(self, df: pd.DataFrame) -> ValidationResult:
        """Validate features dataset."""
        errors = []
        warnings = []

        if df.empty:
            errors.append("Features dataframe is empty")
            return ValidationResult(is_valid=False, error_count=1, errors=errors)

        # Check required columns
        if "customer_id" not in df.columns:
            errors.append("Missing required column: customer_id")
            return ValidationResult(is_valid=False, error_count=1, errors=errors)

        # Check for duplicates
        duplicate_count = df.duplicated(subset=["customer_id"]).sum()
        if duplicate_count > 0:
            errors.append(f"Duplicate customer_id(s): {duplicate_count}")

        # Check for missing values
        missing_ratio = df.isnull().sum() / len(df)
        high_missing = missing_ratio[missing_ratio > self.config.max_missing_ratio]
        if not high_missing.empty:
            errors.append(f"Columns with >{self.config.max_missing_ratio:.0%} missing: {high_missing.index.tolist()}")

        # Validate customer IDs
        invalid_customer_ids = df[~df["customer_id"].apply(validate_uuid)]
        if not invalid_customer_ids.empty:
            errors.append(f"Invalid customer IDs: {len(invalid_customer_ids)}")

        is_valid = len(errors) == 0
        return ValidationResult(
            is_valid=is_valid,
            error_count=len(errors),
            errors=errors,
            warnings=warnings,
        )

    def validate_labels(self, df: pd.DataFrame) -> ValidationResult:
        """Validate labels dataset."""
        errors = []
        warnings = []

        if df.empty:
            errors.append("Labels dataframe is empty")
            return ValidationResult(is_valid=False, error_count=1, errors=errors)

        # Check required columns
        required_columns = ["customer_id", "label"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {missing_columns}")
            return ValidationResult(is_valid=False, error_count=len(errors), errors=errors)

        # Check for duplicates
        duplicate_count = df.duplicated(subset=["customer_id"]).sum()
        if duplicate_count > 0:
            errors.append(f"Duplicate customer_id(s): {duplicate_count}")

        # Check for missing values
        missing_ratio = df.isnull().sum() / len(df)
        high_missing = missing_ratio[missing_ratio > self.config.max_missing_ratio]
        if not high_missing.empty:
            errors.append(f"Columns with >{self.config.max_missing_ratio:.0%} missing: {high_missing.index.tolist()}")

        # Validate customer IDs
        invalid_customer_ids = df[~df["customer_id"].apply(validate_uuid)]
        if not invalid_customer_ids.empty:
            errors.append(f"Invalid customer IDs: {len(invalid_customer_ids)}")

        # Validate label values (assuming binary or numeric labels)
        if "label" in df.columns:
            if df["label"].isnull().any():
                errors.append(f"Missing label values: {df['label'].isnull().sum()}")

        is_valid = len(errors) == 0
        return ValidationResult(
            is_valid=is_valid,
            error_count=len(errors),
            errors=errors,
            warnings=warnings,
        )
