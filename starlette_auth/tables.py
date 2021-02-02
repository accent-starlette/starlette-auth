import binascii
import hashlib
import os

import sqlalchemy as sa
from sqlalchemy import orm
from starlette_core.database import Base

user_scopes = sa.Table(
    "userscope",
    Base.metadata,
    sa.Column("user_id", Base.id.type, sa.ForeignKey("user.id"), primary_key=True),
    sa.Column("scope_id", Base.id.type, sa.ForeignKey("scope.id"), primary_key=True),
)


class User(Base):
    email = sa.Column(sa.String(255), nullable=False, index=True, unique=True)
    password = sa.Column(sa.String(255))
    first_name = sa.Column(sa.String(120))
    last_name = sa.Column(sa.String(120))
    is_active = sa.Column(sa.Boolean, nullable=False, default=True)
    last_login = sa.Column(sa.DateTime, nullable=True)
    scopes = orm.relationship("Scope", secondary=user_scopes)

    def __str__(self):
        return self.email

    @property
    def is_authenticated(self) -> bool:
        return self.is_active

    @property
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def set_password(self, password) -> None:
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
        password_hash = hashlib.pbkdf2_hmac(
            "sha512", password.encode("utf-8"), salt, 100000
        )
        password_hash = binascii.hexlify(password_hash)
        self.password = (salt + password_hash).decode("ascii")

    def check_password(self, password) -> bool:
        salt = self.password[:64]
        stored_password = self.password[64:]
        password_hash = hashlib.pbkdf2_hmac(
            "sha512", password.encode("utf-8"), salt.encode("ascii"), 100000
        )
        password_hash = binascii.hexlify(password_hash).decode("ascii")  # type: ignore
        return password_hash == stored_password


class Scope(Base):
    code = sa.Column(sa.String(50), nullable=False, unique=True)
    description = sa.Column(sa.Text)

    def __str__(self):
        return self.code
