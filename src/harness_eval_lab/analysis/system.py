"""System-level analysis: evaluate the setup as a whole, not component-by-component."""

from __future__ import annotations

from dataclasses import dataclass, field

from harness_eval_lab.analysis.budget import BudgetReport, analyze_budget
from harness_eval_lab.analysis.dependencies import DependencyReport, analyze_dependencies
from harness_eval_lab.analysis.triggers import TriggerReport, analyze_triggers
from harness_eval_lab.core.types import Setup


@dataclass
class SystemReport:
    """Complete system-level analysis of a setup."""

    setup_name: str
    component_count: int
    budget: BudgetReport
    triggers: TriggerReport
    dependencies: DependencyReport
    findings: list[str] = field(default_factory=list)


def analyze_system(setup: Setup) -> SystemReport:
    """Run all system-level analyses on a setup."""
    budget = analyze_budget(setup)
    triggers = analyze_triggers(setup)
    dependencies = analyze_dependencies(setup)

    findings: list[str] = []

    if budget.always_loaded_ratio > 0.7:
        findings.append(
            f"Inverted budget: {budget.always_loaded_ratio:.0%} of tokens are "
            f"always-loaded (CLAUDE.md). Most content should be in on-demand skills."
        )
    elif budget.always_loaded_ratio > 0.5:
        findings.append(
            f"Heavy always-loaded ratio: {budget.always_loaded_ratio:.0%} of tokens "
            f"are always-loaded. Consider moving content to on-demand skills."
        )

    if budget.heaviest_component_ratio > 0.5:
        findings.append(
            f"One component ({budget.heaviest_component_name}) uses "
            f"{budget.heaviest_component_ratio:.0%} of the total token budget."
        )

    for pair in triggers.overlap_pairs:
        findings.append(
            f"Trigger overlap: '{pair[0]}' and '{pair[1]}' have "
            f"{pair[2]:.0%} description similarity, may load together."
        )

    return SystemReport(
        setup_name=setup.name,
        component_count=len(setup.components),
        budget=budget,
        triggers=triggers,
        dependencies=dependencies,
        findings=findings,
    )
