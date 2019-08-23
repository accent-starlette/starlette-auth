import jinja2
import pytest
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from starlette.testclient import TestClient
from starlette_core.database import Database, DatabaseURL, Session
from starlette_core.templating import Jinja2Templates

import starlette_auth
from starlette_auth.tables import User

# basic config for auth app
starlette_auth.config.templates = Jinja2Templates(
    loader=jinja2.FileSystemLoader("tests/templates")
)
starlette_auth.config.login_template = "form.html"
starlette_auth.config.change_pw_template = "form.html"

url = DatabaseURL("sqlite://")
db = Database(url)


@pytest.fixture(scope="session", autouse=True)
def database():
    if database_exists(str(url)):
        drop_database(str(url))

    create_database(str(url))

    db.drop_all()
    db.create_all()

    return db


@pytest.yield_fixture(scope="function", autouse=True)
def session():
    db_session = Session()
    yield db_session
    db.truncate_all(True)


@pytest.fixture(scope="function")
def user():
    test_user = User(email="user@example.com")
    test_user.set_password("password")
    test_user.save()

    return test_user


@pytest.yield_fixture(scope="function")
def client():
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

    with TestClient(app) as client:
        yield client
