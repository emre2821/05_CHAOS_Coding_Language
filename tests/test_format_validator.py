"""
Tests for the new CHAOS file format validator.

Tests validate the new header format with key-value pairs and
[CONTENT BEGIN]/[CONTENT END] markers as specified in SPEC.md.
"""

import pytest
from pathlib import Path

from chaos_language.chaos_format_validator import (
    ChaosValidationError,
    parse_chaos_text,
    validate_chaos_file,
    validate_chaos_text,
)


def make_source(header_lines: list[str], content: str = "Content here") -> str:
    header = "\n".join(header_lines)
    return f"{header}\n\n[CONTENT BEGIN]\n{content}\n[CONTENT END]\n"


def assert_validation_error(source: str, expected_substring: str) -> str:
    with pytest.raises(ChaosValidationError) as exc:
        validate_chaos_text(source)
    assert expected_substring.lower() in str(exc.value).lower()
    return str(exc.value)


def test_minimal_valid_file():
    """Test a minimal valid CHAOS file."""
    source = """file_type: note
tags: example

[CONTENT BEGIN]
This is a minimal valid CHAOS file.
[CONTENT END]
"""
    # Should not raise
    validate_chaos_text(source)
    header, content = parse_chaos_text(source)
    assert header["file_type"] == "note"
    assert header["tags"] == "example"
    assert "minimal valid" in content


def test_complete_file_with_ethics():
    """Test a complete file with all ethics fields."""
    source = """file_type: memory
classification: personal/vow
tags: commitment, healing, 💙
symbolic_identity: Eden.Seiros
consent: explicit
safety_tier: med
sensitive: none
created: 2025-04-30T14:30:00Z

[CONTENT BEGIN]
I vow to honor the boundaries spoken and unspoken.
[CONTENT END]
"""
    validate_chaos_text(source)
    header, content = parse_chaos_text(source)
    assert header["file_type"] == "memory"
    assert header["consent"] == "explicit"
    assert header["safety_tier"] == "med"
    assert header["sensitive"] == "none"
    assert "💙" in header["tags"]


def test_missing_file_type():
    """Test that missing file_type raises error."""
    source = make_source(["tags: example"])
    assert_validation_error(source, "file_type")


def test_missing_tags():
    """Test that missing tags raises error."""
    source = make_source(["file_type: note"])
    assert_validation_error(source, "tags")


def test_empty_tags():
    """Test that empty tags raise error."""
    source = make_source(["file_type: note", "tags:"])
    assert_validation_error(source, "tags")


def test_missing_content_begin():
    """Test that missing CONTENT BEGIN marker raises error."""
    source = """file_type: note
tags: example

Content here
[CONTENT END]
"""
    with pytest.raises(ChaosValidationError) as exc:
        validate_chaos_text(source)
    assert "CONTENT BEGIN" in str(exc.value)


def test_missing_content_end():
    """Test that missing CONTENT END marker raises error."""
    source = """file_type: note
tags: example

[CONTENT BEGIN]
Content here
"""
    with pytest.raises(ChaosValidationError) as exc:
        validate_chaos_text(source)
    assert "CONTENT END" in str(exc.value)


def test_empty_content():
    """Test that empty content raises error."""
    source = make_source(["file_type: note", "tags: example"], content="")
    assert_validation_error(source, "empty")


def test_invalid_consent_value():
    """Test that invalid consent value raises error."""
    source = make_source(
        ["file_type: note", "tags: example", "consent: maybe"]
    )
    message = assert_validation_error(source, "consent")
    assert "maybe" in message


def test_invalid_safety_tier_value():
    """Test that invalid safety_tier value raises error."""
    source = make_source(
        ["file_type: note", "tags: example", "safety_tier: critical"]
    )
    assert_validation_error(source, "safety_tier")


def test_invalid_sensitive_value():
    """Test that invalid sensitive value raises error."""
    source = make_source(
        ["file_type: note", "tags: example", "sensitive: secret"]
    )
    assert_validation_error(source, "sensitive")


def test_unicode_support():
    """Test that Unicode and emojis are supported."""
    source = """file_type: persona
tags: 🌸, ritual, spring
classification: 🔒 confidential

[CONTENT BEGIN]
Language flowers bloom in every season 🌺
[CONTENT END]
"""
    validate_chaos_text(source)
    header, content = parse_chaos_text(source)
    assert "🌸" in header["tags"]
    assert "🔒" in header["classification"]
    assert "🌺" in content


def test_multiline_tags():
    """Test tags with proper comma separation."""
    source = """file_type: note
tags: tag1, tag2, tag3, tag4

[CONTENT BEGIN]
Multiple tags work fine
[CONTENT END]
"""
    validate_chaos_text(source)
    header, _ = parse_chaos_text(source)
    assert "tag1" in header["tags"]
    assert "tag2" in header["tags"]


def test_header_without_colon():
    """Test that header lines without colons raise error."""
    source = make_source(
        ["file_type: note", "tags: example", "invalid header line"]
    )
    assert_validation_error(source, "Invalid header format")


def test_valid_consent_values():
    """Test all valid consent values."""
    for consent_value in ["explicit", "implicit", "none"]:
        source = make_source(
            ["file_type: note", "tags: example", f"consent: {consent_value}"]
        )
        validate_chaos_text(source)


def test_valid_safety_tier_values():
    """Test all valid safety_tier values."""
    for tier in ["low", "med", "high"]:
        source = make_source(
            ["file_type: note", "tags: example", f"safety_tier: {tier}"]
        )
        validate_chaos_text(source)


def test_valid_sensitive_values():
    """Test all valid sensitive values."""
    for sensitive in ["pii", "trauma", "none"]:
        source = make_source(
            ["file_type: note", "tags: example", f"sensitive: {sensitive}"]
        )
        validate_chaos_text(source)


def test_whitespace_handling():
    """Test that whitespace in headers is handled correctly."""
    source = make_source(
        ["file_type:   note   ", "tags:  example , test  "]
    )
    validate_chaos_text(source)
    header, _ = parse_chaos_text(source)
    assert header["file_type"] == "note"
    assert "example" in header["tags"]


def test_empty_file():
    """Test that empty file raises error."""
    with pytest.raises(ChaosValidationError):
        validate_chaos_text("")


def test_example_files_are_valid(tmp_path):
    """Test that all example files in examples/ directory are valid."""
    examples_dir = Path(__file__).parent.parent / "examples"
    if not examples_dir.exists():
        pytest.skip("Examples directory not found")
    
    chaos_files = list(examples_dir.glob("*.chaos"))
    assert len(chaos_files) > 0, "No example files found"
    
    for file_path in chaos_files:
        validate_chaos_file(file_path)


def test_template_files_are_valid(tmp_path):
    """Test that all template files in templates/ directory are valid."""
    templates_dir = Path(__file__).parent.parent / "templates"
    if not templates_dir.exists():
        pytest.skip("Templates directory not found")
    
    chaos_files = list(templates_dir.glob("*.chaos"))
    assert len(chaos_files) > 0, "No template files found"
    
    for file_path in chaos_files:
        validate_chaos_file(file_path)


def test_content_with_special_characters():
    """Test that content can contain special characters."""
    source = """file_type: note
tags: special

[CONTENT BEGIN]
Special characters: @#$%^&*()
Unicode: αβγδε
Emojis: 🎉🎊🎈
JSON: {"key": "value"}
[CONTENT END]
"""
    validate_chaos_text(source)
    header, content = parse_chaos_text(source)
    assert "@#$%^&*()" in content
    assert "αβγδε" in content
    assert "🎉" in content
    assert "JSON" in content


def test_content_with_code():
    """Test that content can contain code snippets."""
    source = """file_type: protocol
tags: code, example

[CONTENT BEGIN]
def hello_world():
    print("Hello, CHAOS!")
    
if __name__ == "__main__":
    hello_world()
[CONTENT END]
"""
    validate_chaos_text(source)
    _, content = parse_chaos_text(source)
    assert "def hello_world" in content
    assert "print" in content


def test_header_case_sensitivity():
    """Test that header keys are case-sensitive."""
    source = """File_Type: note
Tags: example

[CONTENT BEGIN]
Content
[CONTENT END]
"""
    # This should fail because file_type and tags are case-sensitive
    with pytest.raises(ChaosValidationError) as exc:
        validate_chaos_text(source)
    assert "file_type" in str(exc.value).lower()
