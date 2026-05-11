from rank_bm25 import BM25Okapi
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pgvector.django import CosineDistance

from rag.models import DocumentChunk
from rag.services.embedding_service import generate_embedding

from observability.metrics import record_retrieval


def retrieve(query, tenant_id, role):

    query_embedding = np.array(
        generate_embedding(query)
    ).reshape(1, -1)

    tenant_id = tenant_id.strip().lower()

    documents = DocumentChunk.objects.filter(
        tenant_id=tenant_id,
        allowed_roles__overlap=[role]
    )

    corpus = [d.content.split() for d in documents]

    if not corpus:
        return []

    bm25 = BM25Okapi(corpus)
    scores = bm25.get_scores(query.split())

    results = []

    for idx, doc in enumerate(documents):

        doc_embedding = np.array(
            doc.embedding
        ).reshape(1, -1)

        vector_score = cosine_similarity(
            query_embedding,
            doc_embedding
        )[0][0]

        bm25_score = scores[idx]

        # Ignore irrelevant docs
        if bm25_score == 0 and vector_score < 0.55:
            continue

        # Hybrid score
        final_score = (
            0.7 * vector_score +
            0.3 * bm25_score
        )

        results.append({
            "content": doc.content,
            "source": doc.source,
            "score": final_score
        })

        print(
            f"{doc.source} | "
            f"vector={vector_score:.3f} | "
            f"bm25={bm25_score:.3f} | "
            f"final={final_score:.3f}"
        )

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    if not results:
        record_retrieval(False)
        return []

    top_result = results[0]

    if top_result["score"] < 0.35:
        return []

    print(
        f"TOP RESULT: "
        f"{top_result['source']} | "
        f"score={top_result['score']:.3f}"
    )

    record_retrieval(True)
    return [top_result]