# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- CI pipeline: GitHub Actions with lint, typecheck, test, and dogfood jobs
- CODEOWNERS file for PR review governance
- Skillsaw linter config (`.skillsaw.yaml`) for skill context budget validation
- Security test fixture (`tests/fixtures/security-issues/`) with injection, credential, exfiltration, and reverse shell patterns
- E2E CLI tests using Click's CliRunner
- Mock LLM response tests for Layer 2 rubric checker
- Runner abstraction future plan (`future-plans/runner-abstraction/`)
- Prompt versioning: LLM prompts extracted to `src/harness_eval_lab/rubric/prompts/` as markdown files

### Changed
- README updated to remove dimension-based framing, now describes Layer 2 as best-practices + cross-component + redundancy checking
- Future plans restructured from free-form READMEs to structured spec format (problem, proposal, user stories, requirements, success criteria)
- SessionStart `ensure_deps.py` rewritten with isolated venv, stamp-based caching, and uv/pip fallback

### Removed
- References to "5 dimensions" (Soundness, Safety, Coherence, Efficiency, Impact) from README
- `future-plans/impact-dimension/` and `future-plans/scoring-calibration/` removed from README (plans still exist, just not listed as active)

## [0.1.0] - 2026-05-01

Initial release.

- 26 deterministic inspection rules across 8 categories
- System-level analysis (token budget, trigger overlaps, dependencies, context utilization)
- LLM-based qualitative review with per-component issue categories
- CLI with 3 commands: eval-setup-lint, eval-setup-review, eval-skill
- Claude Code plugin with 3 skills
- 62 tests
