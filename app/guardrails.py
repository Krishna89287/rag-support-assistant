import re
_PII = re.compile(r"\b([\w.+-]+@[\w-]+\.[\w.]+|\d{12,19})\b")
_INJECTION = re.compile(r"ignore (previous|all) instructions|system prompt", re.I)


def check_input(text: str) -> dict:
    return {"blocked": bool(_INJECTION.search(text)), "reason": "possible prompt injection" if _INJECTION.search(text) else ""}


def redact(text: str) -> str:
    return _PII.sub("[REDACTED]", text)
