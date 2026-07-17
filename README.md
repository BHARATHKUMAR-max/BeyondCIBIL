# BEYOND CIBIL Backend

Production-oriented FastAPI foundation for the BEYOND CIBIL AI fintech platform.

## Stack

- Python 3.12+, FastAPI, Pydantic v2
- Async SQLAlchemy 2.x, Alembic, PostgreSQL/Supabase
- Uvicorn, Docker, structured JSON logging

## Setup

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`. Check `GET /health`; interactive documentation is at `/docs`.

## Configuration

All application settings are environment based. Start from `.env.example`; set `DATABASE_URL` to the async PostgreSQL connection string supplied by Supabase. Use `BEYOND_CIBIL_DEBUG` for the debug flag to prevent collisions with host-machine variables. Pool behavior is configured through `DB_POOL_SIZE`, `DB_MAX_OVERFLOW`, `DB_POOL_TIMEOUT`, and `DB_POOL_RECYCLE`.

## Database migrations

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

ORM entities inherit `BaseModel` for UUID primary keys and UTC database-managed timestamps; repositories receive an `AsyncSession` through dependency injection.

## Authentication

JWT authentication endpoints are versioned under `/api/v1/auth`:

- `POST /register` creates a user with a bcrypt password hash.
- `POST /login` returns access and refresh tokens.
- `POST /refresh` rotates a valid refresh token.
- `POST /logout` revokes a refresh token.
- `GET /me` requires an `Authorization: Bearer <access_token>` header.

Apply the authentication schema with `python -m alembic upgrade head` once `DATABASE_URL` is valid.

## Mock bank connection

All bank-connection routes require an access token and are available under `/api/v1/bank-connections`. The mock flow is: list banks, create a session, authenticate with non-empty demo credentials, verify the fixed mock OTP `123456`, then submit consent. No real banking API is called. The service targets the `BankConnector` contract, so an Account Aggregator adapter can replace `MockBankConnector` without changing routes or application services.

## Mock transaction fetching

`POST /api/v1/transactions/sync/{bank_connection_id}` fetches and persists the mock transaction dataset for an active connection. `GET /api/v1/transactions` lists the authenticated user's stored transactions. The fetch service depends on the `TransactionSource` contract, allowing a real provider to replace `MockTransactionSource` later without changing the repository or API.

## ML service skeleton

`app/ml` defines predictor, attribution, and recommendation contracts plus dependency-injected services. It contains no trained model, model-loading code, or training workflow; future adapters can implement these contracts independently.

## Architecture

`api` owns HTTP routing; `services` coordinates use cases; `repositories` own persistence; `models` contains ORM entities; and `schemas` contains request/response DTOs. Core configuration and logging, database infrastructure, middleware, utilities, ML integration points, and tests remain isolated in their respective packages.
