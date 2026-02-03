# DATA LINKAGE ISSUES - DETAILED BREAKDOWN

## Missing Passenger Records

### Flights WITHOUT any passenger data (20 flights):

```
Flight Number | Origin | Destination | Aircraft  | Issue
--------------|--------|-------------|-----------|-------------------
EY313         | AUH    | JED         | B777      | No passengers, but 3 bookings orphaned
EY472         | AUH    | SIN         | B777      | No passengers, no bookings
EY101         | AUH    | JFK         | B787-10   | No passengers, no bookings
EY25          | CDG    | AUH         | A320      | No passengers, no bookings
EY8184        | Unknown| Unknown     | Unknown   | No passengers, no bookings
EY6268        | Unknown| Unknown     | Unknown   | No passengers, no bookings
EY19          | Unknown| Unknown     | Unknown   | No passengers, no bookings
EY11          | Unknown| Unknown     | Unknown   | No passengers, no bookings
EY401         | Unknown| Unknown     | Unknown   | No passengers, no bookings
EY406         | Unknown| Unknown     | Unknown   | No passengers, no bookings
EY639         | Unknown| Unknown     | Unknown   | No passengers, no bookings
EY3105        | Unknown| Unknown     | Unknown   | No passengers, no bookings
EY3102        | Unknown| Unknown     | Unknown   | No passengers, no bookings
EY003         | Unknown| Unknown     | Unknown   | No passengers, no bookings
EY8086        | Unknown| Unknown     | Unknown   | No passengers, no bookings
EY8087        | Unknown| Unknown     | Unknown   | No passengers, no bookings
EY402         | Unknown| Unknown     | Unknown   | No passengers, but 2 bookings orphaned
EY106         | Unknown| Unknown     | Unknown   | No passengers, no bookings
EY912         | Unknown| Unknown     | Unknown   | No passengers, no bookings
EY3103        | Unknown| Unknown     | Unknown   | No passengers, no bookings
```

---

## Orphaned Booking Records

### Bookings that reference non-existent passengers (5 bookings):

```
Booking ID      | Flight | Passenger ID | Issue
----------------|--------|--------------|-------
BKG-EY313-001   | EY313  | PAX-016      | Passenger NOT in passengers_enriched_final.csv
BKG-EY313-002   | EY313  | PAX-017      | Passenger NOT in passengers_enriched_final.csv
BKG-EY313-003   | EY313  | PAX-018      | Passenger NOT in passengers_enriched_final.csv
BKG-EY402-001   | EY402  | PAX-019      | Passenger NOT in passengers_enriched_final.csv
BKG-EY402-002   | EY402  | PAX-020      | Passenger NOT in passengers_enriched_final.csv
```

---

## Flights WITHOUT Baggage Records (15 flights):

```
EY313, EY472, EY101, EY401, EY406, EY639, EY3105, EY3102, EY003, 
EY8086, EY8087, EY402, EY106, EY912, EY3103
```

---

## Data Completeness by File

### flights_enriched_scenarios.csv
- ✓ Total Records: 25
- ✓ All flights have basic info (origin, destination, aircraft)
- ⚠️ Issue: Some flights in this file may be missing from other files

### passengers_enriched_final.csv
- ⚠️ Total Records: 15
- ⚠️ Coverage: Only 5 out of 25 flights have passengers
- ❌ Missing passengers: PAX-016 through PAX-020 (referenced in bookings.csv but not here)

### bookings.csv
- ⚠️ Total Records: 20
- ⚠️ Coverage: Only 7 out of 25 flights have bookings
- ❌ Issue: 5 bookings reference passengers not in passengers_enriched_final.csv

### cargo_shipments.csv
- ✓ Total Records: 10
- ✓ All cargo properly linked to flights
- ✓ Coverage: 8 different flights have cargo

### baggage_handling.csv
- ⚠️ Total Records: 22
- ⚠️ Coverage: Only 10 out of 25 flights have baggage
- ⚠️ Anomaly: EY424 has 7 baggage records for 3 passengers

---

## Data Linkage Matrix

```
                    Has Passengers?  Has Bookings?  Has Cargo?  Has Baggage?
EY117               ✓ (3)            ✓ (3)          ✓           ✓ (3)
EY5293              ✓ (3)            ✓ (3)          ✓           ✓ (3)
EY454               ✓ (3)            ✓ (3)          ✓ (2)       ✓ (3)
EY334               ✓ (3)            ✓ (3)          ✓           ✓ (3)
EY424               ✓ (3)            ✓ (3)          ✓           ✓ (7)
EY313               ❌               ⚠️ (3 orphaned)✓           ❌
EY472               ❌               ❌             ✓           ❌
EY101               ❌               ❌             ✓           ❌
EY25                ❌               ❌             ❌           ❌
EY402               ❌               ⚠️ (2 orphaned)❌           ❌
(+15 more flights) ❌               ❌             ❌           ❌
```

---

## Root Cause Analysis

### Why are 20 flights missing passenger data?

**Possible Causes:**
1. **Data generation incomplete** - Only first 5 flights have passenger records generated
2. **File consolidation issue** - Passenger data for other flights may be in different files
3. **Data model mismatch** - flights_enriched_scenarios.csv may contain all planned flights, while passengers_enriched_final.csv only contains booked flights

### Why are bookings orphaned?

**Possible Causes:**
1. **Manual data entry** - Bookings created for passengers who were not yet added to passengers_enriched_final.csv
2. **Data pipeline error** - Passenger records not properly synced from source system
3. **File version mismatch** - bookings.csv may be from a different data version

### Why is baggage coverage incomplete?

**Possible Causes:**
1. **Data generation scope** - Only booked passengers have baggage records
2. **Cargo vs Baggage confusion** - Some flights may have cargo instead of checked baggage
3. **Baggage data optional** - May be intentional for certain flight types

---

## Required Actions

### To fix orphaned bookings:
```
Option A: Add missing passengers to passengers_enriched_final.csv
- PAX-016: Associated with EY313, Booking Ref ABC132?, seat assignment from booking
- PAX-017: Associated with EY313, Booking Ref ABC133?, seat assignment from booking  
- PAX-018: Associated with EY313, Booking Ref ABC134?, seat assignment from booking
- PAX-019: Associated with EY402, Booking Ref ?, seat assignment from booking
- PAX-020: Associated with EY402, Booking Ref ?, seat assignment from booking

Option B: Remove orphaned bookings from bookings.csv
- Delete all 5 orphaned booking records
```

### To add passenger data to remaining flights:
```
1. Identify which flights should have passengers
2. Generate passenger records for those flights
3. Create corresponding baggage records
4. Ensure booking records exist for each passenger
```

### To fix EY424 baggage anomaly:
```
1. Verify if 7 bags for 3 passengers is intentional (e.g., multiple bags per passenger)
2. If not, investigate which baggage records are duplicates/errors
3. Update baggage_handling.csv accordingly
```

---

## Testing Observations

The 4 sample flights tested (EY117, EY5293, EY454, EY334) all show **perfect linkage**:
- ✓ Every passenger has exactly one booking
- ✓ Every booking has a corresponding passenger
- ✓ All baggage records link to valid passengers
- ✓ All booking references match between files
- ✓ All seat assignments are consistent

**However**, these 4 flights represent the EXCEPTION, not the rule. The remaining 21 flights (84%) show significant data gaps.

