from rag.services.retrieval_service import retrieve

def handle_rag(query, tenant_id, role):

    contexts = retrieve(query, tenant_id, role)

    if not contexts:
        return {
            "intent": "retriever",
            "action": "not_found",
            "data": [],
            "sources": []
        }

    return {
        "intent": "retriever",
        "action": "retrieve",
        "data": contexts,
        "sources": [
            c["source"]
            for c in contexts
        ]
    }