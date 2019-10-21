import pytest

from starlette_auth import config


def test_get(client):
    response = client.get("/auth/password/reset")
    assert response.status_code == 200
    assert "form" in response.context
    assert "request" in response.context


def test_post_redirects(client):
    # its important here that the post will redirect regardless
    # of whether the user exists or not so we specifally done create the user
    response = client.post("/auth/password/reset", data={"email": "user@example.com"})
    assert response.status_code == 302
    assert response.next.url == "http://testserver/auth/password/reset/done"


def test_post_redirect_url_is_using_config(client):
    config.reset_pw_redirect_url = "/foo"
    response = client.post("/auth/password/reset", data={"email": "user@example.com"})
    assert response.status_code == 302
    assert response.next.url == "http://testserver/foo"


@pytest.mark.parametrize(
    "test_data",
    [
        {},
        {"email": ""},
        {"email": " "},
        {"email": "invalid"},
        {"email": "user@invalid"},
    ],
)
def test_invalid_data(test_data, client, user):
    response = client.post("/auth/password/reset", data=test_data)

    assert response.status_code == 200
    assert response.url == "http://testserver/auth/password/reset"
