# DATA LINKAGE - VISUAL COMPARISON

## GOOD LINKAGE EXAMPLE (EY117)

```
┌─────────────────────────────────────────────────────┐
│  FLIGHT: EY117 (BKK → AUH)                         │
│  ✅ COMPLETE DATA LINKAGE                           │
└─────────────────────────────────────────────────────┘

flights_enriched_scenarios.csv
├── FLT-1001
│   ├── flight_number: EY117
│   ├── aircraft: A320
│   └── capacity: 180 passengers

       ✓ LINKED TO:
       
       passengers_enriched_final.csv
       ├── PAX-001: Ali Al-Mansouri
       ├── PAX-002: Fatima Al-Mazrouei
       └── PAX-003: Mohammed Al-Kaabi
           
           ✓ LINKED TO:
           
           bookings.csv
           ├── BKG-EY117-001 (PAX-001)
           ├── BKG-EY117-002 (PAX-002)
           └── BKG-EY117-003 (PAX-003)
               
               ✓ LINKED TO:
               
               baggage_handling.csv
               ├── BAG-EY117-001 (PAX-001)
               ├── BAG-EY117-002 (PAX-002)
               └── BAG-EY117-003 (PAX-003)

       ✓ ALSO LINKED TO:
       
       cargo_shipments.csv
       └── CARGO-EY117-001 (2,000 kg)
```

---

## BROKEN LINKAGE EXAMPLE #1 (EY313)

```
┌─────────────────────────────────────────────────────┐
│  FLIGHT: EY313 (AUH → JED)                         │
│  ❌ BROKEN PASSENGER LINKAGE                        │
│  ⚠️ ORPHANED BOOKINGS                               │
└─────────────────────────────────────────────────────┘

flights_enriched_scenarios.csv
├── FLT-6
│   ├── flight_number: EY313
│   ├── aircraft: B777
│   └── capacity: 396 passengers

       ❌ NO PASSENGERS IN passengers_enriched_final.csv
       
       BUT ⚠️ ORPHANED BOOKINGS EXIST:
       
       bookings.csv
       ├── BKG-EY313-001 → PAX-016 ❌ (NOT IN passengers file)
       ├── BKG-EY313-002 → PAX-017 ❌ (NOT IN passengers file)
       └── BKG-EY313-003 → PAX-018 ❌ (NOT IN passengers file)
           
           ❌ NO BAGGAGE FOR THESE PASSENGERS

       ✓ HAS CARGO:
       
       cargo_shipments.csv
       └── CARGO-EY313-001 (1,200 kg, PERISHABLE)
```

---

## BROKEN LINKAGE EXAMPLE #2 (EY101)

```
┌─────────────────────────────────────────────────────┐
│  FLIGHT: EY101 (AUH → JFK)                         │
│  ❌ COMPLETE DATA ABSENCE                           │
│  (except cargo)                                     │
└─────────────────────────────────────────────────────┘

flights_enriched_scenarios.csv
├── FLT-8
│   ├── flight_number: EY101
│   ├── aircraft: B787-10
│   └── capacity: 330 passengers

       ❌ NO PASSENGERS
       ❌ NO BOOKINGS  
       ❌ NO BAGGAGE

       ✓ HAS CARGO:
       
       cargo_shipments.csv
       └── CARGO-EY101-001 (800 kg, HAZMAT)
```

---

## DATA PRESENCE COMPARISON

### Type 1: FULLY LINKED (5 flights) ✅
```
Flight → Passengers → Bookings → Baggage
   ↓         ↓          ↓          ✓
  ✓         ✓          ✓          ✓
   └→ Cargo (exists)
```
Examples: EY117, EY5293, EY454, EY334, EY424

### Type 2: ORPHANED BOOKINGS (2 flights) ⚠️
```
Flight → [No Passengers] ← Bookings (orphaned)
   ↓                           ❌
  ✓                       NO LINKAGE
   └→ Cargo (exists)
```
Examples: EY313 (3 orphaned), EY402 (2 orphaned)

### Type 3: MISSING ALL DATA (18 flights) ❌
```
Flight → [No Passengers]
   ↓         [No Bookings]
  ✓          [No Baggage]
   ├→ Cargo (exists for some)
   └→ Cargo (missing for others)
```
Examples: EY101, EY472, EY25, EY8184, etc.

---

## FILE-BY-FILE STATUS

### flights_enriched_scenarios.csv
```
Status: ✓ Complete
Records: 25 flights
All flights have basic information
├── Origin airport ✓
├── Destination airport ✓
├── Aircraft type ✓
└── Capacity ✓

Coverage to other files:
├── To passengers.csv: 20% (5/25 flights)
├── To bookings.csv: 28% (7/25 flights)
├── To cargo.csv: 32% (8/25 flights)
└── To baggage.csv: 40% (10/25 flights)
```

### passengers_enriched_final.csv
```
Status: ⚠️ INCOMPLETE
Records: 15 passengers
Coverage: Only 5 flights have passengers
│
├─ EY117: 3 passengers ✓
├─ EY5293: 3 passengers ✓
├─ EY454: 3 passengers ✓
├─ EY334: 3 passengers ✓
├─ EY424: 3 passengers ✓
│
└─ Missing: 20 flights with 0 passengers ❌

All existing passengers have proper data
├── Booking references ✓
├── Seat assignments ✓
└── Connection information ✓
```

### bookings.csv
```
Status: ⚠️ BROKEN
Records: 20 bookings
Coverage: 7 flights have bookings
│
✓ Good bookings: 15 (link to existing passengers)
❌ Orphaned bookings: 5 (link to PAX-016 through PAX-020)
│
├─ EY117: 3 bookings ✓
├─ EY5293: 3 bookings ✓
├─ EY454: 3 bookings ✓
├─ EY334: 3 bookings ✓
├─ EY424: 3 bookings ✓
├─ EY313: 3 bookings ⚠️ (orphaned)
├─ EY402: 2 bookings ⚠️ (orphaned)
│
└─ Missing: 18 flights with 0 bookings ❌
```

### cargo_shipments.csv
```
Status: ✓ GOOD
Records: 10 shipments
Coverage: 8 flights have cargo
│
All shipments properly linked
├─ EY117: 1 shipment ✓
├─ EY5293: 1 shipment ✓
├─ EY454: 2 shipments ✓
├─ EY334: 1 shipment ✓
├─ EY424: 1 shipment ✓
├─ EY313: 1 shipment ✓
├─ EY472: 1 shipment ✓
├─ EY101: 1 shipment ✓
│
└─ Missing: 17 flights with 0 cargo (informational)
```

### baggage_handling.csv
```
Status: ⚠️ INCOMPLETE
Records: 22 baggage items
Coverage: 10 flights have baggage
│
All linked to valid passengers ✓
├─ EY117: 3 items ✓
├─ EY5293: 3 items ✓
├─ EY454: 3 items ✓
├─ EY334: 3 items ✓
├─ EY424: 7 items ✓ (⚠️ more items than passengers)
│
├─ EY11: 1 item (no passenger data)
├─ EY19: 1 item (no passenger data)
├─ EY25: 2 items (no passenger data)
├─ EY6268: 1 item (no passenger data)
└─ EY8184: 2 items (no passenger data)

Missing: 15 flights with 0 baggage ❌
```

---

## CRITICAL DATA FLOW BREAKS

```
Expected Flow:
Flight → Passenger → Booking → Baggage
  1        2          3        4

Status by Stage:
Stage 1: Flight → Passenger     ❌ 80% fail (20/25 flights)
Stage 2: Passenger → Booking    ⚠️ 25% fail orphaned (5/20)
Stage 3: Booking → Baggage      ⚠️ 60% missing (15/25 flights)
Stage 4: All linked             ❌ 80% fail (20/25 flights)

Success Rate by Flight:
✓ 5 flights (20%) - All stages pass
⚠️ 2 flights (8%) - Partial success (bookings orphaned)
❌ 18 flights (72%) - Complete failure

```

---

## WHAT NEEDS TO HAPPEN

### For the 5 Good Flights:
```
✓ EY117  - PRODUCTION READY (all data complete)
✓ EY5293 - PRODUCTION READY (all data complete)
✓ EY334  - PRODUCTION READY (all data complete)
✓ EY424  - PRODUCTION READY (all data complete)
✓ EY454  - PRODUCTION READY (all data complete)
```

### For the 2 Broken Flights (Orphaned):
```
Option A: Add Missing Passengers
├── Add PAX-016, PAX-017, PAX-018 to passengers_enriched_final.csv
├── Populate their details from booking records
├── Create baggage records for them
└── Result: Fix broken linkage

Option B: Delete Orphaned Bookings  
├── Remove BKG-EY313-001, 002, 003 from bookings.csv
├── Remove BKG-EY402-001, 002 from bookings.csv
└── Result: Remove broken records

Recommended: Option A (recover data, don't delete)
```

### For the 18 Empty Flights:
```
Step 1: Decide - Are these flights supposed to have passengers?
        ├─ If YES: Generate passenger data
        ├─ If NO: Mark as test/placeholder flights
        └─ If UNKNOWN: Get clarification

Step 2: For each flight that needs passengers:
        ├─ Add passengers to passengers_enriched_final.csv
        ├─ Create bookings in bookings.csv
        ├─ Create baggage in baggage_handling.csv
        └─ Create cargo in cargo_shipments.csv (if applicable)

Step 3: Validate all linkages
        ├─ Run linkage checks
        ├─ Confirm no orphaned records
        └─ Verify referential integrity
```

---

## SUMMARY TABLE

| Flight | Pax | Bkg | Cargo | Bag | Status | Action Required |
|--------|-----|-----|-------|-----|--------|-----------------|
| EY117 | ✓ | ✓ | ✓ | ✓ | READY | None |
| EY5293 | ✓ | ✓ | ✓ | ✓ | READY | None |
| EY334 | ✓ | ✓ | ✓ | ✓ | READY | None |
| EY424 | ✓ | ✓ | ✓ | ✓ | READY | None |
| EY454 | ✓ | ✓ | ✓ | ✓ | READY | None |
| EY313 | ❌ | ⚠️ | ✓ | ❌ | BROKEN | Add PAX-16/17/18 or delete BKG |
| EY402 | ❌ | ⚠️ | ✓ | ❌ | BROKEN | Add PAX-19/20 or delete BKG |
| 18 others | ❌ | ❌ | var | ❌ | EMPTY | Populate with data or mark as test |

