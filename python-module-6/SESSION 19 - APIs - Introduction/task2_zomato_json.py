"""
Task 2: Zomato Restaurant Object to JSON String
Create a Python dictionary that represents a Zomato-style restaurant object
with fields like name, location, cuisines, and ratings.
Convert this dictionary to a JSON string using the json module and print the result.
"""

import json


def zomato_restaurant_to_json():
    # 1. Create a Python dictionary representing a Zomato-style restaurant object
    restaurant = {
        "id": "res_84920",
        "name": "Spice Garden & Grill",
        "location": {
            "address": "42, Linking Road, Near Bandra Station",
            "city": "Mumbai",
            "locality": "Bandra West",
            "pincode": "400050",
            "latitude": 19.0596,
            "longitude": 72.8295,
        },
        "cuisines": ["North Indian", "Mughlai", "Biryani", "Chinese"],
        "ratings": {
            "aggregate_rating": 4.5,
            "rating_text": "Very Good",
            "votes_count": 1280,
        },
        "cost_for_two": 750,
        "is_delivering_now": True,
        "features": [
            "Online Ordering",
            "Table Reservation",
            "Outdoor Seating",
            "Free Wi-Fi",
        ],
    }

    print("=" * 60)
    print("1. Python Dictionary (Original Object):")
    print("=" * 60)
    print(restaurant)
    print(f"\nData Type: {type(restaurant)}\n")

    # 2. Convert dictionary to JSON formatted string using json.dumps
    json_string = json.dumps(restaurant, indent=4)

    print("=" * 60)
    print("2. Serialized JSON String (via json.dumps):")
    print("=" * 60)
    print(json_string)
    print(f"\nData Type: {type(json_string)}")

    return json_string


if __name__ == "__main__":
    zomato_restaurant_to_json()
