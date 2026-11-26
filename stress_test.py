import requests
import concurrent.futures
import time

def stress_test(endpoint, iterations):
    success = 0
    failed = 0

    for _ in range(iterations):
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                success += 1
            else:
                failed += 1
        except Exception as e:
            failed += 1

    return success, failed

def run_stress_tests():
    endpoints = [
        "http://localhost/api/books",
        "http://localhost/api/staff",
        "http://localhost/api/readers"
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(stress_test, endpoint, 1000)
            for endpoint in endpoints
        ]

        for future, endpoint in zip(futures, endpoints):
            success, failed = future.result()
            print(f"Endpoint {endpoint}: {success} successful, {failed} failed")

if __name__ == "__main__":
    run_stress_tests()
