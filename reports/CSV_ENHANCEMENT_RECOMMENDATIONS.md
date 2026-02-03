# CSV FILE ENHANCEMENT RECOMMENDATIONS
## Mapping Missing Industry Standard Parameters to Data Files

**Date**: February 3, 2026  
**Purpose**: Guide CSV enrichment to support comprehensive disruption analysis  
**Target**: All 21 CSV files (1 new file recommended)

---

## CATEGORY 1: MAINTENANCE TRACKING PARAMETERS

### Affected Files: 
- **aircraft_maintenance_workorders.csv** (PRIMARY)
- **aircraft_availability_enriched_mel.csv** (SECONDARY)

### Current Columns:
```
workorder_id, aircraft_registration, aircraft_type, maintenance_type, status, 
scheduled_start, scheduled_end, actual_start, actual_end, estimated_duration_hours, 
priority, location, assigned_technician_id
```

### **RECOMMENDED ADDITIONS to aircraft_maintenance_workorders.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **maintenance_category** | VARCHAR | Planned vs Unplanned | PLANNED, UNPLANNED, CORRECTIVE |
| **is_repeat_issue** | BOOLEAN | Repeat fault tracking | TRUE, FALSE |
| **component_name** | VARCHAR | System being serviced | Hydraulic_System_A, Engine_1_Compressor |
| **component_service_hours** | INTEGER | Component life usage | 8450 (hours since new) |
| **component_service_cycles** | INTEGER | Component cycle count | 12320 (flight cycles) |
| **mtbf_hours** | INTEGER | Mean Time Between Failures | 4500 (expected hours) |
| **reliability_score** | DECIMAL | Component reliability % | 0.94 (94% reliability) |
| **predictive_alert** | VARCHAR | Any pre-warning signs | VIBRATION_DETECTED, TEMP_SPIKE, NONE |
| **predictive_alert_severity** | VARCHAR | Alert risk level | CRITICAL, HIGH, MEDIUM, LOW |
| **maintenance_history_count** | INTEGER | Previous repairs on component | 3 (3 prior repairs) |

### **Sample Enhanced Row:**
```
MWO-A6-EYM-001,A6-EYM,A350,CORRECTIVE,IN_PROGRESS,2026-01-30 05:45,2026-01-30 08:45,
2026-01-30 05:45,NULL,3,CRITICAL,AUH,TECH-002,UNPLANNED,TRUE,Hydraulic_System_A,
8920,11580,4500,0.91,PRESSURE_SPIKE_DETECTED,CRITICAL,2
```

### **RECOMMENDED ADDITIONS to aircraft_availability_enriched_mel.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **last_major_inspection_date** | DATE | Last C-check or overhaul | 2025-09-15 |
| **next_major_inspection_due** | DATE | Scheduled next major inspection | 2026-03-15 |
| **hours_since_last_inspection** | INTEGER | Operating hours since inspection | 1240 |
| **hydraulic_system_health** | VARCHAR | Hydraulic system status | NORMAL, DEGRADED, AT_RISK |
| **engine_health_status** | VARCHAR | Engine condition | EXCELLENT, GOOD, FAIR, POOR |
| **structural_inspection_status** | VARCHAR | Airframe integrity | NO_ISSUES, MINOR_CRACKS, FATIGUE_RISK |
| **repeat_fault_history** | TEXT | List of recurring issues | Hydraulic_pressure_variance; Wheel_bearing_wear |

---

## CATEGORY 2: DETAILED REPAIR LOGISTICS PARAMETERS

### Affected Files:
- **NEW FILE RECOMMENDED**: `maintenance_facilities_repair_logistics.csv`
- **aircraft_maintenance_workorders.csv** (ENHANCED)

### **NEW FILE: maintenance_facilities_repair_logistics.csv**

**Columns**:
```
facility_id, facility_name, airport_code, facility_type, max_concurrent_repairs, 
shift_coverage_type, operating_hours_daily, spare_parts_warehouse_distance_km, 
spare_parts_availability_pct, engineering_support_available, external_vendor_required,
vendor_name, vendor_contact_hours, vendor_approval_time_hours, quality_control_sampling,
repair_start_to_completion_avg_hours, labor_cost_per_hour, equipment_cost_per_job
```

**Sample Data**:
```
FACILITY-AUH-001,Abu Dhabi Maintenance Center,AUH,AIRCRAFT_HANGAR,4,24_HOUR_COVERAGE,24,
0.5,0.98,TRUE,FALSE,NULL,NULL,NULL,TRUE,3.5,350,2500

FACILITY-AUH-002,Etihad Maintenance Hangar B19,AUH,LINE_MAINTENANCE,8,24_HOUR_COVERAGE,24,
0.2,0.95,TRUE,TRUE,Liebherr_Aerospace,24/7,4,TRUE,2.5,280,1800

FACILITY-SIN-001,Singapore Changi Maintenance,SIN,AIRCRAFT_HANGAR,3,16_HOUR_COVERAGE,16,
1.2,0.92,TRUE,TRUE,Rolls_Royce_Support,08:00-20:00,8,TRUE,5.5,420,3200
```

### **RECOMMENDED ADDITIONS to aircraft_maintenance_workorders.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **facility_id** | VARCHAR | Which maintenance facility | FACILITY-AUH-001 |
| **parts_warehouse_distance_km** | DECIMAL | Distance to spare parts | 0.5 |
| **parts_availability_pct** | DECIMAL | Spare parts stock level | 0.98 (98% in stock) |
| **external_vendor_required** | BOOLEAN | Third-party approval needed | TRUE |
| **vendor_name** | VARCHAR | External vendor company | Liebherr_Aerospace |
| **vendor_approval_time_hours** | INTEGER | Vendor review time | 4 |
| **qc_sampling_required** | BOOLEAN | Quality control inspection | TRUE |
| **qc_sampling_time_hours** | DECIMAL | QC inspection duration | 1.5 |
| **estimated_actual_duration_hours** | DECIMAL | Realistic completion time | 3.75 |

---

## CATEGORY 3: ENVIRONMENTAL/SUSTAINABILITY PARAMETERS

### Affected Files:
- **NEW FILE RECOMMENDED**: `sustainability_impact_metrics.csv`
- **financial_impact.csv** (ENHANCED)
- **recovery_scenarios.csv** (ENHANCED)

### **NEW FILE: sustainability_impact_metrics.csv**

**Columns**:
```
metric_id, flight_number, disruption_scenario, fuel_consumption_kg, 
carbon_emission_kg_co2, gate_hold_duration_min, repositioning_distance_km,
repositioning_fuel_kg, repositioning_emissions_kg_co2, rebooking_detour_km,
rebooking_extra_fuel_kg, rebooking_extra_emissions_kg_co2, total_disruption_emissions_kg_co2,
offset_cost_usd, sustainability_impact_rating
```

**Sample Data**:
```
SUST-EY117-001,EY117,BANGKOK_TYPHOON,0,0,1440,0,0,0,0,0,0,0,0,CANCELLED_NO_FLIGHT

SUST-EY402-001,EY402,BANGKOK_TYPHOON,8500,25650,240,450,2150,6500,180,850,2550,35700,1785,HIGH_IMPACT

SUST-EY5293-001,EY5293,BANGKOK_TYPHOON,9200,27700,180,800,3400,10200,220,1050,3150,41050,2052,HIGH_IMPACT
```

### **RECOMMENDED ADDITIONS to financial_impact.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **sustainability_cost_usd** | DECIMAL | Carbon offset cost | 1,785 |
| **sustainability_cost_aed** | DECIMAL | Carbon offset (AED) | 6,553 |
| **environmental_rating** | VARCHAR | Impact severity | HIGH, MEDIUM, LOW |
| **total_cost_including_sustainability** | DECIMAL | Full cost with ESG | 85,000 + 1,785 |

---

## CATEGORY 4: NETWORK ANALYSIS PARAMETERS

### Affected Files:
- **flights_enriched_scenarios.csv** (ENHANCED)
- **airport_slots.csv** (ENHANCED)
- **NEW FILE RECOMMENDED**: `partner_airline_capacity.csv`
- **recovery_scenarios.csv** (ENHANCED)

### **RECOMMENDED ADDITIONS to flights_enriched_scenarios.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **alternative_route_1** | VARCHAR | Primary alternative routing | AUH→SIN→BKK |
| **alternative_route_1_distance_km** | INTEGER | Distance increase | 850 |
| **alternative_route_1_extra_time_hours** | DECIMAL | Time penalty | 1.5 |
| **alternative_route_2** | VARCHAR | Secondary routing | AUH→KUL→BKK |
| **alternative_route_2_distance_km** | INTEGER | Distance increase | 1200 |
| **hub_concentration_risk** | VARCHAR | Hub dependency level | HIGH, MEDIUM, LOW |
| **schedule_reliability_pct** | DECIMAL | Historical on-time % | 0.94 (94% on-time) |
| **affected_by_hub_disruption** | BOOLEAN | Vulnerable to hub issues | TRUE |

### **NEW FILE: partner_airline_capacity.csv**

**Columns**:
```
capacity_id, origin_airport, destination_airport, partner_airline_code, 
available_seats_today, available_seats_next_7_days, codeshare_available,
interline_agreement_active, priority_booking_level, booking_cost_markup_pct,
booking_lead_time_required_hours, can_carry_pax_baggage, pet_policy
```

**Sample Data**:
```
CAP-AUH-BKK-SQ,AUH,BKK,SQ,0,45,TRUE,TRUE,STANDARD,15,2,TRUE,TRUE
CAP-AUH-BKK-BA,AUH,BKK,BA,0,28,FALSE,TRUE,STANDARD,20,4,TRUE,FALSE
CAP-AUH-BKK-TG,AUH,BKK,TG,0,35,FALSE,TRUE,PREMIUM,25,6,TRUE,TRUE
```

### **RECOMMENDED ADDITIONS to airport_slots.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **arrival_slot_recovery_options** | INTEGER | Available recovery slots next 24h | 3 |
| **congestion_level** | VARCHAR | Airport traffic density | HIGH, MEDIUM, LOW |
| **hub_risk_concentration** | DECIMAL | % of network through this hub | 0.28 (28% network concentration) |
| **alternative_airport_code** | VARCHAR | Diversion airport option | SIN, KUL |
| **alternative_airport_distance_km** | INTEGER | Distance to alternate | 750 |

---

## CATEGORY 5: PASSENGER COMMUNICATION PARAMETERS

### Affected Files:
- **passengers_enriched_final.csv** (ENHANCED)
- **NEW FILE RECOMMENDED**: `passenger_communication_preferences.csv`
- **bookings.csv** (ENHANCED)

### **RECOMMENDED ADDITIONS to passengers_enriched_final.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **preferred_contact_method** | VARCHAR | SMS, Email, Phone | EMAIL |
| **languages_spoken** | VARCHAR | Comma-separated list | ENGLISH,ARABIC,FRENCH |
| **preferred_language_for_communications** | VARCHAR | Primary communication language | ENGLISH |
| **accessibility_requirements** | VARCHAR | Special needs | WHEELCHAIR, HEARING_AID, NONE |
| **vip_status** | VARCHAR | Frequent flyer tier | PLATINUM, GOLD, SILVER, BRONZE |
| **email_address** | VARCHAR | Email for notifications | ali.mansouri@email.com |
| **phone_number_country_code** | VARCHAR | Country dialing code | +971 |

### **NEW FILE: passenger_communication_preferences.csv**

**Columns**:
```
preference_id, flight_number, disruption_type, notification_timestamp,
notification_method, message_language, passenger_response_time_minutes,
passenger_feedback_sentiment, rebooking_choice_made, choice_timestamp,
communication_clarity_rating, satisfaction_with_communication_pct
```

**Sample Data**:
```
PREF-EY117-001,EY117,WEATHER_DISRUPTION,2026-01-30 06:15:00,SMS,ENGLISH,12,
FRUSTRATED,YES,2026-01-30 06:27:00,3.5,65

PREF-EY117-002,EY117,WEATHER_DISRUPTION,2026-01-30 06:15:00,EMAIL,ARABIC,45,
UNDERSTANDING,YES,2026-01-30 07:00:00,4.2,78
```

### **RECOMMENDED ADDITIONS to bookings.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **contact_email** | VARCHAR | Passenger email | passenger@email.com |
| **contact_phone** | VARCHAR | Passenger phone | +971501234567 |
| **sms_opt_in** | BOOLEAN | Agreed to SMS updates | TRUE |
| **email_opt_in** | BOOLEAN | Agreed to email updates | TRUE |
| **language_preference** | VARCHAR | Communication language | ENGLISH |

---

## CATEGORY 6: SLOT & SCHEDULE MANAGEMENT PARAMETERS

### Affected Files:
- **airport_slots.csv** (ENHANCED)
- **minimum_connection_times.csv** (ENHANCED)
- **airport_curfews.csv** (ENHANCED)

### **RECOMMENDED ADDITIONS to airport_slots.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **arrival_slot_recovery_24h_count** | INTEGER | Recovery slots available | 5 |
| **arrival_slot_recovery_48h_count** | INTEGER | Recovery slots 48 hours out | 12 |
| **congestion_index** | DECIMAL | Aerodrome utilization % | 0.87 (87% busy) |
| **minimum_ground_time_required_minutes** | INTEGER | Minimum handling time | 45 |
| **maximum_ground_hold_time_minutes** | INTEGER | Max gate hold allowed | 240 |
| **slot_flexibility_rating** | VARCHAR | Can slot be adjusted | FLEXIBLE, RIGID, SEMI_FLEXIBLE |

### **RECOMMENDED ADDITIONS to minimum_connection_times.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **optimized_time_flexibility_minutes** | INTEGER | Can reduce by this much | 10 |
| **maximum_allowable_time_minutes** | INTEGER | Can extend by this much | 30 |
| **high_risk_missed_connection_pct** | DECIMAL | Historical miss rate | 0.05 (5% miss rate) |
| **special_equipment_required** | VARCHAR | Equipment for connection | WHEELCHAIR, TRANSFER_BUS |

### **RECOMMENDED ADDITIONS to airport_curfews.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **curfew_flexibility** | VARCHAR | Can be adjusted | FIRM, FLEXIBLE |
| **noise_restriction_hours** | VARCHAR | Restricted flight windows | 23:00-06:00 |
| **departure_slot_impact** | VARCHAR | Affects which flights | DEPARTURES_ONLY, ALL_OPERATIONS |
| **arrival_slot_availability** | INTEGER | Available arrival slots | 8 |

---

## CATEGORY 7: QUALITY METRICS & KPIs

### Affected Files:
- **recovery_scenarios.csv** (ENHANCED)
- **NEW FILE RECOMMENDED**: `kpi_tracking_metrics.csv`

### **RECOMMENDED ADDITIONS to recovery_scenarios.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **schedule_reliability_pct** | DECIMAL | On-time performance during recovery | 0.92 (92%) |
| **nps_score** | INTEGER | Net Promoter Score after disruption | 42 |
| **customer_satisfaction_pct** | DECIMAL | % satisfied with handling | 0.78 (78%) |
| **revenue_recovery_pct** | DECIMAL | % of normal revenue recovered | 0.85 (85%) |
| **operational_recovery_hours** | DECIMAL | Hours to full normal operations | 24.5 |
| **repeat_incident_risk_pct** | DECIMAL | Risk of similar disruption | 0.08 (8%) |
| **cost_per_passenger_aed** | DECIMAL | Disruption cost per pax | 445 |

### **NEW FILE: kpi_tracking_metrics.csv**

**Columns**:
```
kpi_id, disruption_id, kpi_name, kpi_category, target_value, actual_value,
performance_status, measurement_date, trend_direction, root_cause_if_missed,
improvement_action, owner_department
```

**Sample Data**:
```
KPI-EY117-001,DISRUPT-WEATHER-001,Schedule_Reliability,%,95,78,MISS,2026-01-31,DOWN,
Weather_Beyond_Control,Improve_Forecast_Lead_Time,Operations

KPI-EY117-002,DISRUPT-WEATHER-001,NPS_Score,Points,50,38,MISS,2026-01-31,DOWN,
Poor_Communication_Response,Enhance_Notification_System,Customer_Service

KPI-EY117-003,DISRUPT-WEATHER-001,Revenue_Recovery,%,90,82,MISS,2026-01-31,DOWN,
Competitor_Pressure,Loyalty_Incentive_Offer,Revenue_Management
```

---

## CATEGORY 8: INSURANCE & LIABILITY PARAMETERS

### Affected Files:
- **NEW FILE RECOMMENDED**: `insurance_liability_coverage.csv`
- **financial_impact.csv** (ENHANCED)

### **NEW FILE: insurance_liability_coverage.csv**

**Columns**:
```
coverage_id, aircraft_registration, coverage_type, coverage_limit_usd,
coverage_limit_aed, deductible_usd, deductible_aed, policy_start_date,
policy_end_date, carrier_name, claim_history_count, excluded_scenarios,
third_party_liability_coverage, passenger_liability_coverage, cargo_liability_coverage
```

**Sample Data**:
```
INS-A6-EYM-001,A6-EYM,AOG_MECHANICAL,2500000,9175000,50000,183500,2025-01-01,
2026-01-01,Allianz_Aviation,0,WAR;TERRORISM,TRUE,TRUE,TRUE

INS-A6-EYM-002,A6-EYM,PASSENGER_LIABILITY,5000000,18350000,100000,367000,2025-01-01,
2026-01-01,AIG_Specialty,1,WEATHER,FALSE,TRUE,FALSE

INS-A6-EYM-003,A6-EYM,THIRD_PARTY_LIABILITY,3000000,11010000,75000,275250,2025-01-01,
2026-01-01,XL_Catlin,0,SECURITY,TRUE,FALSE,FALSE
```

### **RECOMMENDED ADDITIONS to financial_impact.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **insurance_claim_amount_usd** | DECIMAL | Potential insurance recovery | 50,000 |
| **insurance_claim_amount_aed** | DECIMAL | Insurance recovery (AED) | 183,500 |
| **insurance_deductible_usd** | DECIMAL | Out-of-pocket deductible | 5,000 |
| **insurance_deductible_aed** | DECIMAL | Deductible (AED) | 18,350 |
| **third_party_liability_exposure_usd** | DECIMAL | Airport/handler liability risk | 15,000 |
| **third_party_liability_exposure_aed** | DECIMAL | Liability risk (AED) | 55,050 |
| **net_cost_after_insurance_usd** | DECIMAL | Final cost with coverage | 55,000 |
| **net_cost_after_insurance_aed** | DECIMAL | Final cost (AED) | 201,850 |

---

## CATEGORY 9: OPERATIONAL RESILIENCE METRICS

### Affected Files:
- **crew_roster_enriched.csv** (ENHANCED)
- **aircraft_availability_enriched_mel.csv** (ENHANCED)
- **reserve_crew_pool.csv** (ENHANCED)

### **RECOMMENDED ADDITIONS to crew_roster_enriched.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **redundancy_level** | VARCHAR | Backup availability | PRIMARY, BACKUP_1, BACKUP_2 |
| **contingency_callout_minutes** | INTEGER | Time to mobilize crew | 30 |
| **max_duty_hours_remaining** | DECIMAL | Available duty time | 4.5 |
| **crew_rest_quality** | VARCHAR | Last rest adequacy | FULL_REST, PARTIAL_REST, FATIGUED |
| **can_operate_night_sectors** | BOOLEAN | Night flying qualification | TRUE |
| **hot_standby_status** | VARCHAR | Standby commitment level | ON_CALL, STANDBY, ACTIVE |

### **RECOMMENDED ADDITIONS to aircraft_availability_enriched_mel.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **rto_recovery_hours** | DECIMAL | Recovery Time Objective | 4 |
| **bc_plan_activation_level** | VARCHAR | Business continuity readiness | LEVEL_1_ALERT, LEVEL_2_RESPONSE |
| **hot_standby_status** | BOOLEAN | Immediately available for swap | TRUE |
| **spare_aircraft_available** | INTEGER | Number of swappable aircraft | 2 |
| **crew_redundancy_count** | INTEGER | Available backup crew groups | 3 |

### **RECOMMENDED ADDITIONS to reserve_crew_pool.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **contingency_callout_time_minutes** | INTEGER | Response time | 45 |
| **max_duty_hours_available** | DECIMAL | Available duty time | 7.5 |
| **crew_rest_status** | VARCHAR | Current rest adequacy | FULLY_RESTED, PARTIAL_REST |
| **highest_qualification** | VARCHAR | Most advanced cert | B787_CAPTAIN |
| **language_proficiency** | VARCHAR | Operational languages | ENGLISH,ARABIC,FRENCH |
| **recent_disruption_experience** | BOOLEAN | Recently handled emergencies | TRUE |

---

## CATEGORY 10: DATA INTELLIGENCE & ANALYTICS

### Affected Files:
- **NEW FILE RECOMMENDED**: `historical_disruption_patterns.csv`
- **recovery_scenarios.csv** (ENHANCED)
- **disruption_events.csv** (ENHANCED)

### **NEW FILE: historical_disruption_patterns.csv**

**Columns**:
```
pattern_id, disruption_type, location, historical_frequency_per_year,
average_duration_hours, root_cause_frequency_ranking, similar_incident_count,
avg_passengers_affected, avg_cost_aed, prediction_confidence_pct,
ml_model_accuracy_pct, scenario_simulation_results_json, outcome_probability_distribution
```

**Sample Data**:
```
PATTERN-WEATHER-BKK,TYPHOON,BKK,0.3,48,MONSOON_SEASON=85%;CLIMATE_ANOMALY=15%,4,
350,1287135,0.92,0.89,"{""option1_cost"":1316148,""option2_cost"":313200,""option3_cost"":1771750}",
"{""prob_option1"":0.70,""prob_option2"":0.95,""prob_option3"":1.00}"

PATTERN-MECHANICAL-AOG,AOG_AIRCRAFT,AUH,1.2,3.5,HYDRAULIC_FAILURE=45%;ENGINE_ISSUE=35%;OTHER=20%,12,
350,205175,0.87,0.85,"{""repair_success"":0.85,""swap_success"":0.99,""cancel_success"":1.00}",
"{""prob_repair"":0.85,""prob_swap"":0.99,""prob_cancel"":0.25}"

PATTERN-MEDICAL-DIVERSION,MEDICAL_EMERGENCY,ROUTE,2.5,6,PAX_ILLNESS=60%;CREW_ILLNESS=25%;OTHER=15%,8,
330,87600,0.76,0.82,"{""divert_success"":0.95,""continue_success"":0.40}",
"{""prob_divert"":0.95,""prob_continue"":0.05}"
```

### **RECOMMENDED ADDITIONS to recovery_scenarios.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **ml_predicted_outcome_pct** | DECIMAL | ML model prediction | 0.92 (92% success) |
| **scenario_simulation_count** | INTEGER | Number of Monte Carlo runs | 10000 |
| **probability_success_pct** | DECIMAL | P(successful recovery) | 0.95 |
| **probability_partial_success_pct** | DECIMAL | P(partial recovery) | 0.04 |
| **probability_failure_pct** | DECIMAL | P(recovery fails) | 0.01 |
| **confidence_interval_95_pct** | VARCHAR | Statistical confidence band | 0.92-0.98 |
| **similar_historical_incidents** | INTEGER | Past comparable cases | 4 |
| **lessons_learned_applied** | TEXT | Improvement from history | Faster crew callout; Better communication |

### **RECOMMENDED ADDITIONS to disruption_events.csv:**

| New Column | Data Type | Purpose | Example |
|------------|-----------|---------|---------|
| **predicted_duration_minutes** | INTEGER | ML forecast | 180 |
| **predicted_cascading_flights** | INTEGER | Expected cascade count | 8 |
| **prediction_confidence_pct** | DECIMAL | Model confidence | 0.87 |
| **similar_past_incidents** | INTEGER | Historical comparison | 3 |
| **lessons_from_similar_incidents** | TEXT | Applied improvements | Used faster crew callout |
| **outcome_after_resolution** | VARCHAR | Final result | RESOLVED_OPTION_2 |
| **actual_duration_vs_predicted** | INTEGER | Duration variance minutes | +15 |

---

## SUMMARY TABLE: CSV FILE ENHANCEMENT ROADMAP

| File | Category | Enhancement Level | New Columns | New File Required |
|------|----------|-------------------|-------------|-------------------|
| **aircraft_maintenance_workorders.csv** | 1,2 | HIGH | 15 | NO |
| **aircraft_availability_enriched_mel.csv** | 1,9 | HIGH | 8 | NO |
| **flights_enriched_scenarios.csv** | 4 | MEDIUM | 6 | NO |
| **airport_slots.csv** | 4,6 | MEDIUM | 7 | NO |
| **minimum_connection_times.csv** | 6 | LOW | 4 | NO |
| **airport_curfews.csv** | 6 | LOW | 4 | NO |
| **passengers_enriched_final.csv** | 5 | MEDIUM | 6 | NO |
| **bookings.csv** | 5 | MEDIUM | 4 | NO |
| **crew_roster_enriched.csv** | 9 | HIGH | 6 | NO |
| **reserve_crew_pool.csv** | 9 | HIGH | 6 | NO |
| **aircraft_availability_enriched_mel.csv** | 9 | HIGH | 3 | NO |
| **financial_impact.csv** | 3,8 | HIGH | 7 | NO |
| **recovery_scenarios.csv** | 7,10 | HIGH | 8 | NO |
| **disruption_events.csv** | 10 | MEDIUM | 6 | NO |
| **NEW: maintenance_facilities_repair_logistics.csv** | 2 | HIGH | 17 | YES |
| **NEW: sustainability_impact_metrics.csv** | 3 | MEDIUM | 13 | YES |
| **NEW: partner_airline_capacity.csv** | 4 | MEDIUM | 10 | YES |
| **NEW: passenger_communication_preferences.csv** | 5 | MEDIUM | 12 | YES |
| **NEW: insurance_liability_coverage.csv** | 8 | MEDIUM | 14 | YES |
| **NEW: historical_disruption_patterns.csv** | 10 | HIGH | 8 | YES |

---

## IMPLEMENTATION PRIORITY

### **PHASE 1 (CRITICAL - Week 1):**
1. Enhance `aircraft_maintenance_workorders.csv` (MTBF, component tracking)
2. Enhance `crew_roster_enriched.csv` (redundancy, callout time)
3. Create `maintenance_facilities_repair_logistics.csv` (facility capacity)
4. Create `insurance_liability_coverage.csv` (financial risk mgmt)

### **PHASE 2 (HIGH - Week 2):**
5. Enhance `aircraft_availability_enriched_mel.csv` (health status, RTO)
6. Enhance `financial_impact.csv` (insurance, sustainability)
7. Create `historical_disruption_patterns.csv` (ML models)
8. Enhance `recovery_scenarios.csv` (KPIs, probabilities)

### **PHASE 3 (MEDIUM - Week 3):**
9. Enhance `flights_enriched_scenarios.csv` (alternative routes)
10. Enhance `passengers_enriched_final.csv` (communication prefs)
11. Create `passenger_communication_preferences.csv` (tracking)
12. Create `partner_airline_capacity.csv` (rebooking options)

### **PHASE 4 (LOW - Week 4):**
13. Enhance `airport_slots.csv` (recovery options, congestion)
14. Create `sustainability_impact_metrics.csv` (ESG tracking)
15. Enhance `minimum_connection_times.csv` (flexibility)
16. Enhance `disruption_events.csv` (ML predictions)

---

## EXPECTED IMPACT

**After All Enhancements:**
- ✅ 10/10 missing parameter categories covered
- ✅ 16 CSV files enhanced (15 existing + 1 new core)
- ✅ 6 new specialized CSV files created
- ✅ 150+ new data columns added across system
- ✅ Real-time disruption predictions enabled (via ML models)
- ✅ Comprehensive financial + ESG impact modeling
- ✅ Predictive maintenance alerting
- ✅ Dynamic crew & aircraft resilience tracking
- ✅ Historical pattern learning & pattern recognition
- ✅ Production-ready enterprise analytics system

---

**Status**: ENHANCEMENT ROADMAP COMPLETE  
**Total New Files**: 6 recommended  
**Total New Columns**: 150+  
**Implementation Effort**: 3-4 weeks (full team)  
**Expected ROI**: 40%+ improvement in disruption prediction accuracy
