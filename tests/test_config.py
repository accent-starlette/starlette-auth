from starlette_auth.config import AppConfig


def test_defaults():
    config = AppConfig()
    assert config.change_pw_template == "starlette_auth/change_password.html"
    assert config.login_template == "starlette_auth/login.html"
    assert config.reset_pw_template == "starlette_auth/password_reset.html"
    assert config.reset_pw_done_template == "starlette_auth/password_reset_done.html"
    assert (
        config.reset_pw_confirm_template == "starlette_auth/password_reset_confirm.html"
    )
    assert (
        config.reset_pw_complete_template
        == "starlette_auth/password_reset_complete.html"
    )
    assert config.reset_pw_email_subject_template == ""
    assert config.reset_pw_email_template == ""
    assert config.reset_pw_html_email_template == ""
    assert config.change_pw_redirect_url == "/"
    assert config.login_redirect_url == "/"
    assert config.logout_redirect_url == "/"
    assert config.reset_pw_timeout == 60 * 60 * 24 * 3
    assert str(config.secret_key) == ""
