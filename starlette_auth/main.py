from starlette.routing import Route, Router

from . import endpoints

app = Router(
    [
        Route(
            "/login", endpoint=endpoints.Login, methods=["GET", "POST"], name="login"
        ),
        Route("/logout", endpoint=endpoints.Logout, methods=["GET"], name="logout"),
        Route(
            "/password/change",
            endpoint=endpoints.ChangePassword,
            methods=["GET", "POST"],
            name="password_change",
        ),
        Route(
            "/password/reset",
            endpoint=endpoints.PasswordReset,
            methods=["GET", "POST"],
            name="password_reset",
        ),
        Route(
            "/password/reset/done",
            endpoint=endpoints.PasswordResetDone,
            methods=["GET"],
            name="password_reset_done",
        ),
        Route(
            "/password/reset/{uidb64:str}/{token:str}",
            endpoint=endpoints.PasswordResetConfirm,
            methods=["GET", "POST"],
            name="password_reset_confirm",
        ),
        Route(
            "/password/reset/complete",
            endpoint=endpoints.PasswordResetComplete,
            methods=["GET"],
            name="password_reset_complete",
        ),
    ]
)
