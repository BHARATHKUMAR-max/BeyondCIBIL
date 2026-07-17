from app.ml.contracts import (
    GeneratedRecommendation,
    RecommendationGenerator,
    RecommendationInput,
)


class RecommendationService:
    """Delegates recommendation generation to an injected policy/model adapter."""

    def __init__(self, generator: RecommendationGenerator) -> None:
        self.generator = generator

    def generate(self, recommendation_input: RecommendationInput) -> list[GeneratedRecommendation]:
        return self.generator.generate(recommendation_input)
