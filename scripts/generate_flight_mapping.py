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

print("\n" + "="*120)
print("FLIGHT-BY-FLIGHT DATA LINKAGE MAPPING")
print("="*120)

# Create detailed mapping
for flight_num in sorted(flights.keys()):
    flight = flights[flight_num]
    pax_list = passengers.get(flight_num, [])
    bkg_list = bookings.get(flight_num, [])
    cargo_list = cargo.get(flight_num, [])
    baggage_list = baggage.get(flight_num, [])
    
    print(f"\n{flight_num.ljust(8)} | {flight.get('origin_code', '???').ljust(3)} → {flight.get('destination_code', '???').ljust(3)} | {flight.get('aircraft_code', '?????').ljust(8)} | PAX:{str(len(pax_list)).ljust(2)} BKG:{str(len(bkg_list)).ljust(2)} CARGO:{str(len(cargo_list)).ljust(2)} BAG:{str(len(baggage_list)).ljust(2)}", end="")
    
    # Status indicators
    status_chars = []
    if len(pax_list) == 0:
        status_chars.append("❌PAX")
    elif len(pax_list) > 0:
        status_chars.append("✓PAX")
    
    if len(bkg_list) == 0:
        status_chars.append("❌BKG")
    elif len(bkg_list) > 0:
        # Check for orphaned bookings
        orphaned = sum(1 for b in bkg_list if b['passenger_id'] not in [p['passenger_id'] for p in pax_list])
        if orphaned > 0:
            status_chars.append(f"⚠️BKG({orphaned}orph)")
        else:
            status_chars.append("✓BKG")
    
    if len(cargo_list) > 0:
        status_chars.append("✓CARGO")
    
    if len(baggage_list) == 0 and len(pax_list) > 0:
        status_chars.append("❌BAG")
    elif len(baggage_list) > 0:
        status_chars.append("✓BAG")
    
    print(f" | {' '.join(status_chars)}")

print("\n" + "="*120)
print("\nLEGEND:")
print("  ✓ = Data present and properly linked")
print("  ❌ = Data missing or broken linkage")
print("  ⚠️ = Data present but has issues")
print("  orph = Orphaned records (reference non-existent data)")
print("\n" + "="*120)

# Export detailed mapping to file
print("\n\nGenerating detailed CSV mapping file...")

with open('FLIGHT_DATA_LINKAGE_MAPPING.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Flight', 'Origin', 'Destination', 'Aircraft', 'Passengers', 'Bookings', 'Cargo', 'Baggage', 
                     'Pax_Status', 'Bkg_Status', 'Cargo_Status', 'Bag_Status', 'Data_Complete'])
    
    for flight_num in sorted(flights.keys()):
        flight = flights[flight_num]
        pax_list = passengers.get(flight_num, [])
        bkg_list = bookings.get(flight_num, [])
        cargo_list = cargo.get(flight_num, [])
        baggage_list = baggage.get(flight_num, [])
        
        # Determine statuses
        pax_status = "PRESENT" if pax_list else "MISSING"
        bkg_status = "PRESENT" if bkg_list else "MISSING"
        cargo_status = "PRESENT" if cargo_list else "ABSENT"
        bag_status = "PRESENT" if baggage_list else "MISSING" if pax_list else "ABSENT"
        
        # Check for orphaned bookings
        if bkg_list:
            orphaned = sum(1 for b in bkg_list if b['passenger_id'] not in [p['passenger_id'] for p in pax_list])
            if orphaned > 0:
                bkg_status = f"BROKEN({orphaned}_ORPHANED)"
        
        # Check if all data is complete
        data_complete = pax_status == "PRESENT" and bkg_status == "PRESENT" and bag_status == "PRESENT"
        
        writer.writerow([
            flight_num,
            flight.get('origin_code', ''),
            flight.get('destination_code', ''),
            flight.get('aircraft_code', ''),
            len(pax_list),
            len(bkg_list),
            len(cargo_list),
            len(baggage_list),
            pax_status,
            bkg_status,
            cargo_status,
            bag_status,
            "YES" if data_complete else "NO"
        ])

print("✓ Mapping file created: FLIGHT_DATA_LINKAGE_MAPPING.csv")
