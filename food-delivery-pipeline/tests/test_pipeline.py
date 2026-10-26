"""
Unit and integration tests for Food Delivery Pipeline
"""
import unittest
import os
import tempfile
import json
from src.pipeline_app import Order, FoodDeliveryPipeline

class TestFoodDeliveryPipeline(unittest.TestCase):
    def test_order_serialization(self):
        order = Order(1, "Test Bistro", 250.0, "Active", 30)
        data = order.to_dict()
        self.assertEqual(data["order_id"], 1)
        self.assertEqual(data["name"], "Test Bistro")
        self.assertEqual(data["amount"], 250.0)

        reconstructed = Order.from_dict(data)
        self.assertEqual(reconstructed.order_id, 1)
        self.assertEqual(reconstructed.name, "Test Bistro")

    def test_commission_tiers(self):
        self.assertEqual(FoodDeliveryPipeline.calculate_commission(100.0), 10.0)  # 10%
        self.assertEqual(FoodDeliveryPipeline.calculate_commission(200.0), 20.0)  # 10%
        self.assertEqual(FoodDeliveryPipeline.calculate_commission(400.0), 60.0)  # 15%
        self.assertEqual(FoodDeliveryPipeline.calculate_commission(500.0), 75.0)  # 15%
        self.assertEqual(FoodDeliveryPipeline.calculate_commission(600.0), 120.0) # 20%

    def test_persistence_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_records.json")
            orders = [
                Order(10, "Bistro One", 150.0),
                Order(20, "Cafe Two", 450.0)
            ]
            # Save
            with open(filepath, "w") as f:
                json.dump([o.to_dict() for o in orders], f)
            
            # Load
            with open(filepath, "r") as f:
                loaded = [Order.from_dict(d) for d in json.load(f)]
            
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0].name, "Bistro One")
            self.assertEqual(loaded[1].name, "Cafe Two")

if __name__ == "__main__":
    unittest.main()
