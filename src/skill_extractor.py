"""
Extracts canonical skills from raw text using word-boundary regex
matching against the alias dictionary in config.py.
"""

import re
from src.config import SKILL_ALIASES

def _build_pattern(alias : str) -> str:
    escaped = re.escape(alias)
    return rf"\b{escaped}\b"

def extract_skills(text : str) -> dict:
    if not text or not text.strip():
        return {}

    text_lower = text.lower()
    found = {}

    for canonical, aliases in SKILL_ALIASES.items():
        count = 0
        for alias in aliases:
            pattern = _build_pattern(alias)
            matches = re.findall(pattern, text_lower)
            count += len(matches)

        if count > 0:
            found[canonical] = count

    return found