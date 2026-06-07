# Scoring Calibration: Making Scores Trustworthy

> **Status:** future

## The problem

When the plugin's Layer 2 (Claude scoring components on rubric dimensions) is implemented, users will see scores like "Redundancy: 4/5" or "Trigger quality: 2/5." If those scores don't match reality, users lose trust and ignore them.

Calibration means: when the tool says 4/5, a human looking at the same component would also say "that's good." When it says 2/5, a human would agree "that needs work."

## Why it matters

Uncalibrated scores have two failure modes:

**Too generous:** Everything gets 4-5/5, so the scores are meaningless. Users learn to ignore them. The tool becomes a formality.

**Too harsh:** Everything gets 1-2/5, so users either feel demoralized or learn to ignore the scores. Same result.

The goal is correlation: the tool's ranking of setups should match a human expert's ranking, even if the absolute numbers differ slightly.

## Approaches explored

### Approach 1: Human-rated calibration set

Collect 15-20 real Claude Code setups. Have 2-3 human raters score each on the rubric dimensions. Run the tool on the same setups. Compare. Adjust rubric descriptions until scores correlate.

**Trade-offs:**
- Gold standard for calibration
- Expensive to create (needs human raters with Claude Code expertise)
- Static: calibration set becomes stale as best practices evolve
- Reusable: future rubric changes can be regression-tested against the set

### Approach 2: Relative ranking

Instead of calibrating absolute scores, calibrate ranking. Take 5 setups, have humans rank them best-to-worst. Run the tool. Check if the tool's ranking matches.

**Trade-offs:**
- Easier than scoring (ranking is cognitively simpler than rating)
- Doesn't validate the absolute 1-5 scale
- Fewer raters needed (ranking agreement is higher than rating agreement)
- Good enough for "is this tool useful?" validation

### Approach 3: Anchor examples

For each rubric dimension at each score level (1-5), provide a concrete example in the rubric file. "A 3/5 on Specificity looks like this: [example]. A 5/5 looks like this: [example]."

**Trade-offs:**
- No external calibration set needed
- Directly improves scoring consistency (Claude has examples to compare against)
- Doesn't validate whether the scale itself is meaningful
- Easy to maintain (examples evolve with the rubric)

## Recommended direction

Start with **Approach 3 (anchor examples)** because it's free, immediately useful, and improves every evaluation. Add examples to each rubric file as part of the Layer 2 implementation.

Then build **Approach 2 (relative ranking)** as a validation step: 5-10 setups, ranked by a human, compared to the tool's ranking. This confirms the tool is directionally correct without the cost of full calibration.

**Approach 1** is the long-term goal but depends on having enough real-world usage data.

## How to build it

**Phase 1 (anchor examples):** When writing the Layer 2 rubric files (`rubric/skills-rubric.md`, etc.), include a concrete example for score levels 1, 3, and 5 for each dimension. These are short inline examples, not separate files.

**Phase 2 (ranking validation):**
1. Create `calibration/` directory in the repo
2. Add 5-10 sample setups (anonymized or synthetic) as fixture directories
3. Include a `rankings.json` with human-assigned rankings per dimension
4. Add a test that runs the tool on each setup and checks ranking correlation
5. Run this test whenever rubric descriptions change

## Open questions

- Where to source real setups for calibration? (Open-source repos, team setups, synthetic?)
- How many raters are needed for reliable human scores?
- Should calibration be per-dimension or overall?
- How often does the calibration set need to be refreshed?
