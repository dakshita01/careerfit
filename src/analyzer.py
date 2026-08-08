"""
Compares extracted job-description skills against a user's extracted
skills, computes match percentage, and ranks missing skills by priority.
"""

def analyze_gap(jd_skills: dict, user_skills: list) -> dict:
    required = set(jd_skills.keys())
    user_set = set(user_skills)

    have = sorted(required & user_set)
    missing = sorted(required - user_set)

    match_percent = round((len(have) / len(required)) * 100, 1) if required else 0.0
    priority = sorted(missing, key=lambda s: jd_skills.get(s, 0), reverse=True)

    return {
        "have" : have,
        "missing" : missing,
        "match_percent" : match_percent,
        "priority" : priority,
        "required_count" : len(required)
    }