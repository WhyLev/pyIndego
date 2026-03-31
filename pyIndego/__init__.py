"""Init for Indego class."""
from .indego_async_client import IndegoAsyncClient
from .indego_client import IndegoClient
from .exceptions import (
    IndegoException,
    IndegoAuthError,
    IndegoConnectionError,
    IndegoRequestError,
    IndegoNotFoundError,
    IndegoDataError,
)

