import typing
import typesystem


class Email(typesystem.String):
    """ A field that validates an email """

    custom_errors = {
        'pattern': 'Must be a valid email.'
    }

    def __init__(self, **kwargs: typing.Any) -> None:
        kwargs.setdefault('pattern', r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
        kwargs.setdefault('format', 'email')
        self.errors.update(self.custom_errors)
        super().__init__(**kwargs)
