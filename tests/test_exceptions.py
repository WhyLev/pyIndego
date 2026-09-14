"""Tests for the pyIndego.exceptions hierarchy: subclassing must keep
existing `except ValueError` / `except IndexError` call sites working."""
from pyIndego.exceptions import (
    IndegoCalendarError,
    IndegoCommandError,
    IndegoError,
    IndegoIndexError,
    IndegoNotLoadedError,
    IndegoValueError,
)


def test_indego_value_error_is_a_value_error():
    assert issubclass(IndegoValueError, ValueError)
    assert issubclass(IndegoValueError, IndegoError)


def test_indego_index_error_is_an_index_error():
    assert issubclass(IndegoIndexError, IndexError)
    assert issubclass(IndegoIndexError, IndegoError)


def test_command_and_calendar_and_not_loaded_errors_are_value_errors():
    assert issubclass(IndegoCommandError, ValueError)
    assert issubclass(IndegoCalendarError, ValueError)
    assert issubclass(IndegoNotLoadedError, ValueError)


def test_raising_and_catching_as_stdlib_types():
    try:
        raise IndegoCommandError("bad command")
    except ValueError as exc:
        assert isinstance(exc, IndegoError)

    try:
        raise IndegoIndexError("bad index")
    except IndexError as exc:
        assert isinstance(exc, IndegoError)
