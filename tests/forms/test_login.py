from starlette_core.testing import DummyPostData

from starlette_auth.forms import LoginForm


def test_valid():
    data = {"email": "stu@example.com", "password": "password"}
    form = LoginForm(DummyPostData(data))
    assert form.validate()
    assert form.data == data


def test_invalid():
    data = {}
    form = LoginForm(DummyPostData(data))
    assert form.validate() is False
    assert form.errors == {
        "email": ["This field is required."],
        "password": ["This field is required."],
    }

    data = {"email": "", "password": ""}
    form = LoginForm(DummyPostData(data))
    assert form.validate() is False
    assert form.errors == {
        "email": ["This field is required."],
        "password": ["This field is required."],
    }

    data = {"email": "invalid.com"}
    form = LoginForm(DummyPostData(data))
    assert form.validate() is False
    assert form.errors == {
        "email": ["Must be a valid email."],
        "password": ["This field is required."],
    }

    data = {"email": "invalid"}
    form = LoginForm(DummyPostData(data))
    assert form.validate() is False
    assert form.errors == {
        "email": ["Must be a valid email."],
        "password": ["This field is required."],
    }

    data = {"email": "invalid@invalid"}
    form = LoginForm(DummyPostData(data))
    assert form.validate() is False
    assert form.errors == {
        "email": ["Must be a valid email."],
        "password": ["This field is required."],
    }
