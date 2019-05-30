from starlette.templating import Jinja2Templates


class AppConfig:
    templates: Jinja2Templates = Jinja2Templates(directory="templates")
    change_pw_redirect_url = "/"
    login_redirect_url = "/"
    logout_redirect_url = "/"


config = AppConfig()
