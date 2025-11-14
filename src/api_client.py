"""API client module for Villages Event Scraper.

This module handles authenticated requests to The Villages API
and validates responses.
"""

import requests
from typing import Dict, Any

from .exceptions import APIError
from .config import Config


def fetch_events(
    session: requests.Session,
    api_url: str,
    auth_token: str,
    timeout: int = Config.DEFAULT_TIMEOUT
) -> Dict[str, Any]:
    """Fetches events from The Villages API.
    
    Args:
        session: Active requests session with cookies
        api_url: Full API endpoint URL with query parameters
        auth_token: Authorization token in format "Basic <base64>"
        timeout: Request timeout in seconds
        
    Returns:
        Parsed JSON response as dictionary
        
    Raises:
        APIError: If request fails or response is invalid
    """
    try:
        # Prepare headers with authorization
        # Extract date range from API URL to use in Referer
        # For simplicity, use a generic calendar URL as referer
        headers = {
            'Authorization': auth_token,
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': Config.USER_AGENT,
            'Origin': 'https://www.thevillages.com',
            'Referer': 'https://www.thevillages.com/calendar/',
        }
        
        # Make authenticated GET request
        response = session.get(api_url, headers=headers, timeout=timeout)
        
        # Validate HTTP response status code
        if response.status_code != 200:
            raise APIError(
                f"API request failed with status code {response.status_code}: "
                f"{response.text[:200]}"
            )
        
        # Parse JSON response
        try:
            data = response.json()
        except ValueError as e:
            raise APIError(f"Failed to parse JSON response: {e}")
        
        # Validate response structure - ensure it's a dictionary
        if not isinstance(data, dict):
            raise APIError(
                f"Invalid API response structure: expected dict, got {type(data).__name__}"
            )
        
        return data
        
    except requests.exceptions.Timeout as e:
        raise APIError(f"API request timed out after {timeout} seconds: {e}")
    except requests.exceptions.RequestException as e:
        raise APIError(f"API request failed: {e}")
