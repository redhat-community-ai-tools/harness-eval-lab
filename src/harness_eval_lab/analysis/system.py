"""System-level analysis: evaluate the setup as a whole, not component-by-component."""

from __future__ import annotations

from dataclasses import dataclass, field

from harness_eval_lab.analysis.budget import BudgetReport, analyze_budget
from harness_eval_lab.analysis.dependencies import DependencyReport, analyze_dependencies
from harness_eval_lab.analysis.triggers import TriggerReport, analyze_triggers
from harness_eval_lab.core.types import Setup
from harness_eval_lab.inspection.types import InspectionResult


@dataclass
class SystemReport:
    """Complete system-level analysis of a setup."""

    setup_name: str
    component_count: int
    budget: BudgetReport
    triggers: TriggerReport
    dependencies: DependencyReport
    dimension_scores: dict[str, float] = field(default_factory=dict)
    findings: list[str] = field(default_factory=list)

    def compute_scores(
        self, inspection_results: list[InspectionResult] | None = None,
    ) -> None:
        """Compute the 5 dimension scores from all available data."""
        self.dimension_scores["soundness"] = self._score_soundness(inspection_results)
        self.dimension_scores["safety"] = self._score_safety(inspection_results)
        self.dimension_scores["coherence"] = self._score_coherence(inspection_results)
        self.dimension_scores["efficiency"] = self._score_efficiency()
        self.dimension_scores["impact"] = 0.0  # requires Layer 4 (task probing)

    def _score_soundness(self, results: list[InspectionResult] | None) -> float:
        if not results:
            return 0.0
        soundness_rules = {"structural/", "frontmatter/", "parser"}
        total = 0
        passed = 0
        for r in results:
            total += 1
            has_soundness_error = any(
                d.severity.value == "error"
                and any(d.rule_id.startswith(p) for p in soundness_rules)
                for d in r.diagnostics
            )
            if not has_soundness_error:
                passed += 1
        return round((passed / total) * 5, 1) if total else 5.0

    def _score_safety(self, results: list[InspectionResult] | None) -> float:
        if not results:
            return 0.0
        safety_rules = {"security/", "command/no-credential", "command/no-prompt",
                        "agent/no-credential", "agent/no-prompt", "hooks/"}
        total_issues = 0
        for r in results:
            for d in r.diagnostics:
                if d.severity.value == "error" and any(
                    d.rule_id.startswith(p) for p in safety_rules
                ):
                    total_issues += 1
        if total_issues == 0:
            return 5.0
        if total_issues <= 2:
            return 3.0
        return 1.0

    def _score_coherence(self, results: list[InspectionResult] | None) -> float:
        score = 5.0

        if self.triggers.overlap_pairs:
            score -= min(len(self.triggers.overlap_pairs) * 0.5, 2.0)

        if self.dependencies.broken_refs:
            score -= min(len(self.dependencies.broken_refs) * 1.0, 2.0)

        if results:
            coherence_rules = {"content/duplicate", "claude-md/skill-duplication",
                               "command/skill-overlap", "command/duplicate"}
            for r in results:
                for d in r.diagnostics:
                    if any(d.rule_id.startswith(p) for p in coherence_rules):
                        score -= 0.3

        return round(max(score, 1.0), 1)

    def _score_efficiency(self) -> float:
        score = 5.0

        if self.budget.always_loaded_ratio > 0.7:
            score -= 2.0
            self.findings.append(
                f"Inverted budget: {self.budget.always_loaded_ratio:.0%} of tokens are "
                f"always-loaded (CLAUDE.md). Most content should be in on-demand skills."
            )
        elif self.budget.always_loaded_ratio > 0.5:
            score -= 1.0

        if self.budget.heaviest_component_ratio > 0.5:
            score -= 1.0
            self.findings.append(
                f"One component ({self.budget.heaviest_component_name}) uses "
                f"{self.budget.heaviest_component_ratio:.0%} of the total token budget."
            )

        if self.triggers.overlap_pairs:
            score -= min(len(self.triggers.overlap_pairs) * 0.3, 1.5)
            for pair in self.triggers.overlap_pairs:
                self.findings.append(
                    f"Trigger overlap: '{pair[0]}' and '{pair[1]}' have "
                    f"{pair[2]:.0%} description similarity, may load together."
                )

        return round(max(score, 1.0), 1)


def analyze_system(setup: Setup) -> SystemReport:
    """Run all system-level analyses on a setup."""
    budget = analyze_budget(setup)
    triggers = analyze_triggers(setup)
    dependencies = analyze_dependencies(setup)

    report = SystemReport(
        setup_name=setup.name,
        component_count=len(setup.components),
        budget=budget,
        triggers=triggers,
        dependencies=dependencies,
    )

    return report
