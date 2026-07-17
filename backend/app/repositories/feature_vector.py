import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.feature_vector import FeatureVector


class FeatureVectorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_latest_by_user(self, user_id: uuid.UUID) -> FeatureVector | None:
        result = await self.session.execute(
            select(FeatureVector)
            .where(FeatureVector.user_id == user_id, FeatureVector.deleted_at.is_(None))
            .order_by(FeatureVector.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_by_user_and_version(self, user_id: uuid.UUID, feature_version: str) -> list[FeatureVector]:
        result = await self.session.execute(
            select(FeatureVector)
            .where(
                FeatureVector.user_id == user_id,
                FeatureVector.feature_version == feature_version,
                FeatureVector.deleted_at.is_(None),
            )
            .order_by(FeatureVector.created_at.desc())
        )
        return list(result.scalars().all())

    def add(self, feature_vector: FeatureVector) -> None:
        self.session.add(feature_vector)
