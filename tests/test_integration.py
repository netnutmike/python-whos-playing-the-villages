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
        self.assertEqual(parsed[0]["venue"], "Brownwood")
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
        self.assertEqual(lines[0], "venue,title")
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
        self.assertIn("Brownwood: Jazz Band", output)
        self.assertIn("Spanish Springs: Rock Group", output)

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
        self.assertEqual(parsed[0]["venue"], "Brownwood")
        
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
        self.assertEqual(parsed[0]["venue"], "Brownwood")
        
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
        self.assertEqual(parsed[0]["venue"], "Brownwood")
        
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
