import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.prediction_history import PredictionHistory


class PredictionHistoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_user_id(self, user_id: uuid.UUID, limit: int = 10) -> list[PredictionHistory]:
        result = await self.session.execute(
            select(PredictionHistory)
            .where(PredictionHistory.user_id == user_id, PredictionHistory.deleted_at.is_(None))
            .order_by(PredictionHistory.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_id(self, prediction_id: uuid.UUID) -> PredictionHistory | None:
        result = await self.session.execute(
            select(PredictionHistory).where(
                PredictionHistory.id == prediction_id, PredictionHistory.deleted_at.is_(None)
            )
        )
        return result.scalar_one_or_none()

    def add(self, prediction: PredictionHistory) -> None:
        self.session.add(prediction)
