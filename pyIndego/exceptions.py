"""Exception hierarchy for pyIndego.

All exceptions raised directly by this library (as opposed to exceptions
raised by the underlying HTTP transport, e.g. ``aiohttp`` or ``requests``,
which are left to propagate unchanged when ``raise_request_exceptions`` is
enabled) derive from :class:`IndegoError`.

For backward compatibility, the exceptions that replace what used to be
plain :class:`ValueError`/:class:`IndexError` instances also inherit from
those built-in types, so existing ``except ValueError`` / ``except
IndexError`` call sites keep working unchanged.
"""


class IndegoError(Exception):
    """Base class for all exceptions raised directly by pyIndego."""


class IndegoValueError(IndegoError, ValueError):
    """Raised when a caller passes an invalid value to a pyIndego call."""


class IndegoIndexError(IndegoError, IndexError):
    """Raised when an alert index is out of range."""


class IndegoNotLoadedError(IndegoValueError):
    """Raised when alert data is used before ``update_alerts`` has run."""


class IndegoCommandError(IndegoValueError):
    """Raised when an invalid mower command is supplied to ``put_command``."""


class IndegoCalendarError(IndegoValueError):
    """Raised when a calendar payload fails validation."""
