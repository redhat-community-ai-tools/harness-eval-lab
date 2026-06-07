"""Tests for system-level analysis (Layer 3)."""

from __future__ import annotations

from pathlib import Path

from harness_eval_lab.analysis.budget import analyze_budget
from harness_eval_lab.analysis.dependencies import analyze_dependencies
from harness_eval_lab.analysis.system import analyze_system
from harness_eval_lab.analysis.triggers import analyze_triggers
from harness_eval_lab.core.setup import discover_setup

FIXTURES = Path(__file__).parent / "fixtures"


class TestBudgetAnalysis:
    def test_budget_totals(self, setup_a_path: str) -> None:
        setup = discover_setup("a", setup_a_path)
        budget = analyze_budget(setup)
        assert budget.total_tokens > 0
        assert budget.always_loaded_tokens + budget.on_demand_tokens == budget.total_tokens

    def test_always_loaded_ratio(self, setup_a_path: str) -> None:
        setup = discover_setup("a", setup_a_path)
        budget = analyze_budget(setup)
        assert 0.0 <= budget.always_loaded_ratio <= 1.0

    def test_by_type_sums_to_total(self, setup_a_path: str) -> None:
        setup = discover_setup("a", setup_a_path)
        budget = analyze_budget(setup)
        assert sum(budget.by_type.values()) == budget.total_tokens

    def test_heaviest_component(self, setup_b_path: str) -> None:
        setup = discover_setup("b", setup_b_path)
        budget = analyze_budget(setup)
        assert budget.heaviest_component_name
        assert budget.heaviest_component_ratio > 0

    def test_setup_b_has_more_tokens(
        self, setup_a_path: str, setup_b_path: str,
    ) -> None:
        a = analyze_budget(discover_setup("a", setup_a_path))
        b = analyze_budget(discover_setup("b", setup_b_path))
        assert b.total_tokens > a.total_tokens


class TestTriggerAnalysis:
    def test_skill_counts(self, setup_b_path: str) -> None:
        setup = discover_setup("b", setup_b_path)
        triggers = analyze_triggers(setup)
        assert triggers.skill_count == 2
        assert triggers.skills_with_description == 2

    def test_missing_use_when(self, setup_a_path: str) -> None:
        setup = discover_setup("a", setup_a_path)
        triggers = analyze_triggers(setup)
        assert "code-review" in triggers.missing_use_when

    def test_no_overlap_in_distinct_skills(self, setup_b_path: str) -> None:
        setup = discover_setup("b", setup_b_path)
        triggers = analyze_triggers(setup)
        for _, _, sim in triggers.overlap_pairs:
            assert sim >= 0.50


class TestDependencyAnalysis:
    def test_no_broken_refs_in_fixtures(self, setup_a_path: str) -> None:
        setup = discover_setup("a", setup_a_path)
        deps = analyze_dependencies(setup)
        assert len(deps.broken_refs) == 0

    def test_finds_components(self, setup_b_path: str) -> None:
        setup = discover_setup("b", setup_b_path)
        deps = analyze_dependencies(setup)
        assert isinstance(deps.edges, list)
        assert isinstance(deps.orphan_components, list)


class TestSystemAnalysis:
    def test_analyze_produces_report(self, setup_a_path: str) -> None:
        setup = discover_setup("a", setup_a_path)
        report = analyze_system(setup)
        assert report.setup_name == "a"
        assert report.component_count == len(setup.components)
        assert report.budget.total_tokens > 0

    def test_findings_generated(self, setup_a_path: str) -> None:
        setup = discover_setup("a", setup_a_path)
        report = analyze_system(setup)
        assert isinstance(report.findings, list)


class TestReportOutput:
    def test_terminal_format(self, setup_a_path: str) -> None:
        from harness_eval_lab.analysis.system import analyze_system
        from harness_eval_lab.output.report import format_terminal

        setup = discover_setup("a", setup_a_path)
        system = analyze_system(setup)
        output = format_terminal(system, [])
        assert "Setup Assessment" in output
        assert "Token Budget" in output

    def test_json_format(self, setup_a_path: str) -> None:
        import json

        from harness_eval_lab.analysis.system import analyze_system
        from harness_eval_lab.output.report import format_json

        setup = discover_setup("a", setup_a_path)
        system = analyze_system(setup)
        output = format_json(system, [])
        parsed = json.loads(output)
        assert "budget" in parsed
        assert parsed["setup"] == "a"
