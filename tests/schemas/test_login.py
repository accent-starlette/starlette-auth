from starlette_auth.schemas import LoginSchema


def test_fields():
    keys = LoginSchema.fields.keys()
    assert list(keys) == ["email", "password"]


def test_valid():
    data = {"email": "stu@example.com", "password": "password"}
    value, errors = LoginSchema.validate_or_error(data)
    assert dict(value) == data
    assert errors is None


def test_invalid():
    data = {}
    value, errors = LoginSchema.validate_or_error(data)
    assert dict(errors) == {
        "email": "This field is required.",
        "password": "This field is required.",
    }

    data = {"email": "", "password": ""}
    value, errors = LoginSchema.validate_or_error(data)
    assert dict(errors) == {
        "email": "Must not be blank.",
        "password": "Must not be blank.",
    }

    data = {"email": "invalid.com"}
    value, errors = LoginSchema.validate_or_error(data)
    assert dict(errors)["email"] == "Must be a valid email."

    data = {"email": "invalid"}
    value, errors = LoginSchema.validate_or_error(data)
    assert dict(errors)["email"] == "Must be a valid email."

    data = {"email": "invalid@invalid"}
    value, errors = LoginSchema.validate_or_error(data)
    assert dict(errors)["email"] == "Must be a valid email."
