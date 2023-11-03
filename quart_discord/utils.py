"""Few utility functions and decorators."""

import functools
import datetime

from . import exceptions
from quart import current_app

DISCORD_EPOCH = 1420070400000


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


def snowflake_time(id: int, /) -> datetime.datetime:
    """Returns the creation time of the given snowflake.

    .. versionchanged:: 2.0
        The ``id`` parameter is now positional-only.

    Parameters
    -----------
    id: :class:`int`
        The snowflake ID.

    Returns
    --------
    :class:`datetime.datetime`
        An aware datetime in UTC representing the creation time of the snowflake.
    """
    timestamp = ((id >> 22) + DISCORD_EPOCH) / 1000
    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)


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
