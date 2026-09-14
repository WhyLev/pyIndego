"""Shared machinery for pyIndego's data model classes.

The Bosch Indego API is not formally specified, so its response payloads
occasionally grow new fields we don't (yet) model. ``indego_dataclass`` is
used in place of the stdlib ``@dataclass`` decorator on every model class in
this package: it behaves identically, except construction silently ignores
any keys that aren't declared fields (logged at debug level) instead of
raising ``TypeError``, and it recursively constructs nested dataclass fields
(including ``List[SomeDataclass]`` fields) from plain dicts.
"""
import logging
from dataclasses import dataclass, fields, is_dataclass, replace
from typing import Any, Optional

_LOGGER = logging.getLogger(__name__)


def _filter_known_fields(cls: type, data: dict) -> dict:
    """Return the subset of data whose keys are declared, init-accepting fields of cls."""
    known = {f.name for f in fields(cls) if f.init}
    unknown = data.keys() - known
    if unknown:
        _LOGGER.debug(
            "Ignoring unknown field(s) for %s: %s", cls.__name__, sorted(unknown)
        )
    return {key: value for key, value in data.items() if key in known}


def indego_dataclass(*args, **kwargs):  # noqa: D202
    """Class decorator: a dataclass that tolerates unknown API fields and
    knows how to instantiate nested dataclass (and List[dataclass]) fields
    from plain dicts.
    """

    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            kwargs = _filter_known_fields(cls, kwargs)
            for name, value in kwargs.items():
                field_type = cls.__annotations__.get(name)
                if hasattr(field_type, "__args__"):
                    inner_type = field_type.__args__[0]
                    if is_dataclass(inner_type) and isinstance(value, list):
                        kwargs[name] = [
                            inner_type(**item) if isinstance(item, dict) else item
                            for item in value
                        ]
                elif is_dataclass(field_type) and isinstance(value, dict):
                    kwargs[name] = field_type(**value)

            original_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper


# Backward-compatible alias; this was the public (if undocumented) name
# prior to the pyIndego.models split.
nested_dataclass = indego_dataclass


def generate_update(current: Optional[Any], new: Optional[dict], model: type) -> Optional[Any]:
    """Merge new API data into the current model instance, or create a new one.

    Args:
        current: current value of the field being updated, or None.
        new: new values coming back from the API, or None/empty if there's nothing to apply.
        model: model class to instantiate if current is None.

    Returns:
        An instance of model with new merged in, or current unchanged if new is empty.

    """
    if not new:
        return current
    filtered = _filter_known_fields(model, new)
    if current is not None:
        return replace(current, **filtered)
    return model(**filtered)
