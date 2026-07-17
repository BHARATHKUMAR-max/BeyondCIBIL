"""Pydantic schemas for ML data structures."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class TransactionSchema(BaseModel):
    """Schema for a single transaction."""

    transaction_id: str = Field(..., description="Unique transaction identifier")
    customer_id: str = Field(..., description="Customer identifier")
    transaction_date: datetime = Field(..., description="Transaction date")
    amount: float = Field(..., description="Transaction amount")
    transaction_type: str = Field(..., description="Credit or Debit")
    category: str = Field(..., description="Transaction category")
    merchant: str = Field(..., description="Merchant name")
    payment_mode: str = Field(..., description="Payment mode")
    balance_after: float = Field(..., description="Balance after transaction")
    description: str = Field(..., description="Transaction description")
    location: str = Field(..., description="Transaction location")
    is_recurring: bool = Field(..., description="Whether transaction is recurring")

    @field_validator("amount", "balance_after")
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if not isinstance(v, (int, float)):
            raise ValueError("Amount must be numeric")
        return float(v)

    @field_validator("transaction_type")
    @classmethod
    def validate_transaction_type(cls, v: str) -> str:
        if v not in ["Credit", "Debit"]:
            raise ValueError("transaction_type must be 'Credit' or 'Debit'")
        return v


class CustomerSchema(BaseModel):
    """Schema for customer information."""

    customer_id: str = Field(..., description="Unique customer identifier")
    name: str = Field(..., description="Customer name")
    email: str = Field(..., description="Customer email")
    phone: str = Field(..., description="Customer phone number")
    address: str = Field(..., description="Customer address")
    registration_date: datetime = Field(..., description="Registration date")
    credit_score: int | None = Field(None, description="Credit score if available")
    annual_income: float | None = Field(None, description="Annual income if available")


class FeatureVectorSchema(BaseModel):
    """Schema for engineered feature vector."""

    customer_id: str = Field(..., description="Customer identifier")
    features: dict[str, float] = Field(..., description="Feature name to value mapping")
    feature_count: int = Field(..., description="Number of features")
    computed_at: datetime = Field(default_factory=datetime.now, description="Timestamp when features were computed")


class ValidationResult(BaseModel):
    """Schema for validation results."""

    is_valid: bool = Field(..., description="Whether data passed validation")
    error_count: int = Field(default=0, description="Number of errors found")
    errors: list[str] = Field(default_factory=list, description="List of error messages")
    warnings: list[str] = Field(default_factory=list, description="List of warnings")


class PipelineResult(BaseModel):
    """Schema for pipeline execution result."""

    success: bool = Field(..., description="Whether pipeline executed successfully")
    feature_matrix: dict[str, Any] | list[dict[str, Any]] | None = Field(None, description="Feature matrix (X)")
    labels: dict[str, Any] | None = Field(None, description="Labels (y)")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Pipeline metadata")
    errors: list[str] = Field(default_factory=list, description="Error messages if any")
