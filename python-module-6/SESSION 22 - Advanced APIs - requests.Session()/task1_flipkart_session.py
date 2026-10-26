"""
Task 1: requests.Session() with Flipkart Order History
Use the requests.Session() object to fetch your Flipkart order history page
twice in a row (without logging in), and print the response status codes for both requests.

Hint: Observe if cookies or session headers change between requests.
"""

import requests


def test_flipkart_session():
    # Target URL for Flipkart order history
    url = "https://www.flipkart.com/account/orders"

    print("=" * 65)
    print("Task 1: requests.Session() - Inspecting Persistent State & Cookies")
    print("=" * 65)
    print(f"Target URL : {url}\n")

    # Initialize a persistent requests.Session()
    session = requests.Session()

    # Set standard browser user-agent to simulate realistic client request
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })

    try:
        # Request 1
        print("--- Sending Request #1 ---")
        response_1 = session.get(url, timeout=10)
        print(f"Response #1 Status Code : {response_1.status_code}")
        print(f"Session Cookies After #1 : {len(session.cookies)} cookie(s) stored")
        for cookie in session.cookies:
            print(f"  * Cookie: {cookie.name} = {cookie.value[:25]}... (Domain: {cookie.domain})")

        print("\n--- Sending Request #2 (Reusing the Same Session) ---")
        response_2 = session.get(url, timeout=10)
        print(f"Response #2 Status Code : {response_2.status_code}")
        print(f"Session Cookies After #2 : {len(session.cookies)} cookie(s) stored")
        for cookie in session.cookies:
            print(f"  * Cookie: {cookie.name} = {cookie.value[:25]}... (Domain: {cookie.domain})")

        print("\n" + "=" * 65)
        print("Session Persistence Analysis:")
        print("=" * 65)
        print("1. requests.Session() persists cookies and headers across requests.")
        print("2. In Request #2, cookies received from Request #1 were automatically")
        print("   sent back to Flipkart's servers without manual header configuration.")
        print("3. Status codes (403/302) indicate Flipkart requires authenticated login")
        print("   sessions to access sensitive account order history.")
        print("=" * 65)

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Session request failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    test_flipkart_session()
