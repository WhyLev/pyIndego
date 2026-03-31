"""Custom exceptions for PyIndego."""


class IndegoException(Exception):
    """Base exception for all PyIndego errors."""

    pass


class IndegoAuthError(IndegoException):
    """Exception raised for authentication-related errors (401, 403)."""

    pass


class IndegoConnectionError(IndegoException):
    """Exception raised for connection errors (network timeouts, connection failures)."""

    pass


class IndegoRequestError(IndegoException):
    """Exception raised for API request errors (4xx, 5xx errors)."""

    pass


class IndegoNotFoundError(IndegoRequestError):
    """Exception raised when resource is not found (404)."""

    pass


class IndegoDataError(IndegoException):
    """Exception raised for data validation or parsing errors."""

    pass
