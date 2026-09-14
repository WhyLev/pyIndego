"""Mower configuration, setup and security models."""
from .base import indego_dataclass


@indego_dataclass
class Config:
    """Mower configuration: region, border cut, wire, bump sensitivity and PIN/alarm settings."""

    region: int = None
    language: int = None
    border_cut: int = None
    is_pin_set: bool = None
    wire_id: int = None
    bump_sensitivity: int = None
    alarm_mode: bool = None


@indego_dataclass
class Setup:
    """Mower setup/onboarding status."""

    hasOwner: bool = None
    hasPin: bool = None
    hasMap: bool = None
    hasAutoCal: bool = None
    hasIntegrityCheckPassed: bool = None


@indego_dataclass
class Security:
    """Mower security settings."""

    enabled: bool = None
    autolock: bool = None
