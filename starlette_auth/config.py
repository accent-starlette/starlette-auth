from starlette.templating import Jinja2Templates


class AppConfig:
    templates: Jinja2Templates = Jinja2Templates(directory="templates")
    change_pw_redirect_url = "/"
    change_pw_template = "starlette_auth/change_password.html"
    login_redirect_url = "/"
    login_template = "starlette_auth/login.html"
    logout_redirect_url = "/"
    reset_pw_template = "starlette_auth/password_reset.html"
    reset_pw_timeout = 60
    secret_key = ""


config = AppConfig()
