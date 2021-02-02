import sqlalchemy as sa
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    UnauthenticatedUser,
)
from starlette.requests import HTTPConnection

from .tables import User


class ModelAuthBackend(AuthenticationBackend):
    async def get_user(self, conn: HTTPConnection):
        user_id = conn.session.get("user")
        if user_id:
            try:
                return await User.get(user_id)
            except:
                conn.session.pop("user")

    async def authenticate(self, conn: HTTPConnection):
        user = await self.get_user(conn)
        if user and user.is_authenticated:
            scopes = ["authenticated"] + sorted([str(s) for s in user.scopes])
            return AuthCredentials(scopes), user
        scopes = ["unauthenticated"]
        return AuthCredentials(scopes), UnauthenticatedUser()
