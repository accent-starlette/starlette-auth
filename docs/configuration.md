# Configuration

There are several parts of the package that require config options.

Configuration can either be stored in environment variables or set directly within the package.

## Templates

These are the paths that are used to the templates.

```bash
# the below are the defaults
LOGIN_TEMPLATE="starlette_auth/login.html"
CHANGE_PW_TEMPLATE="starlette_auth/change_password.html"
RESET_PW_TEMPLATE="starlette_auth/password_reset.html"
RESET_PW_DONE_TEMPLATE="starlette_auth/password_reset_done.html"
RESET_PW_CONFIRM_TEMPLATE="starlette_auth/password_reset_confirm.html"
RESET_PW_COMPLETE_TEMPLATE="starlette_auth/password_reset_complete.html"
RESET_PW_EMAIL_SUBJECT_TEMPLATE="starlette_auth/password_reset_subject.txt"
RESET_PW_EMAIL_TEMPLATE="starlette_auth/password_reset_body.txt"

# only required for html email
RESET_PW_HTML_EMAIL_TEMPLATE="starlette_auth/password_reset_body.html"
```

If you don't want to set these as environment variables you can also define them in code.

```python
from starlette_auth import config

config.login_template = ...
config.change_pw_template = ...
config.reset_pw_template = ...
config.reset_pw_done_template = ...
config.reset_pw_confirm_template = ...
config.reset_pw_complete_template = ...
config.reset_pw_email_subject_template = ...
config.reset_pw_email_template = ...
config.reset_pw_html_email_template = ...

app = Starlette()
```

So that the package can load your templates you also need to specify the `templates` variable:

```python
import jinja2
from starlette_auth import config
from starlette_core.templating import Jinja2Templates

templates = Jinja2Templates(loader=jinja2.FileSystemLoader("templates"))

config.templates = templates

app = Starlette()
```

## Routing

The below are a list of redirect urls:

```bash
# below are the defaults
LOGIN_REDIRECT_URL="/"
LOGOUT_REDIRECT_URL="/"
CHANGE_PW_REDIRECT_URL="/"
```

or directly in python:

```python
from starlette_auth import config

config.login_redirect_url = ...
config.logout_redirect_url = ...
config.change_pw_redirect_url = ...

app = Starlette()
```

## General

The below are a list of other variables:

```bash
# used to make pw reset urls invalid after x seconds
# default 3 days = 60 * 60 * 24 * 3
RESET_PW_TIMEOUT="86400"
# used to create pw reset urls
# default = ""
SECRET_KEY="some-secret-key"
```

or directly in python:

```python
from starlette_auth import config

config.reset_pw_timeout = ...
config.secret_key = ...

app = Starlette()
```