import re
from typing import List, Set


EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def extract_emails_from_text(text: str) -> List[str]:
    if not text:
        return []
    emails: Set[str] = set(re.findall(EMAIL_REGEX, text))
    return sorted(emails)


