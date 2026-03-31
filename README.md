[![PyPI](https://img.shields.io/pypi/v/pyIndego)](https://pypi.python.org/pypi/pyIndego/)

# PyIndego - Python API for Bosch Indego Lawnmowers

PyIndego is a Python library for controlling and monitoring Bosch Indego robotic lawnmowers via the Bosch API.

**Join the Discord channel:** https://discord.gg/aD33GsP

## Links

- **Source code**: https://github.com/sander1988/pyIndego
- **PyPI package**: https://pypi.org/project/pyIndego
- **Home Assistant integration**: https://github.com/sander1988/Indego

## Requirements

- Python 3.8 or higher
- OAuth2 token from Bosch Smart Gardening API (see [Home Assistant integration](https://github.com/sander1988/Indego) for authentication setup)

## Installation

```bash
pip install pyIndego
```

## Quick Start

### Synchronous Usage

```python
from pyIndego import IndegoClient

# Initialize with OAuth2 token
indego = IndegoClient(token='your_oauth2_token')

# Update mower state
indego.update_state()
print(indego.state_description)  # e.g., "Mowing", "Docked", etc.

# Get all alerts
indego.update_alerts()
for alert in indego.alerts:
    print(alert.headline)

# Send a command
indego.put_command('mow')  # Start mowing
```

### Asynchronous Usage

```python
from pyIndego import IndegoAsyncClient

async def main():
    # Initialize with OAuth2 token
    async with IndegoAsyncClient(token='your_oauth2_token') as indego:
        await indego.update_state()
        print(indego.state_description)

        await indego.update_alerts()
        for alert in indego.alerts:
            print(alert.headline)

        # Send a command
        await indego.put_command('mow')

# Run async code
import asyncio
asyncio.run(main())
```

## Authentication

PyIndego uses **OAuth2 token-based authentication**. The token must be obtained from the Bosch Smart Gardening API. The Home Assistant integration handles this automatically.

For direct use, you need to:
1. Authenticate with Bosch Smart Gardening API
2. Obtain an OAuth2 token
3. Pass it to PyIndego as shown above

**Note:** Login with email/password directly is no longer supported. Use OAuth2 tokens only.

## Properties

### `indego.serial`
Returns the serial number of the mower (automatically set after first API call).

### `indego.state_description`
Returns a human-readable state description (e.g., "Mowing", "Docked", "Stuck").

### `indego.state_description_detail`
Returns a detailed state description (e.g., "Mowing - Learning lawn", "Docked - Charging").

### `indego.next_mows`
Returns a list of next scheduled mowing times from the calendar.

### `indego.alerts_count`
Returns the number of current alerts for the mower.

## Update Methods

All update methods fetch data from the Bosch API. Some methods also wake up the mower from sleep.

### Data Update Functions

| Method | Description | API | Mower | Online Required |
|--------|-------------|-----|-------|-----------------|
| `update_alerts()` | Get current alerts | ✓ | - | - |
| `update_calendar()` | Get regular mowing schedule | ✓ | - | - |
| `update_config()` | Get mower configuration | ✓ | ✓ | - |
| `update_generic_data()` | Get mower info (serial, firmware, model) | ✓ | - | - |
| `update_last_completed_mow()` | Get timestamp of last mowing | ✓ | - | - |
| `update_location()` | Get GPS location and timezone | ✓ | - | - |
| `update_network()` | Get mobile network info | ✓ | ✓ | ✓ |
| `update_next_mow()` | Get next scheduled mowing time | ✓ | - | - |
| `update_operating_data()` | Get battery, runtime, temp data | ✓ | ✓ | - |
| `update_predictive_calendar()` | Get smart mow exclusion slots | ✓ | - | - |
| `update_predictive_schedule()` | Get smart mow schedule | ✓ | - | - |
| `update_security()` | Get security settings | ✓ | - | - |
| `update_setup()` | Get setup status | ✓ | - | - |
| `update_state()` | Get current mower state | ✓ | - | - |
| `update_state(force=True)` | Force state refresh (wakes mower) | ✓ | ✓ | - |
| `update_state(longpoll=True, longpoll_timeout=120)` | Long-poll state changes (max 230s) | ✓ | - | - |
| `update_updates_available()` | Check for firmware updates | ✓ | ✓ | - |
| `update_user()` | Get user account info | ✓ | - | - |
| `update_all()` | Update all data above | ✓ | - | - |
| `download_map(filename)` | Download latest lawn map | ✓ | - | - |

#### Return Objects

**State**
```python
indego.state  # Current mower state
# Returns: State(state=64513, mowed=78, xPos=162, yPos=65, ...)
# Use state_description property for human-readable format
```

**Alerts**
```python
indego.alerts  # List of current alerts
# Returns: [Alert(alert_id='...', error_code='...', headline='...', ...)]
```

**Calendar (Regular Schedule)**
```python
indego.calendar  # Regular mowing schedule
# Returns: Calendar(cal=3, days=[CalendarDay(day=0, day_name='monday', slots=[...])])
```

**Generic Data (Mower Info)**
```python
indego.generic_data
# Returns: GenericData(alm_name='Indego', alm_sn='505703041',
#                      alm_firmware_version='00837.01043', model_description='Indego S+ 400', ...)
```

**Operating Data (Battery, Runtime)**
```python
indego.operating_data
# Returns: OperatingData(battery=Battery(percent=85, voltage=35.7, ambient_temp=26, ...),
#                        garden=Garden(...), runtime=Runtime(...))
```

**User Info**
```python
indego.user
# Returns: User(email='...', display_name='...', language='sv', country='SE', ...)
```

Other properties: `location`, `network`, `security`, `setup`, `last_completed_mow`, `next_mow`, `predictive_calendar`, `predictive_schedule`

## Control Commands

### `put_command(command: str)`
Send a control command to the mower.

**Valid commands:**
- `'mow'` - Start mowing
- `'pause'` - Pause mowing
- `'returnToDock'` - Return to charging dock

**Example:**
```python
indego.put_command('mow')  # Start mowing
await indego.put_command('pause')  # Async version
```

### `put_mow_mode(mode: str | bool)`
Set smart mowing mode.

**Valid values:**
- `'true'` or `True` - Enable smart mowing (AI-assisted schedule)
- `'false'` or `False` - Disable smart mowing (use calendar only)

**Example:**
```python
indego.put_mow_mode(True)  # Enable smart mowing
```

### `put_predictive_cal(calendar: dict)`
Set smart mowing exclusion times (time slots where mower should NOT mow).

### `put_alert_read(alert_index: int)`
Mark a specific alert as read (by index in alerts list).

### `put_all_alerts_read()`
Mark all alerts as read.

### `delete_alert(alert_index: int)`
Delete a specific alert (by index in alerts list).

### `delete_all_alerts()`
Delete all alerts.

## Getter Methods

For each update method, there's a corresponding getter that updates AND returns the data:

```python
alerts = await indego.get_alerts()  # Updates + returns alerts
state = await indego.get_state()    # Updates + returns state
calendar = await indego.get_calendar()  # Updates + returns calendar
# ... and so on for all update_* methods
```

## Error Handling

PyIndego uses custom exceptions for better error handling:

```python
from pyIndego import (
    IndegoException,      # Base exception
    IndegoAuthError,      # Auth errors (401, 403)
    IndegoConnectionError, # Network timeouts, connection errors
    IndegoRequestError,   # API errors (4xx, 5xx)
    IndegoNotFoundError,  # 404 errors
)

try:
    indego.update_state()
except IndegoConnectionError as e:
    print(f"Connection failed: {e}")
except IndegoAuthError as e:
    print(f"Invalid token: {e}")
except IndegoException as e:
    print(f"API error: {e}")
```

## Type Hints

PyIndego includes full type hints for better IDE support:

```python
from pyIndego import IndegoClient
from typing import List

client: IndegoClient = IndegoClient(token="...")
alerts: List = client.get_alerts()
state_desc: str = client.state_description
```

## Contributing

Development setup:

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with dev dependencies
pip install -e '.[testing]'

# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=pyIndego
```

## Known Limitations

- **Predictive Setup**: `update_predictive_setup()` / `put_predictive_setup()` are documented in API but not yet fully implemented
- **Some mower models**: `update_config()` doesn't work on all models (e.g., Indego 1000), works better on newer models (e.g., Indego S+)
- **Network info**: Some mowers may not report detailed network information (`update_network()`)

## Supported Mower Models

PyIndego works with all Bosch Indego models including:
- Indego 1000/1100/1200
- Indego 10C/13C
- Indego 350/400
- Indego S+ 350/400 (Gen 1 & 2)
- Indego S+ 500
- Indego M+ 700 (Gen 1 & 2)

## License

MIT License

## Support

For issues with the library or integrations:
- GitHub Issues: https://github.com/sander1988/pyIndego/issues
- Discord: https://discord.gg/aD33GsP
