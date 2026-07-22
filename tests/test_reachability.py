"""Tests for reachability analysis."""

from __future__ import annotations

from harness_eval.analysis.component_graph import ComponentGraph, GraphEdge, GraphNode
from harness_eval.analysis.reachability import compute_reachability
from harness_eval.core.types import ComponentType


def _skill_node(name: str) -> GraphNode:
    return GraphNode(
        name=name,
        component_type=ComponentType.SKILL,
        file_path=f"skills/{name}/SKILL.md",
    )


class TestReachability:
    def test_unreachable_orphan(self) -> None:
        graph = ComponentGraph()
        graph.nodes["a"] = _skill_node("a")
        graph.nodes["b"] = _skill_node("b")

        result = compute_reachability(graph, "skills/b/SKILL.md")
        assert result.reachable is False

    def test_reachable_via_edge(self) -> None:
        graph = ComponentGraph()
        graph.nodes["a"] = _skill_node("a")
        graph.nodes["b"] = _skill_node("b")
        graph.edges.append(GraphEdge(source="a", target="b", edge_type="references"))

        result = compute_reachability(graph, "skills/b/SKILL.md")
        assert result.reachable is True
        assert result.trigger_breadth == "broad"

    def test_unknown_file_defaults_reachable(self) -> None:
        graph = ComponentGraph()
        graph.nodes["a"] = _skill_node("a")

        result = compute_reachability(graph, "skills/nonexistent/SKILL.md")
        assert result.reachable is True
        assert result.trigger_breadth == "unknown"

    def test_narrow_trigger_breadth(self) -> None:
        graph = ComponentGraph()
        graph.nodes["a"] = _skill_node("a")

        descriptions = {"a": "Use when the user asks for security analysis"}
        result = compute_reachability(graph, "skills/a/SKILL.md", descriptions)
        assert result.reachable is True
        assert result.trigger_breadth == "narrow"

    def test_broad_trigger_breadth(self) -> None:
        graph = ComponentGraph()
        graph.nodes["a"] = _skill_node("a")

        descriptions = {"a": "General purpose skill for everything"}
        result = compute_reachability(graph, "skills/a/SKILL.md", descriptions)
        assert result.reachable is True
        assert result.trigger_breadth == "broad"
