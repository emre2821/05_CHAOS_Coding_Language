#!/usr/bin/env python3
# tools/generate_chaos_shims.py
from pathlib import Path

CANON_PKG = "chaos_language"
CANON_HINT = "05_CHAOS_Coding_Language/src/chaos_language"

MIRROR_ROOTS = [
    "EdenOS_Origin/vaults/EdenOS_Origin/05_CHAOS_Coding_Language",
    "EdenOS_Origin/vaults/EdenOS_Origin/000_Eden_Dropbox/EdenOS_Mobile/CHAOS",
]

# Core modules from canonical __init__.py + jscpd findings
CORE_MODULES = [
    "chaos_lexer",
    "chaos_parser",
    "chaos_interpreter",
    "chaos_runtime",
    "chaos_validator",
    "chaos_agent",
    "chaos_reports",
    "chaos_emergence",
    "chaos_emotion",
    "chaos_context",
    "chaos_errors",
    "chaos_stdlib",
    "chaos_protocols",
    "chaos_logger",
    "chaos_graph",
    "chaos_dreams",
    "chaos_format_validator",
    "chaos_continued.complete_build",
    "chaos_language.complete_build",
    "chaos_fuzz",
    "chaos_exec",
    "chaos_cli",
    "chaos_agent_cli",
    "chaos_monorepo",
    "EdenCore",
    "conftest",
]

def write_shim(path: Path) -> None:
    """Write deprecation shim that warns but doesn't import (filesystem-level)."""
    path.write_text(f'''"""
DEPRECATED: This file is a legacy mirror.

The canonical CHAOS implementation is at:
{CANON_HINT}

Import from the canonical package:
    from {CANON_PKG} import <module>

This file remains for backward compatibility but should not be used.
"""
import warnings

warnings.warn(
    f"{{__file__}} is deprecated. Use {CANON_PKG} instead (canonical: {CANON_HINT})",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export from canonical (if this path is somehow still imported)
try:
    from {CANON_PKG}.{path.stem} import *
except ImportError:
    pass  # Mirror file, not meant to be imported
'''.strip())

def main() -> None:
    for root in MIRROR_ROOTS:
        base = Path(root)
        base.mkdir(parents=True, exist_ok=True)
        
        # Package-level README warning
        (base / "README_DEPRECATED.md").write_text(f'''# ⚠️ DEPRECATED CHAOS MIRROR

This directory is a **deprecated copy** of the CHAOS language implementation.

## Canonical Source
The authoritative CHAOS implementation is:
```
{CANON_HINT}
```

## Migration
Import from the canonical package:
```python
from {CANON_PKG} import ChaosLexer, ChaosParser, ChaosInterpreter
```

All files in this directory are legacy mirrors and will be removed in a future version.
'''.strip())
        
        # Generate shims for each module
        for mod in CORE_MODULES:
            shim_path = base / f"{mod}.py"
            write_shim(shim_path)
        
        print(f"✅ Shimmed CHAOS mirror: {base}")
        print(f"   - Created {len(CORE_MODULES)} module shims")
        print("   - Created README_DEPRECATED.md")

if __name__ == "__main__":
    main()
