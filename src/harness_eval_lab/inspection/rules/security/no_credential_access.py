from __future__ import annotations

import re

from harness_eval_lab.inspection.types import (
    Location,
    ReportDescriptor,
    RuleCategory,
    RuleContext,
    RuleMeta,
    Severity,
)

_SENSITIVE_PATHS = [
    re.compile(r"~/\.ssh/", re.I),
    re.compile(r"~/\.aws/credentials", re.I),
    re.compile(r"~/\.config/gcloud", re.I),
    re.compile(r"~/\.kube/config", re.I),
    re.compile(r"/etc/shadow", re.I),
    re.compile(r"~/\.netrc", re.I),
    re.compile(r"~/\.env\b"),
    re.compile(r"~/\.docker/config\.json", re.I),
    re.compile(r"~/\.npmrc\b"),
    re.compile(r"~/\.pypirc\b"),
]

_SENSITIVE_ENV_VARS = [
    re.compile(r"\$(?:ANTHROPIC|OPENAI|GEMINI|GOOGLE)_API_KEY"),
    re.compile(r"\$(?:AWS_SECRET_ACCESS_KEY|AWS_SESSION_TOKEN)"),
    re.compile(r"\$(?:DATABASE_URL|DB_PASSWORD)"),
    re.compile(r"\$(?:GITHUB_TOKEN|GH_TOKEN)"),
    re.compile(r"\$(?:SECRET_KEY|PRIVATE_KEY)"),
    re.compile(r"\$SLACK_TOKEN"),
    re.compile(r"\$STRIPE_SECRET_KEY"),
    re.compile(r"\$JWT_SECRET"),
    re.compile(r"\$ENCRYPTION_KEY"),
]

_DANGEROUS_COMMANDS = [
    (re.compile(r"\bsudo\s+"), "sudo"),
    (re.compile(r"\bchmod\s+777\b"), "chmod 777"),
    (re.compile(r"\bchown\s+root\b"), "chown root"),
]


class NoCredentialAccess:
    meta: RuleMeta = RuleMeta(
        id="security/no-credential-access",
        default_severity=Severity.ERROR,
        fixable=False,
        description="Skill should not reference sensitive file paths or environment variables",
        category=RuleCategory.SECURITY,
        messages={
            "sensitive_path": "References sensitive path '{{match}}' at line {{line}}",
            "sensitive_env": "References sensitive environment variable '{{match}}' at line {{line}}",
            "dangerous_command": "Contains dangerous command '{{match}}' at line {{line}}",
        },
    )

    def create(self, context: RuleContext) -> None:
        skill = context.skill
        if not skill.raw_content:
            return

        lines = skill.raw_content.split("\n")

        for i, line in enumerate(lines):
            for pattern in _SENSITIVE_PATHS:
                match = pattern.search(line)
                if match:
                    context.report(
                        ReportDescriptor(
                            message_id="sensitive_path",
                            data={"match": match.group(0), "line": str(i + 1)},
                            location=Location(
                                file=skill.skill_md_path,
                                start_line=i + 1,
                            ),
                        )
                    )
                    break

            for pattern in _SENSITIVE_ENV_VARS:
                match = pattern.search(line)
                if match:
                    context.report(
                        ReportDescriptor(
                            message_id="sensitive_env",
                            data={"match": match.group(0), "line": str(i + 1)},
                            location=Location(
                                file=skill.skill_md_path,
                                start_line=i + 1,
                            ),
                        )
                    )
                    break

            for pattern, label in _DANGEROUS_COMMANDS:
                match = pattern.search(line)
                if match:
                    context.report(
                        ReportDescriptor(
                            message_id="dangerous_command",
                            data={"match": label, "line": str(i + 1)},
                            location=Location(
                                file=skill.skill_md_path,
                                start_line=i + 1,
                            ),
                        )
                    )
                    break
