import pytest

from starlette_auth import config


def test_get(client):
    response = client.get("/auth/password/reset")
    assert response.status_code == 200
    assert "form" in response.context
    assert "request" in response.context


def test_post_redirects(client, monkeypatch):
    # its important here that the post will redirect regardless
    # of whether the user exists or not so we specifally dont use a valid email

    def fake_send(msg):
        raise Exception("An email should not have been sent")

    monkeypatch.setattr("starlette_auth.forms.send_message", fake_send)

    response = client.post("/auth/password/reset", data={"email": "user@example.com"})
    assert response.status_code == 302
    assert response.next.url == "http://testserver/auth/password/reset/done"


def test_email_not_sent_if_user_is_not_active(client, user, monkeypatch):
    user.is_active = False
    user.save()

    def fake_send(msg):
        raise Exception("An email should not have been sent")

    monkeypatch.setattr("starlette_auth.forms.send_message", fake_send)

    response = client.post("/auth/password/reset", data={"email": "user@example.com"})
    assert response.status_code == 302
    assert response.next.url == "http://testserver/auth/password/reset/done"


def test_txt_email_sent_if_user_exists(client, user, monkeypatch):
    def fake_send(msg):
        assert msg.get_content_maintype() == "text"
        assert msg["To"] == user.email
        assert msg["Subject"] == "Change Password at example.com"
        assert "http://testserver/auth/password/reset" in msg.as_string()

    monkeypatch.setattr("starlette_auth.forms.send_message", fake_send)

    response = client.post("/auth/password/reset", data={"email": user.email})
    assert response.status_code == 302
    assert response.next.url == "http://testserver/auth/password/reset/done"


def test_html_email_sent_if_template_is_defined(client, user, monkeypatch):
    def fake_send(msg):
        assert msg.get_content_maintype() == "multipart"
        assert msg["To"] == user.email
        assert msg["Subject"] == "Change Password at example.com"
        assert '<a href="http://testserver/auth/password/reset' in msg.as_string()

    monkeypatch.setattr("starlette_auth.forms.send_message", fake_send)

    config.reset_pw_html_email_template = "password_reset_body.html"

    response = client.post("/auth/password/reset", data={"email": user.email})
    assert response.status_code == 302
    assert response.next.url == "http://testserver/auth/password/reset/done"


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
