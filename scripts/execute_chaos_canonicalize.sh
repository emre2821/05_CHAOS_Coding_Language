#!/bin/bash
# scripts/execute_chaos_canonicalize.sh

set -e

echo "🔮 CHAOS Canonicalization Protocol"
echo "=================================="

cd "$(git rev-parse --show-toplevel)"

git fetch origin
git checkout -b feat/chaos-canonicalize

echo ""
echo "Step 1: Generating deprecation shims..."
python3 tools/generate_chaos_shims.py

echo ""
echo "Step 2: Staging canonical package..."
git add 05_CHAOS_Coding_Language/src/chaos_language/

git commit -m "feat(chaos): declare canonical chaos_language package

- Establish 05_CHAOS_Coding_Language/src/chaos_language/ as single source of truth
- Export ChaosLexer, ChaosParser, ChaosInterpreter, and core APIs
- Canonical package for all CHAOS language functionality"

echo ""
echo "Step 3: Staging mirror shims..."
git add EdenOS_Origin/vaults/EdenOS_Origin/05_CHAOS_Coding_Language/
git add EdenOS_Origin/vaults/EdenOS_Origin/000_Eden_Dropbox/EdenOS_Mobile/CHAOS/
git commit -m "refactor(chaos): replace mirror copies with deprecation shims

- Convert EdenOS_Origin vault copies to deprecation shims
- Add README_DEPRECATED.md to each mirror location
- Shims emit DeprecationWarning and point to canonical package
- Measured baseline: 33.82% duplication across 4,296 lines"

echo ""
echo "Step 4: Staging tests..."
git add tests/test_chaos_canonical.py

git commit -m "test(chaos): add canonical package smoke tests

- Verify canonical imports resolve correctly
- Test core class instantiation
- Validate deprecation shims exist in mirror locations
- Ensure README_DEPRECATED.md present in legacy paths"

echo ""
echo "Step 5: Staging CI workflow..."
git add .github/workflows/chaos-quality.yml

git commit -m "ci(chaos): add duplication gate and quality workflow

- Run pytest on canonical CHAOS package
- Execute jscpd duplication analysis
- Fail if duplication exceeds 10% threshold
- Enforce structural invariant: one source of truth"

echo ""
echo "✅ CHAOS canonicalization complete"
echo ""
echo "Current branch: feat/chaos-canonicalize"
echo "Ready to push and open PR"
