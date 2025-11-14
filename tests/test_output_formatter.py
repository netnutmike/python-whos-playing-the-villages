"""Unit tests for output_formatter module."""

import unittest
import json
from src.output_formatter import OutputFormatter


class TestOutputFormatter(unittest.TestCase):
    """Test cases for output formatter functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_events = [
            {"location.title": "Brownwood", "title": "Artist One"},
            {"location.title": "Spanish Springs", "title": "Artist Two"},
            {"location.title": "Sawgrass", "title": "Artist Three"}
        ]
        self.default_field_names = ["location.title", "title"]

    def test_format_meshtastic_with_events(self):
        """Test Meshtastic format with events."""
        result = OutputFormatter.format_meshtastic(self.sample_events, self.default_field_names)
        expected = "Brownwood,Artist One#Spanish Springs,Artist Two#Sawgrass,Artist Three#"
        self.assertEqual(result, expected)

    def test_format_meshtastic_empty(self):
        """Test Meshtastic format with empty events list."""
        result = OutputFormatter.format_meshtastic([], self.default_field_names)
        self.assertEqual(result, "#")

    def test_format_meshtastic_custom_fields(self):
        """Test Meshtastic format with custom fields."""
        events = [
            {"title": "Event 1", "start.date": "2025-11-14", "location.title": "Venue 1"},
            {"title": "Event 2", "start.date": "2025-11-15", "location.title": "Venue 2"}
        ]
        result = OutputFormatter.format_meshtastic(events, ["title", "start.date"])
        expected = "Event 1,2025-11-14#Event 2,2025-11-15#"
        self.assertEqual(result, expected)

    def test_format_meshtastic_missing_fields(self):
        """Test Meshtastic format handles missing fields."""
        events = [{"location.title": "Brownwood"}]
        result = OutputFormatter.format_meshtastic(events, self.default_field_names)
        expected = "Brownwood,#"
        self.assertEqual(result, expected)

    def test_format_json_with_events(self):
        """Test JSON format with events."""
        result = OutputFormatter.format_json(self.sample_events)
        parsed = json.loads(result)
        
        self.assertEqual(len(parsed), 3)
        self.assertEqual(parsed[0], {"location.title": "Brownwood", "title": "Artist One"})
        self.assertEqual(parsed[1], {"location.title": "Spanish Springs", "title": "Artist Two"})
        self.assertEqual(parsed[2], {"location.title": "Sawgrass", "title": "Artist Three"})

    def test_format_json_empty(self):
        """Test JSON format with empty events list."""
        result = OutputFormatter.format_json([])
        parsed = json.loads(result)
        self.assertEqual(parsed, [])

    def test_format_json_all_fields(self):
        """Test JSON format outputs all fields from event dictionaries."""
        events = [
            {"title": "Event", "start.date": "2025-11-14", "location.title": "Venue", "description": "Test"}
        ]
        result = OutputFormatter.format_json(events)
        parsed = json.loads(result)
        self.assertEqual(len(parsed[0]), 4)
        self.assertIn("description", parsed[0])

    def test_format_csv_with_events(self):
        """Test CSV format with events."""
        result = OutputFormatter.format_csv(self.sample_events, self.default_field_names)
        lines = [line.strip() for line in result.strip().split('\n')]
        
        self.assertEqual(lines[0], "location.title,title")
        self.assertEqual(lines[1], "Brownwood,Artist One")
        self.assertEqual(lines[2], "Spanish Springs,Artist Two")
        self.assertEqual(lines[3], "Sawgrass,Artist Three")

    def test_format_csv_empty(self):
        """Test CSV format with empty events list."""
        result = OutputFormatter.format_csv([], self.default_field_names)
        self.assertEqual(result.strip(), "location.title,title")

    def test_format_csv_custom_fields(self):
        """Test CSV format with custom field names."""
        events = [
            {"title": "Event 1", "start.date": "2025-11-14", "location.title": "Venue 1"}
        ]
        result = OutputFormatter.format_csv(events, ["title", "start.date", "location.title"])
        lines = [line.strip() for line in result.strip().split('\n')]
        self.assertEqual(lines[0], "title,start.date,location.title")
        self.assertEqual(lines[1], "Event 1,2025-11-14,Venue 1")

    def test_format_csv_missing_fields(self):
        """Test CSV format handles missing fields."""
        events = [{"location.title": "Brownwood"}]
        result = OutputFormatter.format_csv(events, self.default_field_names)
        lines = [line.strip() for line in result.strip().split('\n')]
        self.assertEqual(lines[1], "Brownwood,")

    def test_format_plain_with_events(self):
        """Test plain format with events."""
        result = OutputFormatter.format_plain(self.sample_events, self.default_field_names)
        expected = "location.title: Brownwood, title: Artist One\nlocation.title: Spanish Springs, title: Artist Two\nlocation.title: Sawgrass, title: Artist Three\n"
        self.assertEqual(result, expected)

    def test_format_plain_empty(self):
        """Test plain format with empty events list."""
        result = OutputFormatter.format_plain([], self.default_field_names)
        self.assertEqual(result, "")

    def test_format_plain_custom_fields(self):
        """Test plain format with custom fields."""
        events = [
            {"title": "Event 1", "start.date": "2025-11-14"}
        ]
        result = OutputFormatter.format_plain(events, ["title", "start.date"])
        expected = "title: Event 1, start.date: 2025-11-14\n"
        self.assertEqual(result, expected)

    def test_format_plain_missing_fields(self):
        """Test plain format handles missing fields."""
        events = [{"location.title": "Brownwood"}]
        result = OutputFormatter.format_plain(events, self.default_field_names)
        expected = "location.title: Brownwood, title: \n"
        self.assertEqual(result, expected)

    def test_format_events_meshtastic(self):
        """Test format_events dispatcher with Meshtastic format."""
        result = OutputFormatter.format_events(self.sample_events, "meshtastic", self.default_field_names)
        self.assertIn("Brownwood,Artist One#", result)

    def test_format_events_json(self):
        """Test format_events dispatcher with JSON format."""
        result = OutputFormatter.format_events(self.sample_events, "json", self.default_field_names)
        parsed = json.loads(result)
        self.assertEqual(len(parsed), 3)

    def test_format_events_csv(self):
        """Test format_events dispatcher with CSV format."""
        result = OutputFormatter.format_events(self.sample_events, "csv", self.default_field_names)
        self.assertIn("location.title,title", result)

    def test_format_events_plain(self):
        """Test format_events dispatcher with plain format."""
        result = OutputFormatter.format_events(self.sample_events, "plain", self.default_field_names)
        self.assertIn("location.title: Brownwood", result)

    def test_format_events_default_field_names(self):
        """Test format_events uses default field names when not provided."""
        result = OutputFormatter.format_events(self.sample_events, "meshtastic")
        expected = "Brownwood,Artist One#Spanish Springs,Artist Two#Sawgrass,Artist Three#"
        self.assertEqual(result, expected)

    def test_format_events_invalid_format(self):
        """Test format_events with invalid format type."""
        with self.assertRaises(ValueError) as context:
            OutputFormatter.format_events(self.sample_events, "invalid", self.default_field_names)
        
        self.assertIn("Invalid format type", str(context.exception))


if __name__ == '__main__':
    unittest.main()
