"""get the current time in a human-readable format."""

import datetime


def get_time(**kwargs) -> str:
    """
    Get the current local time.

    Use this tool when the user asks what time it is now, or asks for the
    current time.

    Args:
        No Arguements

    Returns:
        str: The current local time formatted as HH:MM.
    """
    now = datetime.datetime.now()
    return now.strftime("%H:%M")


def get_date(**kwargs) -> str:
    """
    Get the current local date.

    Use this tool when the user asks what the date is today, or asks for the
    current day, month, or year.

    Args:
        No Arguements

    Returns:
        str: The current local date formatted as YYYY-MM-DD.
    """
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")
