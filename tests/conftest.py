import pytest
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette_core.database import Database, DatabaseURL, Session

url = DatabaseURL("sqlite://")
db = Database(url)

from starlette_auth.tables import User  # noqa isort:skip


@pytest.fixture(scope="session", autouse=True)
def database():
    if database_exists(str(url)):
        drop_database(str(url))

    create_database(str(url))

    db.drop_all()
    db.create_all()

    return db


@pytest.yield_fixture(scope="function", autouse=True)
def session():
    db_session = Session()
    db_session.begin_nested()

    yield db_session

    db_session.rollback()
