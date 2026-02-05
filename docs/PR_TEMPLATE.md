# PR: refactor(chaos): canonicalize CHAOS language & replace mirrors with shims

## What Changed

- Established `05_CHAOS_Coding_Language/src/chaos_language/` as the single source of truth for all CHAOS language implementation
- Converted duplicate implementations in `EdenOS_Origin/vaults/` to deprecation shims
- Added filesystem-level deprecation warnings to all legacy mirror locations
- Created CI enforcement to prevent future duplication

## Why

- **33.82% code duplication** across CHAOS implementations (4,296 lines, 39,373 tokens)
- Byte-for-byte identical copies of core modules (lexer, parser, runtime, protocols)
- Bug fixes required touching 3+ locations
- No clear source of truth

## Canonical Package

```
05_CHAOS_Coding_Language/src/chaos_language/
├── chaos_lexer.py (ChaosLexer)
├── chaos_parser.py (ChaosParser)  
├── chaos_interpreter.py (ChaosInterpreter)
├── chaos_runtime.py (run_chaos)
├── chaos_validator.py (validate_chaos)
├── chaos_agent.py (ChaosAgent)
├── chaos_emotion.py (ChaosEmotionStack)
├── chaos_protocols.py
├── chaos_stdlib.py
└── ... (17 total modules)
```

## Migration Guide

### Old (deprecated)
```python
# From mirror locations - still works but warns
from EdenOS_Origin.vaults.EdenOS_Origin.05_CHAOS_Coding_Language.chaos_lexer import ChaosLexer
```

### New (canonical)
```python
from chaos_language import ChaosLexer, ChaosParser, ChaosInterpreter
```

**All mirror paths emit `DeprecationWarning` and contain `README_DEPRECATED.md` with migration instructions.**

## Rollback Plan

1. `git revert` the 4 commits in reverse order
2. Duplication returns but all paths remain accessible
3. No data loss—mirrors converted to shims, not deleted

## Testing

- [x] Canonical imports resolve correctly
- [x] Core classes instantiable
- [x] Deprecation shims exist in mirror locations
- [x] CI duplication gate functional
- [x] Baseline measured: 33.82% → Target: <10%

## Post-Merge Duplication Target

After shims merge, duplication should drop to <5%. CI will enforce 10% threshold and can be tightened as consumer code migrates.

## Checklist

- [x] No logic changes—pure structural refactor
- [x] No API breakage—canonical package already exported
- [x] No file deletions—mirrors converted to shims
- [x] Tests verify canonical + shim existence
- [x] CI structural invariant enforced
