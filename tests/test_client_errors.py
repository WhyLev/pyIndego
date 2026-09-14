"""Tests for HTTP error handling, including the raise_request_exceptions=True
path the Home Assistant integration always uses."""
import asyncio
from socket import error as SocketError
from unittest.mock import patch

import aiohttp
import pytest
import requests
from aiohttp import ClientOSError, ClientResponseError, ServerTimeoutError, TooManyRedirects
from aiohttp.web_exceptions import HTTPGatewayTimeout
from requests.exceptions import RequestException, Timeout
from requests.exceptions import TooManyRedirects as ReqTooManyRedirects

from pyIndego import IndegoAsyncClient, IndegoClient
from pyIndego.const import Methods

from .conftest import AsyncMock, MockResponseAsync, MockResponseSync
from .data import USER_RESPONSE


@pytest.mark.parametrize(
    "sync, response, func, attr, ret_value",
    [
        (True, 204, IndegoClient.update_user, "user", USER_RESPONSE),
        (True, 400, IndegoClient.update_user, "user", USER_RESPONSE),
        (True, 401, IndegoClient.update_user, "user", USER_RESPONSE),
        (True, 403, IndegoClient.update_user, "user", USER_RESPONSE),
        (True, 405, IndegoClient.update_user, "user", USER_RESPONSE),
        (True, 501, IndegoClient.update_user, "user", USER_RESPONSE),
        (True, 504, IndegoClient.update_user, "user", USER_RESPONSE),
        (False, 204, IndegoAsyncClient.update_user, "user", USER_RESPONSE),
        (False, 400, IndegoAsyncClient.update_user, "user", USER_RESPONSE),
        (False, 401, IndegoAsyncClient.update_user, "user", USER_RESPONSE),
        (False, 403, IndegoAsyncClient.update_user, "user", USER_RESPONSE),
        (False, 405, IndegoAsyncClient.update_user, "user", USER_RESPONSE),
        (False, 501, IndegoAsyncClient.update_user, "user", USER_RESPONSE),
        (False, 504, IndegoAsyncClient.update_user, "user", USER_RESPONSE),
    ],
)
@pytest.mark.asyncio
async def test_client_responses_default_swallows_errors(sync, response, func, attr, ret_value, test_config):
    """By default (raise_request_exceptions=False) request failures are logged, not raised."""
    if sync:
        resp = MockResponseSync(ret_value, response)
        with patch("requests.request", return_value=resp):
            indego = IndegoClient(**test_config)
            func(indego)
            assert getattr(indego, attr) is None
    else:
        resp = MockResponseAsync(ret_value, response)
        with patch("aiohttp.ClientSession.request", return_value=resp):
            async with IndegoAsyncClient(**test_config) as indego:
                await func(indego)
                assert getattr(indego, attr) is None


@pytest.mark.parametrize("status", [400, 401, 403, 405, 500, 501])
@pytest.mark.asyncio
async def test_async_raise_request_exceptions_true_propagates_client_response_error(status, test_config):
    """This is exactly what the Home Assistant integration relies on: with
    raise_request_exceptions=True, a failing HTTP call must raise
    aiohttp.ClientResponseError with a `.status` attribute, not swallow it."""
    resp = MockResponseAsync(None, status)
    with patch("aiohttp.ClientSession.request", return_value=resp):
        async with IndegoAsyncClient(raise_request_exceptions=True, **test_config) as indego:
            with pytest.raises(aiohttp.ClientResponseError) as exc_info:
                await indego.update_state()
            assert exc_info.value.status == status


@pytest.mark.asyncio
async def test_async_raise_request_exceptions_true_propagates_timeout_error(test_config):
    """A longpoll timeout must surface as asyncio.TimeoutError, unwrapped."""
    with patch("aiohttp.ClientSession.request", side_effect=asyncio.TimeoutError()):
        async with IndegoAsyncClient(raise_request_exceptions=True, **test_config) as indego:
            with pytest.raises(asyncio.TimeoutError):
                await indego.update_state(longpoll=True, longpoll_timeout=10)


@pytest.mark.parametrize("status", [400, 401, 403, 405, 500, 501])
def test_sync_raise_request_exceptions_true_propagates_http_error(status, test_config):
    """The sync client should behave symmetrically with the async client."""
    resp = MockResponseSync(None, status)
    with patch("requests.request", return_value=resp):
        indego = IndegoClient(raise_request_exceptions=True, **test_config)
        with pytest.raises(requests.HTTPError):
            indego.update_state()


@pytest.mark.parametrize("error", [Timeout, ReqTooManyRedirects, RequestException])
def test_sync_raise_request_exceptions_true_propagates_transport_errors(error, test_config):
    """Regression test: previously the sync client silently swallowed these
    even when raise_request_exceptions=True, unlike the async client."""
    with patch("requests.request", side_effect=error):
        indego = IndegoClient(raise_request_exceptions=True, **test_config)
        with pytest.raises(error):
            indego._request(method=Methods.GET, path="alerts", timeout=1)


@pytest.mark.parametrize(
    "error",
    [asyncio.CancelledError, Exception, asyncio.TimeoutError, ServerTimeoutError, HTTPGatewayTimeout, ClientOSError, TooManyRedirects, ClientResponseError, SocketError],
)
@pytest.mark.asyncio
async def test_a_client_response_errors(error, test_config):
    """With the default raise_request_exceptions=False, transport errors are swallowed."""
    with patch("aiohttp.ClientSession.request", side_effect=error), patch(
        "asyncio.sleep", new_callable=AsyncMock
    ):
        async with IndegoAsyncClient(**test_config) as indego:
            resp = await indego._request(method=Methods.GET, path="alerts", timeout=1)
            assert resp is None


@pytest.mark.parametrize("error", [Exception, Timeout, ReqTooManyRedirects, RequestException])
def test_client_response_errors(error, test_config):
    """With the default raise_request_exceptions=False, transport errors are swallowed."""
    with patch("requests.request", side_effect=error):
        indego = IndegoClient(**test_config)
        resp = indego._request(method=Methods.GET, path="alerts", timeout=1)
        assert resp is None
