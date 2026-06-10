# Scoring Calibration: Making Scores Trustworthy

**Status:** future
**Created:** 2026-06-10

## Problem

When the plugin's Layer 2 (Claude scoring components on rubric dimensions) is implemented, users will see scores like "Redundancy: 4/5" or "Trigger quality: 2/5." If those scores don't match reality, users lose trust and ignore them.

Calibration means: when the tool says 4/5, a human looking at the same component would also say "that's good." When it says 2/5, a human would agree "that needs work."

Uncalibrated scores have two failure modes. Too generous: everything gets 4-5/5, so the scores are meaningless and users learn to ignore them. Too harsh: everything gets 1-2/5, so users feel demoralized or learn to ignore the scores. Same result either way. The goal is correlation: the tool's ranking of setups should match a human expert's ranking, even if the absolute numbers differ slightly.

## Proposal

A three-phase approach, starting cheap and increasing rigor over time.

**Phase 1: Anchor examples.** When writing the Layer 2 rubric files (`rubric/skills-rubric.md`, etc.), include a concrete example for score levels 1, 3, and 5 for each dimension. These are short inline examples, not separate files. This directly improves scoring consistency by giving Claude examples to compare against.

**Phase 2: Ranking validation.** Create a `calibration/` directory in the repo with 5-10 sample setups (anonymized or synthetic) as fixture directories. Include a `rankings.json` with human-assigned rankings per dimension. Add a test that runs the tool on each setup and checks ranking correlation. Run this test whenever rubric descriptions change.

**Phase 3: Human-rated calibration set (long-term).** Collect 15-20 real Claude Code setups. Have 2-3 human raters score each on the rubric dimensions. Run the tool on the same setups. Compare. Adjust rubric descriptions until scores correlate. This is the gold standard but depends on having enough real-world usage data.

## User stories

**Story 1: Consistent scoring via anchor examples**
- **Given** a rubric dimension (e.g., Specificity) with anchor examples at levels 1, 3, and 5
- **When** Claude scores a component on that dimension
- **Then** the score aligns with the anchor examples (a component similar to the level-3 example gets a score near 3)
- **Acceptance criteria:** Scores on known anchor-like inputs land within 1 point of the expected level.

**Story 2: Ranking validation against human judgment**
- **Given** a calibration set of 5-10 setups with human-assigned rankings
- **When** the tool ranks those setups
- **Then** the tool's ranking matches the human ranking (Spearman correlation > 0.7)
- **Acceptance criteria:** Automated test fails if ranking correlation drops below threshold after rubric changes.

**Story 3: Score trust from end users**
- **Given** a user receives a scored evaluation report
- **When** they review the scores against their own judgment
- **Then** the scores feel credible and actionable, not inflated or deflated
- **Acceptance criteria:** User feedback on score accuracy is positive in > 70% of cases.

## Requirements

1. Every rubric dimension must have anchor examples at levels 1, 3, and 5.
2. Calibration fixtures must be anonymized or synthetic (no real user data without consent).
3. Ranking validation test must run as part of the test suite when rubric files change.
4. Calibration set must include at least 5 setups spanning poor to excellent quality.
5. Human raters must have Claude Code expertise.
6. Ranking correlation metric must be Spearman rank correlation.

## Success criteria

- Anchor examples are present for all rubric dimensions before Layer 2 launches.
- Ranking validation test passes with Spearman correlation > 0.7 on the calibration set.
- Score distribution across real evaluations follows a roughly normal shape (not clustered at extremes).
- Rubric changes that break ranking correlation are caught by CI.

## Open questions

- Where to source real setups for calibration? (Open-source repos, team setups, synthetic?)
- How many raters are needed for reliable human scores?
- Should calibration be per-dimension or overall?
- How often does the calibration set need to be refreshed?
