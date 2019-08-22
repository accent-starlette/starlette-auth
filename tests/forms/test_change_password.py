import pytest
from starlette_core.testing import DummyPostData

from starlette_auth.forms import ChangePasswordForm


def test_valid():
    data = {
        "current_password": "password",
        "new_password": "password",
        "confirm_new_password": "password",
    }
    form = ChangePasswordForm(DummyPostData(data))
    assert form.validate()
    assert form.data == data


@pytest.mark.parametrize(
    "test_data",
    [
        {},
        {"current_password": "", "new_password": "", "confirm_new_password": ""},
        {"current_password": " ", "new_password": " ", "confirm_new_password": " "},
    ],
)
def test_invalid(test_data):
    form = ChangePasswordForm(DummyPostData(test_data))
    assert form.validate() is False
    assert "current_password" in form.errors
    assert "new_password" in form.errors
    assert "confirm_new_password" in form.errors


def test_passwords_dont_match():
    data = {
        "current_password": "password",
        "new_password": "password1",
        "confirm_new_password": "password2",
    }
    form = ChangePasswordForm(DummyPostData(data))
    assert form.validate() is False
    assert form.errors == {"confirm_new_password": ["The passwords do not match."]}
