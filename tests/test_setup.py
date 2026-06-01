"""Tests for setup discovery."""

from __future__ import annotations

import pytest

from harness_eval_lab.core.setup import discover_setup
from harness_eval_lab.core.types import ComponentType


def test_discover_setup_a(setup_a_path: str) -> None:
    setup = discover_setup("setup-a", setup_a_path)
    assert setup.name == "setup-a"
    assert setup.fingerprint
    assert setup.total_tokens > 0


def test_discover_claude_md(setup_a_path: str) -> None:
    setup = discover_setup("setup-a", setup_a_path)
    claude_mds = setup.by_type(ComponentType.CLAUDE_MD)
    assert len(claude_mds) == 1
    assert "Project Instructions" in claude_mds[0].content


def test_discover_skills(setup_a_path: str) -> None:
    setup = discover_setup("setup-a", setup_a_path)
    skills = setup.by_type(ComponentType.SKILL)
    assert len(skills) == 1
    assert skills[0].name == "code-review"
    assert skills[0].frontmatter is not None
    assert skills[0].frontmatter["name"] == "code-review"


def test_discover_commands(setup_a_path: str) -> None:
    setup = discover_setup("setup-a", setup_a_path)
    commands = setup.by_type(ComponentType.COMMAND)
    assert len(commands) == 1
    assert commands[0].name == "review"


def test_discover_hooks(setup_a_path: str) -> None:
    setup = discover_setup("setup-a", setup_a_path)
    hooks = setup.by_type(ComponentType.HOOKS)
    assert len(hooks) == 1
    assert "PreToolUse" in hooks[0].content


def test_setup_b_has_more_components(setup_a_path: str, setup_b_path: str) -> None:
    setup_a = discover_setup("setup-a", setup_a_path)
    setup_b = discover_setup("setup-b", setup_b_path)
    assert len(setup_b.components) > len(setup_a.components)


def test_setup_b_skills(setup_b_path: str) -> None:
    setup = discover_setup("setup-b", setup_b_path)
    skills = setup.by_type(ComponentType.SKILL)
    skill_names = {s.name for s in skills}
    assert skill_names == {"code-review", "security-scan"}


def test_setup_b_commands(setup_b_path: str) -> None:
    setup = discover_setup("setup-b", setup_b_path)
    commands = setup.by_type(ComponentType.COMMAND)
    cmd_names = {c.name for c in commands}
    assert cmd_names == {"review", "deploy"}


def test_discover_nonexistent_path() -> None:
    with pytest.raises(FileNotFoundError):
        discover_setup("bad", "/nonexistent/path")
