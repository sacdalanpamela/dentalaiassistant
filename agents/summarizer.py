from agents.services.llm_service import chat_completion
from security.redaction import redact_phi


def summarize(query, tool_result):

    messages = [
        {
            "role": "system",
            "content": open(
                "prompts/rag_prompt.txt"
            ).read()
        },
        {
            "role": "user",
            "content": f"""

                Question:
                {query}

                Tool Result:
                {tool_result}
                """

        }
    ]

    raw_llm_answer = chat_completion(messages)
    answer = redact_phi(raw_llm_answer)

    return {
        "answer": answer,
        "citations": [
            {"source": s}
            for s in tool_result.get("sources", [])
        ]
    }