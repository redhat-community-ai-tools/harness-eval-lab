from __future__ import annotations

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

_all_skill_texts: dict[str, str] = {}
_duplicates_reported: set[tuple[str, str]] = set()


def reset_duplicate_state() -> None:
    _all_skill_texts.clear()
    _duplicates_reported.clear()


class DuplicateDetection:
    meta: RuleMeta = RuleMeta(
        id="content/duplicate-detection",
        default_severity=Severity.WARNING,
        fixable=False,
        description="Detect near-duplicate skills",
        category=RuleCategory.CONTENT,
        messages={
            "duplicate": "{{similarity}}% similar to '{{other}}' — consider merging",
        },
    )

    def create(self, context: RuleContext) -> None:
        skill = context.skill
        if not skill.body:
            return

        skill_key = skill.dir_name
        _all_skill_texts[skill_key] = skill.body

        for other_name, other_text in _all_skill_texts.items():
            if other_name == skill_key:
                continue

            pair = tuple(sorted([skill_key, other_name]))
            if pair in _duplicates_reported:
                continue

            similarity = tfidf_similarity(skill.body, other_text)
            if similarity >= SIMILARITY_THRESHOLD:
                _duplicates_reported.add(pair)
                context.report(
                    ReportDescriptor(
                        message_id="duplicate",
                        data={
                            "similarity": str(int(similarity * 100)),
                            "other": other_name,
                        },
                        location=Location(
                            file=skill.skill_md_path,
                            start_line=1,
                        ),
                    )
                )
