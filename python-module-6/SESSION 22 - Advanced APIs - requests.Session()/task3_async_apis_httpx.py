"""
Task 3: Concurrent Async Data Fetch with asyncio and httpx
Simulate an async data fetch from two different APIs (for example, fetch trending songs
from Spotify and trending movies from BookMyShow) using Python's asyncio and httpx library,
and print both results when done.

Hint: Use asyncio.gather() to run both requests concurrently.
"""

import asyncio
import time
import httpx


async def fetch_trending_songs(client: httpx.AsyncClient):
    """Simulates fetching top trending songs asynchronously from Spotify."""
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {"userId": 1}
    print("[SONGS] Starting async request for Spotify trending songs...")

    start_time = time.time()
    response = await client.get(url, params=params, timeout=10)
    elapsed = time.time() - start_time

    if response.status_code == 200:
        posts = response.json()
        # Transform into song records
        songs = [
            {
                "rank": idx,
                "track_name": f"Track: {post.get('title')[:30].title()}...",
                "artist": f"Artist {post.get('id')}",
                "stream_count": f"{post.get('id') * 125000:,} plays"
            }
            for idx, post in enumerate(posts[:3], start=1)
        ]
        print(f"[SONGS] Completed in {elapsed:.2f}s (Fetched {len(songs)} tracks)")
        return songs
    else:
        return []


async def fetch_trending_movies(client: httpx.AsyncClient):
    """Simulates fetching top trending movies asynchronously from BookMyShow."""
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {"userId": 2}
    print("[MOVIES] Starting async request for BookMyShow trending movies...")

    start_time = time.time()
    response = await client.get(url, params=params, timeout=10)
    elapsed = time.time() - start_time

    if response.status_code == 200:
        posts = response.json()
        # Transform into movie records
        movies = [
            {
                "rank": idx,
                "title": f"Movie: {post.get('title')[:30].title()}...",
                "rating": f"{8.0 + (post.get('id') % 10) * 0.1:.1f}/10",
                "genre": ["Action", "Sci-Fi", "Drama"][post.get('id') % 3]
            }
            for idx, post in enumerate(posts[:3], start=1)
        ]
        print(f"[MOVIES] Completed in {elapsed:.2f}s (Fetched {len(movies)} movies)")
        return movies
    else:
        return []


async def main():
    print("=" * 65)
    print("Task 3: Asynchronous Concurrent API Calls with httpx & asyncio")
    print("=" * 65)

    overall_start = time.time()

    # Create a shared asynchronous HTTP client session
    async with httpx.AsyncClient() as client:
        print("Launching both API requests concurrently via asyncio.gather()...\n")
        # Run both async coroutines concurrently
        songs_result, movies_result = await asyncio.gather(
            fetch_trending_songs(client),
            fetch_trending_movies(client)
        )

    total_duration = time.time() - overall_start

    print("\n" + "=" * 65)
    print(f"[COMPLETED] Total Concurrent Execution Time: {total_duration:.2f} seconds")
    print("=" * 65)

    print("\n--- Trending Songs (Spotify Simulation) ---")
    for song in songs_result:
        print(f"  #{song['rank']} | {song['track_name']} | {song['artist']} ({song['stream_count']})")

    print("\n--- Trending Movies (BookMyShow Simulation) ---")
    for movie in movies_result:
        print(f"  #{movie['rank']} | {movie['title']} | Genre: {movie['genre']} | Rating: {movie['rating']}")

    print("=" * 65)


if __name__ == "__main__":
    asyncio.run(main())
