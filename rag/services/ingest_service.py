import logging
import time
import json
import hashlib

from rag.models import DocumentChunk
from rag.services.embedding_service import generate_embedding

logger = logging.getLogger(__name__)


def ingest_documents():

    try:        
        start_time = time.time()

        logger.info("Starting ingestion process...")

        with open("mock_data/documents.json") as file:
            docs = json.load(file)

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for doc in docs:

            tenant_id = doc["tenant_id"]
            source = doc["source"]
            content = doc["content"]

            # Generate content hash 
            content_hash = hashlib.md5(
                content.encode("utf-8")
            ).hexdigest()

            existing_doc = DocumentChunk.objects.filter(
                tenant_id=tenant_id,
                source=source
            ).first()

            # Skip unchanged documents
            if (
                existing_doc and
                getattr(existing_doc, "content_hash", None) == content_hash
            ):
                skipped_count += 1

                logger.info(
                    f"Skipped unchanged document: {source}"
                )

                continue

            # Only generate embedding if content changed
            embedding = generate_embedding(content)

            _, created = DocumentChunk.objects.update_or_create(
                tenant_id=tenant_id,
                source=source,

                defaults={
                    "doc_type": doc["doc_type"],
                    "content": content,
                    "embedding": embedding,
                    "effective_date": doc.get("effective_date"),
                    "allowed_roles": doc.get("allowed_roles", []),
                    "content_hash": content_hash
                }
            )

            if created:
                created_count += 1
                logger.info(f"Created document: {source}")

            else:
                updated_count += 1
                logger.info(f"Updated document: {source}")

        total_chunks = DocumentChunk.objects.count()
        duration = round(time.time() - start_time, 2)

        logger.info(
            "Ingestion completed successfully | "
            f"Created={created_count} | "
            f"Updated={updated_count} | "
            f"Skipped={skipped_count} | "
            f"TotalChunks={total_chunks} | "
            f"Duration={duration}s"
        )

    except Exception:
        logger.exception("Ingestion failed!")
        raise