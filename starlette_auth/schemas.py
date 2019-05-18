import typing

import typesystem
from starlette_core.typesystem import Email


class ChangePasswordSchema(typesystem.Schema):
    current_password = typesystem.String(title="Current password", format="password")
    new_password = typesystem.String(title="New password", format="password")
    confirm_new_password = typesystem.String(
        title="Confirm new password", format="password"
    )

    @classmethod
    def validate(
        cls, value: typing.Any, *, strict: bool = False
    ) -> "ChangePasswordSchema":
        validator = cls.make_validator(strict=strict)
        value = validator.validate(value, strict=strict)
        if value["new_password"] != value["confirm_new_password"]:
            message = typesystem.Message(
                text="The passwords do not match.", index=["confirm_new_password"]
            )
            raise typesystem.ValidationError(messages=[message])
        return cls(value)


class LoginSchema(typesystem.Schema):
    email = Email(title="Email")
    password = typesystem.String(title="Password", format="password")
