# SkyMarshal Data Relationship Diagram
## Output2 Dataset - Airline Disruption Recovery System

**Frozen Point:** January 30, 2026 00:00H (UTC+4 Abu Dhabi)  
**Purpose:** AI-driven dynamic disruption discovery and recovery optimization

---

## Entity Relationship Diagram (Mermaid)

```mermaid
erDiagram
    FLIGHTS ||--o{ PASSENGERS : "carries"
    FLIGHTS ||--o{ CARGO : "transports"
    FLIGHTS ||--o{ BAGGAGE : "holds"
    FLIGHTS ||--o{ CREW_ROSTER : "staffed_by"
    FLIGHTS }o--|| AIRCRAFT : "operated_by"
    FLIGHTS }o--|| WEATHER : "affected_by"
    FLIGHTS ||--o| FLIGHTS : "rotation_chain"
    
    PASSENGERS ||--o{ BAGGAGE : "owns"
    PASSENGERS }o--o| PASSENGERS : "connecting_from"
    
    AIRCRAFT ||--o{ FLIGHTS : "operates"
    
    CREW_ROSTER }o--|| RESERVE_CREW : "replaced_by"
    
    WEATHER }o--|| AIRPORT_SLOTS : "impacts"
    WEATHER }o--|| AIRPORT_CURFEWS : "triggers"
    
    FLIGHTS {
        string flight_id PK
        string flight_number
        string aircraft_registration FK
        string origin
        string destination
        datetime scheduled_departure_utc
        datetime scheduled_arrival_utc
        string prev_flight_in_rotation FK
        string next_flight_in_rotation FK
    }
    
    AIRCRAFT {
        string aircraft_registration PK
        string aircraft_type
        string status
        string location
        int passenger_capacity
        string mel_status
    }
    
    PASSENGERS {
        string passenger_id PK
        string flight_id FK
        string pnr
        string cabin_class
        string frequent_flyer_tier
        string connecting_from_flight FK
    }
    
    CREW_ROSTER {
        string roster_id PK
        string flight_id FK
        string employee_id
        string role
        float duty_hours
        float max_fdp_hours
        boolean fdp_exceeded
    }
    
    RESERVE_CREW {
        string reserve_id PK
        string employee_id
        string role
        string base
        string qualifications
        datetime available_from_utc
        datetime available_until_utc
    }
    
    CARGO {
        string shipment_id PK
        string flight_id FK
        string cargo_type
        float weight_kg
        boolean is_temperature_sensitive
        string priority
    }
    
    BAGGAGE {
        string baggage_id PK
        string passenger_id FK
        string flight_id FK
        string status
        boolean is_connecting
        string connecting_flight FK
    }
    
    WEATHER {
        string weather_id PK
        string airport_code
        datetime observation_time_utc
        string condition
        boolean is_operational
    }
    
    AIRPORT_SLOTS {
        string slot_id PK
        string airport_code
        datetime slot_time_utc
        int available_slots
        boolean is_congested
    }
    
    AIRPORT_CURFEWS {
        string curfew_id PK
        string airport_code
        time curfew_start_local
        time curfew_end_local
        boolean is_active
    }
```

---

## Data Flow Diagram

```mermaid
flowchart TB
    subgraph DISRUPTION_SEEDS["🌪️ Disruption Seeds"]
        WX[weather.csv]
    end
    
    subgraph CORE_OPERATIONS["✈️ Core Operations"]
        FLT[flights.csv]
        ACF[aircraft.csv]
        CRW[crew_roster.csv]
        RES[reserve_crew.csv]
    end
    
    subgraph CUSTOMER_DATA["👥 Customer Data"]
        PAX[passengers.csv]
        BAG[baggage.csv]
        CGO[cargo.csv]
    end
    
    subgraph CONSTRAINTS["⚠️ Constraints & Rules"]
        SLT[airport_slots.csv]
        CRF[airport_curfews.csv]
        MCT[minimum_connection_times.csv]
        SAF[safety_constraints.csv]
        BGR[baggage_rules.csv]
    end
    
    subgraph FINANCIAL["💰 Financial Parameters"]
        FIN[financial_parameters.csv]
        RCM[recovery_cost_matrix.csv]
        CMP[compensation_rules.csv]
    end
    
    subgraph REPORTS["📊 Disruption Reports"]
        EY117[EY117_DISRUPTION_REPORT.md]
        EY402[EY402_DISRUPTION_REPORT.md]
    end
    
    WX -->|"triggers"| FLT
    WX -->|"closes"| SLT
    
    FLT -->|"uses"| ACF
    FLT -->|"staffed by"| CRW
    FLT -->|"carries"| PAX
    FLT -->|"transports"| CGO
    FLT -->|"holds"| BAG
    
    CRW -->|"replaced by"| RES
    
    PAX -->|"owns"| BAG
    PAX -->|"connects via"| MCT
    
    FLT -->|"constrained by"| SLT
    FLT -->|"limited by"| CRF
    FLT -->|"must follow"| SAF
    
    BAG -->|"follows"| BGR
    
    FLT -->|"costs from"| FIN
    FLT -->|"recovery via"| RCM
    PAX -->|"compensated per"| CMP
    
    FLT -->|"analyzed in"| EY117
    FLT -->|"analyzed in"| EY402
```

---

## Key Relationships Summary

| Primary Entity | Related Entity | Relationship | Join Key |
|----------------|----------------|--------------|----------|
| flights | aircraft | Many-to-One | aircraft_registration |
| flights | flights | Self-reference | prev/next_flight_in_rotation |
| flights | weather | Many-to-One | origin/destination ↔ airport_code |
| passengers | flights | Many-to-One | flight_id |
| passengers | passengers | Self-reference | connecting_from_flight |
| baggage | passengers | Many-to-One | passenger_id |
| baggage | flights | Many-to-One | flight_id |
| cargo | flights | Many-to-One | flight_id |
| crew_roster | flights | Many-to-One | flight_id |
| reserve_crew | crew_roster | Replacement | base, qualifications |
| airport_slots | weather | Impacted by | airport_code |
| airport_curfews | flights | Constrains | airport_code |

---

## Disruption Discovery Flow

```mermaid
sequenceDiagram
    participant AI as AI Agent
    participant WX as weather.csv
    participant FLT as flights.csv
    participant PAX as passengers.csv
    participant FIN as financial_parameters.csv
    participant RPT as Disruption Report
    
    AI->>WX: Query weather conditions
    WX-->>AI: BKK TYPHOON 06:00-15:00 UTC
    
    AI->>FLT: Find affected flights
    FLT-->>AI: EY117 (08:00), EY402 (11:00) blocked
    
    AI->>FLT: Check rotation chains
    FLT-->>AI: A6-BLA: EY401→EY402→EY406→EY407
    
    AI->>PAX: Identify affected passengers
    PAX-->>AI: 250+ pax, connections at risk
    
    AI->>FIN: Calculate recovery costs
    FIN-->>AI: Delay=$581K, Cancel=$1.69M
    
    AI->>RPT: Generate recommendation
    RPT-->>AI: DELAY AND OPERATE (saves $1.1M)
```

---

## File Inventory

| File | Records | Primary Key | Description |
|------|---------|-------------|-------------|
| flights.csv | 87 | flight_id | Flight schedule with rotation links |
| aircraft.csv | 20 | aircraft_registration | Fleet with MEL status |
| passengers.csv | 100 | passenger_id | Passenger manifest with connections |
| crew_roster.csv | 42 | roster_id | Crew assignments with FDP tracking |
| reserve_crew.csv | 34 | reserve_id | Standby crew pool |
| cargo.csv | 80 | shipment_id | Cargo manifest with temp requirements |
| baggage.csv | 65 | baggage_id | Baggage tracking with transfers |
| weather.csv | 86 | weather_id | Weather observations (disruption seeds) |
| airport_slots.csv | 83 | slot_id | Slot availability |
| airport_curfews.csv | 4 | curfew_id | Night curfew rules |
| minimum_connection_times.csv | 52 | mct_id | MCT by airport/connection type |
| financial_parameters.csv | 100 | parameter_id | Cost parameters |
| recovery_cost_matrix.csv | 58 | matrix_id | Recovery option costs |
| compensation_rules.csv | 40 | rule_id | EU261/DOT/UAE compensation |
| safety_constraints.csv | 70 | constraint_id | Regulatory safety rules |
| baggage_rules.csv | 40 | rule_id | Baggage handling rules |

---

## Weather Disruption Seeds (Jan 30, 2026)

| Airport | Condition | Window (UTC) | Impact |
|---------|-----------|--------------|--------|
| **BKK** | TYPHOON | 06:00-15:00 | Airport CLOSED |
| **LHR** | FOG | 06:00-12:00 | Airport CLOSED |
| **CDG** | SNOW_STORM | 06:00-15:00 | Airport CLOSED |
| **SIN** | THUNDERSTORM | 12:00-18:00 | Operational but degraded |
| **AUH** | SANDSTORM | 09:00-15:00 | Operational but degraded |

---

*Generated for SkyMarshal AI Recovery System*  
*Data frozen at: January 30, 2026 00:00H UTC+4*