#!/usr/bin/env python3
"""
Script to add "WEEK OT-NO FLOAT" pay code to all triggers that have "REGULAR-NO FLOAT"
"""
import json
from pathlib import Path

def add_weekot_nofloat(data):
    """
    Recursively traverse the JSON structure and add WEEK OT-NO FLOAT
    to any qualifying pay codes list that contains REGULAR-NO FLOAT
    """
    count = 0

    def traverse(obj):
        nonlocal count
        if isinstance(obj, dict):
            # Check if this dict has a "payCodes" key
            if "payCodes" in obj and isinstance(obj["payCodes"], list):
                qpc_list = obj["payCodes"]
                # Check if REGULAR-NO FLOAT is in the list
                has_regular_no_float = any(
                    item.get("qualifier") == "REGULAR-NO FLOAT" or item.get("name") == "REGULAR-NO FLOAT"
                    for item in qpc_list if isinstance(item, dict)
                )
                # Check if WEEK OT-NO FLOAT is already in the list
                has_weekot_no_float = any(
                    item.get("qualifier") == "WEEK OT-NO FLOAT" or item.get("name") == "WEEK OT-NO FLOAT"
                    for item in qpc_list if isinstance(item, dict)
                )

                if has_regular_no_float and not has_weekot_no_float:
                    # Add WEEK OT-NO FLOAT after REGULAR-NO FLOAT
                    new_entry = {
                        "qualifier": "WEEK OT-NO FLOAT",
                        "name": "WEEK OT-NO FLOAT"
                    }
                    # Find position of REGULAR-NO FLOAT and insert after it
                    for i, item in enumerate(qpc_list):
                        if isinstance(item, dict) and (item.get("qualifier") == "REGULAR-NO FLOAT" or item.get("name") == "REGULAR-NO FLOAT"):
                            qpc_list.insert(i + 1, new_entry)
                            count += 1
                            break

            # Continue traversing
            for value in obj.values():
                traverse(value)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)

    traverse(data)
    return count

def main():
    input_file = Path("/Users/evan/mygit/cn-working/AdjRules/v6/AllAdjustmentRules/AdjustmentRule/response.json")

    print(f"Reading {input_file}...")
    with open(input_file, 'r') as f:
        data = json.load(f)

    print("Adding WEEK OT-NO FLOAT to triggers with REGULAR-NO FLOAT...")
    count = add_weekot_nofloat(data)

    print(f"Added WEEK OT-NO FLOAT to {count} qualifying pay code lists")

    # Write back
    print(f"Writing updated file...")
    with open(input_file, 'w') as f:
        json.dump(data, f, indent=2)

    print("Done!")

if __name__ == "__main__":
    main()
