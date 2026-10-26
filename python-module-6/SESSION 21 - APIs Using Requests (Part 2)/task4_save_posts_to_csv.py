"""
Task 4: Fetch Latest 5 Posts and Save to CSV
Write a script that fetches the latest 5 posts from https://jsonplaceholder.typicode.com/posts,
parses the JSON response, and saves the post titles and userIds to a CSV file called posts.csv.

Hint: Use the csv module for writing to CSV.
"""

import csv
import os
import requests


def save_posts_to_csv():
    url = "https://jsonplaceholder.typicode.com/posts"

    # Define output file path in the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_csv = os.path.join(script_dir, "posts.csv")

    print("=" * 60)
    print("Task 4: Fetch Posts and Save to posts.csv")
    print("=" * 60)
    print(f"Fetching posts from: {url} ...")

    try:
        response = requests.get(url, timeout=10)
        print(f"HTTP Status Code: {response.status_code}")

        if response.status_code == 200:
            all_posts = response.json()
            # Select the first 5 posts
            latest_5_posts = all_posts[:5]

            print(f"Total posts fetched: {len(all_posts)}")
            print("Selected latest 5 posts for export:\n")

            for idx, post in enumerate(latest_5_posts, start=1):
                print(f"  {idx}. UserID: {post.get('userId')} | Title: {post.get('title')}")

            # Write to CSV using csv module
            with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["userId", "id", "title"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for post in latest_5_posts:
                    writer.writerow({
                        "userId": post.get("userId"),
                        "id": post.get("id"),
                        "title": post.get("title")
                    })

            print("\n" + "=" * 60)
            print(f"[SUCCESS] Successfully saved 5 posts to: {output_csv}")
            print("=" * 60)

            # Display saved CSV contents for verification
            print("\nCSV File Contents Preview:")
            with open(output_csv, mode="r", encoding="utf-8") as f:
                print(f.read().strip())

        else:
            print(f"[ERROR] Request failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API request failed: {e}")
    except IOError as e:
        print(f"[ERROR] File writing failed: {e}")


if __name__ == "__main__":
    save_posts_to_csv()
