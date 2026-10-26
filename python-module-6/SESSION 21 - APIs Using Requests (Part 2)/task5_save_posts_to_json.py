"""
Task 5: Fetch Latest 5 Posts and Save to JSON
Modify your script to save the same API data (latest 5 posts from
https://jsonplaceholder.typicode.com/posts) into a JSON file named posts.json instead of CSV.
"""

import json
import os
import requests


def save_posts_to_json():
    url = "https://jsonplaceholder.typicode.com/posts"

    # Define output file path in the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_json = os.path.join(script_dir, "posts.json")

    print("=" * 60)
    print("Task 5: Fetch Posts and Save to posts.json")
    print("=" * 60)
    print(f"Fetching posts from: {url} ...")

    try:
        response = requests.get(url, timeout=10)
        print(f"HTTP Status Code: {response.status_code}")

        if response.status_code == 200:
            all_posts = response.json()
            # Select the latest 5 posts
            latest_5_posts = all_posts[:5]

            print(f"Total posts fetched: {len(all_posts)}")
            print("Selected latest 5 posts for export:\n")

            for idx, post in enumerate(latest_5_posts, start=1):
                print(f"  {idx}. UserID: {post.get('userId')} | ID: {post.get('id')} | Title: {post.get('title')}")

            # Format data to save (preserving title, userId, id, and body)
            formatted_data = [
                {
                    "userId": post.get("userId"),
                    "id": post.get("id"),
                    "title": post.get("title"),
                    "body": post.get("body"),
                }
                for post in latest_5_posts
            ]

            # Save data to posts.json with indentation
            with open(output_json, mode="w", encoding="utf-8") as jsonfile:
                json.dump(formatted_data, jsonfile, indent=4)

            print("\n" + "=" * 60)
            print(f"[SUCCESS] Successfully exported 5 posts to: {output_json}")
            print("=" * 60)

            # Display saved JSON file preview
            print("\nJSON File Contents Preview:")
            with open(output_json, mode="r", encoding="utf-8") as f:
                print(f.read().strip())

        else:
            print(f"[ERROR] Request failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API request failed: {e}")
    except IOError as e:
        print(f"[ERROR] File writing failed: {e}")


if __name__ == "__main__":
    save_posts_to_json()
