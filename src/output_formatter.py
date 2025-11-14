"""Output formatting module for event data."""

import json
import csv
import io


class OutputFormatter:
    """Formats event data for output in various formats."""

    @staticmethod
    def format_meshtastic(events: list[tuple[str, str]]) -> str:
        """
        Formats events in Meshtastic format.
        
        Format: venue1,title1#venue2,title2#
        
        Args:
            events: List of (venue, title) tuples
            
        Returns:
            Formatted string with # delimiters
        """
        if not events:
            return "#"
        
        formatted_parts = [f"{venue},{title}" for venue, title in events]
        return "#".join(formatted_parts) + "#"

    @staticmethod
    def format_json(events: list[tuple[str, str]]) -> str:
        """
        Formats events as JSON array.
        
        Format: [{"venue": "...", "title": "..."}, ...]
        
        Args:
            events: List of (venue, title) tuples
            
        Returns:
            JSON string
        """
        event_objects = [
            {"venue": venue, "title": title}
            for venue, title in events
        ]
        return json.dumps(event_objects, indent=2)

    @staticmethod
    def format_csv(events: list[tuple[str, str]]) -> str:
        """
        Formats events as CSV with headers.
        
        Format: venue,title\nVenue1,Title1\n...
        
        Args:
            events: List of (venue, title) tuples
            
        Returns:
            CSV formatted string with headers
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(["venue", "title"])
        
        # Write event rows
        for venue, title in events:
            writer.writerow([venue, title])
        
        return output.getvalue()

    @staticmethod
    def format_plain(events: list[tuple[str, str]]) -> str:
        """
        Formats events as plain text, one per line.
        
        Format: venue: title\n...
        
        Args:
            events: List of (venue, title) tuples
            
        Returns:
            Plain text string with one event per line
        """
        if not events:
            return ""
        
        lines = [f"{venue}: {title}" for venue, title in events]
        return "\n".join(lines) + "\n"

    @staticmethod
    def format_events(
        events: list[tuple[str, str]],
        format_type: str = "meshtastic"
    ) -> str:
        """
        Formats events according to specified format type.
        
        Args:
            events: List of (venue, title) tuples
            format_type: One of "meshtastic", "json", "csv", "plain"
            
        Returns:
            Formatted string ready for output
            
        Raises:
            ValueError: If format_type is not recognized
        """
        formatters = {
            "meshtastic": OutputFormatter.format_meshtastic,
            "json": OutputFormatter.format_json,
            "csv": OutputFormatter.format_csv,
            "plain": OutputFormatter.format_plain,
        }
        
        if format_type not in formatters:
            raise ValueError(
                f"Invalid format type: {format_type}. "
                f"Valid options are: {', '.join(formatters.keys())}"
            )
        
        return formatters[format_type](events)
