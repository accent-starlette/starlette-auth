import pytest


@pytest.mark.asyncio
async def test_get(client):
    response = await client.get("/auth/password/reset/complete")
    assert response.status_code == 200
