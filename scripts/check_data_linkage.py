import csv
import json

# Read all CSV files
flights = {}
passengers = {}
bookings = {}
cargo = {}
baggage = {}

# Read flights
with open('flights_enriched_scenarios.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        flights[row['flight_number']] = row

# Read passengers
with open('passengers_enriched_final.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['flight_number'] not in passengers:
            passengers[row['flight_number']] = []
        passengers[row['flight_number']].append(row)

# Read bookings
with open('bookings.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['flight_number'] not in bookings:
            bookings[row['flight_number']] = []
        bookings[row['flight_number']].append(row)

# Read cargo
with open('cargo_shipments.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['flight_number'] not in cargo:
            cargo[row['flight_number']] = []
        cargo[row['flight_number']].append(row)

# Read baggage
with open('baggage_handling.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['flight_number'] not in baggage:
            baggage[row['flight_number']] = []
        baggage[row['flight_number']].append(row)

# Analyze first 4 flights
test_flights = list(flights.keys())[:4]

print("\n" + "="*80)
print("DATA LINKAGE ANALYSIS - FIRST 4 FLIGHTS")
print("="*80)

for flight_num in test_flights:
    print(f'\n{"="*80}')
    print(f'FLIGHT: {flight_num}')
    print(f'{"="*80}')
    
    # Flight info
    if flight_num in flights:
        print(f'✓ Flight exists in flights_enriched_scenarios.csv')
        print(f'  - Origin: {flights[flight_num]["origin_code"]} → Destination: {flights[flight_num]["destination_code"]}')
        print(f'  - Aircraft: {flights[flight_num]["aircraft_code"]} ({flights[flight_num]["aircraft_registration"]})')
    
    # Passengers
    pax_list = passengers.get(flight_num, [])
    print(f'\n📌 Passengers: {len(pax_list)} found')
    if pax_list:
        for pax in pax_list:
            print(f'   - {pax["passenger_id"]}: {pax["passenger_name"]} (Booking: {pax["booking_reference"]})')
    
    # Bookings
    bkg_list = bookings.get(flight_num, [])
    print(f'\n📌 Bookings: {len(bkg_list)} found')
    if bkg_list:
        for bkg in bkg_list:
            print(f'   - {bkg["booking_id"]}: Passenger {bkg["passenger_id"]} (Ref: {bkg["booking_reference"]}, Status: {bkg["booking_status"]})')
    
    # Cargo
    cargo_list = cargo.get(flight_num, [])
    print(f'\n📌 Cargo: {len(cargo_list)} found')
    if cargo_list:
        total_weight = sum(float(c['weight_kg']) for c in cargo_list)
        for crg in cargo_list:
            print(f'   - {crg["shipment_id"]}: {crg["shipment_type"]} ({crg["weight_kg"]} kg)')
        print(f'   Total cargo weight: {total_weight} kg')
    
    # Baggage
    baggage_list = baggage.get(flight_num, [])
    print(f'\n📌 Baggage: {len(baggage_list)} found')
    if baggage_list:
        for bag in baggage_list:
            print(f'   - {bag["baggage_id"]}: Passenger {bag["passenger_id"]} ({bag["weight_kg"]} kg, Status: {bag["status"]})')
    
    # Linkage verification
    print(f'\n⚠️  LINKAGE VERIFICATION:')
    
    # Check passenger-booking linkage
    pax_ids = set(p['passenger_id'] for p in pax_list)
    bkg_pax_ids = set(b['passenger_id'] for b in bkg_list)
    if pax_ids == bkg_pax_ids:
        print(f'   ✓ All passengers have corresponding bookings')
    else:
        missing = pax_ids - bkg_pax_ids
        extra = bkg_pax_ids - pax_ids
        if missing:
            print(f'   ❌ Passengers without bookings: {missing}')
        if extra:
            print(f'   ❌ Bookings without passengers: {extra}')
    
    # Check baggage-passenger linkage
    baggage_pax_ids = set(b['passenger_id'] for b in baggage_list)
    if baggage_pax_ids.issubset(pax_ids) or len(baggage_pax_ids) == 0:
        print(f'   ✓ All baggage linked to valid passengers (or no baggage)')
    else:
        orphan = baggage_pax_ids - pax_ids
        print(f'   ❌ Baggage linked to non-existent passengers: {orphan}')
    
    # Check booking-reference linkage
    pax_refs = {p['passenger_id']: p['booking_reference'] for p in pax_list}
    bkg_refs = {b['passenger_id']: b['booking_reference'] for b in bkg_list}
    mismatch = []
    for pax_id in pax_ids:
        if pax_id in pax_refs and pax_id in bkg_refs:
            if pax_refs[pax_id] != bkg_refs[pax_id]:
                mismatch.append(f'{pax_id}: Passenger ref={pax_refs[pax_id]}, Booking ref={bkg_refs[pax_id]}')
    
    if mismatch:
        print(f'   ❌ Booking reference mismatches:')
        for m in mismatch:
            print(f'      {m}')
    else:
        print(f'   ✓ All booking references match between passengers and bookings')
    
    # Cargo linkage check
    if cargo_list:
        print(f'   ✓ Cargo present for flight')
    else:
        print(f'   ⚠️  No cargo data linked to this flight')

print(f'\n{"="*80}')
print("SUMMARY")
print(f'{"="*80}')
print(f'Total flights analyzed: {len(test_flights)}')
print(f'Total passengers: {sum(len(passengers.get(f, [])) for f in test_flights)}')
print(f'Total bookings: {sum(len(bookings.get(f, [])) for f in test_flights)}')
print(f'Total cargo shipments: {sum(len(cargo.get(f, [])) for f in test_flights)}')
print(f'Total baggage records: {sum(len(baggage.get(f, [])) for f in test_flights)}')
