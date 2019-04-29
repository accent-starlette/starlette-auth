from starlette.authentication import AuthenticationBackend, AuthCredentials, UnauthenticatedUser
from starlette.requests import HTTPConnection

from starlette_auth.tables import User


class ModelAuthBackend(AuthenticationBackend):

    def get_user(self, conn: HTTPConnection):
        user_id = conn.session.get('user')
        if user_id:
            return User.query.get(user_id)

    async def authenticate(self, conn: HTTPConnection):
        user = self.get_user(conn)
        if user and user.is_authenticated:
            return AuthCredentials(['authenticated']), user
        return AuthCredentials(['unauthenticated']), UnauthenticatedUser()
