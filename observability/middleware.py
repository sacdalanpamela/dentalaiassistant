import time

from observability.metrics import metrics


class MetricsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        start = time.time()

        response = self.get_response(request)

        metrics["requests"] += 1

        latency = time.time() - start

        print({
            "path": request.path,
            "latency": latency
        })

        return response