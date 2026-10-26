"""
Task 4: Filter Posts by Query Parameter (userId=2)
Modify your GET request to https://jsonplaceholder.typicode.com/posts so it only
fetches posts by userId=2 by passing the correct query parameter.
Print the IDs of the returned posts.

Hint: Use the 'params' argument in requests.get().
"""

import requests


def fetch_posts_by_userid(target_user_id=2):
    url = "https://jsonplaceholder.typicode.com/posts"
    query_parameters = {"userId": target_user_id}

    print("=" * 60)
    print(f"Target URL       : {url}")
    print(f"Query Parameters : {query_parameters}")
    print("=" * 60)

    try:
        # Pass query parameters using the 'params' argument
        response = requests.get(url, params=query_parameters, timeout=10)

        print(f"\nFinal Request URL with Query String:\n  {response.url}")
        print(f"Response Status Code: {response.status_code}\n")

        if response.status_code == 200:
            posts = response.json()
            print(f"Total posts returned for userId={target_user_id}: {len(posts)}")

            # Extract list of IDs
            post_ids = [post.get("id") for post in posts]
            print(f"Returned Post IDs: {post_ids}\n")

            print("=" * 60)
            print("Post Breakdown:")
            print("=" * 60)
            for post in posts:
                print(
                    f" - ID: {post.get('id'):<3} | UserID: {post.get('userId')} | Title: {post.get('title')[:45]}..."
                )
        else:
            print(f"Failed to retrieve posts. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching posts: {e}")


if __name__ == "__main__":
    fetch_posts_by_userid(2)
