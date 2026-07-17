from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BankResponse(BaseModel):
    code: str
    name: str


class StartBankConnectionRequest(BaseModel):
    bank_code: str = Field(min_length=2, max_length=100)


class MockAuthenticationRequest(BaseModel):
    customer_id: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=128)


class OtpVerificationRequest(BaseModel):
    otp: str = Field(pattern=r"^\d{6}$")


class BankConnectionSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    bank_code: str
    status: str
    expires_at: datetime
    bank_connection_id: UUID | None


class BankConnectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    provider: str
    institution_name: str | None
    account_name: str | None
    account_mask: str | None
    currency: str
    connection_status: str
    last_synced_at: datetime | None
