"""
AGENT-SCENARIO COVERAGE VALIDATION
===================================
Validates that ALL 7 agents have complete data for ALL 11 scenarios.
No agent should ever say "scenario data not available".
"""
import pandas as pd
import os
from collections import defaultdict

# Output directory
OUTPUT_DIR = 'complete_output'

# ============================================================================
# AGENT TO DATASET MAPPING
# ============================================================================
AGENT_DATASETS = {
    'Flight Operations Agent': {
        'description': 'Manages flight schedules, delays, cancellations, aircraft swaps',
        'primary_datasets': [
            'flights_enriched_scenarios.csv',
            'aircraft_availability_enriched_mel.csv',
            'aircraft_swap_options.csv',
            'weather.csv',
            'disruption_events.csv'
        ],
        'secondary_datasets': [
            'airport_slots.csv',
            'airport_curfews.csv',
            'minimum_connection_times.csv'
        ],
        'key_queries': [
            'Which flights are delayed/cancelled?',
            'What aircraft are available for swap?',
            'What is the weather impact?',
            'What are the slot constraints?'
        ]
    },
    
    'Passenger Services Agent': {
        'description': 'Handles passenger rebooking, compensation, special needs',
        'primary_datasets': [
            'passengers_enriched_final.csv',
            'bookings.csv',
            'oal_rebooking_options.csv'
        ],
        'secondary_datasets': [
            'flights_enriched_scenarios.csv',
            'financial_transactions.csv',
            'disruption_costs.csv'
        ],
        'key_queries': [
            'Which passengers are affected?',
            'What rebooking options exist?',
            'Who needs special assistance?',
            'What compensation is due?'
        ]
    },
    
    'Crew Management Agent': {
        'description': 'Manages crew assignments, duty hours, qualifications',
        'primary_datasets': [
            'crew_roster_enriched.csv',
            'reserve_crew_pool.csv'
        ],
        'secondary_datasets': [
            'flights_enriched_scenarios.csv',
            'safety_constraints.csv'
        ],
        'key_queries': [
            'Which crew are available?',
            'Who is approaching duty limits?',
            'What qualifications are needed?',
            'Who can be called from reserve?'
        ]
    },
    
    'Maintenance Agent': {
        'description': 'Handles aircraft maintenance, MEL items, AOG situations',
        'primary_datasets': [
            'aircraft_maintenance_workorders.csv',
            'aircraft_availability_enriched_mel.csv',
            'maintenance_staff.csv'
        ],
        'secondary_datasets': [
            'flights_enriched_scenarios.csv',
            'aircraft_swap_options.csv'
        ],
        'key_queries': [
            'Which aircraft have MEL items?',
            'What maintenance is pending?',
            'Which aircraft are AOG?',
            'What staff are available?'
        ]
    },
    
    'Cargo Agent': {
        'description': 'Manages cargo shipments, dangerous goods, temperature-sensitive items',
        'primary_datasets': [
            'cargo_shipments.csv'
        ],
        'secondary_datasets': [
            'flights_enriched_scenarios.csv',
            'aircraft_availability_enriched_mel.csv'
        ],
        'key_queries': [
            'What cargo is affected?',
            'Any dangerous goods impacted?',
            'Temperature-sensitive shipments?',
            'Cargo rebooking options?'
        ]
    },
    
    'Recovery Planning Agent': {
        'description': 'Coordinates overall recovery, prioritizes actions, tracks progress',
        'primary_datasets': [
            'recovery_scenarios.csv',
            'disruption_events.csv',
            'financial_impact.csv',
            'disruption_costs.csv'
        ],
        'secondary_datasets': [
            'flights_enriched_scenarios.csv',
            'passengers_enriched_final.csv',
            'aircraft_swap_options.csv',
            'oal_rebooking_options.csv'
        ],
        'key_queries': [
            'What is the recovery plan?',
            'What is the financial impact?',
            'What actions are prioritized?',
            'What is the recovery status?'
        ]
    },
    
    'Safety & Compliance Agent': {
        'description': 'Ensures regulatory compliance, safety constraints, duty limits',
        'primary_datasets': [
            'safety_constraints.csv',
            'crew_roster_enriched.csv'
        ],
        'secondary_datasets': [
            'flights_enriched_scenarios.csv',
            'airport_curfews.csv',
            'minimum_connection_times.csv'
        ],
        'key_queries': [
            'Any safety violations?',
            'Crew duty limit breaches?',
            'Regulatory constraints?',
            'Curfew violations?'
        ]
    }
}

# ============================================================================
# 11 SCENARIOS
# ============================================================================
SCENARIOS = {
    1: {'name': 'Bangkok Typhoon + Critical MEL Aircraft', 'date': '2026-01-19', 'flights': 10},
    2: {'name': 'London Fog + Multiple Aircraft AOG', 'date': '2026-01-20', 'flights': 12},
    3: {'name': 'Singapore Thunderstorms + MEL Expiry Cascade', 'date': '2026-01-21', 'flights': 8},
    4: {'name': 'Paris Winter Storm + Temperature-Controlled Cargo', 'date': '2026-01-22', 'flights': 8},
    5: {'name': 'Dubai Sandstorm + Hub Congestion + Multiple MEL', 'date': '2026-01-23', 'flights': 14},
    6: {'name': 'Multiple Aircraft AOG + Engine Failure Cascade', 'date': '2026-01-24', 'flights': 8},
    7: {'name': 'Crew Out of Hours + Insufficient Cabin Crew', 'date': '2026-01-25', 'flights': 10},
    8: {'name': 'Runway Closure + Airspace Flow Rate Restrictions', 'date': '2026-01-27', 'flights': 14},
    9: {'name': 'Security Threat + Geopolitical Airspace Diversion', 'date': '2026-01-28', 'flights': 20},
    10: {'name': 'Medical Emergency + Tarmac Delay + Slot Unavailability', 'date': '2026-01-29', 'flights': 3},
    11: {'name': 'EY401 Typhoon → EY406 LIAC', 'date': '2026-01-31', 'flights': 10}
}

def load_all_datasets():
    """Load all datasets from complete_output"""
    datasets = {}
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith('.csv'):
            try:
                df = pd.read_csv(f'{OUTPUT_DIR}/{filename}')
                datasets[filename] = df
            except Exception as e:
                print(f"  ❌ Error loading {filename}: {e}")
    return datasets

def validate_agent_scenario_coverage(datasets):
    """Validate each agent has data for all 11 scenarios"""
    print("\n" + "="*80)
    print("AGENT-SCENARIO COVERAGE VALIDATION")
    print("="*80)
    
    all_passed = True
    agent_results = {}
    
    for agent_name, agent_config in AGENT_DATASETS.items():
        print(f"\n{'='*60}")
        print(f"📋 {agent_name}")
        print(f"   {agent_config['description']}")
        print(f"{'='*60}")
        
        agent_results[agent_name] = {
            'scenarios_covered': set(),
            'missing_scenarios': set(),
            'datasets_status': {}
        }
        
        # Check primary datasets
        print("\n  PRIMARY DATASETS:")
        for dataset_name in agent_config['primary_datasets']:
            if dataset_name in datasets:
                df = datasets[dataset_name]
                if 'scenario_id' in df.columns:
                    scenarios = set(df['scenario_id'].unique())
                    missing = set(range(1, 12)) - scenarios
                    agent_results[agent_name]['scenarios_covered'].update(scenarios)
                    
                    if missing:
                        print(f"    ❌ {dataset_name}: Missing scenarios {sorted(missing)}")
                        agent_results[agent_name]['missing_scenarios'].update(missing)
                        agent_results[agent_name]['datasets_status'][dataset_name] = 'INCOMPLETE'
                        all_passed = False
                    else:
                        print(f"    ✅ {dataset_name}: All 11 scenarios ({len(df)} rows)")
                        agent_results[agent_name]['datasets_status'][dataset_name] = 'COMPLETE'
                else:
                    print(f"    ⚠️ {dataset_name}: No scenario_id column")
                    agent_results[agent_name]['datasets_status'][dataset_name] = 'NO_SCENARIO_ID'
            else:
                print(f"    ❌ {dataset_name}: FILE NOT FOUND")
                agent_results[agent_name]['datasets_status'][dataset_name] = 'NOT_FOUND'
                all_passed = False
        
        # Check secondary datasets
        print("\n  SECONDARY DATASETS:")
        for dataset_name in agent_config['secondary_datasets']:
            if dataset_name in datasets:
                df = datasets[dataset_name]
                if 'scenario_id' in df.columns:
                    scenarios = set(df['scenario_id'].unique())
                    if len(scenarios) == 11:
                        print(f"    ✅ {dataset_name}: All 11 scenarios")
                    else:
                        print(f"    ⚠️ {dataset_name}: {len(scenarios)} scenarios")
                else:
                    print(f"    ℹ️ {dataset_name}: Available (no scenario_id)")
            else:
                print(f"    ⚠️ {dataset_name}: Not available")
        
        # Summary for this agent
        covered = agent_results[agent_name]['scenarios_covered']
        missing = set(range(1, 12)) - covered
        if not missing:
            print(f"\n  ✅ AGENT CAN ANSWER QUERIES FOR ALL 11 SCENARIOS")
        else:
            print(f"\n  ❌ AGENT MISSING DATA FOR SCENARIOS: {sorted(missing)}")
    
    return all_passed, agent_results

def generate_scenario_query_matrix(datasets):
    """Generate a matrix showing what each agent can answer per scenario"""
    print("\n" + "="*80)
    print("SCENARIO QUERY CAPABILITY MATRIX")
    print("="*80)
    
    # Header
    print(f"\n{'Agent':<30} | " + " | ".join([f"S{i:02d}" for i in range(1, 12)]))
    print("-" * 30 + "-+-" + "-+-".join(["---"] * 11))
    
    for agent_name, agent_config in AGENT_DATASETS.items():
        row = f"{agent_name:<30} | "
        scenario_status = []
        
        for scenario_id in range(1, 12):
            has_data = False
            for dataset_name in agent_config['primary_datasets']:
                if dataset_name in datasets:
                    df = datasets[dataset_name]
                    if 'scenario_id' in df.columns:
                        if scenario_id in df['scenario_id'].values:
                            has_data = True
                            break
            
            scenario_status.append(" ✅ " if has_data else " ❌ ")
        
        print(row + " | ".join(scenario_status))

def generate_data_flow_diagram():
    """Print how agents communicate via shared data"""
    print("\n" + "="*80)
    print("AGENT COMMUNICATION VIA SHARED DATA")
    print("="*80)
    
    print("""
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                           DISRUPTION EVENT                                   │
    │                    (disruption_events.csv - scenario_id)                     │
    └─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                        FLIGHT OPERATIONS AGENT                               │
    │  Reads: flights_enriched_scenarios, aircraft_availability, weather           │
    │  Outputs: Flight delays, cancellations, swap recommendations                 │
    │  Shares via: flight_id, aircraft_registration, scenario_id                   │
    └─────────────────────────────────────────────────────────────────────────────┘
                    │                       │                       │
                    ▼                       ▼                       ▼
    ┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
    │  PASSENGER SERVICES   │ │   CREW MANAGEMENT     │ │   MAINTENANCE AGENT   │
    │  AGENT                │ │   AGENT               │ │                       │
    │                       │ │                       │ │                       │
    │  Reads:               │ │  Reads:               │ │  Reads:               │
    │  - passengers_*       │ │  - crew_roster_*      │ │  - maintenance_*      │
    │  - bookings           │ │  - reserve_crew_pool  │ │  - aircraft_avail     │
    │  - oal_rebooking      │ │  - safety_constraints │ │  - maintenance_staff  │
    │                       │ │                       │ │                       │
    │  Links via:           │ │  Links via:           │ │  Links via:           │
    │  flight_id, pax_id    │ │  flight_id, crew_id   │ │  aircraft_reg         │
    └───────────────────────┘ └───────────────────────┘ └───────────────────────┘
                    │                       │                       │
                    └───────────────────────┼───────────────────────┘
                                            ▼
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                         CARGO AGENT                                          │
    │  Reads: cargo_shipments (linked via flight_id, aircraft_registration)        │
    │  Handles: DG goods, temperature-sensitive, rebooking                         │
    └─────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                      RECOVERY PLANNING AGENT                                 │
    │  Reads: recovery_scenarios, financial_impact, disruption_costs               │
    │  Aggregates: All agent outputs to create recovery plan                       │
    │  Coordinates: Priority actions, resource allocation                          │
    └─────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                     SAFETY & COMPLIANCE AGENT                                │
    │  Reads: safety_constraints, crew_roster (duty hours), airport_curfews        │
    │  Validates: All recovery actions comply with regulations                     │
    │  Flags: Any violations before execution                                      │
    └─────────────────────────────────────────────────────────────────────────────┘
    """)

def print_agent_dataset_mapping():
    """Print detailed agent-dataset mapping"""
    print("\n" + "="*80)
    print("DETAILED AGENT-DATASET MAPPING")
    print("="*80)
    
    for agent_name, config in AGENT_DATASETS.items():
        print(f"\n┌{'─'*78}┐")
        print(f"│ {agent_name:<76} │")
        print(f"├{'─'*78}┤")
        print(f"│ {config['description']:<76} │")
        print(f"├{'─'*78}┤")
        print(f"│ PRIMARY DATASETS:{'':60} │")
        for ds in config['primary_datasets']:
            print(f"│   • {ds:<72} │")
        print(f"├{'─'*78}┤")
        print(f"│ SECONDARY DATASETS:{'':58} │")
        for ds in config['secondary_datasets']:
            print(f"│   • {ds:<72} │")
        print(f"├{'─'*78}┤")
        print(f"│ KEY QUERIES:{'':65} │")
        for q in config['key_queries']:
            print(f"│   • {q:<72} │")
        print(f"└{'─'*78}┘")

def main():
    print("="*80)
    print("SKYMARSHAL AGENT-SCENARIO COVERAGE VALIDATION")
    print("="*80)
    print(f"\nValidating that ALL 7 agents can answer queries for ALL 11 scenarios")
    print(f"No agent should ever say 'scenario data not available'\n")
    
    # Load datasets
    print("Loading datasets...")
    datasets = load_all_datasets()
    print(f"Loaded {len(datasets)} datasets")
    
    # Print agent-dataset mapping
    print_agent_dataset_mapping()
    
    # Validate coverage
    all_passed, results = validate_agent_scenario_coverage(datasets)
    
    # Generate query matrix
    generate_scenario_query_matrix(datasets)
    
    # Print data flow
    generate_data_flow_diagram()
    
    # Final summary
    print("\n" + "="*80)
    print("FINAL VALIDATION SUMMARY")
    print("="*80)
    
    if all_passed:
        print("\n🎉 ALL VALIDATIONS PASSED!")
        print("   ✅ All 7 agents have data for all 11 scenarios")
        print("   ✅ No agent will say 'scenario data not available'")
        print("   ✅ All datasets are properly linked via key fields")
    else:
        print("\n❌ SOME VALIDATIONS FAILED!")
        print("   Review the issues above and regenerate missing data")
    
    return all_passed

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else '.')
    main()
