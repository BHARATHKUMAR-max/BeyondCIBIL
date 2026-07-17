"""Pydantic schemas for ML prediction requests and responses."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class PredictionRequest(BaseModel):
    """Schema for prediction request with engineered features."""

    customer_id: str = Field(..., description="Unique customer identifier")
    savings_ratio: float = Field(..., description="Ratio of savings to income (0-1)")
    average_monthly_income: float = Field(..., description="Average monthly income in currency units")
    income_consistency: float = Field(..., description="Combined measure of savings and transaction consistency")
    total_expense: float = Field(..., description="Total monthly expenses in currency units")
    transaction_frequency: float = Field(..., description="Number of transactions per day")

    @field_validator("savings_ratio")
    @classmethod
    def validate_savings_ratio(cls, v: float) -> float:
        if not 0 <= v <= 1:
            raise ValueError("savings_ratio must be between 0 and 1")
        return float(v)

    @field_validator("average_monthly_income")
    @classmethod
    def validate_income(cls, v: float) -> float:
        if v < 0:
            raise ValueError("average_monthly_income must be non-negative")
        return float(v)

    @field_validator("total_expense")
    @classmethod
    def validate_expense(cls, v: float) -> float:
        if v < 0:
            raise ValueError("total_expense must be non-negative")
        return float(v)

    @field_validator("transaction_frequency")
    @classmethod
    def validate_frequency(cls, v: float) -> float:
        if v < 0:
            raise ValueError("transaction_frequency must be non-negative")
        return float(v)

    @field_validator("income_consistency")
    @classmethod
    def validate_consistency(cls, v: float) -> float:
        if v < 0:
            raise ValueError("income_consistency must be non-negative")
        return float(v)


class PredictionResponse(BaseModel):
    """Schema for prediction response."""

    customer_id: str = Field(..., description="Customer identifier")
    alternative_credit_score: int = Field(..., description="Alternative credit score (300-900)")
    repayment_probability: float = Field(..., description="Probability of repayment (0-1)")
    risk_category: str = Field(..., description="Risk category classification")
    confidence: float = Field(..., description="Confidence score (0-1)")
    prediction: str = Field(..., description="Binary prediction (Low Risk/High Risk)")
    top_positive_factors: list[dict[str, Any]] = Field(..., description="Top positive contributing factors")
    top_negative_factors: list[dict[str, Any]] = Field(..., description="Top negative contributing factors")
    recommendations: list[str] = Field(..., description="Personalized recommendations")
    model_version: str = Field(..., description="Model version identifier")
    prediction_timestamp: datetime = Field(..., description="Timestamp of prediction")

    @field_validator("alternative_credit_score")
    @classmethod
    def validate_score(cls, v: int) -> int:
        if not 300 <= v <= 900:
            raise ValueError("alternative_credit_score must be between 300 and 900")
        return v

    @field_validator("repayment_probability")
    @classmethod
    def validate_probability(cls, v: float) -> float:
        if not 0 <= v <= 1:
            raise ValueError("repayment_probability must be between 0 and 1")
        return float(v)

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        if not 0 <= v <= 1:
            raise ValueError("confidence must be between 0 and 1")
        return float(v)

    @field_validator("risk_category")
    @classmethod
    def validate_risk_category(cls, v: str) -> str:
        valid_categories = ["Very Low Risk", "Low Risk", "Medium Risk", "High Risk", "Very High Risk"]
        if v not in valid_categories:
            raise ValueError(f"risk_category must be one of {valid_categories}")
        return v

    @field_validator("prediction")
    @classmethod
    def validate_prediction(cls, v: str) -> str:
        if v not in ["Low Risk", "High Risk"]:
            raise ValueError("prediction must be 'Low Risk' or 'High Risk'")
        return v


class FeatureContribution(BaseModel):
    """Schema for individual feature contribution."""

    feature_name: str = Field(..., description="Name of the feature")
    contribution: float = Field(..., description="SHAP contribution value")
    value: float = Field(..., description="Feature value")


class BatchPredictionRequest(BaseModel):
    """Schema for batch prediction request."""

    predictions: list[PredictionRequest] = Field(..., description="List of prediction requests")


class BatchPredictionResponse(BaseModel):
    """Schema for batch prediction response."""

    predictions: list[PredictionResponse] = Field(..., description="List of prediction responses")
    total_count: int = Field(..., description="Total number of predictions")
    success_count: int = Field(..., description="Number of successful predictions")
    failure_count: int = Field(..., description="Number of failed predictions")
    errors: list[str] = Field(default_factory=list, description="Error messages for failed predictions")
