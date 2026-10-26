"""
Task 1: Fetch Latest Posts from JSONPlaceholder API
Use the requests.get() function to fetch the latest posts from the JSONPlaceholder
API endpoint https://jsonplaceholder.typicode.com/posts and print the status code
and the first post's title.
"""

import requests


def fetch_latest_posts():
    url = "https://jsonplaceholder.typicode.com/posts"

    print("=" * 60)
    print("Task 1: Fetching Posts via requests.get()")
    print("=" * 60)
    print(f"Target URL: {url}\n")

    try:
        # Send GET request
        response = requests.get(url, timeout=10)

        # Print HTTP status code
        print(f"HTTP Status Code : {response.status_code}")

        if response.status_code == 200:
            posts = response.json()
            print(f"Total Posts Received : {len(posts)}")

            if posts:
                first_post = posts[0]
                print("\n--- First Post Details ---")
                print(f"Post ID : {first_post.get('id')}")
                print(f"User ID : {first_post.get('userId')}")
                print(f"Title   : {first_post.get('title')}")
                print(f"Body    : {first_post.get('body')}")
            else:
                print("[INFO] No posts found in response.")
        else:
            print(f"[ERROR] Failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] An exception occurred while requesting data: {e}")


if __name__ == "__main__":
    fetch_latest_posts()
