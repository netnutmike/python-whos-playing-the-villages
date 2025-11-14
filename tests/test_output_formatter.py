"""Unit tests for output_formatter module."""

import unittest
import json
from src.output_formatter import OutputFormatter


class TestOutputFormatter(unittest.TestCase):
    """Test cases for output formatter functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_events = [
            ("Brownwood", "Artist One"),
            ("Spanish Springs", "Artist Two"),
            ("Sawgrass", "Artist Three")
        ]

    def test_format_meshtastic_with_events(self):
        """Test Meshtastic format with events."""
        result = OutputFormatter.format_meshtastic(self.sample_events)
        expected = "Brownwood,Artist One#Spanish Springs,Artist Two#Sawgrass,Artist Three#"
        self.assertEqual(result, expected)

    def test_format_meshtastic_empty(self):
        """Test Meshtastic format with empty events list."""
        result = OutputFormatter.format_meshtastic([])
        self.assertEqual(result, "#")

    def test_format_json_with_events(self):
        """Test JSON format with events."""
        result = OutputFormatter.format_json(self.sample_events)
        parsed = json.loads(result)
        
        self.assertEqual(len(parsed), 3)
        self.assertEqual(parsed[0], {"venue": "Brownwood", "title": "Artist One"})
        self.assertEqual(parsed[1], {"venue": "Spanish Springs", "title": "Artist Two"})
        self.assertEqual(parsed[2], {"venue": "Sawgrass", "title": "Artist Three"})

    def test_format_json_empty(self):
        """Test JSON format with empty events list."""
        result = OutputFormatter.format_json([])
        parsed = json.loads(result)
        self.assertEqual(parsed, [])

    def test_format_csv_with_events(self):
        """Test CSV format with events."""
        result = OutputFormatter.format_csv(self.sample_events)
        lines = [line.strip() for line in result.strip().split('\n')]
        
        self.assertEqual(lines[0], "venue,title")
        self.assertEqual(lines[1], "Brownwood,Artist One")
        self.assertEqual(lines[2], "Spanish Springs,Artist Two")
        self.assertEqual(lines[3], "Sawgrass,Artist Three")

    def test_format_csv_empty(self):
        """Test CSV format with empty events list."""
        result = OutputFormatter.format_csv([])
        self.assertEqual(result.strip(), "venue,title")

    def test_format_plain_with_events(self):
        """Test plain format with events."""
        result = OutputFormatter.format_plain(self.sample_events)
        expected = "Brownwood: Artist One\nSpanish Springs: Artist Two\nSawgrass: Artist Three\n"
        self.assertEqual(result, expected)

    def test_format_plain_empty(self):
        """Test plain format with empty events list."""
        result = OutputFormatter.format_plain([])
        self.assertEqual(result, "")

    def test_format_events_meshtastic(self):
        """Test format_events dispatcher with Meshtastic format."""
        result = OutputFormatter.format_events(self.sample_events, "meshtastic")
        self.assertIn("Brownwood,Artist One#", result)

    def test_format_events_json(self):
        """Test format_events dispatcher with JSON format."""
        result = OutputFormatter.format_events(self.sample_events, "json")
        parsed = json.loads(result)
        self.assertEqual(len(parsed), 3)

    def test_format_events_csv(self):
        """Test format_events dispatcher with CSV format."""
        result = OutputFormatter.format_events(self.sample_events, "csv")
        self.assertIn("venue,title", result)

    def test_format_events_plain(self):
        """Test format_events dispatcher with plain format."""
        result = OutputFormatter.format_events(self.sample_events, "plain")
        self.assertIn("Brownwood: Artist One", result)

    def test_format_events_invalid_format(self):
        """Test format_events with invalid format type."""
        with self.assertRaises(ValueError) as context:
            OutputFormatter.format_events(self.sample_events, "invalid")
        
        self.assertIn("Invalid format type", str(context.exception))


if __name__ == '__main__':
    unittest.main()
