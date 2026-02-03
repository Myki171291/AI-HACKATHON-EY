# DATA LINKAGE ANALYSIS - EXECUTIVE SUMMARY

**Analysis Date:** February 3, 2026  
**Analyst:** AI Data Quality Check  
**Dataset:** SkyMarshal Airline Operations System

---

## 🚨 CRITICAL FINDINGS

Your suspicion is **CONFIRMED**. Data linkage is **NOT properly done** across CSV files for flights, passengers, bookings, cargo, and baggage.

### Key Issues Found:
1. ❌ **80% of flights have NO passenger data** (20 out of 25 flights)
2. ❌ **72% of flights have NO booking data** (18 out of 25 flights)
3. ❌ **5 booking records are ORPHANED** (reference non-existent passengers)
4. ⚠️ **60% of flights have NO baggage data** (15 out of 25 flights)

---

## DATA QUALITY SCORECARD

| Metric | Status | Details |
|--------|--------|---------|
| **Passenger Coverage** | ❌ CRITICAL | Only 5/25 flights (20%) have passengers |
| **Booking Coverage** | ❌ CRITICAL | Only 7/25 flights (28%) have bookings |
| **Baggage Coverage** | ⚠️ WARNING | Only 10/25 flights (40%) have baggage |
| **Cargo Coverage** | ✓ GOOD | 8/25 flights (32%) have cargo |
| **Passenger-Booking Linkage** | ⚠️ WARNING | 5/20 bookings are orphaned |
| **Baggage-Passenger Linkage** | ✓ GOOD | 22/22 records properly linked |

**Overall Data Quality Score: 2.5/5** 🔴

---

## THE 4 TEST FLIGHTS ANALYZED

### Sample Flight #1: EY117 (BKK → AUH)
**Status:** ✅ PERFECTLY LINKED

| Component | Count | Status |
|-----------|-------|--------|
| Passengers | 3 | ✓ Complete |
| Bookings | 3 | ✓ Complete |
| Cargo | 1 | ✓ Complete |
| Baggage | 3 | ✓ Complete |

**Passengers:** Ali Al-Mansouri, Fatima Al-Mazrouei, Mohammed Al-Kaabi

---

### Sample Flight #2: EY5293 (AUH → BKK)
**Status:** ✅ PERFECTLY LINKED

| Component | Count | Status |
|-----------|-------|--------|
| Passengers | 3 | ✓ Complete |
| Bookings | 3 | ✓ Complete |
| Cargo | 1 | ✓ Complete |
| Baggage | 3 | ✓ Complete |

**Passengers:** Sarah Johnson, James Mitchell, Emma Brown

---

### Sample Flight #3: EY454 (AUH → SYD)
**Status:** ✅ PERFECTLY LINKED

| Component | Count | Status |
|-----------|-------|--------|
| Passengers | 3 | ✓ Complete |
| Bookings | 3 | ✓ Complete |
| Cargo | 2 | ✓ Complete |
| Baggage | 3 | ✓ Complete |

**Passengers:** Yuki Tanaka, Pierre Dubois, Maria Garcia

---

### Sample Flight #4: EY334 (AUH → CDG)
**Status:** ✅ PERFECTLY LINKED

| Component | Count | Status |
|-----------|-------|--------|
| Passengers | 3 | ✓ Complete |
| Bookings | 3 | ✓ Complete |
| Cargo | 1 | ✓ Complete |
| Baggage | 3 | ✓ Complete |

**Passengers:** Heinrich Mueller, Lisa Wong, Marcus Johnson

---

## WHAT LINKAGE ACTUALLY WORKS?

### ✅ Working Linkages:
- **Passenger → Booking** - Every passenger that exists has a booking
- **Booking Reference Match** - References match between passengers and bookings files
- **Seat Assignment** - Seat numbers match consistently between files
- **Baggage → Passenger** - All baggage records properly link to passengers
- **Cargo → Flight** - All cargo shipments properly linked to flights

### ❌ Broken Linkages:
- **Flight → Passenger** - 20 flights have no passengers
- **Flight → Booking** - 18 flights have no bookings
- **Booking → Passenger** - 5 bookings reference non-existent passengers (PAX-016 to PAX-020)
- **Flight → Baggage** - 15 flights have no baggage records

---

## ORPHANED RECORDS FOUND

### 5 Bookings with Missing Passengers:

| Booking ID | Flight | Passenger ID | Status |
|-----------|--------|--------------|--------|
| BKG-EY313-001 | EY313 | PAX-016 | NOT IN passengers_enriched_final.csv |
| BKG-EY313-002 | EY313 | PAX-017 | NOT IN passengers_enriched_final.csv |
| BKG-EY313-003 | EY313 | PAX-018 | NOT IN passengers_enriched_final.csv |
| BKG-EY402-001 | EY402 | PAX-019 | NOT IN passengers_enriched_final.csv |
| BKG-EY402-002 | EY402 | PAX-020 | NOT IN passengers_enriched_final.csv |

---

## FLIGHTS WITH COMPLETE DATA (5 only):

```
1. EY117 - Bangkok → Abu Dhabi
2. EY5293 - Abu Dhabi → Bangkok  
3. EY334 - Abu Dhabi → Paris
4. EY424 - Abu Dhabi → Singapore
5. EY454 - Abu Dhabi → Sydney
```

**These 5 flights represent the EXCEPTION with perfect linkage.**

---

## FLIGHTS WITH BROKEN LINKAGES (2):

```
1. EY313 - Abu Dhabi → Jeddah
   ⚠️ Has 3 bookings but NO passengers (bookings are orphaned)
   ⚠️ Has cargo (PHARMA)

2. EY402 - Bangkok → Abu Dhabi
   ⚠️ Has 2 bookings but NO passengers (bookings are orphaned)
   ⚠️ Has cargo
```

---

## FLIGHTS WITH ZERO DATA (10):

```
EY003, EY101, EY106, EY11, EY19, EY25, EY3102, EY3103, EY3105, 
EY639, EY8086, EY8087, EY912, EY401, EY406, EY472, EY6268, EY8184
```

These flights exist in flights_enriched_scenarios.csv but have **NO** passenger, booking, or baggage data.

---

## ROOT CAUSES

### Why is data incomplete?

1. **Incomplete Data Generation** - Only first 5 flights have full passenger/booking records
2. **Multiple Data Sources** - Different files may be from different data loads or system states
3. **Test Data Confusion** - Some flights may be test/backup flights not meant to have passenger data
4. **Manual Data Entry Issues** - Bookings created for passengers not yet added to passenger file
5. **Missing Data Pipeline Step** - No synchronization between flights and passengers files

### Why are bookings orphaned?

- **Out-of-sync files** - bookings.csv references passengers (PAX-016 to PAX-020) that don't exist in passengers_enriched_final.csv
- **Version mismatch** - Files may be from different update cycles
- **Manual corrections** - Someone may have manually adjusted one file but not the other

---

## RECOMMENDATIONS (Priority Order)

### 🔴 IMMEDIATE (Fix in next 24 hours):

1. **Add missing passengers** - Create PAX-016 through PAX-020 in passengers_enriched_final.csv
   OR
   **Delete orphaned bookings** - Remove BKG-EY313-001/002/003 and BKG-EY402-001/002

2. **Document data state** - Identify which flights SHOULD have passenger data vs. which are placeholders

### 🟠 URGENT (Fix within 1 week):

3. **Populate passenger data** - For all 20 flights currently missing passengers
4. **Create corresponding bookings** - For newly added passengers
5. **Add baggage records** - For all flights with passengers

### 🟡 IMPORTANT (Fix within 1 month):

6. **Implement validation rules** - Prevent future orphaned records
7. **Create data linkage tests** - Automated checks for referential integrity
8. **Document requirements** - Specify which data elements are mandatory for each flight

---

## ANALYSIS ARTIFACTS CREATED

The following analysis files have been created:

1. **DATA_LINKAGE_ANALYSIS_REPORT.md** - Comprehensive detailed report
2. **DATA_LINKAGE_ISSUES_DETAILED.md** - Issue breakdown with root causes
3. **FLIGHT_DATA_LINKAGE_MAPPING.csv** - Flight-by-flight mapping table
4. **check_data_linkage.py** - Analysis script for 4 sample flights
5. **comprehensive_linkage_check.py** - Global analysis script
6. **generate_flight_mapping.py** - Flight mapping generation script

Use these files to:
- Share with your team
- Track remediation progress
- Implement automated validation
- Document data quality baseline

---

## NEXT STEPS

1. ✅ Review this summary with your team
2. ✅ Decide on orphaned bookings handling (add passengers or delete bookings)
3. ✅ Identify which of the 20 missing-data flights SHOULD have passengers
4. ✅ Create data population plan
5. ✅ Assign ownership for each issue
6. ✅ Set remediation timeline

---

## CONCLUSION

Your data linkage concerns are **absolutely valid**. The current state shows:
- ✅ Good: 5 flights with perfect end-to-end linkage
- ⚠️ Partial: Orphaned records exist
- ❌ Poor: 80% of flights lack basic passenger data

**Immediate action is required to remediate these issues before the system can be considered production-ready.**

