from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.transaction import TransactionResponse, TransactionSyncResponse
from app.services.transaction_fetch import TransactionFetchError, TransactionFetchService
from app.services.transactions.mock_source import MockTransactionSource

router = APIRouter(prefix="/transactions")
SessionDependency = Annotated[AsyncSession, Depends(get_db)]
CurrentUserDependency = Annotated[User, Depends(get_current_user)]


def get_transaction_fetch_service(session: SessionDependency) -> TransactionFetchService:
    """Dependency seam for a future Account Aggregator transaction source."""
    return TransactionFetchService(session, MockTransactionSource())


ServiceDependency = Annotated[TransactionFetchService, Depends(get_transaction_fetch_service)]


@router.post("/sync/{bank_connection_id}", response_model=TransactionSyncResponse, status_code=status.HTTP_200_OK)
async def sync_transactions(
    bank_connection_id: UUID,
    user: CurrentUserDependency,
    service: ServiceDependency,
) -> TransactionSyncResponse:
    try:
        created, updated = await service.sync(user, bank_connection_id)
    except TransactionFetchError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return TransactionSyncResponse(created=created, updated=updated)


@router.get("", response_model=list[TransactionResponse])
async def list_transactions(
    user: CurrentUserDependency,
    service: ServiceDependency,
    bank_connection_id: UUID | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[TransactionResponse]:
    return await service.list_transactions(user, bank_connection_id, limit, offset)
