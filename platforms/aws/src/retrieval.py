from __future__ import annotations

import re
from collections.abc import Iterable

from .authorization import normalize
from .models import AccessContext


INJECTION_PATTERNS = (
    r"ignore (all |any )?previous instructions",
    r"reveal (the )?(system prompt|credentials|secrets)",
    r"bypass (authorization|policy|access)",
    r"submit the claim now",
)


def has_prompt_injection(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in INJECTION_PATTERNS)


def sanitize_untrusted_text(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if has_prompt_injection(line):
            lines.append("[UNTRUSTED INSTRUCTION REMOVED]")
        else:
            lines.append(line)
    return "\n".join(lines)


def _terms(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9-]+", text.lower()))


def retrieve_policies(
    ctx: AccessContext,
    question: str,
    policies: Iterable[dict],
    limit: int = 4,
) -> list[dict]:
    """Authorization filter first; deterministic relevance rank second."""
    eligible = []
    for policy in policies:
        if not policy.get("approved", False) or not policy.get("current", False):
            continue
        roles = {normalize(x) for x in policy.get("allowed_roles", [])}
        if roles and normalize(ctx.role) not in roles:
            continue
        purposes = {normalize(x) for x in policy.get("allowed_purposes", [])}
        if purposes and normalize(ctx.purpose) not in purposes:
            continue
        safe = dict(policy)
        safe["prompt_injection_flag"] = has_prompt_injection(policy.get("text", ""))
        safe["text"] = sanitize_untrusted_text(policy.get("text", ""))
        eligible.append(safe)

    query_terms = _terms(question)
    for policy in eligible:
        policy["score"] = len(query_terms & _terms(policy["title"] + " " + policy["text"]))
    return sorted(eligible, key=lambda item: (-item["score"], item["policy_id"]))[:limit]
