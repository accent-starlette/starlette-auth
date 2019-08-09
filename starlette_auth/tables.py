import binascii
import hashlib
import os
import typing

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_utils import EmailType
from starlette_core.database import Base

from .config import config

try:
    import pyotp
except ImportError:
    pyotp = None


user_scopes = sa.Table(
    "userscope",
    Base.metadata,
    sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id")),
    sa.Column("scope_id", sa.Integer, sa.ForeignKey("scope.id")),
)


class User(Base):
    email = sa.Column(EmailType, nullable=False, index=True, unique=True)
    password = sa.Column(sa.String(255))
    first_name = sa.Column(sa.String(120))
    last_name = sa.Column(sa.String(120))
    is_active = sa.Column(sa.Boolean, nullable=False, default=True)
    two_factor_enabled = sa.Column(sa.Boolean, nullable=False, default=False)
    two_factor_verified = sa.Column(sa.Boolean, nullable=False, default=False)
    two_factor_secret = sa.Column(sa.String(50), nullable=True)
    scopes = orm.relationship("Scope", secondary=user_scopes)

    def __str__(self):
        return self.email

    @property
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def is_authenticated(self) -> bool:
        return self.is_active

    @property
    def two_factor_provisioning_uri(self):
        assert (
            pyotp is not None
        ), "pyotp must be installed to use two factor authentication"
        totp = pyotp.totp.TOTP(self.two_factor_secret)
        return totp.provisioning_uri(
            self.email, issuer_name=config.two_factor_issuer_name
        )

    def save(self):
        if self.two_factor_enabled and not self.two_factor_secret:
            assert (
                pyotp is not None
            ), "pyotp must be installed to use two factor authentication"
            self.two_factor_secret = pyotp.random_base32()
        elif not self.two_factor_enabled:
            self.two_factor_verified = False
            self.two_factor_secret = None
        return super().save()

    def check_password(self, password) -> bool:
        salt = self.password[:64]
        stored_password = self.password[64:]
        password_hash = hashlib.pbkdf2_hmac(
            "sha512", password.encode("utf-8"), salt.encode("ascii"), 100000
        )
        password_hash = binascii.hexlify(password_hash).decode("ascii")  # type: ignore
        return password_hash == stored_password

    def check_two_factor(self, token: typing.Union[int, str]):
        assert (
            pyotp is not None
        ), "pyotp must be installed to use two factor authentication"
        totp = pyotp.TOTP(self.two_factor_secret)
        return totp.now() == str(token)

    def set_password(self, password) -> None:
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
        password_hash = hashlib.pbkdf2_hmac(
            "sha512", password.encode("utf-8"), salt, 100000
        )
        password_hash = binascii.hexlify(password_hash)
        self.password = (salt + password_hash).decode("ascii")


class Scope(Base):
    code = sa.Column(sa.String(50), nullable=False, unique=True)
    description = sa.Column(sa.Text)

    def __str__(self):
        return self.code
