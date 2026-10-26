"""
Task 3: Send POST Request with JSON Payload
Send a POST request to https://jsonplaceholder.typicode.com/posts to add a new playlist
with fields: title, userId, and body. Print the status code and the JSON response.

Hint: Use requests.post() and pass your data as a JSON payload.
"""

import requests


def create_new_playlist():
    url = "https://jsonplaceholder.typicode.com/posts"

    # Define the playlist payload with title, userId, and body
    playlist_data = {
        "title": "Midnight Indie & Chill Beats",
        "userId": 5,
        "body": "A curated 25-track playlist featuring acoustic indie, lofi beats, and mellow pop for late-night study sessions.",
    }

    print("=" * 60)
    print(f"Target URL : {url}")
    print("Payload to Send:")
    print(playlist_data)
    print("=" * 60)

    try:
        # requests.post automatically converts dict to JSON and sets Content-Type: application/json
        response = requests.post(url, json=playlist_data, timeout=10)

        print(f"\nResponse Status Code: {response.status_code}")
        print("Server Response JSON:")
        print(response.json())

        if response.status_code in (200, 201):
            print("\n[SUCCESS] New resource was created on the server!")
        else:
            print(
                f"\n[WARNING] Request completed with unexpected status code: {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the POST request: {e}")


if __name__ == "__main__":
    create_new_playlist()
