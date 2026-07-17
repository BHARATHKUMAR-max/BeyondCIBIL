from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.bank_connection import (
    BankConnectionResponse,
    BankConnectionSessionResponse,
    BankResponse,
    MockAuthenticationRequest,
    OtpVerificationRequest,
    StartBankConnectionRequest,
)
from app.services.bank_connection import BankConnectionFlowError, BankConnectionService
from app.services.banking.mock_connector import MockBankConnector

router = APIRouter(prefix="/bank-connections")
SessionDependency = Annotated[AsyncSession, Depends(get_db)]
CurrentUserDependency = Annotated[User, Depends(get_current_user)]


def get_bank_connection_service(session: SessionDependency) -> BankConnectionService:
    """Dependency seam for replacing MockBankConnector with an AA connector."""
    return BankConnectionService(session, MockBankConnector())


ServiceDependency = Annotated[BankConnectionService, Depends(get_bank_connection_service)]


@router.get("/banks", response_model=list[BankResponse])
async def list_banks(_: CurrentUserDependency, service: ServiceDependency) -> list[BankResponse]:
    return [BankResponse(code=bank.code, name=bank.name) for bank in service.list_banks()]


@router.post("/sessions", response_model=BankConnectionSessionResponse, status_code=status.HTTP_201_CREATED)
async def start_connection(payload: StartBankConnectionRequest, user: CurrentUserDependency, service: ServiceDependency) -> BankConnectionSessionResponse:
    try:
        return await service.start(user, payload.bank_code.lower())
    except BankConnectionFlowError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/sessions/{session_id}/authenticate", response_model=BankConnectionSessionResponse)
async def authenticate(session_id: UUID, payload: MockAuthenticationRequest, user: CurrentUserDependency, service: ServiceDependency) -> BankConnectionSessionResponse:
    try:
        return await service.authenticate(user, session_id, payload.customer_id, payload.password)
    except BankConnectionFlowError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/sessions/{session_id}/verify-otp", response_model=BankConnectionSessionResponse)
async def verify_otp(session_id: UUID, payload: OtpVerificationRequest, user: CurrentUserDependency, service: ServiceDependency) -> BankConnectionSessionResponse:
    try:
        return await service.verify_otp(user, session_id, payload.otp)
    except BankConnectionFlowError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/sessions/{session_id}/consent", response_model=BankConnectionSessionResponse)
async def grant_consent(session_id: UUID, user: CurrentUserDependency, service: ServiceDependency) -> BankConnectionSessionResponse:
    try:
        return await service.grant_consent(user, session_id)
    except BankConnectionFlowError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("", response_model=list[BankConnectionResponse])
async def list_connections(user: CurrentUserDependency, service: ServiceDependency) -> list[BankConnectionResponse]:
    return await service.list_connections(user)
