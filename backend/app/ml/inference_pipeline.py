"""End-to-end inference pipeline for alternative credit scoring."""

import logging
import time
from typing import Any

from app.ml.predictor import PredictionService, get_prediction_service
from app.ml.prediction_schema import PredictionRequest, PredictionResponse

logger = logging.getLogger(__name__)


class InferencePipeline:
    """End-to-end inference pipeline for credit scoring predictions."""

    def __init__(self, prediction_service: PredictionService | None = None):
        """
        Initialize the inference pipeline.

        Args:
            prediction_service: Optional prediction service instance. If not provided,
                               will use the global service instance.
        """
        self.prediction_service = prediction_service or get_prediction_service()

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        """
        Execute end-to-end prediction pipeline.

        Pipeline steps:
        1. Input validation (handled by Pydantic schema)
        2. Feature validation
        3. Feature preprocessing
        4. Model inference
        5. Score conversion
        6. Risk categorization
        7. Confidence calculation
        8. SHAP explanation generation
        9. Recommendation generation
        10. Response formatting

        Args:
            request: Prediction request with engineered features

        Returns:
            Prediction response with credit score and explanations

        Raises:
            ValueError: If input validation fails
            RuntimeError: If prediction pipeline fails
        """
        start_time = time.time()

        try:
            logger.info(f"Starting inference pipeline for customer {request.customer_id}")

            # Execute prediction through prediction service
            response = self.prediction_service.predict(request)

            # Calculate pipeline latency
            latency_ms = (time.time() - start_time) * 1000
            logger.info(f"Inference pipeline completed for customer {request.customer_id} in {latency_ms:.2f}ms")

            return response

        except ValueError as e:
            logger.error(f"Validation error in inference pipeline: {e}")
            raise
        except Exception as e:
            logger.error(f"Inference pipeline error: {e}")
            raise RuntimeError(f"Inference pipeline failed: {e}")

    def predict_batch(self, requests: list[PredictionRequest]) -> list[PredictionResponse]:
        """
        Execute batch prediction pipeline.

        Args:
            requests: List of prediction requests

        Returns:
            List of prediction responses

        Raises:
            ValueError: If any request validation fails
            RuntimeError: If batch prediction fails
        """
        logger.info(f"Starting batch inference pipeline for {len(requests)} customers")

        responses = []
        errors = []

        for i, request in enumerate(requests):
            try:
                response = self.predict(request)
                responses.append(response)
            except Exception as e:
                logger.error(f"Failed to predict for customer {request.customer_id}: {e}")
                errors.append(f"Customer {request.customer_id}: {str(e)}")

        logger.info(f"Batch inference completed: {len(responses)} successful, {len(errors)} failed")

        if errors:
            logger.warning(f"Batch prediction had {len(errors)} errors")

        return responses

    def health_check(self) -> dict[str, Any]:
        """
        Perform health check on the inference pipeline.

        Returns:
            Dictionary with health status information
        """
        service_health = self.prediction_service.health_check()

        return {
            "pipeline_status": "healthy",
            "prediction_service_status": service_health["status"],
            "model_version": service_health["model_version"],
            "components_loaded": {
                "model": service_health["model_loaded"],
                "scaler": service_health["scaler_loaded"],
                "feature_columns": service_health["feature_columns_loaded"],
                "shap_explainer": service_health["shap_explainer_loaded"]
            },
            "required_features": service_health["required_features"],
            "feature_count": service_health["feature_count"]
        }

    def get_pipeline_metrics(self) -> dict[str, Any]:
        """
        Get pipeline performance metrics.

        Returns:
            Dictionary with pipeline metrics
        """
        return {
            "pipeline_name": "Beyond Cibil Inference Pipeline",
            "version": "1.0",
            "model_version": self.prediction_service.MODEL_VERSION,
            "target_latency_ms": 100,
            "feature_count": len(self.prediction_service.REQUIRED_FEATURES),
            "supports_batch": True,
            "supports_shap": True,
            "supports_recommendations": True
        }


# Global inference pipeline instance
_inference_pipeline: InferencePipeline | None = None


def get_inference_pipeline() -> InferencePipeline:
    """
    Get or create the global inference pipeline instance.

    Returns:
        InferencePipeline instance
    """
    global _inference_pipeline
    if _inference_pipeline is None:
        _inference_pipeline = InferencePipeline()
    return _inference_pipeline


__all__ = ["InferencePipeline", "get_inference_pipeline"]
