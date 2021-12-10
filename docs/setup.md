# Setup


## Tables

Firstly import both the `User` and `Scope` tables into your project. Please refer to the [starlette-core documentation](https://accent-starlette.github.io/starlette-core/database/) for more information.

```python
from starlette_core.database import Database, DatabaseURL, metadata
from app.settings import DATABASE_URL

url = DatabaseURL("sqlite:///./db.sqlite3")

# set engine config options
engine_kwargs = {}

# setup the database
database = Database(DATABASE_URL, engine_kwargs=engine_kwargs)

# once the db is initialised you can import any project 
# and external tables into this file.

# the metadata imported above will be the complete metadata 
# used for your db for the likes of alembic migrations.
from my_project import tables
from starlette_auth import tables
```


## Middleware

Add both `AuthenticationMiddleware` and `SessionMiddleware`:

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette_auth import ModelAuthBackend
from starlette_auth.middleware import SessionMiddleware

middleware = [
    ...
    Middleware(SessionMiddleware, secret_key="some-secret-key"),
    Middleware(AuthenticationMiddleware, backend=ModelAuthBackend()),
]

app = Starlette(middleware=middleware)
```

## Routing

You will need to mount the urls as follows:

```python
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette_auth import app as auth_app

routes = [
    ...
    Mount("/auth", app=auth_app, name="auth"),
]

app = Starlette(routes=routes)
```

This will also allow you to reference the urls in templates such as `auth:login` etc.
