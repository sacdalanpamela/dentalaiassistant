import time

metrics = {
    "requests": 0,
    "llm_calls": 0,
    "fallback_calls": 0,
    "total_latency": 0,
    "latencies": [],
    "retrieval_hits": 0,
    "retrieval_misses": 0
}

def record_request(latency):

    metrics["requests"] += 1
    metrics["total_latency"] += latency
    metrics["latencies"].append(latency)


def record_retrieval(hit: bool):

    if hit:
        metrics["retrieval_hits"] += 1
    else:
        metrics["retrieval_misses"] += 1


def get_metrics():

    total_requests = metrics["requests"]

    avg_latency = 0

    if total_requests > 0:
        avg_latency = (
            metrics["total_latency"]
            / total_requests
        )

    sorted_latencies = sorted(metrics["latencies"])

    p95_latency = 0

    if sorted_latencies:

        index = int(
            0.95 * len(sorted_latencies)
        ) - 1

        p95_latency = sorted_latencies[
            max(index, 0)
        ]

    total_retrievals = (
        metrics["retrieval_hits"]
        + metrics["retrieval_misses"]
    )

    hit_rate = 0

    if total_retrievals > 0:
        hit_rate = (
            metrics["retrieval_hits"]
            / total_retrievals
        )

    return {
        "total_requests": total_requests,
        "avg_latency_ms": round(avg_latency, 2),
        "p95_latency_ms": round(p95_latency, 2),
        "retrieval_hit_rate": round(hit_rate, 2)
    }