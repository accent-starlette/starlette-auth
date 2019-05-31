from wtforms import fields, form, validators
from wtforms.fields.html5 import EmailField


class ChangePasswordForm(form.Form):
    current_password = fields.PasswordField(validators=[validators.InputRequired()])
    new_password = fields.PasswordField(validators=[validators.InputRequired()])
    confirm_new_password = fields.PasswordField(
        validators=[
            validators.InputRequired(),
            validators.EqualTo("new_password", message="The passwords do not match."),
        ]
    )


class LoginForm(form.Form):
    email = EmailField(
        validators=[
            validators.InputRequired(),
            validators.Email(message="Must be a valid email."),
        ]
    )
    password = fields.PasswordField(validators=[validators.InputRequired()])
