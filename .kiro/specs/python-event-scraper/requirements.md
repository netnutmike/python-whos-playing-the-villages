# Requirements Document

## Introduction

This document specifies the requirements for converting a bash shell script that fetches entertainment events from The Villages API into a Python application. The system will replicate the existing functionality while providing better maintainability, error handling, and documentation. The Python application will fetch event data, process venue names, and output formatted event information.

## Glossary

- **Event Scraper**: The Python application that fetches and processes event data from The Villages API
- **Auth Token**: A Base64-encoded authentication token extracted from a JavaScript file used to authorize API requests
- **Venue Abbreviation**: A shortened version of a venue name based on predefined keywords
- **Cookie Jar**: A mechanism for storing and managing HTTP session cookies
- **API Response**: JSON-formatted data returned from The Villages events API containing event information

## Requirements

### Requirement 1

**User Story:** As a developer, I want to fetch entertainment events from The Villages API using Python, so that I can process event data programmatically with better error handling and maintainability than the shell script.

#### Acceptance Criteria

1. WHEN the Event Scraper executes, THE Event Scraper SHALL fetch the main.js file from https://cdn.thevillages.com/web_components/myvillages-auth-forms/main.js
2. WHEN the Event Scraper receives the main.js content, THE Event Scraper SHALL extract the dp_AUTH_TOKEN value using pattern matching for "Basic" followed by Base64-encoded characters
3. IF the Event Scraper fails to fetch main.js or extract the token, THEN THE Event Scraper SHALL log an error message and terminate with a non-zero exit code
4. WHEN the Event Scraper has a valid Auth Token, THE Event Scraper SHALL make an authenticated API request to https://api.v2.thevillages.com/events/ with appropriate query parameters for today's entertainment events at town squares
5. WHEN making API requests, THE Event Scraper SHALL include proper HTTP headers including User-Agent, Authorization, Accept, Origin, and Referer

### Requirement 2

**User Story:** As a developer, I want the application to handle HTTP sessions and cookies properly, so that the API requests are accepted by the server.

#### Acceptance Criteria

1. WHEN the Event Scraper prepares to make API requests, THE Event Scraper SHALL first visit the calendar page at https://www.thevillages.com/calendar/ to establish a session and capture cookies
2. WHEN the Event Scraper makes the events API request, THE Event Scraper SHALL include the session cookies obtained from the calendar page visit
3. WHEN the Event Scraper completes execution, THE Event Scraper SHALL clean up any temporary cookie storage files
4. IF cookie handling fails, THEN THE Event Scraper SHALL log a warning but attempt to proceed with the API request

### Requirement 3

**User Story:** As a developer, I want venue names to be abbreviated according to predefined rules, so that the output is concise and consistent.

#### Acceptance Criteria

1. THE Event Scraper SHALL maintain a configurable mapping of venue keywords to their abbreviated forms
2. WHEN the Event Scraper processes a venue name, THE Event Scraper SHALL check if the venue name contains any predefined keywords
3. IF a venue name contains a keyword from the mapping, THEN THE Event Scraper SHALL replace the full venue name with the corresponding abbreviation
4. IF a venue name does not match any keyword, THEN THE Event Scraper SHALL use the original venue name without modification
5. THE Event Scraper SHALL support the following default venue abbreviations: Brownwood, Sawgrass, Spanish Springs, and Lake Sumter

### Requirement 4

**User Story:** As a developer, I want the application to parse and validate JSON responses, so that I can ensure data integrity before processing events.

#### Acceptance Criteria

1. WHEN the Event Scraper receives an API response, THE Event Scraper SHALL validate that the response is valid JSON format
2. IF the API response is not valid JSON, THEN THE Event Scraper SHALL log an error message with details and terminate with a non-zero exit code
3. WHEN the Event Scraper parses valid JSON, THE Event Scraper SHALL extract the events array from the response
4. WHEN the Event Scraper processes each event, THE Event Scraper SHALL extract the location title and event title fields
5. IF required fields are missing from an event object, THEN THE Event Scraper SHALL skip that event and log a warning

### Requirement 5

**User Story:** As a developer, I want the application to output formatted event data with configurable output formats, so that I can choose between different presentation styles while maintaining backward compatibility with the original shell script.

#### Acceptance Criteria

1. THE Event Scraper SHALL support multiple output format options selectable via command-line argument
2. WHEN no output format is specified, THE Event Scraper SHALL use the legacy format as the default
3. WHEN the Event Scraper uses legacy format, THE Event Scraper SHALL format each event as "abbreviated_venue,event_title" concatenated with "#" delimiters and a final "#" character
4. WHEN the Event Scraper uses JSON format option, THE Event Scraper SHALL output a valid JSON array containing event objects with venue and title fields
5. WHEN the Event Scraper uses CSV format option, THE Event Scraper SHALL output comma-separated values with headers "venue,title"
6. WHEN the Event Scraper uses plain text format option, THE Event Scraper SHALL output one event per line formatted as "venue: title"
7. THE Event Scraper SHALL output the formatted data to standard output
8. IF no events are found, THEN THE Event Scraper SHALL output format-appropriate empty data (single "#" for legacy, empty array for JSON, headers only for CSV, empty string for plain text)

### Requirement 9

**User Story:** As a user, I want to configure which fields from the API response are included in the output, so that I can customize the information displayed based on my needs.

#### Acceptance Criteria

1. THE Event Scraper SHALL support configurable output fields that can be specified in the configuration file
2. THE Event Scraper SHALL support configurable output fields that can be specified via command-line argument
3. WHEN no output fields are specified, THE Event Scraper SHALL default to outputting "location.title" and "title" fields (maintaining backward compatibility)
4. THE Event Scraper SHALL support the following field paths from the API response: title, description, excerpt, category, subcategories, start.date, end.date, allDay, cancelled, featured, location.title, location.category, address.streetAddress, address.locality, address.region, address.postalCode, address.country, image, url, otherInfo, id
5. WHEN a user specifies nested fields, THE Event Scraper SHALL use dot notation (e.g., "location.title", "start.date", "address.locality")
6. WHEN a specified field is missing from an event, THE Event Scraper SHALL output an empty string or null value for that field
7. WHEN outputting in JSON format, THE Event Scraper SHALL include all specified fields as separate properties in each event object
8. WHEN outputting in CSV format, THE Event Scraper SHALL include all specified fields as separate columns with appropriate headers
9. WHEN outputting in plain text format, THE Event Scraper SHALL display all specified fields in a readable format
10. WHEN outputting in meshtastic format, THE Event Scraper SHALL use the first two specified fields for the comma-separated pairs (maintaining backward compatibility with venue,title format)
11. THE Event Scraper SHALL apply venue abbreviation only to the "location.title" field when it is included in the output
12. THE configuration file SHALL include an "output_fields" setting that accepts a list of field names
13. THE command-line interface SHALL include a "--fields" argument that accepts a comma-separated list of field names
14. WHEN both configuration file and command-line fields are specified, THE command-line argument SHALL take precedence

### Requirement 6

**User Story:** As a developer, I want comprehensive documentation for the Python application, so that I can understand how to install, configure, and use the system.

#### Acceptance Criteria

1. THE Event Scraper SHALL include a README.md file that explains the purpose and functionality of the application
2. THE Event Scraper SHALL include installation instructions with all required dependencies listed
3. THE Event Scraper SHALL include usage examples showing how to run the application
4. THE Event Scraper SHALL include documentation explaining the configuration options for venue abbreviations
5. THE Event Scraper SHALL include documentation explaining the output format and how to parse it

### Requirement 7

**User Story:** As a developer, I want proper project structure and dependency management, so that the Python application is easy to install and maintain.

#### Acceptance Criteria

1. THE Event Scraper SHALL include a requirements.txt file listing all Python package dependencies with version specifications
2. THE Event Scraper SHALL use the requests library for HTTP operations
3. THE Event Scraper SHALL organize code into logical modules with clear separation of concerns
4. THE Event Scraper SHALL include a main entry point that can be executed as a script
5. THE Event Scraper SHALL follow Python best practices for code structure and naming conventions

### Requirement 8

**User Story:** As a developer, I want robust error handling and logging, so that I can diagnose issues when the application fails.

#### Acceptance Criteria

1. WHEN the Event Scraper encounters an error, THE Event Scraper SHALL log descriptive error messages to standard error
2. WHEN the Event Scraper executes successfully, THE Event Scraper SHALL exit with code 0
3. WHEN the Event Scraper encounters a fatal error, THE Event Scraper SHALL exit with a non-zero exit code
4. THE Event Scraper SHALL handle network timeouts with appropriate error messages
5. THE Event Scraper SHALL handle HTTP error status codes with appropriate error messages
