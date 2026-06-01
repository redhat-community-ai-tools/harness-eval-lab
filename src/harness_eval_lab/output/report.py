"""Report generation: structured output for assess results."""

from __future__ import annotations

import json

from harness_eval_lab.analysis.system import SystemReport
from harness_eval_lab.inspection.types import InspectionResult


def score_to_stars(score: float) -> str:
    rounded = max(1, min(5, round(score)))
    return "★" * rounded + "☆" * (5 - rounded)


def score_to_verdict(score: float) -> str:
    rounded = round(score)
    if rounded >= 4:
        return "HEALTHY"
    if rounded == 3:
        return "NEEDS WORK"
    return "PROBLEMATIC"


def format_terminal(
    system: SystemReport,
    inspection_results: list[InspectionResult],
) -> str:
    """Format a full assessment report for terminal output."""
    lines: list[str] = []

    lines.append(f"{'=' * 60}")
    lines.append(f"Setup Assessment: {system.setup_name}")
    lines.append(f"{'=' * 60}")
    lines.append(f"Components: {system.component_count}")
    lines.append(f"Total tokens: {system.budget.total_tokens}")
    lines.append("")

    lines.append("Dimension Scores:")
    lines.append(f"{'─' * 60}")
    overall_scores = []
    for dim in ["soundness", "safety", "coherence", "efficiency", "impact"]:
        score = system.dimension_scores.get(dim, 0.0)
        stars = score_to_stars(score)
        verdict = score_to_verdict(score)
        if dim == "impact":
            lines.append(f"  {dim:<12} {stars}  (requires task probing)")
        else:
            lines.append(f"  {dim:<12} {stars}  {score}/5  [{verdict}]")
            overall_scores.append(score)

    if overall_scores:
        avg = sum(overall_scores) / len(overall_scores)
        lines.append(f"{'─' * 60}")
        lines.append(
            f"  {'overall':<12} {score_to_stars(avg)}  "
            f"{avg:.1f}/5  [{score_to_verdict(avg)}]"
        )

    lines.append("")
    lines.append("Token Budget:")
    lines.append(f"{'─' * 60}")
    lines.append(
        f"  Always-loaded (CLAUDE.md, hooks): "
        f"{system.budget.always_loaded_tokens} tokens "
        f"({system.budget.always_loaded_ratio:.0%})"
    )
    lines.append(
        f"  On-demand (skills, commands, agents): "
        f"{system.budget.on_demand_tokens} tokens "
        f"({1 - system.budget.always_loaded_ratio:.0%})"
    )
    if system.budget.by_type:
        lines.append("  By type:")
        for type_name, tokens in sorted(
            system.budget.by_type.items(), key=lambda x: x[1], reverse=True
        ):
            pct = tokens / system.budget.total_tokens * 100 if system.budget.total_tokens else 0
            lines.append(f"    {type_name:<12} {tokens:>6} tokens ({pct:.0f}%)")

    if system.triggers.skill_count > 0:
        lines.append("")
        lines.append("Trigger Analysis:")
        lines.append(f"{'─' * 60}")
        lines.append(
            f"  {system.triggers.skills_with_description}/{system.triggers.skill_count} "
            f"skills have descriptions"
        )
        if system.triggers.missing_use_when:
            lines.append(
                f"  {len(system.triggers.missing_use_when)} skills lack "
                f"activation context ('use when' phrasing):"
            )
            for name in system.triggers.missing_use_when:
                lines.append(f"    - {name}")
        if system.triggers.overlap_pairs:
            lines.append(f"  {len(system.triggers.overlap_pairs)} trigger overlap(s) detected:")
            for name_a, name_b, sim in system.triggers.overlap_pairs:
                lines.append(f"    - {name_a} <-> {name_b} ({sim:.0%} similar)")

    if system.dependencies.broken_refs or system.dependencies.orphan_components:
        lines.append("")
        lines.append("Dependencies:")
        lines.append(f"{'─' * 60}")
        if system.dependencies.broken_refs:
            lines.append(f"  {len(system.dependencies.broken_refs)} broken reference(s):")
            for edge in system.dependencies.broken_refs:
                lines.append(
                    f"    - {edge.source_type}/{edge.source_name} "
                    f"references missing {edge.target_type}/{edge.target_name}"
                )
        if system.dependencies.orphan_components:
            lines.append(f"  {len(system.dependencies.orphan_components)} orphan component(s):")
            for name in system.dependencies.orphan_components:
                lines.append(f"    - {name}")

    if system.findings:
        lines.append("")
        lines.append("Findings:")
        lines.append(f"{'─' * 60}")
        for finding in system.findings:
            lines.append(f"  [!] {finding}")

    total_errors = sum(r.error_count for r in inspection_results)
    total_warnings = sum(r.warning_count for r in inspection_results)
    if total_errors or total_warnings:
        lines.append("")
        lines.append("Inspection Summary:")
        lines.append(f"{'─' * 60}")
        lines.append(
            f"  {len(inspection_results)} components inspected, "
            f"{total_errors} errors, {total_warnings} warnings"
        )
        for r in inspection_results:
            if r.diagnostics:
                lines.append(f"  {r.target_type}/{r.target_name}:")
                for d in r.diagnostics:
                    icon = "X" if d.severity.value == "error" else "!"
                    lines.append(f"    [{icon}] {d.rule_id}: {d.message}")

    lines.append("")
    return "\n".join(lines)


def format_json(
    system: SystemReport,
    inspection_results: list[InspectionResult],
) -> str:
    """Format a full assessment report as JSON."""
    output = {
        "setup": system.setup_name,
        "component_count": system.component_count,
        "dimension_scores": system.dimension_scores,
        "overall": (
            sum(v for k, v in system.dimension_scores.items() if k != "impact")
            / max(1, sum(1 for k in system.dimension_scores if k != "impact"))
        ),
        "budget": {
            "total_tokens": system.budget.total_tokens,
            "always_loaded": system.budget.always_loaded_tokens,
            "on_demand": system.budget.on_demand_tokens,
            "always_loaded_ratio": round(system.budget.always_loaded_ratio, 2),
            "by_type": system.budget.by_type,
            "heaviest": system.budget.heaviest_component_name,
        },
        "triggers": {
            "skill_count": system.triggers.skill_count,
            "with_description": system.triggers.skills_with_description,
            "missing_use_when": system.triggers.missing_use_when,
            "overlaps": [
                {"a": a, "b": b, "similarity": round(s, 2)}
                for a, b, s in system.triggers.overlap_pairs
            ],
        },
        "dependencies": {
            "total_edges": len(system.dependencies.edges),
            "broken": [
                {
                    "source": f"{e.source_type}/{e.source_name}",
                    "target": f"{e.target_type}/{e.target_name}",
                }
                for e in system.dependencies.broken_refs
            ],
            "orphans": system.dependencies.orphan_components,
        },
        "findings": system.findings,
        "inspection": [
            {
                "target": f"{r.target_type}/{r.target_name}",
                "tokens": r.tokens,
                "errors": r.error_count,
                "warnings": r.warning_count,
                "findings": [
                    {
                        "rule": d.rule_id,
                        "severity": d.severity.value,
                        "message": d.message,
                    }
                    for d in r.diagnostics
                ],
            }
            for r in inspection_results
        ],
    }
    return json.dumps(output, indent=2)
