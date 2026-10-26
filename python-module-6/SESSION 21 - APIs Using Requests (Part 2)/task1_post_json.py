"""
Task 1: Send a POST Request with JSON Payload
Use the requests library to send a POST request to https://jsonplaceholder.typicode.com/posts
with a JSON payload containing a title, body, and userId, then print the response status code
and JSON data.
"""

import requests


def send_post_request():
    url = "https://jsonplaceholder.typicode.com/posts"

    # Define the JSON payload containing title, body, and userId
    payload = {
        "title": "Mastering REST APIs in Python",
        "body": "Comprehensive guide on making GET and POST requests, handling payloads, and parsing responses.",
        "userId": 42,
    }

    print("=" * 60)
    print("Task 1: POST Request with JSON Payload")
    print("=" * 60)
    print(f"Target URL: {url}")
    print("Payload:")
    for key, value in payload.items():
        print(f"  * {key}: {value}")
    print("=" * 60)

    try:
        # Pass payload with json= argument
        response = requests.post(url, json=payload, timeout=10)

        # Print the HTTP status code and response JSON
        print(f"\nResponse Status Code : {response.status_code}")
        print(f"Response JSON Data   :\n{response.json()}")

        if response.status_code in (200, 201):
            print(
                "\n[SUCCESS] Resource successfully created on the mock server!"
            )
        else:
            print(
                f"\n[WARNING] Received unexpected status code: {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] An exception occurred while sending POST request: {e}")


if __name__ == "__main__":
    send_post_request()
