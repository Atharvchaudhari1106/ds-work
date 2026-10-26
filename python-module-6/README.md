# Python Module 6: Core & Advanced Python Programming

Comprehensive hands-on Python exercises, real-world case studies, and coding assignments covering Python from fundamental syntax to advanced Object-Oriented Programming, functional paradigms, REST APIs, asynchronous programming, and data handling.

---

## 📚 Curriculum Overview

| Session | Topic / Focus Area | Key Concepts Covered |
| :--- | :--- | :--- |
| **SESSION-1** | Introduction & Setup | Python setup, notebooks, basic script execution (`analytics_intro.ipynb`, `hello_app.py`) |
| **SESSION-2** | Python Basics & Syntax | Variables, user inputs, comments, indentation conventions |
| **SESSION-3** | Data Types & Type Casting | Numeric types, float conversions, boolean evaluations, type casting |
| **SESSION-4** | String Operations | String manipulation, slicing, case conversions, f-strings, text cleaning |
| **SESSION-5** | Lists & Tuples | Indexing, slicing, mutable vs. immutable sequences, collection operations |
| **SESSION-6** | Dictionaries & Sets | Key-value mapping, set operations (union, intersection, difference), dictionary updates |
| **SESSION-7** | Control Flow & Conditionals | `if-elif-else` branches, nested conditions, eligibility & business logic checks |
| **SESSION-8** | Loops & Iteration | `for` and `while` loops, accumulator patterns, `enumerate()` |
| **SESSION-9** | Functions & Modularity | Defining functions, positional & keyword arguments, return values |
| **SESSION-12** | Functional Programming | `lambda` functions, `map()`, `filter()`, `reduce()` from `functools` |
| **SESSION-13** | Recursion & Variable Scope | Recursive algorithms, base cases, call stack, local vs. global scope |
| **SESSION-14** | File I/O & Serialization | Reading & writing text files, CSV handling, JSON serialization, `pathlib` |
| **SESSION-15** | Exception Handling | Robust programming with `try-except-else-finally`, custom exceptions |
| **SESSION-16** | Iterators & Generators | Iterables, `iter()`, `next()`, memory-efficient stream generation with `yield`, `zip()` |
| **SESSION-17** | Standard Library & Modules | Built-in modules (`math`, `datetime`, `statistics`), custom module imports |
| **SESSION-18** | Regular Expressions (`re`) | Pattern matching, phone/email validation, data masking, text extraction |
| **SESSION-19** | OOP: Classes & Objects | Class definitions, instance attributes, methods, constructors (`__init__`) |
| **SESSION 19 - APIs** | APIs: Introduction | What is an API?, JSON structure, REST (GET/POST), query params, custom HTTP headers |
| **SESSION-20** | OOP: Encapsulation | Private/protected attributes, getters & setters, property decorators |
| **SESSION 20 - APIs** | APIs Using Requests (Part 1) | `requests.get()`, `requests.post()`, status codes, JSON responses, query params, OMDB API |
| **SESSION-21** | OOP: Inheritance & Polymorphism | Base and derived classes, `super()`, method overriding, polymorphic behavior |
| **SESSION 21 - APIs** | APIs Using Requests (Part 2) | POST with JSON payloads, interactive user input, ReqRes API, exporting data to CSV/JSON| **SESSION 22 - APIs** | Advanced APIs & Authentication | `requests.Session()`, async APIs with `httpx` & `asyncio`, OpenWeatherMap, Bearer auth, OAuth 2.0 |
| **SESSION 23 - APIs** | API Mini Projects | OpenWeatherMap, CoinGecko crypto rates, NASA APOD downloader, COVID-19 tables, multi-API dashboard |
| **SESSION 24 - APIs** | Binance Crypto Price Tracker (Part 1) | CoinGecko markets API, top 10 crypto prices, 24h high/low, % change, CSV export, error handling |
| **SESSION 25 - APIs** | Binance Crypto Price Tracker (Part 2) | Binance 24hr ticker API, volatility calculation, below-average scanner, volume ranking, hourly scheduler |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ installed on your system.
- Required packages:
  ```bash
  pip install requests httpx schedule
  ```

### Running Any Task
Clone the repository and run any session script directly with Python:

```bash
# Clone the repository
git clone https://github.com/Atharvchaudhari1106/python-module-6.git
cd python-module-6

# Run a specific session task
python SESSION-4/task4_f-string.py
python SESSION-14/task3_ipl_csv.py
python "SESSION 19 - APIs - Introduction/task1_get_posts.py"
python "SESSION 20 - APIs Using Requests (Part 1)/task1_fetch_posts.py"
python "SESSION 21 - APIs Using Requests (Part 2)/task1_post_json.py"
python "SESSION 22 - Advanced APIs - requests.Session()/task1_flipkart_session.py"
python "SESSION 23 - API Mini Projects - Weather API/task2_crypto_prices_coingecko.py"
python "SESSION 24 - Case Study - Binance Crypto Price Tracker (Part 1)/crypto_tracker_part1.py"
python "SESSION 25 - Case Study - Binance Crypto Price Tracker (Part 2)/crypto_tracker_part2.py"
python SESSION-21/task1_inheritance.py
```

---

## 🗂️ Project Structure

```text
python-module-6/
├── SESSION-1/                                  # Intro to analytics & basic scripts
├── SESSION-2/                                  # Syntax, variables & indentation
├── SESSION-3/                                  # Data types & conversions
├── SESSION-4/                                  # String manipulation & f-strings
├── SESSION-5/                                  # Lists and tuples
├── SESSION-6/                                  # Dictionaries and sets
├── SESSION-7/                                  # Conditional logic
├── SESSION-8/                                  # Loops & iteration
├── SESSION-9/                                  # Reusable functions
├── SESSION-12/                                 # Lambda, map, filter, reduce
├── SESSION-13/                                 # Recursion & scope
├── SESSION-14/                                 # File I/O, CSV, JSON & pathlib
├── SESSION-15/                                 # Exception handling
├── SESSION-16/                                 # Iterators & generators
├── SESSION-17/                                 # Python standard modules
├── SESSION-18/                                 # Regular expressions (regex)
├── SESSION-19/                                 # OOP: Classes & objects
├── SESSION 19 - APIs - Introduction/          # REST APIs, requests, JSON, params & headers
│   ├── task1_get_posts.py
│   ├── task2_zomato_json.py
│   ├── task3_post_playlist.py
│   ├── task4_query_params.py
│   ├── task5_custom_headers.py
│   └── README.md
├── SESSION-20/                                 # OOP: Encapsulation & getters/setters
├── SESSION 20 - APIs Using Requests (Part 1)/ # requests.get(), requests.post(), params, OMDB API
│   ├── task1_fetch_posts.py
│   ├── task2_create_post.py
│   ├── task3_filter_users.py
│   ├── task4_omdb_movies.py
│   └── README.md
├── SESSION-21/                                 # OOP: Inheritance & polymorphism
├── SESSION 21 - APIs Using Requests (Part 2)/ # POST with JSON, ReqRes, export to CSV & JSON
│   ├── task1_post_json.py
│   ├── task2_playlist_input_post.py
│   ├── task3_reqres_create_user.py
│   ├── task4_save_posts_to_csv.py
│   ├── task5_save_posts_to_json.py
│   ├── posts.csv
│   ├── posts.json
│   └── README.md
├── SESSION 22 - Advanced APIs - requests.Session()/ # requests.Session(), OpenWeatherMap, httpx async, Bearer, OAuth 2.0
│   ├── task1_flipkart_session.py
│   ├── task2_openweathermap.py
│   ├── task3_async_apis_httpx.py
│   ├── task4_bearer_auth.py
│   ├── task5_oauth_url_generator.py
│   └── README.md
├── SESSION 23 - API Mini Projects - Weather API/ # Weather, CoinGecko crypto, NASA APOD, COVID-19, Multi-API
│   ├── task1_weather_api.py
│   ├── task2_crypto_prices_coingecko.py
│   ├── task3_nasa_apod_downloader.py
│   ├── task4_covid_statistics_india.py
│   ├── task5_multi_api_dashboard.py
│   ├── nasa_apod.jpg
│   └── README.md
├── SESSION 24 - Case Study - Binance Crypto Price Tracker (Part 1)/ # Top 10 crypto, 24h change, high/low, CSV export
│   ├── crypto_tracker_part1.py
│   ├── crypto_prices.csv
│   └── README.md
├── SESSION 25 - Case Study - Binance Crypto Price Tracker (Part 2)/ # Binance 24hr API, volatility, average price, volume rank, scheduler
│   ├── crypto_tracker_part2.py
│   ├── scheduler_hourly.py
│   ├── crypto_data.json
│   └── README.md
├── .gitignore                                  # Git ignore rules
└── README.md                                   # Documentation
```

---

## 👤 Author
- **Atharv Chaudhari** ([@Atharvchaudhari1106](https://github.com/Atharvchaudhari1106))
