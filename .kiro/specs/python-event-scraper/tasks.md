# Implementation Plan

- [x] 1. Set up project structure and dependencies
  - Create src/ directory with __init__.py
  - Create requirements.txt with requests library
  - Create main entry point villages_events.py
  - _Requirements: 7.1, 7.2, 7.4_

- [x] 2. Implement configuration and exception modules
  - Create src/config.py with Config class containing all URLs, default venue mappings, HTTP settings, and valid output formats
  - Create src/exceptions.py with custom exception classes: VillagesEventError, TokenFetchError, SessionError, APIError, ProcessingError
  - _Requirements: 7.5, 8.1, 8.3_

- [x] 3. Implement token fetcher module
  - Create src/token_fetcher.py with fetch_auth_token() function
  - Implement HTTP request to fetch main.js using requests library with timeout
  - Implement regex pattern matching to extract dp_AUTH_TOKEN value
  - Reconstruct token in "Basic <base64>" format
  - Raise TokenFetchError with descriptive message on failure
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 4. Implement session manager module
  - Create src/session_manager.py with SessionManager class
  - Implement __init__() to create requests.Session instance
  - Implement establish_session() to visit calendar URL and capture cookies
  - Set appropriate HTTP headers (User-Agent, Accept, Origin, Referer)
  - Implement get_session() to return active session
  - Implement close() method and context manager protocol for cleanup
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 5. Implement API client module
  - Create src/api_client.py with fetch_events() function
  - Implement authenticated GET request using session with Authorization header
  - Include all required HTTP headers from requirements
  - Validate HTTP response status code
  - Parse JSON response and validate structure
  - Raise APIError with descriptive message on failure
  - _Requirements: 1.4, 1.5, 4.1, 4.2, 4.3_

- [x] 6. Implement event processor module
  - Create src/event_processor.py with EventProcessor class
  - Implement __init__() to accept venue_mappings dictionary
  - Implement abbreviate_venue() with keyword substring matching logic
  - Implement process_events() to extract events array from API response
  - Extract location.title and title fields from each event object
  - Apply venue abbreviation to each location
  - Handle missing fields gracefully with warning logs and skip invalid events
  - Return list of (abbreviated_venue, event_title) tuples
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 4.4, 4.5_

- [x] 7. Implement output formatter module
  - Create src/output_formatter.py with OutputFormatter class
  - Implement format_legacy() for shell script compatible format (venue,title# delimited)
  - Implement format_json() to output JSON array with venue and title fields
  - Implement format_csv() to output CSV with headers
  - Implement format_plain() to output one event per line as "venue: title"
  - Implement format_events() dispatcher function to route to appropriate formatter
  - Handle empty events list appropriately for each format
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8_

- [x] 8. Implement main entry point and CLI
  - Create main() function in villages_events.py
  - Implement argparse for command-line argument parsing with --format option
  - Set default format to "legacy" for backward compatibility
  - Initialize Config and load venue mappings
  - Orchestrate execution: fetch token → establish session → fetch events → process events → format output
  - Implement top-level error handling with appropriate logging to stderr
  - Print formatted output to stdout
  - Return exit code 0 on success, 1 on runtime error, 2 on invalid arguments
  - Add if __name__ == "__main__" block to call main()
  - _Requirements: 6.4, 7.3, 8.1, 8.2, 8.3_

- [x] 9. Create comprehensive documentation
  - Create README.md with project overview and purpose
  - Document installation instructions including Python version requirement and pip install -r requirements.txt
  - Document usage examples for all output formats with command-line syntax
  - Document configuration options for venue abbreviations
  - Document output format specifications with examples
  - Explain how the application works and its relationship to the original shell script
  - Include troubleshooting section for common issues
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 10. Write unit tests
  - Create tests/ directory structure
  - Write unit tests for token_fetcher module with mocked HTTP responses
  - Write unit tests for event_processor module testing venue abbreviation and event extraction
  - Write unit tests for output_formatter module testing all format types
  - Write unit tests for session_manager module
  - Use unittest or pytest framework
  - Mock HTTP requests using unittest.mock or responses library
  - _Requirements: 4.5, 8.4, 8.5_

- [x] 11. Write integration tests
  - Write end-to-end integration test with all HTTP requests mocked
  - Test complete pipeline from token fetch to formatted output
  - Test error handling paths (network failures, invalid JSON, missing fields)
  - Verify output matches expected format for each output type
  - _Requirements: 8.1, 8.2, 8.3_

- [x] 12. Add configurable output fields support to Config module
  - Add DEFAULT_OUTPUT_FIELDS constant with ["location.title", "title"] for backward compatibility
  - Add AVAILABLE_FIELDS constant listing all supported field paths from API response
  - Update Config class documentation to include field configuration
  - _Requirements: 9.3, 9.4_

- [x] 13. Update EventProcessor to support configurable fields
  - Modify __init__() to accept output_fields parameter with default to DEFAULT_OUTPUT_FIELDS
  - Implement extract_field() method to extract values using dot notation (e.g., "location.title", "start.date")
  - Update process_events() to return list of dictionaries instead of tuples
  - Extract all specified fields for each event using extract_field()
  - Apply venue abbreviation only to "location.title" field when present
  - Handle missing nested fields gracefully (return empty string)
  - _Requirements: 9.5, 9.6, 9.11_

- [x] 14. Update OutputFormatter to support configurable fields
  - Modify format_meshtastic() to accept field_names parameter and use first two fields
  - Modify format_json() to output all fields from event dictionaries
  - Modify format_csv() to accept field_names parameter and create headers from field names
  - Modify format_plain() to accept field_names parameter and display all fields
  - Update format_events() to accept field_names parameter and pass to formatters
  - Handle empty or missing field values in all formats
  - _Requirements: 9.7, 9.8, 9.9, 9.10_

- [x] 15. Add output_fields configuration to config.yaml
  - Add output_fields setting to config.yaml.example with default ["location.title", "title"]
  - Add comments explaining available field paths and dot notation
  - Add example configurations showing different field combinations
  - Update ConfigLoader to load output_fields from YAML
  - _Requirements: 9.12_

- [x] 16. Add --fields command-line argument
  - Add --fields argument to argparse that accepts comma-separated field names
  - Parse comma-separated string into list of field names
  - Implement precedence: command-line overrides config file, config file overrides defaults
  - Validate field names against AVAILABLE_FIELDS and warn about invalid fields
  - _Requirements: 9.13, 9.14_

- [x] 17. Update main entry point to use configurable fields
  - Load output_fields from config file using ConfigLoader
  - Override with --fields argument if provided
  - Pass output_fields to EventProcessor initialization
  - Pass field_names to OutputFormatter.format_events()
  - Update error handling for invalid field specifications
  - _Requirements: 9.2, 9.14_

- [x] 18. Update documentation for configurable fields
  - Update README.md with examples of using --fields argument
  - Document all available field paths in AVAILABLE_FIELDS
  - Add examples showing different field combinations for various use cases
  - Document the output_fields configuration setting
  - Add examples of output in different formats with custom fields
  - _Requirements: 9.4, 9.12, 9.13_

- [x] 19. Write tests for configurable fields feature
  - Write unit tests for extract_field() method with various dot notation paths
  - Write unit tests for EventProcessor with custom output_fields
  - Write unit tests for OutputFormatter with custom field_names
  - Write integration tests with various field combinations
  - Test backward compatibility with default fields
  - Test handling of missing/invalid fields
  - _Requirements: 9.5, 9.6, 9.7, 9.8, 9.9, 9.10_
