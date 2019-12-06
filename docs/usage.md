# Usage

Starlette already comes complete with an authentication package providing functionality to both `User` and `Auth` models. These can be used in your endpoints via `request` like so: `request.User`

For basic setup and useage please refer to Starlette's [docs](https://www.starlette.io/authentication/).

For adding users and scopes please refer to our starlette-admin [docs](https://accent-starlette.github.io/starlette-admin/templating/)


### User Model

The User model itself includes the following fields:

```python

class User(Base):
    email = sa.Column(EmailType, nullable=False, index=True, unique=True)
    password = sa.Column(sa.String(255))
    first_name = sa.Column(sa.String(120))
    last_name = sa.Column(sa.String(120))
    is_active = sa.Column(sa.Boolean, nullable=False, default=True)
    last_login = sa.Column(sa.DateTime, nullable=True)
    scopes = orm.relationship("Scope", secondary=user_scopes)

```

**Setting the field `is_active == False` will disable the ability for that user to login**  


The User model included within this package has all the required authentication functionality pre-defined.


.set_password includes functionality to hash passwords passed to it as defined in tables.py:

```python

    def set_password(self, password) -> None:

```

.check_password is included for comparing an unhashed password returning a boolean value:

```python

    def check_password(self, password) -> bool:

```
