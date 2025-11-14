"""Integration tests for Villages Event Scraper.

This module contains end-to-end integration tests that verify
the complete pipeline from token fetch to formatted output.
"""

import unittest
from unittest.mock import patch, Mock
import json
import sys
from io import StringIO

from villages_events import main
from src.config import Config
from src.exceptions import TokenFetchError, SessionError, APIError


class TestIntegrationEndToEnd(unittest.TestCase):
    """End-to-end integration tests with mocked HTTP requests."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_js_content = 'dp_AUTH_TOKEN = "Basic dGVzdHRva2VuMTIzNDU2";'
        self.mock_api_response = {
            "events": [
                {
                    "location": {"title": "Brownwood Paddock Square"},
                    "title": "Jazz Band"
                },
                {
                    "location": {"title": "Spanish Springs Town Square"},
                    "title": "Rock Group"
                },
                {
                    "location": {"title": "Sawgrass Grove"},
                    "title": "Country Singer"
                }
            ]
        }

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py'])
    def test_complete_pipeline_meshtastic_format(self, mock_token_get, mock_session_get, mock_api_get):
        """Test complete pipeline with Meshtastic format output."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify output format
        expected = "Brownwood,Jazz Band#Spanish Springs,Rock Group#Sawgrass,Country Singer#"
        self.assertEqual(output, expected)

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--format', 'json'])
    def test_complete_pipeline_json_format(self, mock_token_get, mock_session_get, mock_api_get):
        """Test complete pipeline with JSON format output."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify JSON output
        parsed = json.loads(output)
        self.assertEqual(len(parsed), 3)
        self.assertEqual(parsed[0]["location.title"], "Brownwood")
        self.assertEqual(parsed[0]["title"], "Jazz Band")

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--format', 'csv'])
    def test_complete_pipeline_csv_format(self, mock_token_get, mock_session_get, mock_api_get):
        """Test complete pipeline with CSV format output."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify CSV output
        lines = [line.strip() for line in output.strip().split('\n')]
        self.assertEqual(lines[0], "location.title,title")
        self.assertIn("Brownwood,Jazz Band", lines[1])

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--format', 'plain'])
    def test_complete_pipeline_plain_format(self, mock_token_get, mock_session_get, mock_api_get):
        """Test complete pipeline with plain format output."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify plain output
        self.assertIn("location.title: Brownwood, title: Jazz Band", output)
        self.assertIn("location.title: Spanish Springs, title: Rock Group", output)

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py'])
    def test_empty_events_list(self, mock_token_get, mock_session_get, mock_api_get):
        """Test pipeline with empty events list."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request with empty events
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = {"events": []}
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify empty output (single # for Meshtastic format)
        self.assertEqual(output, "#")


class TestIntegrationErrorHandling(unittest.TestCase):
    """Integration tests for error handling paths."""

    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py'])
    def test_token_fetch_network_failure(self, mock_get):
        """Test error handling when token fetch fails due to network error."""
        # Mock network failure
        mock_get.side_effect = __import__('requests').exceptions.RequestException("Network error")
        
        exit_code = main()
        
        # Verify non-zero exit code
        self.assertEqual(exit_code, 1)

    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py'])
    def test_token_pattern_not_found(self, mock_get):
        """Test error handling when token pattern is not found."""
        # Mock response without token
        mock_response = Mock()
        mock_response.text = "var someCode = 'no token here';"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        exit_code = main()
        
        # Verify non-zero exit code
        self.assertEqual(exit_code, 1)

    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py'])
    def test_session_establishment_failure(self, mock_token_get, mock_session_get):
        """Test error handling when session establishment fails."""
        # Mock successful token fetch
        mock_token_response = Mock()
        mock_token_response.text = 'dp_AUTH_TOKEN = "Basic dGVzdHRva2VuMTIzNDU2";'
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session failure
        mock_session_get.side_effect = __import__('requests').exceptions.RequestException("Connection error")
        
        exit_code = main()
        
        # Verify non-zero exit code
        self.assertEqual(exit_code, 1)

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py'])
    def test_api_request_failure(self, mock_token_get, mock_session_get, mock_api_get):
        """Test error handling when API request fails."""
        # Mock successful token fetch
        mock_token_response = Mock()
        mock_token_response.text = 'dp_AUTH_TOKEN = "Basic dGVzdHRva2VuMTIzNDU2";'
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock successful session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API failure
        mock_api_response = Mock()
        mock_api_response.status_code = 500
        mock_api_response.text = "Internal Server Error"
        mock_api_get.return_value = mock_api_response
        
        exit_code = main()
        
        # Verify non-zero exit code
        self.assertEqual(exit_code, 1)

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py'])
    def test_invalid_json_response(self, mock_token_get, mock_session_get, mock_api_get):
        """Test error handling when API returns invalid JSON."""
        # Mock successful token fetch
        mock_token_response = Mock()
        mock_token_response.text = 'dp_AUTH_TOKEN = "Basic dGVzdHRva2VuMTIzNDU2";'
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock successful session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API response with invalid JSON
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.side_effect = ValueError("Invalid JSON")
        mock_api_get.return_value = mock_api_response
        
        exit_code = main()
        
        # Verify non-zero exit code
        self.assertEqual(exit_code, 1)

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py'])
    def test_missing_events_field(self, mock_token_get, mock_session_get, mock_api_get):
        """Test error handling when API response is missing events field."""
        # Mock successful token fetch
        mock_token_response = Mock()
        mock_token_response.text = 'dp_AUTH_TOKEN = "Basic dGVzdHRva2VuMTIzNDU2";'
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock successful session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API response without events field
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = {"data": []}
        mock_api_get.return_value = mock_api_response
        
        exit_code = main()
        
        # Verify non-zero exit code
        self.assertEqual(exit_code, 1)

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py'])
    def test_events_with_missing_fields(self, mock_token_get, mock_session_get, mock_api_get):
        """Test handling of events with missing required fields."""
        # Mock successful token fetch
        mock_token_response = Mock()
        mock_token_response.text = 'dp_AUTH_TOKEN = "Basic dGVzdHRva2VuMTIzNDU2";'
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock successful session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API response with some events missing fields
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = {
            "events": [
                {"title": "Missing Location"},  # Missing location field
                {
                    "location": {"title": "Brownwood Paddock Square"},
                    "title": "Valid Event"
                },
                {"location": {"title": "Sawgrass Grove"}}  # Missing title field
            ]
        }
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code is still 0 (graceful handling)
        self.assertEqual(exit_code, 0)
        
        # Verify only valid event is in output
        self.assertIn("Brownwood,Valid Event", output)

    @patch('sys.argv', ['villages_events.py', '--format', 'invalid'])
    def test_invalid_format_argument(self):
        """Test error handling for invalid format argument."""
        # Capture stderr
        captured_error = StringIO()
        sys.stderr = captured_error
        
        try:
            exit_code = main()
        finally:
            sys.stderr = sys.__stderr__
        
        # Verify exit code 2 for invalid arguments
        self.assertEqual(exit_code, 2)


class TestIntegrationDateRange(unittest.TestCase):
    """Integration tests for date range parameter."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_js_content = 'dp_AUTH_TOKEN = "Basic dGVzdHRva2VuMTIzNDU2";'
        self.mock_api_response = {
            "events": [
                {
                    "location": {"title": "Brownwood Paddock Square"},
                    "title": "Test Event"
                }
            ]
        }

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--date-range', 'this-week'])
    def test_date_range_this_week(self, mock_token_get, mock_session_get, mock_api_get):
        """Test pipeline with 'this-week' date range."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify output contains event
        self.assertIn("Brownwood,Test Event", output)
        
        # Verify API was called with correct date range
        api_call_args = mock_api_get.call_args
        self.assertIn("dateRange=this-week", api_call_args[0][0])

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--date-range', 'all'])
    def test_date_range_all(self, mock_token_get, mock_session_get, mock_api_get):
        """Test pipeline with 'all' date range (no date filter)."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify API was called without dateRange parameter
        api_call_args = mock_api_get.call_args
        self.assertNotIn("dateRange", api_call_args[0][0])

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--date-range', 'tomorrow', '--format', 'json'])
    def test_date_range_with_format(self, mock_token_get, mock_session_get, mock_api_get):
        """Test date range combined with format parameter."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify JSON output
        parsed = json.loads(output)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["location.title"], "Brownwood")
        
        # Verify API was called with correct date range
        api_call_args = mock_api_get.call_args
        self.assertIn("dateRange=tomorrow", api_call_args[0][0])

    @patch('sys.argv', ['villages_events.py', '--date-range', 'invalid-range'])
    def test_invalid_date_range_argument(self):
        """Test error handling for invalid date range argument."""
        exit_code = main()
        
        # Verify exit code 2 for invalid arguments
        self.assertEqual(exit_code, 2)


class TestIntegrationCategory(unittest.TestCase):
    """Integration tests for category parameter."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_js_content = 'dp_AUTH_TOKEN = "Basic dGVzdHRva2VuMTIzNDU2";'
        self.mock_api_response = {
            "events": [
                {
                    "location": {"title": "Brownwood Paddock Square"},
                    "title": "Test Event"
                }
            ]
        }

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--category', 'sports'])
    def test_category_sports(self, mock_token_get, mock_session_get, mock_api_get):
        """Test pipeline with 'sports' category."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify output contains event
        self.assertIn("Brownwood,Test Event", output)
        
        # Verify API was called with correct category
        api_call_args = mock_api_get.call_args
        self.assertIn("categories=sports", api_call_args[0][0])

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--category', 'all'])
    def test_category_all(self, mock_token_get, mock_session_get, mock_api_get):
        """Test pipeline with 'all' categories (no category filter)."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify API was called without categories parameter
        api_call_args = mock_api_get.call_args
        self.assertNotIn("categories=", api_call_args[0][0])
        self.assertIn("locationCategories=town-squares", api_call_args[0][0])

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch(
        'sys.argv',
        ['villages_events.py', '--date-range', 'next-week', '--category', 'recreation', '--format', 'json']
    )
    def test_category_with_date_range_and_format(
        self, mock_token_get, mock_session_get, mock_api_get
    ):
        """Test category combined with date range and format parameters."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify JSON output
        parsed = json.loads(output)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["location.title"], "Brownwood")
        
        # Verify API was called with correct parameters
        api_call_args = mock_api_get.call_args
        self.assertIn("dateRange=next-week", api_call_args[0][0])
        self.assertIn("categories=recreation", api_call_args[0][0])

    @patch('sys.argv', ['villages_events.py', '--category', 'invalid-category'])
    def test_invalid_category_argument(self):
        """Test error handling for invalid category argument."""
        exit_code = main()
        
        # Verify exit code 2 for invalid arguments
        self.assertEqual(exit_code, 2)


class TestIntegrationLocation(unittest.TestCase):
    """Integration tests for location parameter."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_js_content = 'dp_AUTH_TOKEN = "Basic dGVzdHRva2VuMTIzNDU2";'
        self.mock_api_response = {
            "events": [
                {
                    "location": {"title": "Brownwood Paddock Square"},
                    "title": "Test Event"
                }
            ]
        }

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--location', 'Brownwood+Paddock+Square'])
    def test_location_brownwood(self, mock_token_get, mock_session_get, mock_api_get):
        """Test pipeline with 'Brownwood+Paddock+Square' location."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify output contains event
        self.assertIn("Brownwood,Test Event", output)
        
        # Verify API was called with correct location
        api_call_args = mock_api_get.call_args
        self.assertIn("locationCategories=Brownwood+Paddock+Square", api_call_args[0][0])

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--location', 'all'])
    def test_location_all(self, mock_token_get, mock_session_get, mock_api_get):
        """Test pipeline with 'all' locations (no location filter)."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify API was called without locationCategories parameter
        api_call_args = mock_api_get.call_args
        self.assertNotIn("locationCategories", api_call_args[0][0])

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch(
        'sys.argv',
        ['villages_events.py', '--date-range', 'next-week', '--category', 'sports', 
         '--location', 'sports-recreation', '--format', 'json']
    )
    def test_location_with_all_filters(
        self, mock_token_get, mock_session_get, mock_api_get
    ):
        """Test location combined with all other parameters."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify JSON output
        parsed = json.loads(output)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["location.title"], "Brownwood")
        
        # Verify API was called with correct parameters
        api_call_args = mock_api_get.call_args
        self.assertIn("dateRange=next-week", api_call_args[0][0])
        self.assertIn("categories=sports", api_call_args[0][0])
        self.assertIn("locationCategories=sports-recreation", api_call_args[0][0])

    @patch('sys.argv', ['villages_events.py', '--location', 'invalid-location'])
    def test_invalid_location_argument(self):
        """Test error handling for invalid location argument."""
        exit_code = main()
        
        # Verify exit code 2 for invalid arguments
        self.assertEqual(exit_code, 2)


class TestIntegrationRawOutput(unittest.TestCase):
    """Integration tests for raw output option."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_js_content = 'dp_AUTH_TOKEN = "Basic dGVzdHRva2VuMTIzNDU2";'
        self.mock_api_response = {
            "events": [
                {
                    "location": {"title": "Brownwood Paddock Square"},
                    "title": "Test Event",
                    "extra_field": "extra_data"
                }
            ],
            "metadata": {
                "total": 1,
                "page": 1
            }
        }

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--raw'])
    def test_raw_output(self, mock_token_get, mock_session_get, mock_api_get):
        """Test raw output returns unprocessed API response."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify output is valid JSON
        parsed = json.loads(output)
        
        # Verify raw output contains all fields
        self.assertIn("events", parsed)
        self.assertIn("metadata", parsed)
        self.assertEqual(parsed["events"][0]["extra_field"], "extra_data")
        self.assertEqual(parsed["metadata"]["total"], 1)

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--raw', '--format', 'csv'])
    def test_raw_output_ignores_format(self, mock_token_get, mock_session_get, mock_api_get):
        """Test that raw output ignores format parameter."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify output is JSON (not CSV), proving --format is ignored
        parsed = json.loads(output)
        self.assertIn("events", parsed)


if __name__ == '__main__':
    unittest.main()


class TestIntegrationConfigurableFields(unittest.TestCase):
    """Integration tests for configurable output fields feature."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_js_content = 'dp_AUTH_TOKEN = "Basic dGVzdHRva2VuMTIzNDU2";'
        self.mock_api_response = {
            "events": [
                {
                    "location": {"title": "Brownwood Paddock Square", "category": "town-square"},
                    "title": "Jazz Band",
                    "description": "Live jazz performance",
                    "category": "entertainment",
                    "start": {"date": "2025-11-14T22:00:00.000Z"},
                    "end": {"date": "2025-11-14T23:30:00.000Z"},
                    "address": {
                        "streetAddress": "123 Main St",
                        "locality": "The Villages",
                        "region": "FL",
                        "postalCode": "32162"
                    },
                    "url": "https://example.com/event1"
                },
                {
                    "location": {"title": "Spanish Springs Town Square", "category": "town-square"},
                    "title": "Rock Group",
                    "description": "Rock concert",
                    "category": "entertainment",
                    "start": {"date": "2025-11-15T20:00:00.000Z"},
                    "end": {"date": "2025-11-15T22:00:00.000Z"},
                    "address": {
                        "streetAddress": "456 Oak Ave",
                        "locality": "The Villages",
                        "region": "FL",
                        "postalCode": "32163"
                    },
                    "url": "https://example.com/event2"
                }
            ]
        }

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--fields', 'location.title,title,start.date'])
    def test_custom_fields_meshtastic_format(self, mock_token_get, mock_session_get, mock_api_get):
        """Test custom fields with Meshtastic format (uses first two fields)."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify output uses first two fields (location.title and title)
        self.assertIn("Brownwood,Jazz Band", output)
        self.assertIn("Spanish Springs,Rock Group", output)

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--fields', 'title,start.date,location.title', '--format', 'json'])
    def test_custom_fields_json_format(self, mock_token_get, mock_session_get, mock_api_get):
        """Test custom fields with JSON format (includes all specified fields)."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify JSON output contains all three fields
        parsed = json.loads(output)
        self.assertEqual(len(parsed), 2)
        
        # Check first event
        self.assertIn("title", parsed[0])
        self.assertIn("start.date", parsed[0])
        self.assertIn("location.title", parsed[0])
        self.assertEqual(parsed[0]["title"], "Jazz Band")
        self.assertEqual(parsed[0]["start.date"], "2025-11-14T22:00:00.000Z")
        self.assertEqual(parsed[0]["location.title"], "Brownwood")
        
        # Check second event
        self.assertEqual(parsed[1]["title"], "Rock Group")
        self.assertEqual(parsed[1]["start.date"], "2025-11-15T20:00:00.000Z")
        self.assertEqual(parsed[1]["location.title"], "Spanish Springs")

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--fields', 'location.title,title,description,url', '--format', 'csv'])
    def test_custom_fields_csv_format(self, mock_token_get, mock_session_get, mock_api_get):
        """Test custom fields with CSV format."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify CSV output
        lines = [line.strip() for line in output.strip().split('\n')]
        
        # Check header
        self.assertEqual(lines[0], "location.title,title,description,url")
        
        # Check data rows
        self.assertIn("Brownwood,Jazz Band,Live jazz performance,https://example.com/event1", lines[1])
        self.assertIn("Spanish Springs,Rock Group,Rock concert,https://example.com/event2", lines[2])

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--fields', 'title,location.title,start.date', '--format', 'plain'])
    def test_custom_fields_plain_format(self, mock_token_get, mock_session_get, mock_api_get):
        """Test custom fields with plain text format."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify plain text output
        self.assertIn("title: Jazz Band, location.title: Brownwood, start.date: 2025-11-14T22:00:00.000Z", output)
        self.assertIn("title: Rock Group, location.title: Spanish Springs, start.date: 2025-11-15T20:00:00.000Z", output)

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--fields', 'location.title,title,address.streetAddress,address.locality', '--format', 'json'])
    def test_nested_fields_extraction(self, mock_token_get, mock_session_get, mock_api_get):
        """Test extraction of nested fields using dot notation."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify nested fields are extracted correctly
        parsed = json.loads(output)
        self.assertEqual(len(parsed), 2)
        
        # Check first event
        self.assertEqual(parsed[0]["address.streetAddress"], "123 Main St")
        self.assertEqual(parsed[0]["address.locality"], "The Villages")
        
        # Check second event
        self.assertEqual(parsed[1]["address.streetAddress"], "456 Oak Ave")
        self.assertEqual(parsed[1]["address.locality"], "The Villages")

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py'])
    def test_backward_compatibility_default_fields(self, mock_token_get, mock_session_get, mock_api_get):
        """Test backward compatibility with default fields when no --fields specified."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify default format (meshtastic) with default fields (location.title, title)
        expected = "Brownwood,Jazz Band#Spanish Springs,Rock Group#"
        self.assertEqual(output, expected)

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--fields', 'title,nonexistent.field,location.title', '--format', 'json'])
    def test_invalid_fields_handling(self, mock_token_get, mock_session_get, mock_api_get):
        """Test handling of invalid field names (should warn and filter them out)."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code is still 0 (graceful handling)
        self.assertEqual(exit_code, 0)
        
        # Verify output only contains valid fields (invalid fields are filtered out)
        parsed = json.loads(output)
        self.assertEqual(len(parsed), 2)
        self.assertIn("title", parsed[0])
        self.assertIn("location.title", parsed[0])
        # nonexistent.field should not be in output
        self.assertNotIn("nonexistent.field", parsed[0])

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--fields', 'title,description', '--format', 'json'])
    def test_missing_fields_in_events(self, mock_token_get, mock_session_get, mock_api_get):
        """Test handling of events where some specified fields are missing."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API response with some events missing description field
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = {
            "events": [
                {
                    "title": "Event with description",
                    "description": "This event has a description"
                },
                {
                    "title": "Event without description"
                    # description field is missing
                }
            ]
        }
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify both events are in output
        parsed = json.loads(output)
        self.assertEqual(len(parsed), 2)
        
        # First event should have description
        self.assertEqual(parsed[0]["title"], "Event with description")
        self.assertEqual(parsed[0]["description"], "This event has a description")
        
        # Second event should have empty string for missing description
        self.assertEqual(parsed[1]["title"], "Event without description")
        self.assertEqual(parsed[1]["description"], "")

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--fields', 'title,location.title,category', '--format', 'json'])
    def test_venue_abbreviation_only_on_location_title(self, mock_token_get, mock_session_get, mock_api_get):
        """Test that venue abbreviation is only applied to location.title field."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API response with "Brownwood" in multiple fields
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = {
            "events": [
                {
                    "location": {"title": "Brownwood Paddock Square"},
                    "title": "Brownwood Artist",
                    "category": "Brownwood entertainment"
                }
            ]
        }
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify venue abbreviation only applied to location.title
        parsed = json.loads(output)
        self.assertEqual(len(parsed), 1)
        
        # location.title should be abbreviated
        self.assertEqual(parsed[0]["location.title"], "Brownwood")
        
        # title and category should NOT be abbreviated
        self.assertEqual(parsed[0]["title"], "Brownwood Artist")
        self.assertEqual(parsed[0]["category"], "Brownwood entertainment")

    @patch('src.api_client.requests.Session.get')
    @patch('src.session_manager.requests.Session.get')
    @patch('src.token_fetcher.requests.get')
    @patch('sys.argv', ['villages_events.py', '--fields', 'title,start.date,end.date,category', '--format', 'csv'])
    def test_multiple_nested_fields(self, mock_token_get, mock_session_get, mock_api_get):
        """Test extraction of multiple nested fields from different objects."""
        # Mock token fetch
        mock_token_response = Mock()
        mock_token_response.text = self.mock_js_content
        mock_token_response.raise_for_status = Mock()
        mock_token_get.return_value = mock_token_response
        
        # Mock session establishment
        mock_session_response = Mock()
        mock_session_response.raise_for_status = Mock()
        mock_session_get.return_value = mock_session_response
        
        # Mock API request
        mock_api_response = Mock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = self.mock_api_response
        mock_api_get.return_value = mock_api_response
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            exit_code = main()
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        
        # Verify exit code
        self.assertEqual(exit_code, 0)
        
        # Verify CSV output with multiple nested fields
        lines = [line.strip() for line in output.strip().split('\n')]
        
        # Check header
        self.assertEqual(lines[0], "title,start.date,end.date,category")
        
        # Check data rows contain nested field values
        self.assertIn("Jazz Band,2025-11-14T22:00:00.000Z,2025-11-14T23:30:00.000Z,entertainment", lines[1])
        self.assertIn("Rock Group,2025-11-15T20:00:00.000Z,2025-11-15T22:00:00.000Z,entertainment", lines[2])
