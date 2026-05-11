import ollama
import logging
import json

logger = logging.getLogger(__name__)
LLM_CACHE = {}

def chat_completion(messages):

    cache_key = json.dumps(messages,sort_keys=True)

    if cache_key in LLM_CACHE:

        logger.info("LLM CACHE HIT")

        return LLM_CACHE[cache_key]

    logger.info("LLM CACHE MISS")

    response = ollama.chat(
        model="phi3:mini",
        messages=messages,
        keep_alive="5m"
    )

    content = response["message"]["content"]

    LLM_CACHE[cache_key] = content

    return content