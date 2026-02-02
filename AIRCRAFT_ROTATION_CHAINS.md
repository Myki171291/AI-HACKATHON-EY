# Aircraft Rotation Chains - Jan 30, 2026 Frozen Baseline

## Overview
Explicit aircraft rotation sequences linking flights for dynamic cascade discovery. Each aircraft maintains a sequence of flights throughout the operational period, enabling system to traverse connections and predict downstream impacts.

---

## Rotation Sequence Map

### Scenario 1: Bangkok Typhoon (FLT-1001 to FLT-1010)

#### Aircraft A6-EYV (A320, 180 pax)
```
Rotation Seq 1: EY334 → EY117 → EY424
├─ EY334: Unknown → AUH (connecting from SIN)
├─ EY117: BKK → AUH (PRIMARY DISRUPTED - Typhoon cannot depart BKK 06:40)
│  └─ Disruption: TYPHOON at BKK
│  └─ Impact: 180 passengers stranded, 4 crew
│  └─ Cascade: Blocks EY424 (downline)
└─ EY424: AUH → SIN (BLOCKED by EY117 delay)
   └─ Impact: 180 passengers, 4 crew cannot depart

Flight Details:
- EY117: FLT-1001, BKK→AUH, Scheduled: 2026-01-30 06:40→10:40
  Gate: B5, Terminal: 3, Crew: 4, Capacity: 180
```

#### Aircraft A6-EYU (A320, 180 pax)
```
Rotation Seq 2: EY25 → EY5293 → EY334
├─ EY25: LHR → AUH (connecting from EY334)
├─ EY5293: AUH → BKK (SECONDARY - LIAC from EY117 delay)
│  └─ Impact: Late inbound aircraft due to EY117→EY424 delay
│  └─ Crew: 4, Capacity: 180 passengers
└─ EY334: CDG → AUH (connecting to EY25)

Flight Details:
- EY5293: FLT-1002, AUH→BKK, Scheduled: 2026-01-30 08:37→17:37
  Gate: B17, Terminal: 3, Crew: 4, Capacity: 180
```

#### Aircraft A6-EYA (A380, 516 pax)
```
Rotation Seq 3: EY313 → EY454 → EY472
├─ EY313: AUH → JED (connecting from EY472)
├─ EY454: AUH → SYD (SECONDARY - Missed connection from EY117)
│  └─ Impact: Passenger connections from EY117 cannot make EY454
│  └─ Crew: 16, Capacity: 516 passengers
└─ EY472: SIN → AUH (connecting for EY313 rotation)

Flight Details:
- EY454: FLT-1003, AUH→SYD, Scheduled: 2026-01-30 10:26→16:26
  Gate: C26, Terminal: 1, Crew: 16, Capacity: 516
```

#### Aircraft A6-EYJ (B787-10, 330 pax)
```
Rotation Seq 4: EY101 → EY334 → EY424
├─ EY101: JFK → AUH (connecting from EY334)
├─ EY334: AUH → CDG (SECONDARY - Missed connection from EY117)
│  └─ Impact: Passengers from EY117→EY424→EY334 cascade
│  └─ Crew: 10, Capacity: 330 passengers
└─ EY424: SIN → AUH (connecting for EY101 rotation)

Flight Details:
- EY334: FLT-1004, AUH→CDG, Scheduled: 2026-01-30 12:48→17:48
  Gate: C9, Terminal: 1, Crew: 10, Capacity: 330
```

---

### Scenario 2: London Fog (FLT-1011 to FLT-1022)

#### Aircraft A6-EYM (B787-10, 330 pax)
```
Rotation Seq 10: EY101 → EY8184 → EY25
├─ EY101: AUH → JFK (connecting from EY8184)
├─ EY8184: AUH → LHR (PRIMARY DISRUPTED - Fog delays arrival)
│  └─ Disruption: FOG at LHR (200m visibility)
│  └─ Impact: 330 passengers, 10 crew, 2+ hour delay
│  └─ Cascade: Blocks EY25 departure slot
└─ EY25: LHR → AUH (BLOCKED - Cannot depart due to arrival fog)
   └─ Impact: 180 passengers, 4 crew cannot depart

Flight Details:
- EY8184: FLT-1010, AUH→LHR, Scheduled: 2026-01-30 08:30→14:30
  Gate: C12, Terminal: 1, Crew: 10, Capacity: 330
```

#### Aircraft A6-EYL (A350, 350 pax)
```
Rotation Seq 11: EY472 → EY6268 → EY19
├─ EY472: AUH → SIN (connecting from EY6268)
├─ EY6268: AUH → LHR (PRIMARY DISRUPTED - Fog delays arrival)
│  └─ Disruption: FOG at LHR (200m visibility)
│  └─ Impact: 350 passengers, 10 crew, 2+ hour delay
└─ EY19: LHR → AUH (BLOCKED - Cannot depart due to arrival fog)
   └─ Impact: 290 passengers, 9 crew cannot depart

Flight Details:
- EY6268: FLT-1011, AUH→LHR, Scheduled: 2026-01-30 10:15→16:15
  Gate: C15, Terminal: 1, Crew: 4, Capacity: 180
```

#### Aircraft A6-EYF (A320, 180 pax)
```
Rotation Seq 9/12: EY334 → EY25 → EY5293
├─ EY334: AUH → CDG (connecting from EY25)
├─ EY25: LHR → AUH (PRIMARY DISRUPTED - Cannot depart due to fog)
│  └─ Disruption: FOG at LHR blocks departure
│  └─ Impact: 180 passengers, 4 crew blocked from departing
│  └─ Cascade: Blocks EY5293 rotation at AUH
└─ EY5293: AUH → BKK (BLOCKED by EY25 LIAC)

Flight Details:
- EY25: FLT-1012, LHR→AUH, Scheduled: 2026-01-31 20:00→2026-02-01 12:00
  Gate: C18, Terminal: 1, Crew: 4, Capacity: 180
```

#### Aircraft A6-EYC (B787-9, 290 pax)
```
Rotation Seq 13: EY6268 → EY19 → EY106
├─ EY6268: AUH → LHR (arrival fog-delayed)
├─ EY19: LHR → AUH (BLOCKED - Cannot depart due to fog)
│  └─ Impact: 290 passengers, 9 crew
└─ EY106: AUH → Unknown (Blocked by EY19 delay)

Flight Details:
- EY19: FLT-1013, LHR→AUH, Scheduled: 2026-01-31 22:00→2026-02-01 14:00
  Gate: C20, Terminal: 1, Crew: 9, Capacity: 290
```

#### Aircraft A6-EYK (B777, 396 pax)
```
Rotation Seq 14: EY454 → EY11 → EY334
├─ EY454: AUH → SYD (connecting from EY11)
├─ EY11: LHR → AUH (PRIMARY DISRUPTED - Cannot depart due to fog)
│  └─ Impact: 396 passengers, 12 crew, critical A380 aircraft
└─ EY334: AUH → CDG (Blocked by EY11 delay)

Flight Details:
- EY11: FLT-1014, LHR→AUH, Scheduled: 2026-02-01 00:00→16:00
  Gate: C22, Terminal: 1, Crew: 12, Capacity: 396
```

---

## Disruption Impact Analysis

### Bangkok Typhoon - Impact Cascade
```
Weather Trigger
      ↓
BKK TYPHOON (is_operational=N)
      ↓
EY117 CANNOT DEPART (Primary)
      ↓
A6-EYV Rotation Blocked
      ├─ EY117: 180 pax, 4 crew STRANDED
      └─ EY424: 180 pax, 4 crew BLOCKED (downline)
      ├─ EY5293: A6-EYU LIAC (SECONDARY)
      │  └─ 180 pax, 4 crew delayed
      ├─ EY454: A6-EYA SECONDARY
      │  └─ 516 pax, 16 crew affected (connections)
      ├─ EY334: A6-EYJ SECONDARY
      │  └─ 330 pax, 10 crew affected (connections)
      └─ ... 6 more secondary flights

TOTAL IMPACT: 10 flights, ~2,700+ affected passengers
```

### London Fog - Impact Cascade
```
Weather Trigger
      ↓
LHR FOG + CDG FOG (is_operational=N)
      ↓
EY8184 + EY6268 ARRIVE DELAYED
      ↓
A6-EYM + A6-EYL Rotation Delayed
      ├─ EY8184: 330 pax, 10 crew DELAYED
      ├─ EY6268: 180 pax, 4 crew DELAYED
      └─ CASCADE to Departures
         ├─ EY25: 180 pax CANNOT DEPART (BLOCKED)
         ├─ EY19: 290 pax CANNOT DEPART (BLOCKED)
         └─ EY11: 396 pax CANNOT DEPART (BLOCKED)
         
Secondary Cascades:
├─ EY26: 180 pax LIAC (from EY25 delay)
├─ EY20: 290 pax LIAC (from EY19 delay)
├─ EY12: 290 pax LIAC (from EY11 delay)
├─ EY334: 330 pax affected
├─ EY1202: 330 pax affected
├─ EY639: 516 pax affected
└─ EY454: 516 pax affected

TOTAL IMPACT: 12 flights, ~3,800+ affected passengers
```

---

## Dynamic Discovery Mechanism

### Flight Connectivity Traversal
```
ALGORITHM: Traverse Flight Dependency Graph
INPUT: Disrupted flight (e.g., EY117)
OUTPUT: All downstream affected flights

1. Find aircraft rotation:
   A6-EYV → [EY334, EY117, EY424]

2. Identify position of disrupted flight:
   Disrupted flight EY117 is at index 1

3. Get downline flights:
   Downline: [EY424] → Check if EY424 depends on EY117 arrival

4. Check passenger connections:
   booking_records where origin_flight=EY117 & connection_flight!=NULL
   → Identify connecting flights that cannot be made

5. Check crew duty continuity:
   crew_roster where duty_flight=EY117 & next_duty_flight!=NULL
   → Identify crew that cannot make next duty

6. Recursively apply algorithm to identified downstream flights:
   For each downstream flight, repeat steps 1-5

7. Aggregate impact:
   Total passengers affected = sum(passengers on disrupted + connected flights)
   Total crew affected = sum(crew on disrupted + connected flights)
   Total flights affected = count of unique flights with disruption
```

### Data Sources for Discovery
- **flights_enriched_scenarios.csv**: Rotation sequences, upline/downline links
- **weather.csv**: Disruption triggers (condition, is_operational)
- **bookings.csv**: Passenger connections (origin_flight, connection_flight)
- **crew_roster_enriched.csv**: Crew duty sequences (duty_flight, next_duty_flight)
- **aircraft_availability_enriched_mel.csv**: Aircraft constraints (MEL status, availability)

---

## Key Properties for Dynamic Discovery

### Required Fields
- **flights_enriched_scenarios.csv**:
  - `aircraft_registration`: Link to aircraft rotations
  - `rotation_sequence`: Order of flights in rotation
  - `upline_flight_number`: Previous flight in rotation
  - `downline_flight_number`: Next flight in rotation

- **weather.csv**:
  - `airport_code`: Trigger location
  - `is_operational`: N = disruption active
  - `condition`: Type of disruption (TYPHOON, FOG, etc.)

- **bookings.csv** (pending update):
  - `passenger_flight`: Origin flight
  - `connection_flight`: Destination after connection
  - `connection_airport`: Where connection occurs

- **crew_roster_enriched.csv** (pending update):
  - `crew_flight`: Current duty flight
  - `next_duty_flight`: Following duty flight
  - `crew_hours_remaining`: Remaining flight duty time

### No Pre-Computed Data
- ❌ No scenario_id (scenarios computed dynamically)
- ❌ No delay_minutes (computed from impact assessment)
- ❌ No is_disrupted flag (computed from weather + connectivity)
- ❌ No downstream_flights list (discovered via traversal)

---

## Testing Procedure

### Test Scenario 1: Bangkok Typhoon
1. **Input**: Inject weather disruption to weather.csv (BKK TYPHOON)
2. **Trigger**: System detects BKK is_operational=N
3. **Discovery**: Find all flights with origin=BKK (EY117)
4. **Cascade**: Traverse A6-EYV rotation → EY424 downline
5. **Connections**: Find passengers booked EY117→EY424
6. **Output**: System returns all 10 affected flights with impact summary

### Test Scenario 2: London Fog
1. **Input**: Inject weather disruption to weather.csv (LHR FOG + CDG FOG)
2. **Trigger**: System detects LHR, CDG is_operational=N
3. **Discovery**: Find all flights with destination=LHR or CDG
4. **Cascades**: 
   - EY8184, EY6268 arrival delays
   - EY25, EY19, EY11 departure blocks
5. **Connections**: Find all booked connections from delayed arrivals
6. **Output**: System returns all 12 affected flights with impact summary

---

**Generated**: Dynamic Cascade Discovery Infrastructure
**Status**: Rotation chains defined for 20 flights across 2 scenarios
**Next**: Update supporting CSV files for passenger/crew connectivity data
