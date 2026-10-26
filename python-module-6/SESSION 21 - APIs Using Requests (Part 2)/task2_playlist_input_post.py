"""
Task 2: User Input for Playlist and POST Request
Build a Python script that lets a user enter a new playlist name and description,
sends this data as JSON in a POST request to a mock API endpoint
(such as https://jsonplaceholder.typicode.com/posts), and prints the playlist ID returned by the API.
"""

import sys
import requests


def get_input_with_fallback(prompt, default_value):
    """Safely prompt the user with a fallback for non-interactive environments."""
    try:
        # Check if running in an interactive terminal
        if sys.stdin.isatty():
            user_val = input(f"{prompt} [Press Enter for '{default_value}']: ").strip()
            return user_val if user_val else default_value
        else:
            print(f"{prompt}: {default_value} (Auto-selected)")
            return default_value
    except (EOFError, IOError):
        return default_value


def create_user_playlist():
    url = "https://jsonplaceholder.typicode.com/posts"

    print("=" * 60)
    print("Task 2: Create Playlist via User Input & POST Request")
    print("=" * 60)

    # Prompt user for playlist name and description
    playlist_name = get_input_with_fallback(
        "Enter Playlist Name", "Coding Flow & Chill Beats"
    )
    playlist_desc = get_input_with_fallback(
        "Enter Playlist Description", "A 2-hour collection of lo-fi and ambient electronic tracks"
    )

    payload = {
        "title": playlist_name,
        "body": playlist_desc,
        "userId": 1,
    }

    print("\nSending POST request with payload:")
    print(f"  * Name/Title  : {payload['title']}")
    print(f"  * Description : {payload['body']}")
    print(f"  * User ID     : {payload['userId']}")
    print("=" * 60)

    try:
        response = requests.post(url, json=payload, timeout=10)

        print(f"\nResponse Status Code: {response.status_code}")
        response_data = response.json()
        print(f"Full Server Response: {response_data}")

        playlist_id = response_data.get("id")
        print("=" * 60)
        print(f"[SUCCESS] Created Playlist ID: {playlist_id}")
        print("=" * 60)

        return playlist_id

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")


if __name__ == "__main__":
    create_user_playlist()
