"""Utility functions for the ML pipeline."""

import logging
from datetime import datetime
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def setup_logging(log_level: str = "INFO") -> None:
    """Configure logging for the ML pipeline."""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def safe_divide(numerator: float | pd.Series, denominator: float | pd.Series, default: float = 0.0) -> float | pd.Series:
    """Safely divide two values, returning default on division by zero."""
    if isinstance(numerator, pd.Series) or isinstance(denominator, pd.Series):
        result = numerator / denominator
        result.replace([np.inf, -np.inf], default, inplace=True)
        result.fillna(default, inplace=True)
        return result
    if denominator == 0:
        return default
    return numerator / denominator


def calculate_volatility(values: pd.Series, window: int = 6) -> float:
    """Calculate volatility (standard deviation) of values over a window."""
    if len(values) < 2:
        return 0.0
    return float(values.std())


def calculate_growth_rate(current: float, previous: float) -> float:
    """Calculate percentage growth rate between two values."""
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100


def parse_date(date_str: str, date_format: str = "%Y-%m-%d") -> datetime | None:
    """Parse date string to datetime object."""
    try:
        return datetime.strptime(date_str, date_format)
    except (ValueError, TypeError):
        return None


def validate_uuid(uuid_str: str) -> bool:
    """Validate if string is a valid UUID format."""
    import uuid as uuid_module

    try:
        uuid_module.UUID(uuid_str)
        return True
    except (ValueError, AttributeError):
        return False


def calculate_percentile_rank(value: float, series: pd.Series) -> float:
    """Calculate percentile rank of a value within a series."""
    if len(series) == 0:
        return 0.0
    return float((series < value).sum() / len(series) * 100)


def normalize_series(series: pd.Series, method: str = "minmax") -> pd.Series:
    """Normalize a series using specified method."""
    if method == "minmax":
        min_val = series.min()
        max_val = series.max()
        if max_val == min_val:
            return pd.Series([0.0] * len(series), index=series.index)
        return (series - min_val) / (max_val - min_val)
    elif method == "zscore":
        mean_val = series.mean()
        std_val = series.std()
        if std_val == 0:
            return pd.Series([0.0] * len(series), index=series.index)
        return (series - mean_val) / std_val
    else:
        raise ValueError(f"Unknown normalization method: {method}")


def detect_outliers_iqr(series: pd.Series, multiplier: float = 1.5) -> pd.Series:
    """Detect outliers using IQR method."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr
    return (series < lower_bound) | (series > upper_bound)


def safe_mean(values: pd.Series) -> float:
    """Calculate mean safely, handling empty series."""
    if len(values) == 0 or values.isna().all():
        return 0.0
    return float(values.mean())


def safe_std(values: pd.Series) -> float:
    """Calculate standard deviation safely, handling empty series."""
    if len(values) < 2 or values.isna().all():
        return 0.0
    return float(values.std())


def format_feature_dict(features: dict[str, float]) -> dict[str, Any]:
    """Format feature dictionary for storage, handling NaN and infinite values."""
    formatted = {}
    for key, value in features.items():
        if pd.isna(value) or np.isinf(value):
            formatted[key] = 0.0
        else:
            formatted[key] = float(value)
    return formatted
