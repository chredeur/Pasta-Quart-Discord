"""Few utility functions and decorators."""

import functools
import bcrypt

from . import exceptions
from quart import current_app


class JSONBool(object):

    def __init__(self, value):
        self.value = bool(value)

    def __bool__(self):
        return self.value

    def __str__(self):
        return "true" if self else "false"

    @classmethod
    def from_string(cls, value):
        if value.lower() == "true":
            return cls(True)
        if value.lower() == "false":
            return cls(False)
        raise ValueError


def json_bool(value):
    if isinstance(value, str):
        return str(JSONBool.from_string(value))
    return str(JSONBool(value))


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)


# Decorators.

def requires_authorization(view):
    """A decorator for quart views which raises exception :py:class:`quart_discord.Unauthorized` if the user
    is not authorized from Discord OAuth2.

    """

    # TODO: Add support to validate scopes.

    @functools.wraps(view)
    async def wrapper(*args, **kwargs):
        if not await current_app.discord.authorized:
            raise exceptions.Unauthorized
        return await view(*args, **kwargs)

    return wrapper
