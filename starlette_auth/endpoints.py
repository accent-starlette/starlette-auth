from sqlalchemy.orm.exc import NoResultFound
from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from typesystem import Jinja2Forms, Message, ValidationError

from starlette_auth.schemas import LoginSchema
from starlette_auth.tables import User


forms = Jinja2Forms(directory='templates')
templates = Jinja2Templates(directory='templates')


LOGIN_REDIRECT_URL = LOGOUT_REDIRECT_URL = '/'


class Login(HTTPEndpoint):
    async def get(self, request):
        template = 'starlette_auth/login.html'
        form = forms.Form(LoginSchema)
        context = {'request': request, 'form': form}
        return templates.TemplateResponse(template, context)

    async def post(self, request):
        template = 'starlette_auth/login.html'

        data = await request.form()
        login, errors = LoginSchema.validate_or_error(data)

        if errors:
            form = forms.Form(LoginSchema, values=data, errors=errors)
            context = {'request': request, 'form': form}
            return templates.TemplateResponse(template, context)

        try:
            user = User.query.filter(User.email == login.email.lower()).one()
            if user.check_password(login.password):
                request.session['user'] = user.id
                return RedirectResponse(LOGIN_REDIRECT_URL)

        except NoResultFound:
            pass

        request.session.clear()

        message = Message(text='Invalid email or password.', index=['password'])
        errors = ValidationError(messages=[message])

        form = forms.Form(LoginSchema, errors=errors)
        context = {'request': request, 'form': form}

        return templates.TemplateResponse(template, context)


class Logout(HTTPEndpoint):
    async def get(self, request):
        request.session.clear()
        return RedirectResponse(LOGOUT_REDIRECT_URL)
