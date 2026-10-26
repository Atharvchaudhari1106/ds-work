# Complete Submission Guide: Data Science Assessment M2-A1

**Program**: Data Science (TOPS Technologies)  
**Assessment Code**: M2-A1  
**Assessment Title**: Python for Data Science  
**Technology Stack**: Python 3.14 / Git & Git Bash  
**GitHub Repository Link**: [https://github.com/Atharvchaudhari1106/food-delivery-pipeline](https://github.com/Atharvchaudhari1106/food-delivery-pipeline)  

---

## Workspace Deliverables Directory Tree

```
assessment/
├── SECTION_A_THEORY_ANSWERS.md       # Full structured prose answers for S1 to S6 (Markdown)
├── SECTION_A_THEORY_ANSWERS.txt      # Text submission version of Section A answers
├── task1_git_commands.txt            # Task 1 Git command log and .gitignore verification
├── task2_cleaning.py                 # Task 2 Record cleaning, string methods & running total
├── task3_fee_calculator.py           # Task 3 Functional tools (map, lambda, filter, reduce)
├── task4_record_manager.py           # Task 4 OOP Order persistence with try-except-finally
├── section_c_pipeline.py             # Section C Mini Capstone Live Data Pipeline console tool
├── SECTION_D_AI_LEARNING.md          # Section D AI prompt, code comparison & 3-4 line diagnostic note
├── section_d_corrected.py            # Section D production-ready corrected Python script
├── FULL_ASSESSMENT_SUBMISSION_GUIDE.md # This comprehensive grading and submission index
└── food-delivery-pipeline/           # Integrative Professional Git Repository (Tasks 1, 4, & Section C)
    ├── .git/                         # 8 commits on main, feature branch merged via PR
    ├── .gitignore                    # Configured exclusions (venv, __pycache__, *.log, secrets)
    ├── README.md                     # Portfolio-ready documentation
    ├── notes.log                     # Verification test file (IGNORED by Git)
    ├── data/
    │   ├── raw/
    │   │   ├── .gitkeep
    │   │   └── orders_sample.txt     # Verification test file (TRACKED by Git)
    │   └── processed/
    │       ├── .gitkeep
    │       └── records.json          # Persisted JSON orders with indent=2
    ├── docs/
    │   ├── .gitkeep
    │   └── git_command_log.txt       # Version control log for repository setup
    ├── tests/
    │   ├── .gitkeep
    │   └── test_pipeline.py          # Unit test suite verifying Order class, tiers, & roundtrips
    └── src/
        ├── .gitkeep
        ├── task2_cleaning.py
        ├── task3_fee_calculator.py
        ├── task4_record_manager.py
        ├── pipeline_app.py           # Interactive & automated menu-driven capstone pipeline
        └── section_d_corrected.py
```

---

## Section-by-Section Summary & Verification

### Section A: Concept Application
- **File**: `SECTION_A_THEORY_ANSWERS.md` (and plain text: `SECTION_A_THEORY_ANSWERS.txt`)
- **Coverage**:
  - **S1**: Comprehensive walkthrough of all 6 Data Science Lifecycle stages (Problem Definition, Data Collection, Data Preparation, Exploration, Modelling, Evaluation) with concrete deliverables. Evaluates Generative AI acceleration in Data Preparation and EDA with specific unreviewed risks (data leakage and hallucinated causal inferences).
  - **S2**: Git feature-branch strategy with branch protection on `main`. Exact command sequences from branch creation to PR review and merge. Realistic `src/config.py` merge conflict scenario and step-by-step resolution.
  - **S3**: Named commission function applied via `map()` and a `lambda`. Justification of `map()`'s declarative immutability and iterator efficiency over a second `for` loop. Role of `filter()` for audit isolation and `functools.reduce()` for single-expression total accumulation.
  - **S4**: OOP account hierarchy (`User`, `Customer`, `DeliveryPartner`, `Admin`) with method overriding. Diagnostic explanation of runtime `AttributeError` when iterating over un-overridden subclasses. Redesign using `abc.ABC` and `@abstractmethod` to enforce compile/instantiation-time contracts.
  - **S5**: Comprehensive explanation of HTTP codes `200`, `401`, `429`, and `500` with required script behaviors. Detailed analysis of `try-except-finally` preventing file corruption and the runtime execution guarantee of `finally`.
  - **S6**: Customer contact cleaning with Python `re`. Verbal description of regex pattern structure. Comparative justification for `re.findall()` over `re.search()` for batch text. Real-world formatting edge case analysis (international prefixes and numeric serial collision).

---

### Section B: Practical Tasks

#### Task 1: Food Delivery Project Repository Setup
- **Directory**: `food-delivery-pipeline/`
- **Verification**:
  - Initialized Git repository on `main` branch.
  - Structure created with `.gitkeep` placeholders: `src/`, `data/raw/`, `data/processed/`, `docs/`, `tests/`.
  - Staged and committed: `'feat: initialise project structure'`.
  - Configured `.gitignore` excluding `venv/`, `.env`, `__pycache__/`, `*.pyc`, `*.log`, `config.ini`, `secrets.json`.
  - Professional `README.md` created and committed: `'docs: add README and .gitignore'`.
  - Test files created: `notes.log` and `data/raw/orders_sample.txt`.
  - **Proof of `.gitignore` Functionality**:
    ```bash
    git status
    # Output confirms:
    # notes.log does NOT appear in untracked files (ignored by *.log rule)
    # data/raw/orders_sample.txt DOES appear under Untracked files
    ```
- **Log File**: `task1_git_commands.txt` & `food-delivery-pipeline/docs/git_command_log.txt`.

#### Task 2: Food Delivery Record Cleaning Script
- **Source File**: `task2_cleaning.py` (and `food-delivery-pipeline/src/task2_cleaning.py`)
- **Execution Command**: `python task2_cleaning.py`
- **Output Metrics**:
  - Total Input Records Evaluated: `10`
  - Total Valid Records Cleaned: `6`
  - Total Invalid Records Skipped: `4` (empty string, whitespace-only, and numeric inputs)
  - Final Cumulative Running Total: `Rs. 1,927.00`

#### Task 3: Food Delivery Fee Calculator with Functional Tools
- **Source File**: `task3_fee_calculator.py` (and `food-delivery-pipeline/src/task3_fee_calculator.py`)
- **Execution Command**: `python task3_fee_calculator.py`
- **Output Metrics**:
  - Tiered commission function: Tier 1 (<= Rs.200: 10%), Tier 2 (Rs.201-500: 15%), Tier 3 (> Rs.500: 20%).
  - Evaluated 7 restaurant dictionaries via `map()` with a `lambda`.
  - Filtered audit-flagged records exceeding Rs. 45.00 threshold via `filter()`: 4 flagged records.
  - Cumulative Grand Total Fee via `functools.reduce()` in a single expression: `Rs. 474.10`.

#### Task 4: Food Delivery Record Manager with Persistence
- **Source File**: `task4_record_manager.py` (and `food-delivery-pipeline/src/task4_record_manager.py`)
- **Execution Command**: `python src/task4_record_manager.py` (from `food-delivery-pipeline`)
- **Capabilities Verified**:
  - `Order` class with attributes (`order_id`, `restaurant_name`, `amount`, `delivery_time_minutes`, `is_delivered`).
  - `to_dict()` and `from_dict()` serialization/deserialization.
  - `save_records()` with `json.dump()` inside `with open()`.
  - `load_records()` with defensive `try-except-finally` catching `FileNotFoundError` (returns `[]` gracefully) and printing `'Operation complete'`.
  - Committed with message: `'feat: add record manager with JSON persistence'`.

---

### Section C: Mini Capstone Project (Live Data Pipeline Console Tool)
- **Source File**: `food-delivery-pipeline/src/pipeline_app.py` (and root `section_c_pipeline.py`)
- **Execution Commands**:
  - Interactive Mode: `python src/pipeline_app.py`
  - Automated Testing Mode: `python src/pipeline_app.py --demo`
  - Unit Test Suite: `python -m unittest discover -s tests` (3/3 tests passing)
- **Git History & PR Verification**:
  - Created and worked on feature branch: `feature/live-pipeline`.
  - Merged feature branch into `main` using non-fast-forward merge commit (`Merge pull request #1 from feature/live-pipeline into main`).
  - Total 8 meaningful commits on `main` branch.
- **Console App Capabilities**:
  1. REST API Ingestion from `https://jsonplaceholder.typicode.com/posts?_limit=10` with strict HTTP status code checking before `.json()`.
  2. Interactive new restaurant creation with re-prompting validation loops on non-numeric input.
  3. Tiered commission computation and audit reporting via `map()` and `filter()`.
  4. Complete file persistence cycle to `data/processed/records.json` and reloading with verification.

---

### Section D: AI-Augmented Learning
- **Documentation**: `SECTION_D_AI_LEARNING.md`
- **Production Script**: `section_d_corrected.py` (and `food-delivery-pipeline/src/section_d_corrected.py`)
- **Deliverables**:
  1. Exact prompt provided to AI tool.
  2. Side-by-side comparison of AI's flawed code vs. corrected production code.
  3. Concise 3–4 line diagnostic note identifying:
     - Premature `.json()` call before validating `status_code == 200`
     - Truncated integer division (`//`) discarding fractional currency paise
     - Missing parent directory creation triggering `FileNotFoundError`
     - Missing `indent=2` argument in `json.dump()`
