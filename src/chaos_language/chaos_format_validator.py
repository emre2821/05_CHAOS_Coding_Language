"""
CHAOS file format validator with new header structure.

This module provides validation for CHAOS files using the new header format
with key-value pairs and [CONTENT BEGIN]/[CONTENT END] markers as specified
in SPEC.md.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional

from .chaos_errors import ChaosValidationError

CONTENT_BEGIN = "[CONTENT BEGIN]"
CONTENT_END = "[CONTENT END]"

# Required fields as per SPEC.md
REQUIRED_FIELDS = {"file_type", "tags"}

# Enumeration field validation
CONSENT_VALUES = {"explicit", "implicit", "none"}
SAFETY_TIER_VALUES = {"low", "med", "high"}
SENSITIVE_VALUES = {"pii", "trauma", "none"}


class ChaosHeader:
    """Represents and validates a CHAOS file header."""

    def __init__(self, headers: Dict[str, str]):
        self.headers = headers
        self._validate()

    def _validate(self) -> None:
        """Validate header fields against SPEC.md requirements."""
        # Check required fields
        missing = REQUIRED_FIELDS - set(self.headers.keys())
        if missing:
            raise ChaosValidationError(
                f"Missing required field(s): {', '.join(sorted(missing))}"
            )

        # Validate file_type is non-empty
        if not self.headers.get("file_type", "").strip():
            raise ChaosValidationError("file_type cannot be empty")

        # Validate tags is non-empty
        tags = self.headers.get("tags", "").strip()
        if not tags:
            raise ChaosValidationError("tags cannot be empty")

        # Parse tags to ensure they're valid
        tag_list = [t.strip() for t in tags.split(",")]
        if not any(tag_list):
            raise ChaosValidationError("tags must contain at least one non-empty tag")

        # Validate enumeration fields if present
        if "consent" in self.headers:
            consent = self.headers["consent"].strip()
            if consent and consent not in CONSENT_VALUES:
                raise ChaosValidationError(
                    f"Invalid consent value '{consent}'. "
                    f"Must be one of: {', '.join(sorted(CONSENT_VALUES))}"
                )

        if "safety_tier" in self.headers:
            safety_tier = self.headers["safety_tier"].strip()
            if safety_tier and safety_tier not in SAFETY_TIER_VALUES:
                raise ChaosValidationError(
                    f"Invalid safety_tier value '{safety_tier}'. "
                    f"Must be one of: {', '.join(sorted(SAFETY_TIER_VALUES))}"
                )

        if "sensitive" in self.headers:
            sensitive = self.headers["sensitive"].strip()
            if sensitive and sensitive not in SENSITIVE_VALUES:
                raise ChaosValidationError(
                    f"Invalid sensitive value '{sensitive}'. "
                    f"Must be one of: {', '.join(sorted(SENSITIVE_VALUES))}"
                )

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a header value."""
        return self.headers.get(key, default)

    def __getitem__(self, key: str) -> str:
        """Get a header value by key."""
        return self.headers[key]

    def __contains__(self, key: str) -> bool:
        """Check if a header key exists."""
        return key in self.headers


def parse_chaos_file(path: Path) -> tuple[ChaosHeader, str]:
    """
    Parse a CHAOS file with new format.

    Parameters
    ----------
    path : Path
        Path to the CHAOS file

    Returns
    -------
    tuple[ChaosHeader, str]
        Parsed header and content

    Raises
    ------
    ChaosValidationError
        If the file is malformed or validation fails
    """
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ChaosValidationError(f"File must be valid UTF-8: {exc}") from exc
    except Exception as exc:
        raise ChaosValidationError(f"Could not read file: {exc}") from exc

    return parse_chaos_text(text)


def parse_chaos_text(text: str) -> tuple[ChaosHeader, str]:
    """
    Parse CHAOS content from text.

    Parameters
    ----------
    text : str
        CHAOS file content

    Returns
    -------
    tuple[ChaosHeader, str]
        Parsed header and content

    Raises
    ------
    ChaosValidationError
        If the content is malformed or validation fails
    """
    if not isinstance(text, str):
        raise ChaosValidationError("CHAOS source must be textual input")

    # Check for content markers
    begin_count = text.count(CONTENT_BEGIN)
    end_count = text.count(CONTENT_END)

    if begin_count != 1:
        if begin_count == 0:
            raise ChaosValidationError(f"Missing {CONTENT_BEGIN} marker")
        raise ChaosValidationError(f"Multiple {CONTENT_BEGIN} markers found")
    if end_count != 1:
        if end_count == 0:
            raise ChaosValidationError(f"Missing {CONTENT_END} marker")
        raise ChaosValidationError(f"Multiple {CONTENT_END} markers found")

    # Split into header and content sections
    try:
        head, rest = text.split(CONTENT_BEGIN, 1)
        content, _tail = rest.split(CONTENT_END, 1)
    except ValueError as exc:
        raise ChaosValidationError(
            f"Malformed content markers: {CONTENT_BEGIN} and {CONTENT_END} must appear exactly once"
        ) from exc

    # Parse header lines
    headers = {}
    for line_num, line in enumerate(head.splitlines(), 1):
        line = line.strip()
        if not line:
            continue  # Skip empty lines

        # Check for key: value format
        if ":" not in line:
            raise ChaosValidationError(
                f"Line {line_num}: Invalid header format. Expected 'key: value', got: {line}"
            )

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            raise ChaosValidationError(
                f"Line {line_num}: Header key cannot be empty"
            )

        headers[key] = value

    # Validate headers
    header = ChaosHeader(headers)

    # Validate content is non-empty
    content = content.strip()
    if not content:
        raise ChaosValidationError("Content block cannot be empty")

    return header, content


def validate_chaos_file(path: Path) -> None:
    """
    Validate a CHAOS file.

    Parameters
    ----------
    path : Path
        Path to the CHAOS file

    Raises
    ------
    ChaosValidationError
        If validation fails
    """
    parse_chaos_file(path)


def validate_chaos_text(text: str) -> None:
    """
    Validate CHAOS text content.

    Parameters
    ----------
    text : str
        CHAOS file content

    Raises
    ------
    ChaosValidationError
        If validation fails
    """
    parse_chaos_text(text)
