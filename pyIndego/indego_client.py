"""API for Bosch API server for Indego lawn mower."""
import logging
import json
import time
from typing import Any, Dict, Optional, List

import requests
from requests.exceptions import RequestException, Timeout, TooManyRedirects

from .const import (
    COMMANDS,
    CONTENT_TYPE,
    CONTENT_TYPE_JSON,
    DEFAULT_CALENDAR,
    Methods,
)
from .indego_base_client import IndegoBaseClient
from .states import Calendar
from .helpers import random_request_id, validate_command, validate_mow_mode
from .exceptions import IndegoConnectionError, IndegoRequestError, IndegoAuthError

_LOGGER = logging.getLogger(__name__)


class IndegoClient(IndegoBaseClient):
    """Class for Indego Non-Async Client."""

    def __enter__(self):
        """Enter for with."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit for with."""
        pass

    def get_mowers(self) -> List[str]:
        """Get a list of the available mowers (serials) in the account."""
        result = self.get("alms")
        if result is None:
            return []
        return [mower['alm_sn'] for mower in result]

    def delete_alert(self, alert_index: int) -> Optional[Dict]:
        """Delete the alert with the specified index.

        Args:
            alert_index (int): index of alert to be deleted, should be in range or length of alerts.

        """
        if not self._alerts_loaded:
            raise ValueError("Alerts not loaded, please run update_alerts first.")
        alert_id = self._get_alert_by_index(alert_index)
        if alert_id is None:
            return None
        return self._request(Methods.DELETE, f"alerts/{alert_id}/")

    def delete_all_alerts(self) -> Optional[List]:
        """Delete all the alerts."""
        if not self._alerts_loaded:
            raise ValueError("Alerts not loaded, please run update_alerts first.")
        if self.alerts_count > 0:
            return [
                self._request(Methods.DELETE, f"alerts/{alert.alert_id}")
                for alert in self.alerts
            ]
        _LOGGER.info("No alerts to delete")
        return None

    def download_map(self, filename: Optional[str] = None) -> None:
        """Download the map.

        Args:
            filename (str, optional): Filename for the map. Defaults to None, can also be filled by the filename set in init.

        """
        if not self.serial:
            return
        if filename:
            self.map_filename = filename
        if not self.map_filename:
            raise ValueError("No map filename defined.")
        lawn_map = self.get(f"alms/{self.serial}/map")
        if lawn_map:
            with open(self.map_filename, "wb") as afp:
                afp.write(lawn_map)

    def put_alert_read(self, alert_index: int) -> Optional[Dict]:
        """Set the alert to read.

        Args:
            alert_index (int): index of alert to be deleted, should be in range or length of alerts.

        """
        if not self._alerts_loaded:
            raise ValueError("Alerts not loaded, please run update_alerts first.")
        alert_id = self._get_alert_by_index(alert_index)
        if alert_id:
            return self._request(
                Methods.PUT, f"alerts/{alert_id}", data={"read_status": "read"}
            )

    def put_all_alerts_read(self) -> Optional[List]:
        """Set to read the read_status of all alerts."""
        if not self._alerts_loaded:
            raise ValueError("Alerts not loaded, please run update_alerts first.")
        if self.alerts_count > 0:
            return [
                self._request(
                    Methods.PUT,
                    f"alerts/{alert.alert_id}",
                    data={"read_status": "read"},
                )
                for alert in self.alerts
            ]
        _LOGGER.info("No alerts to set to read")
        return None

    def put_command(self, command: str) -> Optional[Dict]:
        """Send a command to the mower.

        Args:
            command (str): command should be one of "mow", "pause", "returnToDock"

        Returns:
            str: either result of the call or 'Wrong Command'

        """
        if not validate_command(command):
            raise ValueError("Wrong Command, use one of 'mow', 'pause', 'returnToDock'")
        if not self.serial:
            return None
        return self.put(f"alms/{self.serial}/state", {"state": command})

    def put_mow_mode(self, command: Any) -> Optional[Dict]:
        """Set the mower to mode manual (false-ish) or predictive (true-ish).

        Args:
            command (str/bool): should be str that is bool-ish (true, True, false, False) or a bool.

        Returns:
            str: either result of the call or 'Wrong Command'

        """
        if not validate_mow_mode(command):
            raise ValueError("Wrong Command, use True or False")
        if not self.serial:
            return None
        return self.put(f"alms/{self.serial}/predictive", {"enabled": command})

    def put_predictive_cal(self, calendar: Dict = DEFAULT_CALENDAR) -> Optional[Dict]:
        """Set the predictive calendar."""
        try:
            Calendar(**calendar["cals"][0])
        except TypeError as exc:
            raise ValueError("Value for calendar is not valid") from exc
        if not self.serial:
            return
        return self.put(f"alms/{self.serial}/predictive/calendar", calendar)

    def update_alerts(self) -> None:
        """Update alerts."""
        self._update_alerts(self.get("alerts"))

    def get_alerts(self) -> List:
        """Update alerts and return them."""
        self.update_alerts()
        return self.alerts

    def update_all(self) -> None:
        """Update all states."""
        self.update_alerts()
        self.update_calendar()
        self.update_config()
        self.update_generic_data()
        self.update_last_completed_mow()
        self.update_location()
        self.update_network()
        self.update_next_mow()
        self.update_operating_data()
        self.update_predictive_calendar()
        self.update_predictive_schedule()
        self.update_security()
        self.update_setup()
        self.update_state()
        self.update_updates_available()
        self.update_user()

    def update_calendar(self) -> None:
        """Update calendar."""
        if not self.serial:
            return
        self._update_calendar(self.get(f"alms/{self.serial}/calendar"))

    def get_calendar(self):
        """Update calendar and return it."""
        self.update_calendar()
        return self.calendar

    def update_config(self) -> None:
        """Update config."""
        if not self.serial:
            return
        self._update_config(self.get(f"alms/{self.serial}/config"))

    def get_config(self):
        """Update config and return it."""
        self.update_config()
        return self.config

    def update_generic_data(self) -> None:
        """Update generic data."""
        if not self.serial:
            return
        self._update_generic_data(self.get(f"alms/{self.serial}"))

    def get_generic_data(self):
        """Update generic_data and return it."""
        self.update_generic_data()
        return self.generic_data

    def update_last_completed_mow(self) -> None:
        """Update last completed mow."""
        if not self.serial:
            return
        self._update_last_completed_mow(
            self.get(f"alms/{self.serial}/predictive/lastcutting")
        )

    def get_last_completed_mow(self):
        """Update last_completed_mow and return it."""
        self.update_last_completed_mow()
        return self.last_completed_mow

    def update_location(self) -> None:
        """Update location."""
        if not self.serial:
            return
        self._update_location(self.get(f"alms/{self.serial}/predictive/location"))

    def get_location(self):
        """Update location and return it."""
        self.update_location()
        return self.location

    def update_network(self) -> None:
        """Update network."""
        if not self.serial:
            return
        self._update_network(self.get(f"alms/{self.serial}/network"))

    def get_network(self):
        """Update network and return it."""
        self.update_network()
        return self.network

    def update_next_mow(self) -> None:
        """Update next mow datetime."""
        if not self.serial:
            return
        self._update_next_mow(self.get(f"alms/{self.serial}/predictive/nextcutting"))

    def get_next_mow(self):
        """Update next_mow and return it."""
        self.update_next_mow()
        return self.next_mow

    def update_operating_data(self) -> None:
        """Update operating data."""
        if not self.serial:
            return
        self._update_operating_data(self.get(f"alms/{self.serial}/operatingData"))

    def get_operating_data(self):
        """Update operating_data and return it."""
        self.update_operating_data()
        return self.operating_data

    def update_predictive_calendar(self) -> None:
        """Update predictive_calendar."""
        if not self.serial:
            return
        self._update_predictive_calendar(
            self.get(f"alms/{self.serial}/predictive/calendar")
        )

    def get_predictive_calendar(self):
        """Update predictive_calendar and return it."""
        self.update_predictive_calendar()
        return self.predictive_calendar

    def update_predictive_schedule(self) -> None:
        """Update predictive_schedule."""
        if not self.serial:
            return
        self._update_predictive_schedule(
            self.get(f"alms/{self.serial}/predictive/schedule")
        )

    def get_predictive_schedule(self):
        """Update predictive_schedule and return it."""
        self.update_predictive_schedule()
        return self.predictive_schedule

    def update_security(self) -> None:
        """Update security."""
        if not self.serial:
            return
        self._update_security(self.get(f"alms/{self.serial}/security"))

    def get_security(self):
        """Update security and return it."""
        self.update_security()
        return self.security

    def update_setup(self) -> None:
        """Update setup."""
        if not self.serial:
            return
        self._update_setup(self.get(f"alms/{self.serial}/setup"))

    def get_setup(self):
        """Update setup and return it."""
        self.update_setup()
        return self.setup

    def update_state(self, force=False, longpoll=False, longpoll_timeout=120) -> None:
        """Update state. Can be both forced and with longpoll.

        Args:
            force (bool, optional): Force the state refresh, wakes up the mower. Defaults to False.
            longpoll (bool, optional): Do a longpoll. Defaults to False.
            longpoll_timeout (int, optional): Timeout of the longpoll. Defaults to 120.

        """
        if not self.serial:
            return
        path = f"alms/{self.serial}/state"
        if longpoll:
            last_state = 0
            if self.state:
                if self.state.state:
                    last_state = self.state.state
            path = f"{path}?longpoll=true&timeout={longpoll_timeout}&last={last_state}"
        if force:
            if longpoll:
                path = f"{path}&forceRefresh=true"
            else:
                path = f"{path}?forceRefresh=true"

        self._update_state(self.get(path, timeout=(longpoll_timeout + 10) if longpoll else 10))

    def get_state(self, force=False, longpoll=False, longpoll_timeout=120):
        """Update state. Can be both forced and with longpoll.

        Args:
            force (bool, optional): Force the state refresh, wakes up the mower. Defaults to False.
            longpoll (bool, optional): Do a longpoll. Defaults to False.
            longpoll_timeout (int, optional): Timeout of the longpoll. Defaults to 120.

        """
        self.update_state(force, longpoll, longpoll_timeout)
        return self.state

    def update_updates_available(self) -> None:
        """Update updates available."""
        if not self.serial:
            return
        if self._online:
            self._update_updates_available(self.get(f"alms/{self.serial}/updates"))

    def get_updates_available(self):
        """Update updates_available and return it."""
        self.update_updates_available()
        return self.update_available

    def update_user(self) -> None:
        """Update users."""
        self._update_user(self.get(f"users/{self._userid}"))

    def get_user(self):
        """Update user and return it."""
        self.update_user()
        return self.user

    def _request(  # noqa: C901
        self,
        method: Methods,
        path: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: int = 30,
    ) -> Optional[Any]:
        """Send a request and return the response."""
        if self._token_refresh_method is not None:
            self._token = self._token_refresh_method()

        url = f"{self._api_url}{path}"

        if not headers:
            headers = self._default_headers.copy()
            headers["Authorization"] = "Bearer %s" % self._token

        request_id = random_request_id()
        request_start_time = time.time()
        try:
            log_headers = headers.copy()
            if 'Authorization' in log_headers:
                log_headers['Authorization'] = '******'
            _LOGGER.debug(
                "[%s] %s call to API endpoint %s, headers: %s, data: %s",
                request_id,
                method.value,
                url,
                json.dumps(log_headers) if log_headers is not None else '',
                json.dumps(data) if data is not None else '',
            )

            response = requests.request(
                method=method.value,
                url=url,
                json=data,
                headers=headers,
                timeout=timeout,
            )
            status = response.status_code
            _LOGGER.debug("[%s] HTTP status code: %i", request_id, status)

            is_json = CONTENT_TYPE_JSON in response.headers[CONTENT_TYPE].split(";")
            if status == 200:
                if method in (Methods.DELETE, Methods.PATCH, Methods.PUT):
                    return True
                if is_json:
                    return response.json()
                return response.content

            if self._log_request_result(request_id, status, url):
                return {} if is_json else ""

            response.raise_for_status()

        except Timeout as exc:
            if self._raise_request_exceptions:
                raise IndegoConnectionError(
                    f"Request to {path} timed out after {time.time() - request_start_time:.1f}s: {exc}"
                ) from exc
            _LOGGER.error(
                "[%s] %s %s request timed out after %.1f seconds: %s",
                request_id,
                method.value,
                path,
                time.time() - request_start_time,
                str(exc)
            )

        except (TooManyRedirects, RequestException) as exc:
            if self._raise_request_exceptions:
                raise IndegoConnectionError(
                    f"Request to {path} failed after {time.time() - request_start_time:.1f}s: {exc}"
                ) from exc
            _LOGGER.error(
                "[%s] %s %s failed after %.1f seconds: %s",
                request_id,
                method.value,
                path,
                time.time() - request_start_time,
                str(exc)
            )

        except Exception as exc:
            if self._raise_request_exceptions:
                raise
            _LOGGER.error(
                "[%s] Request %s %s gave a unhandled error after %.1f seconds: %s",
                request_id,
                method.value,
                path,
                time.time() - request_start_time,
                str(exc)
            )

        return None

    def get(self, path: str, timeout: int = 30) -> Optional[Any]:
        """Send a GET request and return the response as a dict."""
        return self._request(method=Methods.GET, path=path, timeout=timeout)

    def put(self, path: str, data: Dict, timeout: int = 30) -> Optional[Any]:
        """Send a PUT request and return the response as a dict."""
        return self._request(method=Methods.PUT, path=path, data=data, timeout=timeout)
