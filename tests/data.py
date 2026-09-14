"""Shared mock API response payloads used across the test suite."""
from typing import Final

ALERT_RESPONSE: Final = {
    "alm_sn": "test_sn",
    "alert_id": "5efda84ffbf591182723be89",
    "error_code": "104",
    "headline": "Mower requires attention.",
    "date": "2020-07-02T09:26:39.589Z",
    "message": "Stop button activated. The Stop button has been activated. Please follow the instructions on the mower display.",
    "read_status": "read",
    "flag": "warning",
    "push": True,
}

CALENDAR_RESPONSE = {
    "cal": 3,
    "days": [
        {
            "day": 0,
            "slots": [
                {"En": True, "StHr": 10, "StMin": 0, "EnHr": 13, "EnMin": 0},
                {"En": False},
            ],
        },
        {
            "day": 2,
            "slots": [
                {"En": True, "StHr": 11, "StMin": 0, "EnHr": 14, "EnMin": 0},
                {"En": False},
            ],
        },
        {
            "day": 4,
            "slots": [
                {"En": True, "StHr": 10, "StMin": 0, "EnHr": 13, "EnMin": 0},
                {"En": False},
            ],
        },
    ],
}

SETUP_RESPONSE: Final = {
    "hasOwner": True,
    "hasPin": True,
    "hasMap": True,
    "hasAutoCal": False,
    "hasIntegrityCheckPassed": True,
}

LOCATION_RESPONSE: Final = {
    "latitude": "1.1234",
    "longitude": "1.1234",
    "timezone": "Europe/Amsterdam",
}

USER_RESPONSE: Final = {
    "email": "test@test.com",
    "display_name": "test",
    "language": "en",
    "country": "NL",
    "optIn": False,
    "optInApp": False,
}

SECURITY_RESPONSE: Final = {"enabled": True, "autolock": False}

GENERIC_RESPONSE: Final = {
    "alm_sn": "test_sn",
    "service_counter": 69272,
    "needs_service": False,
    "alm_mode": "smart",
    "bareToolnumber": "3600HB0102",
    "alm_firmware_version": "17329.01211",
}

LAST_CUTTING_RESPONSE: Final = {"last_mowed": "2020-06-29T12:24:03.664+02:00"}

NEXT_CUTTING_RESPONSE: Final = {"mow_next": "2020-07-03T10:00:00+02:00"}

NETWORK_RESPONSE: Final = {"mcc": 204, "mnc": 16, "rssi": -83}

CONFIG_RESPONSE: Final = {
    "region": 0,
    "language": 14,
    "border_cut": 0,
    "is_pin_set": True,
    "wire_id": 4,
    "bump_sensitivity": 0,
    "alarm_mode": False,
}

OPERATING_RESPONSE: Final = {
    "runtime": {
        "total": {"operate": 81106, "charge": 11834},
        "session": {"operate": 12, "charge": 12},
    },
    "battery": {
        "voltage": 8.6,
        "cycles": 1,
        "discharge": 0.0,
        "ambient_temp": 23,
        "battery_temp": 23,
        "percent": 86,
    },
    "garden": {
        "id": 34,
        "name": 1,
        "signal_id": 4,
        "size": 80,
        "inner_bounds": 238,
        "cuts": 61172,
        "runtime": 12,
        "charge": 11834,
        "bumps": 183,
        "stops": 10,
        "last_mow": 6,
        "map_cell_size": 120,
    },
    "hmiKeys": 213,
}

PREDICTIVE_CALENDAR_RESPONSE: Final = {
    "sel_cal": 1,
    "cals": [
        {
            "cal": 1,
            "days": [
                {
                    "day": 0,
                    "slots": [
                        {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0},
                        {"En": True, "StHr": 20, "StMin": 0, "EnHr": 23, "EnMin": 59},
                    ],
                },
            ],
        }
    ],
}

PREDICTIVE_SCHEDULE_RESPONSE: Final = {
    "schedule_days": [
        {
            "day": 1,
            "slots": [{"En": True, "StHr": 10, "StMin": 0, "EnHr": 13, "EnMin": 0}],
        },
    ],
    "exclusion_days": [
        {
            "day": 0,
            "slots": [
                {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0, "Attr": "C"},
                {"En": True, "StHr": 8, "StMin": 0, "EnHr": 12, "EnMin": 0, "Attr": "pP"},
            ],
        },
    ],
}

STATE_RESPONSE: Final = {
    "state": 64513,
    "map_update_available": True,
    "mowed": 97,
    "mowmode": 2,
    "xPos": 5,
    "yPos": 50,
    "runtime": {
        "total": {"operate": 81329, "charge": 11912},
        "session": {"operate": 10, "charge": 0},
    },
    "mapsvgcache_ts": 1593609416617,
    "svg_xPos": 720,
    "svg_yPos": 424,
    "config_change": False,
    "mow_trig": True,
}

STATE_UPDATE_RESPONSE: Final = {"state": 513}

STATE_FULL_UPDATE_RESPONSE: Final = {
    "state": 513,
    "map_update_available": True,
    "mowed": 97,
    "mowmode": 2,
    "xPos": 5,
    "yPos": 50,
    "runtime": {
        "total": {"operate": 81329, "charge": 11912},
        "session": {"operate": 10, "charge": 0},
    },
    "mapsvgcache_ts": 1593609416617,
    "svg_xPos": 720,
    "svg_yPos": 424,
    "config_change": False,
    "mow_trig": True,
}

AUTOMATIC_UPDATE_RESPONSE: Final = {"allow_automatic_update": True}

PREDICTIVE_SETUP_RESPONSE: Final = {
    "garden_size": 93,
    "mowing_duration": 3,
    "rain_factor": 1.4,
    "temperature_factor": 1.1,
    "garden_location": {
        "latitude": "48.7357",
        "longitude": "8.9505",
        "timezone": "Europe/Berlin",
    },
    "full_cuts": 3,
    "avoid_rain": True,
    "avoid_temperature": True,
    "use_grass_growth": True,
    "no_mow_calendar_days": [
        {
            "day": 0,
            "slots": [
                {"En": True, "StHr": 0, "StMin": 0, "EnHr": 8, "EnMin": 0},
            ],
        },
    ],
}

PREDICTIVE_WEATHER_RESPONSE: Final = {
    "LocationWeather": {
        "location": {"name": "Berlin", "country": "DE"},
        "forecast": {
            "intervals": [
                {
                    "dateTime": "2020-07-03T10:00:00",
                    "intervalLength": 60,
                    "tt": 21.5,
                    "wwsymbol_mg2008": 1,
                    "prrr": 0.1,
                    "rrr": 0.0,
                },
            ]
        },
    }
}
