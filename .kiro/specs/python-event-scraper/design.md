# Design Document

## Overview

The Python Event Scraper is a command-line application that replicates and enhances the functionality of the existing bash shell script. It fetches entertainment events from The Villages API, processes venue names, and outputs formatted event data. The application is designed with modularity, maintainability, and extensibility in mind, using Python's standard library and the requests library for HTTP operations.

The application follows a pipeline architecture: token extraction → session establishment → API request → data processing → formatted output.

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│   CLI Entry     │
│     Point       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Configuration  │
│    Manager      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Token Fetcher  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Session Manager │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  API Client     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Event Processor │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Output Formatter│
└─────────────────┘
```

### Component Responsibilities

1. **CLI Entry Point**: Parses command-line arguments and orchestrates the execution flow
2. **Configuration Manager**: Manages venue abbreviation mappings and application settings
3. **Token Fetcher**: Retrieves and extracts the authentication token from the JavaScript file
4. **Session Manager**: Handles cookie management and session establishment
5. **API Client**: Makes authenticated requests to The Villages API
6. **Event Processor**: Parses JSON responses and extracts event data
7. **Output Formatter**: Formats event data according to the selected output format

## Components and Interfaces

### 1. Main Module (`villages_events.py`)

**Purpose**: Entry point for the application, orchestrates the workflow

**Interface**:
```python
def main() -> int:
    """
    Main entry point for the application.
    Returns exit code (0 for success, non-zero for failure).
    """
    pass
```

**Responsibilities**:
- Parse command-line arguments using argparse
- Initialize configuration
- Coordinate execution of other components
- Handle top-level error handling and logging
- Return appropriate exit codes

### 2. Token Fetcher Module (`token_fetcher.py`)

**Purpose**: Fetches and extracts authentication token from JavaScript file

**Interface**:
```python
def fetch_auth_token(js_url: str, timeout: int = 10) -> str:
    """
    Fetches main.js and extracts the dp_AUTH_TOKEN.
    
    Args:
        js_url: URL to the JavaScript file
        timeout: Request timeout in seconds
        
    Returns:
        Extracted token in format "Basic <base64_string>"
        
    Raises:
        TokenFetchError: If fetching or extraction fails
    """
    pass
```

**Implementation Details**:
- Use requests.get() with timeout
- Use regex pattern to match: `dp_AUTH_TOKEN\s*=\s*["']Basic\s+[a-zA-Z0-9+/=]+["']`
- Extract and reconstruct as "Basic <base64_token>"
- Raise custom exception on failure

### 3. Session Manager Module (`session_manager.py`)

**Purpose**: Manages HTTP sessions and cookies

**Interface**:
```python
class SessionManager:
    """Manages HTTP session and cookies for API requests."""
    
    def __init__(self):
        """Initialize session with requests.Session()."""
        pass
    
    def establish_session(self, calendar_url: str, timeout: int = 10) -> None:
        """
        Visit calendar page to establish session and capture cookies.
        
        Args:
            calendar_url: URL to the calendar page
            timeout: Request timeout in seconds
            
        Raises:
            SessionError: If session establishment fails
        """
        pass
    
    def get_session(self) -> requests.Session:
        """Returns the active session object."""
        pass
    
    def close(self) -> None:
        """Closes the session and cleans up resources."""
        pass
```

**Implementation Details**:
- Use requests.Session() for automatic cookie handling
- Set appropriate headers (User-Agent, Accept, Origin, Referer)
- Implement context manager protocol for cleanup

### 4. API Client Module (`api_client.py`)

**Purpose**: Makes authenticated requests to The Villages API

**Interface**:
```python
def fetch_events(
    session: requests.Session,
    api_url: str,
    auth_token: str,
    timeout: int = 10
) -> dict:
    """
    Fetches events from The Villages API.
    
    Args:
        session: Active requests session with cookies
        api_url: Full API endpoint URL with query parameters
        auth_token: Authorization token
        timeout: Request timeout in seconds
        
    Returns:
        Parsed JSON response as dictionary
        
    Raises:
        APIError: If request fails or response is invalid
    """
    pass
```

**Implementation Details**:
- Use session.get() with auth_token in Authorization header
- Include all required headers
- Validate response status code
- Parse and validate JSON response
- Raise custom exception on failure

### 5. Event Processor Module (`event_processor.py`)

**Purpose**: Processes event data, extracts configurable fields, and applies venue abbreviations

**Interface**:
```python
class EventProcessor:
    """Processes event data and applies venue abbreviations."""
    
    def __init__(self, venue_mappings: dict[str, str], output_fields: list[str] = None):
        """
        Initialize with venue abbreviation mappings and output fields.
        
        Args:
            venue_mappings: Dictionary mapping keywords to abbreviations
            output_fields: List of field paths to extract (e.g., ["title", "location.title", "start.date"])
                          Defaults to ["location.title", "title"] for backward compatibility
        """
        pass
    
    def abbreviate_venue(self, venue: str) -> str:
        """
        Abbreviates venue name based on keyword matching.
        
        Args:
            venue: Full venue name
            
        Returns:
            Abbreviated venue name or original if no match
        """
        pass
    
    def extract_field(self, event: dict, field_path: str) -> Any:
        """
        Extracts a field value from an event using dot notation.
        
        Args:
            event: Event dictionary from API response
            field_path: Dot-separated path to field (e.g., "location.title", "start.date")
            
        Returns:
            Field value or empty string if not found
        """
        pass
    
    def process_events(self, api_response: dict) -> list[dict[str, Any]]:
        """
        Extracts and processes events from API response.
        
        Args:
            api_response: Parsed JSON response from API
            
        Returns:
            List of dictionaries with extracted fields
        """
        pass
```

**Implementation Details**:
- Iterate through venue_mappings to find keyword matches
- Use substring matching (keyword in venue)
- Extract events array from response
- For each event, extract all specified fields using dot notation
- Apply venue abbreviation to "location.title" field if present
- Handle missing fields gracefully with logging, return empty string
- Return list of processed events as dictionaries

### 6. Output Formatter Module (`output_formatter.py`)

**Purpose**: Formats event data according to selected output format

**Interface**:
```python
class OutputFormatter:
    """Formats event data for output."""
    
    @staticmethod
    def format_meshtastic(events: list[dict[str, Any]], field_names: list[str]) -> str:
        """
        Formats events in meshtastic format using first two fields.
        Format: field1_value,field2_value#field1_value,field2_value#
        """
        pass
    
    @staticmethod
    def format_json(events: list[dict[str, Any]]) -> str:
        """
        Formats events as JSON array with all specified fields.
        Format: [{"field1": "...", "field2": "..."}, ...]
        """
        pass
    
    @staticmethod
    def format_csv(events: list[dict[str, Any]], field_names: list[str]) -> str:
        """
        Formats events as CSV with headers for all fields.
        Format: field1,field2\nValue1,Value2\n...
        """
        pass
    
    @staticmethod
    def format_plain(events: list[dict[str, Any]], field_names: list[str]) -> str:
        """
        Formats events as plain text with all fields.
        Format: field1: value1, field2: value2\n...
        """
        pass
    
    @staticmethod
    def format_events(
        events: list[dict[str, Any]],
        format_type: str = "meshtastic",
        field_names: list[str] = None
    ) -> str:
        """
        Formats events according to specified format type.
        
        Args:
            events: List of event dictionaries with extracted fields
            format_type: One of "meshtastic", "json", "csv", "plain"
            field_names: List of field names for ordering (used for CSV headers and plain text)
            
        Returns:
            Formatted string ready for output
        """
        pass
```

**Implementation Details**:
- Meshtastic format: Use first two fields from field_names, join with "#" delimiter, append final "#"
- JSON format: Use json.dumps() with all fields from event dictionaries
- CSV format: Use csv module with field_names as headers, output all fields
- Plain format: Format each event with all fields as "field1: value1, field2: value2"
- Handle empty events list appropriately for each format
- Handle missing field values (empty strings or nulls)

### 7. Configuration Module (`config.py`)

**Purpose**: Manages application configuration and constants

**Interface**:
```python
class Config:
    """Application configuration and constants."""
    
    # URLs
    JS_URL: str = "https://cdn.thevillages.com/web_components/myvillages-auth-forms/main.js"
    CALENDAR_URL: str = "https://www.thevillages.com/calendar/#/?dateRange=today&categories=entertainment&locationCategories=town-squares"
    API_URL: str = "https://api.v2.thevillages.com/events/?cancelled=false&startRow=0&endRow=24&dateRange=today&categories=entertainment&locationCategories=town-squares&subcategoriesQueryType=and"
    
    # Default venue mappings
    DEFAULT_VENUE_MAPPINGS: dict[str, str] = {
        "Brownwood": "Brownwood",
        "Sawgrass": "Sawgrass",
        "Spanish Springs": "Spanish Springs",
        "Lake Sumter": "Lake Sumter"
    }
    
    # HTTP settings
    DEFAULT_TIMEOUT: int = 10
    USER_AGENT: str = "Mozilla/5.0"
    
    # Output formats
    VALID_FORMATS: list[str] = ["meshtastic", "json", "csv", "plain"]
    DEFAULT_FORMAT: str = "meshtastic"
    
    # Output fields
    DEFAULT_OUTPUT_FIELDS: list[str] = ["location.title", "title"]
    AVAILABLE_FIELDS: list[str] = [
        "title", "description", "excerpt", "category", "subcategories",
        "start.date", "end.date", "allDay", "cancelled", "featured",
        "location.title", "location.category", "location.id",
        "address.streetAddress", "address.locality", "address.region",
        "address.postalCode", "address.country",
        "image", "url", "otherInfo", "id"
    ]
```

### 8. Custom Exceptions Module (`exceptions.py`)

**Purpose**: Defines custom exception classes for better error handling

**Interface**:
```python
class VillagesEventError(Exception):
    """Base exception for Villages Event Scraper."""
    pass

class TokenFetchError(VillagesEventError):
    """Raised when token fetching or extraction fails."""
    pass

class SessionError(VillagesEventError):
    """Raised when session establishment fails."""
    pass

class APIError(VillagesEventError):
    """Raised when API request fails."""
    pass

class ProcessingError(VillagesEventError):
    """Raised when event processing fails."""
    pass
```

## Data Models

### Event Data Structure

Events are represented as dictionaries during processing:
```python
Event = dict[str, Any]  # Dictionary with configurable fields
# Example: {"location.title": "Brownwood", "title": "Artist Name", "start.date": "2025-11-14T22:00:00.000Z"}
```

### API Response Structure

Expected JSON structure from The Villages API:
```json
{
  "events": [
    {
      "location": {
        "title": "Brownwood Paddock Square"
      },
      "title": "Artist Name"
    }
  ]
}
```

### Configuration Data

Venue mappings stored as dictionary:
```python
venue_mappings: dict[str, str] = {
    "keyword": "abbreviation"
}
```

Output fields configuration:
```python
output_fields: list[str] = ["location.title", "title", "start.date"]
```

## Error Handling

### Error Handling Strategy

1. **Network Errors**: Catch requests exceptions, log descriptive messages, exit with code 1
2. **Parsing Errors**: Catch JSON decode errors, log response snippet, exit with code 1
3. **Missing Data**: Log warnings for individual events, continue processing others
4. **Token Extraction Failure**: Log error with pattern details, exit with code 1
5. **Invalid Arguments**: Use argparse to validate, show usage message, exit with code 2

### Logging Strategy

- Use Python's logging module
- Log to stderr for errors and warnings
- Log levels:
  - ERROR: Fatal errors that cause termination
  - WARNING: Non-fatal issues (missing event fields, etc.)
  - INFO: Informational messages (optional, for verbose mode)
- Format: `[LEVEL] message`

### Exit Codes

- 0: Success
- 1: Runtime error (network, parsing, API)
- 2: Invalid arguments or configuration

## Testing Strategy

### Unit Tests

Test each module independently:

1. **Token Fetcher Tests**:
   - Test successful token extraction with mock response
   - Test failure when token pattern not found
   - Test network error handling

2. **Event Processor Tests**:
   - Test venue abbreviation with various inputs
   - Test event extraction from valid JSON
   - Test handling of missing fields

3. **Output Formatter Tests**:
   - Test each output format with sample data
   - Test empty events list handling
   - Test special characters in venue/title

4. **Session Manager Tests**:
   - Test session establishment
   - Test cookie handling
   - Test cleanup

### Integration Tests

Test the complete workflow:

1. **End-to-End Test** (with mocked HTTP):
   - Mock all HTTP requests
   - Verify complete pipeline execution
   - Verify output format

2. **Error Path Tests**:
   - Test behavior with network failures
   - Test behavior with invalid JSON
   - Test behavior with missing API fields

### Manual Testing

1. Run against live API to verify functionality
2. Compare output with original shell script
3. Test all output formats
4. Test command-line argument parsing

## Project Structure

```
.
├── README.md                    # Comprehensive documentation
├── requirements.txt             # Python dependencies
├── villages_square_events.sh    # Original shell script (kept for reference)
├── villages_events.py           # Main entry point
└── src/
    ├── __init__.py
    ├── config.py                # Configuration and constants
    ├── exceptions.py            # Custom exceptions
    ├── token_fetcher.py         # Token extraction logic
    ├── session_manager.py       # Session and cookie management
    ├── api_client.py            # API request handling
    ├── event_processor.py       # Event processing and venue abbreviation
    └── output_formatter.py      # Output formatting logic
```

## Dependencies

- **requests**: HTTP library for making API requests and managing sessions
- **Python 3.8+**: Required for type hints and modern Python features

## Security Considerations

1. **Token Handling**: Token is extracted from public JavaScript file, no sensitive credentials stored
2. **HTTPS**: All requests use HTTPS for encrypted communication
3. **Input Validation**: Validate all user inputs (command-line arguments)
4. **No Credential Storage**: No persistent storage of authentication data
5. **Timeout Settings**: All HTTP requests have timeouts to prevent hanging

## Performance Considerations

1. **Session Reuse**: Use requests.Session() to reuse TCP connections
2. **Minimal Dependencies**: Keep dependency list small for fast installation
3. **Efficient Parsing**: Use built-in json module for fast parsing
4. **Single API Call**: Fetch all events in one request (matching shell script behavior)

## Future Enhancements

Potential improvements not included in initial implementation:

1. Configuration file support for custom venue mappings
2. Date range selection via command-line arguments
3. Filtering by event categories
4. Caching of authentication token
5. Retry logic for transient network failures
6. Verbose/debug logging mode
7. Output to file instead of stdout
