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
    reset_pw_template: str = "starlette_auth/password_reset.html"
    reset_pw_done_template: str = "starlette_auth/password_reset_done.html"
    reset_pw_redirect_url: str = "/auth/password/reset/done"
    reset_pw_timeout: int = 60
    secret_key: typing.Union[str, Secret] = ""


config = AppConfig()
