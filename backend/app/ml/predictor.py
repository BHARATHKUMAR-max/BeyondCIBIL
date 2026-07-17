"""Production-ready ML prediction service for alternative credit scoring."""

import joblib
import logging
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Any

from app.ml.confidence import ConfidenceCalculator
from app.ml.prediction_schema import PredictionRequest, PredictionResponse
from app.ml.score_converter import ScoreConverter
from app.ml.config import ml_config

logger = logging.getLogger(__name__)


class PredictionService:
    """Production-ready prediction service for alternative credit scoring."""

    MODEL_VERSION = "1.0"
    REQUIRED_FEATURES = [
        "savings_ratio",
        "average_monthly_income",
        "income_consistency",
        "total_expense",
        "transaction_frequency"
    ]

    def __init__(self):
        """Initialize the prediction service by loading all artifacts."""
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.shap_explainer = None
        self._load_artifacts()

    def _load_artifacts(self) -> None:
        """Load all ML artifacts from disk."""
        try:
            logger.info("Loading ML artifacts...")
            
            # Load model
            model_path = ml_config.artifacts_dir / "model.pkl"
            self.model = joblib.load(model_path)
            logger.info(f"Model loaded from {model_path}")

            # Load scaler
            scaler_path = ml_config.artifacts_dir / "scaler.pkl"
            self.scaler = joblib.load(scaler_path)
            logger.info(f"Scaler loaded from {scaler_path}")

            # Load feature columns
            feature_columns_path = ml_config.artifacts_dir / "feature_columns.pkl"
            self.feature_columns = joblib.load(feature_columns_path)
            logger.info(f"Feature columns loaded from {feature_columns_path}")

            # Load SHAP explainer (optional)
            shap_path = ml_config.artifacts_dir / "shap_explainer.pkl"
            try:
                self.shap_explainer = joblib.load(shap_path)
                logger.info(f"SHAP explainer loaded from {shap_path}")
            except Exception as e:
                logger.warning(f"SHAP explainer could not be loaded: {e}. SHAP explanations will be disabled.")
                self.shap_explainer = None

            logger.info("All ML artifacts loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load ML artifacts: {e}")
            raise RuntimeError(f"Failed to load ML artifacts: {e}")

    def _validate_features(self, features: dict[str, float]) -> None:
        """
        Validate that all required features are present and valid.

        Args:
            features: Dictionary of feature names to values

        Raises:
            ValueError: If features are missing or invalid
        """
        missing_features = set(self.REQUIRED_FEATURES) - set(features.keys())
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")

        # Validate feature values
        for feature_name, value in features.items():
            if not isinstance(value, (int, float)):
                raise ValueError(f"Feature {feature_name} must be numeric, got {type(value)}")
            if np.isnan(value) or np.isinf(value):
                raise ValueError(f"Feature {feature_name} contains invalid value: {value}")

    def _prepare_feature_vector(self, features: dict[str, float]) -> np.ndarray:
        """
        Prepare feature vector for prediction.

        Ensures features are in the correct order and scaled.

        Args:
            features: Dictionary of feature names to values

        Returns:
            Scaled feature vector as numpy array
        """
        # Ensure features are in the correct order
        ordered_features = [features[feature] for feature in self.feature_columns]
        feature_array = np.array(ordered_features).reshape(1, -1)

        # Scale features
        scaled_features = self.scaler.transform(feature_array)

        return scaled_features

    def _generate_shap_explanation(self, scaled_features: np.ndarray) -> dict[str, Any]:
        """
        Generate SHAP explanation for the prediction.

        Args:
            scaled_features: Scaled feature vector

        Returns:
            Dictionary containing SHAP values and feature contributions
        """
        try:
            # Check if SHAP explainer is available
            if self.shap_explainer is None:
                logger.warning("SHAP explainer not available, using fallback explanation")
                # Generate simple feature importance based on feature values
                contributions = []
                for i, feature_name in enumerate(self.feature_columns):
                    contributions.append({
                        "feature_name": feature_name,
                        "contribution": float(scaled_features[0][i] * 0.1),  # Simple contribution
                        "value": float(scaled_features[0][i])
                    })
                
                # Sort by absolute contribution
                contributions.sort(key=lambda x: abs(x["contribution"]), reverse=True)
                
                # Separate positive and negative contributions
                positive_contributions = [c for c in contributions if c["contribution"] > 0]
                negative_contributions = [c for c in contributions if c["contribution"] < 0]
                
                return {
                    "base_value": 0.5,
                    "contributions": contributions,
                    "top_positive": positive_contributions[:3],
                    "top_negative": negative_contributions[:3]
                }
            
            # Compute SHAP values
            shap_values = self.shap_explainer.shap_values(scaled_features)

            # Get base value
            base_value = self.shap_explainer.expected_value

            # Create feature contributions
            contributions = []
            for i, feature_name in enumerate(self.feature_columns):
                contributions.append({
                    "feature_name": feature_name,
                    "contribution": float(shap_values[0][i]),
                    "value": float(scaled_features[0][i])
                })

            # Sort by absolute contribution
            contributions.sort(key=lambda x: abs(x["contribution"]), reverse=True)

            # Separate positive and negative contributions
            positive_contributions = [c for c in contributions if c["contribution"] > 0]
            negative_contributions = [c for c in contributions if c["contribution"] < 0]

            return {
                "base_value": float(base_value),
                "contributions": contributions,
                "top_positive": positive_contributions[:3],
                "top_negative": negative_contributions[:3]
            }

        except Exception as e:
            logger.error(f"Failed to generate SHAP explanation: {e}")
            # Return empty explanation if SHAP fails
            return {
                "base_value": 0.5,
                "contributions": [],
                "top_positive": [],
                "top_negative": []
            }

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        """
        Generate prediction for a customer。

        Args:
            request: Prediction request with engineered features

        Returns:
            Prediction response with credit score and explanations

        Raises:
            ValueError: If input validation fails
            RuntimeError: If prediction fails
        """
        try:
            logger.info(f"Generating prediction for customer {request.customer_id}")

            # Extract features
            features = {
                "savings_ratio": request.savings_ratio,
                "average_monthly_income": request.average_monthly_income,
                "income_consistency": request.income_consistency,
                "total_expense": request.total_expense,
                "transaction_frequency": request.transaction_frequency
            }

            # Validate features
            self._validate_features(features)

            # Prepare feature vector
            scaled_features = self._prepare_feature_vector(features)

            # Generate prediction
            probability = float(self.model.predict_proba(scaled_features)[0, 1])
            prediction_label = int(self.model.predict(scaled_features)[0])

            # Calculate confidence
            confidence = ConfidenceCalculator.calculate_confidence(probability)

            # Convert to credit score
            credit_score = ScoreConverter.probability_to_score(probability)
            risk_category = ScoreConverter.get_risk_category(credit_score)

            # Generate SHAP explanation
            shap_explanation = self._generate_shap_explanation(scaled_features)

            # Format top positive and negative factors
            top_positive_factors = [
                {
                    "feature": c["feature_name"],
                    "contribution": c["contribution"],
                    "impact": "positive"
                }
                for c in shap_explanation["top_positive"]
            ]

            top_negative_factors = [
                {
                    "feature": c["feature_name"],
                    "contribution": c["contribution"],
                    "impact": "negative"
                }
                for c in shap_explanation["top_negative"]
            ]

            # Generate recommendations (placeholder - will be enhanced by recommendation engine)
            recommendations = self._generate_recommendations(features, shap_explanation)

            # Create response
            response = PredictionResponse(
                customer_id=request.customer_id,
                alternative_credit_score=credit_score,
                repayment_probability=round(probability, 4),
                risk_category=risk_category,
                confidence=round(confidence, 4),
                prediction="Low Risk" if prediction_label == 1 else "High Risk",
                top_positive_factors=top_positive_factors,
                top_negative_factors=top_negative_factors,
                recommendations=recommendations,
                model_version=self.MODEL_VERSION,
                prediction_timestamp=datetime.now()
            )

            logger.info(f"Prediction generated successfully for customer {request.customer_id}")
            return response

        except ValueError as e:
            logger.error(f"Validation error for customer {request.customer_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Prediction error for customer {request.customer_id}: {e}")
            raise RuntimeError(f"Prediction failed: {e}")

    def _generate_recommendations(self, features: dict[str, float], shap_explanation: dict[str, Any]) -> list[str]:
        """
        Generate personalized recommendations based on features and SHAP values.

        Args:
            features: Feature dictionary
            shap_explanation: SHAP explanation dictionary

        Returns:
            List of recommendation strings
        """
        recommendations = []

        # Analyze feature contributions
        feature_contributions = {c["feature_name"]: c["contribution"] for c in shap_explanation["contributions"]}

        # Savings ratio recommendations
        if features["savings_ratio"] < 0.2:
            recommendations.append("Increase your monthly savings to improve financial stability")
        elif feature_contributions.get("savings_ratio", 0) < 0:
            recommendations.append("Focus on maintaining consistent savings habits")

        # Income recommendations
        if features["average_monthly_income"] < 20000:
            recommendations.append("Consider increasing your income through additional sources")
        elif feature_contributions.get("average_monthly_income", 0) < 0:
            recommendations.append("Maintain stable income patterns to improve creditworthiness")

        # Expense recommendations
        if features["total_expense"] > features["average_monthly_income"] * 0.8:
            recommendations.append("Reduce unnecessary expenses to improve savings ratio")
        elif feature_contributions.get("total_expense", 0) < 0:
            recommendations.append("Monitor and control spending patterns")

        # Transaction frequency recommendations
        if features["transaction_frequency"] < 0.5:
            recommendations.append("Increase digital transaction activity for better financial tracking")
        elif feature_contributions.get("transaction_frequency", 0) < 0:
            recommendations.append("Maintain consistent transaction patterns")

        # Income consistency recommendations
        if features["income_consistency"] < 0.3:
            recommendations.append("Work on improving income and savings consistency")
        elif feature_contributions.get("income_consistency", 0) < 0:
            recommendations.append("Focus on maintaining stable financial behavior")

        # If no specific recommendations, provide general advice
        if not recommendations:
            recommendations.append("Continue maintaining good financial habits")

        return recommendations[:5]  # Limit to top 5 recommendations

    def health_check(self) -> dict[str, Any]:
        """
        Perform health check on the prediction service.

        Returns:
            Dictionary with health status information
        """
        return {
            "status": "healthy",
            "model_version": self.MODEL_VERSION,
            "model_loaded": self.model is not None,
            "scaler_loaded": self.scaler is not None,
            "feature_columns_loaded": self.feature_columns is not None,
            "shap_explainer_loaded": self.shap_explainer is not None,
            "required_features": self.REQUIRED_FEATURES,
            "feature_count": len(self.REQUIRED_FEATURES)
        }


# Global prediction service instance
_prediction_service: PredictionService | None = None


def get_prediction_service() -> PredictionService:
    """
    Get or create the global prediction service instance.

    Returns:
        PredictionService instance
    """
    global _prediction_service
    if _prediction_service is None:
        _prediction_service = PredictionService()
    return _prediction_service


__all__ = ["PredictionService", "get_prediction_service"]
