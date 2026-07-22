# harness-eval — Security Differentiation & Enhancement Plan

**For:** Claude Code (Opus 4.6), executing against the `harness-eval` repo.
**Objective:** Move the security subsystem off the single-file scanner model and onto harness-eval's real axis: whole-harness, cross-component, multi-assistant analysis. Then bump the version and ship the changes consistently across every surface.

## Hard rules (apply to every task)

- Keep the test suite green (`make test` / `pytest`). Add tests for all new behavior; do not weaken existing coverage.
- Never make a change whose only purpose is cosmetic (renaming symbols, reshuffling files). If a task has no engineering justification, skip it. Reviewers reject cosmetic diffs.
- The deterministic `security` scan must run fully offline, with no API key. LLM and network steps (CVE, semantic review) stay strictly opt-in.
- **Cross-surface parity is mandatory.** Every user-facing capability added here must work and behave identically across all delivery surfaces:
  - the CLI (`harness-eval …`, entry points in `src/harness_eval/cli/`),
  - the Claude Code plugin (`.claude-plugin/`, `skills/`, `commands/`),
  - the GitHub Action (`action.yml`, `.github/actions/harness-eval/`, `.github/workflows/`),
  - the Cursor commands (`.cursor/commands/`, `commands/`),
  - the pre-commit hook (`.pre-commit-config.yaml`).
  When you add a flag, rule category, or output field, wire it through all five and update each surface's docs. A feature that only works in the CLI is incomplete.
- All changes ship in a single PR with an engineering rationale in the description (reviewers @Benkapner @csoceanu).

---

# PART A — Security differentiation

## A1 — Elevate security into the cross-component engine (headline feature)

**Rationale:** harness-eval already discovers the whole harness (Claude/Cursor/Copilot/Gemini/OpenCode) and already has cross-component content rules (`content/mcp_skill_alignment.py`, `content/permission_escalation.py`, `content/orphan_skills.py`, `content/circular_references.py`). Security currently ignores that graph and scans file-by-file. This task makes security graph-aware.

1. Add `src/harness_eval/inspection/rules/security/cross_component_flow.py` that runs after per-file taint and reasons over component boundaries, using the component/reference graph the discoverers already build:
   - **Inter-component exfiltration:** a command/hook/agent reads a secret (source) and hands it to a skill whose script reaches a network sink. Propagate taint along graph edges (references, invocations), not just within a file.
   - **Confused-deputy / privilege re-grant:** an agent declares `disallowedTools` but references a skill or command that re-enables the blocked capability.
   - **MCP capability vs. skill claim as a security finding:** extend `content/mcp_skill_alignment.py` logic; if a skill's script calls an MCP tool the config never grants (or grants via wildcard), raise a security finding.
2. Give cross-component findings their own ID prefix (e.g. `XC-*`) and a dedicated `RuleCategory` so they render distinctly in `output/report.py` and SARIF (`output/sarif.py`).
3. This is the headline feature. Prioritize it.

## A2 — Shell-first taint analysis

**Rationale:** Agent hooks, `settings.json` commands, and many skills are bash. harness-eval already has `bash_taint_tracking.py`; deepen it into an ownable strength.

1. Replace regex/line-based bash handling with a real parse via `tree-sitter-bash` (or `bashlex`). Add it as an optional dependency extra in `pyproject.toml` so the base install stays light; degrade gracefully when the extra is absent.
2. Taint through pipes, `$(...)` command substitution, process substitution, heredocs, and subshells. Add shell-specific sinks: `curl … | bash`, `wget -O- … | sh`, `eval "$(…)"`, base64→`bash` pipelines, and env-var flows (`$OPENAI_API_KEY` → `curl -d`/`-H`).
3. Model hook input as a taint source (Claude Code hooks receive tool input on stdin) and connect hook discovery into the A1 graph so tainted hook input can flow into a referenced script.

## A3 — Reachability- and trigger-aware severity

**Rationale:** harness-eval already models triggers (`analysis/triggers.py`) and context (`analysis/context_utilization.py`). Gate severity on reachability from a declared entry point.

1. For each security finding, compute whether the sink is in a script the skill's trigger/description/frontmatter actually causes to run, versus dead or example code. Downgrade unreachable findings; upgrade findings reachable from a broad/auto-firing trigger.
2. Add a `reachability` field to the finding/`ReportDescriptor` type; surface it in reports and as a SARIF property.
3. Compose with A1: a finding is CRITICAL when a broad-trigger → tainted-flow → cross-component-network-sink chain exists end to end.

## A4 — Config-driven capability taxonomy

**Rationale:** Hard-coded source/sink frozensets are brittle and hard to extend. Driving them from data, organized by capability, is better engineering.

1. Extract source/sink/exec definitions out of `taint_tracking.py` and `ast_behavioral.py` into a versioned data file `src/harness_eval/data/capabilities.yaml`, keyed by capability (`filesystem.read`, `network.egress`, `process.exec`, `credential.read`, `persistence.write`), each mapping to per-language matchers (python names, bash builtins, JS APIs). Analyzers become thin engines over the taxonomy.
2. Give findings harness-eval-native IDs tied to capabilities (e.g. `HE-SEC-EGRESS-001`) and regenerate the `rules` listing (`cli/rules.py`) and docs from the taxonomy so IDs, code, and docs never drift.

## A5 — Framework mapping

**Rationale:** Rules that cite external frameworks are credible, comparable, and paper-ready.

1. Add `frameworks: {owasp_llm, owasp_agentic, mitre_atlas}` metadata to each security rule's `RuleMeta`.
2. Emit the mapping into SARIF `rule.properties` and a generated `docs/rules/coverage.md` matrix.
3. Add a `--framework owasp-llm` filter to `security` and `rules`, wired through all five surfaces.

---

# PART B — Enhancements

## B1 — Suggestion plans for findings

**Rationale:** Reporting without actionable guidance is a gap. Attaching structured suggestions to findings helps users understand what to fix and why, without the risk of automated file modifications.

1. For each finding that has a deterministic remedy (broken references, malformed frontmatter, duplicate/dangling refs, unpinned deps, unquoted shell variables), attach a structured `suggestion` field describing what to change, where, and why.
2. Suggestions are advisory only. The tool never modifies user files. Users decide whether to apply them.
3. Surface suggestions in terminal output, JSON, and SARIF reports across all five surfaces.

## B2 — Baseline / suppression for incremental adoption

**Rationale:** Large existing repos won't adopt a linter that floods them with pre-existing findings. A baseline is the standard unlock.

1. Add `harness-eval baseline` to snapshot current findings to a `.harness-eval-baseline.*` file, and make all commands suppress baselined findings so CI only fails on *new* issues. Reuse/extend `inspection/suppression.py`.
2. Support per-finding inline suppression with a required justification, and a summary of suppressed counts.
3. Wire baseline generation and consumption through all five surfaces; the Action must accept a baseline path input.

## B3 — Repo-level grade + badge

**Rationale:** Badges spread because people paste them in READMEs; a single grade drives virality and gives teams a target.

1. Emit a single repo-level grade/score (derive from security labels plus quality/consistency findings) and a `harness-eval badge` command that writes a shields.io-compatible endpoint JSON and an SVG card.
2. Make the Action able to post the grade as a PR comment / status check and update a committed badge file.

## B4 — Documentation & threat-model polish

**Rationale:** Perceived seriousness compounds adoption and reviewer trust.

1. Stand up a docs site (MkDocs Material) generated from the rule catalog and the capability taxonomy so rule docs are always in sync with code.
2. Add/upgrade `THREAT_MODEL.md` (attacker model, trust boundaries, what the tool does and does not defend).
3. Keep the README's rule/badge counts generated, never hand-typed.

## B5 — README & positioning

**Rationale:** The README should lead with what makes harness-eval unique.

1. Lead the README with the differentiator: harness-eval audits the entire harness (CLAUDE.md, skills, commands, hooks, MCP, subagents) together, across five assistants, and reasons about how a weakness in one component becomes an exploit through another.
2. Rewrite the security section to lead with cross-component flow (A1), shell-aware taint (A2), reachability-gated severity (A3), and framework-mapped findings (A5); list the standard checks underneath as table stakes.
3. Update `description` fields in `.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json`, `pyproject.toml`, and `action.yml` to the new one-liner.

---

# Task Z — Version bump (do last, once features land)

1. Find the current version (`pyproject.toml`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `action.yml`). These changes alter rule IDs and add commands, so perform a **major** version bump (current plugin is 5.2.0 → release as **6.0.0**; align the PyPI package version to match).
2. Update the version in every location above and anywhere else it appears (`git grep` the current version string).
3. Write a `CHANGELOG.md` entry for 6.0.0 summarizing: cross-component security analysis, shell-first taint, reachability-gated severity, capability taxonomy + native rule IDs, framework mapping, suggestion plans, baseline, and the grade/badge.
4. Confirm the version is consistent across CLI `--version`, plugin manifest, Action metadata, and PyPI packaging before tagging the release.

# Definition of done

- All five surfaces expose the new capabilities with matching behavior and updated docs.
- `security` runs offline with no key; CVE/semantic remain opt-in.
- Cross-component findings demonstrably catch at least one attack that per-file analysis misses (add a fixture proving it).
- Tests green, docs and CHANGELOG updated, version bumped to 6.0.0 everywhere, single PR for all changes.
