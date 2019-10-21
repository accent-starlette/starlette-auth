import pytest


def test_get(client, user):
    client.post(
        "/auth/login", data={"email": "user@example.com", "password": "password"}
    )

    response = client.get("/auth/password/change")
    assert response.status_code == 200


def test_get_requires_login(client):
    client.post(
        "/auth/login", data={"email": "user@example.com", "password": "password"}
    )

    response = client.get("/auth/password/change")
    assert response.status_code == 403


def test_can_change_password(client, user):
    client.post(
        "/auth/login", data={"email": "user@example.com", "password": "password"}
    )

    response = client.post(
        "/auth/password/change",
        data={
            "current_password": "password",
            "new_password": "password1",
            "confirm_new_password": "password1",
        },
    )
    assert response.status_code == 302

    # can then use new password
    response = client.get("/auth/logout")
    assert response.status_code == 200

    response = client.post(
        "/auth/login", data={"email": "user@example.com", "password": "password1"}
    )
    assert response.status_code == 302
    assert response.next.url == "http://testserver/"


@pytest.mark.parametrize(
    "test_data",
    [
        {},
        {"current_password": "", "new_password": "", "confirm_new_password": ""},
        {"current_password": " ", "new_password": " ", "confirm_new_password": " "},
        {
            "current_password": "password",
            "new_password": "password1",
            "confirm_new_password": "password2",
        },
        {
            "current_password": "password1",
            "new_password": "password",
            "confirm_new_password": "password",
        },
    ],
)
def test_invalid(test_data, client, user):
    client.post(
        "/auth/login", data={"email": "user@example.com", "password": "password"}
    )

    response = client.post("/auth/password/change", data=test_data)
    assert response.status_code == 200
    assert response.url == "http://testserver/auth/password/change"
