import uuid
from datetime import UTC, datetime

import pytest

from app.models.bank_connection import BankConnection
from app.services.transactions.mock_source import MockTransactionSource


@pytest.mark.asyncio
async def test_mock_source_returns_deterministic_transactions() -> None:
    connection = BankConnection(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        provider="mock",
        external_account_id="mock-account",
    )

    transactions = await MockTransactionSource().fetch_transactions(connection)

    assert len(transactions) == 3
    assert {item.transaction_type for item in transactions} == {"credit", "debit"}
    assert all(item.currency == "INR" for item in transactions)


@pytest.mark.asyncio
async def test_mock_source_respects_sync_cursor() -> None:
    connection = BankConnection(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        provider="mock",
        external_account_id="mock-account",
    )

    transactions = await MockTransactionSource().fetch_transactions(
        connection, datetime(2026, 7, 5, 4, 15, tzinfo=UTC)
    )

    assert len(transactions) == 1
