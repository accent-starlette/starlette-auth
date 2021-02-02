from typing import AsyncIterator

import jinja2
import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from starlette.testclient import TestClient
from starlette_core.database import Database, DatabaseURL
from starlette_core.templating import Jinja2Templates

import starlette_auth
from starlette_auth.tables import User

# basic config for auth app
starlette_auth.config.templates = Jinja2Templates(
    loader=jinja2.FileSystemLoader("tests/templates")
)
starlette_auth.config.login_template = "form.html"
starlette_auth.config.change_pw_template = "form.html"
starlette_auth.config.reset_pw_template = "form.html"
starlette_auth.config.reset_pw_done_template = "thanks.html"
starlette_auth.config.reset_pw_email_subject_template = "password_reset_subject.txt"
starlette_auth.config.reset_pw_email_template = "password_reset_body.txt"
starlette_auth.config.reset_pw_confirm_template = "form.html"
starlette_auth.config.reset_pw_complete_template = "thanks.html"

url = DatabaseURL("sqlite://")
db = Database(url)


@pytest.fixture(scope="function", autouse=True)
async def database():
    await db.create_all()
    return db


@pytest.fixture(scope="function", autouse=True)
async def cleanup():
    await db.truncate_all(True)


@pytest.fixture(scope="function")
async def user():
    test_user = User(email="user@example.com")
    test_user.set_password("password")
    await test_user.save()
    return test_user


@pytest.fixture()
def app():
    @requires(["authenticated"], redirect="auth:login")
    def home(request):
        return JSONResponse({"user": request.user.email})

    app = Starlette()
    app.mount(path="/auth", app=starlette_auth.app, name="auth")
    app.add_middleware(
        AuthenticationMiddleware, backend=starlette_auth.backends.ModelAuthBackend()
    )
    app.add_middleware(SessionMiddleware, secret_key="secret")
    app.add_route("/", home)

    return app


@pytest.fixture()
async def client(app) -> AsyncIterator[AsyncClient]:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://testserver") as ac:
            yield ac
