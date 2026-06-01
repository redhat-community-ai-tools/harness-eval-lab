"""Core types for harness-eval-lab."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ComponentType(StrEnum):
    SKILL = "skill"
    COMMAND = "command"
    CLAUDE_MD = "claude_md"
    HOOKS = "hooks"
    AGENT = "agent"
    MCP_CONFIG = "mcp_config"


@dataclass(frozen=True)
class ParsedComponent:
    """A parsed component with its raw content and metadata."""

    component_type: ComponentType
    name: str
    path: str
    content: str
    frontmatter: dict[str, object] | None = None
    token_count: int = 0


@dataclass(frozen=True)
class Setup:
    """A complete agent setup discovered from a directory."""

    name: str
    path: str
    fingerprint: str
    components: list[ParsedComponent] = field(default_factory=list)
    total_tokens: int = 0

    def by_type(self, component_type: ComponentType) -> list[ParsedComponent]:
        return [c for c in self.components if c.component_type == component_type]
