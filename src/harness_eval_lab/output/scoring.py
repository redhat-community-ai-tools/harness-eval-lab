"""Compute a composite health score from inspection results.

Organizes rules into weighted tiers and produces a single 0-1 number.
Inspired by SDG Hub's three-tier composite scoring pattern.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from harness_eval_lab.inspection.types import InspectionResult, RuleCategory

TIER_DEFINITIONS: dict[str, dict] = {
    "security": {
        "weight": 0.35,
        "categories": {RuleCategory.SECURITY},
    },
    "structure": {
        "weight": 0.25,
        "categories": {RuleCategory.STRUCTURAL, RuleCategory.FRONTMATTER},
    },
    "content": {
        "weight": 0.25,
        "categories": {RuleCategory.CONTENT},
    },
    "best_practices": {
        "weight": 0.15,
        "categories": {RuleCategory.BEST_PRACTICES},
    },
}


@dataclass(frozen=True)
class TierScore:
    name: str
    weight: float
    rules_passed: int
    rules_total: int
    score: float


@dataclass(frozen=True)
class ScoreReport:
    tiers: list[TierScore]
    composite: float
    components_scanned: int
    rules_checked: int


def compute_score(results: list[InspectionResult]) -> ScoreReport:
    """Compute a composite score from inspection results."""
    tier_passed: dict[str, int] = {}
    tier_total: dict[str, int] = {}

    rule_category_map: dict[str, RuleCategory] = {}
    for r in results:
        for rr in r.rules_run:
            parts = rr.rule_id.split("/", 1)
            if len(parts) == 2:
                prefix = parts[0]
                cat = _prefix_to_category(prefix)
                if cat:
                    rule_category_map[rr.rule_id] = cat

    for r in results:
        for rr in r.rules_run:
            cat = rule_category_map.get(rr.rule_id)
            if cat is None:
                continue
            tier_name = _category_to_tier(cat)
            if tier_name is None:
                continue
            tier_total[tier_name] = tier_total.get(tier_name, 0) + 1
            if rr.passed:
                tier_passed[tier_name] = tier_passed.get(tier_name, 0) + 1

    tiers: list[TierScore] = []
    composite = 0.0

    for tier_name, tier_def in TIER_DEFINITIONS.items():
        passed = tier_passed.get(tier_name, 0)
        total = tier_total.get(tier_name, 0)
        score = passed / total if total > 0 else 1.0
        ts = TierScore(
            name=tier_name,
            weight=tier_def["weight"],
            rules_passed=passed,
            rules_total=total,
            score=round(score, 4),
        )
        tiers.append(ts)
        composite += score * tier_def["weight"]

    total_rules = sum(len(r.rules_run) for r in results)

    return ScoreReport(
        tiers=tiers,
        composite=round(composite, 4),
        components_scanned=len(results),
        rules_checked=total_rules,
    )


def compare_scores(
    before: ScoreReport,
    after: ScoreReport,
    threshold: float = 0.8,
) -> tuple[bool, str]:
    """Compare before/after scores. Returns (passed, markdown_report)."""
    before_tiers = {t.name: t for t in before.tiers}
    after_tiers = {t.name: t for t in after.tiers}

    lines = ["## Setup Health Score Gate", ""]
    lines.append("| Tier | Before | After | Delta |")
    lines.append("|------|--------|-------|-------|")

    any_regression = False
    for tier_name in TIER_DEFINITIONS:
        b = before_tiers.get(tier_name)
        a = after_tiers.get(tier_name)
        b_score = b.score if b else 0.0
        a_score = a.score if a else 0.0
        delta = a_score - b_score
        icon = "+" if delta > 0 else ("-" if delta < 0 else "=")
        status = "PASS" if delta >= 0 else "REGRESSED"
        if delta < 0:
            any_regression = True
        lines.append(
            f"| {tier_name} | {b_score:.2f} | {a_score:.2f} | {icon}{abs(delta):.2f} {status} |"
        )

    delta_composite = after.composite - before.composite
    icon = "+" if delta_composite > 0 else ("-" if delta_composite < 0 else "=")
    lines.append(
        f"| **composite** | **{before.composite:.2f}** | **{after.composite:.2f}** "
        f"| **{icon}{abs(delta_composite):.2f}** |"
    )
    lines.append("")

    passed = True
    if any_regression:
        lines.append("**FAILED:** one or more tiers regressed.")
        passed = False
    if after.composite < threshold:
        lines.append(
            f"**FAILED:** composite {after.composite:.2f} below threshold {threshold:.2f}."
        )
        passed = False
    if passed:
        lines.append("**PASSED**")

    return passed, "\n".join(lines)


def score_to_json(report: ScoreReport) -> str:
    """Serialize a ScoreReport to JSON."""
    return json.dumps(
        {
            "composite": report.composite,
            "components_scanned": report.components_scanned,
            "rules_checked": report.rules_checked,
            "tiers": {
                t.name: {
                    "weight": t.weight,
                    "score": t.score,
                    "rules_passed": t.rules_passed,
                    "rules_total": t.rules_total,
                }
                for t in report.tiers
            },
        },
        indent=2,
    )


def score_from_json(data: str) -> ScoreReport:
    """Deserialize a ScoreReport from JSON."""
    obj = json.loads(data)
    tiers = []
    for name, t in obj["tiers"].items():
        tiers.append(
            TierScore(
                name=name,
                weight=t["weight"],
                score=t["score"],
                rules_passed=t["rules_passed"],
                rules_total=t["rules_total"],
            )
        )
    return ScoreReport(
        tiers=tiers,
        composite=obj["composite"],
        components_scanned=obj["components_scanned"],
        rules_checked=obj["rules_checked"],
    )


def _prefix_to_category(prefix: str) -> RuleCategory | None:
    mapping = {
        "security": RuleCategory.SECURITY,
        "structural": RuleCategory.STRUCTURAL,
        "frontmatter": RuleCategory.FRONTMATTER,
        "content": RuleCategory.CONTENT,
        "commands": RuleCategory.BEST_PRACTICES,
        "claude-md": RuleCategory.CONTENT,
        "hooks": RuleCategory.STRUCTURAL,
        "agents": RuleCategory.BEST_PRACTICES,
    }
    return mapping.get(prefix)


def _category_to_tier(cat: RuleCategory) -> str | None:
    for tier_name, tier_def in TIER_DEFINITIONS.items():
        if cat in tier_def["categories"]:
            return tier_name
    return None
