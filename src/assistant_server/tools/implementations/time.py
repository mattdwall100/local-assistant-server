"""get the current time in a human-readable format."""
import datetime


def getTime() -> str:
    """Returns the current time as a string."""
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")

def getDate() -> str:
    """Returns the current date as a string."""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")