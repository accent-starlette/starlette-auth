import pytest


def test_get(client):
    response = client.get("/auth/login")
    assert response.status_code == 200


def test_can_login(client, user):
    response = client.post(
        "/auth/login", data={"email": "user@example.com", "password": "password"}
    )

    assert response.status_code == 302
    assert response.next.url == "http://testserver/"

    response = client.get("/")
    assert response.json() == {"user": "user@example.com"}


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
def test_invalid_credentials(test_data, client, user):
    response = client.post("/auth/login", data=test_data)

    assert response.status_code == 200
    assert response.url == "http://testserver/auth/login"
