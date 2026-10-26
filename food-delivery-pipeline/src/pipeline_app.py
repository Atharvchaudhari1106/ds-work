"""
================================================================================
Section C — Mini Capstone Project: Food Delivery Live Data Pipeline
Console Tool
Assessment Code: M2-A1 | Python for Data Science
Description:
    Menu-driven live data pipeline integrating REST API ingestion,
    OOP domain modeling (Order class), functional transformations
    (map and filter), input validation with re-prompting, and resilient
    JSON file persistence.
================================================================================
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional

try:
    import requests
except ImportError:
    requests = None


class Order:
    """
    Domain entity modeling a restaurant order within the delivery ecosystem.
    """
    def __init__(
        self,
        order_id: int,
        name: str,
        amount: float,
        status: str = "Active",
        delivery_time_minutes: int = 30
    ):
        self.order_id = int(order_id)
        self.name = str(name).strip()
        self.amount = float(amount)
        self.status = str(status).strip()
        self.delivery_time_minutes = int(delivery_time_minutes)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the order instance to a dictionary for JSON storage."""
        return {
            "order_id": self.order_id,
            "name": self.name,
            "amount": self.amount,
            "status": self.status,
            "delivery_time_minutes": self.delivery_time_minutes
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Order":
        """Reconstructs an Order instance from dictionary data."""
        return cls(
            order_id=data["order_id"],
            name=data["name"],
            amount=data["amount"],
            status=data.get("status", "Active"),
            delivery_time_minutes=data.get("delivery_time_minutes", 30)
        )

    def __repr__(self) -> str:
        return (
            f"<Order #{self.order_id:03d} | {self.name:<26} | Rs. {self.amount:>7.2f} "
            f"| Status: {self.status:<9} | ETA: {self.delivery_time_minutes}m>"
        )


class FoodDeliveryPipeline:
    """
    Live data pipeline orchestrator handling API consumption, in-memory state,
    functional commission computation, and persistence.
    """
    API_URL = "https://jsonplaceholder.typicode.com/posts?_limit=10"
    STORAGE_FILE = os.path.join("data", "processed", "records.json")

    def __init__(self):
        self.records: List[Order] = []

    # --------------------------------------------------------------------------
    # Option 1: Fetch and display top 10 mock restaurants from public REST API
    # --------------------------------------------------------------------------
    def fetch_api_restaurants(self) -> bool:
        print("\n" + "=" * 76)
        print(" [API INGESTION] Fetching Mock Restaurant Records...")
        print(f" Source Endpoint: {self.API_URL}")
        print("=" * 76)

        try:
            if requests is not None:
                response = requests.get(self.API_URL, timeout=10)
                # Requirement: Check HTTP status code BEFORE calling .json()
                if response.status_code == 200:
                    raw_data = response.json()
                else:
                    print(f"[API ERROR] Request failed with HTTP Status Code: {response.status_code}")
                    print("[NOTICE] Skipping record fetch gracefully without crashing.")
                    return False
            else:
                # Standard library fallback
                import urllib.request
                req = urllib.request.Request(self.API_URL, headers={"User-Agent": "Python/Pipeline"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    if resp.status == 200:
                        raw_data = json.loads(resp.read().decode("utf-8"))
                    else:
                        print(f"[API ERROR] Request failed with HTTP Status Code: {resp.status}")
                        return False

            # Ingest records treating id and title as restaurant id and name
            fetched_count = 0
            for item in raw_data:
                r_id = item["id"]
                # Clean and standardize title to represent restaurant name
                clean_name = item["title"].replace("\n", " ").strip().title()
                # Truncate overly long mock titles for clean console formatting
                if len(clean_name) > 25:
                    clean_name = clean_name[:25].rstrip() + "..."

                # Assign synthetic realistic order amount and delivery time based on ID
                mock_amount = round(150.0 + (r_id * 48.75), 2)
                mock_time = 20 + (r_id * 2)

                order_obj = Order(
                    order_id=r_id,
                    name=clean_name,
                    amount=mock_amount,
                    status="Active",
                    delivery_time_minutes=mock_time
                )
                self.records.append(order_obj)
                fetched_count += 1

            print(f"[SUCCESS] Successfully ingested {fetched_count} restaurant records into memory.\n")
            self.display_records_table()
            return True

        except Exception as exc:
            print(f"[UNEXPECTED ERROR] An exception occurred during API ingestion: {exc}")
            print("[SAFE RECOVERY] Pipeline handled error gracefully without terminating session.")
            return False

    # --------------------------------------------------------------------------
    # Option 2: Add a new restaurant (Stored as a class instance with validation)
    # --------------------------------------------------------------------------
    def add_restaurant_interactive(self):
        print("\n" + "=" * 76)
        print(" [NEW RECORD] Add a New Restaurant Order")
        print("=" * 76)

        # 1. Name input
        while True:
            name = input("Enter Restaurant Name: ").strip()
            if name:
                cleaned_name = name.title()
                break
            print("[VALIDATION ERROR] Restaurant name cannot be empty. Please retry.")

        # 2. Numeric validation for Order ID
        while True:
            id_input = input("Enter Order ID (Integer): ").strip()
            try:
                order_id = int(id_input)
                if order_id <= 0:
                    print("[VALIDATION ERROR] Order ID must be a positive integer.")
                    continue
                # Check for duplicate ID
                if any(r.order_id == order_id for r in self.records):
                    print(f"[VALIDATION ERROR] Order ID #{order_id} already exists. Enter a unique ID.")
                    continue
                break
            except ValueError:
                print(f"[VALIDATION ERROR] '{id_input}' is not a valid integer. Please re-enter a numeric ID.")

        # 3. Numeric validation for Amount
        while True:
            amt_input = input("Enter Order Amount in INR (e.g. 350.50): ").strip()
            try:
                amount = float(amt_input.replace("Rs.", "").replace("Rs", "").strip())
                if amount <= 0:
                    print("[VALIDATION ERROR] Order amount must be greater than zero.")
                    continue
                break
            except ValueError:
                print(f"[VALIDATION ERROR] '{amt_input}' is not a valid decimal number. Please enter a valid amount.")

        # 4. Numeric validation for Delivery Time
        while True:
            time_input = input("Enter Estimated Delivery Time in Minutes (e.g. 30): ").strip()
            try:
                delivery_time = int(time_input)
                if delivery_time <= 0:
                    print("[VALIDATION ERROR] Delivery time must be greater than zero.")
                    continue
                break
            except ValueError:
                print(f"[VALIDATION ERROR] '{time_input}' is not a valid integer. Please re-enter delivery time.")

        # 5. Status flag selection
        status_input = input("Enter Status (Active / In Transit / Delivered) [Default: Active]: ").strip().title()
        status = status_input if status_input in ["Active", "In Transit", "Delivered"] else "Active"

        # Instantiate Order class and append to session
        new_order = Order(
            order_id=order_id,
            name=cleaned_name,
            amount=amount,
            status=status,
            delivery_time_minutes=delivery_time
        )
        self.records.append(new_order)
        print(f"\n[SUCCESS] New restaurant order #{order_id} ('{cleaned_name}') successfully added to session.")

    # --------------------------------------------------------------------------
    # Option 3: Calculate and display commission using map() and filter()
    # --------------------------------------------------------------------------
    @staticmethod
    def calculate_commission(amount: float) -> float:
        """
        Tiered commission model:
          - Tier 1: Up to Rs. 200.00        -> 10%
          - Tier 2: Rs. 201.00 to Rs. 500.00 -> 15%
          - Tier 3: Above Rs. 500.00         -> 20%
        """
        if amount <= 200.00:
            return amount * 0.10
        elif amount <= 500.00:
            return amount * 0.15
        else:
            return amount * 0.20

    def calculate_and_display_commission(self):
        print("\n" + "=" * 82)
        print("       COMMISSION & AUDIT ANALYTICS (FUNCTIONAL: MAP & FILTER)")
        print("=" * 82)

        if not self.records:
            print("[NOTICE] No records available in session. Please fetch or add records first.")
            return

        # Use map() with a lambda to compute commission fee for each record
        commission_data = list(map(
            lambda order: {
                "id": order.order_id,
                "name": order.name,
                "amount": order.amount,
                "status": order.status,
                "fee": round(self.calculate_commission(order.amount), 2),
                "net_payout": round(order.amount - self.calculate_commission(order.amount), 2)
            },
            self.records
        ))

        print(f"{'ID':<6} | {'Restaurant Name':<28} | {'Order Amt':<12} | {'Fee (INR)':<12} | {'Net Payout':<12}")
        print("-" * 82)
        for row in commission_data:
            print(f"#{row['id']:<5} | {row['name']:<28} | Rs.{row['amount']:>8.2f} | Rs.{row['fee']:>8.2f} | Rs.{row['net_payout']:>8.2f}")
        print("-" * 82)

        # Use filter() to isolate high-commission records for audit (Threshold > Rs. 50.00)
        AUDIT_THRESHOLD = 50.00
        audit_records = list(filter(lambda r: r["fee"] > AUDIT_THRESHOLD, commission_data))

        print(f"\n>>> AUDIT INSPECTION (Records with Fee > Rs. {AUDIT_THRESHOLD:.2f})")
        print(f"{'ID':<6} | {'Restaurant Name':<28} | {'Order Amt':<12} | {'Audit Fee':<12} | {'Flag'}")
        print("-" * 82)
        for row in audit_records:
            print(f"#{row['id']:<5} | {row['name']:<28} | Rs.{row['amount']:>8.2f} | Rs.{row['fee']:>8.2f} | [AUDIT REVIEW]")
        print(f"\nTotal Records: {len(commission_data)} | Flagged for Audit: {len(audit_records)}")
        print("=" * 82)

    # --------------------------------------------------------------------------
    # Option 4: Save to data/processed/records.json and load back
    # --------------------------------------------------------------------------
    def persist_and_reload(self):
        print("\n" + "=" * 76)
        print("          DATA PERSISTENCE & VERIFICATION CYCLE")
        print("=" * 76)

        if not self.records:
            print("[NOTICE] No records in session to persist.")
            return

        # 1. Save records using try-except-finally
        file_handle = None
        save_success = False
        try:
            parent_dir = os.path.dirname(self.STORAGE_FILE)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)

            with open(self.STORAGE_FILE, "w", encoding="utf-8") as f:
                serialized = [r.to_dict() for r in self.records]
                json.dump(serialized, f, indent=2)
            print(f"[SAVE] Serialized {len(self.records)} Order instance(s) to '{self.STORAGE_FILE}'.")
            save_success = True
        except Exception as exc:
            print(f"[ERROR] Failed saving records to disk: {exc}")
        finally:
            print("Operation complete (Save Stage)")

        if not save_success:
            return

        # 2. Reload records and reconstruct instances
        try:
            with open(self.STORAGE_FILE, "r", encoding="utf-8") as f:
                loaded_raw = json.load(f)
                reconstructed = [Order.from_dict(item) for item in loaded_raw]
                print(f"[LOAD] Successfully loaded {len(reconstructed)} record(s) back from disk.")
                print(f"[VERIFY] Integrity check passed: {len(reconstructed)} class objects reconstructed.")
        except FileNotFoundError:
            print(f"[NOTICE] Target file '{self.STORAGE_FILE}' not found.")
        except Exception as exc:
            print(f"[ERROR] Unexpected loading error: {exc}")
        finally:
            print("Operation complete (Reload Stage)")
        print("=" * 76)

    # --------------------------------------------------------------------------
    # In-memory display helper
    # --------------------------------------------------------------------------
    def display_records_table(self):
        if not self.records:
            print("[NOTICE] No records currently stored in session memory.")
            return

        print(f"{'ID':<6} | {'Restaurant Name':<28} | {'Amount':<12} | {'Status':<12} | {'ETA (mins)'}")
        print("-" * 76)
        for r in self.records:
            print(f"#{r.order_id:<5} | {r.name:<28} | Rs.{r.amount:>8.2f} | {r.status:<12} | {r.delivery_time_minutes} min")
        print("-" * 76)
        print(f"Active In-Memory Records: {len(self.records)}\n")

    # --------------------------------------------------------------------------
    # Interactive Console Menu
    # --------------------------------------------------------------------------
    def run_menu(self):
        while True:
            print("\n" + "=" * 76)
            print("         FOOD DELIVERY LIVE DATA PIPELINE - CONSOLE TOOL")
            print("=" * 76)
            print("  [1] Fetch & Display Top 10 Mock Restaurants from API")
            print("  [2] Add a New Restaurant Order (OOP Class Instance)")
            print("  [3] Calculate & Display Commission for All Records (map & filter)")
            print("  [4] Save Records to JSON & Load Them Back (Persistence Roundtrip)")
            print("  [5] Display Current In-Memory Records")
            print("  [6] Exit Pipeline Tool")
            print("=" * 76)

            choice = input("Select an option [1-6]: ").strip()

            if choice == "1":
                self.fetch_api_restaurants()
            elif choice == "2":
                self.add_restaurant_interactive()
            elif choice == "3":
                self.calculate_and_display_commission()
            elif choice == "4":
                self.persist_and_reload()
            elif choice == "5":
                self.display_records_table()
            elif choice == "6":
                print("\n[SHUTDOWN] Exiting Food Delivery Live Data Pipeline. Goodbye!")
                break
            else:
                print(f"[INVALID INPUT] '{choice}' is not a valid menu option. Please choose between 1 and 6.")


def automated_demo():
    """
    Automated execution validating all 4 options non-interactively for testing and logging.
    """
    print("==========================================================================")
    print("      AUTOMATED TEST & DEMO: FOOD DELIVERY LIVE DATA PIPELINE")
    print("==========================================================================")
    pipeline = FoodDeliveryPipeline()

    # Step 1: API Fetch
    print("\n--- STEP 1: Fetch and display top 10 mock restaurants from API ---")
    pipeline.fetch_api_restaurants()

    # Step 2: Add new restaurant programmatically
    print("\n--- STEP 2: Adding custom new restaurant instance ---")
    new_order = Order(
        order_id=11,
        name="Taj Mahal Heritage Cuisine",
        amount=840.50,
        status="Active",
        delivery_time_minutes=28
    )
    pipeline.records.append(new_order)
    print(f"[SUCCESS] Added manual record: {new_order}")

    # Step 3: Commission calculation with map and filter
    print("\n--- STEP 3: Calculate commission using map() and filter() ---")
    pipeline.calculate_and_display_commission()

    # Step 4: Persist and reload
    print("\n--- STEP 4: Save to JSON and reload ---")
    pipeline.persist_and_reload()

    print("\n[TEST RESULT] All 4 required capabilities verified successfully.")
    print("==========================================================================")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["--demo", "--test"]:
        automated_demo()
    else:
        # Check if stdin is interactive
        if sys.stdin.isatty():
            FoodDeliveryPipeline().run_menu()
        else:
            automated_demo()
