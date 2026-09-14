"""Shared test fixtures: config and realistic sync/async HTTP response mocks.

The mocks intentionally implement the same surface real `requests.Response`
/ `aiohttp.ClientResponse` objects expose for the code paths pyIndego's
request layer exercises (``.content``, ``.raise_for_status()``), so that
tests actually cover the non-200 and ``raise_request_exceptions=True``
paths instead of silently short-circuiting on an incomplete mock.
"""
import json as json_module

import aiohttp
import pytest
import requests

from pyIndego.const import CONTENT_TYPE, CONTENT_TYPE_JSON

TEST_CONFIG = {"serial": "123456789", "token": "testtoken"}


class AsyncMock:
    """A minimal async-callable mock, standing in for unittest.mock.AsyncMock
    where a plain return value (rather than a coroutine) needs awaiting."""

    def __init__(self, return_value=None):
        self.return_value = return_value

    async def __call__(self, *args, **kwargs):
        return self.return_value


class MockContent:
    """Stand-in for aiohttp's StreamReader (`response.content`)."""

    def __init__(self, data: bytes):
        self._data = data

    async def read(self):
        return self._data


class MockResponseAsync:
    """Stand-in for aiohttp.ClientResponse used as an async context manager."""

    def __init__(self, json, status):
        self._json = json
        self.status = status
        raw = b"" if json is None else json_module.dumps(json).encode()
        self.content = MockContent(raw)
        self.request_info = aiohttp.RequestInfo(
            url=aiohttp.client.URL("https://example.invalid/"), method="GET", headers={}
        )
        self.history = ()

    async def json(self):
        return self._json

    @property
    def content_type(self):
        if self._json is not None:
            return CONTENT_TYPE_JSON
        return None

    def raise_for_status(self):
        if 400 <= self.status:
            raise aiohttp.ClientResponseError(
                self.request_info, self.history, status=self.status, message="mock error"
            )

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


class MockResponseSync:
    """Stand-in for requests.Response."""

    def __init__(self, json, status):
        self._json = json
        self.status_code = status
        self.content = b"" if json is None else json_module.dumps(json).encode()

    def json(self):
        return self._json

    @property
    def headers(self):
        if self._json is not None:
            return {CONTENT_TYPE: f"{CONTENT_TYPE_JSON};"}
        return {}

    def raise_for_status(self):
        if 400 <= self.status_code:
            raise requests.HTTPError(f"mock {self.status_code} error", response=self)


@pytest.fixture
def test_config():
    return dict(TEST_CONFIG)
