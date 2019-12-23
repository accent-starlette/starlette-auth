# Introduction

The package provides a SQLAlchemy backend for user authentication within starlette.

Includes:

- `User` and `Scope` tables in SQLAlchemy
- Login
- Logout
- Password Change
- Password Reset

### Getting Started - Installation

The minimum Python requirement is 3.7.

This package has not been published to [PyPI](https://pypi.org) so you will need to install it from this [repo](https://github.com/accent-starlette/starlette-auth). To do this simply run:

```
pip install git+https://github.com/accent-starlette/starlette-auth.git@master#egg=starlette-auth

```

### Before You Begin

This package assumes you have a basic starlette site operational and that you are using the [database](https://accent-starlette.github.io/starlette-core/database/) functionality within the [starlette-core](https://accent-starlette.github.io/starlette-core) package.
