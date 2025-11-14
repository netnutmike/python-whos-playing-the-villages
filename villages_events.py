#!/usr/bin/env python3
"""
Villages Event Scraper - Main entry point

Fetches entertainment events from The Villages API and outputs formatted event data.
"""

import sys
import argparse
import logging

from src.config import Config
from src.config_loader import ConfigLoader
from src.token_fetcher import fetch_auth_token
from src.session_manager import SessionManager
from src.api_client import fetch_events
from src.event_processor import EventProcessor
from src.output_formatter import OutputFormatter
from src.exceptions import VillagesEventError


def main() -> int:
    """
    Main entry point for the application.
    Returns exit code (0 for success, non-zero for failure).
    """
    # Configure logging
    logging.basicConfig(
        level=logging.WARNING,
        format='[%(levelname)s] %(message)s',
        stream=sys.stderr
    )
    
    # Load configuration from YAML file
    yaml_config = ConfigLoader.load_config()
    
    # Get defaults from config file or fall back to hardcoded defaults
    default_format = ConfigLoader.get_default(yaml_config, 'format', Config.DEFAULT_FORMAT)
    default_date_range = ConfigLoader.get_default(yaml_config, 'date_range', Config.DEFAULT_DATE_RANGE)
    default_category = ConfigLoader.get_default(yaml_config, 'category', Config.DEFAULT_CATEGORY)
    default_location = ConfigLoader.get_default(yaml_config, 'location', Config.DEFAULT_LOCATION)
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Fetch and format entertainment events from The Villages API'
    )
    parser.add_argument(
        '--format',
        choices=Config.VALID_FORMATS,
        default=default_format,
        help=f'Output format (default: {default_format})'
    )
    parser.add_argument(
        '--date-range',
        choices=Config.VALID_DATE_RANGES,
        default=default_date_range,
        help=f'Date range for events (default: {default_date_range})'
    )
    parser.add_argument(
        '--category',
        choices=Config.VALID_CATEGORIES,
        default=default_category,
        help=f'Event category (default: {default_category})'
    )
    parser.add_argument(
        '--location',
        choices=Config.VALID_LOCATIONS,
        default=default_location,
        help=f'Event location (default: {default_location})'
    )
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    parser.add_argument(
        '--raw',
        action='store_true',
        help='Output raw API response without processing (for debugging)'
    )
    parser.add_argument(
        '--fields',
        type=str,
        help='Comma-separated list of field names to include in output (e.g., "location.title,title,start.date")'
    )
    
    try:
        args = parser.parse_args()
    except SystemExit as e:
        # argparse calls sys.exit() on error or --help
        # Return exit code 2 for invalid arguments, 0 for --help
        return 2 if e.code != 0 else 0
    
    try:
        # Load venue mappings from config file or use defaults
        venue_mappings = ConfigLoader.get_default(
            yaml_config, 'venue_mappings', Config.DEFAULT_VENUE_MAPPINGS
        )
        
        # Get timeout from config file or use default
        timeout = ConfigLoader.get_default(yaml_config, 'timeout', Config.DEFAULT_TIMEOUT)
        
        # Determine output fields with precedence: CLI > config file > defaults
        output_fields = Config.DEFAULT_OUTPUT_FIELDS
        
        # Load from config file if present
        config_fields = ConfigLoader.get_output_fields(yaml_config, Config.DEFAULT_OUTPUT_FIELDS)
        if config_fields != Config.DEFAULT_OUTPUT_FIELDS:
            output_fields = config_fields
        
        # Override with command-line argument if provided
        if args.fields:
            # Parse comma-separated field names
            cli_fields = [field.strip() for field in args.fields.split(',') if field.strip()]
            
            # Validate field names against AVAILABLE_FIELDS
            invalid_fields = [f for f in cli_fields if f not in Config.AVAILABLE_FIELDS]
            if invalid_fields:
                logging.warning(
                    f"Invalid field names will be ignored: {', '.join(invalid_fields)}. "
                    f"Valid fields are: {', '.join(Config.AVAILABLE_FIELDS)}"
                )
            
            # Filter to only valid fields
            valid_fields = [f for f in cli_fields if f in Config.AVAILABLE_FIELDS]
            
            if valid_fields:
                output_fields = valid_fields
            else:
                logging.warning(
                    f"No valid fields specified, using defaults: {', '.join(Config.DEFAULT_OUTPUT_FIELDS)}"
                )
        
        # Generate URLs with specified filters
        calendar_url = Config.get_calendar_url(args.date_range, args.category, args.location)
        api_url = Config.get_api_url(args.date_range, args.category, args.location)
        
        # Step 1: Fetch authentication token
        logging.debug("Fetching authentication token...")
        auth_token = fetch_auth_token(Config.JS_URL, timeout=timeout)
        
        # Step 2: Establish session with context manager for cleanup
        with SessionManager() as session_manager:
            logging.debug("Establishing session...")
            session_manager.establish_session(calendar_url, timeout=timeout)
            session = session_manager.get_session()
            
            # Step 3: Fetch events from API
            logging.debug(
                f"Fetching events from API (date range: {args.date_range}, "
                f"category: {args.category}, location: {args.location})..."
            )
            api_response = fetch_events(
                session=session,
                api_url=api_url,
                auth_token=auth_token,
                timeout=timeout
            )
            
            # If raw output requested, print API response and exit
            if args.raw:
                import json
                print(json.dumps(api_response, indent=2))
                return 0
            
            # Step 4: Process events
            logging.debug("Processing events...")
            processor = EventProcessor(venue_mappings, output_fields=output_fields)
            processed_events = processor.process_events(api_response)
            
            # Step 5: Format output
            logging.debug(f"Formatting output as {args.format}...")
            formatted_output = OutputFormatter.format_events(
                processed_events,
                format_type=args.format,
                field_names=output_fields
            )
            
            # Step 6: Print formatted output to stdout
            print(formatted_output, end='')
        
        # Success
        return 0
        
    except VillagesEventError as e:
        # Handle all application-specific errors
        logging.error(str(e))
        return 1
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
