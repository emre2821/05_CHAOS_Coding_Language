# CHAOS Language Specification

**Version:** 1.0.0  
**Status:** Canonical  
**Last Updated:** 2025-12-21

## Overview

CHAOS (Contextual Harmonics and Operational Stories) is a symbolic–operational language that combines structured metadata, emotional context, ethical constraints, and narrative content. This specification defines the canonical file format for CHAOS artifacts.

## File Structure

A CHAOS file consists of two main sections:

1. **Header Section**: Key-value metadata pairs
2. **Content Section**: Enclosed narrative or operational content

### Basic Structure

```
file_type: <type>
classification: <classification>
tags: <tag1>, <tag2>, <tag3>
[additional optional headers]

[CONTENT BEGIN]
<narrative or operational content>
[CONTENT END]
```

## Header Fields

### Required Fields

#### `file_type`
- **Required**: Yes
- **Type**: String
- **Description**: Declares the primary purpose or category of the artifact
- **Examples**: `memory`, `ritual`, `vow`, `protocol`, `configuration`, `persona`

#### `tags`
- **Required**: Yes
- **Type**: Comma-separated list of strings
- **Description**: Non-empty list of searchable keywords or categories
- **Unicode Support**: Yes (emojis and Unicode characters allowed)
- **Examples**: 
  - `memory, garden, growth`
  - `🌸, ritual, spring`
  - `vow, commitment, 💙`

### Optional Core Fields

#### `classification`
- **Required**: No
- **Type**: String
- **Description**: Hierarchical or symbolic classification of the artifact
- **Unicode Support**: Yes
- **Examples**: `personal/memory`, `system/daemon`, `🔒 confidential`

#### `symbolic_identity`
- **Required**: No
- **Type**: String
- **Description**: The persona, role, or entity associated with this artifact
- **Examples**: `Eden.Seiros`, `ConcordAgent`, `Memory Keeper`

### Ethics and Safety Fields

These optional fields support consent-aware and safety-conscious systems.

#### `consent`
- **Required**: No
- **Type**: Enumeration
- **Allowed Values**: `explicit`, `implicit`, `none`
- **Description**: Declares the consent posture of the artifact
  - `explicit`: Clear, affirmative consent obtained
  - `implicit`: Consent reasonably assumed from context
  - `none`: No consent obtained or consent not applicable
- **Default**: Not specified

#### `safety_tier`
- **Required**: No
- **Type**: Enumeration
- **Allowed Values**: `low`, `med`, `high`
- **Description**: Indicates the safety or risk sensitivity level
  - `low`: General content, minimal risk
  - `med`: Moderate sensitivity, handle with care
  - `high`: High sensitivity, requires special handling
- **Default**: Not specified

#### `sensitive`
- **Required**: No
- **Type**: Enumeration
- **Allowed Values**: `pii`, `trauma`, `none`
- **Description**: Flags the presence of sensitive content types
  - `pii`: Contains personally identifiable information
  - `trauma`: Contains trauma-related content
  - `none`: No sensitive content
- **Default**: Not specified

### Additional Optional Fields

CHAOS is extensible. Additional metadata fields may be added as needed:

- `author`: Creator or author of the artifact
- `created`: ISO 8601 timestamp of creation
- `version`: Version identifier
- `depends_on`: Dependencies or prerequisites
- `emotion`: Emotional tone or affect (e.g., `joy:7`, `hope:5`)

## Content Section

### Content Markers

Content must be enclosed between `[CONTENT BEGIN]` and `[CONTENT END]` markers.

```
[CONTENT BEGIN]
<content here>
[CONTENT END]
```

### Content Rules

1. **Presence**: Content section must be present (between markers)
2. **Non-empty**: Content must contain at least one non-whitespace character
3. **Format**: Content may be:
   - Prose narrative
   - Structured data (JSON, YAML)
   - Code or pseudocode
   - Symbolic notation
   - Mixed formats

### Example with Content

```
file_type: memory
tags: garden, growth, 🌱
emotion: joy:7

[CONTENT BEGIN]
The garden was alive with color and quiet courage.
Each bloom held a story, each leaf a promise.
[CONTENT END]
```

## Validation Rules

A valid CHAOS file must satisfy:

1. **Required Fields Present**:
   - `file_type` must be specified
   - `tags` must be specified and non-empty

2. **Field Format Compliance**:
   - `tags` must be a comma-separated list
   - Enumeration fields (`consent`, `safety_tier`, `sensitive`) must use allowed values
   - Header lines must follow `key: value` format

3. **Content Block Present**:
   - `[CONTENT BEGIN]` marker must be present
   - `[CONTENT END]` marker must be present
   - Content between markers must be non-empty

4. **UTF-8 Encoding**:
   - Files must be valid UTF-8
   - Unicode characters (including emojis) are allowed in all fields

## Unicode and Emoji Support

CHAOS embraces expressive Unicode:

- ✅ Tags: `🌸, ritual, spring`
- ✅ Classification: `🔒 confidential`
- ✅ Content: Any valid Unicode

## Ethics and Consent Guidelines

### When to Use Consent Fields

- **`consent: explicit`**: When you have clear, documented permission
- **`consent: implicit`**: When context reasonably implies permission
- **`consent: none`**: When consent is absent or you're documenting that

### When to Use Safety Tier

- **`safety_tier: high`**: Personal data, trauma narratives, high-risk operations
- **`safety_tier: med`**: Sensitive but not critical content
- **`safety_tier: low`**: General-purpose, public-safe content

### When to Use Sensitive Field

- **`sensitive: pii`**: Names, addresses, identifiers, personal details
- **`sensitive: trauma`**: Abuse, violence, grief, distress narratives
- **`sensitive: none`**: General content without specific sensitivities

## Example Files

### Minimal Valid File

```
file_type: note
tags: example

[CONTENT BEGIN]
This is a minimal valid CHAOS file.
[CONTENT END]
```

### Complete Example with Ethics

```
file_type: memory
classification: personal/vow
tags: commitment, healing, 💙
symbolic_identity: Eden.Seiros
consent: explicit
safety_tier: med
sensitive: none
created: 2025-04-30T14:30:00Z

[CONTENT BEGIN]
I vow to honor the boundaries spoken and unspoken,
to remember that every story belongs to its teller,
and to hold space without judgment.

This is my promise, written in code and care.
[CONTENT END]
```

### Example with PII

```
file_type: configuration
classification: system/user-profile
tags: user, settings
consent: explicit
safety_tier: high
sensitive: pii

[CONTENT BEGIN]
{
  "user_id": "user_12345",
  "email": "user@example.com",
  "preferences": {
    "theme": "dark",
    "notifications": true
  }
}
[CONTENT END]
```

## File Extension

- **Recommended**: `.chaos`
- **Legacy**: `.sn` (Story Notation)

The `.chaos` extension is preferred for new artifacts to clearly identify the file type.

## Implementation Notes

### Parser Requirements

A compliant CHAOS parser must:

1. Parse UTF-8 encoded files
2. Extract key-value pairs from headers
3. Validate required fields
4. Validate enumeration values
5. Locate and extract content between markers
6. Report validation errors with line numbers
7. Handle Unicode/emojis correctly

### Validator Requirements

A compliant CHAOS validator must:

1. Check for required fields
2. Validate field formats and enumerations
3. Ensure content block is present and non-empty
4. Provide human-readable error messages
5. Return non-zero exit code on failure
6. Support batch validation of multiple files

## Security Considerations

1. **No Code Execution**: CHAOS files are data, not executable code. Parsers must not execute embedded content.
2. **Sanitization**: When displaying content, apply appropriate sanitization for the output context.
3. **PII Handling**: Files marked `sensitive: pii` require special handling and must not be logged or transmitted without encryption.
4. **Consent Enforcement**: Systems should honor the `consent` field and not process data marked `consent: none` without explicit override.

## Versioning

This specification follows semantic versioning:

- **Major**: Breaking changes to required fields or structure
- **Minor**: New optional fields or non-breaking additions
- **Patch**: Clarifications, examples, typo fixes

Current version: **1.0.0**

## References

- [README.md](README.md) - Project overview
- [GLOSSARY.md](GLOSSARY.md) - Terminology reference
- [schema/chaos.schema.json](schema/chaos.schema.json) - JSON Schema definition

---

**Canonical Authority**: This document is the single source of truth for CHAOS file format.  
**Governance**: Changes require community review per [GOVERNANCE.md](GOVERNANCE.md).
