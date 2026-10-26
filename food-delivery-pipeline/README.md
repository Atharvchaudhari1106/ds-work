# Food Delivery Demand Analytics & Pipeline

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Assessment](https://img.shields.io/badge/Assessment-M2--A1-orange.svg)](#)
[![Module](https://img.shields.io/badge/Module-Python%20for%20Data%20Science-green.svg)](#)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](#)

A comprehensive data engineering and analytics pipeline built for the **TOPS Technologies Data Science Assessment (M2-A1: Python for Data Science)**. This project integrates automated data cleaning, functional transformation workflows, object-oriented domain modeling, resilient JSON persistence, and a live console pipeline consuming public REST APIs.

---

## Assessment Deliverables Index

| Section | Topic | Primary Deliverable File(s) |
| :--- | :--- | :--- |
| **Section A** | **Concept Application** | [`docs/SECTION_A_THEORY_ANSWERS.md`](docs/SECTION_A_THEORY_ANSWERS.md) (Detailed 6-8+ line answers for S1 to S6) |
| **Section B: Task 1** | **Git Repo Setup** | Repository structure, [`.gitignore`](.gitignore), [`docs/git_command_log.txt`](docs/git_command_log.txt) |
| **Section B: Task 2** | **Record Cleaning** | [`src/task2_cleaning.py`](src/task2_cleaning.py) (String methods, invalid/numeric skipping, running totals) |
| **Section B: Task 3** | **Functional Fee Calculator** | [`src/task3_fee_calculator.py`](src/task3_fee_calculator.py) (`map()`, `lambda`, `filter()`, `functools.reduce()`) |
| **Section B: Task 4** | **Record Manager with Persistence** | [`src/task4_record_manager.py`](src/task4_record_manager.py) (OOP `Order` class, JSON serialization, `try-except-finally`) |
| **Section C** | **Mini Capstone Live Pipeline** | [`src/pipeline_app.py`](src/pipeline_app.py), [`tests/test_pipeline.py`](tests/test_pipeline.py) (PR merged from `feature/live-pipeline`) |
| **Section D** | **AI-Augmented Learning** | [`docs/SECTION_D_AI_LEARNING.md`](docs/SECTION_D_AI_LEARNING.md), [`src/section_d_corrected.py`](src/section_d_corrected.py) |
| **Master Guide** | **Complete Assessment Guide** | [`docs/FULL_ASSESSMENT_SUBMISSION_GUIDE.md`](docs/FULL_ASSESSMENT_SUBMISSION_GUIDE.md) |

---

## Project Structure

```
food-delivery-pipeline/
├── .gitignore                    # Excludes venv, __pycache__, logs, and secrets
├── README.md                     # Project overview and submission index
├── data/
│   ├── raw/
│   │   ├── .gitkeep
│   │   └── orders_sample.txt     # Test file proving .gitignore allows tracked data files
│   └── processed/
│       ├── .gitkeep
│       └── records.json          # Formatted JSON output with indent=2
├── docs/
│   ├── git_command_log.txt       # Execution log of Task 1 Git commands & verification
│   ├── SECTION_A_THEORY_ANSWERS.md # Exhaustive answers for S1 to S6
│   ├── SECTION_D_AI_LEARNING.md    # AI prompt, comparison, and 3-4 line diagnostic note
│   └── FULL_ASSESSMENT_SUBMISSION_GUIDE.md # Master verification and grading guide
├── tests/
│   └── test_pipeline.py          # Unit tests for OOP serialization, commission tiers & roundtrips
└── src/
    ├── task2_cleaning.py         # Task 2: Data cleaning & validation script
    ├── task3_fee_calculator.py   # Task 3: Functional commission calculator
    ├── task4_record_manager.py   # Task 4: JSON persistent record manager
    ├── pipeline_app.py           # Section C: Interactive Live Data Pipeline Console App
    └── section_d_corrected.py    # Section D: Corrected AI-augmented pipeline script
```

---

## Quickstart & Execution Guide

### 1. Environment Setup
```bash
# Clone the repository
git clone <YOUR_GITHUB_REPO_URL>
cd food-delivery-pipeline

# Install required package
pip install requests
```

### 2. Run Individual Assessment Scripts
```bash
# Task 2: Record Cleaning
python src/task2_cleaning.py

# Task 3: Functional Fee Calculator
python src/task3_fee_calculator.py

# Task 4: Persistent Record Manager
python src/task4_record_manager.py

# Section C: Live Console Pipeline (Automated Demo Mode)
python src/pipeline_app.py --demo

# Section C: Live Console Pipeline (Interactive Menu Mode)
python src/pipeline_app.py

# Section D: AI-Augmented Corrected Script
python src/section_d_corrected.py
```

### 3. Run Unit Tests
```bash
python -m unittest discover -s tests
```

---

## Git Workflow & Repository History
This repository reflects professional Git best practices with a feature-branch workflow:
- Initialized on `main` branch with conventional commit messages.
- Created `feature/live-pipeline` branch for the Section C capstone application.
- Successfully merged into `main` with a non-fast-forward merge commit (`Merge pull request #1 from feature/live-pipeline into main`).
- Clean log history with **8+ commits**:
  ```
  * feat: add comprehensive documentation to repository
  * feat: add section d corrected ai pipeline and execution documentation
  * Merge pull request #1 from feature/live-pipeline into main
  |\  
  | * feat: implement console live data pipeline with API ingestion and persistence
  |/  
  * feat: add functional commission calculator with map filter reduce
  * feat: add data cleaning and string validation module
  * feat: add record manager with JSON persistence
  * docs: add README and .gitignore
  * feat: initialise project structure
  ```
