# SESSION 20: APIs Using Requests (Part 1)

> **Concepts Covered:** `requests.get()`, `requests.post()` • Inspecting `.status_code` & `.json()` • Query Parameters (`params={}`) • Filtering API Responses • External REST APIs (OMDB)

---

## 📖 Key API Concepts

### 1. `requests.get()` vs `requests.post()`
- **`requests.get(url, params={})`**: Used to fetch data from an endpoint without modifying the server state. Supports query parameters appended to the URL string.
- **`requests.post(url, json={})`**: Used to submit new data/resources to an endpoint. In `requests`, passing a dictionary to the `json=` parameter automatically serializes it to a JSON string and sets the `Content-Type: application/json` header.

### 2. Inspecting Responses
- **`response.status_code`**: Returns the numeric HTTP status (e.g., `200` OK, `201` Created, `400` Bad Request, `401` Unauthorized, `404` Not Found).
- **`response.json()`**: Deserializes JSON response body into native Python dictionaries or lists.
- **`response.url`**: Shows the final URL after query parameters are encoded and redirects followed.

### 3. Query Parameters (`params={}`)
Instead of manually concatenating query strings (e.g., `url + "?key=value"`), pass a dictionary to `params`:
```python
response = requests.get(
    "http://www.omdbapi.com/", params={"apikey": "demo", "s": "Avengers"}
)
```
The library automatically encodes special characters, spaces, and formatting.

---

## 📝 Tasks & Solutions Summary

| File | Task Summary | Concepts Demonstrated |
| :--- | :--- | :--- |
| [`task1_fetch_posts.py`](task1_fetch_posts.py) | Fetch posts from JSONPlaceholder, print status code & 1st post title | `requests.get()`, `response.status_code`, `response.json()[0]` |
| [`task2_create_post.py`](task2_create_post.py) | Send POST request with `title`, `body`, `userId=101` | `requests.post()`, `json=payload`, HTTP 201 Created |
| [`task3_filter_users.py`](task3_filter_users.py) | Fetch users and extract usernames with emails ending in `.org` | `requests.get()`, list iteration, string method `.endswith('.org')` |
| [`task4_omdb_movies.py`](task4_omdb_movies.py) | Query OMDB API with `apikey='demo'` and `s='Avengers'`, print `totalResults` | Query params with `params={}`, API key handling, parsing search results |

---

## 🚀 How to Run

```bash
# Task 1: Fetch posts and print first title
python task1_fetch_posts.py

# Task 2: Create a post via POST request
python task2_create_post.py

# Task 3: Filter users by .org email
python task3_filter_users.py

# Task 4: Search OMDB movies and print total results
python task4_omdb_movies.py
```
