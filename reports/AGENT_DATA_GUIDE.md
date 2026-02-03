# SkyMarshal Agent Data Guide

## Overview
This document describes how the 7 SkyMarshal agents communicate via shared datasets and which datasets each agent should use.

**Key Guarantee**: All 7 agents have complete data for ALL 11 scenarios. No agent should ever say "scenario data not available".

---

## Agent-Dataset Mapping

### 1. Flight Operations Agent
**Purpose**: Manages flight schedules, delays, cancellations, aircraft swaps

| Dataset | Type | Rows | Link Fields |
|---------|------|------|-------------|
| flights_enriched_scenarios.csv | Primary | 117 | flight_id, scenario_id |
| aircraft_availability_enriched_mel.csv | Primary | 242 | aircraft_registration, scenario_id |
| aircraft_swap_options.csv | Primary | 272 | flight_id, scenario_id |
| weather.csv | Primary | 65 | scenario_id |
| disruption_events.csv | Primary | 11 | scenario_id |
| airport_slots.csv | Secondary | 2772 | scenario_id |
| airport_curfews.csv | Secondary | 44 | scenario_id |
| minimum_connection_times.csv | Secondary | 616 | scenario_id |

**Key Queries**:
- Which flights are delayed/cancelled?
- What aircraft are available for swap?
- What is the weather impact?
- What are the slot constraints?

---

### 2. Passenger Services Agent
**Purpose**: Handles passenger rebooking, compensation, special needs

| Dataset | Type | Rows | Link Fields |
|---------|------|------|-------------|
| passengers_enriched_final.csv | Primary | 11,700 | passenger_id, flight_id, scenario_id |
| bookings.csv | Primary | 11,700 | booking_id, flight_id, pnr, scenario_id |
| oal_rebooking_options.csv | Primary | 316 | scenario_id |
| flights_enriched_scenarios.csv | Secondary | 117 | flight_id, scenario_id |
| financial_transactions.csv | Secondary | 16,563 | booking_id, flight_id, scenario_id |
| disruption_costs.csv | Secondary | 121 | scenario_id |

**Key Queries**:
- Which passengers are affected?
- What rebooking options exist?
- Who needs special assistance?
- What compensation is due?

---

### 3. Crew Management Agent
**Purpose**: Manages crew assignments, duty hours, qualifications

| Dataset | Type | Rows | Link Fields |
|---------|------|------|-------------|
| crew_roster_enriched.csv | Primary | 1,204 | crew_id, flight_id, scenario_id |
| reserve_crew_pool.csv | Primary | 220 | crew_id, scenario_id |
| flights_enriched_scenarios.csv | Secondary | 117 | flight_id, scenario_id |
| safety_constraints.csv | Secondary | 66 | scenario_id |

**Key Queries**:
- Which crew are available?
- Who is approaching duty limits?
- What qualifications are needed?
- Who can be called from reserve?

---

### 4. Maintenance Agent
**Purpose**: Handles aircraft maintenance, MEL items, AOG situations

| Dataset | Type | Rows | Link Fields |
|---------|------|------|-------------|
| aircraft_maintenance_workorders.csv | Primary | 60 | workorder_id, aircraft_registration, scenario_id |
| aircraft_availability_enriched_mel.csv | Primary | 242 | aircraft_registration, scenario_id |
| maintenance_staff.csv | Primary | 330 | staff_id, scenario_id |
| flights_enriched_scenarios.csv | Secondary | 117 | flight_id, aircraft_registration |
| aircraft_swap_options.csv | Secondary | 272 | aircraft_registration, scenario_id |

**Key Queries**:
- Which aircraft have MEL items?
- What maintenance is pending?
- Which aircraft are AOG?
- What staff are available?

---

### 5. Cargo Agent
**Purpose**: Manages cargo shipments, dangerous goods, temperature-sensitive items

| Dataset | Type | Rows | Link Fields |
|---------|------|------|-------------|
| cargo_shipments.csv | Primary | 1,419 | shipment_id, flight_id, scenario_id |
| flights_enriched_scenarios.csv | Secondary | 117 | flight_id, scenario_id |
| aircraft_availability_enriched_mel.csv | Secondary | 242 | aircraft_registration, scenario_id |

**Key Queries**:
- What cargo is affected?
- Any dangerous goods impacted?
- Temperature-sensitive shipments?
- Cargo rebooking options?

---

### 6. Recovery Planning Agent
**Purpose**: Coordinates overall recovery, prioritizes actions, tracks progress

| Dataset | Type | Rows | Link Fields |
|---------|------|------|-------------|
| recovery_scenarios.csv | Primary | 44 | scenario_id |
| disruption_events.csv | Primary | 11 | event_id, scenario_id |
| financial_impact.csv | Primary | 11 | scenario_id |
| disruption_costs.csv | Primary | 121 | disruption_id, scenario_id |
| flights_enriched_scenarios.csv | Secondary | 117 | flight_id, scenario_id |
| passengers_enriched_final.csv | Secondary | 11,700 | passenger_id, scenario_id |
| aircraft_swap_options.csv | Secondary | 272 | scenario_id |
| oal_rebooking_options.csv | Secondary | 316 | scenario_id |

**Key Queries**:
- What is the recovery plan?
- What is the financial impact?
- What actions are prioritized?
- What is the recovery status?

---

### 7. Safety & Compliance Agent
**Purpose**: Ensures regulatory compliance, safety constraints, duty limits

| Dataset | Type | Rows | Link Fields |
|---------|------|------|-------------|
| safety_constraints.csv | Primary | 66 | scenario_id |
| crew_roster_enriched.csv | Primary | 1,204 | crew_id, scenario_id |
| flights_enriched_scenarios.csv | Secondary | 117 | flight_id, scenario_id |
| airport_curfews.csv | Secondary | 44 | scenario_id |
| minimum_connection_times.csv | Secondary | 616 | scenario_id |

**Key Queries**:
- Any safety violations?
- Crew duty limit breaches?
- Regulatory constraints?
- Curfew violations?

---

## Agent Communication Flow

```
                    DISRUPTION EVENT
                    (disruption_events.csv)
                            │
                            ▼
                ┌───────────────────────┐
                │  FLIGHT OPERATIONS    │
                │  AGENT                │
                │  (flights, aircraft,  │
                │   weather, slots)     │
                └───────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  PASSENGER    │   │  CREW         │   │  MAINTENANCE  │
│  SERVICES     │   │  MANAGEMENT   │   │  AGENT        │
│  (passengers, │   │  (crew_roster,│   │  (workorders, │
│   bookings)   │   │   reserve)    │   │   staff)      │
└───────────────┘   └───────────────┘   └───────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                ┌───────────────────────┐
                │  CARGO AGENT          │
                │  (cargo_shipments)    │
                └───────────────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │  RECOVERY PLANNING    │
                │  AGENT                │
                │  (recovery_scenarios, │
                │   financial_impact)   │
                └───────────────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │  SAFETY & COMPLIANCE  │
                │  AGENT                │
                │  (safety_constraints) │
                └───────────────────────┘
```

---

## Key Link Fields

All datasets are linked via these common fields:

| Field | Description | Used By |
|-------|-------------|---------|
| `scenario_id` | Links all data to specific disruption scenario (1-11) | ALL datasets |
| `flight_id` | Unique flight identifier (e.g., FLT-1001) | flights, passengers, bookings, cargo, crew |
| `flight_number` | Flight number (e.g., EY401) | flights, bookings, cargo, crew |
| `aircraft_registration` | Aircraft tail number (e.g., A6-BLA) | flights, aircraft_availability, maintenance |
| `passenger_id` | Unique passenger identifier | passengers, bookings |
| `booking_id` | Unique booking identifier | bookings, financial_transactions |
| `crew_id` | Unique crew member identifier | crew_roster, reserve_crew_pool |
| `pnr` | Passenger Name Record | bookings, passengers |

---

## 11 Scenarios Summary

| # | Scenario | Date | Flights | Passengers |
|---|----------|------|---------|------------|
| 1 | Bangkok Typhoon + Critical MEL Aircraft | 2026-01-19 | 10 | 1,000 |
| 2 | London Fog + Multiple Aircraft AOG | 2026-01-20 | 12 | 1,200 |
| 3 | Singapore Thunderstorms + MEL Expiry | 2026-01-21 | 8 | 800 |
| 4 | Paris Winter Storm + Cargo Crisis | 2026-01-22 | 8 | 800 |
| 5 | Dubai Sandstorm + Hub Congestion | 2026-01-23 | 14 | 1,400 |
| 6 | Multiple Aircraft AOG + Engine Failure | 2026-01-24 | 8 | 800 |
| 7 | Crew Out of Hours + Cabin Crew Crisis | 2026-01-25 | 10 | 1,000 |
| 8 | Runway Closure + Airspace Restrictions | 2026-01-27 | 14 | 1,400 |
| 9 | Security Threat + Airspace Diversion | 2026-01-28 | 20 | 2,000 |
| 10 | Medical Emergency + Tarmac Delay | 2026-01-29 | 3 | 300 |
| 11 | EY401 Typhoon → EY406 LIAC | 2026-01-31 | 10 | 1,000 |

---

## Validation Commands

Run these to verify data completeness:

```bash
# Full validation (all files, all scenarios, all agents)
py validate_all_files_complete.py

# Agent-scenario coverage validation
py validate_agent_scenario_coverage.py
```

---

## Data Files Summary (21 files)

| File | Rows | Columns | Scenarios |
|------|------|---------|-----------|
| flights_enriched_scenarios.csv | 117 | 49 | 11 ✅ |
| passengers_enriched_final.csv | 11,700 | 58 | 11 ✅ |
| bookings.csv | 11,700 | 16 | 11 ✅ |
| crew_roster_enriched.csv | 1,204 | 45 | 11 ✅ |
| cargo_shipments.csv | 1,419 | 22 | 11 ✅ |
| aircraft_availability_enriched_mel.csv | 242 | 16 | 11 ✅ |
| aircraft_maintenance_workorders.csv | 60 | 33 | 11 ✅ |
| aircraft_swap_options.csv | 272 | 17 | 11 ✅ |
| weather.csv | 65 | 17 | 11 ✅ |
| disruption_events.csv | 11 | 18 | 11 ✅ |
| recovery_scenarios.csv | 44 | 30 | 11 ✅ |
| safety_constraints.csv | 66 | 11 | 11 ✅ |
| maintenance_staff.csv | 330 | 15 | 11 ✅ |
| reserve_crew_pool.csv | 220 | 15 | 11 ✅ |
| oal_rebooking_options.csv | 316 | 18 | 11 ✅ |
| airport_slots.csv | 2,772 | 12 | 11 ✅ |
| airport_curfews.csv | 44 | 11 | 11 ✅ |
| minimum_connection_times.csv | 616 | 10 | 11 ✅ |
| financial_impact.csv | 11 | 17 | 11 ✅ |
| financial_transactions.csv | 16,563 | 18 | 11 ✅ |
| disruption_costs.csv | 121 | 16 | 11 ✅ |

**Total Records**: 47,893
