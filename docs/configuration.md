# Configuration

There are several parts of the package that require config options.

Configuration should be stored in environment variables, or in a ".env" file that is not committed to source control.

Please refer to [docs](https://github.com/accent-starlette/starlette-auth/blob/master/starlette_auth/config.py) on how to set this up within a config.py file as per example:

```python

import typing

from starlette.config import Config
from starlette.datastructures import Secret
from starlette.templating import Jinja2Templates


class AppConfig:
    _config = Config(".env")

    # templating configuration
    templates: Jinja2Templates = Jinja2Templates(directory="templates")
    change_pw_template: str = _config(
        "CHANGE_PW_TEMPLATE", default="starlette_auth/change_password.html"
    )
    login_template: str = _config("LOGIN_TEMPLATE", default="starlette_auth/login.html")
    reset_pw_template: str = _config(
        "RESET_PW_TEMPLATE", default="starlette_auth/password_reset.html"
    )
    reset_pw_done_template: str = _config(
        "RESET_PW_DONE_TEMPLATE", default="starlette_auth/password_reset_done.html"
    )
    reset_pw_confirm_template: str = _config(
        "RESET_PW_CONFIRM_TEMPLATE",
        default="starlette_auth/password_reset_confirm.html",
    )
    reset_pw_complete_template: str = _config(
        "RESET_PW_COMPLETE_TEMPLATE",
        default="starlette_auth/password_reset_complete.html",
    )

    # email templating configuration
    reset_pw_email_subject_template: str = _config(
        "RESET_PW_EMAIL_SUBJECT_TEMPLATE", default=""
    )
    reset_pw_email_template: str = _config("RESET_PW_EMAIL_TEMPLATE", default="")
    reset_pw_html_email_template: str = _config(
        "RESET_PW_HTML_EMAIL_TEMPLATE", default=""
    )

    # url configuration
    change_pw_redirect_url: str = _config("CHANGE_PW_REDIRECT_URL", default="/")
    login_redirect_url: str = _config("LOGIN_REDIRECT_URL", default="/")
    logout_redirect_url: str = _config("LOGOUT_REDIRECT_URL", default="/")

    # general
    reset_pw_timeout: int = _config(
        "RESET_PW_TIMEOUT", cast=int, default=(60 * 60 * 24 * 3)
    )
    secret_key: typing.Union[str, Secret] = _config(
        "SECRET_KEY", cast=Secret, default=""
    )


config = AppConfig()


```