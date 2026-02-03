# EY402 DISRUPTION REPORT
## Bangkok Typhoon Impact Analysis
**Report Generated:** January 30, 2026 00:00 UTC  
**Frozen Point:** January 30, 2026 00:00H (UTC+4 Abu Dhabi)

---

# A. SITUATION

## 1. Flight Information

| Field | Value |
|-------|-------|
| Flight ID | FLT-1006 |
| Flight Number | **EY402** |
| Route | **BKK → AUH** (Bangkok to Abu Dhabi) |
| Aircraft | A6-BLA (Boeing 787-9) |
| Scheduled Departure | **2026-01-30 11:00 UTC** |
| Scheduled Arrival | 2026-01-30 14:30 UTC |
| Flight Duration | 3h 30m |
| Gate/Terminal | B8 / Terminal 2 (BKK) |
| Aircraft Capacity | 299 passengers |
| Cargo Capacity | 15,000 kg |
| Crew Required | 10 |

## 2. Aircraft Rotation Chain

```
ROTATION CHAIN (Aircraft A6-BLA):

FLT-1005 (EY401) AUH→BKK [Dep 02:30, Arr 09:00] ← Arrives during typhoon!
    ↓ (90 min turnaround)
FLT-1006 (EY402) BKK→AUH [Dep 11:00, Arr 14:30] ← BLOCKED BY TYPHOON
    ↓ (120 min turnaround)
FLT-1007 (EY406) AUH→BKK [Dep 16:30, Arr 23:00] ← CASCADING DELAY
    ↓ (120 min turnaround)
FLT-1008 (EY407) BKK→AUH [Dep 01:00+1, Arr 04:30+1] ← CASCADING DELAY
```

**Critical Issue:** EY401 arrives BKK at 09:00 UTC - during typhoon (airport closed). Aircraft may need to hold or divert.

## 3. Weather Disruption

### Bangkok (BKK) - Suvarnabhumi Airport

| Time (UTC) | Condition | Wind | Visibility | Operational |
|------------|-----------|------|------------|-------------|
| 06:00 | **TYPHOON** | 85 kts | 500m | ❌ **CLOSED** |
| 09:00 | **TYPHOON** | 90 kts | 500m | ❌ **CLOSED** |
| **11:00** | **TYPHOON** | ~85 kts | 500m | ❌ **CLOSED** |
| 12:00 | **TYPHOON** | 82 kts | 500m | ❌ **CLOSED** |
| 15:00 | RAIN | 45 kts | 2000m | ✅ Open |
| 18:00 | RAIN | 30 kts | 4000m | ✅ Open |

### Impact Summary

| Impact | Details |
|--------|---------|
| **EY402 Scheduled Departure** | 11:00 UTC |
| **Airport Status at 11:00** | ❌ **CLOSED - TYPHOON** |
| **Airport Reopens** | ~15:00 UTC |
| **Minimum Delay** | **4 HOURS** |
| **Inbound Aircraft (EY401)** | Arrives 09:00 - may divert/hold |

## 4. Passenger Impact

### Passengers on EY402 (FLT-1006)

| PAX ID | Name | Class | FF Tier | Connecting From | Connecting To |
|--------|------|-------|---------|-----------------|---------------|
| PAX-10006 | John Brown | Economy | - | EY401 (BKK) | EY11 (LHR) |
| PAX-10007 | Emma Garcia | Business | Silver | EY401 (BKK) | EY103 (JFK) |
| PAX-10008 | Michael Martinez | Economy | - | - | - |

**Passenger Summary:**
- Total Passengers: 3 (sample) / ~250 estimated actual
- Connecting FROM EY401: 2 passengers (already disrupted by inbound delay)
- Connecting TO onward flights: 2 passengers at risk

### Downstream Connection Risk at AUH

| Passenger | Connecting To | Scheduled | MCT | Risk |
|-----------|---------------|-----------|-----|------|
| PAX-10006 | EY11 (AUH→LHR) | Various | 90 min | ⚠️ **MISCONNECT** |
| PAX-10007 | EY103 (AUH→JFK) | Various | 90 min | ⚠️ **MISCONNECT** |
| PAX-10009 | EY406 (AUH→BKK) | 16:30 | 90 min | ⚠️ May miss |
| PAX-10010 | EY406 (AUH→BKK) | 16:30 | 90 min | ⚠️ May miss |

## 5. Cargo Impact

### Cargo Manifested on EY402

| Shipment ID | AWB | Type | Weight | Value | Priority |
|-------------|-----|------|--------|-------|----------|
| SHP-70005 | 607-10000005 | General | 1,200 kg | Standard | Standard |
| SHP-70006 | 607-10000006 | **VALUABLE** | 50 kg | High | **Critical** |

**Total Cargo:** 1,250 kg  
**Critical Cargo:** SHP-70006 - Valuable goods requiring secure handling

## 6. Baggage Impact

### Baggage on EY402

| Bag ID | Passenger | Status | Final Dest | Connecting To |
|--------|-----------|--------|------------|---------------|
| BAG-10006 | PAX-10006 (John Brown) | CHECKED_IN | LHR | EY11 |
| BAG-10007 | PAX-10006 (John Brown) | CHECKED_IN | LHR | EY11 |
| BAG-10008 | PAX-10007 (Emma Garcia) | CHECKED_IN | JFK | EY103 |

**Connecting Baggage:** 3 bags require transfer at AUH - will miss connections if delayed 4+ hours.

## 7. Crew Status

**Note:** No crew roster records found for FLT-1006 in current data. Assuming crew positioned in BKK from previous rotation (EY401 crew).

### Available Reserve Crew at BKK

| Reserve ID | Name | Role | Qualification | Available |
|------------|------|------|---------------|-----------|
| RES-5031 | Somchai Prasert | Captain | B787 | 00:00-16:00 |
| RES-5032 | Nattaya Srisawat | First Officer | B787 | 00:00-16:00 |
| RES-5033 | Prasit Chaiyasit | Purser | All Types | 00:00-16:00 |
| RES-5034 | Kannika Wongsawat | Flight Attendant | All Types | 00:00-16:00 |

---

# B. THREE NETWORK CONTROL OPTIONS

## OPTION 1: DELAY AND OPERATE

**Strategy:** Wait for BKK to reopen, operate EY402 with 4-hour delay

### Timeline
```
11:00 UTC │ Scheduled departure - BLOCKED
11:15     │ ► Passenger notification
          │ ► Meal vouchers issued
12:00     │ ► Weather update monitoring
15:00     │ ► BKK reopens
15:30     │ ► Boarding begins
16:00     │ ► EY402 departs (5h delay)
19:30     │ ► EY402 arrives AUH
```

### Cascade Impact
- **EY406 (FLT-1007):** Delayed from 16:30 to ~21:30 (5h delay)
- **EY407 (FLT-1008):** Delayed from 01:00 to ~06:00 (5h delay)

### Pros
- Maintains aircraft rotation integrity
- All passengers eventually transported
- Cargo delivered same day

### Cons
- 5-hour delay affects 250+ passengers
- Cascade delays affect 2 more flights (~500 additional passengers)
- Multiple misconnections at AUH hub

---

## OPTION 2: CANCEL EY402, PROTECT DOWNSTREAM

**Strategy:** Cancel EY402, ferry aircraft from AUH to protect EY406/EY407

### Timeline
```
11:00 UTC │ Scheduled departure - BLOCKED
11:15     │ ► DECISION: Cancel EY402
11:30     │ ► Passenger notification - rebooking begins
12:00     │ ► Ferry flight EY9999 dispatched AUH→BKK (spare aircraft)
15:00     │ ► BKK reopens
18:30     │ ► Ferry arrives BKK
16:30     │ ► EY406 operates on time with spare aircraft
          │ ► EY402 passengers rebooked on EY117 (next BKK→AUH)
```

### Aircraft Swap
- Use A6-BLB or A6-BLD (available B787-9 at AUH)
- Ferry to BKK when airport reopens
- Operate EY406 with spare aircraft

### Pros
- Protects EY406 and EY407 schedules
- Limits cascade to single flight
- Reduces total passenger impact

### Cons
- EY402 passengers fully disrupted
- Ferry flight cost ($45,000)
- Complex rebooking logistics

---

## OPTION 3: AIRCRAFT SWAP + PARTIAL OPERATION

**Strategy:** Swap aircraft, delay EY402 to evening, compress schedule

### Timeline
```
11:00 UTC │ Scheduled departure - BLOCKED
11:15     │ ► Initiate aircraft swap planning
15:00     │ ► BKK reopens
15:30     │ ► A6-BLA (from EY401) available after holding
16:00     │ ► EY402 departs (5h delay)
19:30     │ ► EY402 arrives AUH
21:30     │ ► EY406 departs (5h delay) - compressed turnaround
01:00+1   │ ► EY406 arrives BKK
03:00+1   │ ► EY407 departs (2h delay) - compressed turnaround
06:30+1   │ ► EY407 arrives AUH
```

### Schedule Compression
- Reduce EY406 turnaround from 120 min to 90 min
- Reduce EY407 turnaround from 120 min to 90 min
- Recover 1 hour through compression

### Pros
- No cancellations
- Partial schedule recovery
- All passengers transported

### Cons
- Tight turnarounds increase operational risk
- Ground crew overtime required
- Still significant delays across rotation

---

# C. FINANCIAL IMPACT OF EACH OPTION

## OPTION 1: DELAY AND OPERATE

### Cost Breakdown

| Cost Category | Calculation | Amount (USD) |
|---------------|-------------|--------------|
| **DELAY COSTS** | | |
| EY402 Delay (5h) | 300 min × $100/min | $30,000 |
| EY406 Delay (5h) | 300 min × $100/min | $30,000 |
| EY407 Delay (5h) | 300 min × $100/min | $30,000 |
| **CREW COSTS** | | |
| Crew Overtime (3 flights) | 30 crew × 5h × $75/h | $11,250 |
| **GROUND HANDLING** | | |
| Extended Handling (3 flights) | 3 × 5h × $500/h | $7,500 |
| **PASSENGER CARE** | | |
| Meal Vouchers (EY402) | 250 pax × $25 × 2 | $12,500 |
| Meal Vouchers (EY406) | 250 pax × $25 | $6,250 |
| Meal Vouchers (EY407) | 250 pax × $25 | $6,250 |
| **COMPENSATION** | | |
| UAE CAA (5h delay) | 750 pax × $250 | $187,500 |
| **MISCONNECTIONS** | | |
| Rebooking (est. 100 pax) | 100 × $800 | $80,000 |
| Hotel for misconnects | 100 × $180 | $18,000 |
| **TOTAL HARD COST** | | **$419,250** |
| Soft Cost (2.5×) | | $1,048,125 |
| **TOTAL COST** | | **$1,467,375** |

### Impact Metrics
| Metric | Value |
|--------|-------|
| Flights Affected | 3 |
| Passengers Delayed | ~750 |
| Misconnections | ~100 |
| NPS Impact | -20 points (per flight) |
| Network Propagation | HIGH |

---

## OPTION 2: CANCEL EY402, PROTECT DOWNSTREAM

### Cost Breakdown

| Cost Category | Calculation | Amount (USD) |
|---------------|-------------|--------------|
| **CANCELLATION COSTS** | | |
| EY402 Cancellation (B787) | Fixed | $125,000 |
| **FERRY FLIGHT** | | |
| Ferry AUH→BKK (B787) | Empty positioning | $45,000 |
| Ferry Crew | 2 pilots + expenses | $5,000 |
| **PASSENGER HANDLING** | | |
| Rebooking (OAL) | 100 pax × $800 | $80,000 |
| Rebooking (Own flights) | 150 pax × $400 | $60,000 |
| Hotel Accommodation | 250 pax × $180 | $45,000 |
| Meal Vouchers | 250 pax × $25 × 3 | $18,750 |
| Ground Transport | 250 pax × $50 | $12,500 |
| **COMPENSATION** | | |
| UAE CAA (Cancellation) | 250 pax × $500 | $125,000 |
| **CARGO** | | |
| Cargo Rebooking | 2 shipments × $100 | $200 |
| Valuable Cargo Handling | Special security | $500 |
| **BAGGAGE** | | |
| Baggage Rerouting | 250 bags × $20 | $5,000 |
| **TOTAL HARD COST** | | **$521,950** |
| Soft Cost (2.5×) | | $1,304,875 |
| **TOTAL COST** | | **$1,826,825** |

### Impact Metrics
| Metric | Value |
|--------|-------|
| Flights Cancelled | 1 |
| Flights Protected | 2 (EY406, EY407) |
| Passengers Cancelled | 250 |
| Passengers Protected | ~500 |
| NPS Impact | -35 (cancelled) / 0 (protected) |
| Network Propagation | CONTAINED |

---

## OPTION 3: AIRCRAFT SWAP + SCHEDULE COMPRESSION

### Cost Breakdown

| Cost Category | Calculation | Amount (USD) |
|---------------|-------------|--------------|
| **DELAY COSTS** | | |
| EY402 Delay (5h) | 300 min × $100/min | $30,000 |
| EY406 Delay (5h) | 300 min × $100/min | $30,000 |
| EY407 Delay (2h) | 120 min × $100/min | $12,000 |
| **AIRCRAFT SWAP** | | |
| Swap Coordination | Administrative | $2,000 |
| **CREW COSTS** | | |
| Crew Overtime (3 flights) | 30 crew × 4h avg × $75/h | $9,000 |
| **GROUND HANDLING** | | |
| Extended Handling | 3 × 4h × $500/h | $6,000 |
| Compressed Turnaround Premium | 2 × $2,000 | $4,000 |
| **PASSENGER CARE** | | |
| Meal Vouchers (EY402) | 250 pax × $25 × 2 | $12,500 |
| Meal Vouchers (EY406) | 250 pax × $25 | $6,250 |
| Meal Vouchers (EY407) | 250 pax × $25 | $6,250 |
| **COMPENSATION** | | |
| UAE CAA (EY402 5h) | 250 pax × $250 | $62,500 |
| UAE CAA (EY406 5h) | 250 pax × $250 | $62,500 |
| UAE CAA (EY407 2h) | 0 (under threshold) | $0 |
| **MISCONNECTIONS** | | |
| Rebooking (est. 80 pax) | 80 × $800 | $64,000 |
| Hotel for misconnects | 80 × $180 | $14,400 |
| **TOTAL HARD COST** | | **$321,400** |
| Soft Cost (2.5×) | | $803,500 |
| **TOTAL COST** | | **$1,124,900** |

### Impact Metrics
| Metric | Value |
|--------|-------|
| Flights Affected | 3 |
| Passengers Delayed | ~750 |
| Misconnections | ~80 (reduced) |
| NPS Impact | -18 points avg |
| Network Propagation | MODERATE |
| Schedule Recovery | 1 hour gained |

---

## FINANCIAL COMPARISON SUMMARY

| Option | Hard Cost | Soft Cost | Total Cost | Pax Impact | Recommendation |
|--------|-----------|-----------|------------|------------|----------------|
| **1. Delay All** | $419,250 | $1,048,125 | $1,467,375 | 750 delayed | ⚠️ Simple but costly |
| **2. Cancel + Protect** | $521,950 | $1,304,875 | $1,826,825 | 250 cancelled | ❌ Most expensive |
| **3. Swap + Compress** | $321,400 | $803,500 | **$1,124,900** | 750 delayed | ✅ **RECOMMENDED** |

### Savings Analysis

| Comparison | Savings |
|------------|---------|
| Option 3 vs Option 1 | **$342,475** |
| Option 3 vs Option 2 | **$701,925** |

---

## RECOMMENDED ACTION: OPTION 3

### Decision Rationale
1. **Lowest total cost** ($1,124,900 vs $1.4M-$1.8M alternatives)
2. **No cancellations** - all passengers transported
3. **Schedule recovery** - gains 1 hour through compression
4. **Reduced misconnections** - 80 vs 100 in Option 1
5. **Network stability** - maintains rotation integrity

### Implementation Checklist

| Time | Action | Owner |
|------|--------|-------|
| 11:00 | Confirm BKK closure, initiate delay protocol | Dispatch |
| 11:15 | Notify all EY402 passengers | Customer Service |
| 11:30 | Issue meal vouchers, open lounge | Ground Ops BKK |
| 12:00 | Coordinate compressed turnaround with BKK ground | Hub Control |
| 14:00 | Brief crew on revised schedule | Crew Control |
| 15:00 | Confirm BKK reopening | Dispatch |
| 15:30 | Begin EY402 boarding | Ground Ops |
| 16:00 | EY402 departs | Flight Ops |
| 19:30 | EY402 arrives AUH | Hub Control |
| 19:45 | Begin compressed turnaround for EY406 | Ground Ops AUH |
| 21:15 | EY406 departs (90 min turnaround) | Flight Ops |

### Risk Mitigation
- **Compressed turnaround risk:** Pre-position ground crew, catering, fuel
- **Crew fatigue:** Monitor FDP, have reserve crew on standby
- **Weather uncertainty:** Continuous monitoring, alternate plans ready

---

*Report generated by SkyMarshal AI Recovery System*  
*Data frozen at: January 30, 2026 00:00H UTC+4*
