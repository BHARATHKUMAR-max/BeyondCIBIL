"""API routes for ML prediction endpoints."""

import logging
from typing import Annotated
from pydantic import BaseModel, Field

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database.session import get_db
from app.ml.inference_pipeline import get_inference_pipeline
from app.ml.prediction_schema import BatchPredictionRequest, BatchPredictionResponse, PredictionRequest, PredictionResponse
from app.models.user import User
from app.services.mock_bank_service import mock_bank_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/predictions", tags=["predictions"])
SessionDependency = Annotated[AsyncSession, Depends(get_db)]
CurrentUserDependency = Annotated[User, Depends(get_current_user)]


class BankConnectionRequest(BaseModel):
    """Request for bank-based prediction."""
    
    phone_number: str = Field(..., description="Customer mobile number", min_length=10, max_length=10)
    bank_name: str = Field(..., description="Bank name")


class BankConnectionResponse(BaseModel):
    """Response for bank-based prediction."""
    
    customer: dict
    transaction_summary: dict
    alternative_credit_score: int
    repayment_probability: float
    confidence: float
    risk_category: str
    shap_explanation: dict
    recommendations: list


@router.post("/credit-score", response_model=PredictionResponse)
async def predict_credit_score(
    request: PredictionRequest,
    user: CurrentUserDependency,
) -> PredictionResponse:
    """
    Generate alternative credit score prediction.

    This endpoint uses the trained ML model to predict:
    - Alternative credit score (300-900)
    - Repayment probability
    - Risk category
    - Confidence score
    - SHAP-based feature explanations
    - Personalized recommendations

    Args:
        request: Prediction request with engineered features
        user: Authenticated user (from JWT token)

    Returns:
        Prediction response with credit score and explanations

    Raises:
        HTTPException: If prediction fails or validation error occurs
    """
    try:
        logger.info(f"Credit score prediction request for customer {request.customer_id} by user {user.id}")

        # Get inference pipeline
        pipeline = get_inference_pipeline()

        # Execute prediction
        response = pipeline.predict(request)

        logger.info(f"Credit score prediction completed for customer {request.customer_id}")
        return response

    except ValueError as e:
        logger.error(f"Validation error for customer {request.customer_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )
    except RuntimeError as e:
        logger.error(f"Prediction error for customer {request.customer_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error for customer {request.customer_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during prediction"
        )


@router.post("/batch", response_model=BatchPredictionResponse)
async def predict_batch(
    request: BatchPredictionRequest,
    user: CurrentUserDependency,
) -> BatchPredictionResponse:
    """
    Generate batch credit score predictions.

    This endpoint processes multiple prediction requests in a single call.
    Useful for bulk processing or batch analysis.

    Args:
        request: Batch prediction request with multiple prediction requests
        user: Authenticated user (from JWT token)

    Returns:
        Batch prediction response with results and error information

    Raises:
        HTTPException: If batch prediction fails
    """
    try:
        logger.info(f"Batch prediction request for {len(request.predictions)} customers by user {user.id}")

        # Get inference pipeline
        pipeline = get_inference_pipeline()

        # Execute batch prediction
        responses = pipeline.predict_batch(request.predictions)

        # Count successes and failures
        success_count = len(responses)
        failure_count = len(request.predictions) - success_count

        # Collect errors (if any)
        errors = []
        if failure_count > 0:
            failed_customers = [
                req.customer_id for req in request.predictions
                if req.customer_id not in [resp.customer_id for resp in responses]
            ]
            errors = [f"Prediction failed for customer: {cid}" for cid in failed_customers]

        batch_response = BatchPredictionResponse(
            predictions=responses,
            total_count=len(request.predictions),
            success_count=success_count,
            failure_count=failure_count,
            errors=errors
        )

        logger.info(f"Batch prediction completed: {success_count} successful, {failure_count} failed")
        return batch_response

    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )


@router.get("/health")
async def prediction_health_check() -> dict:
    """
    Health check endpoint for prediction service.

    Returns the status of the ML prediction service including:
    - Model loading status
    - Artifact loading status
    - Required features
    - Model version

    Returns:
        Health check status dictionary
    """
    try:
        pipeline = get_inference_pipeline()
        health_status = pipeline.health_check()
        return health_status
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@router.get("/metrics")
async def prediction_metrics() -> dict:
    """
    Get prediction pipeline metrics.

    Returns performance and configuration metrics for the inference pipeline.

    Returns:
        Pipeline metrics dictionary
    """
    try:
        pipeline = get_inference_pipeline()
        metrics = pipeline.get_pipeline_metrics()
        return metrics
    except Exception as e:
        logger.error(f"Metrics retrieval error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve metrics: {str(e)}"
        )


@router.get("/schema")
async def get_prediction_schema() -> dict:
    """
    Get the prediction request schema.

    Returns the schema definition for prediction requests to help clients
    understand the required fields and their formats.

    Returns:
        Schema definition dictionary
    """
    return {
        "schema": "PredictionRequest",
        "required_fields": [
            "customer_id",
            "savings_ratio",
            "average_monthly_income",
            "income_consistency",
            "total_expense",
            "transaction_frequency"
        ],
        "field_descriptions": {
            "customer_id": "Unique customer identifier (string)",
            "savings_ratio": "Ratio of savings to income (0-1, float)",
            "average_monthly_income": "Average monthly income in currency units (float, non-negative)",
            "income_consistency": "Combined measure of savings and transaction consistency (float, non-negative)",
            "total_expense": "Total monthly expenses in currency units (float, non-negative)",
            "transaction_frequency": "Number of transactions per day (float, non-negative)"
        },
        "validation_rules": {
            "savings_ratio": "Must be between 0 and 1",
            "average_monthly_income": "Must be non-negative",
            "income_consistency": "Must be non-negative",
            "total_expense": "Must be non-negative",
            "transaction_frequency": "Must be non-negative"
        },
        "example_request": {
            "customer_id": "cust_12345",
            "savings_ratio": 0.45,
            "average_monthly_income": 35000.0,
            "income_consistency": 0.38,
            "total_expense": 18000.0,
            "transaction_frequency": 0.75
        }
    }


@router.post("/predict-from-bank", response_model=BankConnectionResponse)
async def predict_from_bank(
    request: BankConnectionRequest,
) -> BankConnectionResponse:
    """
    Generate credit score prediction from bank connection.
    
    This endpoint:
    1. Fetches or generates mock banking data based on phone number and bank
    2. Uses the existing feature engineering pipeline to process the data
    3. Runs the ML model for prediction
    4. Returns comprehensive results including customer data, transaction summary,
       credit score, and recommendations
    
    Args:
        request: Bank connection request with phone number and bank name
        user: Authenticated user (from JWT token)
    
    Returns:
        Bank connection response with customer data and prediction results
    
    Raises:
        HTTPException: If prediction fails or validation error occurs
    """
    try:
        logger.info(f"Bank-based prediction request for phone {request.phone_number} at {request.bank_name}")
        
        # Get or generate customer banking data
        customer_data = mock_bank_service.get_customer_data(
            request.phone_number,
            request.bank_name
        )
        
        # Get transaction summary
        transaction_summary = mock_bank_service.get_transaction_summary(customer_data)
        
        # Create prediction request using engineered features from customer data
        prediction_request = PredictionRequest(
            customer_id=customer_data['customer_id'],
            savings_ratio=customer_data['savings_ratio'],
            average_monthly_income=customer_data['monthly_income'],
            income_consistency=customer_data['income_consistency'],
            total_expense=customer_data['total_expense'],
            transaction_frequency=customer_data['transaction_frequency']
        )
        
        # Get inference pipeline
        pipeline = get_inference_pipeline()
        
        # Execute prediction using actual ML model
        prediction_response = pipeline.predict(prediction_request)
        
        # Build comprehensive response with ML model results
        response = BankConnectionResponse(
            customer={
                "customer_id": customer_data['customer_id'],
                "phone_number": customer_data['phone_number'],
                "bank_name": customer_data['bank_name'],
                "account_number": customer_data['account_number'],
                "account_type": customer_data['account_type'],
                "account_balance": customer_data['account_balance'],
                "monthly_income": customer_data['monthly_income'],
                "total_expense": customer_data['total_expense'],
                "savings": customer_data['savings'],
                "emis": customer_data['emis'],
                "recurring_payments": customer_data['recurring_payments']
            },
            transaction_summary=transaction_summary,
            alternative_credit_score=prediction_response.alternative_credit_score,
            repayment_probability=prediction_response.repayment_probability,
            confidence=prediction_response.confidence,
            risk_category=prediction_response.risk_category,
            shap_explanation={
                "top_positive_factors": prediction_response.top_positive_factors,
                "top_negative_factors": prediction_response.top_negative_factors
            },
            recommendations=prediction_response.recommendations
        )
        
        logger.info(f"Bank-based prediction completed for customer {customer_data['customer_id']} with score {prediction_response.alternative_credit_score}")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error for phone {request.phone_number}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )
    except RuntimeError as e:
        logger.error(f"Prediction error for phone {request.phone_number}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error for phone {request.phone_number}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during prediction"
        )
