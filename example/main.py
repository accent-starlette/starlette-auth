import jinja2
from starlette.applications import Starlette
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import PlainTextResponse
from starlette_auth import app as auth_app, config, ModelAuthBackend, tables
from starlette_core import config as core_config
from starlette_core.database import Database, DatabaseURL
from starlette_core.templating import Jinja2Templates

DEBUG = True

url = DatabaseURL("sqlite:///:memory:")

db = Database(url)

async def startup():
    await db.create_all()
    user = tables.User(
        email="admin@example.com",
        first_name="Admin",
        last_name="User"
    )
    user.set_password("password")
    await user.save()

async def shutdown():
    await db.drop_all()

templates = Jinja2Templates(loader=jinja2.FileSystemLoader("example/templates"))

config.secret_key = "secret"
config.templates = templates

core_config.email_backend = 'starlette_core.mail.backends.console.EmailBackend'

# create app
app = Starlette(debug=DEBUG, on_startup=[startup], on_shutdown=[shutdown])

# static app

async def home(request):
    return PlainTextResponse("home")

app.add_route(path="/", route=home)
app.mount(path="/auth", app=auth_app, name="auth")

app.add_middleware(AuthenticationMiddleware, backend=ModelAuthBackend())
app.add_middleware(SessionMiddleware, secret_key="secret")
