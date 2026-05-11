from agents.planner import plan
from agents.retriever import handle_rag
from agents.biller import handle_billing
from agents.scheduler import handle_scheduler
from agents.safety import handle_safety

from agents.summarizer import summarize
import time
from observability.metrics import record_request
from security.redaction import redact_phi

import logging
logger = logging.getLogger(__name__)


def run_pipeline(query, tenant_id, role):
    start_time = time.time()
    
    intent = plan(query, role)

     # TOOL EXECUTION
    if intent == "safety":
        tool_result = handle_safety(query)

    elif intent == "scheduler":
        tool_result = handle_scheduler(
            query,
            patient_id=tenant_id
        )

    elif intent == "biller":

        rag_result = handle_rag(
            query,
            tenant_id,
            role
        )

        tool_result = handle_billing(
            rag_result["data"]
        )

    else:
        tool_result = handle_rag(
            query,
            tenant_id,
            role
        )

    final_response = summarize(
        query,
        tool_result
    )

    latency_ms = ((time.time() - start_time)* 1000)

    record_request(latency_ms)
    safe_query = redact_phi(query)

    logger.info({
        "tenant_id": tenant_id,
        "intent": intent,
        "query": safe_query,
        "action": tool_result["action"],
        "sources": tool_result.get("sources", []),
        "latency_ms": round(latency_ms, 2)
    })

    return {
        "intent": intent,
        "trace": {
            "planner": intent,
            "action": tool_result["action"]
        },
        "answer": final_response["answer"],
        "citations": final_response["citations"]
    }