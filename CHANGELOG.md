# CN-ADJRULES Changelog

## V3 - Fixes Applied (December 2025)

### Overview
V3 represents the corrected and standardized version of the Children's National Hospital UKG ProWFM Adjustment Rules. All fixes were applied to address inconsistencies found during analysis of the V2 export.

---

### Fix #1: Critical Care DAY/NIGHT Mismatch
**Date:** 2025-12-09
**Rule Affected:** 10301 - Heart And Kidney
**Trigger:** 13

| Field | Before | After |
|-------|--------|-------|
| Result Pay Code | D-CRITICAL CARE NIGHT | D-CRITICAL CARE NIGHT (unchanged) |
| Job Trigger Pay Code | D-CC PAY-DAY | **D-CC PAY-NT** |

**Issue:** The result pay code indicated NIGHT but the trigger pay code was set to DAY, causing a mismatch.

**Resolution:** Changed trigger pay code from `D-CC PAY-DAY` to `D-CC PAY-NT` to match the NIGHT result.

---

### Fix #2: OncePerDay Inconsistencies (Trigger 4 - Standalone Precept)
**Date:** 2025-12-09
**Rules Affected:** 3 rules
**Trigger:** 4 (D-PRECEPT PAY)

| Rule | Before | After |
|------|--------|-------|
| 10053 - Ambulatory Services | OncePerDay=False | **OncePerDay=True** |
| 10300 - Neonatal Intens Care | OncePerDay=False | **OncePerDay=True** |
| 10301 - Heart And Kidney | OncePerDay=False | **OncePerDay=True** |

**Issue:** 20 rules had `OncePerDay=True` but 3 rules had `OncePerDay=False`, creating inconsistent behavior.

**Resolution:** Standardized all 23 rules to `OncePerDay=True` for Trigger 4.

---

### Fix #3: OncePerDay Inconsistencies (Triggers 2, 3, 7, 8)
**Date:** 2025-12-09
**Rules Affected:** 4 rules
**Triggers:** 2 (CRRT), 3 (D-ECMO PAY), 7 (D-CHARGE PAY combo), 8 (D-ECMO PAY combo)

#### Trigger 2 (CRRT - Primary)
| Rule | Before | After |
|------|--------|-------|
| 10053 - Ambulatory Services | OncePerDay=False | **OncePerDay=True** |
| 10300 - Neonatal Intens Care | OncePerDay=False | **OncePerDay=True** |
| 10301 - Heart And Kidney | OncePerDay=False | **OncePerDay=True** |
| 10355 - PACU | OncePerDay=False | **OncePerDay=True** |

#### Trigger 3 (D-ECMO PAY - Primary)
| Rule | Before | After |
|------|--------|-------|
| 10053 - Ambulatory Services | OncePerDay=False | **OncePerDay=True** |
| 10300 - Neonatal Intens Care | OncePerDay=False | **OncePerDay=True** |
| 10301 - Heart And Kidney | OncePerDay=False | **OncePerDay=True** |
| 10355 - PACU | OncePerDay=False | **OncePerDay=True** |

#### Trigger 7 (D-CHARGE PAY - CHG-ECMO Combo Part 1)
| Rule | Before | After |
|------|--------|-------|
| 10300 - Neonatal Intens Care | OncePerDay=False | **OncePerDay=True** |
| 10301 - Heart And Kidney | OncePerDay=False | **OncePerDay=True** |
| 10355 - PACU | OncePerDay=False | **OncePerDay=True** |

#### Trigger 8 (D-ECMO PAY - CHG-ECMO Combo Part 2)
| Rule | Before | After |
|------|--------|-------|
| 10300 - Neonatal Intens Care | OncePerDay=False | **OncePerDay=True** |
| 10301 - Heart And Kidney | OncePerDay=False | **OncePerDay=True** |
| 10355 - PACU | OncePerDay=False | **OncePerDay=True** |

**Issue:** These triggers had inconsistent `OncePerDay` settings across rules.

**Resolution:** Standardized all to `OncePerDay=True` to match the majority pattern.

---

### Fix #4: Missing Qualifying Pay Codes
**Date:** 2025-12-09
**Rule Affected:** Crisis RNs, Float-Eligible General

| Rule | Trigger Index | Result Pay Code | Before | After |
|------|---------------|-----------------|--------|-------|
| Crisis RNs | 3 | D-PRECEPT PAY (Standalone) | (empty) | **REGULAR, WEEK OT** |
| Crisis RNs | 4 | CRRT | (empty) | **REGULAR, WEEK OT** |
| Crisis RNs | 6 | D-ECMO PAY | (empty) | **REGULAR, WEEK OT** |
| Float-Eligible General | 3 | D-PRECEPT PAY (Standalone) | (empty) | **REGULAR, WEEK OT** |

**Issue:** These triggers had no qualifying pay codes defined, meaning the adjustment rules would not fire properly.

**Resolution:** Added `REGULAR` and `WEEK OT` as qualifying pay codes to match all other rules.

---

## V3 Final State - OncePerDay Pattern

| Trigger Range | Pay Code Type | OncePerDay | Count |
|---------------|---------------|------------|-------|
| 1 | D-CHARGE PAY (Primary) | False | 23/23 |
| 2-10 | CRRT, ECMO, Precept, Combos | **True** | 23/23 |
| 11-22 | D-CRITICAL CARE (Day/Night) | False | 23/23 |
| 23-44 | D-FLOAT PAY | False | 23/23 |

---

## Total Fixes Applied

| Fix Type | Count |
|----------|-------|
| DAY/NIGHT Mismatch | 1 |
| OncePerDay Corrections | 17 |
| Missing Qualifying Pay Codes | 4 |
| **Total** | **22** |

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| V1 | 2025-12-08 | Original export (before changes) |
| V2 | 2025-12-08 | Changes uploaded - added missing triggers to 10053, 10300 |
| V3 | 2025-12-09 | Fixes applied - standardized OncePerDay, fixed DAY/NIGHT mismatch |
