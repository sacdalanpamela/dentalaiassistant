import re


def redact_phi(text):

    text = re.sub(
        r'(\+63|63|0)9\d{9}',
        '[REDACTED_PHONE]',
        text
    )

    text = re.sub(
        r'[\w\.-]+@[\w\.-]+',
        '[REDACTED_EMAIL]',
        text
    )

    return text