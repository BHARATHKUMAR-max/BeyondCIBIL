"""add fintech domain models

Revision ID: 20260717_02
Revises: 20260717_01
Create Date: 2026-07-17
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260717_02"
down_revision: Union[str, Sequence[str], None] = "20260717_01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _audit_columns() -> list[sa.Column]:
    return [
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    ]


def upgrade() -> None:
    op.add_column("users", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index("ix_users_deleted_at", "users", ["deleted_at"])
    op.add_column("refresh_tokens", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index("ix_refresh_tokens_deleted_at", "refresh_tokens", ["deleted_at"])

    op.create_table(
        "bank_connections",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("provider", sa.String(length=100), nullable=False),
        sa.Column("external_account_id", sa.String(length=255), nullable=False),
        sa.Column("institution_name", sa.String(length=255), nullable=True),
        sa.Column("account_name", sa.String(length=255), nullable=True),
        sa.Column("account_mask", sa.String(length=8), nullable=True),
        sa.Column("currency", sa.String(length=3), server_default="INR", nullable=False),
        sa.Column("connection_status", sa.String(length=20), server_default="pending", nullable=False),
        sa.Column("access_token_encrypted", sa.String(length=2048), nullable=True),
        sa.Column("last_synced_at", sa.DateTime(timezone=True), nullable=True),
        *_audit_columns(),
        sa.CheckConstraint("connection_status IN ('active', 'pending', 'error', 'revoked')", name="ck_bank_connections_status"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_bank_connections_deleted_at", "bank_connections", ["deleted_at"])
    op.create_index("ix_bank_connections_user_status", "bank_connections", ["user_id", "connection_status"])
    op.create_index("ix_bank_connections_provider_external", "bank_connections", ["provider", "external_account_id"], unique=True)

    op.create_table(
        "transactions",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("bank_connection_id", sa.Uuid(), nullable=False),
        sa.Column("external_transaction_id", sa.String(length=255), nullable=False),
        sa.Column("amount", sa.Numeric(precision=14, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=3), server_default="INR", nullable=False),
        sa.Column("transaction_type", sa.String(length=10), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("merchant_name", sa.String(length=255), nullable=True),
        sa.Column("description", sa.String(length=1000), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        *_audit_columns(),
        sa.CheckConstraint("amount >= 0", name="ck_transactions_nonnegative_amount"),
        sa.CheckConstraint("transaction_type IN ('credit', 'debit')", name="ck_transactions_type"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["bank_connection_id"], ["bank_connections.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_transactions_deleted_at", "transactions", ["deleted_at"])
    op.create_index("ix_transactions_user_occurred", "transactions", ["user_id", "occurred_at"])
    op.create_index("ix_transactions_connection_external", "transactions", ["bank_connection_id", "external_transaction_id"], unique=True)

    op.create_table(
        "feature_vectors",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("transaction_id", sa.Uuid(), nullable=True),
        sa.Column("feature_version", sa.String(length=100), nullable=False),
        sa.Column("features", postgresql.JSONB(), nullable=False),
        sa.Column("period_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("period_end", sa.DateTime(timezone=True), nullable=True),
        *_audit_columns(),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["transaction_id"], ["transactions.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_feature_vectors_deleted_at", "feature_vectors", ["deleted_at"])
    op.create_index("ix_feature_vectors_user_version", "feature_vectors", ["user_id", "feature_version"])
    op.create_index("ix_feature_vectors_transaction", "feature_vectors", ["transaction_id"])

    op.create_table(
        "alternative_credit_scores",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("score", sa.Numeric(precision=7, scale=2), nullable=False),
        sa.Column("model_version", sa.String(length=100), nullable=False),
        sa.Column("score_components", postgresql.JSONB(), nullable=False),
        sa.Column("calculated_at", sa.DateTime(timezone=True), nullable=False),
        *_audit_columns(),
        sa.CheckConstraint("score BETWEEN 0 AND 1000", name="ck_alternative_credit_scores_range"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_alternative_credit_scores_deleted_at", "alternative_credit_scores", ["deleted_at"])
    op.create_index("ix_alternative_scores_user_calculated", "alternative_credit_scores", ["user_id", "calculated_at"])

    op.create_table(
        "prediction_history",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("alternative_credit_score_id", sa.Uuid(), nullable=True),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column("model_version", sa.String(length=100), nullable=False),
        sa.Column("prediction_type", sa.String(length=100), nullable=False),
        sa.Column("input_snapshot", postgresql.JSONB(), nullable=False),
        sa.Column("prediction", postgresql.JSONB(), nullable=False),
        sa.Column("confidence", sa.Numeric(precision=5, scale=4), nullable=True),
        *_audit_columns(),
        sa.CheckConstraint("confidence IS NULL OR confidence BETWEEN 0 AND 1", name="ck_prediction_history_confidence"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["alternative_credit_score_id"], ["alternative_credit_scores.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_prediction_history_deleted_at", "prediction_history", ["deleted_at"])
    op.create_index("ix_prediction_history_user_created", "prediction_history", ["user_id", "created_at"])
    op.create_index("ix_prediction_history_model", "prediction_history", ["model_name", "model_version"])

    op.create_table(
        "recommendations",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("prediction_id", sa.Uuid(), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=2000), nullable=False),
        sa.Column("action_url", sa.String(length=2048), nullable=True),
        sa.Column("priority", sa.Integer(), server_default="3", nullable=False),
        sa.Column("status", sa.String(length=20), server_default="active", nullable=False),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        *_audit_columns(),
        sa.CheckConstraint("priority BETWEEN 1 AND 5", name="ck_recommendations_priority"),
        sa.CheckConstraint("status IN ('active', 'dismissed', 'completed', 'expired')", name="ck_recommendations_status"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["prediction_id"], ["prediction_history.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_recommendations_deleted_at", "recommendations", ["deleted_at"])
    op.create_index("ix_recommendations_user_status", "recommendations", ["user_id", "status"])


def downgrade() -> None:
    op.drop_table("recommendations")
    op.drop_table("prediction_history")
    op.drop_table("alternative_credit_scores")
    op.drop_table("feature_vectors")
    op.drop_table("transactions")
    op.drop_table("bank_connections")
    op.drop_index("ix_refresh_tokens_deleted_at", table_name="refresh_tokens")
    op.drop_column("refresh_tokens", "deleted_at")
    op.drop_index("ix_users_deleted_at", table_name="users")
    op.drop_column("users", "deleted_at")
