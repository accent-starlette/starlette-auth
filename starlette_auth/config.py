import typing

from starlette.datastructures import Secret
from starlette.templating import Jinja2Templates


class AppConfig:
    templates: Jinja2Templates = Jinja2Templates(directory="templates")
    change_pw_redirect_url: str = "/"
    change_pw_template: str = "starlette_auth/change_password.html"
    login_redirect_url: str = "/"
    login_template: str = "starlette_auth/login.html"
    logout_redirect_url: str = "/"
    reset_pw_redirect_url: str = "/auth/password/reset/done"
    reset_pw_template: str = "starlette_auth/password_reset.html"
    reset_pw_done_template: str = "starlette_auth/password_reset_done.html"
    reset_pw_confirm_redirect_url: str = "/auth/password/reset/complete"
    reset_pw_confirm_template: str = "starlette_auth/password_reset_confirm.html"
    reset_pw_complete_template: str = "starlette_auth/password_reset_complete.html"
    reset_pw_email_subject_template: str = ""
    reset_pw_email_template: str = ""
    reset_pw_timeout: int = 60 * 60 * 24 * 3
    secret_key: typing.Union[str, Secret] = ""


config = AppConfig()
