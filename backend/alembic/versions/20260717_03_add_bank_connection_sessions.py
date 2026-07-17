"""add bank connection sessions

Revision ID: 20260717_03
Revises: 20260717_02
Create Date: 2026-07-17
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260717_03"
down_revision: Union[str, Sequence[str], None] = "20260717_02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bank_connection_sessions",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("bank_code", sa.String(length=100), nullable=False),
        sa.Column("provider_reference", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="auth_required", nullable=False),
        sa.Column("customer_id", sa.String(length=255), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consented_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("bank_connection_id", sa.Uuid(), nullable=True),
        sa.Column("provider_payload", postgresql.JSONB(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "status IN ('auth_required', 'otp_pending', 'consent_required', 'completed', 'failed', 'expired')",
            name="ck_bank_connection_sessions_status",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["bank_connection_id"], ["bank_connections.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("bank_connection_id"),
    )
    op.create_index("ix_bank_connection_sessions_deleted_at", "bank_connection_sessions", ["deleted_at"])
    op.create_index("ix_bank_connection_sessions_user_status", "bank_connection_sessions", ["user_id", "status"])
    op.create_index("ix_bank_connection_sessions_reference", "bank_connection_sessions", ["provider_reference"], unique=True)


def downgrade() -> None:
    op.drop_table("bank_connection_sessions")
