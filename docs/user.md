# The `User` Class

The `User` class is defined as follows:

```python
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_utils import EmailType
from starlette_core.database import Base

class User(Base):
    email = sa.Column(EmailType, nullable=False, index=True, unique=True)
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
        """ hashes and sets a users password, will require saving.
        
        eg: user.set_password("password")
        """

    def check_password(self, password) -> bool:
        """ hashes and checks the given password is the same as the stored one.
        
        eg: user.check_password("password")
        """
```