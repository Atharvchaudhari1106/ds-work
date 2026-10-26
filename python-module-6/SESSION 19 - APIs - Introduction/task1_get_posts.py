"""
Task 1: Fetch Posts from Public API using requests
Use the requests library in Python to send a GET request to the public API
https://jsonplaceholder.typicode.com/posts and print the titles of the first 5 posts.
"""

import requests


def fetch_first_5_post_titles():
    url = "https://jsonplaceholder.typicode.com/posts"
    print(f"Sending GET request to: {url} ...\n")

    try:
        response = requests.get(url, timeout=10)

        # Check HTTP status code
        if response.status_code == 200:
            posts = response.json()
            print(f"Total posts received from API: {len(posts)}")
            print("=" * 60)
            print("Titles of the First 5 Posts:")
            print("=" * 60)

            for index, post in enumerate(posts[:5], start=1):
                print(f"Post #{index} (ID: {post.get('id')}): {post.get('title')}")
        else:
            print(f"Failed to fetch posts. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")


if __name__ == "__main__":
    fetch_first_5_post_titles()
