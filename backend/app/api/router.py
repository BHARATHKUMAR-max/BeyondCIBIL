from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.bank_connections import router as bank_connections_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.predictions import router as predictions_router
from app.api.routes.transactions import router as transactions_router

api_router = APIRouter()
api_router.include_router(auth_router, tags=["authentication"])
api_router.include_router(bank_connections_router, tags=["bank connections"])
api_router.include_router(transactions_router, tags=["transactions"])
api_router.include_router(dashboard_router, tags=["dashboard"])
api_router.include_router(predictions_router, tags=["predictions"])
