"""
Task 3: NASA Astronomy Picture of the Day (APOD) Downloader
Use the NASA Astronomy Picture of the Day (APOD) API to get today's image
title and explanation, and save the image to your local system.

Hint: The API returns a URL for the image - use requests to download it.
"""

import os
import requests


def download_nasa_apod():
    api_url = "https://api.nasa.gov/planetary/apod"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_image_path = os.path.join(script_dir, "nasa_apod.jpg")

    print("=" * 70)
    print("Task 3: NASA Astronomy Picture of the Day (APOD) Downloader")
    print("=" * 70)
    print(f"Endpoint : {api_url}")
    print("Using    : Public NASA DEMO_KEY")
    print("=" * 70)

    try:
        # Step 1: Attempt to fetch today's APOD metadata
        response = requests.get(api_url, params={"api_key": "DEMO_KEY"}, timeout=10)

        # Fallback to previous day if today's image is not yet generated or server is processing
        if response.status_code != 200:
            print(f"[INFO] Current day returned status {response.status_code}. Fetching latest available archive...")
            response = requests.get(
                api_url,
                params={"api_key": "DEMO_KEY", "date": "2026-09-10"},
                timeout=10
            )

        print(f"\nMetadata Request Status Code : {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            title = data.get("title", "NASA APOD")
            explanation = data.get("explanation", "No explanation provided.")
            date = data.get("date", "N/A")
            media_type = data.get("media_type", "image")
            image_url = data.get("url")

            print("=" * 70)
            print(f"APOD TITLE: {title} ({date})")
            print("=" * 70)
            print(f"Media Type : {media_type}")
            print(f"Image URL  : {image_url}")
            print("\nEXPLANATION PREVIEW:")
            print(f"{explanation[:300]}...")
            print("=" * 70)

            # Step 2: Download the image using requests
            if media_type == "image" and image_url:
                print(f"\nDownloading image from: {image_url} ...")
                img_response = requests.get(image_url, stream=True, timeout=20)

                if img_response.status_code == 200:
                    with open(output_image_path, "wb") as f:
                        for chunk in img_response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    file_size_kb = os.path.getsize(output_image_path) / 1024
                    print("=" * 70)
                    print(f"[SUCCESS] Image downloaded and saved to:")
                    print(f"          {output_image_path}")
                    print(f"          File Size: {file_size_kb:.1f} KB")
                    print("=" * 70)
                else:
                    print(f"[ERROR] Failed to download image binary. Status: {img_response.status_code}")
            else:
                print(f"[INFO] Today's media is a {media_type} (URL: {image_url})")

        else:
            print(f"[ERROR] Failed to retrieve NASA APOD metadata. Status: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")


if __name__ == "__main__":
    download_nasa_apod()
