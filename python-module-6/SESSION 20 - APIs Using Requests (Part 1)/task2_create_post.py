"""
Task 2: Send a POST Request to JSONPlaceholder API
Send a POST request to https://jsonplaceholder.typicode.com/posts using
requests.post() with the data:
  - title: 'My First Post'
  - body: 'Hello from Python!'
  - userId: 101
and print the status code and the returned JSON response.
"""

import requests


def create_post():
    url = "https://jsonplaceholder.typicode.com/posts"

    # Define the payload as requested
    payload = {
        "title": "My First Post",
        "body": "Hello from Python!",
        "userId": 101,
    }

    print("=" * 60)
    print("Task 2: Creating a Post via requests.post()")
    print("=" * 60)
    print(f"Target URL: {url}")
    print("Payload:")
    for key, value in payload.items():
        print(f"  * {key}: {value}")
    print("=" * 60)

    try:
        # Pass payload using json= argument
        response = requests.post(url, json=payload, timeout=10)

        # Print HTTP status code
        print(f"\nHTTP Status Code : {response.status_code}")

        # Print returned JSON response
        response_json = response.json()
        print(f"Returned JSON    : {response_json}")

        if response.status_code in (200, 201):
            print("\n[SUCCESS] Post successfully submitted and assigned an ID!")
        else:
            print(
                f"\n[WARNING] Unexpected response status: {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] An exception occurred while creating the post: {e}")


if __name__ == "__main__":
    create_post()
