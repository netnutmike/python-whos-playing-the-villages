# Feature: Configurable Output Fields

## Overview

This feature adds support for configurable output fields, allowing users to select which fields from the API response are included in the output. Previously, the application only output two fields: venue (location.title) and event title. With this enhancement, users can customize the output to include any combination of available fields from the API response.

## Motivation

The Villages Events API returns rich event data with many fields including descriptions, dates, addresses, images, URLs, and more. Users may want to:
- Include event times (start.date, end.date) for scheduling
- Show event descriptions or excerpts for more context
- Display addresses for navigation
- Include images and URLs for promotional materials
- Export event IDs for tracking and integration

By making fields configurable, users can tailor the output to their specific needs without requiring code changes.

## Available Fields

Based on the sample API response in `sampleoutput.json`, the following fields are available:

### Basic Event Information
- `title` - Event title/name
- `description` - Full event description
- `excerpt` - Short event description
- `category` - Event category (e.g., "entertainment")
- `subcategories` - Array of subcategories (e.g., ["classic-rock", "dance"])
- `id` - Unique event ID

### Date/Time Information
- `start.date` - Event start date/time (ISO 8601 format)
- `end.date` - Event end date/time (ISO 8601 format)
- `allDay` - Boolean indicating if event is all day

### Status Flags
- `cancelled` - Boolean indicating if event is cancelled
- `featured` - Boolean indicating if event is featured
- `enrolement` - Boolean for enrollment status

### Location Information
- `location.title` - Venue name (e.g., "Spanish Springs Town Square")
- `location.category` - Venue category (e.g., "town-squares")
- `location.id` - Unique venue ID
- `location.complexId` - Complex ID for venue grouping

### Address Information
- `address.streetAddress` - Street address
- `address.locality` - City/locality (e.g., "The Villages")
- `address.region` - State/region (e.g., "FL")
- `address.postalCode` - Postal code
- `address.country` - Country code (e.g., "US")

### Media and Links
- `image` - Event image URL
- `url` - Event website URL
- `otherInfo` - Additional information text

### Geographic Data
- `geo.type` - Geographic type (e.g., "Point")
- `geo.coordinates` - Array of [longitude, latitude]

## Configuration

### Config File (config.yaml)

Users can specify default output fields in the configuration file:

```yaml
output_fields:
  - location.title
  - title
  - start.date
  - description
```

### Command Line

Users can override the config file settings using the `--fields` argument:

```bash
./villages_events.py --fields location.title,title,start.date,category
```

### Precedence

1. Command-line `--fields` argument (highest priority)
2. Config file `output_fields` setting
3. Default fields: `["location.title", "title"]` (lowest priority)

## Output Format Behavior

### Meshtastic Format
Uses only the first two specified fields in the format: `field1,field2#field1,field2#`

Example with fields `["location.title", "title"]`:
```
Brownwood,Artist Name#Lake Sumter,Band Name#
```

### JSON Format
Includes all specified fields as properties in each event object:

```json
[
  {
    "location.title": "Brownwood",
    "title": "Artist Name",
    "start.date": "2025-11-14T22:00:00.000Z",
    "category": "entertainment"
  }
]
```

### CSV Format
Creates columns for all specified fields with headers:

```csv
location.title,title,start.date,category
Brownwood,Artist Name,2025-11-14T22:00:00.000Z,entertainment
Lake Sumter,Band Name,2025-11-14T22:00:00.000Z,entertainment
```

### Plain Text Format
Displays all fields in a readable format:

```
location.title: Brownwood, title: Artist Name, start.date: 2025-11-14T22:00:00.000Z
location.title: Lake Sumter, title: Band Name, start.date: 2025-11-14T22:00:00.000Z
```

## Implementation Details

### Field Extraction

Fields are extracted using dot notation to navigate nested objects:
- `title` → `event["title"]`
- `location.title` → `event["location"]["title"]`
- `start.date` → `event["start"]["date"]`
- `address.locality` → `event["address"]["locality"]`

### Missing Fields

When a specified field is missing from an event:
- The field value is set to an empty string `""`
- A warning is logged (optional, based on logging level)
- Processing continues for other fields and events

### Venue Abbreviation

The venue abbreviation feature (from `venue_mappings`) is applied only to the `location.title` field when it is included in the output. Other fields are output as-is from the API response.

## Backward Compatibility

The default output fields are `["location.title", "title"]`, which maintains backward compatibility with the existing behavior. Users who don't specify custom fields will see no change in output.

## Use Cases

### Use Case 1: Event Calendar with Times
```yaml
format: csv
output_fields:
  - title
  - location.title
  - start.date
  - end.date
```

### Use Case 2: Event Promotion
```yaml
format: json
output_fields:
  - title
  - description
  - image
  - url
  - location.title
```

### Use Case 3: Navigation/Mapping
```yaml
format: csv
output_fields:
  - title
  - location.title
  - address.streetAddress
  - address.locality
  - geo.coordinates
```

### Use Case 4: Event Filtering
```yaml
format: json
output_fields:
  - title
  - category
  - subcategories
  - cancelled
  - featured
```

## Testing Considerations

Tests should verify:
1. Field extraction with dot notation for nested fields
2. Handling of missing fields (empty string output)
3. Venue abbreviation applied only to location.title
4. All output formats work with custom fields
5. Backward compatibility with default fields
6. Command-line override of config file settings
7. Invalid field names are handled gracefully

## Documentation Updates

The following documentation needs to be updated:
1. README.md - Add examples of using --fields argument
2. config.yaml.example - Add output_fields with comments and examples
3. API.md - Document available fields and dot notation
4. QUICKSTART.md - Add quick examples of custom fields
