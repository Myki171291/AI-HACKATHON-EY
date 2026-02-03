import csv

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

print("\n" + "="*100)
print("COMPREHENSIVE DATA LINKAGE ANALYSIS - GLOBAL CHECK")
print("="*100)

# Issues found
issues = {
    'flights_without_passengers': [],
    'flights_without_bookings': [],
    'flights_without_cargo': [],
    'flights_without_baggage': [],
    'passengers_without_bookings': [],
    'bookings_without_passengers': [],
    'baggage_without_passengers': [],
    'booking_ref_mismatches': [],
    'seat_mismatches': [],
}

print("\n1. CHECKING FLIGHTS WITHOUT RELATED DATA")
print("-" * 100)

for flight_num, flight_data in flights.items():
    if flight_num not in passengers:
        issues['flights_without_passengers'].append(flight_num)
    if flight_num not in bookings:
        issues['flights_without_bookings'].append(flight_num)
    if flight_num not in cargo:
        issues['flights_without_cargo'].append(flight_num)
    if flight_num not in baggage:
        issues['flights_without_baggage'].append(flight_num)

print(f"✓ Total flights: {len(flights)}")
print(f"  - Flights WITH passengers: {len(flights) - len(issues['flights_without_passengers'])}")
print(f"  - Flights WITHOUT passengers: {len(issues['flights_without_passengers'])} {issues['flights_without_passengers'] if issues['flights_without_passengers'] else '✓'}")
print(f"  - Flights WITH bookings: {len(flights) - len(issues['flights_without_bookings'])}")
print(f"  - Flights WITHOUT bookings: {len(issues['flights_without_bookings'])} {issues['flights_without_bookings'] if issues['flights_without_bookings'] else '✓'}")
print(f"  - Flights WITH cargo: {len(flights) - len(issues['flights_without_cargo'])}")
print(f"  - Flights WITHOUT cargo: {len(issues['flights_without_cargo'])} (⚠️ Informational - not all flights may have cargo)")
print(f"  - Flights WITH baggage: {len(flights) - len(issues['flights_without_baggage'])}")
print(f"  - Flights WITHOUT baggage: {len(issues['flights_without_baggage'])} {issues['flights_without_baggage'] if issues['flights_without_baggage'] else '✓'}")

print("\n2. CHECKING PASSENGER-BOOKING LINKAGE")
print("-" * 100)

all_passengers = {}
for flight_num, pax_list in passengers.items():
    for pax in pax_list:
        all_passengers[pax['passenger_id']] = pax

all_bookings = {}
for flight_num, bkg_list in bookings.items():
    for bkg in bkg_list:
        all_bookings[bkg['booking_id']] = bkg

# Check passengers without bookings
for pax_id, pax_data in all_passengers.items():
    # Find booking for this passenger
    found_booking = False
    for bkg_id, bkg_data in all_bookings.items():
        if bkg_data['passenger_id'] == pax_id:
            found_booking = True
            # Check for reference mismatch
            if pax_data['booking_reference'] != bkg_data['booking_reference']:
                issues['booking_ref_mismatches'].append({
                    'passenger_id': pax_id,
                    'pax_ref': pax_data['booking_reference'],
                    'bkg_ref': bkg_data['booking_reference']
                })
            # Check for seat mismatch
            if pax_data['seat_assignment'] != bkg_data['seat_assignment']:
                issues['seat_mismatches'].append({
                    'passenger_id': pax_id,
                    'pax_seat': pax_data['seat_assignment'],
                    'bkg_seat': bkg_data['seat_assignment']
                })
            break
    if not found_booking:
        issues['passengers_without_bookings'].append(pax_id)

# Check bookings without passengers
for bkg_id, bkg_data in all_bookings.items():
    if bkg_data['passenger_id'] not in all_passengers:
        issues['bookings_without_passengers'].append({
            'booking_id': bkg_id,
            'passenger_id': bkg_data['passenger_id']
        })

print(f"✓ Total passengers: {len(all_passengers)}")
print(f"  - Passengers WITH bookings: {len(all_passengers) - len(issues['passengers_without_bookings'])}")
print(f"  - Passengers WITHOUT bookings: {len(issues['passengers_without_bookings'])} {issues['passengers_without_bookings'] if issues['passengers_without_bookings'] else '✓'}")
print(f"✓ Total bookings: {len(all_bookings)}")
print(f"  - Bookings WITH passengers: {len(all_bookings) - len(issues['bookings_without_passengers'])}")
print(f"  - Bookings WITHOUT passengers: {len(issues['bookings_without_passengers'])} {issues['bookings_without_passengers'] if issues['bookings_without_passengers'] else '✓'}")
print(f"  - Booking reference mismatches: {len(issues['booking_ref_mismatches'])} {issues['booking_ref_mismatches'] if issues['booking_ref_mismatches'] else '✓'}")
print(f"  - Seat assignment mismatches: {len(issues['seat_mismatches'])} {issues['seat_mismatches'] if issues['seat_mismatches'] else '✓'}")

print("\n3. CHECKING BAGGAGE-PASSENGER LINKAGE")
print("-" * 100)

all_baggage = {}
for flight_num, bag_list in baggage.items():
    for bag in bag_list:
        if bag['baggage_id'] not in all_baggage:
            all_baggage[bag['baggage_id']] = bag

# Check baggage without passengers
for bag_id, bag_data in all_baggage.items():
    if bag_data['passenger_id'] not in all_passengers:
        issues['baggage_without_passengers'].append({
            'baggage_id': bag_id,
            'passenger_id': bag_data['passenger_id']
        })

print(f"✓ Total baggage records: {len(all_baggage)}")
print(f"  - Baggage WITH valid passengers: {len(all_baggage) - len(issues['baggage_without_passengers'])}")
print(f"  - Baggage WITHOUT valid passengers: {len(issues['baggage_without_passengers'])} {issues['baggage_without_passengers'] if issues['baggage_without_passengers'] else '✓'}")

print("\n4. CARGO LINKAGE CHECK")
print("-" * 100)

all_cargo = {}
for flight_num, cargo_list in cargo.items():
    for crg in cargo_list:
        all_cargo[crg['shipment_id']] = crg

print(f"✓ Total cargo shipments: {len(all_cargo)}")
print(f"  - Cargo linked to flights: {len([c for c in all_cargo.values() if c['flight_number'] in flights])}")

print("\n5. CRITICAL ISSUES SUMMARY")
print("-" * 100)

critical_issues = 0

if issues['flights_without_passengers']:
    print(f"❌ {len(issues['flights_without_passengers'])} flight(s) without passengers")
    critical_issues += 1

if issues['flights_without_bookings']:
    print(f"❌ {len(issues['flights_without_bookings'])} flight(s) without bookings")
    critical_issues += 1

if issues['passengers_without_bookings']:
    print(f"❌ {len(issues['passengers_without_bookings'])} passenger(s) without bookings")
    critical_issues += 1

if issues['bookings_without_passengers']:
    print(f"❌ {len(issues['bookings_without_passengers'])} booking(s) without passengers")
    critical_issues += 1

if issues['booking_ref_mismatches']:
    print(f"❌ {len(issues['booking_ref_mismatches'])} booking reference mismatch(es)")
    critical_issues += 1

if issues['seat_mismatches']:
    print(f"❌ {len(issues['seat_mismatches'])} seat assignment mismatch(es)")
    critical_issues += 1

if issues['baggage_without_passengers']:
    print(f"❌ {len(issues['baggage_without_passengers'])} baggage record(s) without valid passengers")
    critical_issues += 1

if critical_issues == 0:
    print("✓ NO CRITICAL ISSUES FOUND - All data linkages are properly maintained!")
else:
    print(f"\n⚠️ Total critical issues found: {critical_issues}")

print("\n" + "="*100)
