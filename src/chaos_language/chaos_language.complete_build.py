"""Compatibility shim for the relocated CHAOS complete-build script."""
from __future__ import annotations

from .complete_build import main as _main


def main(argv=None) -> int:
    """Entrypoint retained for backward compatibility."""
    return _main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
