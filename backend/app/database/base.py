import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Uuid, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""


class UUIDTimestampMixin:
    """Common UUID identity and lifecycle columns for persistent entities."""

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"), nullable=False
    )


class SoftDeleteMixin:
    """Marks records as deleted without removing their audit history."""

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

    def soft_delete(self) -> None:
        self.deleted_at = datetime.now(UTC)


class BaseModel(UUIDTimestampMixin, SoftDeleteMixin, Base):
    """Abstract base model for future application entities."""

    __abstract__ = True
