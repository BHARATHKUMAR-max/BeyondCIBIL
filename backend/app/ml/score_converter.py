"""Credit score conversion utilities for alternative credit scoring."""

from typing import Literal


class ScoreConverter:
    """Converts prediction probabilities to alternative credit scores (300-900)."""

    MIN_SCORE = 300
    MAX_SCORE = 900
    SCORE_RANGE = MAX_SCORE - MIN_SCORE

    @staticmethod
    def probability_to_score(probability: float) -> int:
        """
        Convert repayment probability to credit score.

        Maps probability (0-1) to credit score (300-900) using linear scaling.

        Args:
            probability: Repayment probability between 0 and 1

        Returns:
            Credit score between 300 and 900

        Raises:
            ValueError: If probability is not between 0 and 1
        """
        if not 0 <= probability <= 1:
            raise ValueError(f"Probability must be between 0 and 1, got {probability}")

        # Linear mapping: score = min_score + (probability * score_range)
        score = ScoreConverter.MIN_SCORE + (probability * ScoreConverter.SCORE_RANGE)
        return int(round(score))

    @staticmethod
    def score_to_probability(score: int) -> float:
        """
        Convert credit score back to repayment probability.

        Args:
            score: Credit score between 300 and 900

        Returns:
            Repayment probability between 0 and 1

        Raises:
            ValueError: If score is not between 300 and 900
        """
        if not ScoreConverter.MIN_SCORE <= score <= ScoreConverter.MAX_SCORE:
            raise ValueError(f"Score must be between {ScoreConverter.MIN_SCORE} and {ScoreConverter.MAX_SCORE}, got {score}")

        # Reverse linear mapping: probability = (score - min_score) / score_range
        probability = (score - ScoreConverter.MIN_SCORE) / ScoreConverter.SCORE_RANGE
        return round(probability, 4)

    @staticmethod
    def get_risk_category(score: int) -> str:
        """
        Convert credit score to risk category.

        Risk categories:
        - Very Low Risk: 750-900
        - Low Risk: 650-749
        - Medium Risk: 550-649
        - High Risk: 450-549
        - Very High Risk: 300-449

        Args:
            score: Credit score between 300 and 900

        Returns:
            Risk category string

        Raises:
            ValueError: If score is not between 300 and 900
        """
        if not ScoreConverter.MIN_SCORE <= score <= ScoreConverter.MAX_SCORE:
            raise ValueError(f"Score must be between {ScoreConverter.MIN_SCORE} and {ScoreConverter.MAX_SCORE}, got {score}")

        if score >= 750:
            return "Very Low Risk"
        elif score >= 650:
            return "Low Risk"
        elif score >= 550:
            return "Medium Risk"
        elif score >= 450:
            return "High Risk"
        else:
            return "Very High Risk"

    @staticmethod
    def get_risk_category_from_probability(probability: float) -> str:
        """
        Convert repayment probability directly to risk category.

        Args:
            probability: Repayment probability between 0 and 1

        Returns:
            Risk category string
        """
        score = ScoreConverter.probability_to_score(probability)
        return ScoreConverter.get_risk_category(score)

    @staticmethod
    def get_risk_level(category: str) -> int:
        """
        Get numeric risk level from category.

        Returns:
            Risk level (1=Very Low Risk, 5=Very High Risk)
        """
        risk_levels = {
            "Very Low Risk": 1,
            "Low Risk": 2,
            "Medium Risk": 3,
            "High Risk": 4,
            "Very High Risk": 5
        }
        return risk_levels.get(category, 3)  # Default to Medium Risk if unknown

    @staticmethod
    def get_score_description(score: int) -> str:
        """
        Get human-readable description for credit score.

        Args:
            score: Credit score between 300 and 900

        Returns:
            Description string
        """
        if score >= 750:
            return "Excellent - Very low risk of default"
        elif score >= 650:
            return "Good - Low risk of default"
        elif score >= 550:
            return "Fair - Moderate risk of default"
        elif score >= 450:
            return "Poor - High risk of default"
        else:
            return "Very Poor - Very high risk of default"

    @staticmethod
    def get_score_color(score: int) -> str:
        """
        Get color code for credit score visualization.

        Args:
            score: Credit score between 300 and 900

        Returns:
            Color hex code
        """
        if score >= 750:
            return "#10B981"  # Green
        elif score >= 650:
            return "#3B82F6"  # Blue
        elif score >= 550:
            return "#F59E0B"  # Yellow
        elif score >= 450:
            return "#F97316"  # Orange
        else:
            return "#EF4444"  # Red
