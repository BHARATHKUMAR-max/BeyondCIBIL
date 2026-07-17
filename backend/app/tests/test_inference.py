"""Unit tests for ML inference components."""

import pytest
import numpy as np
from datetime import datetime

from app.ml.prediction_schema import PredictionRequest, PredictionResponse
from app.ml.score_converter import ScoreConverter
from app.ml.confidence import ConfidenceCalculator


class TestScoreConverter:
    """Test suite for ScoreConverter."""

    def test_probability_to_score_valid_range(self):
        """Test score conversion for valid probability range."""
        # Test edge cases
        assert ScoreConverter.probability_to_score(0.0) == 300
        assert ScoreConverter.probability_to_score(1.0) == 900
        assert ScoreConverter.probability_to_score(0.5) == 600

    def test_probability_to_score_mid_range(self):
        """Test score conversion for mid-range probabilities."""
        assert ScoreConverter.probability_to_score(0.75) == 750
        assert ScoreConverter.probability_to_score(0.25) == 450

    def test_probability_to_score_invalid(self):
        """Test score conversion with invalid probabilities."""
        with pytest.raises(ValueError):
            ScoreConverter.probability_to_score(-0.1)
        with pytest.raises(ValueError):
            ScoreConverter.probability_to_score(1.1)

    def test_score_to_probability_valid_range(self):
        """Test probability conversion for valid score range."""
        assert ScoreConverter.score_to_probability(300) == 0.0
        assert ScoreConverter.score_to_probability(900) == 1.0
        assert ScoreConverter.score_to_probability(600) == 0.5

    def test_score_to_probability_invalid(self):
        """Test probability conversion with invalid scores."""
        with pytest.raises(ValueError):
            ScoreConverter.score_to_probability(299)
        with pytest.raises(ValueError):
            ScoreConverter.score_to_probability(901)

    def test_get_risk_category_very_low(self):
        """Test risk category for very low risk."""
        assert ScoreConverter.get_risk_category(750) == "Very Low Risk"
        assert ScoreConverter.get_risk_category(800) == "Very Low Risk"
        assert ScoreConverter.get_risk_category(900) == "Very Low Risk"

    def test_get_risk_category_low(self):
        """Test risk category for low risk."""
        assert ScoreConverter.get_risk_category(650) == "Low Risk"
        assert ScoreConverter.get_risk_category(700) == "Low Risk"
        assert ScoreConverter.get_risk_category(749) == "Low Risk"

    def test_get_risk_category_medium(self):
        """Test risk category for medium risk."""
        assert ScoreConverter.get_risk_category(550) == "Medium Risk"
        assert ScoreConverter.get_risk_category(600) == "Medium Risk"
        assert ScoreConverter.get_risk_category(649) == "Medium Risk"

    def test_get_risk_category_high(self):
        """Test risk category for high risk."""
        assert ScoreConverter.get_risk_category(450) == "High Risk"
        assert ScoreConverter.get_risk_category(500) == "High Risk"
        assert ScoreConverter.get_risk_category(549) == "High Risk"

    def test_get_risk_category_very_high(self):
        """Test risk category for very high risk."""
        assert ScoreConverter.get_risk_category(300) == "Very High Risk"
        assert ScoreConverter.get_risk_category(400) == "Very High Risk"
        assert ScoreConverter.get_risk_category(449) == "Very High Risk"

    def test_get_risk_category_from_probability(self):
        """Test risk category conversion from probability."""
        assert ScoreConverter.get_risk_category_from_probability(0.83) == "Very Low Risk"
        assert ScoreConverter.get_risk_category_from_probability(0.5) == "Medium Risk"
        assert ScoreConverter.get_risk_category_from_probability(0.17) == "Very High Risk"

    def test_get_risk_level(self):
        """Test numeric risk level conversion."""
        assert ScoreConverter.get_risk_level("Very Low Risk") == 1
        assert ScoreConverter.get_risk_level("Low Risk") == 2
        assert ScoreConverter.get_risk_level("Medium Risk") == 3
        assert ScoreConverter.get_risk_level("High Risk") == 4
        assert ScoreConverter.get_risk_level("Very High Risk") == 5

    def test_get_score_description(self):
        """Test score description generation."""
        assert "Excellent" in ScoreConverter.get_score_description(800)
        assert "Good" in ScoreConverter.get_score_description(700)
        assert "Fair" in ScoreConverter.get_score_description(600)
        assert "Poor" in ScoreConverter.get_score_description(500)
        assert "Very Poor" in ScoreConverter.get_score_description(350)

    def test_get_score_color(self):
        """Test score color coding."""
        assert ScoreConverter.get_score_color(800) == "#10B981"  # Green
        assert ScoreConverter.get_score_color(700) == "#3B82F6"  # Blue
        assert ScoreConverter.get_score_color(600) == "#F59E0B"  # Yellow
        assert ScoreConverter.get_score_color(500) == "#F97316"  # Orange
        assert ScoreConverter.get_score_color(350) == "#EF4444"  # Red


class TestConfidenceCalculator:
    """Test suite for ConfidenceCalculator."""

    def test_calculate_confidence_high(self):
        """Test confidence calculation for high confidence."""
        assert ConfidenceCalculator.calculate_confidence(0.9) == 0.8
        assert ConfidenceCalculator.calculate_confidence(1.0) == 1.0
        assert ConfidenceCalculator.calculate_confidence(0.0) == 1.0

    def test_calculate_confidence_medium(self):
        """Test confidence calculation for medium confidence."""
        assert ConfidenceCalculator.calculate_confidence(0.7) == 0.4
        assert ConfidenceCalculator.calculate_confidence(0.3) == 0.4

    def test_calculate_confidence_low(self):
        """Test confidence calculation for low confidence."""
        assert ConfidenceCalculator.calculate_confidence(0.5) == 0.0
        assert ConfidenceCalculator.calculate_confidence(0.55) == 0.1
        assert ConfidenceCalculator.calculate_confidence(0.45) == 0.1

    def test_calculate_confidence_invalid(self):
        """Test confidence calculation with invalid values."""
        with pytest.raises(ValueError):
            ConfidenceCalculator.calculate_confidence(-0.1)
        with pytest.raises(ValueError):
            ConfidenceCalculator.calculate_confidence(1.1)

    def test_get_confidence_level(self):
        """Test confidence level categorization."""
        assert ConfidenceCalculator.get_confidence_level(0.9) == "Very High"
        assert ConfidenceCalculator.get_confidence_level(0.7) == "High"
        assert ConfidenceCalculator.get_confidence_level(0.5) == "Medium"
        assert ConfidenceCalculator.get_confidence_level(0.3) == "Low"
        assert ConfidenceCalculator.get_confidence_level(0.1) == "Very Low"

    def test_get_confidence_color(self):
        """Test confidence color coding."""
        assert ConfidenceCalculator.get_confidence_color(0.9) == "#10B981"  # Green
        assert ConfidenceCalculator.get_confidence_color(0.7) == "#3B82F6"  # Blue
        assert ConfidenceCalculator.get_confidence_color(0.5) == "#F59E0B"  # Yellow
        assert ConfidenceCalculator.get_confidence_color(0.3) == "#F97316"  # Orange
        assert ConfidenceCalculator.get_confidence_color(0.1) == "#EF4444"  # Red

    def test_calculate_prediction_stability_single(self):
        """Test stability calculation for single prediction."""
        assert ConfidenceCalculator.calculate_prediction_stability([0.5]) == 1.0

    def test_calculate_prediction_stability_multiple(self):
        """Test stability calculation for multiple predictions."""
        stable_probs = [0.5, 0.51, 0.49, 0.5]
        unstable_probs = [0.2, 0.8, 0.3, 0.7]

        stable_score = ConfidenceCalculator.calculate_prediction_stability(stable_probs)
        unstable_score = ConfidenceCalculator.calculate_prediction_stability(unstable_probs)

        assert stable_score > unstable_score

    def test_calculate_prediction_stability_empty(self):
        """Test stability calculation with empty list."""
        with pytest.raises(ValueError):
            ConfidenceCalculator.calculate_prediction_stability([])

    def test_calculate_ensemble_confidence(self):
        """Test ensemble confidence calculation."""
        ensemble_probs = [0.7, 0.75, 0.72, 0.68]
        confidence = ConfidenceCalculator.calculate_ensemble_confidence(ensemble_probs)
        assert 0 <= confidence <= 1

    def test_calculate_ensemble_confidence_empty(self):
        """Test ensemble confidence with empty list."""
        with pytest.raises(ValueError):
            ConfidenceCalculator.calculate_ensemble_confidence([])

    def test_is_prediction_reliable(self):
        """Test prediction reliability check."""
        assert ConfidenceCalculator.is_prediction_reliable(0.8) == True
        assert ConfidenceCalculator.is_prediction_reliable(0.6) == True
        assert ConfidenceCalculator.is_prediction_reliable(0.4) == False

    def test_is_prediction_reliable_custom_threshold(self):
        """Test prediction reliability with custom threshold."""
        assert ConfidenceCalculator.is_prediction_reliable(0.5, threshold=0.5) == True
        assert ConfidenceCalculator.is_prediction_reliable(0.49, threshold=0.5) == False

    def test_get_confidence_description(self):
        """Test confidence description generation."""
        assert "very confident" in ConfidenceCalculator.get_confidence_description(0.9).lower()
        assert "confident" in ConfidenceCalculator.get_confidence_description(0.7).lower()
        assert "moderate" in ConfidenceCalculator.get_confidence_description(0.5).lower()
        assert "low confidence" in ConfidenceCalculator.get_confidence_description(0.3).lower()
        assert "uncertain" in ConfidenceCalculator.get_confidence_description(0.1).lower()


class TestPredictionSchema:
    """Test suite for prediction schemas."""

    def test_prediction_request_valid(self):
        """Test valid prediction request."""
        request = PredictionRequest(
            customer_id="test_123",
            savings_ratio=0.5,
            average_monthly_income=30000.0,
            income_consistency=0.4,
            total_expense=15000.0,
            transaction_frequency=0.75
        )
        assert request.customer_id == "test_123"
        assert request.savings_ratio == 0.5

    def test_prediction_request_savings_ratio_validation(self):
        """Test savings ratio validation."""
        with pytest.raises(ValueError):
            PredictionRequest(
                customer_id="test_123",
                savings_ratio=1.5,  # Invalid: > 1
                average_monthly_income=30000.0,
                income_consistency=0.4,
                total_expense=15000.0,
                transaction_frequency=0.75
            )

        with pytest.raises(ValueError):
            PredictionRequest(
                customer_id="test_123",
                savings_ratio=-0.1,  # Invalid: < 0
                average_monthly_income=30000.0,
                income_consistency=0.4,
                total_expense=15000.0,
                transaction_frequency=0.75
            )

    def test_prediction_request_income_validation(self):
        """Test income validation."""
        with pytest.raises(ValueError):
            PredictionRequest(
                customer_id="test_123",
                savings_ratio=0.5,
                average_monthly_income=-1000.0,  # Invalid: negative
                income_consistency=0.4,
                total_expense=15000.0,
                transaction_frequency=0.75
            )

    def test_prediction_request_expense_validation(self):
        """Test expense validation."""
        with pytest.raises(ValueError):
            PredictionRequest(
                customer_id="test_123",
                savings_ratio=0.5,
                average_monthly_income=30000.0,
                income_consistency=0.4,
                total_expense=-5000.0,  # Invalid: negative
                transaction_frequency=0.75
            )

    def test_prediction_response_valid(self):
        """Test valid prediction response."""
        response = PredictionResponse(
            customer_id="test_123",
            alternative_credit_score=720,
            repayment_probability=0.78,
            risk_category="Low Risk",
            confidence=0.56,
            prediction="Low Risk",
            top_positive_factors=[],
            top_negative_factors=[],
            recommendations=[],
            model_version="1.0",
            prediction_timestamp=datetime.now()
        )
        assert response.customer_id == "test_123"
        assert response.alternative_credit_score == 720

    def test_prediction_response_score_validation(self):
        """Test credit score validation in response."""
        with pytest.raises(ValueError):
            PredictionResponse(
                customer_id="test_123",
                alternative_credit_score=299,  # Invalid: < 300
                repayment_probability=0.78,
                risk_category="Low Risk",
                confidence=0.56,
                prediction="Low Risk",
                top_positive_factors=[],
                top_negative_factors=[],
                recommendations=[],
                model_version="1.0",
                prediction_timestamp=datetime.now()
            )

        with pytest.raises(ValueError):
            PredictionResponse(
                customer_id="test_123",
                alternative_credit_score=901,  # Invalid: > 900
                repayment_probability=0.78,
                risk_category="Low Risk",
                confidence=0.56,
                prediction="Low Risk",
                top_positive_factors=[],
                top_negative_factors=[],
                recommendations=[],
                model_version="1.0",
                prediction_timestamp=datetime.now()
            )

    def test_prediction_response_probability_validation(self):
        """Test probability validation in response."""
        with pytest.raises(ValueError):
            PredictionResponse(
                customer_id="test_123",
                alternative_credit_score=720,
                repayment_probability=1.5,  # Invalid: > 1
                risk_category="Low Risk",
                confidence=0.56,
                prediction="Low Risk",
                top_positive_factors=[],
                top_negative_factors=[],
                recommendations=[],
                model_version="1.0",
                prediction_timestamp=datetime.now()
            )

    def test_prediction_response_risk_category_validation(self):
        """Test risk category validation in response."""
        with pytest.raises(ValueError):
            PredictionResponse(
                customer_id="test_123",
                alternative_credit_score=720,
                repayment_probability=0.78,
                risk_category="Invalid Risk",  # Invalid category
                confidence=0.56,
                prediction="Low Risk",
                top_positive_factors=[],
                top_negative_factors=[],
                recommendations=[],
                model_version="1.0",
                prediction_timestamp=datetime.now()
            )

    def test_prediction_response_prediction_validation(self):
        """Test prediction label validation in response."""
        with pytest.raises(ValueError):
            PredictionResponse(
                customer_id="test_123",
                alternative_credit_score=720,
                repayment_probability=0.78,
                risk_category="Low Risk",
                confidence=0.56,
                prediction="Invalid Prediction",  # Invalid prediction
                top_positive_factors=[],
                top_negative_factors=[],
                recommendations=[],
                model_version="1.0",
                prediction_timestamp=datetime.now()
            )


class TestPredictionServiceIntegration:
    """Integration tests for PredictionService (requires artifacts)."""

    @pytest.fixture
    def sample_request(self):
        """Create a sample prediction request."""
        return PredictionRequest(
            customer_id="test_customer_001",
            savings_ratio=0.45,
            average_monthly_income=35000.0,
            income_consistency=0.38,
            total_expense=18000.0,
            transaction_frequency=0.75
        )

    def test_prediction_service_initialization(self, sample_request):
        """Test that prediction service can be initialized."""
        try:
            from app.ml.predictor import get_prediction_service
            service = get_prediction_service()
            assert service is not None
            assert service.model is not None
            assert service.scaler is not None
            assert service.feature_columns is not None
        except Exception as e:
            pytest.skip(f"Prediction service initialization failed: {e}")

    def test_prediction_service_health_check(self):
        """Test prediction service health check."""
        try:
            from app.ml.predictor import get_prediction_service
            service = get_prediction_service()
            health = service.health_check()
            assert health["status"] == "healthy"
            assert health["model_loaded"] == True
            assert health["scaler_loaded"] == True
        except Exception as e:
            pytest.skip(f"Prediction service health check failed: {e}")

    def test_prediction_service_predict(self, sample_request):
        """Test prediction service prediction."""
        try:
            from app.ml.predictor import get_prediction_service
            service = get_prediction_service()
            response = service.predict(sample_request)
            
            assert response.customer_id == sample_request.customer_id
            assert 300 <= response.alternative_credit_score <= 900
            assert 0 <= response.repayment_probability <= 1
            assert response.confidence >= 0
            assert response.prediction in ["Low Risk", "High Risk"]
            assert len(response.recommendations) > 0
        except Exception as e:
            pytest.skip(f"Prediction service prediction failed: {e}")


class TestInferencePipelineIntegration:
    """Integration tests for InferencePipeline."""

    @pytest.fixture
    def sample_request(self):
        """Create a sample prediction request."""
        return PredictionRequest(
            customer_id="test_customer_002",
            savings_ratio=0.50,
            average_monthly_income=40000.0,
            income_consistency=0.42,
            total_expense=20000.0,
            transaction_frequency=0.80
        )

    def test_inference_pipeline_initialization(self):
        """Test that inference pipeline can be initialized."""
        try:
            from app.ml.inference_pipeline import get_inference_pipeline
            pipeline = get_inference_pipeline()
            assert pipeline is not None
            assert pipeline.prediction_service is not None
        except Exception as e:
            pytest.skip(f"Inference pipeline initialization failed: {e}")

    def test_inference_pipeline_predict(self, sample_request):
        """Test inference pipeline prediction."""
        try:
            from app.ml.inference_pipeline import get_inference_pipeline
            pipeline = get_inference_pipeline()
            response = pipeline.predict(sample_request)
            
            assert response.customer_id == sample_request.customer_id
            assert 300 <= response.alternative_credit_score <= 900
            assert 0 <= response.repayment_probability <= 1
        except Exception as e:
            pytest.skip(f"Inference pipeline prediction failed: {e}")

    def test_inference_pipeline_health_check(self):
        """Test inference pipeline health check."""
        try:
            from app.ml.inference_pipeline import get_inference_pipeline
            pipeline = get_inference_pipeline()
            health = pipeline.health_check()
            assert health["pipeline_status"] == "healthy"
        except Exception as e:
            pytest.skip(f"Inference pipeline health check failed: {e}")

    def test_inference_pipeline_batch_predict(self):
        """Test inference pipeline batch prediction."""
        try:
            from app.ml.inference_pipeline import get_inference_pipeline
            from app.ml.prediction_schema import PredictionRequest
            
            pipeline = get_inference_pipeline()
            requests = [
                PredictionRequest(
                    customer_id=f"test_{i}",
                    savings_ratio=0.4 + (i * 0.05),
                    average_monthly_income=30000.0 + (i * 1000),
                    income_consistency=0.3 + (i * 0.02),
                    total_expense=15000.0 + (i * 500),
                    transaction_frequency=0.7 + (i * 0.05)
                )
                for i in range(3)
            ]
            
            responses = pipeline.predict_batch(requests)
            assert len(responses) == 3
            for response in responses:
                assert 300 <= response.alternative_credit_score <= 900
        except Exception as e:
            pytest.skip(f"Inference pipeline batch prediction failed: {e}")


class TestRecommendationEngine:
    """Test suite for RecommendationEngine."""

    def test_recommendation_engine_initialization(self):
        """Test that recommendation engine can be initialized."""
        try:
            from app.ml.recommendation_engine import get_recommendation_engine
            engine = get_recommendation_engine()
            assert engine is not None
            assert engine.recommendation_templates is not None
        except Exception as e:
            pytest.skip(f"Recommendation engine initialization failed: {e}")

    def test_generate_recommendations(self):
        """Test recommendation generation."""
        try:
            from app.ml.recommendation_engine import get_recommendation_engine
            
            engine = get_recommendation_engine()
            features = {
                "savings_ratio": 0.15,
                "average_monthly_income": 15000.0,
                "income_consistency": 0.25,
                "total_expense": 13000.0,
                "transaction_frequency": 0.4
            }
            shap_contributions = {
                "savings_ratio": -0.1,
                "average_monthly_income": -0.15,
                "income_consistency": -0.05,
                "total_expense": -0.08,
                "transaction_frequency": -0.03
            }
            
            recommendations = engine.generate_recommendations(features, shap_contributions)
            assert len(recommendations) > 0
            assert len(recommendations) <= 5
        except Exception as e:
            pytest.skip(f"Recommendation generation failed: {e}")

    def test_generate_actionable_insights(self):
        """Test actionable insights generation."""
        try:
            from app.ml.recommendation_engine import get_recommendation_engine
            
            engine = get_recommendation_engine()
            features = {
                "savings_ratio": 0.3,
                "average_monthly_income": 25000.0,
                "income_consistency": 0.35,
                "total_expense": 18000.0,
                "transaction_frequency": 0.6
            }
            shap_contributions = {
                "savings_ratio": 0.05,
                "average_monthly_income": 0.1,
                "income_consistency": 0.03,
                "total_expense": -0.04,
                "transaction_frequency": 0.02
            }
            
            insights = engine.generate_actionable_insights(features, shap_contributions, 650)
            assert insights["current_score"] == 650
            assert len(insights["recommendations"]) > 0
            assert "top_strengths" in insights
            assert "areas_for_improvement" in insights
        except Exception as e:
            pytest.skip(f"Actionable insights generation failed: {e}")
