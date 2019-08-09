from starlette.routing import Route, Router

from .endpoints import ChangePassword, Login, Logout, TwoFactorVerify

app = Router(
    [
        Route("/login", endpoint=Login, methods=["GET", "POST"], name="login"),
        Route("/logout", endpoint=Logout, methods=["GET"], name="logout"),
        Route(
            "/change-password",
            endpoint=ChangePassword,
            methods=["GET", "POST"],
            name="change_password",
        ),
        Route(
            "/two-factor-verify",
            endpoint=TwoFactorVerify,
            methods=["GET", "POST"],
            name="two_factor_verify",
        ),
    ]
)
