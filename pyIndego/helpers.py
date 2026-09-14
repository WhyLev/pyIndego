"""Generic helpers for pyIndego, independent of the data models."""
import logging
import random
import string
from datetime import datetime
from typing import Any, Optional

_LOGGER = logging.getLogger(__name__)


def convert_bosch_datetime(dt: Any = None) -> Optional[datetime]:
    """Create a datetime object from the string (or give back the datetime object) from Bosch.

    Checks if a valid number of milliseconds is sent.
    """
    if dt:
        if isinstance(dt, str):
            if dt.find(".") > 0:
                return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f%z")
            return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S%z")
        if isinstance(dt, datetime):
            return dt
    return None


def random_request_id() -> str:
    """A random ID for API request to for easier tracking of corresponding log messages."""
    return ''.join(random.choices('ABCDEF' + string.digits, k=6))
