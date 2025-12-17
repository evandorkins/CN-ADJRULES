#!/usr/bin/env python3
"""
Script to update D-FLOAT PAY triggers:
- Extract 5-digit cost center from business structure job (jobOrLocation)
- Populate costCenter field with that value
- Clear out jobOrLocation (set to empty object)
- Keep laborCategoryEntries, payCodes, and resulting pay code unchanged
"""
import json
import re
from pathlib import Path

def extract_cost_center(job_qualifier):
    """
    Extract 5-digit cost center from business structure job string.
    Format: "CN/10100/Patient Services/CHG" -> "10100"
    """
    if not job_qualifier:
        return None

    # Look for 5-digit number after "CN/"
    match = re.search(r'CN/(\d{5})/', job_qualifier)
    if match:
        return match.group(1)
    return None

def update_float_triggers(data):
    """
    Find all D-FLOAT PAY triggers and update them:
    - Extract cost center from jobOrLocation
    - Set costCenter field
    - Clear jobOrLocation to empty object
    """
    count = 0
    details = []

    def traverse(obj, path=""):
        nonlocal count
        if isinstance(obj, dict):
            # Check if this is a trigger with D-FLOAT PAY
            is_float_trigger = False
            try:
                pay_code = obj.get("adjustmentAllocation", {}).get("adjustmentAllocation", {}).get("payCode", {})
                if pay_code.get("qualifier") == "D-FLOAT PAY" or pay_code.get("name") == "D-FLOAT PAY":
                    is_float_trigger = True
            except (AttributeError, TypeError):
                pass

            if is_float_trigger:
                # Check if jobOrLocation has a value
                job_or_location = obj.get("jobOrLocation", {})
                qualifier = job_or_location.get("qualifier", "") if isinstance(job_or_location, dict) else ""

                if qualifier:
                    # Extract cost center
                    cost_center = extract_cost_center(qualifier)

                    if cost_center:
                        # Update the trigger
                        obj["costCenter"] = cost_center
                        obj["jobOrLocation"] = {}
                        # laborCategoryEntries stays as is
                        # payCodes stay as is

                        count += 1
                        details.append({
                            "original_job": qualifier,
                            "cost_center": cost_center,
                            "version_num": obj.get("versionNum", "unknown")
                        })

            # Continue traversing
            for key, value in obj.items():
                traverse(value, f"{path}.{key}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                traverse(item, f"{path}[{i}]")

    traverse(data)
    return count, details

def main():
    input_file = Path("/Users/evan/mygit/cn-working/AdjRules/v6/AllAdjustmentRules/AdjustmentRule/response.json")

    print(f"Reading {input_file}...")
    with open(input_file, 'r') as f:
        data = json.load(f)

    print("Finding and updating D-FLOAT PAY triggers...")
    count, details = update_float_triggers(data)

    print(f"\nUpdated {count} D-FLOAT PAY triggers")

    # Show sample of changes
    if details:
        print("\nSample of changes (first 10):")
        for i, d in enumerate(details[:10]):
            print(f"  {i+1}. Version {d['version_num']}: {d['original_job']} -> costCenter: {d['cost_center']}")

        # Show unique cost centers found
        unique_cost_centers = sorted(set(d['cost_center'] for d in details))
        print(f"\nUnique cost centers found: {len(unique_cost_centers)}")
        print(f"  {', '.join(unique_cost_centers)}")

    # Write back
    print(f"\nWriting updated file...")
    with open(input_file, 'w') as f:
        json.dump(data, f, indent=2)

    print("Done!")

if __name__ == "__main__":
    main()
