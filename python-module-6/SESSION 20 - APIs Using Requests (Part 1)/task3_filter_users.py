"""
Task 3: Filter Users by Email Domain (.org)
Fetch a list of users from https://jsonplaceholder.typicode.com/users using
requests.get(), then use the .json() method to extract and print the usernames
of all users whose email ends with '.org'.
"""

import requests


def fetch_org_users():
    url = "https://jsonplaceholder.typicode.com/users"

    print("=" * 60)
    print("Task 3: Filter Users with '.org' Email Address")
    print("=" * 60)
    print(f"Target URL: {url}\n")

    try:
        response = requests.get(url, timeout=10)
        print(f"HTTP Status Code : {response.status_code}")

        if response.status_code == 200:
            users = response.json()
            print(f"Total Users Fetched : {len(users)}\n")

            # Extract usernames of all users whose email ends with '.org'
            org_users = []
            for user in users:
                email = user.get("email", "")
                if email.lower().endswith(".org"):
                    org_users.append(user)

            print("=" * 60)
            print("Users whose email ends with '.org':")
            print("=" * 60)

            if org_users:
                for idx, u in enumerate(org_users, start=1):
                    print(f"{idx}. Username : {u.get('username')}")
                    print(f"   Name     : {u.get('name')}")
                    print(f"   Email    : {u.get('email')}")
                    print(f"   Company  : {u.get('company', {}).get('name')}")
                    print("-" * 40)

                usernames_only = [u.get("username") for u in org_users]
                print(f"\nExtracted Usernames List: {usernames_only}")
            else:
                print("[INFO] No users found with email ending in '.org'.")

        else:
            print(f"[ERROR] Request failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] An exception occurred: {e}")


if __name__ == "__main__":
    fetch_org_users()
