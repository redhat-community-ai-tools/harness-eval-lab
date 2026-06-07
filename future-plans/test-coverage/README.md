# Test Coverage: Making the Rules Trustworthy

> **Status:** future

## The problem

The test suite has 62 tests for ~4,200 lines of source. The 26 inspection rules are the core value of the tool, but not all have individual test cases with edge cases. Without full coverage, adding or modifying a rule can silently break another.

## Why it matters

The rules are the tool's credibility. If `no-prompt-injection` has a false positive on a common pattern, users stop trusting the tool. If `description-quality` misses a clear violation, the tool looks incompetent. Tests are the safety net that prevents both.

Also: the rules use shared infrastructure (the engine, parsers, registry, scan_state). A change to the engine can break rules in non-obvious ways. Integration tests catch this.

## What needs coverage

### Unit tests for each rule

Each of the 26 rules should have at minimum:

| Test type | What it verifies | Example |
|-----------|-----------------|---------|
| Positive case | Rule fires when it should | A SKILL.md with no description triggers `description-required` |
| Negative case | Rule stays silent on clean input | A SKILL.md with a good description passes `description-required` |
| Edge case | Rule handles tricky input | Pattern inside a code block doesn't trigger `no-prompt-injection` |

That's 78 test cases as a baseline. Some rules warrant more:
- `no-prompt-injection` (17 patterns, code block detection, example detection)
- `duplicate-detection` (scan_state handling, threshold boundary)
- `token-budget` (adaptive budget calculation, line count)

### CLI integration tests

Use Click's `CliRunner` to test the CLI commands end-to-end:
1. Create fixture directories with known setups (one clean, one with issues)
2. Run `scan`, `eval-setup`, `eval-skill` against them
3. Assert on exit codes and key strings in the output
4. Verify JSON output parses correctly and contains expected keys

### System analysis tests

Test the budget, trigger, and dependency analyzers with known inputs:
- Budget: verify always-loaded ratio calculation, heaviest component detection
- Triggers: verify overlap detection thresholds, missing "use when" detection
- Dependencies: verify broken reference detection, orphan identification

## How to build it

### Approach: fixture-based testing

Create a `tests/fixtures/` directory (already partially exists) with setups that exercise specific rule combinations:

```
tests/fixtures/
  clean-setup/           <- passes all rules
  broken-setup/          <- triggers specific known errors
  security-issues/       <- triggers injection/credential rules
  duplicate-skills/      <- triggers duplicate detection
  single-file/           <- for single-file scan testing
```

Each fixture is a minimal directory with just enough files to test the relevant rules. Not a real project, just the agent setup files.

### Approach: parametrized tests

Use `@pytest.mark.parametrize` to run the same test structure across multiple rules:

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

This keeps the test file compact while covering many cases.

## Open questions

- Should fixtures be minimal (just the files needed) or realistic (resembling real setups)?
- Should integration tests run the actual CLI or call the Python functions directly?
- How to test the plugin skills (SKILL.md instructions for Claude)? Static analysis of the SKILL.md? Or skip since they're prompt instructions, not code?
