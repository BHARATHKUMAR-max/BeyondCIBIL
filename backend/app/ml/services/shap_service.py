from app.ml.contracts import (
    AttributionExplainer,
    FeatureAttribution,
    PredictionInput,
    PredictionOutput,
)


class ShapService:
    """Delegates explanation generation to an injected SHAP-compatible adapter."""

    def __init__(self, explainer: AttributionExplainer) -> None:
        self.explainer = explainer

    def explain(
        self, prediction_input: PredictionInput, prediction_output: PredictionOutput
    ) -> list[FeatureAttribution]:
        return self.explainer.explain(prediction_input, prediction_output)
