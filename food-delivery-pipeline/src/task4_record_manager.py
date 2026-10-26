"""
================================================================================
Task 4: Food Delivery Record Manager with Persistence
Assessment Code: M2-A1 | Python for Data Science
Description:
    OOP Order record manager implementing JSON serialization/deserialization,
    custom to_dict() and from_dict() methods, and resilient file I/O using
    try-except-finally handling with FileNotFoundError recovery.
================================================================================
"""

import os
import json
from typing import List, Dict, Any

class Order:
    """
    Represents an individual food delivery order with domain-specific attributes.
    """
    def __init__(
        self,
        order_id: int,
        restaurant_name: str,
        amount: float,
        delivery_time_minutes: int,
        is_delivered: bool
    ):
        self.order_id = int(order_id)
        self.restaurant_name = str(restaurant_name)
        self.amount = float(amount)
        self.delivery_time_minutes = int(delivery_time_minutes)
        self.is_delivered = bool(is_delivered)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the Order instance into a JSON-compatible dictionary."""
        return {
            "order_id": self.order_id,
            "restaurant_name": self.restaurant_name,
            "amount": self.amount,
            "delivery_time_minutes": self.delivery_time_minutes,
            "is_delivered": self.is_delivered
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Order":
        """Reconstructs an Order instance from a loaded dictionary."""
        return cls(
            order_id=data["order_id"],
            restaurant_name=data["restaurant_name"],
            amount=data["amount"],
            delivery_time_minutes=data["delivery_time_minutes"],
            is_delivered=data["is_delivered"]
        )

    def __repr__(self) -> str:
        status_str = "Delivered" if self.is_delivered else "In Transit"
        return (
            f"Order(id={self.order_id}, restaurant='{self.restaurant_name}', "
            f"amount=Rs.{self.amount:.2f}, time={self.delivery_time_minutes}m, status='{status_str}')"
        )


def save_records(records: List[Order], filepath: str) -> bool:
    """
    Saves a list of Order objects to a JSON file using json.dump inside a with open() block.
    Wrapped in try-except-finally.
    """
    success = False
    try:
        # Ensure parent directory exists
        parent_dir = os.path.dirname(filepath)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as file:
            serialized_data = [record.to_dict() for record in records]
            json.dump(serialized_data, file, indent=2)
            print(f"[SUCCESS] Successfully saved {len(records)} record(s) to '{filepath}'.")
            success = True
    except Exception as exc:
        print(f"[ERROR] An unexpected error occurred while saving records: {exc}")
        success = False
    finally:
        print("Operation complete")
    return success


def load_records(filepath: str) -> List[Order]:
    """
    Loads JSON order records from disk and reconstructs Order class instances.
    Catches FileNotFoundError specifically to return an empty list instead of crashing,
    catches generic Exception for anything else, and uses finally to print 'Operation complete'.
    """
    reconstructed_orders: List[Order] = []
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            raw_data = json.load(file)
            reconstructed_orders = [Order.from_dict(item) for item in raw_data]
            print(f"[SUCCESS] Loaded {len(reconstructed_orders)} record(s) from '{filepath}'.")
    except FileNotFoundError:
        print(f"[NOTICE] File '{filepath}' not found. Returning an empty list instead of crashing.")
        return []
    except Exception as exc:
        print(f"[ERROR] An unexpected error occurred while loading records: {exc}")
        return []
    finally:
        print("Operation complete")
    return reconstructed_orders


def demo_persistence():
    print("=" * 76)
    print("       TASK 4: FOOD DELIVERY RECORD MANAGER WITH JSON PERSISTENCE")
    print("=" * 76)

    # 1. Instantiate sample Order objects
    sample_orders = [
        Order(101, "Royal Biryani House", 450.00, 32, True),
        Order(102, "Spice Garden Bistro", 320.50, 25, True),
        Order(103, "Pizza Palace Express", 680.00, 40, False),
        Order(104, "Burger King Corner", 190.25, 18, True),
        Order(105, "Urban Wok Asian", 510.00, 35, False),
    ]

    target_filepath = os.path.join("data", "processed", "records.json")

    print("\n--- [Step 1] Saving Order Instances to JSON ---")
    save_records(sample_orders, target_filepath)

    print("\n--- [Step 2] Loading Records Back from JSON File ---")
    loaded_orders = load_records(target_filepath)

    print("\n--- [Step 3] Verifying Reconstructed Objects ---")
    for order in loaded_orders:
        print(f"  * {order}")

    print("\n--- [Step 4] Testing Resilient FileNotFoundError Recovery ---")
    missing_filepath = os.path.join("data", "processed", "non_existent_orders.json")
    empty_result = load_records(missing_filepath)
    print(f"Returned object type: {type(empty_result)}, Content: {empty_result}")

    print("=" * 76)

if __name__ == "__main__":
    demo_persistence()
