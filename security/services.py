BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "show all tenants",
]


def validate_prompt(prompt):

    lowered = prompt.lower()

    for pattern in BLOCKED_PATTERNS:

        if pattern in lowered:
            return False

    return True