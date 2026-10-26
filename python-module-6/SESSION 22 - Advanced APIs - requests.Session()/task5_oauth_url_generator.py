"""
Task 5: OAuth 2.0 Authorization Flow - Step 1 (Redirect URL Generator)
Demonstrates the first step of an OAuth 2.0 login flow by generating the URL
to redirect a user to Spotify's OAuth 2.0 authorization page.

Includes a brief explanation of what the code does and the role of each parameter.
"""

import secrets
import urllib.parse


def generate_spotify_oauth_url(client_id=None, redirect_uri=None, scopes=None):
    """
    Generates the Spotify OAuth 2.0 authorization URL for Step 1 of the Authorization Code Flow.
    """
    # 1. Spotify's OAuth 2.0 Authorization Endpoint
    auth_base_url = "https://accounts.spotify.com/authorize"

    # 2. Configure Client Credentials & Callback URI
    if not client_id:
        client_id = "your_registered_spotify_client_id_here"
    if not redirect_uri:
        redirect_uri = "https://myapp.example.com/api/auth/spotify/callback"
    if not scopes:
        scopes = [
            "user-read-private",
            "user-read-email",
            "playlist-read-private",
            "user-top-read"
        ]

    # 3. Generate a cryptographically secure state token to prevent CSRF attacks
    state_token = secrets.token_urlsafe(16)

    # 4. Construct query parameters required by OAuth 2.0 (RFC 6749)
    query_parameters = {
        "client_id": client_id,
        "response_type": "code",                    # Requests an authorization code grant
        "redirect_uri": redirect_uri,               # Where Spotify sends user after approval
        "scope": " ".join(scopes),                  # Space-delimited permissions requested
        "state": state_token,                       # Anti-CSRF verification token
        "show_dialog": "true"                       # Force approval prompt for testing
    }

    # 5. Encode parameters cleanly into a standard URL query string
    encoded_query = urllib.parse.urlencode(query_parameters)
    full_authorization_url = f"{auth_base_url}?{encoded_query}"

    return full_authorization_url, state_token, query_parameters


def main():
    print("=" * 70)
    print("Task 5: OAuth 2.0 Authorization Flow - Step 1 URL Generation")
    print("=" * 70)

    auth_url, state, params = generate_spotify_oauth_url()

    print("\n[Generated Spotify OAuth 2.0 Authorization URL]:")
    print("-" * 70)
    print(auth_url)
    print("-" * 70)

    print("\n" + "=" * 70)
    print("Explanation of OAuth 2.0 Step 1 Components:")
    print("=" * 70)
    print("1. Authorization Base URL (https://accounts.spotify.com/authorize):")
    print("   The endpoint where Spotify prompts the user to log in and grant permissions.")
    print()
    print("2. client_id:")
    print("   The unique identifier assigned to your registered application by Spotify.")
    print()
    print("3. response_type='code':")
    print("   Tells Spotify to return an 'Authorization Code' instead of a raw access token.")
    print("   The backend exchanges this code later for secure access and refresh tokens.")
    print()
    print("4. redirect_uri:")
    print(f"   The callback endpoint ({params['redirect_uri']}) where the user is")
    print("   redirected after granting permission. Must match Spotify Developer Dashboard.")
    print()
    print("5. scope:")
    print(f"   Specific permissions requested ({params['scope']}).")
    print()
    print("6. state (CSRF Protection):")
    print(f"   Random token ({state}). Your server stores this in the user session")
    print("   and verifies that Spotify sends the exact same state back in Step 2.")
    print("=" * 70)


if __name__ == "__main__":
    main()
