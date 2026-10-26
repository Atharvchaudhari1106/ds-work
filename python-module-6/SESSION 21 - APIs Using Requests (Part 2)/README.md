# SESSION 21: APIs Using Requests (Part 2)

> **Concepts Covered:** Advanced POST Requests with JSON Payloads • User Input Integration • Consuming Third-Party APIs (ReqRes) • Response Parsing (`response.json()`) • Exporting API Data to CSV and JSON formats

---

## 📖 Theoretical Concepts

### 1. Sending Data via `requests.post()`
When sending structured payloads to REST APIs:
```python
payload = {"title": "Post Title", "body": "Post description", "userId": 1}
response = requests.post(url, json=payload)
```
- **`json=payload` parameter**: Automatically serializes the Python dictionary to a JSON-formatted string and sets the HTTP header `Content-Type: application/json`.
- **Expected Status Codes**: Typically `201 Created` upon successful resource creation.

### 2. Extracting Nested & Dynamic Data
Modern APIs return metadata and timestamps alongside entity IDs:
```python
data = response.json()
user_id = data.get("id")
created_at = data.get("createdAt")
```

### 3. Persisting API Data
- **CSV Export (`csv` module)**: Best for tabular data analysis in tools like Excel, Pandas, or database bulk loaders. Uses `csv.DictWriter` to enforce column headers.
- **JSON Export (`json` module)**: Best for preserving hierarchical and nested data structures using `json.dump(data, file, indent=4)`.

---

## 📝 Tasks & Solutions Summary

| File | Task Description | Key Concepts Demonstrated |
| :--- | :--- | :--- |
| [`task1_post_json.py`](task1_post_json.py) | POST request to JSONPlaceholder with title, body, userId | `requests.post(url, json=payload)`, HTTP 201 |
| [`task2_playlist_input_post.py`](task2_playlist_input_post.py) | Interactive user input for playlist name/description, extract created ID | CLI user prompts, dynamic payload construction, extracting returned ID |
| [`task3_reqres_create_user.py`](task3_reqres_create_user.py) | POST request to ReqRes (`/api/users`), extract `id` and `createdAt` | Third-party API integration, extracting created resource metadata |
| [`task4_save_posts_to_csv.py`](task4_save_posts_to_csv.py) | Fetch latest 5 posts and save titles & userIds to `posts.csv` | `requests.get()`, list slicing, `csv.DictWriter` |
| [`task5_save_posts_to_json.py`](task5_save_posts_to_json.py) | Fetch latest 5 posts and save to `posts.json` | `requests.get()`, `json.dump()`, structured formatting |

---

## 📄 Exported Data Files

- [`posts.csv`](posts.csv): Contains headers `userId,id,title` for the first 5 posts.
- [`posts.json`](posts.json): Formatted JSON array containing the full attributes of the first 5 posts.

---

## 🚀 How to Run

```bash
# Task 1: POST request with JSON payload
python task1_post_json.py

# Task 2: Interactive playlist input & POST
python task2_playlist_input_post.py

# Task 3: ReqRes user creation & timestamp extraction
python task3_reqres_create_user.py

# Task 4: Export latest 5 posts to CSV
python task4_save_posts_to_csv.py

# Task 5: Export latest 5 posts to JSON
python task5_save_posts_to_json.py
```
