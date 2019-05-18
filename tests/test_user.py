import sqlalchemy as sa
from sqlalchemy_utils import EmailType
from starlette_core.testing import assert_model_field

from starlette_auth.tables import User

data = {
    "email": "john@mail.com",
    "first_name": "Me",
    "last_name": "Jones",
    "is_active": True,
}


def test_fields():
    assert_model_field(User, "email", EmailType, False, True, True, 255)
    assert_model_field(User, "first_name", sa.String, True, False, False, 120)
    assert_model_field(User, "last_name", sa.String, True, False, False, 120)
    assert_model_field(User, "is_active", sa.Boolean, False, False, False)
    assert_model_field(User, "password", sa.String, True, False, False, 255)


def test_relationships():
    assert User.scopes.property.target.name == "scope"


def test_model_data():
    user = User(**data)

    assert user.email == "john@mail.com"
    assert user.first_name == "Me"
    assert user.last_name == "Jones"
    assert user.is_active is True
    assert user.password is None


def test_display_name():
    user = User(**data)

    assert user.display_name == "Me Jones"


def test_str():
    user = User(**data)

    assert str(user) == "john@mail.com"


def test_password():
    user = User(**data)

    user.set_password("password")
    assert user.check_password("password")
