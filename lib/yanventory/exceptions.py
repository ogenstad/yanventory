"""yanventory.exceptions."""


class YanventoryError(Exception):
    """Yanventory base exception."""

    pass


class YanventoryParsingError(YanventoryError):
    """Yanventory parsing exception."""

    pass
