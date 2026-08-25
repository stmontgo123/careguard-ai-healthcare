import re

INJECTION_PATTERNS = [
    r"ignore\s+(?:all\s+)?(?:previous|prior)?\s*instructions",
    r"reveal (all|restricted|private|secret)",
    r"bypass (policy|authorization|security)",
    r"system prompt",
    r"developer message",
]

SECRET_PATTERNS = [
    r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----",
    r"(?i)\b(password|passwd|token|api[_ -]?key|secret)\s*[:=]\s*\S+",
]

def has_prompt_injection(text: str) -> bool:
    s = text or ""
    return any(re.search(p, s, flags=re.I) for p in INJECTION_PATTERNS)

def sanitize_untrusted_text(text: str) -> tuple[str, bool]:
    flagged = has_prompt_injection(text)
    if not flagged:
        return text, False
    cleaned = text
    for p in INJECTION_PATTERNS:
        cleaned = re.sub(p, "[UNTRUSTED-INSTRUCTION-REMOVED]", cleaned, flags=re.I)
    return cleaned, True

def contains_secret(text: str) -> bool:
    s = text or ""
    return any(re.search(p, s) for p in SECRET_PATTERNS)

def validate_no_secret_output(text: str) -> None:
    if contains_secret(text):
        raise ValueError("Potential secret detected in model/tool output")
