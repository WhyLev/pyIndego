"""Tests for alert management, mower commands, calendar/predictive-cal puts, and map download."""
from unittest.mock import patch

import pytest

from pyIndego import IndegoAsyncClient, IndegoClient
from pyIndego.exceptions import IndegoCalendarError, IndegoCommandError, IndegoIndexError, IndegoNotLoadedError
from pyIndego.states import Alert

from .conftest import MockResponseAsync, MockResponseSync
from .data import ALERT_RESPONSE


def test_repr(test_config):
    """__repr__ should not blow up, with or without data loaded."""
    indego = IndegoClient(**test_config)
    str(indego)


@pytest.mark.parametrize(
    "alerts, loaded, index, error",
    [
        ([Alert(**ALERT_RESPONSE)], True, 0, None),
        ([Alert(**ALERT_RESPONSE)], True, 1, IndegoIndexError),
        (None, True, 0, IndegoNotLoadedError),
        (None, False, 0, IndegoNotLoadedError),
    ],
)
@pytest.mark.asyncio
async def test_alert_functions(alerts, loaded, index, error, test_config):
    """Test the function for handling alerts."""
    resp = MockResponseSync(True, 200)
    with patch("requests.request", return_value=resp):
        indego = IndegoClient(**test_config)
        indego.alerts = alerts
        indego._alerts_loaded = loaded
        try:
            res = indego.delete_alert(index)
            if error and not loaded:
                assert False
            elif not alerts and loaded:
                assert res is None
            else:
                assert res
        except error:
            assert True
        try:
            res = indego.put_alert_read(index)
            if error and not loaded:
                assert False
            elif not alerts and loaded:
                assert res is None
            else:
                assert res
        except error:
            assert True
        try:
            res = indego.delete_all_alerts()
            if alerts is None and loaded:
                assert res is None
            else:
                assert res
        except error:
            assert True
        try:
            res = indego.put_all_alerts_read()
            if alerts is None and loaded:
                assert res is None
            else:
                assert res
        except error:
            assert True

    resp = MockResponseAsync(True, 200)
    with patch("aiohttp.ClientSession.request", return_value=resp), patch(
        "pyIndego.IndegoAsyncClient.start", return_value=True
    ):
        async with IndegoAsyncClient(**test_config) as indego:
            indego.alerts = alerts
            indego._alerts_loaded = loaded
            try:
                res = await indego.delete_alert(index)
                if error and not loaded:
                    assert False
                elif not alerts and loaded:
                    assert res is None
                else:
                    assert res
            except error:
                assert True
            try:
                res = await indego.put_alert_read(index)
                if error and not loaded:
                    assert False
                elif not alerts and loaded:
                    assert res is None
                else:
                    assert res
            except error:
                assert True
            try:
                res = await indego.delete_all_alerts()
                if alerts is None and loaded:
                    assert res is None
                else:
                    assert res
            except error:
                assert True
            try:
                res = await indego.put_all_alerts_read()
                if alerts is None and loaded:
                    assert res is None
                else:
                    assert res
            except error:
                assert True


@pytest.mark.parametrize(
    "command, param, error",
    [
        ("command", "mow", None),
        ("command", "pause", None),
        ("command", "returnToDock", None),
        ("command", "mows", IndegoCommandError),
        ("mow_mode", "true", None),
        ("mow_mode", "false", None),
        ("mow_mode", "True", None),
        ("mow_mode", "False", None),
        ("mow_mode", True, None),
        ("mow_mode", False, None),
        ("mow_mode", "mows", IndegoCommandError),
        ("pred_cal", None, None),
        ("pred_cal", {"cals": 1}, IndegoCalendarError),
        ("automatic_update", True, None),
        ("automatic_update", False, None),
    ],
)
@pytest.mark.asyncio
async def test_commands(command, param, error, test_config):
    """Test the functions for sending commands to the mower."""
    resp = MockResponseSync(True, 200)
    with patch("requests.request", return_value=resp):
        indego = IndegoClient(**test_config)
        try:
            if command == "command":
                indego.put_command(param)
            elif command == "mow_mode":
                indego.put_mow_mode(param)
            elif command == "pred_cal":
                indego.put_predictive_cal(param) if param else indego.put_predictive_cal()
            elif command == "automatic_update":
                indego.put_automatic_update(param)
            if error:
                assert False
            assert True
        except error:
            assert True

    resp = MockResponseAsync(True, 200)
    with patch("aiohttp.ClientSession.request", return_value=resp), patch(
        "pyIndego.IndegoAsyncClient.start", return_value=True
    ):
        async with IndegoAsyncClient(**test_config) as indego:
            try:
                if command == "command":
                    await indego.put_command(param)
                elif command == "mow_mode":
                    await indego.put_mow_mode(param)
                elif command == "pred_cal":
                    await indego.put_predictive_cal(param) if param else await indego.put_predictive_cal()
                elif command == "automatic_update":
                    await indego.put_automatic_update(param)
                if error:
                    assert False
                assert True
            except error:
                assert True


@pytest.mark.parametrize(
    "config, param, error",
    [(None, None, ValueError), (None, "test.svg", None), ("test.svg", None, None)],
)
@pytest.mark.asyncio
async def test_download(config, param, error, test_config):
    """Test the function for downloading the map."""
    conf = dict(test_config)
    if config:
        conf.update({"map_filename": config})
    with patch("pyIndego.IndegoClient.get", return_value=None):
        indego = IndegoClient(**conf)
        try:
            indego.download_map(param)
            assert indego.map_filename == "test.svg"
            if error:
                assert False
        except error:
            assert True

    with patch("pyIndego.IndegoAsyncClient.start", return_value=True), patch(
        "pyIndego.IndegoAsyncClient.get", return_value=None
    ):
        async with IndegoAsyncClient(**conf) as indego:
            try:
                await indego.download_map(param)
                assert indego.map_filename == "test.svg"
                if error:
                    assert False
            except error:
                assert True
