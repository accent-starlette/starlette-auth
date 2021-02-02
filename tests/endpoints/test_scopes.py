import pytest
from httpx import AsyncClient
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


@pytest.mark.asyncio
async def test_scoped_endpoints(app, user):
    read_scope = Scope(code="read")
    write_scope = Scope(code="write")

    await read_scope.save()
    await write_scope.save()

    app.add_route("/unauthed", unauthed)
    app.add_route("/authed", authed)
    app.add_route("/read", read)
    app.add_route("/write", write)

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        assert (await client.get("/unauthed")).status_code == 200
        assert (await client.get("/authed")).status_code == 403
        assert (await client.get("/read")).status_code == 403
        assert (await client.get("/write")).status_code == 403

        login = await client.post(
            "/auth/login", data={"email": "user@example.com", "password": "password"}
        )

        assert login.status_code == 200
        assert login.url == "http://testserver/"

        assert (await client.get("/unauthed")).status_code == 403
        assert (await client.get("/authed")).status_code == 200
        assert (await client.get("/read")).status_code == 403
        assert (await client.get("/write")).status_code == 403

        user.scopes.append(read_scope)
        await user.save()

        assert (await client.get("/unauthed")).status_code == 403
        assert (await client.get("/authed")).status_code == 200
        assert (await client.get("/read")).status_code == 200
        assert (await client.get("/write")).status_code == 403

        user.scopes.append(write_scope)
        await user.save()

        assert (await client.get("/unauthed")).status_code == 403
        assert (await client.get("/authed")).status_code == 200
        assert (await client.get("/read")).status_code == 200
        assert (await client.get("/write")).status_code == 200
