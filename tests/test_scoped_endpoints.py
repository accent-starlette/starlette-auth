from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from starlette_auth import app as auth_app
from starlette_auth.backends import ModelAuthBackend
from starlette_auth.tables import Scope, User


@requires(["unauthenticated"])
def unauthed(request):
    return JSONResponse({"status": "ok"})


@requires(["authenticated"])
def authed(request):
    return JSONResponse({"status": "ok"})


@requires(["authenticated", "read"])
def read(request):
    return JSONResponse({"status": "ok"})


@requires(["authenticated", "write"])
def write(request):
    return JSONResponse({"status": "ok"})


def create_app():
    app = Starlette()
    app.mount(path="/auth", app=auth_app, name="auth")
    app.add_middleware(AuthenticationMiddleware, backend=ModelAuthBackend())
    app.add_middleware(SessionMiddleware, secret_key="secret")
    app.add_route("/unauthed", unauthed)
    app.add_route("/authed", authed)
    app.add_route("/read", read)
    app.add_route("/write", write)
    return app


def test_scoped_endpoints(session):
    user = User(email="user@example.com")
    user.set_password("password")

    read_scope = Scope(code="read")
    write_scope = Scope(code="write")

    session.add_all([user, read_scope, write_scope])
    session.flush()

    app = create_app()

    with TestClient(app) as client:

        assert client.get("/unauthed").status_code == 200
        assert client.get("/authed").status_code == 403
        assert client.get("/read").status_code == 403
        assert client.get("/write").status_code == 403

        login = client.post(
            "/auth/login", data={"email": "user@example.com", "password": "password"}
        )

        assert login.status_code == 302

        assert client.get("/unauthed").status_code == 403
        assert client.get("/authed").status_code == 200
        assert client.get("/read").status_code == 403
        assert client.get("/write").status_code == 403

        user.scopes.append(read_scope)
        session.add(user)
        session.flush()

        assert client.get("/unauthed").status_code == 403
        assert client.get("/authed").status_code == 200
        assert client.get("/read").status_code == 200
        assert client.get("/write").status_code == 403

        user.scopes.append(write_scope)
        session.add(user)
        session.flush()

        assert client.get("/unauthed").status_code == 403
        assert client.get("/authed").status_code == 200
        assert client.get("/read").status_code == 200
        assert client.get("/write").status_code == 200
