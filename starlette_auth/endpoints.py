from sqlalchemy.orm.exc import NoResultFound
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse

from .config import config
from .forms import ChangePasswordForm, LoginForm
from .tables import User


class ChangePassword(HTTPEndpoint):
    @requires(["authenticated"])
    async def get(self, request):
        template = "starlette_auth/change_password.html"
        form = ChangePasswordForm()
        context = {"request": request, "form": form}
        return config.templates.TemplateResponse(template, context)

    @requires(["authenticated"])
    async def post(self, request):
        template = "starlette_auth/change_password.html"

        data = await request.form()
        form = ChangePasswordForm(data)

        if not form.validate():
            context = {"request": request, "form": form}
            return config.templates.TemplateResponse(template, context)

        if not request.user.check_password(form.current_password.data):
            form.current_password.errors.append("Enter your current password.")
            context = {"request": request, "form": form}
            return config.templates.TemplateResponse(template, context)

        else:
            request.user.set_password(form.new_password.data)
            request.user.save()

        return RedirectResponse(config.change_pw_redirect_url)


class Login(HTTPEndpoint):
    async def get(self, request):
        template = "starlette_auth/login.html"
        form = LoginForm()
        context = {"request": request, "form": form}
        return config.templates.TemplateResponse(template, context)

    async def post(self, request):
        template = "starlette_auth/login.html"

        data = await request.form()
        form = LoginForm(data)

        if not form.validate():
            context = {"request": request, "form": form}
            return config.templates.TemplateResponse(template, context)

        try:
            user = User.query.filter(User.email == form.email.data.lower()).one()
            if user.check_password(form.password.data):
                request.session["user"] = user.id
                return RedirectResponse(config.login_redirect_url)

        except NoResultFound:
            pass

        request.session.clear()

        form.password.errors.append("Invalid email or password.")
        context = {"request": request, "form": form}

        return config.templates.TemplateResponse(template, context)


class Logout(HTTPEndpoint):
    async def get(self, request):
        request.session.clear()
        return RedirectResponse(config.logout_redirect_url)
