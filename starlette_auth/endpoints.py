from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from starlette import status
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from .config import config
from .forms import (
    ChangePasswordForm,
    LoginForm,
    PasswordResetConfirmForm,
    PasswordResetForm,
)
from .tables import User
from .tokens import token_generator
from .utils.http import urlsafe_base64_decode


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
                user.last_login = datetime.utcnow()
                user.save()
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


class PasswordReset(HTTPEndpoint):
    async def get(self, request):
        template = config.reset_pw_template

        form = PasswordResetForm()
        context = {"request": request, "form": form}
        return config.templates.TemplateResponse(template, context)

    async def post(self, request):
        template = config.reset_pw_template

        data = await request.form()
        form = PasswordResetForm(data)

        if not form.validate():
            context = {"request": request, "form": form}
            return config.templates.TemplateResponse(template, context)

        user = User.query.filter(User.email == form.email.data).one_or_none()
        if user and user.is_active:
            await form.send_email(request)

        return RedirectResponse(
            url=config.reset_pw_redirect_url, status_code=status.HTTP_302_FOUND
        )


class PasswordResetDone(HTTPEndpoint):
    async def get(self, request):
        template = config.reset_pw_done_template

        context = {"request": request}
        return config.templates.TemplateResponse(template, context)


class PasswordResetConfirm(HTTPEndpoint):
    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.query.get(uid)
        except:
            user = None
        return user

    async def get(self, request):
        template = config.reset_pw_confirm_template

        uidb64 = request.path_params["uidb64"]
        token = request.path_params["token"]

        user = self.get_user(uidb64)

        if not user or not user.is_active:
            raise HTTPException(status_code=404)

        if not token_generator.check_token(user, token):
            raise HTTPException(status_code=404)

        form = PasswordResetConfirmForm()
        context = {"request": request, "form": form}
        return config.templates.TemplateResponse(template, context)

    async def post(self, request):
        template = config.reset_pw_confirm_template

        uidb64 = request.path_params["uidb64"]
        token = request.path_params["token"]

        user = self.get_user(uidb64)

        if not user or not user.is_active:
            raise HTTPException(status_code=404)

        if not token_generator.check_token(user, token):
            raise HTTPException(status_code=404)

        data = await request.form()
        form = PasswordResetConfirmForm(data)

        if not form.validate():
            context = {"request": request, "form": form}
            return config.templates.TemplateResponse(template, context)

        user.set_password(form.new_password.data)
        user.save()

        return RedirectResponse(
            url=config.reset_pw_confirm_redirect_url, status_code=status.HTTP_302_FOUND
        )


class PasswordResetComplete(HTTPEndpoint):
    async def get(self, request):
        template = config.reset_pw_complete_template

        context = {"request": request}
        return config.templates.TemplateResponse(template, context)
