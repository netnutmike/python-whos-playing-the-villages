"""Unit tests for event_processor module."""

import unittest
from src.event_processor import EventProcessor
from src.exceptions import ProcessingError


class TestEventProcessor(unittest.TestCase):
    """Test cases for event processor functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.venue_mappings = {
            "Brownwood": "Brownwood",
            "Sawgrass": "Sawgrass",
            "Spanish Springs": "Spanish Springs",
            "Lake Sumter": "Lake Sumter"
        }
        self.processor = EventProcessor(self.venue_mappings)

    def test_abbreviate_venue_with_match(self):
        """Test venue abbreviation with matching keyword."""
        result = self.processor.abbreviate_venue("Brownwood Paddock Square")
        self.assertEqual(result, "Brownwood")

    def test_abbreviate_venue_no_match(self):
        """Test venue abbreviation with no matching keyword."""
        result = self.processor.abbreviate_venue("Unknown Venue Location")
        self.assertEqual(result, "Unknown Venue Location")

    def test_abbreviate_venue_empty_string(self):
        """Test venue abbreviation with empty string."""
        result = self.processor.abbreviate_venue("")
        self.assertEqual(result, "")

    def test_process_events_success(self):
        """Test successful event processing."""
        api_response = {
            "events": [
                {
                    "location": {"title": "Brownwood Paddock Square"},
                    "title": "Artist One"
                },
                {
                    "location": {"title": "Spanish Springs Town Square"},
                    "title": "Artist Two"
                }
            ]
        }
        
        result = self.processor.process_events(api_response)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], {"location.title": "Brownwood", "title": "Artist One"})
        self.assertEqual(result[1], {"location.title": "Spanish Springs", "title": "Artist Two"})

    def test_process_events_missing_events_key(self):
        """Test error when events key is missing."""
        api_response = {"data": []}
        
        with self.assertRaises(ProcessingError) as context:
            self.processor.process_events(api_response)
        
        self.assertIn("Missing 'events' key", str(context.exception))

    def test_process_events_not_a_list(self):
        """Test error when events is not a list."""
        api_response = {"events": "not a list"}
        
        with self.assertRaises(ProcessingError) as context:
            self.processor.process_events(api_response)
        
        self.assertIn("not a list", str(context.exception))

    def test_process_events_empty_list(self):
        """Test processing empty events list."""
        api_response = {"events": []}
        
        result = self.processor.process_events(api_response)
        
        self.assertEqual(result, [])

    def test_process_events_missing_location(self):
        """Test handling event with missing location field."""
        api_response = {
            "events": [
                {"title": "Artist One"},
                {
                    "location": {"title": "Brownwood Paddock Square"},
                    "title": "Artist Two"
                }
            ]
        }
        
        result = self.processor.process_events(api_response)
        
        # Both events should be processed, first one with empty location.title
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], {"location.title": "", "title": "Artist One"})
        self.assertEqual(result[1], {"location.title": "Brownwood", "title": "Artist Two"})

    def test_process_events_missing_title(self):
        """Test handling event with missing title field."""
        api_response = {
            "events": [
                {
                    "location": {"title": "Brownwood Paddock Square"},
                    "title": "Artist One"
                },
                {
                    "location": {"title": "Sawgrass Grove"}
                }
            ]
        }
        
        result = self.processor.process_events(api_response)
        
        # Both events should be processed, second one with empty title
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], {"location.title": "Brownwood", "title": "Artist One"})
        self.assertEqual(result[1], {"location.title": "Sawgrass", "title": ""})

    def test_extract_field_simple(self):
        """Test extracting a simple field."""
        event = {"title": "Test Event"}
        result = self.processor.extract_field(event, "title")
        self.assertEqual(result, "Test Event")

    def test_extract_field_nested(self):
        """Test extracting a nested field using dot notation."""
        event = {
            "location": {"title": "Test Location"},
            "start": {"date": "2025-11-14"}
        }
        result = self.processor.extract_field(event, "location.title")
        self.assertEqual(result, "Test Location")
        
        result = self.processor.extract_field(event, "start.date")
        self.assertEqual(result, "2025-11-14")

    def test_extract_field_missing(self):
        """Test extracting a missing field returns empty string."""
        event = {"title": "Test Event"}
        result = self.processor.extract_field(event, "description")
        self.assertEqual(result, "")

    def test_extract_field_missing_nested(self):
        """Test extracting a missing nested field returns empty string."""
        event = {"title": "Test Event"}
        result = self.processor.extract_field(event, "location.title")
        self.assertEqual(result, "")

    def test_extract_field_none_value(self):
        """Test extracting a field with None value returns empty string."""
        event = {"description": None}
        result = self.processor.extract_field(event, "description")
        self.assertEqual(result, "")

    def test_custom_output_fields(self):
        """Test processing events with custom output fields."""
        processor = EventProcessor(
            self.venue_mappings,
            output_fields=["title", "location.title", "category"]
        )
        
        api_response = {
            "events": [
                {
                    "location": {"title": "Brownwood Paddock Square"},
                    "title": "Artist One",
                    "category": "entertainment"
                }
            ]
        }
        
        result = processor.process_events(api_response)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], {
            "title": "Artist One",
            "location.title": "Brownwood",
            "category": "entertainment"
        })

    def test_venue_abbreviation_only_on_location_title(self):
        """Test that venue abbreviation is only applied to location.title field."""
        processor = EventProcessor(
            self.venue_mappings,
            output_fields=["title", "location.title", "description"]
        )
        
        api_response = {
            "events": [
                {
                    "location": {"title": "Brownwood Paddock Square"},
                    "title": "Brownwood Artist",
                    "description": "Event at Brownwood"
                }
            ]
        }
        
        result = processor.process_events(api_response)
        
        self.assertEqual(len(result), 1)
        # Only location.title should be abbreviated
        self.assertEqual(result[0]["location.title"], "Brownwood")
        # title and description should not be abbreviated
        self.assertEqual(result[0]["title"], "Brownwood Artist")
        self.assertEqual(result[0]["description"], "Event at Brownwood")


if __name__ == '__main__':
    unittest.main()
