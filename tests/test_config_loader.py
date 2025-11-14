"""Unit tests for config_loader module."""

import unittest
import os
import tempfile
from src.config_loader import ConfigLoader


class TestConfigLoader(unittest.TestCase):
    """Test cases for configuration loader functionality."""

    def test_load_config_file_not_exists(self):
        """Test loading config when file doesn't exist."""
        config = ConfigLoader.load_config('nonexistent.yaml')
        self.assertEqual(config, {})

    def test_load_config_valid_yaml(self):
        """Test loading valid YAML configuration."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('format: json\n')
            f.write('date_range: tomorrow\n')
            f.write('category: sports\n')
            temp_file = f.name
        
        try:
            config = ConfigLoader.load_config(temp_file)
            self.assertEqual(config['format'], 'json')
            self.assertEqual(config['date_range'], 'tomorrow')
            self.assertEqual(config['category'], 'sports')
        finally:
            os.unlink(temp_file)

    def test_load_config_invalid_yaml(self):
        """Test loading invalid YAML returns empty dict."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('invalid: yaml: content:\n')
            f.write('  - broken\n')
            f.write('  bad indentation\n')
            temp_file = f.name
        
        try:
            config = ConfigLoader.load_config(temp_file)
            self.assertEqual(config, {})
        finally:
            os.unlink(temp_file)

    def test_load_config_empty_file(self):
        """Test loading empty YAML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_file = f.name
        
        try:
            config = ConfigLoader.load_config(temp_file)
            self.assertEqual(config, {})
        finally:
            os.unlink(temp_file)

    def test_load_config_with_venue_mappings(self):
        """Test loading config with venue mappings."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('venue_mappings:\n')
            f.write('  Brownwood: BW\n')
            f.write('  Sawgrass: SG\n')
            temp_file = f.name
        
        try:
            config = ConfigLoader.load_config(temp_file)
            self.assertIn('venue_mappings', config)
            self.assertEqual(config['venue_mappings']['Brownwood'], 'BW')
            self.assertEqual(config['venue_mappings']['Sawgrass'], 'SG')
        finally:
            os.unlink(temp_file)

    def test_get_default_key_exists(self):
        """Test getting value when key exists."""
        config = {'format': 'json', 'timeout': 20}
        value = ConfigLoader.get_default(config, 'format', 'meshtastic')
        self.assertEqual(value, 'json')

    def test_get_default_key_not_exists(self):
        """Test getting fallback when key doesn't exist."""
        config = {'format': 'json'}
        value = ConfigLoader.get_default(config, 'category', 'entertainment')
        self.assertEqual(value, 'entertainment')

    def test_get_default_empty_config(self):
        """Test getting fallback from empty config."""
        config = {}
        value = ConfigLoader.get_default(config, 'format', 'meshtastic')
        self.assertEqual(value, 'meshtastic')

    def test_load_config_with_timeout(self):
        """Test loading config with timeout setting."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('timeout: 30\n')
            temp_file = f.name
        
        try:
            config = ConfigLoader.load_config(temp_file)
            self.assertEqual(config['timeout'], 30)
        finally:
            os.unlink(temp_file)

    def test_get_output_fields_from_config(self):
        """Test getting output_fields from config."""
        config = {'output_fields': ['title', 'location.title', 'start.date']}
        fallback = ['location.title', 'title']
        fields = ConfigLoader.get_output_fields(config, fallback)
        self.assertEqual(fields, ['title', 'location.title', 'start.date'])

    def test_get_output_fields_fallback(self):
        """Test getting output_fields fallback when not in config."""
        config = {'format': 'json'}
        fallback = ['location.title', 'title']
        fields = ConfigLoader.get_output_fields(config, fallback)
        self.assertEqual(fields, fallback)

    def test_get_output_fields_invalid_type(self):
        """Test getting output_fields when config has invalid type."""
        config = {'output_fields': 'not-a-list'}
        fallback = ['location.title', 'title']
        fields = ConfigLoader.get_output_fields(config, fallback)
        self.assertEqual(fields, fallback)

    def test_get_output_fields_non_string_items(self):
        """Test getting output_fields when list contains non-strings."""
        config = {'output_fields': ['title', 123, 'location.title']}
        fallback = ['location.title', 'title']
        fields = ConfigLoader.get_output_fields(config, fallback)
        self.assertEqual(fields, fallback)

    def test_load_config_with_output_fields(self):
        """Test loading config with output_fields setting."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('output_fields:\n')
            f.write('  - location.title\n')
            f.write('  - title\n')
            f.write('  - start.date\n')
            temp_file = f.name
        
        try:
            config = ConfigLoader.load_config(temp_file)
            self.assertIn('output_fields', config)
            self.assertEqual(config['output_fields'], ['location.title', 'title', 'start.date'])
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    unittest.main()
