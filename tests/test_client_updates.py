"""Tests for the update_*/get_* family of methods on both clients."""
from datetime import datetime
from unittest.mock import patch

import pytest

from pyIndego import IndegoAsyncClient, IndegoClient
from pyIndego.states import (
    Alert,
    AutomaticUpdate,
    Calendar,
    Config,
    GenericData,
    Location,
    Network,
    OperatingData,
    PredictiveSchedule,
    PredictiveSetup,
    Security,
    Setup,
    State,
    User,
    Weather,
)

from .conftest import MockResponseAsync, MockResponseSync
from .data import (
    ALERT_RESPONSE,
    AUTOMATIC_UPDATE_RESPONSE,
    CALENDAR_RESPONSE,
    CONFIG_RESPONSE,
    GENERIC_RESPONSE,
    LOCATION_RESPONSE,
    NETWORK_RESPONSE,
    OPERATING_RESPONSE,
    PREDICTIVE_CALENDAR_RESPONSE,
    PREDICTIVE_SCHEDULE_RESPONSE,
    PREDICTIVE_SETUP_RESPONSE,
    PREDICTIVE_WEATHER_RESPONSE,
    SECURITY_RESPONSE,
    SETUP_RESPONSE,
    STATE_FULL_UPDATE_RESPONSE,
    STATE_RESPONSE,
    STATE_UPDATE_RESPONSE,
    USER_RESPONSE,
)


@pytest.mark.parametrize(
    "sync, func, attr, ret_value, assert_value",
    [
        (True, IndegoClient.update_calendar, "calendar", {"sel_cal": 3, "cals": [CALENDAR_RESPONSE]}, Calendar(**CALENDAR_RESPONSE)),
        (True, IndegoClient.update_alerts, "alerts", [ALERT_RESPONSE], [Alert(**ALERT_RESPONSE)]),
        (True, IndegoClient.update_config, "config", CONFIG_RESPONSE, Config(**CONFIG_RESPONSE)),
        (True, IndegoClient.update_generic_data, "generic_data", GENERIC_RESPONSE, GenericData(**GENERIC_RESPONSE)),
        (
            True,
            IndegoClient.update_last_completed_mow,
            "last_completed_mow",
            {"last_mowed": "2020-07-01T13:22:43.15+02:00"},
            datetime.fromisoformat("2020-07-01 13:22:43.150000+02:00"),
        ),
        (True, IndegoClient.update_location, "location", LOCATION_RESPONSE, Location(**LOCATION_RESPONSE)),
        (True, IndegoClient.update_network, "network", NETWORK_RESPONSE, Network(**NETWORK_RESPONSE)),
        (
            True,
            IndegoClient.update_next_mow,
            "next_mow",
            {"mow_next": "2020-07-03T10:00:00+02:00"},
            datetime.fromisoformat("2020-07-03 10:00:00+02:00"),
        ),
        (True, IndegoClient.update_operating_data, "operating_data", OPERATING_RESPONSE, OperatingData(**OPERATING_RESPONSE)),
        (
            True,
            IndegoClient.update_predictive_calendar,
            "predictive_calendar",
            PREDICTIVE_CALENDAR_RESPONSE,
            Calendar(**PREDICTIVE_CALENDAR_RESPONSE["cals"][0]),
        ),
        (
            True,
            IndegoClient.update_predictive_schedule,
            "predictive_schedule",
            PREDICTIVE_SCHEDULE_RESPONSE,
            PredictiveSchedule(**PREDICTIVE_SCHEDULE_RESPONSE),
        ),
        (True, IndegoClient.update_predictive_setup, "predictive_setup", PREDICTIVE_SETUP_RESPONSE, PredictiveSetup(**PREDICTIVE_SETUP_RESPONSE)),
        (
            True,
            IndegoClient.update_predictive_weather,
            "predictive_weather",
            PREDICTIVE_WEATHER_RESPONSE,
            Weather(**PREDICTIVE_WEATHER_RESPONSE["LocationWeather"]),
        ),
        (True, IndegoClient.update_automatic_update, "automatic_update", AUTOMATIC_UPDATE_RESPONSE, AutomaticUpdate(**AUTOMATIC_UPDATE_RESPONSE)),
        (True, IndegoClient.update_security, "security", SECURITY_RESPONSE, Security(**SECURITY_RESPONSE)),
        (True, IndegoClient.update_setup, "setup", SETUP_RESPONSE, Setup(**SETUP_RESPONSE)),
        (True, IndegoClient.update_state, "state", STATE_RESPONSE, State(**STATE_RESPONSE)),
        (True, IndegoClient.update_updates_available, "update_available", {"available": False}, False),
        (True, IndegoClient.update_user, "user", USER_RESPONSE, User(**USER_RESPONSE)),
        (True, IndegoClient.update_all, "user", None, None),
        (False, IndegoAsyncClient.update_calendar, "calendar", {"sel_cal": 3, "cals": [CALENDAR_RESPONSE]}, Calendar(**CALENDAR_RESPONSE)),
        (False, IndegoAsyncClient.update_alerts, "alerts", [ALERT_RESPONSE], [Alert(**ALERT_RESPONSE)]),
        (False, IndegoAsyncClient.update_config, "config", CONFIG_RESPONSE, Config(**CONFIG_RESPONSE)),
        (False, IndegoAsyncClient.update_generic_data, "generic_data", GENERIC_RESPONSE, GenericData(**GENERIC_RESPONSE)),
        (
            False,
            IndegoAsyncClient.update_last_completed_mow,
            "last_completed_mow",
            {"last_mowed": "2020-07-01T13:22:43.15+02:00"},
            datetime.fromisoformat("2020-07-01 13:22:43.150000+02:00"),
        ),
        (False, IndegoAsyncClient.update_location, "location", LOCATION_RESPONSE, Location(**LOCATION_RESPONSE)),
        (False, IndegoAsyncClient.update_network, "network", NETWORK_RESPONSE, Network(**NETWORK_RESPONSE)),
        (
            False,
            IndegoAsyncClient.update_next_mow,
            "next_mow",
            {"mow_next": "2020-07-03T10:00:00+02:00"},
            datetime.fromisoformat("2020-07-03 10:00:00+02:00"),
        ),
        (False, IndegoAsyncClient.update_operating_data, "operating_data", OPERATING_RESPONSE, OperatingData(**OPERATING_RESPONSE)),
        (
            False,
            IndegoAsyncClient.update_predictive_calendar,
            "predictive_calendar",
            PREDICTIVE_CALENDAR_RESPONSE,
            Calendar(**PREDICTIVE_CALENDAR_RESPONSE["cals"][0]),
        ),
        (
            False,
            IndegoAsyncClient.update_predictive_schedule,
            "predictive_schedule",
            PREDICTIVE_SCHEDULE_RESPONSE,
            PredictiveSchedule(**PREDICTIVE_SCHEDULE_RESPONSE),
        ),
        (
            False,
            IndegoAsyncClient.update_predictive_setup,
            "predictive_setup",
            PREDICTIVE_SETUP_RESPONSE,
            PredictiveSetup(**PREDICTIVE_SETUP_RESPONSE),
        ),
        (
            False,
            IndegoAsyncClient.update_predictive_weather,
            "predictive_weather",
            PREDICTIVE_WEATHER_RESPONSE,
            Weather(**PREDICTIVE_WEATHER_RESPONSE["LocationWeather"]),
        ),
        (
            False,
            IndegoAsyncClient.update_automatic_update,
            "automatic_update",
            AUTOMATIC_UPDATE_RESPONSE,
            AutomaticUpdate(**AUTOMATIC_UPDATE_RESPONSE),
        ),
        (False, IndegoAsyncClient.update_security, "security", SECURITY_RESPONSE, Security(**SECURITY_RESPONSE)),
        (False, IndegoAsyncClient.update_setup, "setup", SETUP_RESPONSE, Setup(**SETUP_RESPONSE)),
        (False, IndegoAsyncClient.update_state, "state", STATE_RESPONSE, State(**STATE_RESPONSE)),
        (False, IndegoAsyncClient.update_updates_available, "update_available", {"available": False}, False),
        (False, IndegoAsyncClient.update_user, "user", USER_RESPONSE, User(**USER_RESPONSE)),
        (False, IndegoAsyncClient.update_all, "user", None, None),
    ],
)
@pytest.mark.asyncio
async def test_client_update_functions(sync, func, attr, ret_value, assert_value, test_config):
    """Test the base client functions with 200."""
    if sync:
        resp = MockResponseSync(ret_value, 200)
        with patch("requests.request", return_value=resp):
            indego = IndegoClient(**test_config)
            func(indego)
            assert getattr(indego, attr) == assert_value
            if attr == "state":
                assert indego.state_description == "Docked"
                assert indego.state_description_detail == "Sleeping"
    else:
        resp = MockResponseAsync(ret_value, 200)
        with patch("aiohttp.ClientSession.request", return_value=resp), patch(
            "pyIndego.IndegoAsyncClient.start", return_value=True
        ):
            async with IndegoAsyncClient(**test_config) as indego:
                await func(indego)
                assert getattr(indego, attr) == assert_value
                if attr == "state":
                    assert indego.state_description == "Docked"
                    assert indego.state_description_detail == "Sleeping"


@pytest.mark.parametrize(
    "sync, func, param, attr, ret_value, assert_value",
    [
        (True, IndegoClient.update_state, {"force": True}, "state", STATE_RESPONSE, State(**STATE_RESPONSE)),
        (True, IndegoClient.update_state, {"longpoll": True}, "state", STATE_RESPONSE, State(**STATE_RESPONSE)),
        (True, IndegoClient.update_state, {"force": True, "longpoll": True}, "state", STATE_RESPONSE, State(**STATE_RESPONSE)),
        (False, IndegoAsyncClient.update_state, {"force": True}, "state", STATE_RESPONSE, State(**STATE_RESPONSE)),
        (False, IndegoAsyncClient.update_state, {"longpoll": True}, "state", STATE_RESPONSE, State(**STATE_RESPONSE)),
        (False, IndegoAsyncClient.update_state, {"force": True, "longpoll": True}, "state", STATE_RESPONSE, State(**STATE_RESPONSE)),
    ],
)
@pytest.mark.asyncio
async def test_client_update_state_params(sync, func, param, attr, ret_value, assert_value, test_config):
    """Test the base client functions with 200."""
    if sync:
        resp = MockResponseSync(ret_value, 200)
        with patch("requests.request", return_value=resp):
            indego = IndegoClient(**test_config)
            func(indego, **param)
            assert getattr(indego, attr) == assert_value
    else:
        resp = MockResponseAsync(ret_value, 200)
        with patch("aiohttp.ClientSession.request", return_value=resp), patch(
            "pyIndego.IndegoAsyncClient.start", return_value=True
        ):
            async with IndegoAsyncClient(**test_config) as indego:
                await func(indego, **param)
                assert getattr(indego, attr) == assert_value


@pytest.mark.parametrize(
    "sync, func, initial_ret_value, updated_ret_value, initial_assert_value, updated_assert_value",
    [
        (True, IndegoClient.update_state, STATE_RESPONSE, None, State(**STATE_RESPONSE), State(**STATE_RESPONSE)),
        (
            False,
            IndegoAsyncClient.update_state,
            STATE_RESPONSE,
            STATE_UPDATE_RESPONSE,
            State(**STATE_RESPONSE),
            State(**STATE_FULL_UPDATE_RESPONSE),
        ),
    ],
)
@pytest.mark.asyncio
async def test_state_long_poll_updates(
    sync, func, initial_ret_value, updated_ret_value, initial_assert_value, updated_assert_value, test_config
):
    """Test a state update using longpoll and make sure the state is correctly merged."""
    if sync:
        indego = IndegoClient(**test_config)

        resp = MockResponseSync(initial_ret_value, 200)
        with patch("requests.request", return_value=resp):
            func(indego, longpoll=True, longpoll_timeout=10)
            assert getattr(indego, "state") == initial_assert_value

        resp = MockResponseSync(updated_ret_value, 504 if updated_ret_value is None else 200)
        with patch("requests.request", return_value=resp):
            func(indego, longpoll=True, longpoll_timeout=10)
            assert getattr(indego, "state") == updated_assert_value
    else:
        async with IndegoAsyncClient(**test_config) as indego:
            resp = MockResponseAsync(initial_ret_value, 200)
            with patch("aiohttp.ClientSession.request", return_value=resp), patch(
                "pyIndego.IndegoAsyncClient.start", return_value=True
            ):
                await func(indego, longpoll=True, longpoll_timeout=10)
                assert getattr(indego, "state") == initial_assert_value

            resp = MockResponseAsync(updated_ret_value, 504 if updated_ret_value is None else 200)
            with patch("aiohttp.ClientSession.request", return_value=resp), patch(
                "pyIndego.IndegoAsyncClient.start", return_value=True
            ):
                await func(indego, longpoll=True, longpoll_timeout=10)
                assert getattr(indego, "state") == updated_assert_value


@pytest.mark.parametrize(
    "sync, func, attr, ret_value, assert_value",
    [
        (True, IndegoClient.update_user, "user", USER_RESPONSE, User(**USER_RESPONSE)),
        (False, IndegoAsyncClient.update_user, "user", USER_RESPONSE, User(**USER_RESPONSE)),
    ],
)
@pytest.mark.asyncio
async def test_client_replace(sync, func, attr, ret_value, assert_value, test_config):
    """Calling an update function twice should replace, not duplicate, the stored value."""
    if sync:
        resp = MockResponseSync(ret_value, 200)
        with patch("requests.request", return_value=resp):
            indego = IndegoClient(**test_config)
            func(indego)
            assert getattr(indego, attr) == assert_value
            func(indego)
            assert getattr(indego, attr) == assert_value
    else:
        resp = MockResponseAsync(ret_value, 200)
        with patch("aiohttp.ClientSession.request", return_value=resp), patch(
            "pyIndego.IndegoAsyncClient.start", return_value=True
        ):
            async with IndegoAsyncClient(**test_config) as indego:
                await func(indego)
                assert getattr(indego, attr) == assert_value
                await func(indego)
                assert getattr(indego, attr) == assert_value
