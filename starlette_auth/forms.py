from email.message import EmailMessage

from starlette.requests import Request
from starlette_core.mail import send_message
from wtforms import fields, form, validators
from wtforms.fields.html5 import EmailField

from .exceptions import ImproperlyConfigured
from .tables import User
from .tokens import token_generator
from .utils.http import urlsafe_base64_encode


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

        user = User.query.filter(User.email == self.data["email"]).one_or_none()

        if not user:
            return

        templates = config.templates
        context = {
            "request": request,
            "uid": urlsafe_base64_encode(bytes(str(user.id), encoding="utf-8")),
            "user": user,
            "token": token_generator.make_token(user),
        }
        msg = EmailMessage()

        if (
            not config.reset_pw_email_subject_template
            or not config.reset_pw_email_template
        ):
            error_message = (
                "To sent a password reset email you must specify both the "
                "`reset_pw_email_subject_template` and `reset_pw_email_template` "
                "templates. Additionally you can also specify the "
                "`reset_pw_html_email_template` to send an html version."
            )
            raise ImproperlyConfigured(error_message)

        subject_tmpl = templates.get_template(config.reset_pw_email_subject_template)
        subject = subject_tmpl.render(context)
        body_tmpl = templates.get_template(config.reset_pw_email_template)
        body = body_tmpl.render(context)

        msg["To"] = [user.email]
        msg["Subject"] = subject
        msg.set_content(body)

        if config.reset_pw_html_email_template:
            html_body_tmpl = templates.get_template(config.reset_pw_html_email_template)
            html_body = html_body_tmpl.render(context)
            msg.add_alternative(html_body, subtype="html")

        send_message(msg)


class PasswordResetConfirmForm(form.Form):
    new_password = fields.PasswordField(validators=[validators.DataRequired()])
    confirm_new_password = fields.PasswordField(
        validators=[
            validators.DataRequired(),
            validators.EqualTo("new_password", message="The passwords do not match."),
        ]
    )
