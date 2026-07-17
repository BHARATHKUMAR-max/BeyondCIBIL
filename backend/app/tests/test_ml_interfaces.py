from app.ml.contracts import (
    AttributionExplainer,
    FeatureAttribution,
    GeneratedRecommendation,
    PredictionInput,
    PredictionOutput,
    Predictor,
    RecommendationGenerator,
    RecommendationInput,
)
from app.ml.services import PredictionService, RecommendationService, ShapService


class StubPredictor:
    def predict(self, prediction_input: PredictionInput) -> PredictionOutput:
        return PredictionOutput(prediction={"score": 650}, model_version="stub-v1", confidence=0.8)


class StubExplainer:
    def explain(self, prediction_input: PredictionInput, prediction_output: PredictionOutput) -> list[FeatureAttribution]:
        return [FeatureAttribution(feature_name="income_stability", contribution=0.4)]


class StubRecommendationGenerator:
    def generate(self, recommendation_input: RecommendationInput) -> list[GeneratedRecommendation]:
        return [GeneratedRecommendation(category="savings", title="Build an emergency fund", description="Set aside funds monthly.", priority=2)]


def test_ml_services_depend_only_on_their_interfaces() -> None:
    prediction_input = PredictionInput(user_id="user-1", features={"income": 85000}, model_name="credit-score")
    predictor = StubPredictor()
    prediction = PredictionService(predictor).predict(prediction_input)

    assert isinstance(predictor, Predictor)
    assert isinstance(StubExplainer(), AttributionExplainer)
    assert isinstance(StubRecommendationGenerator(), RecommendationGenerator)
    assert ShapService(StubExplainer()).explain(prediction_input, prediction)[0].feature_name == "income_stability"
    assert RecommendationService(StubRecommendationGenerator()).generate(
        RecommendationInput(user_id="user-1", prediction=prediction, features=prediction_input.features)
    )[0].category == "savings"
