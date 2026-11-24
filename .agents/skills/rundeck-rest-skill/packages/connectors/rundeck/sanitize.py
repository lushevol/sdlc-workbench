"""Best-effort redaction before data reaches an agent. NOT a DLP guarantee."""
import re

SENSITIVE_KEY = re.compile(r"(?i)(password|passwd|secret|credential|(?:api[_-]?)?token|api[_-]?key|private[_-]?key|authorization|session|cookie|secureinput|keypass)")
ASSIGNMENT = re.compile(r"(?i)\b(password|passwd|secret|token|api[_-]?key|authorization)\s*[:=]\s*([^\s,;\]\}\"']+)")
BEARER = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{6,}")
BASIC = re.compile(r"(?i)\bBasic\s+[A-Za-z0-9+/=]{6,}")
URL_CREDS = re.compile(r"(?i)(https?://)[^/@\s]+:[^/@\s]+@")


def scrub_text(value, limit=600):
    value = str(value)
    value = URL_CREDS.sub(r"\1[REDACTED]@", value)
    value = BEARER.sub("Bearer [REDACTED]", value)
    value = BASIC.sub("Basic [REDACTED]", value)
    value = ASSIGNMENT.sub(lambda m: f"{m.group(1)}=[REDACTED]", value)
    if len(value) > limit:
        return value[:limit] + "... [TRUNCATED]"
    return value


def scrub(value, depth=0):
    if depth > 18:
        return "[MAX_DEPTH]"
    if isinstance(value, dict):
        return {str(k): ("[REDACTED]" if SENSITIVE_KEY.search(str(k)) else scrub(v, depth + 1)) for k, v in value.items()}
    if isinstance(value, list):
        return [scrub(v, depth + 1) for v in value[:500]]
    if isinstance(value, str):
        return scrub_text(value)
    return value
