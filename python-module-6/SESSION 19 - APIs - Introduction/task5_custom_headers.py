"""
Task 5: Setting Custom HTTP Headers in Python Requests
Research using ChatGPT or Copilot to find out how to set custom HTTP headers
(like 'Authorization') in a Python requests call.
Write a short code snippet that sends a GET request to any API endpoint
with a custom header and print the response status code.
"""

import requests


def request_with_custom_headers():
    # We use httpbin.org/headers, which inspects and echoes back all received headers.
    url = "https://httpbin.org/headers"

    # Define custom headers dictionary
    custom_headers = {
        "Authorization": "Bearer sample_jwt_token_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        "User-Agent": "StudentAPIClient/1.0 (Module6_Coursework)",
        "Accept": "application/json",
        "X-Request-Source": "Python-Requests-Session-19",
    }

    print("=" * 60)
    print(f"Target API Endpoint : {url}")
    print("=" * 60)
    print("Custom HTTP Headers to Send:")
    for header, value in custom_headers.items():
        print(f"  * {header}: {value}")
    print("=" * 60)

    try:
        # Pass the headers dictionary via the `headers` parameter in requests.get()
        response = requests.get(url, headers=custom_headers, timeout=10)

        print(f"\nResponse Status Code : {response.status_code}")

        if response.status_code == 200:
            print("\nServer Received Headers (Echo Verification):")
            data = response.json()
            received_headers = data.get("headers", {})

            for key, val in received_headers.items():
                marker = (
                    "[CUSTOM]"
                    if key
                    in [
                        "Authorization",
                        "User-Agent",
                        "X-Request-Source",
                        "Accept",
                    ]
                    else "[DEFAULT]"
                )
                print(f"  {marker:<9} {key}: {val}")

            print(
                "\n[SUCCESS] Custom 'Authorization' header was received and processed by the server!"
            )
        else:
            print(
                f"[WARNING] Received non-200 HTTP status code: {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending the request: {e}")


if __name__ == "__main__":
    request_with_custom_headers()
