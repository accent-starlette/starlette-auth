import pytest


def test_logout(client, user):
    client.post(
        "/auth/login", data={"email": "user@example.com", "password": "password"}
    )

    response = client.get("/auth/logout")
    assert response.status_code == 200
    assert response.url == "http://testserver/auth/login"
