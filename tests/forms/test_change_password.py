from starlette_auth.forms import ChangePasswordForm
from starlette_core.testing import DummyPostData


def test_valid():
    data = {
        "current_password": "password",
        "new_password": "password",
        "confirm_new_password": "password",
    }
    form = ChangePasswordForm(DummyPostData(data))
    assert form.validate()
    assert form.data == data


def test_invalid():
    data = {}
    form = ChangePasswordForm(DummyPostData(data))
    assert form.validate() is False
    assert form.errors == {
        "current_password": ["This field is required."],
        "new_password": ["This field is required."],
        "confirm_new_password": ["This field is required."],
    }

    data = {"current_password": "", "new_password": "", "confirm_new_password": ""}
    form = ChangePasswordForm(DummyPostData(data))
    assert form.validate() is False
    assert form.errors == {
        "current_password": ["This field is required."],
        "new_password": ["This field is required."],
        "confirm_new_password": ["This field is required."],
    }

    data = {
        "current_password": "password",
        "new_password": "password1",
        "confirm_new_password": "password2",
    }
    form = ChangePasswordForm(DummyPostData(data))
    assert form.validate() is False
    assert form.errors == {"confirm_new_password": ["The passwords do not match."]}
