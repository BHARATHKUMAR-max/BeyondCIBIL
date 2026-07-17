"""Dataset loading utilities for ML pipeline."""

import logging
from pathlib import Path
from typing import Any

import pandas as pd

from app.ml.config import ml_config
from app.ml.utils import setup_logging

logger = logging.getLogger(__name__)


class DatasetLoader:
    """Loads datasets from CSV files."""

    def __init__(self, config: Any = ml_config):
        """Initialize dataset loader with configuration."""
        self.config = config
        setup_logging(config.log_level)

    def load_transactions(self) -> pd.DataFrame:
        """Load transactions dataset from CSV."""
        path = self.config.get_dataset_path(self.config.transactions_file)
        logger.info(f"Loading transactions from {path}")
        
        if not path.exists():
            raise FileNotFoundError(f"Transactions file not found: {path}")
        
        df = pd.read_csv(path)
        logger.info(f"Loaded {len(df)} transactions")
        return df

    def load_customers(self) -> pd.DataFrame:
        """Load customers dataset from CSV."""
        path = self.config.get_dataset_path(self.config.customers_file)
        logger.info(f"Loading customers from {path}")
        
        if not path.exists():
            raise FileNotFoundError(f"Customers file not found: {path}")
        
        df = pd.read_csv(path)
        logger.info(f"Loaded {len(df)} customers")
        return df

    def load_features(self) -> pd.DataFrame:
        """Load features dataset from CSV."""
        path = self.config.get_dataset_path(self.config.features_file)
        logger.info(f"Loading features from {path}")
        
        if not path.exists():
            logger.warning(f"Features file not found: {path}. Returning empty DataFrame.")
            return pd.DataFrame()
        
        df = pd.read_csv(path)
        logger.info(f"Loaded {len(df)} feature records")
        return df

    def load_labels(self) -> pd.DataFrame:
        """Load labels dataset from CSV."""
        path = self.config.get_dataset_path(self.config.labels_file)
        logger.info(f"Loading labels from {path}")
        
        if not path.exists():
            logger.warning(f"Labels file not found: {path}. Returning empty DataFrame.")
            return pd.DataFrame()
        
        df = pd.read_csv(path)
        logger.info(f"Loaded {len(df)} label records")
        return df

    def load_all(self) -> dict[str, pd.DataFrame]:
        """Load all available datasets."""
        datasets = {
            "transactions": self.load_transactions(),
            "customers": self.load_customers(),
            "features": self.load_features(),
            "labels": self.load_labels(),
        }
        return datasets

    def load_transactions_for_customer(self, customer_id: str) -> pd.DataFrame:
        """Load transactions for a specific customer."""
        df = self.load_transactions()
        customer_transactions = df[df["customer_id"] == customer_id]
        logger.info(f"Loaded {len(customer_transactions)} transactions for customer {customer_id}")
        return customer_transactions

    def get_customer_ids(self) -> list[str]:
        """Get list of unique customer IDs from transactions."""
        df = self.load_transactions()
        return df["customer_id"].unique().tolist()

    def get_transaction_date_range(self) -> tuple[str, str]:
        """Get date range of transactions."""
        df = self.load_transactions()
        df["transaction_date"] = pd.to_datetime(df["transaction_date"])
        min_date = df["transaction_date"].min().strftime("%Y-%m-%d")
        max_date = df["transaction_date"].max().strftime("%Y-%m-%d")
        return min_date, max_date
