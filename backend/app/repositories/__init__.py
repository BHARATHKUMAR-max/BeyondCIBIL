"""Persistence repository layer."""

from app.repositories.alternative_credit_score import AlternativeCreditScoreRepository
from app.repositories.base import BaseRepository
from app.repositories.feature_vector import FeatureVectorRepository
from app.repositories.prediction_history import PredictionHistoryRepository
from app.repositories.recommendation import RecommendationRepository

__all__ = [
    "BaseRepository",
    "AlternativeCreditScoreRepository",
    "PredictionHistoryRepository",
    "RecommendationRepository",
    "FeatureVectorRepository",
]
