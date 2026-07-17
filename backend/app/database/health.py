from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine


async def verify_database_connection(engine: AsyncEngine) -> None:
    """Raise an exception when the database cannot accept a basic query."""
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
