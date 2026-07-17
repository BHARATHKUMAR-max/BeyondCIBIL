"""Personalized recommendation engine for credit improvement."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Generates personalized recommendations based on SHAP feature contributions."""

    # Thresholds for feature-based recommendations
    SAVINGS_RATIO_LOW_THRESHOLD = 0.2
    SAVINGS_RATIO_GOOD_THRESHOLD = 0.4
    INCOME_LOW_THRESHOLD = 20000
    INCOME_GOOD_THRESHOLD = 40000
    EXPENSE_HIGH_RATIO = 0.8
    TRANSACTION_FREQUENCY_LOW = 0.5
    TRANSACTION_FREQUENCY_GOOD = 1.0
    INCOME_CONSISTENCY_LOW = 0.3
    INCOME_CONSISTENCY_GOOD = 0.5

    def __init__(self):
        """Initialize the recommendation engine."""
        self.recommendation_templates = self._load_recommendation_templates()

    def _load_recommendation_templates(self) -> dict[str, list[str]]:
        """
        Load recommendation templates for different scenarios.

        Returns:
            Dictionary mapping feature names to recommendation templates
        """
        return {
            "savings_ratio": {
                "low": [
                    "Increase your monthly savings to at least 20% of your income",
                    "Set up automatic transfers to a savings account",
                    "Reduce discretionary spending to boost savings rate",
                    "Create a budget to track and optimize savings"
                ],
                "medium": [
                    "Maintain consistent savings habits",
                    "Consider increasing savings rate gradually",
                    "Review and optimize your savings strategy"
                ],
                "negative_contribution": [
                    "Focus on maintaining consistent savings habits",
                    "Avoid irregular savings patterns",
                    "Build an emergency fund for stability"
                ]
            },
            "average_monthly_income": {
                "low": [
                    "Consider increasing income through additional sources",
                    "Explore freelance or part-time opportunities",
                    "Invest in skill development for higher-paying roles",
                    "Consider career advancement opportunities"
                ],
                "medium": [
                    "Maintain stable income patterns",
                    "Diversify income sources for stability",
                    "Plan for gradual income growth"
                ],
                "negative_contribution": [
                    "Maintain stable income patterns to improve creditworthiness",
                    "Avoid income volatility",
                    "Build consistent income streams"
                ]
            },
            "total_expense": {
                "high": [
                    "Reduce unnecessary expenses to improve savings ratio",
                    "Review and cut recurring subscriptions",
                    "Implement the 50/30/20 budgeting rule",
                    "Track expenses to identify reduction opportunities"
                ],
                "medium": [
                    "Monitor and control spending patterns",
                    "Review monthly expenses regularly",
                    "Optimize spending without reducing quality of life"
                ],
                "negative_contribution": [
                    "Monitor and control spending patterns",
                    "Avoid unnecessary large expenses",
                    "Maintain consistent spending habits"
                ]
            },
            "transaction_frequency": {
                "low": [
                    "Increase digital transaction activity for better financial tracking",
                    "Use digital payment methods for regular purchases",
                    "Build transaction history for better credit assessment",
                    "Maintain consistent transaction patterns"
                ],
                "medium": [
                    "Maintain consistent transaction patterns",
                    "Use digital payments for better tracking",
                    "Build regular transaction history"
                ],
                "negative_contribution": [
                    "Maintain consistent transaction patterns",
                    "Avoid irregular transaction activity",
                    "Build stable financial behavior patterns"
                ]
            },
            "income_consistency": {
                "low": [
                    "Work on improving income and savings consistency",
                    "Maintain regular income patterns",
                    "Build stable financial habits",
                    "Avoid income volatility"
                ],
                "medium": [
                    "Focus on maintaining stable financial behavior",
                    "Maintain consistent income and savings patterns",
                    "Build financial discipline"
                ],
                "negative_contribution": [
                    "Focus on maintaining stable financial behavior",
                    "Avoid inconsistent financial patterns",
                    "Build regular financial habits"
                ]
            }
        }

    def generate_recommendations(
        self,
        features: dict[str, float],
        shap_contributions: dict[str, float]
    ) -> list[str]:
        """
        Generate personalized recommendations based on features and SHAP values.

        Args:
            features: Dictionary of feature names to values
            shap_contributions: Dictionary of feature names to SHAP contribution values

        Returns:
            List of personalized recommendation strings
        """
        recommendations = []

        # Generate recommendations for each feature
        for feature_name, feature_value in features.items():
            contribution = shap_contributions.get(feature_name, 0)
            feature_recommendations = self._generate_feature_recommendations(
                feature_name, feature_value, contribution
            )
            recommendations.extend(feature_recommendations)

        # Prioritize recommendations based on SHAP contribution magnitude
        prioritized_recommendations = self._prioritize_recommendations(
            recommendations, shap_contributions
        )

        # Remove duplicates and limit to top 5
        unique_recommendations = list(dict.fromkeys(prioritized_recommendations))
        return unique_recommendations[:5]

    def _generate_feature_recommendations(
        self,
        feature_name: str,
        feature_value: float,
        contribution: float
    ) -> list[str]:
        """
        Generate recommendations for a specific feature.

        Args:
            feature_name: Name of the feature
            feature_value: Value of the feature
            contribution: SHAP contribution值

        Returns:
            List of recommendation strings for this feature
        """
        templates = self.recommendation_templates.get(feature_name, {})
        recommendations = []

        # Determine feature status
        if contribution < -0.05:
            # Negative contribution - feature is hurting the score
            recommendations.extend(templates.get("negative_contribution", []))
        elif feature_name == "savings_ratio":
            if feature_value < self.SAVINGS_RATIO_LOW_THRESHOLD:
                recommendations.extend(templates.get("low", []))
            elif feature_value < self.SAVINGS_RATIO_GOOD_THRESHOLD:
                recommendations.extend(templates.get("medium", []))
        elif feature_name == "average_monthly_income":
            if feature_value < self.INCOME_LOW_THRESHOLD:
                recommendations.extend(templates.get("low", []))
            elif feature_value < self.INCOME_GOOD_THRESHOLD:
                recommendations.extend(templates.get("medium", []))
        elif feature_name == "total_expense":
            # Need to compare with income for expense ratio
            income = features.get("average_monthly_income", 1)
            if income > 0 and (feature_value / income) > self.EXPENSE_HIGH_RATIO:
                recommendations.extend(templates.get("high", []))
            else:
                recommendations.extend(templates.get("medium", []))
        elif feature_name == "transaction_frequency":
            if feature_value < self.TRANSACTION_FREQUENCY_LOW:
                recommendations.extend(templates.get("low", []))
            elif feature_value < self.TRANSACTION_FREQUENCY_GOOD:
                recommendations.extend(templates.get("medium", []))
        elif feature_name == "income_consistency":
            if feature_value < self.INCOME_CONSISTENCY_LOW:
                recommendations.extend(templates.get("low", []))
            elif feature_value < self.INCOME_CONSISTENCY_GOOD:
                recommendations.extend(templates.get("medium", []))

        return recommendations

    def _prioritize_recommendations(
        self,
        recommendations: list[str],
        shap_contributions: dict[str, float]
    ) -> list[str]:
        """
        Prioritize recommendations based on SHAP contribution magnitude.

        Args:
            recommendations: List of recommendation strings
            shap_contributions: Dictionary of feature names to SHAP values

        Returns:
            Prioritized list of recommendations
        """
        # Sort features by absolute contribution magnitude
        sorted_features = sorted(
            shap_contributions.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )

        # Reorder recommendations based on feature priority
        prioritized = []
        used_recommendations = set()

        for feature_name, _ in sorted_features:
            for recommendation in recommendations:
                # Check if recommendation is related to this feature
                if self._is_recommendation_for_feature(recommendation, feature_name):
                    if recommendation not in used_recommendations:
                        prioritized.append(recommendation)
                        used_recommendations.add(recommendation)

        # Add any remaining recommendations
        for recommendation in recommendations:
            if recommendation not in used_recommendations:
                prioritized.append(recommendation)

        return prioritized

    def _is_recommendation_for_feature(self, recommendation: str, feature_name: str) -> bool:
        """
        Check if a recommendation is related to a specific feature.

        Args:
            recommendation: Recommendation string
            feature_name: Feature name to check against

        Returns:
            True if recommendation is related to the feature
        """
        feature_keywords = {
            "savings_ratio": ["savings", "save", "budget"],
            "average_monthly_income": ["income", "earn", "salary", "freelance"],
            "total_expense": ["expense", "spending", "cost", "subscription"],
            "transaction_frequency": ["transaction", "payment", "digital"],
            "income_consistency": ["consistent", "stable", "pattern", "habit"]
        }

        keywords = feature_keywords.get(feature_name, [])
        recommendation_lower = recommendation.lower()

        return any(keyword in recommendation_lower for keyword in keywords)

    def get_recommendation_priority(self, recommendation: str) -> int:
        """
        Get priority level for a recommendation.

        Args:
            recommendation: Recommendation string

        Returns:
            Priority level (1=high, 2=medium, 3=low)
        """
        high_priority_keywords = ["increase", "reduce", "improve", "build", "create"]
        medium_priority_keywords = ["maintain", "monitor", "review", "consider"]
        low_priority_keywords = ["optimize", "explore", "plan"]

        recommendation_lower = recommendation.lower()

        if any(keyword in recommendation_lower for keyword in high_priority_keywords):
            return 1
        elif any(keyword in recommendation_lower for keyword in medium_priority_keywords):
            return 2
        else:
            return 3

    def generate_actionable_insights(
        self,
        features: dict[str, float],
        shap_contributions: dict[str, float],
        credit_score: int
    ) -> dict[str, Any]:
        """
        Generate actionable insights for credit improvement.

        Args:
            features: Dictionary of feature names to values
            shap_contributions: Dictionary of feature names to SHAP values
            credit_score: Current credit score

        Returns:
            Dictionary with actionable insights
        """
        recommendations = self.generate_recommendations(features, shap_contributions)

        # Identify top positive and negative factors
        sorted_contributions = sorted(
            shap_contributions.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top_positive = sorted_contributions[:2]
        top_negative = sorted_contributions[-2:]

        return {
            "current_score": credit_score,
            "recommendations": recommendations,
            "top_strengths": [
                {"feature": f[0], "impact": f[1]} for f in top_positive if f[1] > 0
            ],
            "areas_for_improvement": [
                {"feature": f[0], "impact": f[1]} for f in top_negative if f[1] < 0
            ],
            "quick_wins": [r for r in recommendations if self.get_recommendation_priority(r) == 1],
            "long_term_goals": [r for r in recommendations if self.get_recommendation_priority(r) == 3]
        }


# Global recommendation engine instance
_recommendation_engine: RecommendationEngine | None = None


def get_recommendation_engine() -> RecommendationEngine:
    """
    Get or create the global recommendation engine instance.

    Returns:
        RecommendationEngine instance
    """
    global _recommendation_engine
    if _recommendation_engine is None:
        _recommendation_engine = RecommendationEngine()
    return _recommendation_engine


__all__ = ["RecommendationEngine", "get_recommendation_engine"]
