# The Villages Event Scraper

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python application that fetches entertainment events from The Villages API and outputs formatted event data. This tool replaces the original bash shell script (`villages_square_events.sh`) with a more maintainable, well-structured Python implementation that offers better error handling, multiple output formats, and comprehensive documentation.

## Overview

The Villages Event Scraper retrieves today's entertainment events at The Villages town squares by:
1. Extracting an authentication token from The Villages JavaScript files
2. Establishing an HTTP session with proper cookies
3. Making authenticated API requests to fetch event data
4. Processing venue names with configurable abbreviations
5. Outputting formatted event information in multiple formats

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes:
- `requests` - HTTP library for API requests and session management
- `pyyaml` - YAML parser for configuration file support

3. (Optional) Create a configuration file:
```bash
cp config.yaml.example config.yaml
# Edit config.yaml to set your preferred defaults
```

## Usage

### Basic Usage

Run the script with default settings (today's events in Meshtastic format):
```bash
python villages_events.py
```

### Command-Line Options

The application supports two main options:

#### Date Range Option

Specify which events to fetch using the `--date-range` option:

```bash
python villages_events.py --date-range today        # Today's events (default)
python villages_events.py --date-range tomorrow     # Tomorrow's events
python villages_events.py --date-range this-week    # This week's events
python villages_events.py --date-range next-week    # Next week's events
python villages_events.py --date-range this-month   # This month's events
python villages_events.py --date-range next-month   # Next month's events
python villages_events.py --date-range all          # All events (no date filter)
```

#### Category Option

Filter events by category using the `--category` option:

```bash
python villages_events.py --category entertainment      # Entertainment events (default)
python villages_events.py --category arts-and-crafts    # Arts and crafts events
python villages_events.py --category health-and-wellness # Health and wellness events
python villages_events.py --category recreation         # Recreation events
python villages_events.py --category social-clubs       # Social club events
python villages_events.py --category special-events     # Special events
python villages_events.py --category sports             # Sports events
python villages_events.py --category all                # All categories (no filter)
```

#### Location Option

Filter events by location using the `--location` option:

```bash
python villages_events.py --location town-squares                           # Town squares (default)
python villages_events.py --location Brownwood+Paddock+Square               # Brownwood Paddock Square
python villages_events.py --location Spanish+Springs+Town+Square            # Spanish Springs Town Square
python villages_events.py --location Lake+Sumter+Landing+Market+Square      # Lake Sumter Landing
python villages_events.py --location Sawgrass+Grove                         # Sawgrass Grove
python villages_events.py --location The+Sharon                             # The Sharon
python villages_events.py --location sports-recreation                      # Sports & recreation venues
python villages_events.py --location all                                    # All locations (no filter)
```

See `--help` for the complete list of 15 location options.

#### Output Format Options

The application supports multiple output formats via the `--format` option:

#### Meshtastic Format (Default)
Compact format optimized for Meshtastic messaging:
```bash
python villages_events.py --format meshtastic
```

Output example:
```
Brownwood,John Doe#Spanish Springs,Jane Smith#Sawgrass,The Band#
```

Format: `venue1,title1#venue2,title2#` (hash-delimited with trailing #)

#### JSON Format
Structured JSON array output:
```bash
python villages_events.py --format json
```

Output example:
```json
[
  {"venue": "Brownwood", "title": "John Doe"},
  {"venue": "Spanish Springs", "title": "Jane Smith"},
  {"venue": "Sawgrass", "title": "The Band"}
]
```

#### CSV Format
Comma-separated values with headers:
```bash
python villages_events.py --format csv
```

Output example:
```
venue,title
Brownwood,John Doe
Spanish Springs,Jane Smith
Sawgrass,The Band
```

#### Plain Text Format
Human-readable format, one event per line:
```bash
python villages_events.py --format plain
```

Output example:
```
Brownwood: John Doe
Spanish Springs: Jane Smith
Sawgrass: The Band
```

### Configurable Output Fields

The application allows you to customize which fields from the API response are included in the output. This gives you control over the information displayed, from basic venue and title to detailed event information including dates, descriptions, addresses, and more.

#### Using the --fields Option

Specify custom fields using the `--fields` command-line argument with a comma-separated list:

```bash
python villages_events.py --fields location.title,title,start.date
```

#### Available Fields

The following fields can be included in your output using dot notation for nested fields:

| Field Path | Description | Example Value |
|------------|-------------|---------------|
| `title` | Event title | "John Doe Band" |
| `description` | Full event description | "Join us for an evening of..." |
| `excerpt` | Short event description | "Live music performance" |
| `category` | Event category | "entertainment" |
| `subcategories` | List of subcategories | ["live-music", "outdoor"] |
| `start.date` | Event start date/time | "2025-11-14T22:00:00.000Z" |
| `end.date` | Event end date/time | "2025-11-15T01:00:00.000Z" |
| `allDay` | Whether event is all day | false |
| `cancelled` | Whether event is cancelled | false |
| `featured` | Whether event is featured | true |
| `location.title` | Venue name (abbreviated) | "Brownwood Paddock Square" |
| `location.category` | Venue category | "town-squares" |
| `location.id` | Venue ID | "brownwood-paddock-square" |
| `address.streetAddress` | Street address | "1101 Canal Street" |
| `address.locality` | City/locality | "The Villages" |
| `address.region` | State/region | "FL" |
| `address.postalCode` | Postal code | "32162" |
| `address.country` | Country | "US" |
| `image` | Event image URL | "https://..." |
| `url` | Event URL | "https://..." |
| `otherInfo` | Additional information | "Free admission" |
| `id` | Event ID | "event-12345" |

**Note:** The `location.title` field is the only field that applies venue abbreviation rules based on your `venue_mappings` configuration.

#### Field Configuration Examples

**Example 1: Basic event listing with start time**
```bash
python villages_events.py --fields location.title,title,start.date --format json
```

Output:
```json
[
  {
    "location.title": "Brownwood",
    "title": "John Doe Band",
    "start.date": "2025-11-14T22:00:00.000Z"
  }
]
```

**Example 2: Detailed event information**
```bash
python villages_events.py --fields title,location.title,start.date,description,url --format plain
```

Output:
```
title: John Doe Band, location.title: Brownwood, start.date: 2025-11-14T22:00:00.000Z, description: Join us for an evening of live music, url: https://...
```

**Example 3: Event with full address**
```bash
python villages_events.py --fields location.title,title,address.streetAddress,address.locality,address.region --format csv
```

Output:
```
location.title,title,address.streetAddress,address.locality,address.region
Brownwood,John Doe Band,1101 Canal Street,The Villages,FL
```

**Example 4: Meshtastic format with custom fields**
```bash
python villages_events.py --fields title,start.date --format meshtastic
```

Output:
```
John Doe Band,2025-11-14T22:00:00.000Z#Jane Smith,2025-11-14T23:00:00.000Z#
```

**Note:** In Meshtastic format, only the first two fields are used to maintain the compact `field1,field2#` format.

**Example 5: Event category and featured status**
```bash
python villages_events.py --fields location.title,title,category,featured --format json
```

Output:
```json
[
  {
    "location.title": "Spanish Springs",
    "title": "The Band",
    "category": "entertainment",
    "featured": true
  }
]
```

#### Configuration File Support

You can set default output fields in your `config.yaml` file to avoid specifying them on every command:

```yaml
output_fields:
  - location.title
  - title
  - start.date
  - category
```

Then simply run:
```bash
python villages_events.py --format json
```

Command-line `--fields` argument will override the configuration file setting.

#### Use Cases

**For Meshtastic messaging (compact format):**
```bash
# Default: venue and title
python villages_events.py --format meshtastic

# With start time
python villages_events.py --fields location.title,start.date --format meshtastic
```

**For event calendars:**
```bash
python villages_events.py --fields title,location.title,start.date,end.date,description --format json
```

**For location-based apps:**
```bash
python villages_events.py --fields title,location.title,address.streetAddress,address.locality,url --format csv
```

**For event discovery:**
```bash
python villages_events.py --fields title,excerpt,category,location.title,image,url --format json
```

**For simple listings:**
```bash
python villages_events.py --fields location.title,title --format plain
```

#### Backward Compatibility

When no `--fields` argument is provided and no `output_fields` is set in the configuration file, the application defaults to `location.title,title` to maintain backward compatibility with the original implementation.

### Redirecting Output

Save output to a file:
```bash
python villages_events.py --format json > events.json
python villages_events.py --format csv > events.csv
```

### Raw Output (Debugging)

For debugging or exploring the API response structure, use the `--raw` flag to output the unprocessed API response:

```bash
python villages_events.py --raw
```

This outputs the complete JSON response from the API, including all fields and metadata. Useful for:
- Exploring available data fields
- Debugging API responses
- Planning future features

**Note:** When `--raw` is used, the `--format` option is ignored.

### Combining Options

You can combine date range, category, location, format, and fields options:
```bash
# Get next week's entertainment events in JSON format
python villages_events.py --date-range next-week --format json

# Get tomorrow's sports events at Brownwood in CSV format with custom fields
python villages_events.py --date-range tomorrow --category sports --location Brownwood+Paddock+Square --format csv --fields location.title,title,start.date

# Get all recreation events (any date, any location) in plain text format
python villages_events.py --date-range all --category recreation --location all --format plain

# Get today's arts and crafts events at Sawgrass Grove with detailed information
python villages_events.py --category arts-and-crafts --location Sawgrass+Grove --fields title,location.title,description,url --format json

# Get this week's events from all categories at Spanish Springs with times
python villages_events.py --date-range this-week --category all --location Spanish+Springs+Town+Square --fields location.title,title,start.date,end.date --format csv
```

### Integration with Shell Scripts

Use in shell scripts or pipelines:
```bash
#!/bin/bash
# Get today's events
events=$(python villages_events.py --format meshtastic)
echo "Today's events: $events"

# Get this week's events in JSON
python villages_events.py --date-range this-week --format json > this_week.json
```

## Configuration

### Configuration File

The application supports a YAML configuration file (`config.yaml`) to set default values for all parameters. This eliminates the need to specify command-line arguments for your common use cases.

**Create a configuration file:**
```bash
cp config.yaml.example config.yaml
```

**Example configuration:**
```yaml
# Set your preferred defaults
format: json
date_range: this-week
category: sports
location: Brownwood+Paddock+Square

# Customize which fields to include in output
output_fields:
  - location.title
  - title
  - start.date
  - category

# Customize venue abbreviations
venue_mappings:
  Brownwood: BW
  Sawgrass: SG
  Spanish Springs: SS
  Lake Sumter: LS

# Adjust HTTP timeout
timeout: 15
```

**Using the configuration:**
- If `config.yaml` exists, its values become the new defaults
- Command-line arguments override config file settings
- If no config file exists, hardcoded defaults are used

**Example:**
```bash
# With config.yaml setting format: json and category: sports
python villages_events.py                    # Uses JSON format and sports category
python villages_events.py --format csv       # Overrides to CSV, still uses sports category
python villages_events.py --category all     # Uses JSON format, overrides to all categories
```

### Output Fields Configuration

Customize which fields from the API response are included in your output by setting `output_fields` in `config.yaml`:

```yaml
output_fields:
  - location.title
  - title
  - start.date
  - description
  - url
```

**Available fields:** See the complete list in the [Configurable Output Fields](#configurable-output-fields) section above.

**Field notation:** Use dot notation for nested fields (e.g., `location.title`, `start.date`, `address.locality`).

**Default behavior:** If not specified, defaults to `["location.title", "title"]` for backward compatibility.

**Override:** Command-line `--fields` argument takes precedence over config file settings.

### Venue Abbreviations

Venue name abbreviations can be customized in the `config.yaml` file:

```yaml
venue_mappings:
  Brownwood: BW
  Sawgrass: SG
  Spanish Springs: SS
  Lake Sumter: LS
```

The system uses substring matching - if a venue name contains any of the keywords, it will be replaced with the corresponding abbreviation. Abbreviation is only applied to the `location.title` field.

## How It Works

The application follows a pipeline architecture:

1. **Token Extraction** (`src/token_fetcher.py`)
   - Fetches the main.js file from The Villages CDN
   - Extracts the `dp_AUTH_TOKEN` using regex pattern matching
   - Reconstructs the token in "Basic <base64>" format

2. **Session Establishment** (`src/session_manager.py`)
   - Visits the calendar page to establish an HTTP session
   - Captures cookies required for API authentication
   - Manages session lifecycle and cleanup

3. **API Request** (`src/api_client.py`)
   - Makes authenticated GET request to The Villages events API
   - Includes proper headers (Authorization, User-Agent, etc.)
   - Validates response and parses JSON data

4. **Event Processing** (`src/event_processor.py`)
   - Extracts event array from API response
   - Applies venue abbreviation rules
   - Handles missing fields gracefully

5. **Output Formatting** (`src/output_formatter.py`)
   - Formats processed events according to selected format
   - Handles empty results appropriately for each format


## Project Structure

```
.
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── villages_square_events.sh    # Original shell script (reference)
├── villages_events.py           # Main entry point
└── src/
    ├── __init__.py
    ├── config.py                # Configuration and constants
    ├── exceptions.py            # Custom exception classes
    ├── token_fetcher.py         # Token extraction logic
    ├── session_manager.py       # Session and cookie management
    ├── api_client.py            # API request handling
    ├── event_processor.py       # Event processing and venue abbreviation
    └── output_formatter.py      # Output formatting logic
```

## Exit Codes

- `0` - Success
- `1` - Runtime error (network failure, API error, parsing error)
- `2` - Invalid command-line arguments

## Troubleshooting

### No Events Found

**Symptom**: Empty output or format-appropriate empty data (single "#" for Meshtastic, "[]" for JSON)

**Possible Causes**:
- No events scheduled for today at town squares
- API returned empty events array

**Solution**: This is normal behavior when no events are scheduled. Try again on a different day.

### Token Fetch Error

**Symptom**: Error message "Failed to fetch authentication token"

**Possible Causes**:
- Network connectivity issues
- The Villages CDN is unavailable
- JavaScript file structure changed

**Solutions**:
1. Check your internet connection
2. Verify you can access https://cdn.thevillages.com in a browser
3. If the issue persists, the JavaScript file structure may have changed - check `src/token_fetcher.py` regex pattern

### Session Establishment Failed

**Symptom**: Warning about session/cookie handling

**Possible Causes**:
- Network issues
- Calendar page unavailable

**Solutions**:
1. Check network connectivity
2. The application will attempt to proceed anyway - if API request succeeds, no action needed
3. If API request also fails, verify https://www.thevillages.com/calendar/ is accessible

### API Request Failed

**Symptom**: Error message "API request failed" with HTTP status code

**Possible Causes**:
- Invalid authentication token
- API endpoint changed
- Network issues
- Rate limiting

**Solutions**:
1. Check network connectivity
2. Verify the API URL in `src/config.py` is correct
3. If you're running the script frequently, wait a few minutes (possible rate limiting)
4. Check if The Villages API structure has changed

### JSON Parsing Error

**Symptom**: Error message about invalid JSON or missing fields

**Possible Causes**:
- API response structure changed
- Corrupted response data

**Solutions**:
1. Check if The Villages API response structure has changed
2. Review `src/event_processor.py` to ensure field extraction matches current API structure
3. Run with verbose logging (if implemented) to see raw API response

### Import Errors

**Symptom**: `ModuleNotFoundError` or `ImportError`

**Possible Causes**:
- Dependencies not installed
- Wrong Python version

**Solutions**:
1. Ensure you've run `pip install -r requirements.txt`
2. Verify Python version: `python --version` (should be 3.8+)
3. Try using `python3` instead of `python` if you have multiple Python versions

### Permission Errors

**Symptom**: Permission denied when running the script

**Solutions**:
1. Ensure the script has execute permissions: `chmod +x villages_events.py`
2. Or run with: `python villages_events.py`

## Development

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/villages-event-scraper.git
cd villages-event-scraper
```

2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install development dependencies:
```bash
make install-dev
```

### Running Tests

Run all tests:
```bash
make test
```

Run tests with coverage:
```bash
make test-cov
```

Run specific test file:
```bash
python3 -m unittest tests.test_token_fetcher -v
```

### Code Quality

Format code with Black:
```bash
make format
```

Run linters:
```bash
make lint
```

### Documentation

- [API Documentation](docs/API.md) - Detailed module and function documentation
- [Architecture](docs/ARCHITECTURE.md) - System design and architecture overview
- [Testing Guide](docs/TESTING.md) - Comprehensive testing documentation
- [Contributing Guide](CONTRIBUTING.md) - Guidelines for contributors

### Adding New Output Formats

To add a new output format:

1. Add a new static method to `OutputFormatter` class in `src/output_formatter.py`
2. Update the `format_events()` dispatcher method
3. Add the format name to `VALID_FORMATS` in `src/config.py`
4. Update this README with usage examples

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

Key guidelines:
- Code follows existing style and structure
- New features include appropriate error handling
- Documentation is updated accordingly
- Tests are added for new functionality
- All tests pass and linters are happy

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the [documentation](docs/) for detailed information
3. Review the source code comments for implementation details
4. Verify your Python version and dependencies are correct
5. Open an issue on GitHub with details about your problem

## Acknowledgments

- Original shell script implementation that inspired this project
- The Villages for providing the public API
- Contributors and users of this tool

