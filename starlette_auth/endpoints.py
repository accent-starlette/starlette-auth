from sqlalchemy.orm.exc import NoResultFound
from starlette import status
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse

from .config import config
from .forms import ChangePasswordForm, LoginForm, TwoFactorVerifyForm
from .tables import User


class ChangePassword(HTTPEndpoint):
    @requires(["authenticated"])
    async def get(self, request):
        template = config.change_pw_template

        form = ChangePasswordForm()
        context = {"request": request, "form": form}
        return config.templates.TemplateResponse(template, context)

    @requires(["authenticated"])
    async def post(self, request):
        template = config.change_pw_template

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

        return RedirectResponse(
            url=config.change_pw_redirect_url, status_code=status.HTTP_302_FOUND
        )


class Login(HTTPEndpoint):
    async def get(self, request):
        template = config.login_template

        form = LoginForm()
        context = {"request": request, "form": form}
        return config.templates.TemplateResponse(template, context)

    async def post(self, request):
        template = config.login_template

        data = await request.form()
        form = LoginForm(data)

        if not form.validate():
            context = {"request": request, "form": form}
            return config.templates.TemplateResponse(template, context)

        try:
            user = User.query.filter(User.email == form.email.data.lower()).one()
            if user.check_password(form.password.data):
                request.session["user"] = user.id
                return RedirectResponse(
                    url=config.login_redirect_url, status_code=status.HTTP_302_FOUND
                )

        except NoResultFound:
            pass

        request.session.clear()

        form.password.errors.append("Invalid email or password.")
        context = {"request": request, "form": form}

        return config.templates.TemplateResponse(template, context)


class Logout(HTTPEndpoint):
    async def get(self, request):
        request.session.clear()
        return RedirectResponse(
            url=config.logout_redirect_url, status_code=status.HTTP_302_FOUND
        )


class TwoFactorVerify(HTTPEndpoint):
    @requires(["authenticated"])
    async def get(self, request):
        template = config.two_factor_template

        form = TwoFactorVerifyForm()
        context = {"request": request, "form": form}
        return config.templates.TemplateResponse(template, context)

    @requires(["authenticated"])
    async def post(self, request):
        template = config.two_factor_template

        data = await request.form()
        form = TwoFactorVerifyForm(data)

        if not form.validate():
            context = {"request": request, "form": form}
            return config.templates.TemplateResponse(template, context)

        if request.user.check_two_factor(form.authentication_code.data):
            if not request.user.two_factor_verified:
                request.user.two_factor_verified = True
                request.user.save()
            request.session["two_factor_verified"] = True
            return RedirectResponse(
                url=config.login_redirect_url, status_code=status.HTTP_302_FOUND
            )

        form.authentication_code.errors.append("Invalid authentication code.")
        context = {"request": request, "form": form}

        return config.templates.TemplateResponse(template, context)
