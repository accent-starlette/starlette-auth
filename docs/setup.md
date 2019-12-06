# Setup


## Import Tables

Firstly import both the `User` and `Scope` tables into your project. Please refer to the [starlette-core documrntation](https://accent-starlette.github.io/starlette-core/database/) for more information.

```python

from starlette_core.database import Database, DatabaseURL, metadata
from app.settings import DATABASE_URL

url = DatabaseURL("sqlite:///./db.sqlite3")

# set engine config options
engine_kwargs = {}

# setup the database
database = Database(DATABASE_URL, engine_kwargs=engine_kwargs)

# once the db is initialised you can import any project 
# and external tables into this file.

# the metadata imported above will be the complete metadata 
# used for your db for the likes of alembic migrations.
from my_project import tables
from starlette_auth import tables

```


## Middleware

Add both sa=tarletts suthnticattion and session middleware from strarlette:

```python

import starlette_auth
from starlette.applications import Starlette
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware


app = starlette()

app.add_middleware(AuthenticationMiddleware, backend=starlette_auth.ModelAuthBackend())
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
```
 
As per Starlette's [docs](https://www.starlette.io/middleware/), the order of the listed middleware is important. In this case the authentication middleware must be wrapped in the session so must be run first as above.




## Mounting the URL's

You will need to mount the urls as follows:

```python

import starlette_auth
from starlette.applications import Starlette

app = Starlette()

app.mount(path="/auth", app=starlette_auth.app, name="auth")

```
This will also allow you to reference the urls in templates such as auth:login etc.

If the file paths differ from the default set in [config.py](https://github.com/accent-starlette/starlette-auth/blob/master/starlette_auth/config.py). You will need to set env variables for paths to files like so:

```python
from starlette.applications import Starlette
from starlette.config import Config


login: str = "auth/templates/login.html"
reset_password: str = "auth/templates/reset_password.html"
change_password: str = "auth/templates/change_password.html"
password_reset_confirm: str = "auth/templates/password_reset_confirm.html"
password_reset_done: str = "auth/templates/password_reset_done.html"
password_reset_complete: str = "auth/templates/password_reset_complete.html"
```

Please refer to *Configuration* section of these documents for futher information on overiding and adding additional config settings if required.


## Templates

If you've installed our [starlette-admin](https://github.com/accent-starlette/starlette-admin) package it includes all the required HTML templates required for starlette-auth including login, password reset and email confirmation.

```python
from app.globals import templates
```

If you are using this package without starlette-admin you will need to create these templates yourself.

We use **wtforms** for our form fields, please refer to their [docs](https://wtforms.readthedocs.io/en/stable/forms.html#wtforms.form.Form.__iter__) for details.

Below are listed the minimum required templates with basic examples.


### login.html
```html

<!DOCTYPE html>
<html>
<head>
<title>Login</title>
</head>
<body>
<div>
    <p>Please login to get started.</p>
    {% with show_password_reset_link=True, button_name='login' %}
    {% endwith %}
</div>
</body>
</html>
```

### reset_password.html
```html
<!DOCTYPE html>
<html>
<head>
<title>Reset Password</title>
</head>
<body>
<div>
    <p>Please use the below form by providing a valid email address to reset your password.</p>
    {% with button_name='reset my password' %}
    {% endwith %}
</div>
</body>
</html>
```

### change_password.html
```html
<!DOCTYPE html>
<html>
<head>
<title>Change Password</title>
</head>
<body>
<div>
    <p>Please use the below form to change your password.</p>
    {% with button_name='change password' %}
    {% endwith %}
</div>
</body>
</html>
```

### password_reset_confirm.html
```html
<!DOCTYPE html>
<html>
<head>
<title>Confirm Password Reset</title>
</head>
<body>
<div>
    <p>Please use the below to enter your new password.</p>
    {% with button_name='reset my password' %}
    {% endwith %
</div>
</body>
</html>
```

### password_reset_done.html
```html
<!DOCTYPE html>
<html>
<head>
<title>Password Reset Link Sent</title>
</head>
<body>
<div>
    <p>If you have provided a registered email address, you will receive an email with further instructions shortly.</p>
</div>
</body>
</html>
```

### password_reset_complete.html
```html
<!DOCTYPE html>
<html>
<head>
<title>Password Reset Complete</title>
</head>
<body>
<div>
    <p>Your password has been changed you can now <a href="{{ url_for('auth:login') }}">login</a>.</p>
</div>
</body>
</html>
```


### password_reset_body.txt

The .txt templates are used for the content of the password reset email.

```txt

You're receiving this email because you requested a password reset for your user account at {{ request.url.hostname }}.

Please go to the following page and choose a new password:
{{ url_for("auth:password_reset_confirm", uidb64=uid, token=token) }}

Thanks for using our site!

```

### password_reset_subject.txt
```txt

Password reset for {{ request.url.hostname }}

```
