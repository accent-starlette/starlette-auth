import pytest


@pytest.mark.asyncio
async def test_get(client):
    response = await client.get("/auth/login")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_can_login(client, user):
    response = await client.post(
        "/auth/login", data={"email": "user@example.com", "password": "password"}
    )

    assert response.status_code == 200
    assert response.url == "http://testserver/"

    response = await client.get("/")
    assert response.json() == {"user": "user@example.com"}


@pytest.mark.asyncio
async def test_user_last_login_set(client, user):
    assert user.last_login is None
    response = await client.post(
        "/auth/login", data={"email": "user@example.com", "password": "password"}
    )
    await user.refresh_from_db()
    assert user.last_login is not None


@pytest.mark.parametrize(
    "test_data",
    [
        {},
        {"email": "", "password": ""},
        {"email": " ", "password": " "},
        {"email": "user@example.com", "password": "password1"},
        {"email": "bob@example.com", "password": "password"},
    ],
)
@pytest.mark.asyncio
async def test_invalid_credentials(test_data, client, user):
    response = await client.post("/auth/login", data=test_data)

    assert response.status_code == 200
    assert response.url == "http://testserver/auth/login"
