# SESSION 22: Advanced APIs & Authentication

> **Concepts Covered:** `requests.Session()` • Cookie and Connection Persistence • Async HTTP with `httpx` & `asyncio.gather()` • Authentication Schemes (API Keys, Bearer Tokens) • OAuth 2.0 Authorization Code Flow (Step 1 URL Generation)

---

## 📖 Theoretical Concepts

### 1. `requests.Session()` & State Persistence
Standard `requests.get()` opens a new TCP connection on every call and discards cookies upon completion. `requests.Session()`:
- Maintains an underlying TCP connection pool (HTTP Keep-Alive).
- Persists cookies automatically across multiple requests (ideal for login workflows).
- Applies common headers and parameters across all requests.

### 2. Synchronous vs Asynchronous API Calls
- **Synchronous (`requests`)**: Blocks the execution thread until the server responds. Running multiple requests sequentially sums up their latency (`time = t1 + t2`).
- **Asynchronous (`httpx` + `asyncio`)**: Uses an event loop to initiate multiple network calls concurrently (`asyncio.gather()`). Total wait time is bounded by the slowest request (`time = max(t1, t2)`).

### 3. API Authentication Paradigms
- **API Keys**: Unique strings passed via query parameters (e.g. `?appid=KEY`) or custom headers.
- **Bearer Tokens / JWT**: Passed in the standard `Authorization` header:
  ```http
  Authorization: Bearer <token_string>
  ```
- **OAuth 2.0 (Authorization Code Flow)**:
  - **Step 1**: Application generates an authorization redirect URL to the provider (e.g., Spotify, Google) including `client_id`, `redirect_uri`, `scope`, and a secure `state` parameter.
  - **Step 2**: User authenticates with the provider and grants access.
  - **Step 3**: Provider redirects to `redirect_uri` with a temporary `code`.
  - **Step 4**: Server exchanges `code` with provider backend for an `access_token`.

---

## 📝 Tasks & Solutions Summary

| File | Task Description | Key Concepts Demonstrated |
| :--- | :--- | :--- |
| [`task1_flipkart_session.py`](task1_flipkart_session.py) | Fetch Flipkart order history twice with `requests.Session()` | Cookie persistence, session headers, inspect status codes |
| [`task2_openweathermap.py`](task2_openweathermap.py) | Query OpenWeatherMap API for Ahmedabad temperature | API key parameters (`appid`), metric units, parsing temperature data |
| [`task3_async_apis_httpx.py`](task3_async_apis_httpx.py) | Concurrent async fetch from two APIs (Spotify & BookMyShow simulation) | `httpx.AsyncClient()`, `asyncio.gather()`, non-blocking I/O |
| [`task4_bearer_auth.py`](task4_bearer_auth.py) | Authenticated user profile retrieval with Bearer token | `Authorization: Bearer <token>` header format, extracting user details |
| [`task5_oauth_url_generator.py`](task5_oauth_url_generator.py) | Generate OAuth 2.0 Step 1 Authorization Redirect URL for Spotify | `urllib.parse.urlencode`, CSRF protection with `state`, OAuth params |

---

## 🚀 How to Run

```bash
# Task 1: Flipkart session test
python task1_flipkart_session.py

# Task 2: OpenWeatherMap temperature lookup
python task2_openweathermap.py

# Task 3: Async concurrent fetch with httpx & asyncio
python task3_async_apis_httpx.py

# Task 4: Bearer token authenticated profile fetch
python task4_bearer_auth.py

# Task 5: Spotify OAuth 2.0 URL generator
python task5_oauth_url_generator.py
```
