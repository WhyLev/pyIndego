"""Regression tests protecting the sander1988/Indego Home Assistant integration's
exact usage of pyIndego, as catalogued against its source. These are not
generic library tests - each one encodes a specific dependency the
integration has on pyIndego's behavior, so a future change that would break
the integration fails here first.
"""
from unittest.mock import patch

import aiohttp
import pytest

from pyIndego import IndegoAsyncClient

from .conftest import MockResponseAsync
from .data import ALERT_RESPONSE, GENERIC_RESPONSE, OPERATING_RESPONSE, STATE_RESPONSE


@pytest.mark.asyncio
async def test_hub_client_construction_matches_integration(test_config):
    """custom_components/indego/__init__.py constructs the client with exactly
    these keyword arguments, plus set_default_header() right after."""

    async def async_token_refresh():
        return "refreshed-token"

    session = aiohttp.ClientSession(raise_for_status=False)
    try:
        client = IndegoAsyncClient(
            token="initial-token",
            token_refresh_method=async_token_refresh,
            serial=test_config["serial"],
            session=session,
            raise_request_exceptions=True,
        )
        client.set_default_header("User-Agent", "ha-indego-test")
        assert client.serial == test_config["serial"]
    finally:
        await session.close()


@pytest.mark.asyncio
async def test_config_flow_client_construction_matches_integration():
    """custom_components/indego/config_flow.py constructs a short-lived client
    without serial or token_refresh_method, to call get_mowers() once."""
    session = aiohttp.ClientSession(raise_for_status=False)
    try:
        client = IndegoAsyncClient(
            token="initial-token",
            session=session,
            raise_request_exceptions=True,
        )
        resp = MockResponseAsync([{"alm_sn": "SN1"}, {"alm_sn": "SN2"}], 200)
        with patch("aiohttp.ClientSession.request", return_value=resp):
            mowers = client.get_mowers()
            mowers = await mowers
        assert mowers == ["SN1", "SN2"]
        assert all(isinstance(serial, str) for serial in mowers)
    finally:
        await session.close()


@pytest.mark.asyncio
async def test_get_and_put_return_raw_json_not_models(test_config):
    """The integration bypasses update_network/update_config/update_security/
    update_setup entirely and instead calls get()/put() directly, treating the
    result as a plain dict via .get(). These must never become model instances."""
    async with IndegoAsyncClient(**test_config) as indego:
        resp = MockResponseAsync({"rssi": -70, "mcc": 262, "networks": [26201]}, 200)
        with patch("aiohttp.ClientSession.request", return_value=resp):
            result = await indego.get(f"alms/{indego.serial}/network")
        assert isinstance(result, dict)
        assert result.get("rssi") == -70
        assert result.get("networks") == [26201]

        put_resp = MockResponseAsync({"ok": True}, 200)
        with patch("aiohttp.ClientSession.request", return_value=put_resp):
            put_result = await indego.put(f"alms/{indego.serial}/security", {"enabled": True})
        assert isinstance(put_result, dict)


@pytest.mark.asyncio
async def test_get_map_returns_raw_bytes(test_config):
    """download_and_store_map / _update_map_svg fetch the map via raw get()
    and expect bytes back, not a model or a written file (download_map() is
    never called by the integration)."""
    async with IndegoAsyncClient(**test_config) as indego:
        resp = MockResponseAsync(None, 200)
        resp.content._data = b"<svg>fake map</svg>"
        with patch("aiohttp.ClientSession.request", return_value=resp):
            result = await indego.get(f"alms/{indego.serial}/map")
        assert isinstance(result, (bytes, bytearray))


@pytest.mark.asyncio
async def test_state_state_is_a_plain_int(test_config):
    """lawn_mower.py / vacuum.py do raw int range comparisons and dict lookups
    on state.state (e.g. 500 <= state <= 799); it must stay a plain int."""
    resp = MockResponseAsync(STATE_RESPONSE, 200)
    async with IndegoAsyncClient(**test_config) as indego:
        with patch("aiohttp.ClientSession.request", return_value=resp), patch(
            "pyIndego.IndegoAsyncClient.start", return_value=True
        ):
            await indego.update_state()
        assert type(indego.state.state) is int  # noqa: E721 - deliberately exact-type, not isinstance


@pytest.mark.asyncio
async def test_last_completed_mow_and_next_mow_are_real_datetimes(test_config):
    """format_indego_date() calls .astimezone() directly; .isoformat() is
    called directly too - these must stay real datetime objects, never strings."""
    from datetime import datetime

    async with IndegoAsyncClient(**test_config) as indego:
        resp = MockResponseAsync({"last_mowed": "2020-06-29T12:24:03.664+02:00"}, 200)
        with patch("aiohttp.ClientSession.request", return_value=resp):
            await indego.update_last_completed_mow()
        assert isinstance(indego.last_completed_mow, datetime)
        indego.last_completed_mow.isoformat()
        indego.last_completed_mow.astimezone()

        resp = MockResponseAsync({"mow_next": "2020-07-03T10:00:00+02:00"}, 200)
        with patch("aiohttp.ClientSession.request", return_value=resp):
            await indego.update_next_mow()
        assert isinstance(indego.next_mow, datetime)


@pytest.mark.asyncio
async def test_fragile_direct_attribute_paths_used_by_integration(test_config):
    """These specific dotted paths are accessed WITHOUT a getattr guard
    somewhere in the integration (state.state/.error/.svg_xPos/.svg_yPos,
    state_description_detail, online, generic_data.bareToolnumber,
    generic_data.alm_firmware_version, operating_data.garden.size,
    operating_data.battery.percent_adjusted, alerts[].error_code/.message/
    .date/.read_status). A rename anywhere in this list raises AttributeError
    deep inside the integration."""
    async with IndegoAsyncClient(**test_config) as indego:
        state_resp = MockResponseAsync(STATE_RESPONSE, 200)
        with patch("aiohttp.ClientSession.request", return_value=state_resp), patch(
            "pyIndego.IndegoAsyncClient.start", return_value=True
        ):
            await indego.update_state()
        indego.state.state  # noqa: B018
        indego.state.error  # noqa: B018
        indego.state.svg_xPos  # noqa: B018
        indego.state.svg_yPos  # noqa: B018
        indego.state_description_detail  # noqa: B018
        indego.online  # noqa: B018

        generic_resp = MockResponseAsync(GENERIC_RESPONSE, 200)
        with patch("aiohttp.ClientSession.request", return_value=generic_resp):
            await indego.update_generic_data()
        indego.generic_data.bareToolnumber  # noqa: B018
        indego.generic_data.alm_firmware_version  # noqa: B018

        operating_resp = MockResponseAsync(OPERATING_RESPONSE, 200)
        with patch("aiohttp.ClientSession.request", return_value=operating_resp):
            await indego.update_operating_data()
        indego.operating_data.garden.size  # noqa: B018
        indego.operating_data.battery.percent_adjusted  # noqa: B018

        alerts_resp = MockResponseAsync([ALERT_RESPONSE], 200)
        with patch("aiohttp.ClientSession.request", return_value=alerts_resp):
            await indego.update_alerts()
        alert = indego.alerts[0]
        alert.error_code  # noqa: B018
        alert.message  # noqa: B018
        alert.date  # noqa: B018
        alert.read_status  # noqa: B018


@pytest.mark.asyncio
async def test_fragile_calendar_slot_fields_used_by_integration(test_config):
    """_format_calendar_slot()/_schedule_slot_to_text() f-string-format
    slot.StHr/.StMin/.EnHr/.EnMin directly with no getattr guard - the most
    fragile access points in the whole integration."""
    async with IndegoAsyncClient(**test_config) as indego:
        resp = MockResponseAsync(
            {"sel_cal": 1, "cals": [{"cal": 1, "days": [{"day": 0, "slots": [{"En": True, "StHr": 10, "StMin": 0, "EnHr": 13, "EnMin": 0}]}]}]},
            200,
        )
        with patch("aiohttp.ClientSession.request", return_value=resp):
            await indego.update_calendar()
        slot = indego.calendar.days[0].slots[0]
        formatted = f"{slot.StHr:02d}:{slot.StMin:02d}-{slot.EnHr:02d}:{slot.EnMin:02d}"
        assert formatted == "10:00-13:00"
