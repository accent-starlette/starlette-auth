from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from starlette_auth.backends import ModelAuthBackend
from starlette_auth.tables import User


class AuthenticatedBackend(ModelAuthBackend):
    def get_user(self, conn):
        return User(first_name="tom", last_name="jones", is_active=True)


class InactiveBackend(ModelAuthBackend):
    def get_user(self, conn):
        return User(first_name="tom", last_name="jones", is_active=False)


class NoUserBackend(ModelAuthBackend):
    def get_user(self, conn):
        pass


def homepage(request):
    return JSONResponse(
        {
            "authenticated": request.user.is_authenticated,
            "user": request.user.display_name,
        }
    )


@requires("authenticated")
async def dashboard(request):
    return JSONResponse(
        {
            "authenticated": request.user.is_authenticated,
            "user": request.user.display_name,
        }
    )


@requires("unauthenticated")
async def unauthenticated(request):
    return JSONResponse(
        {
            "authenticated": request.user.is_authenticated,
            "user": request.user.display_name,
        }
    )


@requires("authenticated", redirect="homepage")
async def admin(request):
    return JSONResponse(
        {
            "authenticated": request.user.is_authenticated,
            "user": request.user.display_name,
        }
    )


def test_authenticated():
    app = Starlette()
    app.add_middleware(SessionMiddleware, secret_key="example")
    app.add_middleware(AuthenticationMiddleware, backend=AuthenticatedBackend())

    app.add_route("/", homepage)
    app.add_route("/dashboard", dashboard)
    app.add_route("/admin", admin)
    app.add_route("/unauthenticated", unauthenticated)

    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"authenticated": True, "user": "tom jones"}

        response = client.get("/dashboard")
        assert response.status_code == 200
        assert response.json() == {"authenticated": True, "user": "tom jones"}

        response = client.get("/admin")
        assert response.status_code == 200
        assert response.json() == {"authenticated": True, "user": "tom jones"}

        response = client.get("/unauthenticated")
        assert response.status_code == 403


def test_not_active():
    app = Starlette()
    app.add_middleware(SessionMiddleware, secret_key="example")
    app.add_middleware(AuthenticationMiddleware, backend=InactiveBackend())

    app.add_route("/", homepage)
    app.add_route("/dashboard", dashboard)
    app.add_route("/admin", admin)
    app.add_route("/unauthenticated", unauthenticated)

    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"authenticated": False, "user": ""}

        response = client.get("/dashboard")
        assert response.status_code == 403

        response = client.get("/admin")
        assert response.status_code == 200
        assert response.json() == {"authenticated": False, "user": ""}

        response = client.get("/unauthenticated")
        assert response.status_code == 200
        assert response.json() == {"authenticated": False, "user": ""}


def test_no_user():
    app = Starlette()
    app.add_middleware(SessionMiddleware, secret_key="example")
    app.add_middleware(AuthenticationMiddleware, backend=NoUserBackend())

    app.add_route("/", homepage)
    app.add_route("/dashboard", dashboard)
    app.add_route("/admin", admin)
    app.add_route("/unauthenticated", unauthenticated)

    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"authenticated": False, "user": ""}

        response = client.get("/dashboard")
        assert response.status_code == 403

        response = client.get("/admin")
        assert response.status_code == 200
        assert response.json() == {"authenticated": False, "user": ""}

        response = client.get("/unauthenticated")
        assert response.status_code == 200
        assert response.json() == {"authenticated": False, "user": ""}
