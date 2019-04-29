__version__ = "0.0.1.b1"


from starlette.routing import Route, Router
from starlette_auth.endpoints import Login, Logout


app = Router([
    Route('/login', endpoint=Login, methods=['GET', 'POST'], name="login"),
    Route('/logout', endpoint=Logout, methods=['GET'], name="logout")
])
