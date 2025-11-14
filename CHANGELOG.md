# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-14

### Added
- Initial release of Villages Event Scraper
- Token fetching from JavaScript file
- Session management with cookie handling
- API client for authenticated requests
- Event processing with venue abbreviation
- Multiple output formats: Meshtastic, JSON, CSV, plain
- Comprehensive error handling
- Command-line interface with format selection
- Unit tests for all modules
- Integration tests for end-to-end pipeline
- Complete documentation

### Features
- Fetch entertainment events from The Villages API
- Support for multiple output formats
- Graceful error handling with proper exit codes
- Configurable timeout settings
- Venue name abbreviation
- Robust logging system

## [Unreleased]

### Added
- `--raw` command-line option to output unprocessed API response for debugging
- 2 new tests for raw output functionality

## [1.0.6] - 2025-11-14

### Added
- Raw output option with `--raw` flag for debugging and data exploration

## [1.0.5] - 2025-11-14

### Changed
- Renamed "legacy" output format to "meshtastic" to better reflect its purpose
- Updated all documentation and examples to use "meshtastic" terminology

## [1.0.4] - 2025-11-14

### Added
- YAML configuration file support (`config.yaml`)
- Ability to set default values for all parameters in config file
- Customizable venue mappings via config file
- Configurable HTTP timeout
- `config.yaml.example` template file
- 9 new tests for configuration loader

### Changed
- Command-line arguments now override config file defaults
- Application loads defaults from config file if present
- Added PyYAML dependency

## [1.0.3] - 2025-11-14

### Added
- Location filtering with `--location` parameter
- Support for 15 location options

## [1.0.2] - 2025-11-14

### Added
- Category filtering with `--category` parameter
- Support for 8 event categories

## [1.0.1] - 2025-11-14

### Added
- Date range filtering with `--date-range` parameter
- Support for 7 date range options

### Planned
- Add caching support
- Add category filtering options
- Performance optimizations
