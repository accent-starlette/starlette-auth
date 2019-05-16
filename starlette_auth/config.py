from starlette.templating import Jinja2Templates
from typesystem import Jinja2Forms


class AppConfig:
    templates: Jinja2Templates = Jinja2Templates(directory="templates")
    forms: Jinja2Forms = Jinja2Forms(directory="templates")
    change_pw_redirect_url = "/"
    login_redirect_url = "/"
    logout_redirect_url = "/"


config = AppConfig()
