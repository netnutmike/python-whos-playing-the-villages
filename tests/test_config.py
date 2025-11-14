"""Unit tests for config module."""

import unittest
from src.config import Config


class TestConfig(unittest.TestCase):
    """Test cases for configuration functionality."""

    def test_valid_date_ranges(self):
        """Test that all valid date ranges are defined."""
        expected_ranges = [
            "today",
            "tomorrow",
            "this-week",
            "next-week",
            "this-month",
            "next-month",
            "all",
        ]
        self.assertEqual(Config.VALID_DATE_RANGES, expected_ranges)

    def test_default_date_range(self):
        """Test default date range is 'today'."""
        self.assertEqual(Config.DEFAULT_DATE_RANGE, "today")

    def test_valid_categories(self):
        """Test that all valid categories are defined."""
        expected_categories = [
            "entertainment",
            "arts-and-crafts",
            "health-and-wellness",
            "recreation",
            "social-clubs",
            "special-events",
            "sports",
            "all",
        ]
        self.assertEqual(Config.VALID_CATEGORIES, expected_categories)

    def test_default_category(self):
        """Test default category is 'entertainment'."""
        self.assertEqual(Config.DEFAULT_CATEGORY, "entertainment")

    def test_valid_locations(self):
        """Test that all valid locations are defined."""
        expected_locations = [
            "town-squares",
            "Lake+Sumter+Landing+Market+Square",
            "Spanish+Springs+Town+Square",
            "Brownwood+Paddock+Square",
            "Sawgrass+Grove",
            "The+Show+Kitchen+at+Sawgrass+Grove",
            "entertainment",
            "The+Sharon",
            "The+Studio+Theatre+at+Tierra+Del+Sol",
            "sports-recreation",
            "Savannah+Recreation",
            "sports",
            "executive-golf",
            "Polo+Club",
            "all",
        ]
        self.assertEqual(Config.VALID_LOCATIONS, expected_locations)

    def test_default_location(self):
        """Test default location is 'town-squares'."""
        self.assertEqual(Config.DEFAULT_LOCATION, "town-squares")

    def test_get_calendar_url_today(self):
        """Test calendar URL generation for 'today'."""
        url = Config.get_calendar_url("today")
        self.assertIn("dateRange=today", url)
        self.assertIn("categories=entertainment", url)
        self.assertIn("locationCategories=town-squares", url)

    def test_get_calendar_url_this_week(self):
        """Test calendar URL generation for 'this-week'."""
        url = Config.get_calendar_url("this-week")
        self.assertIn("dateRange=this-week", url)

    def test_get_calendar_url_all_dates(self):
        """Test calendar URL generation for 'all' dates (no date range)."""
        url = Config.get_calendar_url("all")
        self.assertNotIn("dateRange", url)
        self.assertIn("categories=entertainment", url)

    def test_get_calendar_url_with_category(self):
        """Test calendar URL generation with specific category."""
        url = Config.get_calendar_url("today", "sports")
        self.assertIn("dateRange=today", url)
        self.assertIn("categories=sports", url)

    def test_get_calendar_url_all_categories(self):
        """Test calendar URL generation for 'all' categories (no category filter)."""
        url = Config.get_calendar_url("today", "all")
        self.assertIn("dateRange=today", url)
        self.assertNotIn("categories=", url)
        self.assertIn("locationCategories=town-squares", url)

    def test_get_calendar_url_all_dates_and_categories(self):
        """Test calendar URL generation with no date or category filters."""
        url = Config.get_calendar_url("all", "all")
        self.assertNotIn("dateRange", url)
        self.assertNotIn("categories=", url)
        self.assertIn("locationCategories=town-squares", url)

    def test_get_api_url_today(self):
        """Test API URL generation for 'today'."""
        url = Config.get_api_url("today")
        self.assertIn("dateRange=today", url)
        self.assertIn("categories=entertainment", url)
        self.assertIn("cancelled=false", url)

    def test_get_api_url_next_month(self):
        """Test API URL generation for 'next-month'."""
        url = Config.get_api_url("next-month")
        self.assertIn("dateRange=next-month", url)

    def test_get_api_url_all_dates(self):
        """Test API URL generation for 'all' dates (no date range)."""
        url = Config.get_api_url("all")
        self.assertNotIn("dateRange", url)
        self.assertIn("categories=entertainment", url)

    def test_get_api_url_with_category(self):
        """Test API URL generation with specific category."""
        url = Config.get_api_url("today", "recreation")
        self.assertIn("dateRange=today", url)
        self.assertIn("categories=recreation", url)

    def test_get_api_url_all_categories(self):
        """Test API URL generation for 'all' categories (no category filter)."""
        url = Config.get_api_url("today", "all")
        self.assertIn("dateRange=today", url)
        self.assertNotIn("categories=", url)
        self.assertIn("locationCategories=town-squares", url)

    def test_get_api_url_all_dates_and_categories(self):
        """Test API URL generation with no date or category filters."""
        url = Config.get_api_url("all", "all")
        self.assertNotIn("dateRange", url)
        self.assertNotIn("categories=", url)
        self.assertIn("locationCategories=town-squares", url)

    def test_get_calendar_url_with_location(self):
        """Test calendar URL generation with specific location."""
        url = Config.get_calendar_url("today", "entertainment", "Brownwood+Paddock+Square")
        self.assertIn("dateRange=today", url)
        self.assertIn("categories=entertainment", url)
        self.assertIn("locationCategories=Brownwood+Paddock+Square", url)

    def test_get_calendar_url_all_locations(self):
        """Test calendar URL generation for 'all' locations (no location filter)."""
        url = Config.get_calendar_url("today", "entertainment", "all")
        self.assertIn("dateRange=today", url)
        self.assertIn("categories=entertainment", url)
        self.assertNotIn("locationCategories", url)

    def test_get_calendar_url_all_filters(self):
        """Test calendar URL generation with all filters set to 'all'."""
        url = Config.get_calendar_url("all", "all", "all")
        self.assertNotIn("dateRange", url)
        self.assertNotIn("categories=", url)
        self.assertNotIn("locationCategories", url)

    def test_get_api_url_with_location(self):
        """Test API URL generation with specific location."""
        url = Config.get_api_url("today", "entertainment", "Spanish+Springs+Town+Square")
        self.assertIn("dateRange=today", url)
        self.assertIn("categories=entertainment", url)
        self.assertIn("locationCategories=Spanish+Springs+Town+Square", url)

    def test_get_api_url_all_locations(self):
        """Test API URL generation for 'all' locations (no location filter)."""
        url = Config.get_api_url("today", "entertainment", "all")
        self.assertIn("dateRange=today", url)
        self.assertIn("categories=entertainment", url)
        self.assertNotIn("locationCategories", url)

    def test_get_api_url_all_filters(self):
        """Test API URL generation with all filters set to 'all'."""
        url = Config.get_api_url("all", "all", "all")
        self.assertNotIn("dateRange", url)
        self.assertNotIn("categories=", url)
        self.assertNotIn("locationCategories", url)
        self.assertIn("subcategoriesQueryType=and", url)

    def test_get_calendar_url_default(self):
        """Test calendar URL generation with default parameters."""
        url = Config.get_calendar_url()
        self.assertIn("dateRange=today", url)
        self.assertIn("categories=entertainment", url)
        self.assertIn("locationCategories=town-squares", url)

    def test_get_api_url_default(self):
        """Test API URL generation with default parameters."""
        url = Config.get_api_url()
        self.assertIn("dateRange=today", url)
        self.assertIn("categories=entertainment", url)
        self.assertIn("locationCategories=town-squares", url)


if __name__ == '__main__':
    unittest.main()
