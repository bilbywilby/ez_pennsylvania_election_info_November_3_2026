#!/usr/bin/env bash
set -euo pipefail

##############################################################################
# Pre-commit verification workflow for Pennsylvania Election Information
#
# This script enforces data integrity, source lineage, and formatting standards
# before any changes are committed to the repository. It prevents unverified
# working notes from research/ from reaching processed/ or public/ outputs.
#
# Usage: ./scripts/verify/pre-commit.sh
# Install as Git hook: ln -sf ../../scripts/verify/pre-commit.sh .git/hooks/pre-commit
##############################################################################

readonly REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
readonly SCRIPTS_DIR="$REPO_ROOT/scripts/verify"
readonly DATA_DIR="$REPO_ROOT/data"
readonly PROCESSED_DIR="$REPO_ROOT/processed"
readonly PUBLIC_DIR="$REPO_ROOT/public"
readonly TESTS_DIR="$REPO_ROOT/tests"

# Color output for visibility
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

log_step() {
    echo -e "${GREEN}[VERIFY]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

##############################################################################
# 1. UNIT TESTS
##############################################################################
log_step "Running unit test suite..."
if ! python3 -m unittest discover -s "$TESTS_DIR" -p "test_*.py" 2>&1; then
    log_error "Unit tests failed. Do not commit until tests pass."
    exit 1
fi
log_step "Unit tests passed."

##############################################################################
# 2. NLP OUTPUT VERIFICATION (if processed/ exists and contains outputs)
##############################################################################
if [[ -d "$PROCESSED_DIR/nlp" ]]; then
    log_step "Validating NLP output lineage and metadata..."
    if ! python3 "$SCRIPTS_DIR/verify_nlp.py" \
        --input-dir "$PROCESSED_DIR/nlp" \
        --strict 2>&1; then
        log_error "NLP verification failed. Ensure all records have complete lineage metadata."
        exit 1
    fi
    log_step "NLP outputs verified."
else
    log_warning "No processed/nlp directory found (optional)."
fi

##############################################################################
# 3. PUBLIC JSON VALIDATION (if public/api exists)
##############################################################################
if [[ -d "$PUBLIC_DIR/api/v1" ]]; then
    log_step "Validating public API JSON formatting and metadata..."
    if ! python3 "$SCRIPTS_DIR/validate_json.py" \
        --data-dir "$PUBLIC_DIR/api/v1" 2>&1; then
        log_error "JSON validation failed. Check formatting and lineage metadata."
        exit 1
    fi
    log_step "Public JSON outputs validated."
else
    log_warning "No public/api/v1 directory found (optional)."
fi

##############################################################################
# 4. RESEARCH DIRECTORY SAFETY CHECK
##############################################################################
log_step "Checking for accidental staging of unverified research materials..."
staged_research=$(git diff --cached --name-only 2>/dev/null | grep '^research/' || true)
if [[ -n "$staged_research" ]]; then
    log_warning "The following research files are staged for commit:"
    echo "$staged_research" | sed 's/^/  /'
    log_warning "Research materials should be preserved but not committed with generated outputs."
    log_warning "Consider unstaging these files unless explicitly reviewing/verifying them."
    read -p "Continue with commit? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_error "Commit aborted by user."
        exit 1
    fi
fi

##############################################################################
# 5. VERIFICATION SUMMARY
##############################################################################
log_step "All verification checks passed."
echo ""
echo "Repository state is clean and ready to commit:"
echo "  ✓ Unit tests passed"
echo "  ✓ NLP lineage metadata verified (if applicable)"
echo "  ✓ Public JSON formatting and metadata validated (if applicable)"
echo "  ✓ Research directory safety checked"
echo ""
exit 0
