import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.recommendation import Recommendation


class RecommendationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_active_by_user(self, user_id: uuid.UUID) -> list[Recommendation]:
        result = await self.session.execute(
            select(Recommendation)
            .where(
                Recommendation.user_id == user_id,
                Recommendation.status == "active",
                Recommendation.deleted_at.is_(None),
            )
            .order_by(Recommendation.priority.asc(), Recommendation.created_at.desc())
        )
        return list(result.scalars().all())

    async def count_active_by_user(self, user_id: uuid.UUID) -> int:
        result = await self.session.execute(
            select(Recommendation)
            .where(
                Recommendation.user_id == user_id,
                Recommendation.status == "active",
                Recommendation.deleted_at.is_(None),
            )
            .count()
        )
        return result.scalar() or 0

    def add(self, recommendation: Recommendation) -> None:
        self.session.add(recommendation)
