from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.dashboard import DashboardResponse, FinancialSummary, Prediction
from app.services.dashboard import DashboardService

router = APIRouter(prefix="/dashboard")
SessionDependency = Annotated[AsyncSession, Depends(get_db)]
CurrentUserDependency = Annotated[User, Depends(get_current_user)]


def get_dashboard_service(session: SessionDependency) -> DashboardService:
    """Dependency injection for dashboard service."""
    return DashboardService(session)


ServiceDependency = Annotated[DashboardService, Depends(get_dashboard_service)]


@router.get("", response_model=DashboardResponse)
async def get_dashboard(
    user: CurrentUserDependency,
    service: ServiceDependency,
) -> DashboardResponse:
    """Get complete dashboard data including credit score, financial summary, and predictions."""
    return await service.get_dashboard(user)


@router.get("/predictions", response_model=list[Prediction])
async def get_predictions(
    user: CurrentUserDependency,
    service: ServiceDependency,
) -> list[Prediction]:
    """Get recent prediction history for the authenticated user."""
    return await service.get_predictions_only(user)


@router.get("/financial-summary", response_model=FinancialSummary)
async def get_financial_summary(
    user: CurrentUserDependency,
    service: ServiceDependency,
) -> FinancialSummary:
    """Get financial summary including transaction metrics and spending patterns."""
    return await service.get_financial_summary_only(user)
