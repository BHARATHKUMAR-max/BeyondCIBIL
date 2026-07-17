from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class PredictionInput:
    user_id: str
    features: dict[str, float | int | Decimal]
    model_name: str


@dataclass(frozen=True)
class PredictionOutput:
    prediction: dict[str, Any]
    model_version: str
    confidence: float | None = None


@dataclass(frozen=True)
class FeatureAttribution:
    feature_name: str
    contribution: float


@dataclass(frozen=True)
class RecommendationInput:
    user_id: str
    prediction: PredictionOutput
    features: dict[str, float | int | Decimal]


@dataclass(frozen=True)
class GeneratedRecommendation:
    category: str
    title: str
    description: str
    priority: int
    action_url: str | None = None


@runtime_checkable
class Predictor(Protocol):
    """Port implemented by a future trained model adapter."""

    def predict(self, prediction_input: PredictionInput) -> PredictionOutput: ...


@runtime_checkable
class AttributionExplainer(Protocol):
    """Port implemented by a future SHAP-compatible explainer adapter."""

    def explain(
        self, prediction_input: PredictionInput, prediction_output: PredictionOutput
    ) -> list[FeatureAttribution]: ...


@runtime_checkable
class RecommendationGenerator(Protocol):
    """Port implemented by a future rule-based or ML recommendation adapter."""

    def generate(self, recommendation_input: RecommendationInput) -> list[GeneratedRecommendation]: ...
