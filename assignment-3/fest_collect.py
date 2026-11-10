"""
================================================================================
SESSION 5: Data Collection using Pandas (Part 2)
Assignment Track 3: Data Science Foundations
Fictional Scenario: Annual College Cultural & Tech Festival (Vivanta Fest 2025)
Author: Atharv Chaudhari (ds-work)
================================================================================
"""

import json
import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd


def main():
    print("=" * 80)
    print("SESSION 5: Data Collection using Pandas (Part 2)")
    print("Vivanta Fest 2025 Festival Management Engine")
    print(f"Pandas Version: {pd.__version__} | NumPy Version: {np.__version__}")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # TASK 1: SQLite Database Setup & SQL Query Ingestion
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 1: SQLite Database Setup & SQL Query Ingestion")
    print("=" * 80)

    np.random.seed(42)

    student_ids = [f"S{i:03d}" for i in range(1, 401)]
    reg_ids = [f"R{i:03d}" for i in range(1, 401)]
    events_pool = ['Dance', 'Coding', 'Quiz', 'Gaming', 'Music']
    colleges_pool = [
        'St. Xavier Institute',
        'National Tech College',
        'Metro Arts Academy',
        'Apex Engineering College',
        'City Commerce College',
        'Global Science University'
    ]
    ticket_tiers = list(range(0, 501, 50))

    df_registrations = pd.DataFrame({
        'reg_id': reg_ids,
        'student_id': student_ids,
        'event': np.random.choice(events_pool, size=400),
        'college': np.random.choice(colleges_pool, size=400),
        'ticket_inr': np.random.choice(ticket_tiers, size=400),
        'paid': np.random.choice(['Yes', 'No'], size=400, p=[0.75, 0.25])
    })

    print(f"Generated Registrations: {df_registrations.shape[0]} rows x {df_registrations.shape[1]} cols")

    conn = sqlite3.connect('fest.db')
    df_registrations.to_sql('registrations', conn, if_exists='replace', index=False)

    sql_query = "SELECT * FROM registrations WHERE paid = 'Yes'"
    df_paid_query = pd.read_sql_query(sql_query, conn)
    df_paid_sql = pd.read_sql(sql_query, conn)

    print(f"pd.read_sql_query shape : {df_paid_query.shape} (Rows: {df_paid_query.shape[0]}, Cols: {df_paid_query.shape[1]})")
    print(f"pd.read_sql shape       : {df_paid_sql.shape} (Rows: {df_paid_sql.shape[0]}, Cols: {df_paid_sql.shape[1]})")
    print(f"Shapes Match Exactly    : {df_paid_query.shape == df_paid_sql.shape}")
    conn.close()

    # -------------------------------------------------------------------------
    # TASK 2: Nested API-Style JSON & pd.json_normalize
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 2: Nested API-Style JSON & pd.json_normalize")
    print("=" * 80)

    sponsors_payload = {
        "status": "ok",
        "data": [
            {"sponsor": "RedBull Gaming", "amount_inr": 150000, "contact": {"city": "Mumbai", "tier": "Platinum"}},
            {"sponsor": "TechGig Hackathon", "amount_inr": 120000, "contact": {"city": "Bengaluru", "tier": "Platinum"}},
            {"sponsor": "Spotify India", "amount_inr": 100000, "contact": {"city": "Mumbai", "tier": "Gold"}},
            {"sponsor": "Domino's Pizza", "amount_inr": 80000, "contact": {"city": "Delhi", "tier": "Gold"}},
            {"sponsor": "Zepto Quick", "amount_inr": 75000, "contact": {"city": "Pune", "tier": "Gold"}},
            {"sponsor": "Boat Lifestyle", "amount_inr": 60000, "contact": {"city": "Delhi", "tier": "Silver"}},
            {"sponsor": "Unstop Campus", "amount_inr": 50000, "contact": {"city": "Bengaluru", "tier": "Silver"}},
            {"sponsor": "Nestle Nescafe", "amount_inr": 45000, "contact": {"city": "Kolkata", "tier": "Silver"}},
            {"sponsor": "Logitech G", "amount_inr": 40000, "contact": {"city": "Hyderabad", "tier": "Bronze"}},
            {"sponsor": "CodeChef Live", "amount_inr": 35000, "contact": {"city": "Chennai", "tier": "Bronze"}},
            {"sponsor": "Decathlon Sports", "amount_inr": 30000, "contact": {"city": "Ahmedabad", "tier": "Bronze"}},
            {"sponsor": "Keventers Shakes", "amount_inr": 25000, "contact": {"city": "Jaipur", "tier": "Bronze"}},
            {"sponsor": "Skillshare Learn", "amount_inr": 20000, "contact": {"city": "Noida", "tier": "Supporter"}},
            {"sponsor": "Subway Fresh", "amount_inr": 15000, "contact": {"city": "Gurugram", "tier": "Supporter"}},
            {"sponsor": "Duolingo Club", "amount_inr": 10000, "contact": {"city": "Chandigarh", "tier": "Supporter"}}
        ]
    }

    with open('sponsors_api.json', 'w', encoding='utf-8') as f:
        json.dump(sponsors_payload, f, indent=2)

    with open('sponsors_api.json', 'r', encoding='utf-8') as f:
        api_data = json.load(f)

    sponsors = pd.json_normalize(api_data['data'])
    print("Flattened sponsors DataFrame Columns:")
    print(sponsors.columns.tolist())
    assert 'contact.city' in sponsors.columns, "contact.city missing!"
    assert 'contact.tier' in sponsors.columns, "contact.tier missing!"
    print("\nFirst 5 Records:")
    print(sponsors.head())

    # -------------------------------------------------------------------------
    # TASK 3: Event Catalog & Web-Based URL Ingestion
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 3: Event Catalog & Web-Based URL Ingestion")
    print("=" * 80)

    events_master_data = {
        'event': ['Dance', 'Coding', 'Quiz', 'Gaming', 'Music'],
        'venue': ['Main Auditorium', 'Computer Lab 3', 'Seminar Hall B', 'E-Sports Arena', 'Open Air Amphitheatre'],
        'day': [1, 2, 1, 3, 2],
        'budget_inr': [80000, 60000, 30000, 95000, 110000]
    }
    events_df = pd.DataFrame(events_master_data)
    events_df.to_csv('fest_events.csv', index=False)

    raw_url = "https://raw.githubusercontent.com/Atharvchaudhari1106/ds-work/main/assignment-3/s05_fest_collect/fest_events.csv"
    try:
        events = pd.read_csv(raw_url)
        print(f"Loaded from GitHub Raw URL: {raw_url}")
    except Exception as e:
        print(f"Loaded local fest_events.csv ({e})")
        events = pd.read_csv('fest_events.csv')

    print(f"events.shape: {events.shape} (5 events x 4 columns)")
    print(events)

    # -------------------------------------------------------------------------
    # TASK 4: Pathlib Handling, Batch Globbing, Concat & Merge
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("TASK 4: Pathlib Handling, Batch Globbing, Concat & Merge")
    print("=" * 80)

    data_dir = Path('fest_data')
    data_dir.mkdir(exist_ok=True)

    day1_df = df_registrations.iloc[:130]
    day2_df = df_registrations.iloc[130:270]
    day3_df = df_registrations.iloc[270:400]

    day1_df.to_csv(data_dir / 'day1.csv', index=False)
    day2_df.to_csv(data_dir / 'day2.csv', index=False)
    day3_df.to_csv(data_dir / 'day3.csv', index=False)

    csv_files = sorted(Path('fest_data').glob('day*.csv'))
    print(f"Discovered {len(csv_files)} files: {[f.name for f in csv_files]}")

    recombined = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
    print(f"Recombined registrations shape: {recombined.shape}")

    fest_master = pd.merge(recombined, events, on='event', how='left', validate='m:1')
    fest_master.to_csv('fest_master.csv', index=False)

    print(f"fest_master.csv Shape: {fest_master.shape} (400 rows x 9 columns)")
    print(fest_master.head())

    assert len(fest_master) == 400, "Master dataset must have 400 rows!"
    missing_venues = fest_master['venue'].isna().sum()
    assert missing_venues == 0, "No missing venues allowed!"
    print(f"\nAll Assertions Verified: Exactly 400 rows and 0 missing venues -> True")
    print("=" * 80)


if __name__ == "__main__":
    main()
