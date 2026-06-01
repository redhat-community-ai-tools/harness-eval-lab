from __future__ import annotations

from harness_eval_lab.core.types import ComponentType
from harness_eval_lab.inspection.types import (
    Location,
    ReportDescriptor,
    RuleCategory,
    RuleContext,
    RuleMeta,
    Severity,
)
from harness_eval_lab.utils.similarity import tfidf_similarity

SIMILARITY_THRESHOLD = 0.85

_all_command_texts: dict[str, str] = {}
_duplicates_reported: set[tuple[str, str]] = set()


def reset_command_duplicate_state() -> None:
    _all_command_texts.clear()
    _duplicates_reported.clear()


class CommandDuplicateDetection:
    meta = RuleMeta(
        id="command/duplicate-detection",
        default_severity=Severity.WARNING,
        fixable=False,
        description="Detect near-duplicate commands",
        category=RuleCategory.CONTENT,
        messages={
            "duplicate": "{{similarity}}% similar to command '{{other}}' — consider merging",
        },
        target_type=ComponentType.COMMAND,
    )

    def create(self, context: RuleContext) -> None:
        cmd = context.command
        if cmd is None or not cmd.body:
            return

        cmd_key = cmd.dir_name
        _all_command_texts[cmd_key] = cmd.body

        for other_name, other_text in _all_command_texts.items():
            if other_name == cmd_key:
                continue

            pair = tuple(sorted([cmd_key, other_name]))
            if pair in _duplicates_reported:
                continue

            similarity = tfidf_similarity(cmd.body, other_text)
            if similarity >= SIMILARITY_THRESHOLD:
                _duplicates_reported.add(pair)
                context.report(ReportDescriptor(
                    message_id="duplicate",
                    data={
                        "similarity": str(int(similarity * 100)),
                        "other": other_name,
                    },
                    location=Location(file=cmd.command_md_path, start_line=1),
                ))
