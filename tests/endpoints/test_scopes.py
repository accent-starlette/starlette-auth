from starlette.authentication import requires
from starlette.responses import JSONResponse

from starlette_auth.tables import Scope


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


def test_scoped_endpoints(client, user):
    read_scope = Scope(code="read")
    write_scope = Scope(code="write")

    read_scope.save()
    write_scope.save()

    client.app.add_route("/unauthed", unauthed)
    client.app.add_route("/authed", authed)
    client.app.add_route("/read", read)
    client.app.add_route("/write", write)

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
    user.save()

    assert client.get("/unauthed").status_code == 403
    assert client.get("/authed").status_code == 200
    assert client.get("/read").status_code == 200
    assert client.get("/write").status_code == 403

    user.scopes.append(write_scope)
    user.save()

    assert client.get("/unauthed").status_code == 403
    assert client.get("/authed").status_code == 200
    assert client.get("/read").status_code == 200
    assert client.get("/write").status_code == 200
