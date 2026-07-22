from __future__ import annotations

import re
from pathlib import Path

from harness_eval.core.types import ComponentType
from harness_eval.inspection.types import (
    Location,
    ReportDescriptor,
    RuleCategory,
    RuleContext,
    RuleMeta,
    Severity,
)

_SKILL_REF_PATTERNS = [
    re.compile(r"/(\w[\w-]+)(?:\s|$|[),\]])"),
    re.compile(r"(?:skill|command)[:\s]+[\"']?(\w[\w-]+)[\"']?", re.IGNORECASE),
    re.compile(
        r"(?:invokes?|calls?|triggers?|runs?)\s+[\"'`]?/?(\w[\w-]+)[\"'`]?",
        re.IGNORECASE,
    ),
]


def _is_referenced(name: str, text: str) -> bool:
    """Check if a skill name appears in the given text via reference patterns or plain mention."""
    for pattern in _SKILL_REF_PATTERNS:
        for match in pattern.finditer(text):
            if match.group(1) == name:
                return True
    # Also check plain name mention (e.g. in CLAUDE.md lists or prose)
    return bool(re.search(rf"\b{re.escape(name)}\b", text))


def _find_project_root(skill_path: str) -> Path | None:
    """Walk up from a skill path to find the project root (containing CLAUDE.md or .claude/)."""
    current = Path(skill_path).resolve()
    for _ in range(10):
        if (current / "CLAUDE.md").is_file() or (current / ".claude").is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def _read_claude_md(project_root: Path) -> str:
    """Read the CLAUDE.md file from the project root, if it exists."""
    claude_md = project_root / "CLAUDE.md"
    if claude_md.is_file():
        try:
            return claude_md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass
    return ""


def _read_agent_bodies(project_root: Path) -> list[str]:
    """Read all agent .md files from .claude/agents/."""
    bodies: list[str] = []
    agents_dir = project_root / ".claude" / "agents"
    if not agents_dir.is_dir():
        return bodies
    for f in sorted(agents_dir.glob("*.md")):
        if f.is_file():
            try:
                bodies.append(f.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                continue
    return bodies


class OrphanSkills:
    meta = RuleMeta(
        id="content/orphan-skills",
        default_severity=Severity.WARNING,
        fixable=False,
        description="Skills not referenced by any command, CLAUDE.md, or agent waste context budget",
        category=RuleCategory.CONTENT,
        messages={
            "orphan": "Skill '{{name}}' is not referenced by any command, CLAUDE.md, or agent",
        },
        target_type=ComponentType.SKILL,
    )

    def create(self, context: RuleContext) -> None:
        if context.scan_state.get("orphan_skills_checked"):
            return
        context.scan_state["orphan_skills_checked"] = True

        all_skills = context.all_skills
        if len(all_skills) <= 1:
            return

        # Collect all reference texts from commands, agents, and CLAUDE.md
        reference_texts: list[str] = []
        for cmd in context.all_commands:
            if cmd.body:
                reference_texts.append(cmd.body)

        # Read CLAUDE.md and agent bodies directly from the project
        project_root = _find_project_root(all_skills[0].dir_path)
        if project_root is not None:
            claude_md_content = _read_claude_md(project_root)
            if claude_md_content:
                reference_texts.append(claude_md_content)

            for body in _read_agent_bodies(project_root):
                reference_texts.append(body)

        combined = "\n".join(reference_texts)

        for skill in all_skills:
            if not _is_referenced(skill.dir_name, combined):
                context.report(
                    ReportDescriptor(
                        message_id="orphan",
                        data={"name": skill.dir_name},
                        location=Location(file=skill.skill_md_path, start_line=1),
                    )
                )
