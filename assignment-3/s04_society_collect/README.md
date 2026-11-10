# Session 4: Data Collection using Pandas (Part 1)

**Course Track:** Assignment Track 3: Data Science Foundations  
**Module:** Data Collection & Multi-Format Ingestion using Pandas  
**Case Study:** Greenwood Heights Housing Society Electricity Billing & Smart Meter System  
**Author:** Atharv Chaudhari (`ds-work`)

---

## 📋 Session Overview

In this session, we transition into data ingestion and structural diagnostics using **Pandas** (`pandas`). Working with the energy consumption records of a 100-flat residential community (**Greenwood Heights Housing Society**), we explore multi-format serialization, delimiter awareness, out-of-core memory streaming with `chunksize`, and early data quality audit techniques.

### 🎯 Key Learning Objectives
1. **Why Pandas is Essential for Data Science:** Seamless interoperability with tabular files, automated type inference, and built-in missing value handling.
2. **Multi-Format Serialization:** Exporting and importing datasets across CSV, Semicolon-separated values, Tab-separated values (TSV), Excel (`.xlsx`), and JSON (`records`).
3. **Delimiter & Separator Awareness:** Handling non-comma delimiters (`sep=';'`, `sep='\t'`) in legacy and enterprise exports.
4. **Out-of-Core Processing with `chunksize`:** Reading 60,000-row smart meter logs via chunked streaming iterators to compute aggregate totals in $O(1)$ memory.
5. **Early Issue Detection (Audit Protocol):** Inspecting schema metadata with `df.info()`, descriptive statistics with `df.describe(include='all')`, and generating automated issue reports (`society_issue_report.csv`).

---

## 🗂️ Files in this Directory

| File | Type | Description |
| :--- | :--- | :--- |
| [`society_collect.ipynb`](./society_collect.ipynb) | **Jupyter Notebook** | Full interactive workflow with pre-rendered results and Markdown documentation. |
| [`society_collect.py`](./society_collect.py) | **Python Script** | Zero-dependency standalone runner for batch headless execution. |
| [`README.md`](./README.md) | **Documentation** | Comprehensive session notes, findings, and usage instructions. |
| [`readings_comma.csv`](./readings_comma.csv) | **Data (CSV)** | Primary dataset saved with default comma separator (1,200 rows). |
| [`readings_semicolon.csv`](./readings_semicolon.csv) | **Data (CSV)** | Dataset saved with semicolon delimiter (`sep=';'`). |
| [`readings_tab.tsv`](./readings_tab.tsv) | **Data (TSV)** | Dataset saved with tab delimiter (`sep='\t'`). |
| [`readings.xlsx`](./readings.xlsx) | **Data (Excel)** | Microsoft Excel workbook generated via `openpyxl`. |
| [`readings.json`](./readings.json) | **Data (JSON)** | JSON record array export (`orient='records'`). |
| [`meter_big.csv`](./meter_big.csv) | **Data (Large CSV)**| 60,000 hourly smart meter readings for chunk streaming demonstration. |
| [`readings_messy.csv`](./readings_messy.csv) | **Data (Messy CSV)**| Dataset with 5% missing values, string currency contamination, and mixed casing. |
| [`society_issue_report.csv`](./society_issue_report.csv) | **Data (Audit CSV)** | Audit report quantifying data quality issues per column. |

---

## 🏢 Business Context: Greenwood Heights Housing Society

Greenwood Heights consists of **100 residential flats** divided into 4 blocks (**A, B, C, D** with flats 01 to 25 each). The society management committee tracks monthly power consumption across all 12 calendar months of 2025:

- **Total Flats:** 100 flats (`A-01` to `D-25`)
- **Billing Horizon:** 12 months (`2025-01` to `2025-12`)
- **Total Records:** $100 \text{ flats} \times 12 \text{ months} = 1,200 \text{ records}$
- **Tariff Rate:** ₹7.50 per kWh
- **Payment Collection Rate:** ~90% on-time settlement (`paid = 'Yes'`)

---

## 📝 Detailed Task Walkthrough & Technical Findings

### Task 2: Dataset Generation & Multi-Format Serialization
- Generated 1,200 monthly electricity records using `np.random.seed(42)`:
  - `flat_id`: Cartesian product of blocks `A-D` and flat numbers `01-25`.
  - `month`: Formatted strings `2025-01` through `2025-12`.
  - `units_kwh`: Random integers uniformly sampled from $[60, 420]$ kWh.
  - `amount_inr`: Evaluated as `units_kwh * 7.5`.
  - `paid`: Categorical variable with 90% `'Yes'` and 10% `'No'` probabilities.
- Exported with `index=False` across 5 file formats:
  1. `readings_comma.csv`
  2. `readings_semicolon.csv` (`sep=';'`)
  3. `readings_tab.tsv` (`sep='\t'`)
  4. `readings.xlsx` (Excel engine `openpyxl`)
  5. `readings.json` (`orient='records'`)

---

### Task 3: Multi-Format Ingestion & Integrity Verification
All 5 exported files were re-ingested into separate pandas DataFrames using their respective parsers:

| File Name | Ingested Shape | `units_kwh` Cumulative Sum | Data Parity Check |
| :--- | :---: | :---: | :---: |
| `readings_comma.csv` | `(1200, 5)` | 289,085 kWh | ✅ 100% Match |
| `readings_semicolon.csv` | `(1200, 5)` | 289,085 kWh | ✅ 100% Match |
| `readings_tab.tsv` | `(1200, 5)` | 289,085 kWh | ✅ 100% Match |
| `readings.xlsx` | `(1200, 5)` | 289,085 kWh | ✅ 100% Match |
| `readings.json` | `(1200, 5)` | 289,085 kWh | ✅ 100% Match |

**Final Verification:** All five files match identically in shape and total electricity consumption (`True`).

---

### Task 4: Chunked Ingestion for Large Files (`chunksize=10000`)
- **Generation:** Synthesized `meter_big.csv` containing **60,000 hourly smart meter readings** with power draws between 0.1 and 2.5 kWh.
- **Streaming Execution:** Streamed the dataset in discrete batches of 10,000 rows using `pd.read_csv('meter_big.csv', chunksize=10000)`.
- **Iterative Accumulation:**
  - Chunk 1: 10,000 rows | Subtotal: 13,096.05 kWh
  - Chunk 2: 10,000 rows | Subtotal: 13,108.24 kWh
  - Chunk 3: 10,000 rows | Subtotal: 13,053.41 kWh
  - Chunk 4: 10,000 rows | Subtotal: 12,946.77 kWh
  - Chunk 5: 10,000 rows | Subtotal: 13,043.24 kWh
  - Chunk 6: 10,000 rows | Subtotal: 12,968.36 kWh
- **Verification vs. Ground Truth:**
  - **Total Chunks:** `6` (exactly matching expected count).
  - **Total Rows:** `60,000` (identical to generator).
  - **Total Energy:** `78,216.07 kWh` vs Ground Truth `78,216.07 kWh` (difference is $0.000000$, well within the $\le 0.01$ tolerance).

---

### Task 1: Realistic Messy Dataset & Early Issue Detection
Deliberately introduced 3 prevalent data corruption patterns into `readings_messy.csv`:
1. **Null Values:** Blanked 5% of `units_kwh` (60 rows out of 1,200).
2. **String Contamination:** Formatted `amount_inr` with currency text like `'Rs 1234.50'`.
3. **Casing Inconsistency:** Mixed letter cases in `paid` (`'yes'`, `'YES'`, `'No'`, `'no'`, `'Yes'`).

#### Society Issue Report (`society_issue_report.csv`)
| Column | Inferred Dtype | Missing Count | Unique Count | Diagnostic Finding |
| :--- | :---: | :---: | :---: | :--- |
| `flat_id` | `str` / `object` | 0 | 100 | Clean categorical identifier. |
| `month` | `str` / `object` | 0 | 12 | Clean temporal sequence. |
| `units_kwh` | `float64` | **60** | 339 | **5.0% missing data**; auto-cast from int to float to accommodate `NaN`. |
| `amount_inr` | `str` / `object` | 0 | 344 | **Corrupted to string**; cannot compute financial aggregates without parsing. |
| `paid` | `str` / `object` | 0 | **5** | **Inconsistent casing**; prevents clean binary classification. |

> **Constraint Adhered:** Problems were quantified and isolated into `society_issue_report.csv` without modifying or fixing the underlying raw data.

---

## 🚀 How to Run

### Method 1: Interactive Jupyter Notebook
```bash
jupyter notebook society_collect.ipynb
```
Select **Kernel -> Restart & Run All** to re-render all data pipelines and chunked streams.

### Method 2: Headless Python Verification Script
```bash
python society_collect.py
```
Executes all four tasks, regenerates all file exports, and outputs the diagnostic issue report in your terminal.
