"""Output formatting module for event data."""

import json
import csv
import io
from typing import Any


class OutputFormatter:
    """Formats event data for output in various formats."""

    @staticmethod
    def format_meshtastic(events: list[dict[str, Any]], field_names: list[str]) -> str:
        """
        Formats events in Meshtastic format using first two fields.
        
        Format: field1_value,field2_value#field1_value,field2_value#
        
        Args:
            events: List of event dictionaries with extracted fields
            field_names: List of field names (uses first two fields)
            
        Returns:
            Formatted string with # delimiters
        """
        if not events:
            return "#"
        
        # Use first two fields for meshtastic format
        fields_to_use = field_names[:2] if len(field_names) >= 2 else field_names
        
        formatted_parts = []
        for event in events:
            values = [str(event.get(field, "")) for field in fields_to_use]
            formatted_parts.append(",".join(values))
        
        return "#".join(formatted_parts) + "#"

    @staticmethod
    def format_json(events: list[dict[str, Any]]) -> str:
        """
        Formats events as JSON array with all specified fields.
        
        Format: [{"field1": "...", "field2": "..."}, ...]
        
        Args:
            events: List of event dictionaries with extracted fields
            
        Returns:
            JSON string
        """
        return json.dumps(events, indent=2)

    @staticmethod
    def format_csv(events: list[dict[str, Any]], field_names: list[str]) -> str:
        """
        Formats events as CSV with headers for all fields.
        
        Format: field1,field2\nValue1,Value2\n...
        
        Args:
            events: List of event dictionaries with extracted fields
            field_names: List of field names for headers
            
        Returns:
            CSV formatted string with headers
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(field_names)
        
        # Write event rows
        for event in events:
            row = [event.get(field, "") for field in field_names]
            writer.writerow(row)
        
        return output.getvalue()

    @staticmethod
    def format_plain(events: list[dict[str, Any]], field_names: list[str]) -> str:
        """
        Formats events as plain text with all fields.
        
        Format: field1: value1, field2: value2\n...
        
        Args:
            events: List of event dictionaries with extracted fields
            field_names: List of field names to display
            
        Returns:
            Plain text string with one event per line
        """
        if not events:
            return ""
        
        lines = []
        for event in events:
            field_parts = [f"{field}: {event.get(field, '')}" for field in field_names]
            lines.append(", ".join(field_parts))
        
        return "\n".join(lines) + "\n"

    @staticmethod
    def format_events(
        events: list[dict[str, Any]],
        format_type: str = "meshtastic",
        field_names: list[str] = None
    ) -> str:
        """
        Formats events according to specified format type.
        
        Args:
            events: List of event dictionaries with extracted fields
            format_type: One of "meshtastic", "json", "csv", "plain"
            field_names: List of field names for ordering (used for CSV headers and plain text)
            
        Returns:
            Formatted string ready for output
            
        Raises:
            ValueError: If format_type is not recognized
        """
        if field_names is None:
            field_names = ["location.title", "title"]
        
        if format_type == "meshtastic":
            return OutputFormatter.format_meshtastic(events, field_names)
        elif format_type == "json":
            return OutputFormatter.format_json(events)
        elif format_type == "csv":
            return OutputFormatter.format_csv(events, field_names)
        elif format_type == "plain":
            return OutputFormatter.format_plain(events, field_names)
        else:
            raise ValueError(
                f"Invalid format type: {format_type}. "
                f"Valid options are: meshtastic, json, csv, plain"
            )
