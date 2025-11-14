# API Documentation

## Module Overview

The Villages Event Scraper is organized into several modules, each with a specific responsibility.

## Core Modules

### `token_fetcher`

Fetches authentication tokens from JavaScript files.

```python
from src.token_fetcher import fetch_auth_token

token = fetch_auth_token(js_url, timeout=10)
```

**Functions:**
- `fetch_auth_token(js_url: str, timeout: int = 10) -> str`
  - Fetches and extracts the authentication token
  - Raises: `TokenFetchError` on failure

### `session_manager`

Manages HTTP sessions and cookies.

```python
from src.session_manager import SessionManager

with SessionManager() as manager:
    manager.establish_session(calendar_url)
    session = manager.get_session()
```

**Class: SessionManager**
- `__init__()` - Initialize session
- `establish_session(calendar_url: str, timeout: int = 10)` - Visit calendar page
- `get_session() -> requests.Session` - Get active session
- `close()` - Close session and cleanup

### `api_client`

Handles authenticated API requests.

```python
from src.api_client import fetch_events

data = fetch_events(session, api_url, auth_token, timeout=10)
```

**Functions:**
- `fetch_events(session, api_url, auth_token, timeout=10) -> Dict[str, Any]`
  - Fetches events from API
  - Raises: `APIError` on failure

### `event_processor`

Processes and transforms event data.

```python
from src.event_processor import EventProcessor

processor = EventProcessor(venue_mappings)
events = processor.process_events(api_response)
```

**Class: EventProcessor**
- `__init__(venue_mappings: Dict[str, str])` - Initialize with venue mappings
- `abbreviate_venue(venue: str) -> str` - Abbreviate venue name
- `process_events(api_response: Dict[str, Any]) -> List[Tuple[str, str]]` - Process events

### `output_formatter`

Formats event data for output.

```python
from src.output_formatter import OutputFormatter

output = OutputFormatter.format_events(events, format_type="json")
```

**Class: OutputFormatter**
- `format_meshtastic(events) -> str` - Meshtastic format
- `format_json(events) -> str` - JSON format
- `format_csv(events) -> str` - CSV format
- `format_plain(events) -> str` - Plain text format
- `format_events(events, format_type) -> str` - Dispatcher method

## Configuration

### `config`

Contains all configuration constants.

```python
from src.config import Config

js_url = Config.JS_URL
timeout = Config.DEFAULT_TIMEOUT
```

**Constants:**
- `JS_URL` - JavaScript file URL
- `DEFAULT_VENUE_MAPPINGS` - Venue abbreviation mappings
- `DEFAULT_TIMEOUT` - HTTP timeout in seconds
- `USER_AGENT` - User agent string
- `VALID_FORMATS` - List of valid output formats
- `DEFAULT_FORMAT` - Default output format
- `VALID_DATE_RANGES` - List of valid date range options
- `DEFAULT_DATE_RANGE` - Default date range (today)
- `VALID_CATEGORIES` - List of valid event categories
- `DEFAULT_CATEGORY` - Default category (entertainment)
- `VALID_LOCATIONS` - List of valid location options
- `DEFAULT_LOCATION` - Default location (town-squares)

**Methods:**
- `get_calendar_url(date_range='today', category='entertainment', location='town-squares') -> str` - Generate calendar URL with filters
- `get_api_url(date_range='today', category='entertainment', location='town-squares') -> str` - Generate API URL with filters

### `config_loader`

Handles loading configuration from YAML files.

```python
from src.config_loader import ConfigLoader

config = ConfigLoader.load_config('config.yaml')
value = ConfigLoader.get_default(config, 'format', 'meshtastic')
```

**Methods:**
- `load_config(config_file='config.yaml') -> Dict[str, Any]` - Load configuration from YAML file
- `get_default(config, key, fallback) -> Any` - Get configuration value with fallback

## Configuration File

The application supports a `config.yaml` file for setting defaults:

```yaml
format: json
date_range: this-week
category: sports
location: Brownwood+Paddock+Square
venue_mappings:
  Brownwood: BW
  Sawgrass: SG
timeout: 15
```

**Behavior:**
- Config file values become new defaults
- Command-line arguments override config file
- Missing config file uses hardcoded defaults
- Invalid YAML is ignored with warning

## Exceptions

### `exceptions`

Custom exception hierarchy.

```python
from src.exceptions import VillagesEventError, TokenFetchError

try:
    # code
except TokenFetchError as e:
    print(f"Token fetch failed: {e}")
```

**Exception Classes:**
- `VillagesEventError` - Base exception
- `TokenFetchError` - Token fetching errors
- `SessionError` - Session management errors
- `APIError` - API request errors
- `ProcessingError` - Event processing errors

## Command Line Interface

```bash
# Default (today's entertainment events at town squares in Meshtastic format)
python3 villages_events.py

# Specify date range
python3 villages_events.py --date-range tomorrow
python3 villages_events.py --date-range this-week
python3 villages_events.py --date-range next-month
python3 villages_events.py --date-range all

# Specify category
python3 villages_events.py --category sports
python3 villages_events.py --category arts-and-crafts
python3 villages_events.py --category all

# Specify location
python3 villages_events.py --location Brownwood+Paddock+Square
python3 villages_events.py --location Spanish+Springs+Town+Square
python3 villages_events.py --location all

# Specify output format
python3 villages_events.py --format json
python3 villages_events.py --format csv
python3 villages_events.py --format plain

# Raw output for debugging
python3 villages_events.py --raw
python3 villages_events.py --raw --date-range tomorrow --category sports

# Combine options
python3 villages_events.py --date-range next-week --category sports --location Brownwood+Paddock+Square --format json
python3 villages_events.py --category recreation --location all --format csv
```

**Options:**
- `--format {meshtastic,json,csv,plain}` - Output format (default: meshtastic)
- `--date-range {today,tomorrow,this-week,next-week,this-month,next-month,all}` - Date range (default: today)
- `--category {entertainment,arts-and-crafts,health-and-wellness,recreation,social-clubs,special-events,sports,all}` - Event category (default: entertainment)
- `--location {town-squares,...,all}` - Event location (default: town-squares, 15 options total)
- `--config CONFIG` - Path to configuration file (default: config.yaml)
- `--raw` - Output raw API response without processing (for debugging)

**Exit Codes:**
- `0` - Success
- `1` - Runtime error
- `2` - Invalid arguments
