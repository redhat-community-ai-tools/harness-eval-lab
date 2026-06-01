"""Dimension definitions per component type."""

from __future__ import annotations

from harness_eval_lab.rubric.types import DimensionDef

SKILL_DIMENSIONS = [
    DimensionDef(
        name="specificity",
        weight=0.25,
        description="1=vague platitudes; 5=every instruction is specific and actionable with concrete patterns",
    ),
    DimensionDef(
        name="redundancy",
        weight=0.25,
        description="1=duplicates default behavior; 5=entirely unique, teaches the agent something new",
    ),
    DimensionDef(
        name="trigger_quality",
        weight=0.20,
        description="1=no description or triggers everything; 5=precise targeting with clear 'use when' phrasing",
    ),
    DimensionDef(
        name="token_efficiency",
        weight=0.15,
        description="1=over 3000 tokens with low value; 5=high value-to-token ratio",
    ),
    DimensionDef(
        name="content_quality",
        weight=0.15,
        description="1=no structure; 5=organized, has examples, valid references, edge cases covered",
    ),
]

COMMAND_DIMENSIONS = [
    DimensionDef(name="description_quality", weight=0.20, description="Clear, actionable description"),
    DimensionDef(name="instruction_clarity", weight=0.20, description="Instructions are unambiguous"),
    DimensionDef(name="script_integrity", weight=0.15, description="Referenced scripts exist and work"),
    DimensionDef(name="scope", weight=0.10, description="Scope is appropriate, not too broad or narrow"),
    DimensionDef(name="token_efficiency", weight=0.10, description="Good value-to-token ratio"),
    DimensionDef(name="redundancy", weight=0.15, description="Not duplicating built-in or skill behavior"),
    DimensionDef(name="robustness", weight=0.10, description="Handles edge cases and errors"),
]

CLAUDE_MD_DIMENSIONS = [
    DimensionDef(
        name="conciseness",
        weight=0.25,
        description="Would removing any part cause the agent to make mistakes? Ruthlessly prune.",
    ),
    DimensionDef(
        name="signal_to_noise",
        weight=0.25,
        description="Only unique knowledge, not generic advice like 'write clean code'",
    ),
    DimensionDef(
        name="skill_separation",
        weight=0.20,
        description="Domain-specific rules belong in skills (on-demand), not CLAUDE.md (every session)",
    ),
    DimensionDef(
        name="structure",
        weight=0.15,
        description="Clear sections, critical rules marked, scannable",
    ),
    DimensionDef(
        name="conflict_free",
        weight=0.15,
        description="No contradictions with skills or other configuration",
    ),
]

AGENT_DIMENSIONS = [
    DimensionDef(
        name="specificity",
        weight=0.25,
        description="1=vague; 5=every phase has specific steps",
    ),
    DimensionDef(
        name="constraint_clarity",
        weight=0.25,
        description="1=no constraints; 5=body and disallowedTools form a coherent boundary",
    ),
    DimensionDef(
        name="zero_trust_integrity",
        weight=0.20,
        description="1=blind trust; 5=explicit verification, injection-resistant",
    ),
    DimensionDef(
        name="token_efficiency",
        weight=0.15,
        description="1=over 5000 tokens with low value; 5=procedures delegated to skills",
    ),
    DimensionDef(
        name="content_quality",
        weight=0.15,
        description="1=no structure; 5=identity, constraints, procedure, output, failure handling",
    ),
]

HOOKS_DIMENSIONS = [
    DimensionDef(name="safety", weight=0.30, description="No dangerous patterns, no destructive commands"),
    DimensionDef(name="reliability", weight=0.25, description="Scripts exist, commands are well-formed"),
    DimensionDef(name="scope", weight=0.25, description="Hooks are scoped appropriately, not over-broad"),
    DimensionDef(name="performance", weight=0.20, description="Hooks are fast, no unnecessary blocking"),
]

DIMENSIONS_BY_TYPE: dict[str, list[DimensionDef]] = {
    "skill": SKILL_DIMENSIONS,
    "command": COMMAND_DIMENSIONS,
    "claude_md": CLAUDE_MD_DIMENSIONS,
    "agent": AGENT_DIMENSIONS,
    "hooks": HOOKS_DIMENSIONS,
}
