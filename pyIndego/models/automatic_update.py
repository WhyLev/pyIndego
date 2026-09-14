"""Automatic firmware update setting model.

Mirrors the response of GET/PUT alms/{serial}/automaticUpdate, previously
undocumented and unimplemented in pyIndego.
"""
from .base import indego_dataclass


@indego_dataclass
class AutomaticUpdate:
    """Whether the mower is allowed to install firmware updates automatically."""

    allow_automatic_update: bool = None
