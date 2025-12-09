# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository manages UKG ProWFM Adjustment Rules for Children's National Hospital. It contains JSON exports from UKG ProWFM that define pay adjustment rules across different organizational units (cost centers).

## Data Structure

- **Export directories**: Versioned directories (`v1 - before changes/`, `v2 - ...`, `v3 - ...`) contain UKG export snapshots
- **ExportConfig.json**: Metadata about the export (source tenant, version info)
- **AdjustmentRule/response.json**: Main data file containing all adjustment rules
  - Structure: `itemsRetrieveResponses[]` → `responseObjectNode` → `{id, name, ruleVersions}`
  - Each rule is named by cost center (e.g., "10053 - Ambulatory Services")

## Key Concepts

**Triggers**: Rules are organized by trigger numbers (1-44) that map to pay code types:
- Trigger 1: D-CHARGE PAY (Primary)
- Triggers 2-10: CRRT, ECMO, Precept, combo rules
- Triggers 11-22: D-CRITICAL CARE (Day/Night variants)
- Triggers 23-44: D-FLOAT PAY

**OncePerDay**: Boolean property that varies by trigger type. See `gitgit/CN-ADJRULES/CHANGELOG.md` for the standardized pattern.

**DAY/NIGHT codes**: Critical care rules have both DAY and NIGHT variants; pay codes must match (e.g., D-CC PAY-DAY with D-CRITICAL CARE DAY).

## Working with the Data

Python with the venv is set up for JSON processing:
```bash
source venv/bin/activate
```

The response.json files are large (~600KB). Use Python to parse:
```python
import json
with open('path/to/response.json') as f:
    data = json.load(f)
rules = data['itemsRetrieveResponses']
```

## Version History

- V1: Original export (baseline)
- V2: Added missing triggers to cost centers 10053, 10300
- V3: Standardized OncePerDay settings, fixed DAY/NIGHT pay code mismatches

See `gitgit/CN-ADJRULES/CHANGELOG.md` for detailed fix documentation.
