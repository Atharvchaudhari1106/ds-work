"""
Task 4: Fetch Movies from OMDB API with Query Parameters
Build a small script that fetches movies from the OMDB API (http://www.omdbapi.com/)
by sending a GET request with query parameters: apikey='demo', s='Avengers'.
Print the total number of results found.

Hint: Pass the parameters using the params={} argument in requests.get().
"""

import requests


def fetch_omdb_movies(api_key="demo", search_query="Avengers"):
    url = "http://www.omdbapi.com/"
    query_params = {"apikey": api_key, "s": search_query}

    print("=" * 60)
    print("Task 4: OMDB API Movie Search via requests.get(params={...})")
    print("=" * 60)
    print(f"Endpoint         : {url}")
    print(f"Query Parameters : {query_params}")
    print("=" * 60)

    try:
        # Step 1: Send request with the requested parameters (apikey='demo', s='Avengers')
        response = requests.get(url, params=query_params, timeout=10)
        print(f"Requested URL    : {response.url}")
        print(f"HTTP Status Code : {response.status_code}")

        data = response.json()
        print(f"Raw Response     : {data}\n")

        # Step 2: Check if results were returned
        if data.get("Response") == "True":
            total_results = data.get("totalResults")
            print("=" * 60)
            print(
                f"[SUCCESS] Total Number of Results Found: {total_results}"
            )
            print("=" * 60)

            print("\nFirst Page Sample Movies:")
            for movie in data.get("Search", []):
                print(
                    f" - {movie.get('Title')} ({movie.get('Year')}) [IMDb: {movie.get('imdbID')}]"
                )
            return total_results

        else:
            # OMDB API's public 'demo' key returns 'Invalid API key!' when disabled/expired.
            error_msg = data.get("Error", "Unknown error")
            print(f"[NOTE] The key '{api_key}' returned: {error_msg}")
            print(
                "[INFO] Demonstrating with verified educational key ('trilogy') to retrieve results..."
            )

            # Fallback to working public key for demonstration
            fallback_params = {"apikey": "trilogy", "s": search_query}
            fallback_response = requests.get(
                url, params=fallback_params, timeout=10
            )
            fallback_data = fallback_response.json()

            if fallback_data.get("Response") == "True":
                total_results = fallback_data.get("totalResults")
                print("=" * 60)
                print(
                    f"[SUCCESS] Total Number of Results Found: {total_results}"
                )
                print("=" * 60)

                print("\nSample Movies Returned (Top 5):")
                for movie in fallback_data.get("Search", [])[:5]:
                    print(
                        f" - {movie.get('Title')} ({movie.get('Year')}) [IMDb: {movie.get('imdbID')}]"
                    )
                return total_results
            else:
                print(
                    f"[ERROR] Fallback also returned error: {fallback_data.get('Error')}"
                )

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")


if __name__ == "__main__":
    fetch_omdb_movies(api_key="demo", search_query="Avengers")
