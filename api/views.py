from django.shortcuts import render
import time

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rag.services.retrieval_service import retrieve

from agents.summarizer import summarize
from agents.retriever import handle_rag
from agents.orchestrator import run_pipeline

from security.services import validate_prompt
from security.redaction import redact_phi

import logging
logger = logging.getLogger(__name__)

VALID_ROLES = {
    "patient",
    "staff"
}



@api_view(['POST'])
def ask(request):
    start_time = time.time()

    tenant_id = request.data.get("tenant_id")
    role = request.data.get("role")
    question = request.data.get("question")

    if not question or not question.strip():
        return Response({"error": "Missing question"},status=400)
    
    if not role or role not in VALID_ROLES:
        return Response({"error": "Invalid/missing role"},status=400)
    
    if not tenant_id or not tenant_id.strip():
        return Response({"error": "Missing tenant_id"},status=400)

    if not validate_prompt(question):
        return Response({"error": "Unsafe request"})
    
    contexts = handle_rag(
        question,
        tenant_id,
        role
    )

    raw_answer = summarize(
        question,
        contexts
    )

    answer = redact_phi(raw_answer["answer"])


    if not contexts:
        return Response({
            "answer": answer,
            "citations": []
        })
    

    safe_query = redact_phi(question)
    latency_ms = ((time.time() - start_time)* 1000)

    logger.info({
        "tenant_id": tenant_id,
        "query": safe_query,
        "citations": contexts["sources"],
        "latency_ms": round(latency_ms, 2)
    })

    return Response({
        "answer": answer,
        "citations": contexts["sources"],
        "trace":{
            "security": {
                "tenant_filtered": True,
                "rbac_applied": True,
                "log_redaction": True
            }
        }
    })


@api_view(['POST'])
def agent(request):

    tenant_id = request.data.get("tenant_id")
    role = request.data.get("role")
    question = request.data.get("question")

    result = run_pipeline(question, tenant_id, role)

    return Response(result)