from email.message import EmailMessage

from starlette.requests import Request
from starlette_core.mail import send_message
from wtforms import fields, form, validators
from wtforms.fields.html5 import EmailField


class ChangePasswordForm(form.Form):
    current_password = fields.PasswordField(validators=[validators.DataRequired()])
    new_password = fields.PasswordField(validators=[validators.DataRequired()])
    confirm_new_password = fields.PasswordField(
        validators=[
            validators.DataRequired(),
            validators.EqualTo("new_password", message="The passwords do not match."),
        ]
    )


class LoginForm(form.Form):
    email = EmailField(
        validators=[
            validators.DataRequired(),
            validators.Email(message="Must be a valid email."),
        ]
    )
    password = fields.PasswordField(validators=[validators.DataRequired()])


class PasswordResetForm(form.Form):
    email = EmailField(
        validators=[
            validators.DataRequired(),
            validators.Email(message="Must be a valid email."),
        ]
    )

    async def send_email(self, request: Request):
        from . import config

        templates = config.templates
        context = {"request": request}
        msg = EmailMessage()

        subject_tmpl = templates.get_template(config.reset_pw_email_subject_template)
        subject = subject_tmpl.render(context)
        body_tmpl = templates.get_template(config.reset_pw_email_template)
        body = body_tmpl.render(context)

        msg["To"] = [self.data["email"]]
        msg["Subject"] = subject
        msg.set_content(body)

        send_message(msg)
