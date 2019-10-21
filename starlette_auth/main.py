from starlette.routing import Route, Router

from .endpoints import ChangePassword, Login, Logout, PasswordReset

app = Router(
    [
        Route("/login", endpoint=Login, methods=["GET", "POST"], name="login"),
        Route("/logout", endpoint=Logout, methods=["GET"], name="logout"),
        Route(
            "/password/change",
            endpoint=ChangePassword,
            methods=["GET", "POST"],
            name="password_change",
        ),
        Route(
            "/password/reset",
            endpoint=PasswordReset,
            methods=["GET", "POST"],
            name="password_reset",
        ),
    ]
)
