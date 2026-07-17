"""Confidence score calculation for prediction reliability."""

import numpy as np


class ConfidenceCalculator:
    """Calculates confidence scores for model predictions."""

    @staticmethod
    def calculate_confidence(probability: float) -> float:
        """
        Calculate confidence score based on prediction probability.

        Confidence is higher when the probability is closer to 0 or 1,
        indicating the model is more certain about its prediction.

        Formula: confidence = 2 * |probability - 0.5|

        Args:
            probability: Prediction probability between 0 and 1

        Returns:
            Confidence score between 0 and 1

        Raises:
            ValueError: If probability is not between 0 and 1
        """
        if not 0 <= probability <= 1:
            raise ValueError(f"Probability must be between 0 and 1, got {probability}")

        # Confidence is highest at extremes (0 or 1), lowest at 0.5
        confidence = 2 * abs(probability - 0.5)
        return round(confidence, 4)

    @staticmethod
    def get_confidence_level(confidence: float) -> str:
        """
        Get human-readable confidence level.

        Args:
            confidence: Confidence score between 0 and 1

        Returns:
            Confidence level string
        """
        if confidence >= 0.8:
            return "Very High"
        elif confidence >= 0.6:
            return "High"
        elif confidence >= 0.4:
            return "Medium"
        elif confidence >= 0.2:
            return "Low"
        else:
            return "Very Low"

    @staticmethod
    def get_confidence_color(confidence: float) -> str:
        """
        Get color code for confidence visualization.

        Args:
            confidence: Confidence score between 0 and 1

        Returns:
            Color hex code
        """
        if confidence >= 0.8:
            return "#10B981"  # Green
        elif confidence >= 0.6:
            return "#3B82F6"  # Blue
        elif confidence >= 0.4:
            return "#F59E0B"  # Yellow
        elif confidence >= 0.2:
            return "#F97316"  # Orange
        else:
            return "#EF4444"  # Red

    @staticmethod
    def calculate_prediction_stability(probabilities: list[float]) -> float:
        """
        Calculate prediction stability across multiple predictions.

        Stability is measured by the standard deviation of probabilities.
        Lower standard deviation indicates higher stability.

        Args:
            probabilities: List of prediction probabilities

        Returns:
            Stability score between 0 and 1 (higher = more stable)

        Raises:
            ValueError: If probabilities list is empty
        """
        if not probabilities:
            raise ValueError("Probabilities list cannot be empty")

        if len(probabilities) == 1:
            return 1.0  # Single prediction is perfectly stable

        std_dev = np.std(probabilities)
        # Convert standard deviation to stability score
        # Lower std_dev = higher stability
        stability = max(0, 1 - std_dev)
        return round(stability, 4)

    @staticmethod
    def calculate_ensemble_confidence(probabilities: list[float]) -> float:
        """
        Calculate confidence from ensemble predictions.

        Uses the variance of predictions to determine confidence.
        Lower variance indicates higher confidence.

        Args:
            probabilities: List of prediction probabilities from ensemble

        Returns:
            Confidence score between 0 and 1

        Raises:
            ValueError: If probabilities list is empty
        """
        if not probabilities:
            raise ValueError("Probabilities list cannot be empty")

        mean_prob = np.mean(probabilities)
        variance = np.var(probabilities)

        # Base confidence from mean probability
        base_confidence = ConfidenceCalculator.calculate_confidence(mean_prob)

        # Adjust confidence based on variance
        # Lower variance = higher confidence
        variance_penalty = min(variance * 2, 0.5)  # Cap penalty at 0.5
        ensemble_confidence = base_confidence - variance_penalty

        return round(max(0, min(1, ensemble_confidence)), 4)

    @staticmethod
    def is_prediction_reliable(confidence: float, threshold: float = 0.6) -> bool:
        """
        Determine if a prediction is reliable based on confidence.

        Args:
            confidence: Confidence score between 0 and 1
            threshold: Minimum confidence threshold (default: 0.6)

        Returns:
            True if prediction is reliable, False otherwise
        """
        return confidence >= threshold

    @staticmethod
    def get_confidence_description(confidence: float) -> str:
        """
        Get human-readable description for confidence score.

        Args:
            confidence: Confidence score between 0 and 1

        Returns:
            Description string
        """
        if confidence >= 0.8:
            return "Model is very confident in this prediction"
        elif confidence >= 0.6:
            return "Model is confident in this prediction"
        elif confidence >= 0.4:
            return "Model has moderate confidence in this prediction"
        elif confidence >= 0.2:
            return "Model has low confidence in this prediction"
        else:
            return "Model is uncertain about this prediction"
