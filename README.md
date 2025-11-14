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

## Usage

### Basic Usage

Run the script with default settings (legacy format output):
```bash
python villages_events.py
```

### Output Format Options

The application supports multiple output formats via the `--format` option:

#### Legacy Format (Default)
Compatible with the original shell script format:
```bash
python villages_events.py --format legacy
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

### Redirecting Output

Save output to a file:
```bash
python villages_events.py --format json > events.json
python villages_events.py --format csv > events.csv
```

### Integration with Shell Scripts

Use in shell scripts or pipelines:
```bash
#!/bin/bash
events=$(python villages_events.py --format legacy)
echo "Today's events: $events"
```

## Configuration

### Venue Abbreviations

The application automatically abbreviates venue names based on keyword matching. Default mappings are defined in `src/config.py`:

```python
DEFAULT_VENUE_MAPPINGS = {
    "Brownwood": "Brownwood",
    "Sawgrass": "Sawgrass",
    "Spanish Springs": "Spanish Springs",
    "Lake Sumter": "Lake Sumter"
}
```

To customize venue abbreviations, modify the `DEFAULT_VENUE_MAPPINGS` dictionary in `src/config.py`. The system uses substring matching - if a venue name contains any of the keywords, it will be replaced with the corresponding abbreviation.

Example customization:
```python
DEFAULT_VENUE_MAPPINGS = {
    "Brownwood": "BW",
    "Sawgrass": "SG",
    "Spanish Springs": "SS",
    "Lake Sumter": "LS"
}
```

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

**Symptom**: Empty output or format-appropriate empty data (single "#" for legacy, "[]" for JSON)

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

