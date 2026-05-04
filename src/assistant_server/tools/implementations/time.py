"""get the current time in a human-readable format."""

import datetime
from typing import Any


def getTime(**kwargs: Any) -> str:
    """Returns the current time as a string."""
    now = datetime.datetime.now()
    return now.strftime("%H:%M")


def getDate(**kwargs: Any) -> str:
    """Returns the current date as a string."""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")
