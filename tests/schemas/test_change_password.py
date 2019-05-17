from starlette_auth.schemas import ChangePasswordSchema


def test_fields():
    keys = ChangePasswordSchema.fields.keys()
    assert list(keys) == ["current_password", "new_password", "confirm_new_password"]


def test_valid():
    data = {
        "current_password": "password",
        "new_password": "password",
        "confirm_new_password": "password",
    }
    value, errors = ChangePasswordSchema.validate_or_error(data)
    assert dict(value) == data
    assert errors is None


def test_invalid():
    data = {}
    value, errors = ChangePasswordSchema.validate_or_error(data)
    assert dict(errors) == {
        "current_password": "This field is required.",
        "new_password": "This field is required.",
        "confirm_new_password": "This field is required.",
    }

    data = {"current_password": "", "new_password": "", "confirm_new_password": ""}
    value, errors = ChangePasswordSchema.validate_or_error(data)
    assert dict(errors) == {
        "current_password": "Must not be blank.",
        "new_password": "Must not be blank.",
        "confirm_new_password": "Must not be blank.",
    }

    data = {
        "current_password": "password",
        "new_password": "password1",
        "confirm_new_password": "password2",
    }
    value, errors = ChangePasswordSchema.validate_or_error(data)
    assert dict(errors) == {"confirm_new_password": "The passwords do not match."}
