def handle_billing(rag_results):

    if not rag_results:
        return {
            "intent": "biller",
            "action": "not_found",
            "data": [],
            "sources": []
        }

    return {
        "intent": "biller",
        "action": "coverage_lookup",
        "data": rag_results,
        "sources": [
            r["source"]
            for r in rag_results
        ]
    }