import pytest

from app.core.config import get_settings
from app.database.health import verify_database_connection
from app.database.session import engine


@pytest.mark.asyncio
async def test_database_connectivity() -> None:
    database_url = get_settings().database_url
    if "your-password" in database_url or "postgres:postgres@localhost" in database_url:
        pytest.skip("DATABASE_URL is not configured for an integration test")

    await verify_database_connection(engine)
