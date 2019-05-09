from starlette.routing import Route, Router

from .endpoints import ChangePassword, Login, Logout


app = Router([
    Route('/login', endpoint=Login, methods=['GET', 'POST'], name="login"),
    Route('/logout', endpoint=Logout, methods=['GET'], name="logout"),
    Route('/change-password', endpoint=ChangePassword, methods=['GET', 'POST'], name="change_password"),
])
