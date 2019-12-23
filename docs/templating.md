# Templating

We do not include any templates that are required by the endpoints or email sending.
You will need to create the following templates in your project and set a config variable
in starlette-auth to load these:

```python
import jinja2
from starlette_auth import config
from starlette_core.templating import Jinja2Templates

templates = Jinja2Templates(loader=jinja2.FileSystemLoader("templates"))

config.templates = templates

app = Starlette()
```

## Example Templates

The below by default are where this package will try to load templates from.

### HTML

*starlette_auth/login.html*
```html
<body>
<p>Please login to get started.</p>
{% for field in form %}
    {{ field.label }}
    {{ field }}
    {% if field.errors %}<cite>{{ field.errors|join(' ') }}</cite>{% endif %}
{% endfor %}
</body>
```

*starlette_auth/change_password.html*
```html
<body>
<p>Please use the below form to change your password.</p>
{% for field in form %}
    {{ field.label }}
    {{ field }}
    {% if field.errors %}<cite>{{ field.errors|join(' ') }}</cite>{% endif %}
{% endfor %}
</body>
```

*starlette_auth/password_reset.html*
```html
<body>
<p>Please use the below form by providing a valid email 
    address to reset your password.</p>
{% for field in form %}
    {{ field.label }}
    {{ field }}
    {% if field.errors %}<cite>{{ field.errors|join(' ') }}</cite>{% endif %}
{% endfor %}
</body>
```

*starlette_auth/password_reset_done.html*
```html
<body>
<p>If you have provided a registered email address, you will 
    receive an email with further instructions shortly.</p>
</body>
```

*starlette_auth/password_reset_confirm.html*
```html
<body>
<p>Please use the below to enter your new password.</p>
{% for field in form %}
    {{ field.label }}
    {{ field }}
    {% if field.errors %}<cite>{{ field.errors|join(' ') }}</cite>{% endif %}
{% endfor %}
</body>
```

*starlette_auth/password_reset_complete.html*
```html
<body>
<p>Your password has been changed you can now 
    <a href="{{ url_for('auth:login') }}">login</a>.
</p>
</body>
```

### Email

*starlette_auth/password_reset_subject.txt*
```txt
Password reset for {{ request.url.hostname }}
```

*starlette_auth/password_reset_body.txt*
```txt
You're receiving this email because you requested a password reset 
for your user account at {{ request.url.hostname }}.

Please go to the following page and choose a new password:
{{ url_for("auth:password_reset_confirm", uidb64=uid, token=token) }}

Thanks for using our site!
```
