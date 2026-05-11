
def handle_safety(query: str):

    return {
        "intent": "safety",
        "action": "blocked",
        "data": {
            "reason": "Sensitive information detected"
        },
        "sources": []
    }