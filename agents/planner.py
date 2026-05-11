from agents.services.llm_service import chat_completion
import json
import logging

logger = logging.getLogger(__name__)



def plan(query: str, role: str):
    VALID_INTENTS = {"retriever", "biller", "scheduler", "safety"}

    with open("prompts/intent_prompt.txt") as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        query=query,
        role=role
    )

    messages = [
        {
            "role": "system",
            "content": prompt
        },
        {
            "role": "user",
            "content": f"""

                Question:
                {query}

                Role:
                {role}
                """

        }
    ]
    response = chat_completion(messages)
    intent = response.strip().lower()

    if intent not in VALID_INTENTS:
        logger.warning(f"Invalid intent from LLM: {intent}")
        return "retriever"

    return intent
