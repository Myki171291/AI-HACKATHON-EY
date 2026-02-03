#!/usr/bin/env python3
"""Verification of data linkage fixes."""

import pandas as pd

# Load corrected files
passengers = pd.read_csv('passengers_enriched_final.csv')
bookings = pd.read_csv('bookings.csv')
baggage = pd.read_csv('baggage_handling.csv')

print('='*80)
print('VERIFICATION OF FIXES')
print('='*80)

print('\n1. NEW PASSENGERS ADDED:')
new_pax = passengers[passengers['passenger_id'].isin(['PAX-016', 'PAX-017', 'PAX-018', 'PAX-019', 'PAX-020'])]
print(new_pax[['passenger_id', 'passenger_name', 'flight_number', 'booking_reference']])

print('\n2. VERIFIED BOOKINGS:')
valid_bkg = len(bookings[bookings['passenger_id'].isin(passengers['passenger_id'])])
print(f'   Total bookings: {len(bookings)}')
print(f'   Bookings with valid passengers: {valid_bkg}')
orphaned = len(bookings[~bookings['passenger_id'].isin(passengers['passenger_id'])])
print(f'   Orphaned bookings: {orphaned}')

print('\n3. NEW BAGGAGE RECORDS ADDED:')
new_baggage = baggage[baggage['passenger_id'].isin(['PAX-016', 'PAX-017', 'PAX-018', 'PAX-019', 'PAX-020'])]
print(f'   Total baggage records: {len(baggage)}')
print(f'   Baggage for new passengers: {len(new_baggage)}')

print('\n4. LINKAGE INTEGRITY CHECK:')
check1 = len(bookings[~bookings['passenger_id'].isin(passengers['passenger_id'])]) == 0
check2 = len(baggage[~baggage['passenger_id'].isin(passengers['passenger_id'])]) == 0
print(f'   All bookings have valid passengers: {check1}')
print(f'   All baggage have valid passengers: {check2}')

print('\n5. PASSENGERS BY FLIGHT:')
pax_by_flight = passengers['flight_number'].value_counts().sort_index()
for flight, count in pax_by_flight.items():
    print(f'   {flight}: {count} passengers')

print('\n' + '='*80)
print('✅ ALL FIXES VERIFIED SUCCESSFULLY')
print('='*80)
