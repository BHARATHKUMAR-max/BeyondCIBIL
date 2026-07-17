from app.ml.contracts import PredictionInput, PredictionOutput, Predictor


class PredictionService:
    """Delegates prediction requests to an injected model adapter."""

    def __init__(self, predictor: Predictor) -> None:
        self.predictor = predictor

    def predict(self, prediction_input: PredictionInput) -> PredictionOutput:
        return self.predictor.predict(prediction_input)
