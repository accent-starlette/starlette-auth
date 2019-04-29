import typesystem
import typing

from starlette_auth.typings import Email


class ChangePasswordSchema(typesystem.Schema):
    old_password = typesystem.String(
        min_length=8,
        format='password'
    )
    new_password = typesystem.String(
        min_length=8,
        format='password'
    )
    confirm_new_password = typesystem.String(
        min_length=8,
        format='password'
    )

    @classmethod
    def validate(cls, value: typing.Any, *, strict: bool = False) -> "Schema":
        validator = cls.make_validator(strict=strict)
        value = validator.validate(value, strict=strict)
        if value['new_password'] != value['confirm_new_password']:
            message = typesystem.Message(
                text='The passwords do not match.',
                index=['confirm_new_password']
            )
            raise typesystem.ValidationError(messages=[message])
        return cls(value)


class LoginSchema(typesystem.Schema):
    email = Email()
    password = typesystem.String(
        min_length=8,
        format='password'
    )
