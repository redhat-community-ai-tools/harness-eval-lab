# Test Coverage: Making the Rules Trustworthy

**Status:** future
**Created:** 2026-06-10

## Problem

The test suite has 62 tests for ~4,200 lines of source. The 26 inspection rules are the core value of the tool, but not all have individual test cases with edge cases. Without full coverage, adding or modifying a rule can silently break another.

The rules are the tool's credibility. If `no-prompt-injection` has a false positive on a common pattern, users stop trusting the tool. If `description-quality` misses a clear violation, the tool looks incompetent. Tests are the safety net that prevents both. The rules also use shared infrastructure (the engine, parsers, registry, scan_state). A change to the engine can break rules in non-obvious ways. Integration tests catch this.

## Proposal

Build comprehensive test coverage using two complementary approaches: fixture-based testing and parametrized tests.

**Fixture-based testing.** Create fixture directories in `tests/fixtures/` that exercise specific rule combinations:

```
tests/fixtures/
  clean-setup/           <- passes all rules
  broken-setup/          <- triggers specific known errors
  security-issues/       <- triggers injection/credential rules
  duplicate-skills/      <- triggers duplicate detection
  single-file/           <- for single-file scan testing
```

Each fixture is a minimal directory with just enough files to test the relevant rules. Not a real project, just the agent setup files.

**Parametrized tests.** Use `@pytest.mark.parametrize` to run the same test structure across multiple rules:

```python
@pytest.mark.parametrize("rule_id,fixture,should_fire", [
    ("frontmatter/description-required", "no-description", True),
    ("frontmatter/description-required", "has-description", False),
    ("frontmatter/description-quality", "first-person-desc", True),
    ...
])
def test_rule(rule_id, fixture, should_fire):
    result = lint(f"tests/fixtures/{fixture}")
    fired = any(d.rule_id == rule_id for d in result.diagnostics)
    assert fired == should_fire
```

**Coverage targets per area:**

- **Unit tests for each rule (26 rules x 3 minimum = 78 tests):** Positive case (rule fires when it should), negative case (rule stays silent on clean input), edge case (tricky input like patterns inside code blocks).
- **CLI integration tests:** Use Click's `CliRunner` to test `scan`, `eval-setup`, `eval-skill` end-to-end against fixture directories. Assert on exit codes, key output strings, and JSON structure.
- **System analysis tests:** Test budget, trigger, and dependency analyzers with known inputs. Verify always-loaded ratio calculation, overlap detection thresholds, broken reference detection.

Rules that warrant extra coverage: `no-prompt-injection` (17 patterns, code block detection, example detection), `duplicate-detection` (scan_state handling, threshold boundary), `token-budget` (adaptive budget calculation, line count).

## User stories

**Story 1: Rule regression safety**
- **Given** a developer modifies the lint engine or a shared parser
- **When** they run `uv run pytest`
- **Then** any rules broken by the change are caught by failing tests
- **Acceptance criteria:** Every rule has at least one positive, one negative, and one edge case test.

**Story 2: CLI correctness verification**
- **Given** a developer changes CLI output formatting or adds a new flag
- **When** they run the integration test suite
- **Then** exit codes, output structure, and JSON format are validated against fixtures
- **Acceptance criteria:** All 3 CLI commands have integration tests covering success and failure paths.

**Story 3: Confident rule development**
- **Given** a developer is adding a new inspection rule
- **When** they follow the test pattern (parametrized with fixtures)
- **Then** they can write tests quickly using existing fixtures and patterns
- **Acceptance criteria:** Adding a new rule requires creating fixture data and adding parametrize entries, not writing test infrastructure from scratch.

## Requirements

1. Each of the 26 rules must have at least 3 test cases (positive, negative, edge case).
2. Fixture directories must be minimal (only files needed for the test, not full project replicas).
3. CLI integration tests must use Click's `CliRunner` for in-process testing.
4. Parametrized test patterns must be documented so new rule authors can follow them.
5. System analysis tests must cover budget ratio calculation, trigger overlap detection, and broken reference detection.
6. Total test count target: 78+ rule tests, 10+ CLI tests, 10+ analysis tests.

## Success criteria

- All 26 rules have individual test cases covering positive, negative, and edge case scenarios.
- CI catches rule regressions before they reach main branch.
- Test count reaches 100+ (up from 62).
- New rules can be tested by adding parametrize entries and fixture data, with no new test infrastructure needed.

## Open questions

- Should fixtures be minimal (just the files needed) or realistic (resembling real setups)?
- Should integration tests run the actual CLI or call the Python functions directly?
- How to test the plugin skills (SKILL.md instructions for Claude)? Static analysis of the SKILL.md? Or skip since they're prompt instructions, not code?
