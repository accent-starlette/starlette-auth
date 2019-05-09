from sqlalchemy.orm.exc import NoResultFound
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse
from typesystem import Message, ValidationError

from starlette_auth.config import config
from starlette_auth.schemas import ChangePasswordSchema, LoginSchema
from starlette_auth.tables import User


class ChangePassword(HTTPEndpoint):
    @requires(['authenticated'])
    async def get(self, request):
        template = 'starlette_auth/change_password.html'
        form = config.forms.Form(ChangePasswordSchema)
        context = {'request': request, 'form': form}
        return config.templates.TemplateResponse(template, context)

    @requires(['authenticated'])
    async def post(self, request):
        template = 'starlette_auth/change_password.html'

        data = await request.form()
        passwords, errors = ChangePasswordSchema.validate_or_error(data)

        if errors:
            form = config.forms.Form(ChangePasswordSchema, errors=errors)
            context = {'request': request, 'form': form}
            return config.templates.TemplateResponse(template, context)

        if not request.user.check_password(passwords.old_password):
            message = Message(text='Enter your current Password.', index=['old_password'])
            errors = ValidationError(messages=[message])

            form = config.forms.Form(ChangePasswordSchema, errors=errors)
            context = {'request': request, 'form': form}
            return config.templates.TemplateResponse(template, context)

        else:
            request.user.set_password(passwords.new_password)
            request.user.save()

        return RedirectResponse(config.change_pw_redirect_url)


class Login(HTTPEndpoint):
    async def get(self, request):
        template = 'starlette_auth/login.html'
        form = config.forms.Form(LoginSchema)
        context = {'request': request, 'form': form}
        return config.templates.TemplateResponse(template, context)

    async def post(self, request):
        template = 'starlette_auth/login.html'

        data = await request.form()
        login, errors = LoginSchema.validate_or_error(data)

        if errors:
            form = config.forms.Form(LoginSchema, values=data, errors=errors)
            context = {'request': request, 'form': form}
            return config.templates.TemplateResponse(template, context)

        try:
            user = User.query.filter(User.email == login.email.lower()).one()
            if user.check_password(login.password):
                request.session['user'] = user.id
                return RedirectResponse(config.login_redirect_url)

        except NoResultFound:
            pass

        request.session.clear()

        message = Message(text='Invalid email or password.', index=['password'])
        errors = ValidationError(messages=[message])

        form = config.forms.Form(LoginSchema, errors=errors)
        context = {'request': request, 'form': form}

        return config.templates.TemplateResponse(template, context)


class Logout(HTTPEndpoint):
    async def get(self, request):
        request.session.clear()
        return RedirectResponse(config.logout_redirect_url)
