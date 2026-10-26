"""
Task 4: Bearer Token Authentication
Many APIs require Bearer tokens for authentication. Write a function get_user_profile()
that calls a mock API endpoint (e.g., https://jsonplaceholder.typicode.com/users/1)
using a fake Bearer token in the Authorization header, and prints the user's name.

Constraint: Use the 'Authorization: Bearer <token>' header format.
"""

import requests


def get_user_profile():
    url = "https://jsonplaceholder.typicode.com/users/1"

    # Define simulated JWT / OAuth Bearer token
    bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIxMDEiLCJyb2xlIjoiYWRtaW4ifQ.sample_signature"

    # Set up Authorization header according to standard constraint
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json",
        "User-Agent": "SecureAPIClient/2.0"
    }

    print("=" * 65)
    print("Task 4: Authenticated Request Using Bearer Token")
    print("=" * 65)
    print(f"Target URL : {url}")
    print(f"Header     : Authorization: Bearer {bearer_token[:30]}...")
    print("=" * 65)

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"\nResponse Status Code : {response.status_code}")

        if response.status_code == 200:
            user_data = response.json()
            user_name = user_data.get("name")
            username = user_data.get("username")
            email = user_data.get("email")
            company = user_data.get("company", {}).get("name")

            print("=" * 65)
            print(f"[SUCCESS] User Name Extracted: {user_name}")
            print("=" * 65)
            print(f"  * Full Name : {user_name}")
            print(f"  * Username  : {username}")
            print(f"  * Email     : {email}")
            print(f"  * Company   : {company}")
            print("=" * 65)

            return user_name
        else:
            print(f"[ERROR] Failed to fetch profile. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")


if __name__ == "__main__":
    get_user_profile()
