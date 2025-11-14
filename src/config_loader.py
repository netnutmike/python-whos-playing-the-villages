"""Configuration loader module for Villages Event Scraper.

This module handles loading configuration from YAML file and merging
with command-line arguments.
"""

import os
import yaml
from typing import Dict, Any, Optional


class ConfigLoader:
    """Loads and manages configuration from YAML file."""
    
    DEFAULT_CONFIG_FILE = "config.yaml"
    
    @staticmethod
    def load_config(config_file: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from YAML file.
        
        Args:
            config_file: Path to config file (optional, defaults to config.yaml)
            
        Returns:
            Dictionary containing configuration values
        """
        if config_file is None:
            config_file = ConfigLoader.DEFAULT_CONFIG_FILE
        
        # Return empty dict if config file doesn't exist
        if not os.path.exists(config_file):
            return {}
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config if config is not None else {}
        except yaml.YAMLError as e:
            # If YAML is invalid, print warning and return empty dict
            print(f"Warning: Invalid YAML in {config_file}: {e}", file=__import__('sys').stderr)
            return {}
        except Exception as e:
            # If file can't be read, print warning and return empty dict
            print(f"Warning: Could not read {config_file}: {e}", file=__import__('sys').stderr)
            return {}
    
    @staticmethod
    def get_default(config: Dict[str, Any], key: str, fallback: Any) -> Any:
        """Get a configuration value with fallback.
        
        Args:
            config: Configuration dictionary
            key: Configuration key
            fallback: Fallback value if key not found
            
        Returns:
            Configuration value or fallback
        """
        return config.get(key, fallback)
