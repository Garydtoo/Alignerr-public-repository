Python
"""
Data Parser Module
Provides functionality to parse, validate, and extract payload structures.
"""

from typing import Any, Dict, Optional


class ParsingError(Exception):
    """Custom exception raised when payload parsing or validation fails."""
    pass


class PayloadParser:
    """Handles parsing and structural extraction for raw data payloads."""

    def __init__(self, strict_mode: bool = False) -> None:
        """
        Initialize the parser.

        :param strict_mode: If True, missing required fields will raise ParsingError.
        """
        self.strict_mode = strict_mode

    def parse_payload(self, data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Parses an incoming raw payload dictionary and returns normalized data.

        :param data: The raw input dictionary to parse.
        :return: Normalized dictionary containing parsed values.
        :raises ParsingError: If input is invalid or missing required keys in strict mode.
        """
        if data is None:
            if self.strict_mode:
                raise ParsingError("Payload cannot be None.")
            return {}

        if not isinstance(data, dict):
            raise ParsingError(f"Expected dict, got {type(data).__name__}")

        # Example extraction logic for downstream evaluation tasks
        parsed_result = {
            "id": str(data.get("id", "")).strip(),
            "status": str(data.get("status", "unknown")).lower(),
            "meta": data.get("meta", {}),
        }

        if self.strict_mode and not parsed_result["id"]:
            raise ParsingError("Payload missing required 'id' field.")

        return parsed_result


if __name__ == "__main__":
    # Example usage / sanity check
    parser = PayloadParser(strict_mode=False)
    sample_data = {"id": "101", "status": "ACTIVE", "meta": {"owner": "admin"}}
    
    try:
        result = parser.parse_payload(sample_data)
        print("Parsed Output:", result)
    except ParsingError as err:
        print(f"Parsing failed: {err}")