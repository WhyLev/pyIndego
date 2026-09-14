[![PyPI](https://img.shields.io/pypi/v/pyIndego)](https://pypi.python.org/pypi/pyIndego/)

# API for Bosch Indego lawnmowers

Join the Discord channel to discuss around this integration:
https://discord.gg/aD33GsP

## Source code
For source files and version handling: https://github.com/sander1988/pyIndego

## PyPi package
For PYPI package: https://pypi.org/project/pyIndego

## Home Assistant
For use in Home Assistant: https://github.com/sander1988/Indego

## Basic information needed

The library requires Python 3.11 or above.

Bosch Indego mowers authenticate through Bosch SingleKey ID (OAuth2). pyIndego does not perform the
login itself - it expects the calling application to obtain an OAuth access token (and, if it wants
automatic token refresh, to supply a callback that returns a fresh one) and hand it to the client.

Required information | Description
----------------------|------------
token                 | A valid Bosch SingleKey ID OAuth access token
serial                | The serial number of the mower (optional - see `get_mowers()` below)

## Call the API and the mower
Call the API, synchronously:

```python
from pyIndego import IndegoClient

indego = IndegoClient(token="your-oauth-access-token", serial="your-mower-serial")
indego.update_state()
print(indego.state_description)
```

Call the API, asynchronously:

```python
from pyIndego import IndegoAsyncClient

async with IndegoAsyncClient(token="your-oauth-access-token", serial="your-mower-serial") as indego:
    await indego.update_state()
    print(indego.state_description)
```

The async client can also take an externally managed `aiohttp.ClientSession` (e.g. one you already
own, such as Home Assistant's shared session), in which case pyIndego will not close it:

```python
indego = IndegoAsyncClient(token=token, serial=serial, session=my_session)
```

### Keeping the token fresh

Both clients accept an optional `token_refresh_method` callback. For the async client this must be
an `async` callable returning the (possibly refreshed) token string; it is invoked before every
request:

```python
async def refresh_token() -> str:
    ...  # refresh with your OAuth provider, return the (possibly new) access token

indego = IndegoAsyncClient(token=token, token_refresh_method=refresh_token, serial=serial)
```

### Handling request failures

By default, pyIndego logs unexpected request failures and returns `None`/leaves state unchanged,
so a single flaky request doesn't crash the caller. Pass `raise_request_exceptions=True` to instead
let the underlying HTTP exception (`aiohttp.ClientResponseError`, `asyncio.TimeoutError`,
`requests.HTTPError`, etc.) propagate, so the caller can decide how to handle it (this is what the
Home Assistant integration does):

```python
indego = IndegoAsyncClient(token=token, serial=serial, raise_request_exceptions=True)
```

Errors raised directly by pyIndego itself (invalid command, calendar not loaded, bad alert index,
etc.) always use the [pyIndego.exceptions](#exceptions) hierarchy, regardless of this flag.

### Finding the mower serial

If you don't know the mower's serial number yet, leave `serial` unset and call `get_mowers()`:

```python
mowers = await indego.get_mowers()  # -> ["123456789"]
```

## Properties
### indego.serial
Returns the serial number of the indego mower, is usefull mostly when serial was not initialized.

### indego.online
Returns whether the mower is currently considered online, based on the most recent state update.

### indego.state_description
Returns a description of the state, instead of a number.

### indego.state_description_detail
Returns a detailed description of the state, instead of a number.

### indego.alerts_count
Returns the number of currently loaded alerts.

### indego.next_mows / indego.next_mows_with_tz
The upcoming scheduled mow times from `indego.calendar`, with the latter converted to the garden's
timezone (from `indego.location`).

## Update/download functions
Description for the functions updating data from API and mower. The functions collecting data from only Bosch API does not wake up mower. Functions collecting data from both Bosch API and mower does wake up mower from sleeping.

Call                                                        | Bosch API | Mower | Mower needs to be online
------------------------------------------------------------|-----------|-------|-------------------------
indego.update_alerts()                                      |    X      |       |
indego.update_automatic_update()                             |    X      |       |
indego.update_calendar()                                    |    X      |       |
indego.update_config()                                      |    X      |  X    |
indego.update_generic_data()                                |    X      |       |
indego.update_last_completed_mow()                          |    X      |       |
indego.update_location()                                    |    X      |       |
indego.update_network()                                     |    ?      |  ?    |   ?
indego.update_next_mow()                                    |           |       |
indego.update_operating_data()                              |    X      |  X    |
indego.update_predictive_calendar()                         |    X      |       |
indego.update_predictive_schedule()                         |    X      |       |
indego.update_predictive_setup()                            |    X      |       |
indego.update_predictive_weather()                          |    X      |       |
indego.update_security()                                    |    X      |       |
indego.update_setup()                                       |    X      |       |
indego.update_state()                                       |    X      |       |
indego.update_state(force=True)                             |    X      |       |
indego.update_state(longpoll=True, longpoll_timeout=120)    |    X      |       |
indego.update_updates_available()                           |    X      |  X?   |
indego.update_user()                                        |    X      |       |
indego.download_map(filename='')                            |    ?      |  ?    |

Every `update_x()` method has a matching `get_x()` counterpart that calls it and returns the
resulting value in one call (e.g. `await indego.get_state()`), and an `update_all()` that refreshes
everything *except* the three predictive/SmartMowing-only calls (`update_predictive_setup`,
`update_predictive_weather`, `update_automatic_update`) and `download_map`, since not every mower
generation supports them.

## List of update functions

### indego.update_all()
Updates alerts, calendar, config, generic_data, last_completed_mow, location, network, next_mow,
operating_data, predictive_calendar, predictive_schedule, security, setup, state,
updates_available and user, in one call.

### indego.update_alerts()
Updates alerts to indego.alerts.

```python
[Alert(alert_id='5d48171263c5345a75dbc017', error_code='ntfy_blade_life', headline='Underhållstips.', date='2019-08-05T11:46:26.397Z', message='Kontrollera klippknivarna. Indego har klippt i 100 timmar. Ska den fungera optimalt, kontrollera klippknivarna så att de är i bra skick. Du kan beställa nya knivar via avsnittet Tillbehör.', read_status='unread', flag='warning', push=True, alert_description='Reminder blade life')]
```
Contains: alerts for mower.

### indego.update_automatic_update()
Updates indego.automatic_update with whether the mower is allowed to install firmware updates on
its own.

```python
AutomaticUpdate(allow_automatic_update=True)
```

### indego.update_calendar()
Updates the calendar to indego.calendar with the next planned mows.

```python
Calendar(cal=3, days=[CalendarDay(day=0, day_name='monday', slots=[CalendarSlot(En=True, StHr=10, StMin=0, EnHr=13, EnMin=0), CalendarSlot(En=False, StHr=None, StMin=None, EnHr=None, EnMin=None)]), CalendarDay(day=2, day_name='wednesday', slalendarSlot(En=False, StHr=None, StMin=None, EnHr=None, EnMin=None)])])
```

### indego.update_config()
Updates indego.config with settings for region, border cut, pin lock, id for the wire, bump and alarm mode. This call doesn't work on some Indegos, this function gives an error on Indego 1000, while it works on newer models (e.g., Indego S+ 400).

```python
Config(region=0, language=1, border_cut=0, is_pin_set=True, wire_id=4, bump_sensitivity=0, alarm_mode=True)
```

### indego.update_generic_data()
Updates indego.generic_data with serial, service counter, name, mowing mode, model number and firmware version, model description, voltage for battery, descripton  of mowing mode.

```python
GenericData(alm_name='Indego', alm_sn='505703041', service_counter=132436, needs_service=False, alm_mode='calendar', bareToolnumber='3600HA2300', alm_firmware_version='00837.01043', model_description='Indego 1000', model_voltage=ModelVoltage(min=297, max=369), mowing_mode_description='Calendar')
```

### indego.update_last_completed_mow()
Updates indego.last_completed_mow with date and time of the latest completed mow.

```python
2020-06-21 21:38:50.115000+02:00
```

### indego.update_location()
Updates indego.location with the location of the garden/mower.

```python
Location(latitude='59.742950', longitude='17.380440', timezone='Europe/Berlin')
```

### indego.update_network()
Updates indego.network with data on the mobile network the Indego is connected to.

```python
Network(mcc=262, mnc=2, rssi=-77, currMode='s', configMode='s', steeredRssi=-100, networkCount=3, networks=[26201, 26202, 26203])
```

### indego.update_next_mow()
Updates the indego.next_mow with the next planned mow date and time.

```python
2020-06-29 10:00:00+02:00
```
or
```python
None
```

### indego.update_operating_data()
Update the indego.operating_data with data about battery, runtime, garden data and temperature.

```python
OperatingData(hmiKeys=1768, battery=Battery(percent=357, voltage=35.7, cycles=0, discharge=0.0, ambient_temp=26, battery_temp=26, percent_adjusted=83), garden=Garden(id=8, name=1, signal_id=1, size=769, inner_bounds=3, cuts=15, runtime=166824, charge=37702, bumps=6646, stops=29, last_mow=1, map_cell_size=None), runtime=Runtime(total=RuntimeDetail(operate=1715, charge=387, cut=1328), session=RuntimeDetail(operate=9, charge=0, cut=0)))
```

### indego.update_predictive_calendar()
Updates the indego.predictive_calendar with the timeslots (days and hours) where the user wants smart mowing not to mow the lawn.

```python
Calendar(cal=1, days=[CalendarDay(day=0, day_name='monday', slots=[CalendarSlot(En=True, StHr=0, StMin=0, EnHr=8, EnMin=0, Attr=None), CalendarSlot(En=True, StHr=20, StMin=0, EnHr=23, EnMin=59, Attr=None)]), ...])
```

### indego.update_predictive_schedule()
Updates the indego.predictive_schedule with the next planned mows (schedule_days) and the days where the smart mowing will not mow the lawn. The latter is combined by the time slots where the user does not want the Indego to mow (Attr='C') and the slots where the weather conditions prevent the mowing (e.g., Attr='pP').

```python
PredictiveSchedule(schedule_days=[CalendarDay(day=0, day_name='monday', slots=[CalendarSlot(En=True, StHr=10, StMin=0, EnHr=13, EnMin=0, Attr=None)]), ...], exclusion_days=[...])
```

### indego.update_predictive_setup()
Updates indego.predictive_setup with the SmartMowing configuration: garden size, mowing duration,
full cuts, weather sensitivity and the garden's location.

```python
PredictiveSetup(garden_size=93, mowing_duration=3, rain_factor=1.4, temperature_factor=1.1, garden_location=GardenLocation(latitude='48.7357', longitude='8.9505', timezone='Europe/Berlin', name=None, country=None), full_cuts=3, avoid_rain=True, avoid_temperature=True, use_grass_growth=True, no_mow_calendar_days=[...])
```

### indego.update_predictive_weather()
Updates indego.predictive_weather with the weather forecast SmartMowing uses to plan around rain.

```python
Weather(location=WeatherLocation(name='Berlin', country='DE'), forecast=WeatherForecast(intervals=[WeatherInterval(dateTime='2020-07-03T10:00:00', intervalLength=60, tt=21.5, wwsymbol_mg2008=1, prrr=0.1, rrr=0.0)]))
```

### indego.update_security()
Updates the indego.security with information about the Indego security state.

```python
Security(enabled=True, autolock=False)
```

### indego.update_setup()
Updates the indego.setup with information if the Indego is set up, has pincode and some other unknown values.

```python
Setup(hasOwner=True, hasPin=True, hasMap=True, hasAutoCal=False, hasIntegrityCheckPassed=True)
```

### indego.update_state(force=False, longpoll=False, longpoll_timeout=120)
Updates the indego.state with state of mower, % lawn mowed, position, runtime, map updates, map coordinates (cached).

```python
State(state=64513, map_update_available=True, mowed=78, mowmode=0, xPos=162, yPos=65, charge=None, operate=None, runtime=Runtime(total=RuntimeDetail(operate=1715, charge=387, cut=1328), session=RuntimeDetail(operate=5, charge=0, cut=0)), mapsvgcache_ts=1593207884109, svg_xPos=192, svg_yPos=544, config_change=None, mow_trig=None)
```

### indego.update_state(force=True, longpoll=False, longpoll_timeout=120)
Updates the indego.state with state of mower, % lawn mowed, position, runtime, map updates and real time map coordinates.

### indego.update_state(force=False, longpoll=True, longpoll_timeout=120)
Updates the indego.state with state of mower, % lawn mowed, position, runtime, map coordinates.

When longpoll is set to True, the indego.state must contain a value. It should contain the current state of the mower (you must run a "regular" update.state first). You send the current value to the API, and the API answers back when the state changes.

This function can be used instead of polling the status every couple of seconds: place one longpoll status request with a timeout of max. 230 seconds and the function will provide its return value when the status has been updated. As soon as an answer is received, the next longpoll status request can be placed. This should save traffic on both ends.

### indego.update_updates_available()
Updates `indego.update_available` with status if there are any updates applicable to the mower.

```python
False
```

### indego.update_user()
Updates the `indego.user` with information about the user.

```python
User(email='youremail@mail.com', display_name='Indego', language='sv', country='SE', optIn=True, optInApp=True)
```

## Sending commands

### indego.delete_alert(alert_index)
Delete an alert from the list, index should exist. If this is called before update_alerts it will not work.

### indego.put_alert_read(alert_index)
Set the specified alert to read. This is a one way action, once read it is not possible to set back to unread. The function looks up the alert_id from indego.alerts, if it cannot find that ID or if update_alerts has not been run, this will stop and log a warning.

### indego.put_all_alerts_read()
Set all alerts to read, the function loops through the alert_id's from indego.alerts, if update_alerts has not been run, this will stop and log a warning.

### indego.put_command(command)
Send commands.

Command     |Description
------------|--------------------
put_command('mow')          |Start mowing
put_command('pause')        |Pause mower
put_command('returnToDock') |Return mower to dock

### indego.put_mow_mode(command)
Send command. Accepted commands:

Command     |Description
------------|--------------------
put_mow_mode(True)  |Smart Mow enabled
put_mow_mode(False) |Smart Mow disabled

### indego.put_predictive_cal(calendar)
Set the predictive (SmartMowing exclusion) calendar. `calendar` must be a dict shaped like
`pyIndego.const.DEFAULT_CALENDAR`.

### indego.put_automatic_update(enabled)
Enable or disable automatic firmware updates.

## Attributes for reading data from locally cached API data
All functions that doesn't contain "update" first in name is collecting data from locally stored variables in the function. No API calls to Bosch or mower.

attributes                 | Description
-------------------------|-----------------------------
alerts_count | Show counts of the current alerts.
alerts | Show detailed list of alerts.
calendar | Get the calendar of planned mows.
automatic_update | Whether automatic firmware updates are enabled.
predictive_setup | SmartMowing configuration (garden size, duration, weather sensitivity).
predictive_weather | Weather forecast used by SmartMowing.
online | Whether the mower is currently considered online.
state_description | Show simple description of current state. States available are Docked, Mowing, Stuck, Diagnostics mode, End of life, Software update.
state_description_detail | Show description in detail of current state.
next_mow | Show next planned mow session.
serial | Show serial number

## Exceptions

Errors raised directly by pyIndego (as opposed to transport-level exceptions from `aiohttp`/
`requests`, which propagate unwrapped when `raise_request_exceptions=True`) all derive from
`pyIndego.exceptions.IndegoError`. The ones that used to be plain `ValueError`/`IndexError`
instances also still inherit from those built-in types, so existing `except ValueError` /
`except IndexError` code keeps working unchanged:

- `IndegoError` - base class for everything below.
- `IndegoValueError(IndegoError, ValueError)`
- `IndegoIndexError(IndegoError, IndexError)` - bad alert index.
- `IndegoNotLoadedError(IndegoValueError)` - alert operation attempted before `update_alerts()`.
- `IndegoCommandError(IndegoValueError)` - invalid `put_command`/`put_mow_mode` argument.
- `IndegoCalendarError(IndegoValueError)` - invalid `put_predictive_cal` payload.

## Module layout

As of 4.0.0, the data model classes (`Alert`, `State`, `GenericData`, `Calendar`, ...) live in
`pyIndego.models`, split by concern across a few modules. `pyIndego.states` re-exports them all
under their original names for backward compatibility - `from pyIndego.states import Alert` still
works, but new code can import from `pyIndego.models` directly.

Model construction tolerates unknown fields: since Bosch's API is undocumented and occasionally
grows new fields, pyIndego drops fields it doesn't recognize (logged at debug level) rather than
raising `TypeError`.

# API CALLS
https://api.indego-cloud.iot.bosch-si.com/api/v1/


```python
get
/alerts
/alms
/alms/<serial>
/alms/<serial>/automaticUpdate
/alms/<serial>/calendar
/alms/<serial>/config
/alms/<serial>/map
/alms/<serial>/network
/alms/<serial>/updates
/alms/<serial>/operatingData
/alms/<serial>/predictive
/alms/<serial>/predictive/calendar
/alms/<serial>/predictive/lastcutting
/alms/<serial>/predictive/location
/alms/<serial>/predictive/nextcutting
/alms/<serial>/predictive/schedule
/alms/<serial>/predictive/setup
/alms/<serial>/predictive/useradjustment
/alms/<serial>/predictive/weather
/alms/<serial>/security
/alms/<serial>/setup
/alms/<serial>/state
/users/<userid>

put
/alms/<serial>/automaticUpdate
/alms/<serial>/predictive/calendar
/alms/<serial>/predictive/location
/alms/<serial>/predictive
/alms/<serial>/state
/alms/<serial>/predictive/useradjustment

delete
/alerts/<alertid>
```

For anything pyIndego doesn't (yet) model as a typed method, `indego.get(path)` and
`indego.put(path, data)` give raw access to any endpoint under the base URL above, returning
whatever the API sends back (a parsed dict/list for JSON, raw bytes otherwise) rather than a model.

# Contributing
The project development is done in a Python virtual environment.

## Setup your environment
Steps required to setup your environment for development and testing:
* Setup your Python virtual environment `python -m venv .venv`.
* Activate the virtual environment by running `source .venv/bin/activate`
* Install the package with its testing extras: `pip install -e ".[testing]"`
* Run `pytest` to test your environment.
* Run `ruff check pyIndego tests` to lint.
