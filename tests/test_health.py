import pytest
from httpx import AsyncClient, ASGITransport

from main import app

@pytest.mark.asyncio
async def test_ping():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        result = await ac.get("/ping")
        assert result.status_code == 200
        assert result.json() == {"message": "pong"}