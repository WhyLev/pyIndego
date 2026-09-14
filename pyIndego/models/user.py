"""Account/user model."""
from .base import indego_dataclass


@indego_dataclass
class User:
    """Bosch account details."""

    email: str = None
    display_name: str = None
    language: str = None
    country: str = None
    optIn: bool = None
    optInApp: bool = None
