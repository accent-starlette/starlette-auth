import typing

from starlette.responses import RedirectResponse
from starlette.types import Receive, Scope, Send


class TwoFactorMiddleware:
    """
    Ensures the user has verified and entered their
    two factor authentication code.
    """

    def __init__(
        self, app, two_factor_url: str, exclude_paths: typing.Tuple[str]
    ) -> None:
        """
        Args:
            two_factor_url (str):
                url to redirect to verify code
            exclude_paths (typing.Tuple[str]):
                url paths to exclude when redirecting. ie to exclude any url starting
                with '/foo' or '/bar' add ("/foo", "/bar")
        """
        self.app = app
        self.two_factor_url = two_factor_url
        self.exclude_paths = exclude_paths

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            # exclude some urls like auth and media
            is_excluded = scope["path"].startswith(self.exclude_paths)

            # if the user is not verified redirect them to verify
            user = scope["user"]
            is_authenticated = user.is_authenticated
            is_enabled = is_authenticated and user.two_factor_enabled
            is_verified = is_enabled and user.two_factor_verified
            has_logged_in = is_verified and scope["session"].get("two_factor_verified")

            if not is_excluded and is_enabled and not has_logged_in:
                response = RedirectResponse(self.two_factor_url, status_code=302)
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)
