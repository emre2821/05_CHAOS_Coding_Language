#!/usr/bin/env python3
"""
CHAOS file validator CLI.

Validates CHAOS files against the canonical specification (SPEC.md).
Supports single files, multiple files, and directory globbing.
"""

import argparse
import sys
from pathlib import Path
from typing import List

from chaos_language.chaos_format_validator import (
    validate_chaos_file,
    ChaosValidationError,
)


def validate_file(path: Path, verbose: bool = False) -> bool:
    """
    Validate a single CHAOS file.

    Parameters
    ----------
    path : Path
        Path to the CHAOS file
    verbose : bool
        Print success messages

    Returns
    -------
    bool
        True if valid, False otherwise
    """
    try:
        validate_chaos_file(path)
        if verbose:
            print(f"✔ {path}")
        return True
    except ChaosValidationError as e:
        print(f"✖ {path}: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✖ {path}: Unexpected error: {e}", file=sys.stderr)
        return False


def find_chaos_files(path: Path) -> List[Path]:
    """
    Find all CHAOS files in a directory.

    Parameters
    ----------
    path : Path
        Directory path

    Returns
    -------
    List[Path]
        List of CHAOS files
    """
    chaos_files = []
    for ext in ["*.chaos", "*.sn"]:
        chaos_files.extend(path.rglob(ext))
    return sorted(chaos_files)


def main() -> int:
    """Main entry point for the validator CLI."""
    parser = argparse.ArgumentParser(
        description="Validate CHAOS files against the canonical specification",
        epilog="Examples:\n"
        "  chaos-validate file.chaos\n"
        "  chaos-validate dir/*.chaos\n"
        "  chaos-validate --dir chaos_corpus/\n"
        "  chaos-validate --require-consent file.chaos\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "paths",
        nargs="*",
        help="CHAOS file(s) to validate. Supports glob patterns.",
    )

    parser.add_argument(
        "--dir",
        type=Path,
        help="Validate all CHAOS files in a directory (recursive)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print success messages for each file",
    )

    parser.add_argument(
        "--require-consent",
        action="store_true",
        help="Fail if consent field is not set to 'explicit'",
    )

    parser.add_argument(
        "--fail-on-sensitive",
        action="store_true",
        help="Fail if file contains sensitive content (pii or trauma)",
    )

    args = parser.parse_args()

    # Collect files to validate
    files_to_validate: List[Path] = []

    if args.dir:
        if not args.dir.is_dir():
            print(f"Error: {args.dir} is not a directory", file=sys.stderr)
            return 1
        files_to_validate.extend(find_chaos_files(args.dir))

    for path_str in args.paths:
        path = Path(path_str)
        if path.is_dir():
            files_to_validate.extend(find_chaos_files(path))
        elif "*" in str(path) or "?" in str(path):
            # Handle glob patterns
            matches = list(path.parent.glob(path.name))
            files_to_validate.extend(matches)
        else:
            files_to_validate.append(path)

    if not files_to_validate:
        print("Error: No files to validate. Use --help for usage.", file=sys.stderr)
        return 1

    # Validate each file
    all_valid = True
    validated_count = 0

    for file_path in files_to_validate:
        if not file_path.exists():
            print(f"✖ {file_path}: File not found", file=sys.stderr)
            all_valid = False
            continue

        if not file_path.is_file():
            print(f"✖ {file_path}: Not a file", file=sys.stderr)
            all_valid = False
            continue

        is_valid = validate_file(file_path, args.verbose)
        
        # Additional checks if requested
        if is_valid and (args.require_consent or args.fail_on_sensitive):
            from chaos_language.chaos_format_validator import parse_chaos_file
            
            try:
                header, _ = parse_chaos_file(file_path)
                
                if args.require_consent:
                    consent = header.get("consent", "").strip()
                    if consent != "explicit":
                        print(
                            f"✖ {file_path}: consent field is not 'explicit' (found: '{consent}')",
                            file=sys.stderr,
                        )
                        is_valid = False
                
                if args.fail_on_sensitive:
                    sensitive = header.get("sensitive", "").strip()
                    if sensitive in ["pii", "trauma"]:
                        print(
                            f"✖ {file_path}: contains sensitive content ({sensitive})",
                            file=sys.stderr,
                        )
                        is_valid = False
            except Exception:
                # Already reported by validate_file
                pass

        if is_valid:
            validated_count += 1
        else:
            all_valid = False

    # Summary
    total = len(files_to_validate)
    if all_valid:
        print(f"\n✓ All {validated_count} file(s) valid")
        return 0
    else:
        failed = total - validated_count
        print(f"\n✖ {failed}/{total} file(s) failed validation", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
