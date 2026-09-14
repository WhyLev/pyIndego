"""Tests for pyIndego's data models: construction, nesting, unknown-field tolerance."""
from datetime import datetime

import pytest

from pyIndego.helpers import convert_bosch_datetime
from pyIndego.states import (
    Alert,
    AutomaticUpdate,
    Calendar,
    GenericData,
    OperatingData,
    PredictiveSetup,
    State,
    Weather,
)

from .data import (
    ALERT_RESPONSE,
    AUTOMATIC_UPDATE_RESPONSE,
    CALENDAR_RESPONSE,
    GENERIC_RESPONSE,
    OPERATING_RESPONSE,
    PREDICTIVE_SETUP_RESPONSE,
    PREDICTIVE_WEATHER_RESPONSE,
    STATE_RESPONSE,
)


@pytest.mark.parametrize(
    "state, json, checks",
    [
        (Alert, ALERT_RESPONSE, ["alm_sn"]),
        (OperatingData, OPERATING_RESPONSE, ["hmiKeys", ("garden.id", "['garden']['id']")]),
        (
            Calendar,
            CALENDAR_RESPONSE,
            [
                "cal",
                ("days[0].day", "['days'][0]['day']"),
                ("days[0].slots[0].En", "['days'][0]['slots'][0]['En']"),
            ],
        ),
        (State, STATE_RESPONSE, ["state"]),
    ],
)
def test_states(state, json, checks):
    """Test model classes construct correctly from raw API dicts."""
    state_instance = state(**json)  # noqa: F841 - referenced below via eval()
    for check in checks:
        if isinstance(check, str):
            value_state = eval(f"state_instance.{check}")
            value_json = eval(f"json['{check}']")
        else:
            value_state = eval(f"state_instance.{check[0]}")
            value_json = eval(f"json{check[1]}")
        assert value_state == value_json


@pytest.mark.parametrize(
    "date_str, date_dt",
    [
        (
            "2020-07-01T13:22:43.15+02:00",
            datetime.fromisoformat("2020-07-01 13:22:43.150000+02:00"),
        ),
        (
            "2020-07-03T10:00:00+02:00",
            datetime.fromisoformat("2020-07-03 10:00:00+02:00"),
        ),
        (
            datetime.fromisoformat("2020-07-03 10:00:00+02:00"),
            datetime.fromisoformat("2020-07-03 10:00:00+02:00"),
        ),
        (None, None),
    ],
)
def test_date_parsing(date_str, date_dt):
    """Test the convert_bosch_datetime function."""
    test_dt = convert_bosch_datetime(date_str)
    assert test_dt == date_dt


def test_update_battery():
    """Test the battery percent_adjusted computation, which spans generic_data + operating_data."""
    from pyIndego import IndegoClient

    indego = IndegoClient(serial="123456789", token="testtoken")
    indego._update_generic_data(GENERIC_RESPONSE)
    indego._update_operating_data(OPERATING_RESPONSE)
    assert indego.operating_data.battery.percent_adjusted is not None


class TestUnknownFieldTolerance:
    """The Bosch API is undocumented and evolves; models must not crash on new fields."""

    def test_flat_dataclass_ignores_unknown_fields(self):
        alert = Alert(**{**ALERT_RESPONSE, "brand_new_bosch_field": "surprise"})
        assert alert.alert_id == ALERT_RESPONSE["alert_id"]
        assert not hasattr(alert, "brand_new_bosch_field")

    def test_nested_dataclass_ignores_unknown_top_level_fields(self):
        state = State(**{**STATE_RESPONSE, "brand_new_bosch_field": "surprise"})
        assert state.state == STATE_RESPONSE["state"]
        assert not hasattr(state, "brand_new_bosch_field")

    def test_nested_list_dataclass_ignores_unknown_fields(self):
        payload = {
            "cal": 1,
            "days": [
                {"day": 0, "slots": [{"En": True, "StHr": 1, "StMin": 0, "EnHr": 2, "EnMin": 0, "unknown": "x"}], "unknown_day_field": "y"}
            ],
        }
        calendar = Calendar(**payload)
        assert calendar.days[0].slots[0].StHr == 1
        assert not hasattr(calendar.days[0], "unknown_day_field")
        assert not hasattr(calendar.days[0].slots[0], "unknown")

    def test_generate_update_merge_ignores_unknown_fields(self):
        from pyIndego.models import generate_update

        current = GenericData(**GENERIC_RESPONSE)
        updated = generate_update(current, {"needs_service": True, "brand_new_bosch_field": "x"}, GenericData)
        assert updated.needs_service is True
        assert not hasattr(updated, "brand_new_bosch_field")


class TestNewModels:
    """Models added in the 4.0.0 rework, closing gaps the HA integration used to hand-parse."""

    def test_automatic_update(self):
        model = AutomaticUpdate(**AUTOMATIC_UPDATE_RESPONSE)
        assert model.allow_automatic_update is True

    def test_predictive_setup(self):
        model = PredictiveSetup(**PREDICTIVE_SETUP_RESPONSE)
        assert model.garden_size == 93
        assert model.garden_location.timezone == "Europe/Berlin"
        assert model.no_mow_calendar_days[0].day_name == "monday"

    def test_weather(self):
        model = Weather(**PREDICTIVE_WEATHER_RESPONSE["LocationWeather"])
        assert model.location.name == "Berlin"
        assert model.forecast.intervals[0].tt == 21.5
