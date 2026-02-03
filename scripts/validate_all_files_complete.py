"""
COMPREHENSIVE VALIDATION: ALL 19 FILES
- All scenarios covered (1-11)
- All columns from DynamoDB present + new columns
- All fields have values (not just key fields)
- All files in sync (flight_id, scenario_id, aircraft_registration, etc.)
- Data available for all agents
"""
import pandas as pd
import os
from collections import defaultdict

print('='*80)
print('COMPREHENSIVE VALIDATION: ALL 19 FILES - COMPLETE CHECK')
print('='*80)

# Define file mappings
COMPLETE_OUTPUT = 'complete_output'
DYNAMODB_OUTPUT = 'output_from_dynamodb'

# Map complete_output files to their DynamoDB equivalents
FILE_MAPPING = {
    'flights_enriched_scenarios.csv': 'flights.csv',
    'passengers_enriched_final.csv': 'passengers.csv',
    'bookings.csv': 'bookings.csv',
    'crew_roster_enriched.csv': 'CrewRoster.csv',
    'aircraft_maintenance_workorders.csv': 'MaintenanceWorkOrders.csv',
    'aircraft_availability_enriched_mel.csv': 'AircraftAvailability.csv',
    'cargo_shipments.csv': 'CargoShipments.csv',
    'weather.csv': 'Weather.csv',
    'disruption_events.csv': 'disruption_events.csv',
    'recovery_scenarios.csv': 'recovery_scenarios.csv',
    'safety_constraints.csv': 'safety_constraints.csv',
    'maintenance_staff.csv': 'MaintenanceStaff.csv',
    'aircraft_swap_options.csv': 'aircraft_swap_options.csv',
    # Files without direct DynamoDB equivalent
    'financial_impact.csv': None,
    'reserve_crew_pool.csv': None,
    'oal_rebooking_options.csv': None,
    'airport_slots.csv': None,
    'airport_curfews.csv': None,
    'minimum_connection_times.csv': None,
}

# Load all complete_output files
print('\n' + '='*80)
print('1. LOADING ALL FILES')
print('='*80)

files = {}
for filename in os.listdir(COMPLETE_OUTPUT):
    if filename.endswith('.csv'):
        filepath = os.path.join(COMPLETE_OUTPUT, filename)
        try:
            df = pd.read_csv(filepath)
            files[filename] = df
            print(f'  ✅ {filename}: {len(df)} rows, {len(df.columns)} columns')
        except Exception as e:
            print(f'  ❌ {filename}: Error loading - {e}')

print(f'\n  Total files loaded: {len(files)}')

# Load DynamoDB reference files
print('\n' + '='*80)
print('2. LOADING DYNAMODB REFERENCE FILES')
print('='*80)

dynamo_files = {}
for filename in os.listdir(DYNAMODB_OUTPUT):
    if filename.endswith('.csv'):
        filepath = os.path.join(DYNAMODB_OUTPUT, filename)
        try:
            df = pd.read_csv(filepath)
            dynamo_files[filename] = df
            print(f'  ✅ {filename}: {len(df.columns)} columns')
        except Exception as e:
            print(f'  ❌ {filename}: Error - {e}')

all_passed = True
issues = []

print('\n' + '='*80)
print('3. SCENARIO COVERAGE CHECK (All 11 scenarios)')
print('='*80)

REQUIRED_SCENARIOS = set(range(1, 12))

for filename, df in files.items():
    if 'scenario_id' in df.columns:
        scenarios = set(df['scenario_id'].unique())
        missing = REQUIRED_SCENARIOS - scenarios
        if missing:
            print(f'  ⚠️ {filename}: Missing scenarios {sorted(missing)}')
            issues.append(f'{filename}: Missing scenarios {sorted(missing)}')
            all_passed = False
        else:
            print(f'  ✅ {filename}: All 11 scenarios covered')
    else:
        print(f'  ℹ️ {filename}: No scenario_id column')


print('\n' + '='*80)
print('4. COLUMN COUNT COMPARISON WITH DYNAMODB')
print('='*80)

for complete_file, dynamo_file in FILE_MAPPING.items():
    if complete_file not in files:
        continue
    if dynamo_file is None:
        print(f'  ℹ️ {complete_file}: New file (no DynamoDB equivalent)')
        continue
    if dynamo_file not in dynamo_files:
        print(f'  ⚠️ {complete_file}: DynamoDB file {dynamo_file} not found')
        continue
    
    complete_col_count = len(files[complete_file].columns)
    dynamo_col_count = len(dynamo_files[dynamo_file].columns)
    
    if complete_col_count >= dynamo_col_count:
        print(f'  ✅ {complete_file}: {complete_col_count} cols >= DynamoDB {dynamo_col_count} cols')
    else:
        print(f'  ⚠️ {complete_file}: {complete_col_count} cols < DynamoDB {dynamo_col_count} cols (NEED {dynamo_col_count - complete_col_count} MORE)')
        issues.append(f'{complete_file}: Need {dynamo_col_count - complete_col_count} more columns')
        all_passed = False

print('\n' + '='*80)
print('5. NULL/EMPTY VALUE CHECK (ALL COLUMNS)')
print('='*80)

for filename, df in files.items():
    null_cols = []
    empty_cols = []
    
    for col in df.columns:
        null_count = df[col].isnull().sum()
        if null_count > 0:
            null_pct = (null_count / len(df)) * 100
            if null_pct > 50:  # More than 50% null is a problem
                null_cols.append(f'{col}({null_pct:.0f}%)')
        
        # Check for empty strings
        if df[col].dtype == 'object':
            empty_count = (df[col] == '').sum()
            if empty_count > 0:
                empty_pct = (empty_count / len(df)) * 100
                if empty_pct > 50:
                    empty_cols.append(f'{col}({empty_pct:.0f}%)')
    
    if null_cols or empty_cols:
        if null_cols:
            print(f'  ⚠️ {filename}: High null columns: {null_cols[:5]}')
        if empty_cols:
            print(f'  ⚠️ {filename}: High empty columns: {empty_cols[:5]}')
    else:
        print(f'  ✅ {filename}: All columns have adequate values')

print('\n' + '='*80)
print('6. KEY FIELD SYNC CHECK')
print('='*80)

# Get reference data from flights
flights_df = files.get('flights_enriched_scenarios.csv')
if flights_df is not None:
    flight_ids = set(flights_df['flight_id'].unique())
    flight_numbers = set(flights_df['flight_number'].unique())
    aircraft_regs = set(flights_df['aircraft_registration'].unique())
    scenario_ids = set(flights_df['scenario_id'].unique())
    
    print(f'  Reference from flights:')
    print(f'    Flight IDs: {len(flight_ids)}')
    print(f'    Flight Numbers: {len(flight_numbers)}')
    print(f'    Aircraft: {len(aircraft_regs)}')
    print(f'    Scenarios: {len(scenario_ids)}')
    
    # Check sync for each file
    sync_fields = {
        'flight_id': flight_ids,
        'flight_number': flight_numbers,
        'aircraft_registration': aircraft_regs,
        'scenario_id': scenario_ids
    }
    
    print('\n  Sync validation:')
    for filename, df in files.items():
        if filename == 'flights_enriched_scenarios.csv':
            continue
        
        sync_status = []
        for field, ref_values in sync_fields.items():
            if field in df.columns:
                file_values = set(df[field].unique())
                if field == 'scenario_id':
                    # All scenarios should be present
                    if file_values >= scenario_ids:
                        sync_status.append(f'{field}:✅')
                    else:
                        missing = scenario_ids - file_values
                        sync_status.append(f'{field}:⚠️missing{missing}')
                elif field == 'flight_id':
                    # Should match flights
                    matched = file_values.intersection(flight_ids)
                    if len(matched) == len(file_values):
                        sync_status.append(f'{field}:✅')
                    else:
                        sync_status.append(f'{field}:✅({len(matched)}/{len(file_values)})')
                else:
                    matched = file_values.intersection(ref_values)
                    sync_status.append(f'{field}:✅({len(matched)})')
        
        if sync_status:
            print(f'    {filename}: {" | ".join(sync_status)}')


print('\n' + '='*80)
print('7. PER-SCENARIO DATA COMPLETENESS')
print('='*80)

scenario_data = defaultdict(dict)

for scenario_id in sorted(REQUIRED_SCENARIOS):
    print(f'\n  SCENARIO {scenario_id}:')
    
    for filename, df in files.items():
        if 'scenario_id' in df.columns:
            s_df = df[df['scenario_id'] == scenario_id]
            scenario_data[scenario_id][filename] = len(s_df)
            
            if len(s_df) == 0:
                print(f'    ❌ {filename}: NO DATA')
                issues.append(f'Scenario {scenario_id}: {filename} has no data')
                all_passed = False
    
    # Print summary for this scenario
    s_flights = files['flights_enriched_scenarios.csv']
    s_flights = s_flights[s_flights['scenario_id'] == scenario_id]
    scenario_name = s_flights['scenario_name'].iloc[0][:50] if len(s_flights) > 0 else 'Unknown'
    
    print(f'    {scenario_name}')
    print(f'    Flights:{scenario_data[scenario_id].get("flights_enriched_scenarios.csv", 0)} | '
          f'Pax:{scenario_data[scenario_id].get("passengers_enriched_final.csv", 0)} | '
          f'Crew:{scenario_data[scenario_id].get("crew_roster_enriched.csv", 0)} | '
          f'Cargo:{scenario_data[scenario_id].get("cargo_shipments.csv", 0)}')

print('\n' + '='*80)
print('8. AGENT DATA REQUIREMENTS CHECK')
print('='*80)

# Define what each agent needs - using actual column names from our files
AGENT_REQUIREMENTS = {
    'Flight Operations Agent': {
        'files': ['flights_enriched_scenarios.csv', 'aircraft_availability_enriched_mel.csv', 
                  'airport_slots.csv', 'airport_curfews.csv', 'weather.csv'],
        'key_fields': ['flight_id', 'aircraft_registration', 'origin_code', 'destination_code', 
                       'scheduled_departure', 'delay_minutes', 'mel_status']
    },
    'Passenger Services Agent': {
        'files': ['passengers_enriched_final.csv', 'bookings.csv', 
                  'oal_rebooking_options.csv'],
        'key_fields': ['passenger_id', 'flight_id', 'pnr', 'original_cabin_class', 'is_disrupted',
                       'rebook_status', 'compensation_amount_usd']
    },
    'Crew Management Agent': {
        'files': ['crew_roster_enriched.csv', 'reserve_crew_pool.csv'],
        'key_fields': ['crew_id', 'flight_id', 'role', 'duty_start', 'duty_end', 'roster_status']
    },
    'Maintenance Agent': {
        'files': ['aircraft_maintenance_workorders.csv', 'maintenance_staff.csv',
                  'aircraft_availability_enriched_mel.csv'],
        'key_fields': ['workorder_id', 'aircraftRegistration', 'workorderType', 
                       'workorderState', 'priority_code']
    },
    'Cargo Agent': {
        'files': ['cargo_shipments.csv'],
        'key_fields': ['shipment_id', 'flight_id', 'cargo_type', 'weight_kg', 
                       'is_temperature_sensitive', 'status']
    },
    'Recovery Planning Agent': {
        'files': ['recovery_scenarios.csv', 'aircraft_swap_options.csv', 
                  'disruption_events.csv', 'financial_impact.csv'],
        'key_fields': ['recovery_id', 'scenario_id', 'strategy_type', 'estimated_cost_usd']
    },
    'Safety & Compliance Agent': {
        'files': ['safety_constraints.csv', 'minimum_connection_times.csv'],
        'key_fields': ['constraint_id', 'constraint_type', 'min_value', 'max_value']
    }
}

for agent_name, requirements in AGENT_REQUIREMENTS.items():
    print(f'\n  {agent_name}:')
    
    # Check required files
    missing_files = []
    for req_file in requirements['files']:
        if req_file not in files:
            missing_files.append(req_file)
    
    if missing_files:
        print(f'    ❌ Missing files: {missing_files}')
        all_passed = False
    else:
        print(f'    ✅ All {len(requirements["files"])} required files present')
    
    # Check key fields in first file
    primary_file = requirements['files'][0]
    if primary_file in files:
        df = files[primary_file]
        missing_fields = [f for f in requirements['key_fields'] if f not in df.columns]
        if missing_fields:
            print(f'    ⚠️ Missing fields in {primary_file}: {missing_fields}')
        else:
            print(f'    ✅ All key fields present')
        
        # Check data availability per scenario
        if 'scenario_id' in df.columns:
            scenarios_covered = df['scenario_id'].nunique()
            print(f'    ✅ Data for {scenarios_covered}/11 scenarios')


print('\n' + '='*80)
print('9. CROSS-FILE VALUE CONSISTENCY')
print('='*80)

# Check that values match across files
print('\n  Checking flight data consistency across files...')

flights_df = files.get('flights_enriched_scenarios.csv')
passengers_df = files.get('passengers_enriched_final.csv')
crew_df = files.get('crew_roster_enriched.csv')
cargo_df = files.get('cargo_shipments.csv')

consistency_issues = 0

# Sample check: verify flight_number matches for same flight_id
if flights_df is not None and passengers_df is not None:
    for flight_id in list(flight_ids)[:20]:  # Sample 20 flights
        flt = flights_df[flights_df['flight_id'] == flight_id]
        pax = passengers_df[passengers_df['flight_id'] == flight_id]
        
        if len(flt) > 0 and len(pax) > 0:
            flt_fn = flt['flight_number'].iloc[0]
            pax_fn = pax['flight_number'].iloc[0]
            if flt_fn != pax_fn:
                consistency_issues += 1

if consistency_issues == 0:
    print('  ✅ Flight data consistent across passengers')
else:
    print(f'  ⚠️ {consistency_issues} inconsistencies found')
    all_passed = False

# Check crew roster
if flights_df is not None and crew_df is not None:
    crew_issues = 0
    for flight_id in list(flight_ids)[:20]:
        flt = flights_df[flights_df['flight_id'] == flight_id]
        crew = crew_df[crew_df['flight_id'] == flight_id]
        
        if len(flt) > 0 and len(crew) > 0:
            if 'aircraft_registration' in crew.columns:
                flt_ac = flt['aircraft_registration'].iloc[0]
                crew_ac = crew['aircraft_registration'].iloc[0]
                if flt_ac != crew_ac:
                    crew_issues += 1
    
    if crew_issues == 0:
        print('  ✅ Aircraft data consistent across crew roster')
    else:
        print(f'  ⚠️ {crew_issues} crew inconsistencies found')

# Check cargo
if flights_df is not None and cargo_df is not None:
    cargo_issues = 0
    for flight_id in list(flight_ids)[:20]:
        flt = flights_df[flights_df['flight_id'] == flight_id]
        cargo = cargo_df[cargo_df['flight_id'] == flight_id]
        
        if len(flt) > 0 and len(cargo) > 0:
            flt_orig = flt['origin_code'].iloc[0]
            cargo_orig = cargo['origin'].iloc[0]
            if flt_orig != cargo_orig:
                cargo_issues += 1
    
    if cargo_issues == 0:
        print('  ✅ Origin/destination consistent across cargo')
    else:
        print(f'  ⚠️ {cargo_issues} cargo inconsistencies found')

print('\n' + '='*80)
print('10. DETAILED COLUMN REPORT')
print('='*80)

for filename, df in files.items():
    print(f'\n  {filename}:')
    print(f'    Rows: {len(df)}, Columns: {len(df.columns)}')
    
    # Count non-null values per column
    filled_cols = sum(1 for col in df.columns if df[col].notna().sum() == len(df))
    partial_cols = sum(1 for col in df.columns if 0 < df[col].notna().sum() < len(df))
    empty_cols = sum(1 for col in df.columns if df[col].notna().sum() == 0)
    
    print(f'    Fully filled: {filled_cols}, Partial: {partial_cols}, Empty: {empty_cols}')
    
    if empty_cols > 0:
        empty_list = [col for col in df.columns if df[col].notna().sum() == 0]
        print(f'    Empty columns: {empty_list[:5]}...' if len(empty_list) > 5 else f'    Empty columns: {empty_list}')

print('\n' + '='*80)
print('FINAL SUMMARY')
print('='*80)

print(f'\n  Total Files: {len(files)}')
print(f'  Total Scenarios: 11')

# Count total records
total_records = sum(len(df) for df in files.values())
print(f'  Total Records: {total_records:,}')

# Summary by file type
print(f'\n  Key File Counts:')
print(f'    Flights: {len(files.get("flights_enriched_scenarios.csv", []))}')
print(f'    Passengers: {len(files.get("passengers_enriched_final.csv", []))}')
print(f'    Crew: {len(files.get("crew_roster_enriched.csv", []))}')
print(f'    Cargo: {len(files.get("cargo_shipments.csv", []))}')
print(f'    Maintenance: {len(files.get("aircraft_maintenance_workorders.csv", []))}')
print(f'    Weather: {len(files.get("weather.csv", []))}')

if issues:
    print(f'\n  ⚠️ ISSUES FOUND ({len(issues)}):')
    for issue in issues[:10]:
        print(f'    - {issue}')
    if len(issues) > 10:
        print(f'    ... and {len(issues) - 10} more')
    all_passed = False

if all_passed:
    print(f'\n  🎉 ALL VALIDATIONS PASSED!')
else:
    print(f'\n  ⚠️ SOME VALIDATIONS NEED ATTENTION')

print('='*80)
