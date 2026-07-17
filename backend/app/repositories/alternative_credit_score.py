import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alternative_credit_score import AlternativeCreditScore


class AlternativeCreditScoreRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_user_id(self, user_id: uuid.UUID) -> AlternativeCreditScore | None:
        result = await self.session.execute(
            select(AlternativeCreditScore)
            .where(AlternativeCreditScore.user_id == user_id, AlternativeCreditScore.deleted_at.is_(None))
            .order_by(AlternativeCreditScore.calculated_at.desc())
        )
        return result.scalar_one_or_none()

    async def get_latest_by_user(self, user_id: uuid.UUID) -> AlternativeCreditScore | None:
        result = await self.session.execute(
            select(AlternativeCreditScore)
            .where(AlternativeCreditScore.user_id == user_id, AlternativeCreditScore.deleted_at.is_(None))
            .order_by(AlternativeCreditScore.calculated_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    def add(self, score: AlternativeCreditScore) -> None:
        self.session.add(score)
