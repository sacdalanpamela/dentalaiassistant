
import os
import ollama

BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

client = ollama.Client(host=BASE_URL)

def generate_embedding(text):

    response = client.embeddings(
        model="nomic-embed-text",
        prompt=text
    )

    return response['embedding']