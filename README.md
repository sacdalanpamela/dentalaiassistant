# Dental AI Assistant — README

## Overview
This project is a multi-tenant AI-powered dental assistant built using Retrieval-Augmented Generation (RAG) and a multi-agent orchestration architecture.

The system supports:
grounded dental Q&A
insurance and billing assistance
appointment scheduling workflows
safety and compliance checks
tenant isolation and RBAC

The project demonstrates:
production-style RAG pipelines
multi-agent orchestration
observability and evaluation
LLMOps and security practices


## Features
### RAG Core
1. Hybrid retrieval:
```
    - Vector search (pgvector embeddings)
    - BM25 lexical retrieval
```
2. Metadata filtering:
```
    - tenant_id
    - allowed_roles
    - doc_type
    - effective_date
```
3. Citation-backed grounded responses
4. Hallucination resistance

## Multi-Agent Architecture

| Agent      | Responsibility                 |
| ---------- | ------------------------------ |
| Planner    | intent classification          |
| Retriever  | hybrid retrieval               |
| Billing    | insurance and coverage queries |
| Scheduler  | draft appointment workflow     |
| Safety     | PHI/jailbreak protection       |
| Summarizer | grounded response generation   |


## Observability
- Structured logging
- Request latency tracking
- Retrieval hit rate tracking
- Cache hit/miss tracking
- /metrics endpoint

## Security
- Tenant isolation at query level
- RBAC filtering
- PHI/PII redaction in logs
- Prompt injection protection

## Tech Stack
Python
Django REST Framework
PostgreSQL
pgvector
Ollama
phi3:mini
rank-bm25
Docker


## Project Structure
```
project/
│
├── agents/
│   ├── planner.py
│   ├── billing_agent.py
│   ├── scheduler_agent.py
│   ├── safety_agent.py
│   ├── summarizer.py
│
├── api/
│   ├── views.py
│
├── observability/
│   ├── metrics.py
│   ├── views.py
│
├── rag/
│   ├── models.py
|   ├── services/
│       ├── retrieval_service.py
│       ├── ingest_service.py
│       ├── embedding_service.py
│
├── security/
│   ├── redaction.py
│   ├── services.py
│
├── prompts/
│   ├── intent_prompt.txt
│   ├── rag_prompt.txt
│
├── mock_data/
│   ├── documents.json
│
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
│
├── evaluations/
│   ├── evaluate_agents.py
│   ├── evaluate_rag.py
│   ├── goldens.json
```

## Prototype (Docker runnable)
The system can be run locally using Docker Compose.

# Docker Setup
1. Install Docker
Install:
- Docker Desktop
- Docker Compose

2. Start Ollama
Install Ollama locally
Pull required model (phi3:mini)
Start Ollama

3. Build Containers
   ``` docker-compose build ```

4. Start Containers
``` docker-compose up ```

5. Run Migrations
``` docker-compose exec api python manage.py migrate ```

6. Seed Mock Data
``` 
docker-compose exec api python manage.py shell 

from rag.services.ingestion_service import ingest_documents
ingest_documents()

```

## Local Setup (Without Docker)
1. Create Virtual Environment
``` python -m venv venv ```

2. Activate environment
``` venv\Scripts\activate ```

3. Install Dependencies
``` pip install -r requirements.txt ```

4. Start PostgreSQL
Example DB config:
```
DB_NAME=ragdb
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

5. Run Migrations
``` python manage.py migrate ```

6. Pull Ollama Models
``` ollama pull phi3:mini ```

7. Ingest Seed Documents
``` 
python manage.py shell

from rag.services.ingestion_service import ingest_documents
ingest_documents()
```

8. Run server
```
python manage.py runserver
```

## API Endpoints

### POST api/ask/
Grounded RAG response with citations.

Example request:
```
{
  "tenant_id": "clinic_a",
  "role": "patient",
  "question": "What is the coverage for root canal?"
}
```

### POST api/agent/
Multi-agent orchestration endpoint with execution trace.

Example request:
```

{
  "tenant_id": "clinic_a",
  "role": "patient",
  "question": "Book me an appointment at 1:00PM"
}

```

### GET /api/metrics/
Returns runtime metrics.

Example response:
```
{
  "total_requests": 12,
  "avg_latency_ms": 412.4,
  "p95_latency_ms": 590.8,
  "retrieval_hit_rate": 0.91
}
```

## Evaluation Harness
Run evaluations
```
python evaluations/evaluate_rag.py
python evaluations/evaluate_agents.py
```

## Red Team Tests

The system includes safety tests for:
- cross-tenant access attempts
- PHI leakage attempts
- jailbreak/prompt injection attempts

Unsafe requests are blocked by the Safety Agent.

## Key Design Decisions
### Hybrid Retrieval

Combines:
- semantic similarity
- lexical keyword matching

to improve grounding quality and reduce hallucinations.

## Multi-Tenancy
Tenant filtering is enforced directly at the database query layer to prevent accidental leakage.

## LLMOps

Implemented:
- prompt caching
- observability metrics
- structured logging

## Future Improvements
- Redis distributed cache
- Async ingestion pipeline
- Authentication/JWT
- Production vector databases
