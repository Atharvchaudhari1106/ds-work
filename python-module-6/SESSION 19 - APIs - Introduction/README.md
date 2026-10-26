# SESSION 19: APIs - Introduction

> **Concepts Covered:** What is an API? • JSON Data Structure • REST Architecture (GET, POST, PUT, DELETE) • HTTP Headers • Query Parameters • Rate Limits

---

## 📖 Theoretical Concepts

### 1. What is an API?
An **API (Application Programming Interface)** acts as a messenger or contract between different software applications. It defines rules, endpoints, and data formats allowing one application (e.g., a mobile client or frontend web app) to request data or invoke services from a backend server.

### 2. JSON Structure
**JSON (JavaScript Object Notation)** is the standard data interchange format used by modern REST APIs.
- Lightweight, language-independent, human-readable text.
- Formatted as key-value pairs (equivalent to Python `dict`) and lists of values (equivalent to Python `list`).
- Python handles JSON seamlessly with `json.dumps()` (serialization to string) and `json.loads()` (deserialization from string).

### 3. REST Architecture & HTTP Methods
**REST (Representational State Transfer)** relies on stateless client-server communication using standard HTTP methods:
- **`GET`**: Retrieve resources without modifying server state (Safe & Idempotent).
- **`POST`**: Create new resources on the server.
- **`PUT`**: Replace / fully update an existing resource.
- **`PATCH`**: Partially update specific fields of a resource.
- **`DELETE`**: Remove a resource from the server.

### 4. HTTP Headers, Query Parameters & Rate Limits
- **HTTP Headers**: Metadata sent alongside the request or response (e.g., `Authorization: Bearer <token>`, `Content-Type: application/json`, `User-Agent`).
- **Query Parameters**: Key-value pairs appended to the URL query string (`?key=value&key2=value2`) used to filter, sort, or paginate data (e.g., `userId=2`).
- **Rate Limits**: Mechanisms enforced by servers (often signaled via `X-RateLimit-*` headers and HTTP `429 Too Many Requests`) to restrict how frequently a client can make requests in a given time window.

---

## 📝 Practical Tasks & Solutions

| File | Task Summary | Concepts Demonstrated |
| :--- | :--- | :--- |
| [`task1_get_posts.py`](task1_get_posts.py) | Fetch first 5 posts from `https://jsonplaceholder.typicode.com/posts` | `requests.get()`, HTTP 200, `.json()`, list slicing |
| [`task2_zomato_json.py`](task2_zomato_json.py) | Represent Zomato restaurant object and serialize to JSON | Python `dict`, nested objects, `json.dumps(..., indent=4)` |
| [`task3_post_playlist.py`](task3_post_playlist.py) | Create new playlist resource via POST request | `requests.post()`, JSON payloads, HTTP 201 Created |
| [`task4_query_params.py`](task4_query_params.py) | Filter posts by `userId=2` using query parameters | `requests.get(url, params={'userId': 2})`, URL query string |
| [`task5_custom_headers.py`](task5_custom_headers.py) | Send GET request with custom `Authorization` & headers | `headers={'Authorization': 'Bearer ...'}`, header inspection |

---

## 🚀 How to Run

```bash
# Task 1: Fetch and display first 5 posts
python task1_get_posts.py

# Task 2: Zomato restaurant dictionary to JSON
python task2_zomato_json.py

# Task 3: Send POST request to add playlist
python task3_post_playlist.py

# Task 4: Filter posts by userId query parameter
python task4_query_params.py

# Task 5: Request with custom Authorization header
python task5_custom_headers.py
```
