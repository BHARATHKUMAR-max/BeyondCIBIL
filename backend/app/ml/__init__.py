"""Machine-learning integration boundary; model adapters are intentionally not included."""

from app.ml.config import MLConfig
from app.ml.constants import (
    FEATURE_NAMES,
    INCOME_FEATURES,
    EXPENSE_FEATURES,
    BEHAVIOUR_FEATURES,
    DEBT_FEATURES,
)
from app.ml.dataset_loader import DatasetLoader
from app.ml.feature_engineering import FeatureEngineer
from app.ml.pipeline import MLPipeline
from app.ml.preprocessing import DataPreprocessor
from app.ml.validation import DataValidator

__all__ = [
    "MLConfig",
    "FEATURE_NAMES",
    "INCOME_FEATURES",
    "EXPENSE_FEATURES",
    "BEHAVIOUR_FEATURES",
    "DEBT_FEATURES",
    "DatasetLoader",
    "FeatureEngineer",
    "MLPipeline",
    "DataPreprocessor",
    "DataValidator",
]
