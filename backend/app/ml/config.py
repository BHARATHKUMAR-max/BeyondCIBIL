"""Configuration settings for the ML pipeline."""

from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class MLConfig(BaseSettings):
    """Configuration for machine learning pipeline."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Dataset paths
    dataset_root: Path = Field(default=Path("DATASET_BEYOND_CIBIL"), description="Root directory for datasets")
    customers_file: str = "customers.csv"
    transactions_file: str = "transactions.csv"
    features_file: str = "features.csv"
    labels_file: str = "labels.csv"

    # Artifact paths
    artifacts_dir: Path = Field(default=Path("app/ml/artifacts"), description="Directory for ML artifacts")

    # Feature engineering settings
    min_transactions_for_features: int = Field(default=3, description="Minimum transactions required for feature calculation")
    income_window_months: int = Field(default=6, description="Window in months for income calculations")
    expense_window_months: int = Field(default=6, description="Window in months for expense calculations")

    # Validation thresholds
    max_missing_ratio: float = Field(default=0.3, description="Maximum ratio of missing values allowed")
    min_transaction_amount: float = Field(default=0.01, description="Minimum valid transaction amount")
    max_transaction_amount: float = Field(default=10_000_000, description="Maximum valid transaction amount")

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO", description="Logging level")

    @field_validator("max_missing_ratio")
    @classmethod
    def validate_missing_ratio(cls, v: float) -> float:
        if not 0 <= v <= 1:
            raise ValueError("max_missing_ratio must be between 0 and 1")
        return v

    @field_validator("min_transaction_amount")
    @classmethod
    def validate_min_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("min_transaction_amount must be positive")
        return v

    @field_validator("max_transaction_amount")
    @classmethod
    def validate_max_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("max_transaction_amount must be positive")
        return v

    def get_dataset_path(self, filename: str) -> Path:
        """Get full path to a dataset file."""
        return self.dataset_root / filename


ml_config = MLConfig()
