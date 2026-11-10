"""
================================================================================
SESSION 4: Data Collection using Pandas (Part 1)
Assignment Track 3: Data Science Foundations
Fictional Scenario: Greenwood Heights Housing Society Electricity Data System
Author: Atharv Chaudhari (ds-work)
================================================================================
"""

import os
import numpy as np
import pandas as pd


def main():
    print("=" * 80)
    print("SESSION 4: Data Collection using Pandas (Part 1)")
    print("Greenwood Heights Housing Society Electricity Billing System")
    print(f"Pandas Version: {pd.__version__} | NumPy Version: {np.__version__}")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # TASK 2: Electricity Readings Generation & Multi-Format Export
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 2: Dataset Generation & Multi-Format Serialization")
    print("=" * 80)

    np.random.seed(42)

    blocks = ['A', 'B', 'C', 'D']
    flats = [f"{b}-{i:02d}" for b in blocks for i in range(1, 26)]
    months = [f"2025-{m:02d}" for m in range(1, 13)]

    records = [{'flat_id': f, 'month': m} for m in months for f in flats]
    df_readings = pd.DataFrame(records)

    df_readings['units_kwh'] = np.random.randint(60, 421, size=len(df_readings))
    df_readings['amount_inr'] = df_readings['units_kwh'] * 7.5
    df_readings['paid'] = np.random.choice(['Yes', 'No'], size=len(df_readings), p=[0.9, 0.1])

    print(f"Generated Dataset: {df_readings.shape[0]} rows x {df_readings.shape[1]} columns")
    print("\nFirst 5 Records:")
    print(df_readings.head())

    # Export to 5 formats
    df_readings.to_csv('readings_comma.csv', index=False)
    df_readings.to_csv('readings_semicolon.csv', sep=';', index=False)
    df_readings.to_csv('readings_tab.tsv', sep='\t', index=False)
    df_readings.to_excel('readings.xlsx', index=False)
    df_readings.to_json('readings.json', orient='records', indent=2)

    print("\nExported to 5 files:")
    print("  1. readings_comma.csv")
    print("  2. readings_semicolon.csv (sep=';')")
    print("  3. readings_tab.tsv (sep='\\t')")
    print("  4. readings.xlsx")
    print("  5. readings.json (orient='records')")

    # -------------------------------------------------------------------------
    # TASK 3: Ingestion & Integrity Verification
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 3: Multi-Format Ingestion & Integrity Verification")
    print("=" * 80)

    df_csv = pd.read_csv('readings_comma.csv')
    df_semi = pd.read_csv('readings_semicolon.csv', sep=';')
    df_tsv = pd.read_csv('readings_tab.tsv', sep='\t')
    df_excel = pd.read_excel('readings.xlsx')
    df_json = pd.read_json('readings.json')

    files = [
        ('readings_comma.csv', df_csv),
        ('readings_semicolon.csv', df_semi),
        ('readings_tab.tsv', df_tsv),
        ('readings.xlsx', df_excel),
        ('readings.json', df_json)
    ]

    print("=" * 65)
    print(f"{'File Name':<25} | {'Shape':<12} | {'units_kwh Sum':<18}")
    print("=" * 65)

    sums = []
    shapes = []
    for fname, df_i in files:
        s = df_i['units_kwh'].sum()
        sums.append(s)
        shapes.append(df_i.shape)
        print(f"{fname:<25} | {str(df_i.shape):<12} | {s:<18,}")
    print("=" * 65)

    all_match = (len(set(shapes)) == 1) and (len(set(sums)) == 1)
    print(f"\nFinal Verification: All five files match identically in shape and units_kwh sum: {all_match}")

    # -------------------------------------------------------------------------
    # TASK 4: Chunked Ingestion for Large Data Files (chunksize)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 4: Chunked Ingestion for Large Data Files (chunksize=10000)")
    print("=" * 80)

    np.random.seed(42)
    df_meter_big = pd.DataFrame({
        'flat_id': np.random.choice(flats, size=60000),
        'hour_no': np.tile(np.arange(1, 25), 2500),
        'kwh': np.round(np.random.uniform(0.1, 2.5, size=60000), 2)
    })
    df_meter_big.to_csv('meter_big.csv', index=False)

    gt_rows = len(df_meter_big)
    gt_kwh = df_meter_big['kwh'].sum()
    print(f"Generated meter_big.csv: {gt_rows:,} rows | Ground Truth Total kWh: {gt_kwh:,.2f}")

    chunk_counter = 0
    total_chunk_rows = 0
    total_chunk_kwh = 0.0

    for chunk in pd.read_csv('meter_big.csv', chunksize=10000):
        chunk_counter += 1
        total_chunk_rows += len(chunk)
        total_chunk_kwh += chunk['kwh'].sum()
        print(f"  Chunk {chunk_counter}: Processed {len(chunk):,} rows | Subtotal kWh: {chunk['kwh'].sum():,.2f}")

    print("\n--- Chunk Processing Results vs Ground Truth ---")
    print(f"Total Chunks Processed : {chunk_counter} (Expected: 6)")
    print(f"Total Rows Processed   : {total_chunk_rows:,} (Ground Truth: {gt_rows:,})")
    print(f"Total kWh Accumulated  : {total_chunk_kwh:,.2f} (Ground Truth: {gt_kwh:,.2f})")

    kwh_diff = abs(total_chunk_kwh - gt_kwh)
    assert chunk_counter == 6, "Chunk count must be 6!"
    assert total_chunk_rows == gt_rows, "Total rows must match ground truth!"
    assert kwh_diff <= 0.01, f"Difference {kwh_diff} exceeds 0.01 tolerance!"
    print(f"Verification: Totals match generating DataFrame within 0.01 (diff = {kwh_diff:.6f}) -> True")

    # -------------------------------------------------------------------------
    # TASK 1: Messy Dataset Creation & Early Issue Detection
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 1: Messy Dataset Creation & Early Issue Detection")
    print("=" * 80)

    np.random.seed(42)
    df_messy = df_readings.copy()

    # 1. Blank 5% of units_kwh
    n_blank = int(len(df_messy) * 0.05)
    blank_idx = np.random.choice(df_messy.index, size=n_blank, replace=False)
    df_messy.loc[blank_idx, 'units_kwh'] = np.nan

    # 2. Turn amount_inr into text like 'Rs 1234.50'
    df_messy['amount_inr'] = df_messy['amount_inr'].apply(lambda x: f"Rs {x:.2f}")

    # 3. Mix the case of paid
    cases = ['yes', 'YES', 'No', 'no', 'Yes']
    df_messy['paid'] = np.random.choice(cases, size=len(df_messy), p=[0.35, 0.35, 0.1, 0.1, 0.1])

    # Save messy dataset
    df_messy.to_csv('readings_messy.csv', index=False)
    print("Saved readings_messy.csv.")

    # Ingest and inspect
    df_loaded_messy = pd.read_csv('readings_messy.csv')
    print("\n=== df.info() Diagnostic ===")
    df_loaded_messy.info()

    print("\n=== df.describe(include='all') ===")
    print(df_loaded_messy.describe(include='all'))

    # Build issue_report
    report_rows = []
    for col in df_loaded_messy.columns:
        report_rows.append({
            'column': col,
            'dtype': str(df_loaded_messy[col].dtype),
            'missing_count': int(df_loaded_messy[col].isna().sum()),
            'unique_count': int(df_loaded_messy[col].nunique())
        })

    issue_report = pd.DataFrame(report_rows)
    issue_report.to_csv('society_issue_report.csv', index=False)

    print("\n=== Society Issue Report (society_issue_report.csv) ===")
    print(issue_report.to_string(index=False))
    print("=" * 80)


if __name__ == "__main__":
    main()
