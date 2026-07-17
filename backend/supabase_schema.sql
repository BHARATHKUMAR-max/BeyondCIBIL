-- BEYOND CIBIL schema through Alembic revision 20260717_03.
-- Run once in the Supabase SQL Editor against an empty project database.

BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

CREATE TABLE users (
    email VARCHAR(320) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT 'true' NOT NULL,
    id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (email)
);
CREATE INDEX ix_users_email ON users (email);

CREATE TABLE refresh_tokens (
    token_id UUID NOT NULL,
    user_id UUID NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    revoked_at TIMESTAMP WITH TIME ZONE,
    id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE,
    UNIQUE (token_id)
);
CREATE INDEX ix_refresh_tokens_token_id ON refresh_tokens (token_id);
CREATE INDEX ix_refresh_tokens_user_id ON refresh_tokens (user_id);

ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE;
CREATE INDEX ix_users_deleted_at ON users (deleted_at);
ALTER TABLE refresh_tokens ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE;
CREATE INDEX ix_refresh_tokens_deleted_at ON refresh_tokens (deleted_at);

CREATE TABLE bank_connections (
    user_id UUID NOT NULL,
    provider VARCHAR(100) NOT NULL,
    external_account_id VARCHAR(255) NOT NULL,
    institution_name VARCHAR(255),
    account_name VARCHAR(255),
    account_mask VARCHAR(8),
    currency VARCHAR(3) DEFAULT 'INR' NOT NULL,
    connection_status VARCHAR(20) DEFAULT 'pending' NOT NULL,
    access_token_encrypted VARCHAR(2048),
    last_synced_at TIMESTAMP WITH TIME ZONE,
    id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (id),
    CONSTRAINT ck_bank_connections_status CHECK (connection_status IN ('active', 'pending', 'error', 'revoked')),
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE RESTRICT
);
CREATE INDEX ix_bank_connections_deleted_at ON bank_connections (deleted_at);
CREATE INDEX ix_bank_connections_user_status ON bank_connections (user_id, connection_status);
CREATE UNIQUE INDEX ix_bank_connections_provider_external ON bank_connections (provider, external_account_id);

CREATE TABLE transactions (
    user_id UUID NOT NULL,
    bank_connection_id UUID NOT NULL,
    external_transaction_id VARCHAR(255) NOT NULL,
    amount NUMERIC(14, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'INR' NOT NULL,
    transaction_type VARCHAR(10) NOT NULL,
    category VARCHAR(100),
    merchant_name VARCHAR(255),
    description VARCHAR(1000),
    occurred_at TIMESTAMP WITH TIME ZONE NOT NULL,
    id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (id),
    CONSTRAINT ck_transactions_nonnegative_amount CHECK (amount >= 0),
    CONSTRAINT ck_transactions_type CHECK (transaction_type IN ('credit', 'debit')),
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE RESTRICT,
    FOREIGN KEY(bank_connection_id) REFERENCES bank_connections (id) ON DELETE RESTRICT
);
CREATE INDEX ix_transactions_deleted_at ON transactions (deleted_at);
CREATE INDEX ix_transactions_user_occurred ON transactions (user_id, occurred_at);
CREATE UNIQUE INDEX ix_transactions_connection_external ON transactions (bank_connection_id, external_transaction_id);

CREATE TABLE feature_vectors (
    user_id UUID NOT NULL,
    transaction_id UUID,
    feature_version VARCHAR(100) NOT NULL,
    features JSONB NOT NULL,
    period_start TIMESTAMP WITH TIME ZONE,
    period_end TIMESTAMP WITH TIME ZONE,
    id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE RESTRICT,
    FOREIGN KEY(transaction_id) REFERENCES transactions (id) ON DELETE SET NULL
);
CREATE INDEX ix_feature_vectors_deleted_at ON feature_vectors (deleted_at);
CREATE INDEX ix_feature_vectors_user_version ON feature_vectors (user_id, feature_version);
CREATE INDEX ix_feature_vectors_transaction ON feature_vectors (transaction_id);

CREATE TABLE alternative_credit_scores (
    user_id UUID NOT NULL,
    score NUMERIC(7, 2) NOT NULL,
    model_version VARCHAR(100) NOT NULL,
    score_components JSONB NOT NULL,
    calculated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (id),
    CONSTRAINT ck_alternative_credit_scores_range CHECK (score BETWEEN 0 AND 1000),
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE RESTRICT
);
CREATE INDEX ix_alternative_credit_scores_deleted_at ON alternative_credit_scores (deleted_at);
CREATE INDEX ix_alternative_scores_user_calculated ON alternative_credit_scores (user_id, calculated_at);

CREATE TABLE prediction_history (
    user_id UUID NOT NULL,
    alternative_credit_score_id UUID,
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(100) NOT NULL,
    prediction_type VARCHAR(100) NOT NULL,
    input_snapshot JSONB NOT NULL,
    prediction JSONB NOT NULL,
    confidence NUMERIC(5, 4),
    id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (id),
    CONSTRAINT ck_prediction_history_confidence CHECK (confidence IS NULL OR confidence BETWEEN 0 AND 1),
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE RESTRICT,
    FOREIGN KEY(alternative_credit_score_id) REFERENCES alternative_credit_scores (id) ON DELETE SET NULL
);
CREATE INDEX ix_prediction_history_deleted_at ON prediction_history (deleted_at);
CREATE INDEX ix_prediction_history_user_created ON prediction_history (user_id, created_at);
CREATE INDEX ix_prediction_history_model ON prediction_history (model_name, model_version);

CREATE TABLE recommendations (
    user_id UUID NOT NULL,
    prediction_id UUID,
    category VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(2000) NOT NULL,
    action_url VARCHAR(2048),
    priority INTEGER DEFAULT '3' NOT NULL,
    status VARCHAR(20) DEFAULT 'active' NOT NULL,
    metadata JSONB,
    expires_at TIMESTAMP WITH TIME ZONE,
    id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (id),
    CONSTRAINT ck_recommendations_priority CHECK (priority BETWEEN 1 AND 5),
    CONSTRAINT ck_recommendations_status CHECK (status IN ('active', 'dismissed', 'completed', 'expired')),
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE RESTRICT,
    FOREIGN KEY(prediction_id) REFERENCES prediction_history (id) ON DELETE SET NULL
);
CREATE INDEX ix_recommendations_deleted_at ON recommendations (deleted_at);
CREATE INDEX ix_recommendations_user_status ON recommendations (user_id, status);

CREATE TABLE bank_connection_sessions (
    user_id UUID NOT NULL,
    bank_code VARCHAR(100) NOT NULL,
    provider_reference VARCHAR(255) NOT NULL,
    status VARCHAR(30) DEFAULT 'auth_required' NOT NULL,
    customer_id VARCHAR(255),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    consented_at TIMESTAMP WITH TIME ZONE,
    bank_connection_id UUID,
    provider_payload JSONB,
    id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (id),
    CONSTRAINT ck_bank_connection_sessions_status CHECK (status IN ('auth_required', 'otp_pending', 'consent_required', 'completed', 'failed', 'expired')),
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE RESTRICT,
    FOREIGN KEY(bank_connection_id) REFERENCES bank_connections (id) ON DELETE SET NULL,
    UNIQUE (bank_connection_id)
);
CREATE INDEX ix_bank_connection_sessions_deleted_at ON bank_connection_sessions (deleted_at);
CREATE INDEX ix_bank_connection_sessions_user_status ON bank_connection_sessions (user_id, status);
CREATE UNIQUE INDEX ix_bank_connection_sessions_reference ON bank_connection_sessions (provider_reference);

INSERT INTO alembic_version (version_num) VALUES ('20260717_03');

COMMIT;
