"""
Task 3: POST Request to ReqRes API & Extract ID and Timestamp
Send a POST request to https://reqres.in/api/users with a JSON object containing
a username and job, then parse the response to extract and print the created user's ID
and creation timestamp.

Hint: Use response.json() to access the returned data.
"""

import requests


def create_reqres_user():
    url = "https://reqres.in/api/users"

    # Define JSON object containing username and job
    user_payload = {
        "username": "atharv_c",
        "name": "Atharv Chaudhari",
        "job": "Software Engineer & Data Analyst",
    }

    print("=" * 60)
    print("Task 3: POST Request to ReqRes API")
    print("=" * 60)
    print(f"Target URL: {url}")
    print("Payload to Send:")
    for key, value in user_payload.items():
        print(f"  * {key}: {value}")
    print("=" * 60)

    try:
        # Send POST request with JSON payload
        response = requests.post(url, json=user_payload, timeout=10)

        print(f"\nResponse Status Code : {response.status_code}")

        # Parse response using .json()
        data = response.json()
        print(f"Raw Response Body    : {data}\n")

        # Extract created user's ID and creation timestamp
        user_id = data.get("id")
        created_at = data.get("createdAt")

        print("=" * 60)
        print("Extracted User Information:")
        print("=" * 60)
        print(f"[+] User ID            : {user_id}")
        print(f"[+] Creation Timestamp : {created_at}")
        print(f"[+] Assigned Role/Job  : {data.get('job')}")
        print(f"[+] Username           : {data.get('username')}")
        print("=" * 60)
        print("[SUCCESS] User successfully created and timestamp verified!")

        return user_id, created_at

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")


if __name__ == "__main__":
    create_reqres_user()
