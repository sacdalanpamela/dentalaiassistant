import json
import time
import requests

BASE_URL = "http://127.0.0.1:8000/api/ask/"


def run_evaluation():

    with open("evaluations/goldens.json") as file:
        test_cases = json.load(file)

    total = len(test_cases)
    passed = 0

    for test in test_cases:

        print("=" * 60)
        print("TEST:", test["name"])

        start = time.time()

        response = requests.post(
            BASE_URL,
            json=test["payload"]
        )

        latency = round(time.time() - start, 2)

        data = response.json()

        answer = data.get("answer", "").lower()

        citations = [
            c["source"]
            for c in data.get("citations", [])
        ]

        success = True

        # Expected content checks
        for expected in test["expected_contains"]:

            if expected.lower() not in answer:
                print(f"FAILED: Missing expected content -> {expected}")
                success = False

        # Forbidden content checks
        for forbidden in test["must_not_contain"]:

            if forbidden.lower() in answer:
                print(f"FAILED: Forbidden content found -> {forbidden}")
                success = False

        # Citation checks
        for source in test["expected_sources"]:

            if source not in citations:
                print(f"FAILED: Missing citation -> {source}")
                success = False

        if success:
            passed += 1
            print("PASS")

        print(f"Latency: {latency}s")
        print()

    print("=" * 60)
    print(f"FINAL SCORE: {passed}/{total}")
    print("=" * 60)


if __name__ == "__main__":
    run_evaluation()