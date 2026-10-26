# Section A — Concept Application: Detailed Assessment Answers

**Program**: Data Science  
**Assessment Code**: M2-A1  
**Stack**: Python / Git  

---

### Question 1 (Scenario S1): Data Science Lifecycle & Generative AI Integration

#### 1. Data Science Lifecycle Walkthrough & Concrete Deliverables
- **Stage 1: Problem Definition**  
  The business objective is translated into a supervised time-series and tabular forecasting problem: predicting order demand volume per restaurant zone during peak dinner hours (7:00 PM – 9:00 PM).  
  *Concrete Deliverable*: **Business Problem & Metric Framing Document (BRS)** specifying model targets, acceptance thresholds (e.g., target MAE < 15 orders/zone, WAPE < 10%), latency SLAs for delivery partner dispatch, and business ROI metrics.
- **Stage 2: Data Collection**  
  Consolidates two years of historical order records stored across disparate spreadsheets, geospatial polygon definitions of delivery zones, restaurant operating hours, customer addresses, weather historical logs, and calendar event/holiday datasets.  
  *Concrete Deliverable*: **Raw Ingestion Pipeline & Centralized Parquet/Warehouse Dataset** with an immutable schema catalog and data lineage tracking.
- **Stage 3: Data Preparation**  
  Involves cleaning corrupted spreadsheet values, resolving missing restaurant zone mappings, normalizing timestamp formats to local operational timezones, treating outliers (e.g., promotional anomalies, delivery cancellations), and engineering features (e.g., rolling 30-day average demand, zone historical order velocity, weather severity index, day-of-week cyclical encoding).  
  *Concrete Deliverable*: **Cleaned, Standardized Feature-Engineered Dataset (Training/Validation/Test Matrix)** with automated schema validation checks.
- **Stage 4: Exploration (EDA)**  
  Performs exploratory data analysis to uncover temporal patterns, seasonal peaks, zone-level demand skewness, correlations between bad weather and order surge, and traffic congestion patterns.  
  *Concrete Deliverable*: **Exploratory Data Analysis Report & Geospatial Heatmaps** containing statistical distributions, correlation matrices, and operational bottleneck insights.
- **Stage 5: Modelling**  
  Selects and trains machine learning algorithms suited for tabular demand forecasting, such as LightGBM, XGBoost, CatBoost, and baseline ARIMA/Prophet models, performing hyperparameter tuning with time-based cross-validation.  
  *Concrete Deliverable*: **Versioned Trained Model Artifacts (e.g., `.pkl` / ONNX files)** accompanied by hyperparameter logs and training run metrics.
- **Stage 6: Evaluation**  
  Validates model performance on out-of-time test sets using MAE, RMSE, and operational cost metrics (under-dispatch penalty vs. over-dispatch idle driver cost), followed by backtesting against the existing gut-feeling baseline.  
  *Concrete Deliverable*: **Model Validation & Business Impact Assessment Report** with deployment sign-off and drift monitoring specifications.

#### 2. Generative AI Acceleration & Unsupervised Risks
1. **Stage: Data Preparation**  
   - *Assistance Task*: Generative AI can accelerate writing complex regular expressions, data normalization scripts, and fuzzy string matching functions to reconcile mislabeled restaurant zones across 24 months of inconsistent spreadsheets.  
   - *Risk without Human Review*: The AI may hallucinate mapping logic or silently introduce data leakage (e.g., imputing missing values using information from future time intervals), contaminating the training dataset and inflating offline accuracy unrealistically.
2. **Stage: Exploration (EDA)**  
   - *Assistance Task*: Generative AI can rapidly generate dynamic visualization scripts (Plotly/Seaborn), write boilerplate SQL aggregation queries, and summarize multi-dimensional statistical distributions into executive summaries.  
   - *Risk without Human Review*: The AI may draw false causal conclusions from purely coincidental correlations (spurious correlation) or overlook real-world domain nuances (such as food delivery festival surge patterns), leading analysts to build features on misleading assumptions.

---

### Question 2 (Scenario S2): Git Branching Strategy & Coordination

#### 1. Branching Strategy & Coordination Workflow
To eliminate breaking changes on the shared code base without slowing down parallel development, the team adopts a **Feature Branching Strategy** (such as GitHub Flow) coupled with branch protection rules on `main`. Under this policy, direct pushes to `main` are strictly blocked. The `main` branch is reserved strictly for production-ready, passing code. Each developer isolates their task within a short-lived feature branch. Continuous integration (CI) tests run automatically on every branch, ensuring that data cleaning, reporting, and order tracking do not introduce conflicting code until properly integrated and verified.

#### 2. Exact Sequence of Git Commands per Developer
1. Ensure the local `main` branch is up-to-date:
   ```bash
   git checkout main
   git pull origin main
   ```
2. Create and switch to a dedicated feature branch:
   ```bash
   git checkout -b feature/order-tracking
   ```
3. Develop the feature, then stage and commit changes incrementally:
   ```bash
   git add src/order_tracking.py
   git commit -m "feat: implement real-time order status tracking handler"
   ```
4. Push the branch to the remote GitHub repository:
   ```bash
   git push -u origin feature/order-tracking
   ```
5. Open a Pull Request (PR) against `main` on GitHub for peer review and automated test checks.
6. Once the PR is approved, merge it into `main` via the GitHub interface (or fast-forward merge), then clean up the local and remote feature branch:
   ```bash
   git checkout main
   git pull origin main
   git branch -d feature/order-tracking
   ```

#### 3. Realistic Merge Conflict Scenario & Step-by-Step Resolution
- **Conflict Scenario**: Both Developer A (data cleaning) and Developer B (order tracking) modify the root configuration file `src/config.py` on line 12 to add their respective settings (`CLEANED_DATA_PATH = "data/processed/"` vs `ORDER_STREAM_URL = "https://api.food.internal/orders"`). When Developer B attempts to merge `main` into their branch, Git halts with:
  ```
  CONFLICT (content): Merge conflict in src/config.py
  Automatic merge failed; fix conflicts and then commit the result.
  ```
- **Resolution Steps**:
  1. Open `src/config.py` to inspect the conflict markers:
     ```python
     <<<<<<< HEAD
     ORDER_STREAM_URL = "https://api.food.internal/orders"
     =======
     CLEANED_DATA_PATH = "data/processed/"
     >>>>>>> main
     ```
  2. Edit the file manually to keep *both* configuration settings, removing the `<<<<<<<`, `=======`, and `>>>>>>>` markers:
     ```python
     CLEANED_DATA_PATH = "data/processed/"
     ORDER_STREAM_URL = "https://api.food.internal/orders"
     ```
  3. Run local unit tests to verify both modules load correctly without syntax or runtime issues.
  4. Stage the resolved file and commit:
     ```bash
     git add src/config.py
     git commit -m "fix: resolve config merge conflict between cleaning and tracking settings"
     git push origin feature/order-tracking
     ```
  5. The Pull Request is now marked as conflict-free and can be safely merged.

---

### Question 3 (Scenario S3): Functional Programming with `map`, `filter`, and `reduce`

#### 1. Solution Design
We define a pure, named function `calculate_commission(amount)` that encapsulates the tiered commission business logic. We then apply this function across the collection of order dictionaries using `map()` combined with a `lambda`:
```python
def calculate_commission(amount):
    if amount <= 200:
        return amount * 0.10
    elif amount <= 500:
        return amount * 0.15
    else:
        return amount * 0.20

# Applying across order dictionaries using map and lambda
commission_records = list(map(lambda order: {
    **order,
    'commission': round(calculate_commission(order['amount']), 2)
}, orders))
```

#### 2. Why `map()` is More Appropriate than a Second `for` Loop
Using `map()` represents a declarative, functional programming paradigm rather than an imperative approach. In a `for` loop, the programmer must manually initialize an empty container (`results = []`), maintain iterative state, and manually call `.append()` on every cycle, introducing boilerplate code and potential mutation bugs. In contrast, `map()` expresses *what* transformation to apply rather than *how* to step through the collection. Furthermore, `map()` returns a lazy iterator in Python 3, computing transformed values on demand without allocating full intermediate lists in memory, which yields superior memory efficiency when processing high-volume streaming order feeds.

#### 3. Role of `filter()` for Audit Isolation
When the finance team requires records exceeding an audit threshold (e.g., high commission payouts > Rs 50), `filter()` provides a clean separation of concerns. Instead of embedding conditional logging or branching inside the payout computation, `filter()` isolates matching items declaratively:
```python
audit_records = list(filter(lambda rec: rec['commission'] > 50.0, commission_records))
```
This leaves the original transformation pure, testable, and reusable while producing an audit-ready subset.

#### 4. Role of `functools.reduce()` for Overall Total
`functools.reduce()` computes the cumulative total payout across all records in a single concise expression by folding the sequence:
```python
from functools import reduce
total_payout = reduce(lambda acc, rec: acc + rec['commission'], commission_records, 0.0)
```
`reduce` eliminates the need for an external mutable accumulator variable (`total = 0`), taking a binary function, sequentially applying it across the iterable from left to right, and yielding a single unified scalar value.

---

### Question 4 (Scenario S4): Object-Oriented Account Hierarchy & Robust Polymorphism

#### 1. Clean Modeling with Inheritance & Method Overriding
We define an abstract base class `User` that establishes shared identity attributes (such as `user_id`, `name`, and `email`) alongside a polymorphic interface method `display_profile()`. Each specialized subclass—`Customer`, `DeliveryPartner`, and `Admin`—inherits from `User` and provides its own implementation of `display_profile()`:
- `Customer.display_profile()` formats delivery addresses, favorite restaurants, and reward points.
- `DeliveryPartner.display_profile()` displays vehicle details, delivery rating, and total earnings.
- `Admin.display_profile()` outputs administrative permissions, audit levels, and system access logs.

This adheres to the Open-Closed Principle (open for extension, closed for modification): new user roles can be added without modifying client code that displays profiles.

#### 2. Specific Runtime Problem in Mixed List Iteration
If a developer writes a polymorphic loop:
```python
for user in user_accounts:
    user.display_profile()
```
and a new subclass (e.g., `Vendor` or `GuestUser`) is introduced that forgets to implement `display_profile()`, Python will attempt dynamic attribute lookup at runtime. Since the method is absent on that specific subclass and was never declared on the base class, Python will raise:
```
AttributeError: 'Vendor' object has no attribute 'display_profile'
```
In a running web backend or batch report, this uncaught exception causes an immediate crash mid-loop, leaving earlier records processed and subsequent records abandoned.

#### 3. Base Class Redesign to Guarantee Loop Safety
To prevent this failure permanently, we redesign `User` using Python's built-in `abc` (Abstract Base Class) module:
```python
from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    @abstractmethod
    def display_profile(self):
        """Must be implemented by all subclasses."""
        pass
```
By decorating `display_profile` with `@abstractmethod`, Python enforces an enforceable design contract at **instantiation time**. If any developer attempts to instantiate a subclass without overriding `display_profile`, Python immediately raises:
```
TypeError: Can't instantiate abstract class Vendor with abstract method display_profile
```
This shifts error discovery from unpredictable production runtime loops to development-time instantiation. Alternatively, if instantiating generic base users is permitted, `User.display_profile(self)` can provide a safe default fallback implementation (printing standard ID and name), guaranteeing that calling `user.display_profile()` can never trigger an `AttributeError`.

---

### Question 5 (Scenario S5): HTTP Status Codes & Resilient File Handling

#### 1. HTTP Status Code Meaning & Script Action
- **`200 OK`**: The request succeeded, and the payment transaction completed or was verified.  
  *Action*: Parse the response JSON body with `response.json()`, extract confirmation IDs, update order payment status to `'SUCCESS'`, and proceed to persist the record to disk.
- **`401 Unauthorized`**: Authentication credentials (API key, Bearer token, or secret signature) are missing, invalid, or expired.  
  *Action*: Stop immediate execution, log a critical security/configuration alert, avoid futile retries, and trigger an alert for operations to verify gateway credentials.
- **`429 Too Many Requests`**: The client has exceeded the gateway's rate limit quota within the current time window.  
  *Action*: Check for a `Retry-After` header in the HTTP response; pause execution using exponential backoff with random jitter, and retry the request gracefully instead of crashing.
- **`500 Internal Server Error`**: An unexpected server-side malfunction occurred on the payment gateway's infrastructure.  
  *Action*: Catch the error gracefully, refrain from writing unverified transaction state to local storage, log the incident with transaction context, and schedule the order for an asynchronous reconciliation queue.

#### 2. Prevention of File Corruption with `try-except-finally`
In the teammate's unhandled script, a direct write occurred without defensive exception handling. When the API crashed with a 500 status code mid-write, the write buffer was left partially written and unclosed, resulting in file corruption and data loss.

A `try-except-finally` block prevents this by isolating dangerous I/O operations:
```python
file_handle = None
try:
    response = call_payment_api(payload)
    if response.status_code == 200:
        data = response.json()
        file_handle = open("data/processed/orders.json", "w")
        json.dump(data, file_handle, indent=2)
    else:
        log_error(f"Payment failed with HTTP {response.status_code}")
except Exception as e:
    log_error(f"Encountered unexpected error during processing: {e}")
    # Rollback or clean up partial output if necessary
finally:
    if file_handle and not file_handle.closed:
        file_handle.flush()
        file_handle.close()
    print("Operation complete: resources safely released.")
```

#### 3. Why `finally` Guarantees Execution
The `finally` block provides an absolute guarantee under the Python runtime language specification: its block of code will **always** execute before exiting the `try` construct. Even if an unhandled exception occurs inside `try` or `except`, or if a `return`, `break`, or `continue` statement is encountered, the Python interpreter suspends stack unwinding, executes every statement inside `finally`, and only then resumes exception propagation or function return. This guarantees that file descriptors are flushed and closed, database transactions are rolled back, and network connections are released, permanently preventing file truncation and file lock leaks.

---

### Question 6 (Scenario S6): Customer Contact Cleaning with Python `re`

#### 1. Regex Pattern Structure Described in Words
To validate and extract standardized 10-digit phone numbers while accommodating optional international calling codes and varied formatting delimiters, the regular expression pattern is structured as follows:
1. **Word Boundary Anchor (`\b`)**: Prevents matching arbitrary substrings inside longer numeric IDs (like order tracking numbers or timestamps).
2. **Optional International Calling Code Group**: A leading literal plus sign (`\+`) followed by 1 to 3 digits (e.g., `91` for India or `1` for US), followed by optional whitespace or hyphen separator.
3. **Optional Trunk / Area Code Prefix**: An optional leading zero (`0`) or an optional opening parenthesis, 2 to 4 digits for an area code, and an optional closing parenthesis.
4. **Primary 10-Digit Subscriber Number**: Ten decimal digits, either as a continuous 10-digit block or divided into common groupings (such as 5 digits and 5 digits, or 3-3-4 digits), separated optionally by spaces, dots, or hyphens.
5. **Closing Word Boundary Anchor (`\b`)**: Ensures the number terminates cleanly without trailing alphanumeric characters.

#### 2. Why `re.findall()` is More Appropriate than `re.search()`
`re.search()` stops evaluating the input text immediately after finding the **very first** pattern match, returning a single `Match` object (or `None`). In contrast, raw customer contact files typically contain hundreds of records across multiline text strings. `re.findall()` (or `re.finditer()`) evaluates the entire input string from start to finish, extracting **every non-overlapping occurrence** that meets the regex criteria into a Python list in a single, high-performance C-optimized operation. Thus, `re.findall()` is necessary for bulk batch extraction across multi-record datasets.

#### 3. Real-World Formatting Edge Cases
- **Naive Pattern**: `r'\d{10}'` (matching any 10 consecutive digits).
- **Incorrectly Rejected Valid Input**: A valid customer phone entered with international notation or visual separators (e.g., `+91 98765-43210` or `(555) 234-5678`) will fail to match because the naive pattern does not accommodate plus signs, spaces, parentheses, or hyphens.
- **Incorrectly Accepted Invalid Input**: A 12-digit transaction ID or tracking code (e.g., `ORDER-987654321099`) contains 10 consecutive digits as an internal substring. The naive pattern will greedily match `9876543210` out of the order number, corrupting the customer contact database with a completely bogus phone number.
