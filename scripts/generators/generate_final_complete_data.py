"""
Generate COMPLETE scenario data with ALL DynamoDB columns for all 11 scenarios.
All files synced by: flight_id, flight_number, aircraft_registration, passenger_id, booking_id, scenario_id

DynamoDB Column Sources:
- passengers.csv: 54 columns
- MaintenanceWorkOrders.csv: 29 columns  
- flights.csv: 43 columns
"""
import pandas as pd
import random
import os
from datetime import datetime, timedelta
import json
import uuid

OUTPUT_DIR = '../complete_output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)

# Aircraft fleet with full details
AIRCRAFT = {
    'A6-EYA': {'type': 'A380', 'type_id': 1, 'code': 'A380', 'capacity': 516, 'cargo': 16000, 'crew': 16},
    'A6-EYB': {'type': 'A380', 'type_id': 1, 'code': 'A380', 'capacity': 516, 'cargo': 16000, 'crew': 16},
    'A6-EYC': {'type': 'A380', 'type_id': 1, 'code': 'A380', 'capacity': 516, 'cargo': 16000, 'crew': 16},
    'A6-EYD': {'type': 'B777X', 'type_id': 2, 'code': 'B777X', 'capacity': 400, 'cargo': 14000, 'crew': 14},
    'A6-EYE': {'type': 'B777X', 'type_id': 2, 'code': 'B777X', 'capacity': 400, 'cargo': 14000, 'crew': 14},
    'A6-EYF': {'type': 'B787-10', 'type_id': 3, 'code': 'B787-10', 'capacity': 330, 'cargo': 12000, 'crew': 10},
    'A6-EYG': {'type': 'B787-10', 'type_id': 3, 'code': 'B787-10', 'capacity': 330, 'cargo': 12000, 'crew': 10},
    'A6-EYH': {'type': 'B787-10', 'type_id': 3, 'code': 'B787-10', 'capacity': 330, 'cargo': 12000, 'crew': 10},
    'A6-EYI': {'type': 'B787-10', 'type_id': 3, 'code': 'B787-10', 'capacity': 330, 'cargo': 12000, 'crew': 10},
    'A6-EYJ': {'type': 'B787-10', 'type_id': 3, 'code': 'B787-10', 'capacity': 330, 'cargo': 12000, 'crew': 10},
    'A6-EYK': {'type': 'A350', 'type_id': 4, 'code': 'A350', 'capacity': 350, 'cargo': 13000, 'crew': 12},
    'A6-EYL': {'type': 'A350', 'type_id': 4, 'code': 'A350', 'capacity': 350, 'cargo': 13000, 'crew': 12},
    'A6-EYM': {'type': 'A350', 'type_id': 4, 'code': 'A350', 'capacity': 350, 'cargo': 13000, 'crew': 12},
    'A6-EYN': {'type': 'A321LR', 'type_id': 5, 'code': 'A321LR', 'capacity': 206, 'cargo': 4200, 'crew': 6},
    'A6-EYO': {'type': 'A321LR', 'type_id': 5, 'code': 'A321LR', 'capacity': 206, 'cargo': 4200, 'crew': 6},
    'A6-EYP': {'type': 'A321LR', 'type_id': 5, 'code': 'A321LR', 'capacity': 206, 'cargo': 4200, 'crew': 6},
    'A6-EYQ': {'type': 'A320', 'type_id': 6, 'code': 'A320', 'capacity': 180, 'cargo': 3500, 'crew': 4},
    'A6-EYR': {'type': 'A320', 'type_id': 6, 'code': 'A320', 'capacity': 180, 'cargo': 3500, 'crew': 4},
    'A6-EYS': {'type': 'A320', 'type_id': 6, 'code': 'A320', 'capacity': 180, 'cargo': 3500, 'crew': 4},
    'A6-EYT': {'type': 'A320', 'type_id': 6, 'code': 'A320', 'capacity': 180, 'cargo': 3500, 'crew': 4},
    'A6-EYU': {'type': 'A320', 'type_id': 6, 'code': 'A320', 'capacity': 180, 'cargo': 3500, 'crew': 4},
    'A6-EYV': {'type': 'A320', 'type_id': 6, 'code': 'A320', 'capacity': 180, 'cargo': 3500, 'crew': 4},
}

AIRPORTS = {
    'AUH': {'name': 'Abu Dhabi International', 'id': 1, 'tz': 4},
    'BKK': {'name': 'Suvarnabhumi', 'id': 2, 'tz': 7},
    'LHR': {'name': 'Heathrow', 'id': 3, 'tz': 0},
    'SIN': {'name': 'Changi', 'id': 4, 'tz': 8},
    'CDG': {'name': 'Charles de Gaulle', 'id': 5, 'tz': 1},
    'FRA': {'name': 'Frankfurt', 'id': 6, 'tz': 1},
    'JFK': {'name': 'John F Kennedy', 'id': 7, 'tz': -5},
    'DEL': {'name': 'Indira Gandhi', 'id': 8, 'tz': 5.5},
    'SYD': {'name': 'Sydney Kingsford Smith', 'id': 9, 'tz': 11},
    'CAI': {'name': 'Cairo International', 'id': 10, 'tz': 2},
    'FCO': {'name': 'Fiumicino', 'id': 11, 'tz': 1},
    'DOH': {'name': 'Hamad International', 'id': 12, 'tz': 3},
    'MCT': {'name': 'Muscat International', 'id': 13, 'tz': 4},
    'JED': {'name': 'King Abdulaziz', 'id': 14, 'tz': 3},
}

FIRST_NAMES = ['Ahmed', 'Mohammed', 'Fatima', 'Sara', 'Omar', 'Layla', 'Yusuf', 'Aisha', 'Hassan', 'Maryam',
               'John', 'Emma', 'Michael', 'Sophia', 'David', 'Olivia', 'James', 'Isabella', 'Robert', 'Mia',
               'Raj', 'Priya', 'Arjun', 'Ananya', 'Wei', 'Mei', 'Hiroshi', 'Yuki', 'Carlos', 'Maria']
LAST_NAMES = ['Al-Rashid', 'Khan', 'Smith', 'Johnson', 'Williams', 'Brown', 'Garcia', 'Martinez', 'Lee', 'Kim',
              'Patel', 'Singh', 'Wang', 'Chen', 'Tanaka', 'Yamamoto', 'Mueller', 'Schmidt', 'Rossi', 'Ferrari']
NATIONALITIES = ['UAE', 'USA', 'GBR', 'IND', 'CHN', 'JPN', 'DEU', 'FRA', 'ITA', 'AUS', 'SAU', 'EGY', 'PAK', 'BRA']
CABIN_CLASSES = ['First', 'Business', 'Economy']
MEAL_PREFS = ['Standard', 'Vegetarian', 'Vegan', 'Halal', 'Kosher', 'Gluten-Free', 'Continental']
BEVERAGES = ['Water', 'Coffee', 'Tea', 'Orange Juice', 'Champagne', 'Red Wine', 'White Wine', 'Hot Latte', 'Cappuccino']
LANGUAGES = ['English', 'Arabic', 'Hindi', 'Mandarin', 'Spanish', 'French', 'German', 'Japanese', 'Portuguese', 'Malayalam']
PROFESSIONS = ['Engineer', 'Doctor', 'Lawyer', 'Teacher', 'CEO', 'Consultant', 'Investment_Banker', 'Pilot', 'Artist', 'Student']
FF_TIERS = ['Gold', 'Silver', 'Platinum', 'Diamond', 'Basic']
PASSENGER_CATEGORIES = ['Regular', 'VIP', 'UMNR', 'Wheelchair', 'Medical', 'Infant']

# All 11 scenarios with exact flights from requirements
SCENARIOS = [
    {
        'id': 1, 'name': 'Bangkok Typhoon + Critical MEL Aircraft', 'date': '2026-01-19', 'event_type': 'WEATHER',
        'primary': [
            {'fn': 'EY117', 'orig': 'BKK', 'dest': 'AUH', 'ac': 'A6-EYV', 'delay': 180, 'issue': 'Cannot depart due to typhoon'},
            {'fn': 'EY5293', 'orig': 'AUH', 'dest': 'BKK', 'ac': 'A6-EYU', 'delay': 180, 'issue': 'LIAC - Late Inbound Aircraft'},
        ],
        'secondary': [
            {'fn': 'EY454', 'orig': 'AUH', 'dest': 'SYD', 'ac': 'A6-EYA', 'delay': 45, 'issue': 'Missed connections from EY117'},
            {'fn': 'EY334', 'orig': 'AUH', 'dest': 'CDG', 'ac': 'A6-EYJ', 'delay': 30, 'issue': 'Missed connections from EY117'},
            {'fn': 'EY25', 'orig': 'AUH', 'dest': 'LHR', 'ac': 'A6-EYF', 'delay': 25, 'issue': 'Missed connections from EY117'},
            {'fn': 'EY101', 'orig': 'AUH', 'dest': 'JFK', 'ac': 'A6-EYB', 'delay': 40, 'issue': 'Missed connections from EY117'},
            {'fn': 'EY170', 'orig': 'AUH', 'dest': 'DEL', 'ac': 'A6-EYQ', 'delay': 20, 'issue': 'Missed connections from EY117'},
            {'fn': 'EY472', 'orig': 'AUH', 'dest': 'SIN', 'ac': 'A6-EYH', 'delay': 35, 'issue': 'Missed connections from EY117'},
            {'fn': 'EY313', 'orig': 'AUH', 'dest': 'JED', 'ac': 'A6-EYN', 'delay': 15, 'issue': 'Missed connections from EY117'},
            {'fn': 'EY424', 'orig': 'AUH', 'dest': 'SIN', 'ac': 'A6-EYO', 'delay': 30, 'issue': 'Missed connections from EY117'},
        ],
        'weather': {'condition': 'TYPHOON', 'wind': 85, 'vis': 500, 'temp': 28}
    },
    {
        'id': 2, 'name': 'London Fog + Multiple Aircraft AOG', 'date': '2026-01-20', 'event_type': 'WEATHER',
        'primary': [
            {'fn': 'EY8184', 'orig': 'AUH', 'dest': 'LHR', 'ac': 'A6-EYK', 'delay': 120, 'issue': 'Fog delays arrival'},
            {'fn': 'EY6268', 'orig': 'AUH', 'dest': 'LHR', 'ac': 'A6-EYL', 'delay': 180, 'issue': 'Fog delays arrival'},
            {'fn': 'EY25', 'orig': 'LHR', 'dest': 'AUH', 'ac': 'A6-EYF', 'delay': 240, 'issue': 'Cannot depart due to fog'},
            {'fn': 'EY19', 'orig': 'LHR', 'dest': 'AUH', 'ac': 'A6-EYG', 'delay': 300, 'issue': 'Cannot depart due to fog'},
            {'fn': 'EY11', 'orig': 'LHR', 'dest': 'AUH', 'ac': 'A6-EYH', 'delay': 360, 'issue': 'Cannot depart due to fog'},
        ],
        'secondary': [
            {'fn': 'EY26', 'orig': 'AUH', 'dest': 'LHR', 'ac': 'A6-EYF', 'delay': 240, 'issue': 'LIAC from EY25'},
            {'fn': 'EY20', 'orig': 'AUH', 'dest': 'LHR', 'ac': 'A6-EYG', 'delay': 300, 'issue': 'LIAC from EY19'},
            {'fn': 'EY12', 'orig': 'AUH', 'dest': 'LHR', 'ac': 'A6-EYH', 'delay': 360, 'issue': 'LIAC from EY11'},
            {'fn': 'EY334', 'orig': 'AUH', 'dest': 'CDG', 'ac': 'A6-EYI', 'delay': 60, 'issue': 'AOG aircraft swap'},
            {'fn': 'EY1202', 'orig': 'AUH', 'dest': 'DEL', 'ac': 'A6-EYJ', 'delay': 45, 'issue': 'AOG aircraft swap'},
            {'fn': 'EY639', 'orig': 'AUH', 'dest': 'JFK', 'ac': 'A6-EYA', 'delay': 90, 'issue': 'AOG aircraft swap'},
            {'fn': 'EY454', 'orig': 'AUH', 'dest': 'SYD', 'ac': 'A6-EYB', 'delay': 75, 'issue': 'Missed connections'},
        ],
        'weather': {'condition': 'FOG', 'wind': 5, 'vis': 100, 'temp': 4}
    },
    {
        'id': 3, 'name': 'Singapore Thunderstorms + MEL Expiry Cascade', 'date': '2026-01-21', 'event_type': 'WEATHER',
        'primary': [
            {'fn': 'EY3105', 'orig': 'AUH', 'dest': 'SIN', 'ac': 'A6-EYM', 'delay': 90, 'issue': 'Thunderstorm delays'},
            {'fn': 'EY472', 'orig': 'SIN', 'dest': 'AUH', 'ac': 'A6-EYH', 'delay': 120, 'issue': 'Cannot depart due to storms'},
            {'fn': 'EY424', 'orig': 'AUH', 'dest': 'SIN', 'ac': 'A6-EYN', 'delay': 180, 'issue': 'MEL expiry forces aircraft swap'},
            {'fn': 'EY868', 'orig': 'SIN', 'dest': 'AUH', 'ac': 'A6-EYO', 'delay': 180, 'issue': 'MEL expiry forces aircraft swap'},
        ],
        'secondary': [
            {'fn': 'EY473', 'orig': 'AUH', 'dest': 'SIN', 'ac': 'A6-EYH', 'delay': 120, 'issue': 'LIAC from EY472'},
            {'fn': 'EY425', 'orig': 'SIN', 'dest': 'AUH', 'ac': 'A6-EYN', 'delay': 180, 'issue': 'LIAC from EY424'},
            {'fn': 'EY869', 'orig': 'AUH', 'dest': 'SIN', 'ac': 'A6-EYO', 'delay': 180, 'issue': 'LIAC from EY868'},
            {'fn': 'EY334', 'orig': 'AUH', 'dest': 'CDG', 'ac': 'A6-EYJ', 'delay': 45, 'issue': 'Missed connections from SIN'},
        ],
        'weather': {'condition': 'THUNDERSTORM', 'wind': 45, 'vis': 2000, 'temp': 30}
    },
    {
        'id': 4, 'name': 'Paris Winter Storm + Temperature-Controlled Cargo Crisis', 'date': '2026-01-22', 'event_type': 'WEATHER',
        'primary': [
            {'fn': 'EY2796', 'orig': 'AUH', 'dest': 'CDG', 'ac': 'A6-EYI', 'delay': 240, 'issue': 'Winter storm delays'},
            {'fn': 'EY334', 'orig': 'AUH', 'dest': 'CDG', 'ac': 'A6-EYJ', 'delay': 300, 'issue': 'Winter storm delays'},
            {'fn': 'EY1677', 'orig': 'AUH', 'dest': 'CDG', 'ac': 'A6-EYK', 'delay': 360, 'issue': 'Winter storm delays'},
            {'fn': 'EY462', 'orig': 'AUH', 'dest': 'FRA', 'ac': 'A6-EYL', 'delay': 180, 'issue': 'Diverted due to CDG closure'},
        ],
        'secondary': [
            {'fn': 'EY2797', 'orig': 'CDG', 'dest': 'AUH', 'ac': 'A6-EYI', 'delay': 240, 'issue': 'LIAC from EY2796'},
            {'fn': 'EY335', 'orig': 'CDG', 'dest': 'AUH', 'ac': 'A6-EYJ', 'delay': 300, 'issue': 'LIAC from EY334'},
            {'fn': 'EY1678', 'orig': 'CDG', 'dest': 'AUH', 'ac': 'A6-EYK', 'delay': 360, 'issue': 'LIAC from EY1677'},
            {'fn': 'EY463', 'orig': 'FRA', 'dest': 'AUH', 'ac': 'A6-EYL', 'delay': 180, 'issue': 'LIAC from EY462'},
        ],
        'weather': {'condition': 'WINTER_STORM', 'wind': 55, 'vis': 800, 'temp': -5}
    },
]

# Scenarios 5-8
SCENARIOS.extend([
    {
        'id': 5, 'name': 'Dubai Sandstorm + Hub Congestion + Multiple MEL Aircraft', 'date': '2026-01-23', 'event_type': 'WEATHER',
        'primary': [
            {'fn': 'EY8396', 'orig': 'AUH', 'dest': 'DOH', 'ac': 'A6-EYM', 'delay': 120, 'issue': 'Sandstorm causes diversion'},
            {'fn': 'EY4943', 'orig': 'AUH', 'dest': 'DOH', 'ac': 'A6-EYN', 'delay': 90, 'issue': 'Hub congestion delays'},
            {'fn': 'EY912', 'orig': 'JFK', 'dest': 'AUH', 'ac': 'A6-EYA', 'delay': 180, 'issue': 'Delayed due to congestion'},
            {'fn': 'EY639', 'orig': 'AUH', 'dest': 'JFK', 'ac': 'A6-EYB', 'delay': 240, 'issue': 'MEL aircraft + congestion'},
            {'fn': 'EY432', 'orig': 'LHR', 'dest': 'AUH', 'ac': 'A6-EYF', 'delay': 150, 'issue': 'Diverted to AUH'},
            {'fn': 'EY8184', 'orig': 'AUH', 'dest': 'LHR', 'ac': 'A6-EYG', 'delay': 90, 'issue': 'Delayed departure'},
            {'fn': 'EY1202', 'orig': 'AUH', 'dest': 'DEL', 'ac': 'A6-EYH', 'delay': 180, 'issue': 'MEL aircraft swap'},
            {'fn': 'EY170', 'orig': 'AUH', 'dest': 'DEL', 'ac': 'A6-EYQ', 'delay': 120, 'issue': 'Delayed due to congestion'},
        ],
        'secondary': [
            {'fn': 'EY8397', 'orig': 'DOH', 'dest': 'AUH', 'ac': 'A6-EYM', 'delay': 120, 'issue': 'LIAC from EY8396'},
            {'fn': 'EY4944', 'orig': 'DOH', 'dest': 'AUH', 'ac': 'A6-EYN', 'delay': 90, 'issue': 'LIAC from EY4943'},
            {'fn': 'EY913', 'orig': 'AUH', 'dest': 'JFK', 'ac': 'A6-EYA', 'delay': 180, 'issue': 'LIAC from EY912'},
            {'fn': 'EY433', 'orig': 'AUH', 'dest': 'LHR', 'ac': 'A6-EYF', 'delay': 150, 'issue': 'LIAC from EY432'},
            {'fn': 'EY1203', 'orig': 'DEL', 'dest': 'AUH', 'ac': 'A6-EYH', 'delay': 180, 'issue': 'LIAC from EY1202'},
            {'fn': 'EY171', 'orig': 'DEL', 'dest': 'AUH', 'ac': 'A6-EYQ', 'delay': 120, 'issue': 'LIAC from EY170'},
        ],
        'weather': {'condition': 'SANDSTORM', 'wind': 65, 'vis': 200, 'temp': 38}
    },
    {
        'id': 6, 'name': 'Multiple Aircraft AOG + Engine Failure Cascade', 'date': '2026-01-24', 'event_type': 'TECHNICAL',
        'primary': [
            {'fn': 'EY7151', 'orig': 'AUH', 'dest': 'CAI', 'ac': 'A6-EYD', 'delay': 480, 'issue': 'No aircraft (B777X AOG)'},
            {'fn': 'EY3102', 'orig': 'AUH', 'dest': 'FCO', 'ac': 'A6-EYE', 'delay': 480, 'issue': 'No aircraft (B777X AOG)'},
            {'fn': 'EY003', 'orig': 'AUH', 'dest': 'DEL', 'ac': 'A6-EYK', 'delay': 480, 'issue': 'No aircraft (B777X AOG)'},
        ],
        'secondary': [
            {'fn': 'EY7152', 'orig': 'CAI', 'dest': 'AUH', 'ac': 'A6-EYD', 'delay': 480, 'issue': 'LIAC from EY7151'},
            {'fn': 'EY3103', 'orig': 'FCO', 'dest': 'AUH', 'ac': 'A6-EYE', 'delay': 480, 'issue': 'LIAC from EY3102'},
            {'fn': 'EY004', 'orig': 'DEL', 'dest': 'AUH', 'ac': 'A6-EYK', 'delay': 480, 'issue': 'LIAC from EY003'},
            {'fn': 'EY8086', 'orig': 'AUH', 'dest': 'FCO', 'ac': 'A6-EYL', 'delay': 120, 'issue': 'Fleet inspection delay'},
            {'fn': 'EY912', 'orig': 'JFK', 'dest': 'AUH', 'ac': 'A6-EYA', 'delay': 45, 'issue': 'Runway closure 45min'},
        ],
        'weather': {'condition': 'CLEAR', 'wind': 10, 'vis': 10000, 'temp': 25}
    },
    {
        'id': 7, 'name': 'Crew Out of Hours + Insufficient Cabin Crew Crisis', 'date': '2026-01-25', 'event_type': 'CREW',
        'primary': [
            {'fn': 'EY8086', 'orig': 'AUH', 'dest': 'FCO', 'ac': 'A6-EYI', 'delay': 300, 'issue': 'Crew FDP exceeded'},
            {'fn': 'EY6622', 'orig': 'DEL', 'dest': 'AUH', 'ac': 'A6-EYJ', 'delay': 240, 'issue': 'Crew FDP exceeded'},
            {'fn': 'EY0739', 'orig': 'AUH', 'dest': 'SYD', 'ac': 'A6-EYA', 'delay': 360, 'issue': 'Insufficient cabin crew'},
            {'fn': 'EY432', 'orig': 'LHR', 'dest': 'AUH', 'ac': 'A6-EYF', 'delay': 180, 'issue': 'Crew FDP exceeded'},
            {'fn': 'EY1202', 'orig': 'AUH', 'dest': 'DEL', 'ac': 'A6-EYH', 'delay': 240, 'issue': 'Insufficient cabin crew'},
            {'fn': 'EY334', 'orig': 'AUH', 'dest': 'CDG', 'ac': 'A6-EYK', 'delay': 300, 'issue': 'Crew FDP exceeded'},
        ],
        'secondary': [
            {'fn': 'EY8087', 'orig': 'FCO', 'dest': 'AUH', 'ac': 'A6-EYI', 'delay': 300, 'issue': 'LIAC from EY8086'},
            {'fn': 'EY0740', 'orig': 'SYD', 'dest': 'AUH', 'ac': 'A6-EYA', 'delay': 360, 'issue': 'LIAC from EY0739'},
            {'fn': 'EY433', 'orig': 'AUH', 'dest': 'LHR', 'ac': 'A6-EYF', 'delay': 180, 'issue': 'LIAC from EY432'},
            {'fn': 'EY335', 'orig': 'CDG', 'dest': 'AUH', 'ac': 'A6-EYK', 'delay': 300, 'issue': 'LIAC from EY334'},
        ],
        'weather': {'condition': 'CLEAR', 'wind': 8, 'vis': 10000, 'temp': 22}
    },
    {
        'id': 8, 'name': 'Runway Closure + Airspace Flow Rate Restrictions', 'date': '2026-01-27', 'event_type': 'OPERATIONAL',
        'primary': [
            {'fn': 'EY8086', 'orig': 'AUH', 'dest': 'FCO', 'ac': 'A6-EYI', 'delay': 60, 'issue': 'Departure delayed'},
            {'fn': 'EY4943', 'orig': 'AUH', 'dest': 'DOH', 'ac': 'A6-EYM', 'delay': 45, 'issue': 'Departure delayed'},
            {'fn': 'EY9626', 'orig': 'CAI', 'dest': 'AUH', 'ac': 'A6-EYN', 'delay': 90, 'issue': 'Arrival delayed'},
            {'fn': 'EY432', 'orig': 'LHR', 'dest': 'AUH', 'ac': 'A6-EYF', 'delay': 75, 'issue': 'Arrival delayed'},
            {'fn': 'EY1202', 'orig': 'AUH', 'dest': 'DEL', 'ac': 'A6-EYH', 'delay': 60, 'issue': 'Departure delayed'},
            {'fn': 'EY8184', 'orig': 'AUH', 'dest': 'LHR', 'ac': 'A6-EYG', 'delay': 90, 'issue': 'Departure delayed'},
            {'fn': 'EY912', 'orig': 'JFK', 'dest': 'AUH', 'ac': 'A6-EYA', 'delay': 120, 'issue': 'Arrival delayed'},
            {'fn': 'EY0739', 'orig': 'AUH', 'dest': 'SYD', 'ac': 'A6-EYB', 'delay': 75, 'issue': 'Departure delayed'},
            {'fn': 'EY6622', 'orig': 'DEL', 'dest': 'AUH', 'ac': 'A6-EYJ', 'delay': 60, 'issue': 'Arrival delayed'},
            {'fn': 'EY5265', 'orig': 'FCO', 'dest': 'AUH', 'ac': 'A6-EYK', 'delay': 90, 'issue': 'Arrival delayed'},
            {'fn': 'EY6005', 'orig': 'DEL', 'dest': 'AUH', 'ac': 'A6-EYL', 'delay': 45, 'issue': 'Arrival delayed'},
            {'fn': 'EY2796', 'orig': 'AUH', 'dest': 'CDG', 'ac': 'A6-EYO', 'delay': 60, 'issue': 'Departure delayed'},
        ],
        'secondary': [
            {'fn': 'EY913', 'orig': 'AUH', 'dest': 'JFK', 'ac': 'A6-EYA', 'delay': 120, 'issue': 'LIAC from EY912'},
            {'fn': 'EY433', 'orig': 'AUH', 'dest': 'LHR', 'ac': 'A6-EYF', 'delay': 75, 'issue': 'LIAC from EY432'},
        ],
        'weather': {'condition': 'CLEAR', 'wind': 12, 'vis': 10000, 'temp': 24}
    },
])

# Scenarios 9-11
SCENARIOS.extend([
    {
        'id': 9, 'name': 'Security Threat + Geopolitical Airspace Diversion', 'date': '2026-01-28', 'event_type': 'SECURITY',
        'primary': [
            {'fn': 'EY8086', 'orig': 'AUH', 'dest': 'FCO', 'ac': 'A6-EYI', 'delay': 180, 'issue': 'Terminal evacuation delay'},
            {'fn': 'EY8184', 'orig': 'AUH', 'dest': 'LHR', 'ac': 'A6-EYG', 'delay': 180, 'issue': 'Terminal evacuation delay'},
            {'fn': 'EY912', 'orig': 'AUH', 'dest': 'JFK', 'ac': 'A6-EYA', 'delay': 240, 'issue': 'Airspace diversion required'},
            {'fn': 'EY334', 'orig': 'AUH', 'dest': 'CDG', 'ac': 'A6-EYJ', 'delay': 180, 'issue': 'Terminal evacuation delay'},
            {'fn': 'EY1202', 'orig': 'AUH', 'dest': 'DEL', 'ac': 'A6-EYH', 'delay': 240, 'issue': 'Airspace diversion required'},
            {'fn': 'EY170', 'orig': 'AUH', 'dest': 'DEL', 'ac': 'A6-EYQ', 'delay': 240, 'issue': 'Airspace diversion required'},
            {'fn': 'EY432', 'orig': 'LHR', 'dest': 'AUH', 'ac': 'A6-EYF', 'delay': 150, 'issue': 'Arrival delayed (terminal closure)'},
            {'fn': 'EY6622', 'orig': 'DEL', 'dest': 'AUH', 'ac': 'A6-EYK', 'delay': 150, 'issue': 'Arrival delayed (terminal closure)'},
            {'fn': 'EY5265', 'orig': 'FCO', 'dest': 'AUH', 'ac': 'A6-EYL', 'delay': 150, 'issue': 'Arrival delayed (terminal closure)'},
            {'fn': 'EY3160', 'orig': 'FCO', 'dest': 'AUH', 'ac': 'A6-EYM', 'delay': 150, 'issue': 'Arrival delayed (terminal closure)'},
            {'fn': 'EY6005', 'orig': 'DEL', 'dest': 'AUH', 'ac': 'A6-EYN', 'delay': 150, 'issue': 'Arrival delayed (terminal closure)'},
            {'fn': 'EY117', 'orig': 'BKK', 'dest': 'AUH', 'ac': 'A6-EYV', 'delay': 150, 'issue': 'Arrival delayed (terminal closure)'},
        ],
        'secondary': [
            {'fn': 'EY913', 'orig': 'JFK', 'dest': 'AUH', 'ac': 'A6-EYA', 'delay': 240, 'issue': 'LIAC from EY912'},
            {'fn': 'EY433', 'orig': 'AUH', 'dest': 'LHR', 'ac': 'A6-EYF', 'delay': 150, 'issue': 'LIAC from EY432'},
            {'fn': 'EY335', 'orig': 'CDG', 'dest': 'AUH', 'ac': 'A6-EYJ', 'delay': 180, 'issue': 'LIAC from EY334'},
            {'fn': 'EY1203', 'orig': 'DEL', 'dest': 'AUH', 'ac': 'A6-EYH', 'delay': 240, 'issue': 'LIAC from EY1202'},
            {'fn': 'EY171', 'orig': 'DEL', 'dest': 'AUH', 'ac': 'A6-EYQ', 'delay': 240, 'issue': 'LIAC from EY170'},
            {'fn': 'EY8087', 'orig': 'FCO', 'dest': 'AUH', 'ac': 'A6-EYI', 'delay': 180, 'issue': 'LIAC from EY8086'},
            {'fn': 'EY8185', 'orig': 'LHR', 'dest': 'AUH', 'ac': 'A6-EYG', 'delay': 180, 'issue': 'LIAC from EY8184'},
            {'fn': 'EY118', 'orig': 'AUH', 'dest': 'BKK', 'ac': 'A6-EYV', 'delay': 150, 'issue': 'LIAC from EY117'},
        ],
        'weather': {'condition': 'CLEAR', 'wind': 10, 'vis': 10000, 'temp': 26}
    },
    {
        'id': 10, 'name': 'Medical Emergency + Tarmac Delay + Slot Unavailability', 'date': '2026-01-29', 'event_type': 'MEDICAL',
        'primary': [
            {'fn': 'EY8086', 'orig': 'AUH', 'dest': 'FCO', 'ac': 'A6-EYI', 'delay': 300, 'issue': 'Diverted to MCT for medical emergency'},
        ],
        'secondary': [
            {'fn': 'EY8087', 'orig': 'FCO', 'dest': 'AUH', 'ac': 'A6-EYI', 'delay': 300, 'issue': 'LIAC from EY8086'},
            {'fn': 'EY334', 'orig': 'AUH', 'dest': 'CDG', 'ac': 'A6-EYJ', 'delay': 60, 'issue': 'Passengers rebooked from EY8086'},
        ],
        'weather': {'condition': 'CLEAR', 'wind': 8, 'vis': 10000, 'temp': 23}
    },
    {
        'id': 11, 'name': 'EY401 Typhoon → EY406 LIAC', 'date': '2026-01-31', 'event_type': 'WEATHER',
        'primary': [
            {'fn': 'EY401', 'orig': 'BKK', 'dest': 'AUH', 'ac': 'A6-EYU', 'delay': 180, 'issue': 'Typhoon delays departure'},
            {'fn': 'EY406', 'orig': 'AUH', 'dest': 'BKK', 'ac': 'A6-EYU', 'delay': 180, 'issue': 'LIAC - Late Inbound Aircraft Connection'},
        ],
        'secondary': [
            {'fn': 'EY454', 'orig': 'AUH', 'dest': 'SYD', 'ac': 'A6-EYA', 'delay': 45, 'issue': 'Missed connections from EY401'},
            {'fn': 'EY334', 'orig': 'AUH', 'dest': 'CDG', 'ac': 'A6-EYJ', 'delay': 30, 'issue': 'Missed connections from EY401'},
            {'fn': 'EY25', 'orig': 'AUH', 'dest': 'LHR', 'ac': 'A6-EYF', 'delay': 25, 'issue': 'Missed connections from EY401'},
            {'fn': 'EY101', 'orig': 'AUH', 'dest': 'JFK', 'ac': 'A6-EYB', 'delay': 40, 'issue': 'Missed connections from EY401'},
            {'fn': 'EY170', 'orig': 'AUH', 'dest': 'DEL', 'ac': 'A6-EYQ', 'delay': 20, 'issue': 'Missed connections from EY401'},
            {'fn': 'EY472', 'orig': 'AUH', 'dest': 'SIN', 'ac': 'A6-EYH', 'delay': 35, 'issue': 'Missed connections from EY401'},
            {'fn': 'EY313', 'orig': 'AUH', 'dest': 'JED', 'ac': 'A6-EYN', 'delay': 15, 'issue': 'Missed connections from EY401'},
            {'fn': 'EY424', 'orig': 'AUH', 'dest': 'SIN', 'ac': 'A6-EYO', 'delay': 30, 'issue': 'Missed connections from EY401'},
        ],
        'weather': {'condition': 'TYPHOON', 'wind': 80, 'vis': 600, 'temp': 29}
    },
])

# Global counters for IDs
flight_counter = 1000
passenger_counter = 1000
booking_counter = 1000
workorder_counter = 1000
crew_counter = 1000
cargo_counter = 1000

def generate_flights():
    """Generate flights with ALL 43 DynamoDB columns"""
    global flight_counter
    flights = []
    
    for scenario in SCENARIOS:
        base_date = datetime.strptime(scenario['date'], '%Y-%m-%d')
        all_flights = scenario['primary'] + scenario['secondary']
        
        # First pass: create basic flight data
        scenario_flights = []
        for i, flt in enumerate(all_flights):
            flight_counter += 1
            ac = AIRCRAFT[flt['ac']]
            orig = AIRPORTS[flt['orig']]
            dest = AIRPORTS[flt['dest']]
            
            # Calculate times
            dep_hour = 6 + (i * 2) % 18
            dep_time = base_date.replace(hour=dep_hour, minute=random.randint(0, 59))
            flight_duration = random.randint(3, 14)
            arr_time = dep_time + timedelta(hours=flight_duration)
            
            # MEL info for some flights
            has_mel = random.random() < 0.2
            mel_cat = random.choice(['A', 'B', 'C', 'D']) if has_mel else ''
            mel_days = random.randint(1, 10) if has_mel else None
            mel_expiry = (base_date + timedelta(days=mel_days)).strftime('%Y-%m-%d') if mel_days else ''
            
            is_primary = flt in scenario['primary']
            status = 'Delayed' if flt['delay'] > 60 else 'On-Time' if flt['delay'] < 30 else 'Scheduled'
            
            flight = {
                'flight_id': f"FLT-{flight_counter}",
                'flight_number': flt['fn'],
                'scenario_id': scenario['id'],
                'scenario_name': scenario['name'],
                'is_primary_disruption': 'Y' if is_primary else 'N',
                'disruption_reason': flt['issue'],
                'delay_minutes': flt['delay'],
                'aircraft_registration': flt['ac'],
                'aircraft_type_id': ac['type_id'],
                'aircraft_code': ac['code'],
                'aircraft_capacity': ac['capacity'],
                'aircraft_cargo_capacity': ac['cargo'],
                'cabin_crew_required': ac['crew'],
                'origin_airport_id': orig['id'],
                'origin_code': flt['orig'],
                'destination_airport_id': dest['id'],
                'destination_code': flt['dest'],
                'scheduled_departure': dep_time.strftime('%Y-%m-%d %H:%M:%S'),
                'scheduled_arrival': arr_time.strftime('%Y-%m-%d %H:%M:%S'),
                'arrival_time': (arr_time + timedelta(minutes=flt['delay'])).strftime('%Y-%m-%d %H:%M:%S'),
                'flight_status': status,
                'gate': f"{random.choice(['A', 'B', 'C', 'D'])}{random.randint(1, 30)}",
                'terminal': str(random.randint(1, 3)),
                'mel_status': 'ACTIVE' if has_mel else 'CLEAR',
                'mel_category': mel_cat,
                'mel_days_remaining': mel_days if mel_days else '',
                'mel_expiry_date': mel_expiry,
                'mel_item': f"MEL-{random.randint(100, 999)}" if has_mel else '',
                'mel_reference': f"REF-{random.randint(1000, 9999)}" if has_mel else '',
                'mel_reported_date': (base_date - timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%d') if has_mel else '',
                'mel_restrictions': 'Speed limited to M0.82' if has_mel else '',
                '_dep_time': dep_time,
                '_arr_time': arr_time,
                '_orig': flt['orig'],
                '_dest': flt['dest'],
                '_ac': flt['ac'],
            }
            scenario_flights.append(flight)
        
        # Second pass: assign upline/downline from other flights in same scenario
        for flight in scenario_flights:
            ac = flight['_ac']
            orig = flight['_orig']
            dest = flight['_dest']
            dep_time = flight['_dep_time']
            arr_time = flight['_arr_time']
            
            # Find upline: another flight with same aircraft arriving at this flight's origin
            upline_candidates = [f for f in scenario_flights 
                                if f['_ac'] == ac 
                                and f['_dest'] == orig 
                                and f['flight_id'] != flight['flight_id']
                                and f['_arr_time'] < dep_time]
            
            if upline_candidates:
                upline = random.choice(upline_candidates)
                upline_fn = upline['flight_number']
                upline_ac = upline['_ac']  # Use the upline flight's aircraft
                upline_dep_airport = upline['_orig']
                upline_arr_airport = upline['_dest']
                upline_dep_time = upline['_dep_time']
                upline_arr_time = upline['_arr_time']
            else:
                # Use another flight from same scenario - use THAT flight's aircraft
                other_flights = [f for f in scenario_flights if f['flight_id'] != flight['flight_id']]
                if other_flights:
                    upline = random.choice(other_flights)
                    upline_fn = upline['flight_number']
                    upline_ac = upline['_ac']  # Use the upline flight's aircraft
                    upline_dep_airport = upline['_orig']
                    upline_arr_airport = upline['_dest']
                    upline_dep_time = upline['_dep_time']
                    upline_arr_time = upline['_arr_time']
                else:
                    # Fallback to self-reference
                    upline_fn = flight['flight_number']
                    upline_ac = ac  # Same aircraft for self-reference
                    upline_dep_airport = orig
                    upline_arr_airport = orig
                    upline_dep_time = dep_time - timedelta(hours=2)
                    upline_arr_time = dep_time - timedelta(hours=1)
            
            # Find downline: another flight with same aircraft departing from this flight's destination
            downline_candidates = [f for f in scenario_flights 
                                  if f['_ac'] == ac 
                                  and f['_orig'] == dest 
                                  and f['flight_id'] != flight['flight_id']
                                  and f['_dep_time'] > arr_time]
            
            if downline_candidates:
                downline = random.choice(downline_candidates)
                downline_fn = downline['flight_number']
                downline_ac = downline['_ac']  # Use the downline flight's aircraft
                downline_dep_airport = downline['_orig']
                downline_arr_airport = downline['_dest']
                downline_dep_time = downline['_dep_time']
                downline_arr_time = downline['_arr_time']
            else:
                # Use another flight from same scenario - use THAT flight's aircraft
                other_flights = [f for f in scenario_flights if f['flight_id'] != flight['flight_id']]
                if other_flights:
                    downline = random.choice(other_flights)
                    downline_fn = downline['flight_number']
                    downline_ac = downline['_ac']  # Use the downline flight's aircraft
                    downline_dep_airport = downline['_orig']
                    downline_arr_airport = downline['_dest']
                    downline_dep_time = downline['_dep_time']
                    downline_arr_time = downline['_arr_time']
                else:
                    # Fallback to self-reference
                    downline_fn = flight['flight_number']
                    downline_ac = ac  # Same aircraft for self-reference
                    downline_dep_airport = dest
                    downline_arr_airport = dest
                    downline_dep_time = arr_time + timedelta(hours=1)
                    downline_arr_time = arr_time + timedelta(hours=4)
            
            # Add upline/downline data - use the referenced flight's aircraft registration
            flight['upline_aircraft_registration'] = upline_ac
            flight['upline_airline'] = 'EY'
            flight['upline_arrival_airport'] = upline_arr_airport
            flight['upline_departure_airport'] = upline_dep_airport
            flight['upline_flight_number'] = upline_fn
            flight['upline_sta_l'] = upline_arr_time.strftime('%Y-%m-%dT%H:%M:%S')
            flight['upline_sta_z'] = upline_arr_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            flight['upline_std_l'] = upline_dep_time.strftime('%Y-%m-%dT%H:%M:%S')
            flight['upline_std_z'] = upline_dep_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            flight['downline_aircraft_registration'] = downline_ac
            flight['downline_airline'] = 'EY'
            flight['downline_arrival_airport'] = downline_arr_airport
            flight['downline_departure_airport'] = downline_dep_airport
            flight['downline_flight_number'] = downline_fn
            flight['downline_sta_l'] = downline_arr_time.strftime('%Y-%m-%dT%H:%M:%S')
            flight['downline_sta_z'] = downline_arr_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            flight['downline_std_l'] = downline_dep_time.strftime('%Y-%m-%dT%H:%M:%S')
            flight['downline_std_z'] = downline_dep_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Third pass: remove temp fields and add to final list
        for flight in scenario_flights:
            del flight['_dep_time']
            del flight['_arr_time']
            del flight['_orig']
            del flight['_dest']
            del flight['_ac']
            
            flights.append(flight)
    
    return pd.DataFrame(flights)

def generate_passengers(flights_df):
    """Generate passengers with ALL 54 DynamoDB columns"""
    global passenger_counter, booking_counter
    passengers = []
    
    for _, flight in flights_df.iterrows():
        ac = AIRCRAFT.get(flight['aircraft_registration'], {'capacity': 200})
        num_pax = random.randint(int(ac['capacity'] * 0.6), int(ac['capacity'] * 0.95))
        
        for p in range(min(num_pax, 100)):  # Cap at 100 per flight for performance
            passenger_counter += 1
            booking_counter += 1
            
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            nationality = random.choice(NATIONALITIES)
            cabin = random.choice(CABIN_CLASSES)
            is_disrupted = flight['delay_minutes'] > 60
            is_vip = random.random() < 0.05
            has_medical = random.random() < 0.03
            
            # Rebook info for disrupted passengers
            rebook_status = ''
            rebook_flight = ''
            rebook_date = ''
            rebook_cabin = ''
            rebook_origin = ''
            rebook_dest = ''
            rebook_dep_time = ''
            rebook_arr_time = ''
            rebook_ac_type = ''
            compensation = 0
            
            if is_disrupted and random.random() < 0.7:
                rebook_status = random.choice(['CONFIRMED', 'PENDING', 'WAITLIST'])
                rebook_flight = f"EY{random.randint(100, 9999)}"
                base_date = datetime.strptime(flight['scheduled_departure'][:10], '%Y-%m-%d')
                rebook_date = (base_date + timedelta(days=random.randint(0, 2))).strftime('%Y-%m-%d')
                rebook_cabin = cabin
                rebook_origin = flight['destination_code']
                rebook_dest = random.choice(list(AIRPORTS.keys()))
                rebook_dep = base_date + timedelta(hours=random.randint(1, 24))
                rebook_dep_time = rebook_dep.strftime('%Y-%m-%dT%H:%M:%SZ')
                rebook_arr_time = (rebook_dep + timedelta(hours=random.randint(2, 12))).strftime('%Y-%m-%dT%H:%M:%SZ')
                rebook_ac_type = random.choice(['A380', 'B777X', 'A350', 'B787-10', 'A321LR', 'A320'])
                compensation = random.choice([0, 250, 400, 600, 800]) if flight['delay_minutes'] > 180 else 0
            
            pnr = f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))}{random.randint(100, 999)}"
            traveler_id = f"{pnr}-{flight['scheduled_departure'][:10]}-PT-{p+1}"
            
            passenger = {
                'passenger_id': f"PAX-{passenger_counter}",
                'traveler_id': traveler_id,
                'pnr': pnr,
                'booking_id': f"BKG-{booking_counter}",
                'flight_id': flight['flight_id'],
                'flight_number': flight['flight_number'],
                'scenario_id': flight['scenario_id'],
                'scenario_name': flight['scenario_name'],
                'aircraft_registration': flight['aircraft_registration'],
                'aircraft_type': AIRCRAFT.get(flight['aircraft_registration'], {}).get('type', 'A320'),
                'departure_airport': flight['destination_code'],
                'arrival_airport': random.choice(list(AIRPORTS.keys())),
                'departure_date': flight['scheduled_departure'][:10],
                'departure_time_zulu': flight['scheduled_departure'].replace(' ', 'T') + 'Z',
                'first_name': first,
                'last_name': last,
                'date_of_birth': f"{random.randint(1950, 2010)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                'nationality': nationality,
                'passport_number': f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))}{random.randint(1000000, 9999999)}",
                'passport_expiry': f"{random.randint(2027, 2035)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                'document_number': f"{random.randint(100, 999)}-{random.randint(1000000000, 9999999999)}",
                'email': f"{first.lower()}.{last.lower()}@email.com",
                'phone': f"971{random.randint(500000000, 999999999)}",
                'preferred_language': random.choice(LANGUAGES),
                'meal_preference': random.choice(MEAL_PREFS),
                'beverage_preference': random.choice(BEVERAGES),
                'original_cabin_class': cabin,
                'original_flight_number': flight['flight_number'],
                'original_flight_date': flight['scheduled_departure'][:10],
                'original_origin': flight['destination_code'],
                'original_destination': random.choice(list(AIRPORTS.keys())),
                'passenger_category': random.choice(PASSENGER_CATEGORIES),
                'frequent_flyer_number': f"EY{random.randint(10000000, 99999999)}" if random.random() < 0.4 else '',
                'frequent_flyer_tier_id': random.choice(FF_TIERS) if random.random() < 0.4 else '',
                'customer_value_score': round(random.uniform(1, 5), 1),
                'is_vip': 1 if is_vip else 0,
                'is_influencer': 'Y' if random.random() < 0.02 else 'N',
                'is_disrupted': 'Y' if is_disrupted else 'N',
                'disruption_reason': flight['disruption_reason'] if is_disrupted else '',
                'is_group_booking': 'Y' if random.random() < 0.1 else 'N',
                'is_agent_booking': 'Y' if random.random() < 0.2 else 'N',
                'corporate_booking': 'Y' if random.random() < 0.15 else 'N',
                'has_medical_condition': 1 if has_medical else 0,
                'medical_notes': 'Requires wheelchair assistance' if has_medical else '',
                'profession': random.choice(PROFESSIONS),
                'rebook_status': rebook_status,
                'rebook_flight_number': rebook_flight,
                'rebook_flight_date': rebook_date,
                'rebook_cabin_class': rebook_cabin,
                'rebook_origin': rebook_origin,
                'rebook_destination': rebook_dest,
                'rebook_departure_time': rebook_dep_time,
                'rebook_arrival_time': rebook_arr_time,
                'rebook_aircraft_type': rebook_ac_type,
                'compensation_offered': 'Y' if compensation > 0 else 'N',
                'compensation_amount_usd': compensation,
                'hotel_provided': 'Y' if is_disrupted and flight['delay_minutes'] > 360 else 'N',
                'meal_voucher_provided': 'Y' if is_disrupted and flight['delay_minutes'] > 120 else 'N',
            }
            passengers.append(passenger)
    
    return pd.DataFrame(passengers)

def generate_maintenance_workorders(flights_df):
    """Generate maintenance work orders with ALL 29 DynamoDB columns"""
    global workorder_counter
    workorders = []
    
    # Track scenarios covered to ensure all 11 have at least one work order
    scenarios_covered = set()
    
    # Create work orders for scenarios with technical issues
    tech_scenarios = [2, 3, 5, 6]  # Scenarios with AOG/MEL issues
    
    for _, flight in flights_df.iterrows():
        # Generate work orders for technical scenarios, MEL issues, OR if scenario not yet covered
        if flight['scenario_id'] in tech_scenarios or flight['mel_status'] == 'ACTIVE' or flight['scenario_id'] not in scenarios_covered:
            workorder_counter += 1
            scenarios_covered.add(flight['scenario_id'])
            base_date = datetime.strptime(flight['scheduled_departure'][:10], '%Y-%m-%d')
            
            priority = random.choice(['AOG', 'HIGH', 'MED', 'LOW'])
            wo_type = 'AOG' if priority == 'AOG' else random.choice(['BASE', 'LINE', 'HEAVY'])
            state = random.choice(['OPEN', 'IN_PROGRESS', 'CLOSED'])
            
            planned_start = base_date - timedelta(hours=random.randint(1, 24))
            planned_end = planned_start + timedelta(hours=random.randint(2, 12))
            actual_end = planned_end + timedelta(hours=random.randint(0, 4)) if state == 'CLOSED' else None
            
            work_steps = [
                {"step": "Inspection", "skill": "B1", "est_minutes": random.randint(30, 90)},
                {"step": "Rectification", "skill": "B1", "est_minutes": random.randint(45, 150)}
            ]
            
            workorder = {
                'workorder_id': f"WO-{workorder_counter}",
                'workorderNumber': f"AUH-{20000 + workorder_counter}",
                'flight_id': flight['flight_id'],
                'flight_number': flight['flight_number'],
                'scenario_id': flight['scenario_id'],
                'scenario_name': flight['scenario_name'],
                'aircraftRegistration': flight['aircraft_registration'],
                'aircraftType': AIRCRAFT.get(flight['aircraft_registration'], {}).get('type', 'A320'),
                'conversationID': f"CONV-{workorder_counter:04d}",
                'date_zulu': base_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'issueDate_zulu': (base_date - timedelta(hours=random.randint(1, 48))).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'issueStation': 'AUH',
                'issueFltTo': flight['destination_code'],
                'workorderType': wo_type,
                'workorderState': state,
                'workorderOriginType': random.choice(['PIREP', 'TECHLOG', 'SCHEDULED']),
                'priority_code': priority,
                'priority_description': 'Operational Impact',
                'priority_sortOrder': 1,
                'planned_start_zulu': planned_start.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'planned_end_zulu': planned_end.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'actual_end_zulu': actual_end.strftime('%Y-%m-%dT%H:%M:%SZ') if actual_end else '',
                'hangarCost': random.randint(1000, 20000),
                'towingCosts': random.randint(200, 5000),
                'engineChange': 1 if random.random() < 0.1 else 0,
                'accident': 0,
                'incident': 0,
                'rampActivity': 1 if random.random() < 0.3 else 0,
                'srmRepair': 1 if random.random() < 0.2 else 0,
                'taxiWeightAndBalance': 1 if random.random() < 0.2 else 0,
                'warranty': 1 if random.random() < 0.15 else 0,
                'notContracted': 1,
                'work_steps_json': json.dumps(work_steps),
            }
            workorders.append(workorder)
    
    return pd.DataFrame(workorders)

def generate_bookings(passengers_df):
    """Generate bookings linked to passengers"""
    bookings = []
    seen_bookings = set()
    
    for _, pax in passengers_df.iterrows():
        if pax['booking_id'] not in seen_bookings:
            seen_bookings.add(pax['booking_id'])
            
            booking = {
                'booking_id': pax['booking_id'],
                'pnr': pax['pnr'],
                'passenger_id': pax['passenger_id'],
                'flight_id': pax['flight_id'],
                'flight_number': pax['flight_number'],
                'scenario_id': pax['scenario_id'],
                'scenario_name': pax['scenario_name'],
                'aircraft_registration': pax['aircraft_registration'],
                'booking_date': (datetime.strptime(pax['departure_date'], '%Y-%m-%d') - timedelta(days=random.randint(7, 90))).strftime('%Y-%m-%d'),
                'booking_status': 'CONFIRMED' if pax['rebook_status'] != 'PENDING' else 'MODIFIED',
                'cabin_class': pax['original_cabin_class'],
                'fare_basis': random.choice(['YOWUS', 'BOWRT', 'JOWRT', 'FOWRT']),
                'total_fare_usd': random.randint(200, 8000),
                'payment_status': 'PAID',
                'is_disrupted': pax['is_disrupted'],
                'rebook_status': pax['rebook_status'],
            }
            bookings.append(booking)
    
    return pd.DataFrame(bookings)


def generate_crew_roster(flights_df):
    """Generate crew roster linked to flights"""
    global crew_counter
    crew = []
    
    CREW_ROLES = ['Captain', 'First Officer', 'Purser', 'Flight Attendant', 'Load Master']
    CREW_BASES = ['AUH', 'LHR', 'JFK', 'SYD', 'SIN']
    
    for _, flight in flights_df.iterrows():
        ac = AIRCRAFT.get(flight['aircraft_registration'], {'crew': 6})
        num_crew = ac['crew']
        
        for c in range(num_crew):
            crew_counter += 1
            role = 'Captain' if c == 0 else 'First Officer' if c == 1 else 'Purser' if c == 2 else 'Flight Attendant'
            crew_type = 'COCKPIT' if role in ['Captain', 'First Officer'] else 'CABIN'
            
            # FDP calculations
            fdp_start = datetime.strptime(flight['scheduled_departure'], '%Y-%m-%d %H:%M:%S') - timedelta(hours=2)
            fdp_end = datetime.strptime(flight['arrival_time'], '%Y-%m-%d %H:%M:%S') + timedelta(minutes=30)
            fdp_hours = (fdp_end - fdp_start).total_seconds() / 3600
            max_fdp = 14 if role in ['Captain', 'First Officer'] else 16
            fdp_exceeded = fdp_hours > max_fdp
            duty_hours = round(fdp_hours - 0.5, 1)
            flight_hours = round(fdp_hours - 2.5, 1)
            
            crew_member = {
                'roster_id': f"RST-{crew_counter}",
                'crew_id': f"CREW-{crew_counter}",
                'employee_id': f"EY{random.randint(10000, 99999)}",
                'position_id': f"POS-{c+1}",
                'flight_id': flight['flight_id'],
                'flight_number': flight['flight_number'],
                'scenario_id': flight['scenario_id'],
                'scenario_name': flight['scenario_name'],
                'aircraft_registration': flight['aircraft_registration'],
                'first_name': random.choice(FIRST_NAMES),
                'last_name': random.choice(LAST_NAMES),
                'role': role,
                'position': role,
                'crew_rank': 'Senior' if random.random() < 0.3 else 'Junior',
                'operation_rank': c + 1,
                'crew_type': crew_type,
                'base_location': random.choice(CREW_BASES),
                'license_type': 'ATPL' if role in ['Captain', 'First Officer'] else 'Cabin',
                'license_expiry': f"{random.randint(2026, 2028)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                'medical_expiry': f"{random.randint(2026, 2027)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                'qualification': AIRCRAFT.get(flight['aircraft_registration'], {}).get('type', 'A320'),
                'duty_type': 'FLIGHT',
                'duty_start': fdp_start.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'duty_end': fdp_end.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'duty_hours': duty_hours,
                'flight_hours': flight_hours,
                'fdp_remaining': round(max_fdp - fdp_hours, 1),
                'max_flight_duty_period': max_fdp,
                'flight_time_limitations': json.dumps({'max_daily': 10, 'max_weekly': 60, 'max_monthly': 100}),
                'fdp_exceeded': 'Y' if fdp_exceeded else 'N',
                'rest_required_hours': 12 if fdp_exceeded else 10,
                'roster_status': 'CONFIRMED',
                'compliance_status': 'COMPLIANT' if not fdp_exceeded else 'WARNING',
                'is_standby': 'N',
                'standby_start': '',
                'standby_end': '',
                'standby_hours': 0,
                'standby_reason': '',
                'is_deadhead': 'N',
                'is_augmented': 'Y' if flight_hours > 10 else 'N',
                'overtime_hours': max(0, round(duty_hours - 8, 1)),
                'max_overtime_hours': 4,
                'per_diem_amount': random.randint(50, 200),
                'scheduled_arrival_time': flight['arrival_time'],
                'activated_for_disruption': 'Y' if flight['delay_minutes'] > 120 else 'N',
            }
            crew.append(crew_member)
    
    return pd.DataFrame(crew)

def generate_weather(flights_df):
    """Generate weather data for all scenarios"""
    weather_data = []
    
    for scenario in SCENARIOS:
        base_date = datetime.strptime(scenario['date'], '%Y-%m-%d')
        w = scenario['weather']
        
        # Get unique airports from scenario flights
        airports_in_scenario = set()
        for flt in scenario['primary'] + scenario['secondary']:
            airports_in_scenario.add(flt['orig'])
            airports_in_scenario.add(flt['dest'])
        
        for airport in airports_in_scenario:
            weather = {
                'weather_id': f"WX-{scenario['id']}-{airport}",
                'scenario_id': scenario['id'],
                'scenario_name': scenario['name'],
                'airport_code': airport,
                'airport_name': AIRPORTS.get(airport, {}).get('name', airport),
                'observation_time': base_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'condition': w['condition'],
                'temperature_c': w['temp'],
                'wind_speed_kts': w['wind'],
                'wind_direction': random.randint(0, 360),
                'visibility_m': w['vis'],
                'ceiling_ft': random.randint(500, 5000) if w['vis'] < 5000 else 10000,
                'precipitation': 'HEAVY' if w['condition'] in ['TYPHOON', 'THUNDERSTORM', 'WINTER_STORM'] else 'NONE',
                'is_operational': 'N' if w['vis'] < 1000 or w['wind'] > 50 else 'Y',
                'metar': f"METAR {airport} {base_date.strftime('%d%H%MZ')} {w['wind']:03d}/{w['wind']:02d}KT {w['vis']}M {w['condition']}",
                'taf_valid_from': base_date.strftime('%Y-%m-%dT00:00:00Z'),
                'taf_valid_to': (base_date + timedelta(hours=24)).strftime('%Y-%m-%dT00:00:00Z'),
            }
            weather_data.append(weather)
    
    return pd.DataFrame(weather_data)


def generate_disruption_events(flights_df):
    """Generate disruption events for all scenarios"""
    events = []
    
    for scenario in SCENARIOS:
        base_date = datetime.strptime(scenario['date'], '%Y-%m-%d')
        
        event = {
            'event_id': f"EVT-{scenario['id']}",
            'scenario_id': scenario['id'],
            'scenario_name': scenario['name'],
            'event_type': scenario['event_type'],
            'event_description': scenario['name'],
            'start_time': base_date.strftime('%Y-%m-%dT06:00:00Z'),
            'end_time': (base_date + timedelta(hours=random.randint(6, 18))).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'severity': 'HIGH' if len(scenario['primary']) > 5 else 'MEDIUM' if len(scenario['primary']) > 2 else 'LOW',
            'affected_airports': ','.join(set([f['orig'] for f in scenario['primary']] + [f['dest'] for f in scenario['primary']])),
            'primary_flights_affected': len(scenario['primary']),
            'secondary_flights_affected': len(scenario['secondary']),
            'total_flights_affected': len(scenario['primary']) + len(scenario['secondary']),
            'estimated_pax_affected': sum([AIRCRAFT.get(f['ac'], {}).get('capacity', 200) for f in scenario['primary']]),
            'weather_condition': scenario['weather']['condition'],
            'wind_speed': scenario['weather']['wind'],
            'visibility': scenario['weather']['vis'],
            'resolution_status': 'RESOLVED',
            'resolution_time': (base_date + timedelta(hours=random.randint(12, 36))).strftime('%Y-%m-%dT%H:%M:%SZ'),
        }
        events.append(event)
    
    return pd.DataFrame(events)


def generate_cargo_shipments(flights_df):
    """Generate cargo shipments linked to flights"""
    global cargo_counter
    cargo = []
    
    CARGO_TYPES = ['General', 'Perishable', 'Dangerous Goods', 'Live Animals', 'Pharmaceuticals', 'Valuables']
    
    for _, flight in flights_df.iterrows():
        num_shipments = random.randint(5, 20)
        ac = AIRCRAFT.get(flight['aircraft_registration'], {'cargo': 5000})
        
        for s in range(num_shipments):
            cargo_counter += 1
            cargo_type = random.choice(CARGO_TYPES)
            is_temp_sensitive = cargo_type in ['Perishable', 'Pharmaceuticals']
            
            shipment = {
                'shipment_id': f"CGO-{cargo_counter}",
                'awb_number': f"{random.randint(100, 999)}-{random.randint(10000000, 99999999)}",
                'flight_id': flight['flight_id'],
                'flight_number': flight['flight_number'],
                'scenario_id': flight['scenario_id'],
                'scenario_name': flight['scenario_name'],
                'aircraft_registration': flight['aircraft_registration'],
                'origin': flight['origin_code'],
                'destination': flight['destination_code'],
                'cargo_type': cargo_type,
                'weight_kg': random.randint(50, 2000),
                'volume_cbm': round(random.uniform(0.5, 10), 2),
                'pieces': random.randint(1, 50),
                'is_temperature_sensitive': 'Y' if is_temp_sensitive else 'N',
                'required_temp_min': -20 if cargo_type == 'Pharmaceuticals' else 2 if cargo_type == 'Perishable' else None,
                'required_temp_max': 8 if cargo_type == 'Pharmaceuticals' else 8 if cargo_type == 'Perishable' else None,
                'is_dangerous_goods': 'Y' if cargo_type == 'Dangerous Goods' else 'N',
                'dg_class': random.choice(['3', '4.1', '8', '9']) if cargo_type == 'Dangerous Goods' else '',
                'priority': random.choice(['EXPRESS', 'STANDARD', 'ECONOMY']),
                'status': 'DELAYED' if flight['delay_minutes'] > 60 else 'ON_TIME',
                'shipper_name': f"Shipper {random.randint(1, 100)}",
                'consignee_name': f"Consignee {random.randint(1, 100)}",
            }
            cargo.append(shipment)
    
    return pd.DataFrame(cargo)

def generate_aircraft_availability(flights_df):
    """Generate aircraft availability data"""
    availability = []
    
    for ac_reg, ac_info in AIRCRAFT.items():
        # Find flights for this aircraft
        ac_flights = flights_df[flights_df['aircraft_registration'] == ac_reg]
        
        for scenario in SCENARIOS:
            base_date = datetime.strptime(scenario['date'], '%Y-%m-%d')
            scenario_flights = ac_flights[ac_flights['scenario_id'] == scenario['id']]
            
            is_aog = any(f['ac'] == ac_reg and 'AOG' in f.get('issue', '') for f in scenario.get('primary', []))
            has_mel = any(f['ac'] == ac_reg and 'MEL' in f.get('issue', '') for f in scenario.get('primary', []))
            
            avail = {
                'availability_id': f"AVL-{ac_reg}-{scenario['id']}",
                'aircraft_registration': ac_reg,
                'aircraft_type': ac_info['type'],
                'scenario_id': scenario['id'],
                'scenario_name': scenario['name'],
                'date': scenario['date'],
                'status': 'AOG' if is_aog else 'MEL' if has_mel else 'AVAILABLE',
                'location': 'AUH',
                'next_scheduled_flight': scenario_flights.iloc[0]['flight_number'] if len(scenario_flights) > 0 else '',
                'next_departure_time': scenario_flights.iloc[0]['scheduled_departure'] if len(scenario_flights) > 0 else '',
                'maintenance_due': (base_date + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
                'hours_until_maintenance': random.randint(10, 500),
                'cycles_until_maintenance': random.randint(5, 100),
                'etops_certified': 'Y' if ac_info['type'] in ['A380', 'B777X', 'B787-10', 'A350'] else 'N',
                'cargo_capacity_kg': ac_info['cargo'],
                'passenger_capacity': ac_info['capacity'],
            }
            availability.append(avail)
    
    return pd.DataFrame(availability)


def generate_reserve_crew_pool():
    """Generate reserve crew pool"""
    reserve_crew = []
    
    for scenario in SCENARIOS:
        base_date = datetime.strptime(scenario['date'], '%Y-%m-%d')
        
        # Generate 20 reserve crew per scenario
        for i in range(20):
            role = random.choice(['Captain', 'First Officer', 'Purser', 'Flight Attendant'])
            
            crew = {
                'reserve_id': f"RSV-{scenario['id']}-{i+1}",
                'employee_id': f"EY{random.randint(10000, 99999)}",
                'scenario_id': scenario['id'],
                'scenario_name': scenario['name'],
                'first_name': random.choice(FIRST_NAMES),
                'last_name': random.choice(LAST_NAMES),
                'role': role,
                'base': 'AUH',
                'status': random.choice(['AVAILABLE', 'ON_CALL', 'RESTING']),
                'available_from': base_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'available_until': (base_date + timedelta(hours=12)).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'qualifications': json.dumps(['A380', 'B777X', 'A350'] if role in ['Captain', 'First Officer'] else ['All']),
                'contact_phone': f"971{random.randint(500000000, 999999999)}",
                'last_duty_end': (base_date - timedelta(hours=random.randint(12, 48))).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'rest_complete': 'Y' if random.random() > 0.2 else 'N',
            }
            reserve_crew.append(crew)
    
    return pd.DataFrame(reserve_crew)


def generate_oal_rebooking_options(flights_df):
    """Generate OAL (Other Airline) rebooking options"""
    oal_options = []
    
    OAL_AIRLINES = ['QR', 'EK', 'SQ', 'BA', 'LH', 'AF', 'TK']
    
    # Ensure at least one OAL option per scenario
    scenarios_covered = set()
    
    for _, flight in flights_df.iterrows():
        # Generate for delayed flights OR if scenario not yet covered
        if flight['delay_minutes'] > 60 or flight['scenario_id'] not in scenarios_covered:
            num_options = random.randint(2, 5)
            scenarios_covered.add(flight['scenario_id'])
            
            for i in range(num_options):
                base_dep = datetime.strptime(flight['scheduled_departure'], '%Y-%m-%d %H:%M:%S')
                oal_dep = base_dep + timedelta(hours=random.randint(1, 12))
                
                option = {
                    'option_id': f"OAL-{flight['flight_id']}-{i+1}",
                    'original_flight_id': flight['flight_id'],
                    'original_flight_number': flight['flight_number'],
                    'scenario_id': flight['scenario_id'],
                    'scenario_name': flight['scenario_name'],
                    'oal_airline': random.choice(OAL_AIRLINES),
                    'oal_flight_number': f"{random.choice(OAL_AIRLINES)}{random.randint(100, 999)}",
                    'oal_departure': oal_dep.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'oal_arrival': (oal_dep + timedelta(hours=random.randint(3, 14))).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'origin': flight['destination_code'],
                    'destination': random.choice(list(AIRPORTS.keys())),
                    'available_seats_f': random.randint(0, 4),
                    'available_seats_j': random.randint(0, 12),
                    'available_seats_y': random.randint(10, 100),
                    'interline_cost_usd': random.randint(200, 2000),
                    'booking_class': random.choice(['Y', 'B', 'M', 'H', 'Q']),
                    'connection_time_min': random.randint(60, 240),
                    'is_recommended': 'Y' if i == 0 else 'N',
                }
                oal_options.append(option)
    
    return pd.DataFrame(oal_options)

def generate_aircraft_swap_options(flights_df):
    """Generate aircraft swap options for disrupted flights"""
    swap_options = []
    
    for _, flight in flights_df.iterrows():
        if flight['delay_minutes'] > 60 or flight['mel_status'] == 'ACTIVE':
            # Find compatible aircraft
            current_ac = AIRCRAFT.get(flight['aircraft_registration'], {})
            
            for ac_reg, ac_info in AIRCRAFT.items():
                if ac_reg != flight['aircraft_registration'] and ac_info['capacity'] >= current_ac.get('capacity', 0) * 0.8:
                    option = {
                        'swap_id': f"SWP-{flight['flight_id']}-{ac_reg}",
                        'flight_id': flight['flight_id'],
                        'flight_number': flight['flight_number'],
                        'scenario_id': flight['scenario_id'],
                        'scenario_name': flight['scenario_name'],
                        'original_aircraft': flight['aircraft_registration'],
                        'original_type': current_ac.get('type', 'Unknown'),
                        'swap_aircraft': ac_reg,
                        'swap_type': ac_info['type'],
                        'capacity_difference': ac_info['capacity'] - current_ac.get('capacity', 0),
                        'cargo_difference': ac_info['cargo'] - current_ac.get('cargo', 0),
                        'crew_change_required': 'Y' if ac_info['type'] != current_ac.get('type') else 'N',
                        'estimated_delay_min': random.randint(30, 120),
                        'cost_impact_usd': random.randint(5000, 50000),
                        'is_available': random.choice(['Y', 'Y', 'Y', 'N']),
                        'location': 'AUH',
                        'ready_time': (datetime.strptime(flight['scheduled_departure'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=random.randint(1, 4))).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    }
                    swap_options.append(option)
                    if len([s for s in swap_options if s['flight_id'] == flight['flight_id']]) >= 3:
                        break
    
    return pd.DataFrame(swap_options)


def generate_financial_impact(flights_df, passengers_df):
    """Generate financial impact data for scenarios"""
    impacts = []
    
    for scenario in SCENARIOS:
        scenario_flights = flights_df[flights_df['scenario_id'] == scenario['id']]
        scenario_pax = passengers_df[passengers_df['scenario_id'] == scenario['id']]
        
        total_delay_min = scenario_flights['delay_minutes'].sum()
        num_pax = len(scenario_pax)
        compensation_total = scenario_pax['compensation_amount_usd'].sum()
        
        impact = {
            'impact_id': f"FIN-{scenario['id']}",
            'scenario_id': scenario['id'],
            'scenario_name': scenario['name'],
            'total_flights_affected': len(scenario_flights),
            'total_passengers_affected': num_pax,
            'total_delay_minutes': total_delay_min,
            'average_delay_minutes': round(total_delay_min / max(len(scenario_flights), 1), 1),
            'compensation_cost_usd': compensation_total,
            'hotel_cost_usd': len(scenario_pax[scenario_pax['hotel_provided'] == 'Y']) * 150,
            'meal_voucher_cost_usd': len(scenario_pax[scenario_pax['meal_voucher_provided'] == 'Y']) * 25,
            'crew_overtime_cost_usd': random.randint(5000, 50000),
            'fuel_cost_impact_usd': random.randint(10000, 100000),
            'ground_handling_cost_usd': random.randint(5000, 30000),
            'oal_rebooking_cost_usd': random.randint(10000, 80000),
            'total_cost_usd': compensation_total + random.randint(50000, 300000),
            'revenue_loss_usd': random.randint(100000, 500000),
            'reputation_impact_score': round(random.uniform(1, 5), 1),
        }
        impacts.append(impact)
    
    return pd.DataFrame(impacts)


def generate_recovery_scenarios(flights_df):
    """Generate recovery scenario options with ALL DynamoDB columns"""
    recoveries = []
    
    for scenario in SCENARIOS:
        scenario_flights = flights_df[flights_df['scenario_id'] == scenario['id']]
        base_date = datetime.strptime(scenario['date'], '%Y-%m-%d')
        
        for i, strategy in enumerate(['DELAY_AND_WAIT', 'AIRCRAFT_SWAP', 'CANCEL_AND_REBOOK', 'OAL_TRANSFER']):
            estimated_delay = random.randint(30, 360)
            pax_score = round(random.uniform(2, 5), 1)
            cargo_score = round(random.uniform(2, 5), 1)
            network_score = round(random.uniform(2, 5), 1)
            
            recovery = {
                'recovery_id': f"RCV-{scenario['id']}-{i+1}",
                'disruption_id': f"DIS-{scenario['id']}",
                'scenario_id': scenario['id'],
                'scenario_name': scenario['name'],
                'scenario_type': scenario['event_type'],
                'scenario_rank': i + 1,
                'scenario_status': 'PROPOSED' if i > 0 else 'RECOMMENDED',
                'strategy_type': strategy,
                'strategy_description': f"Recovery strategy: {strategy.replace('_', ' ').title()}",
                'flights_affected': len(scenario_flights),
                'estimated_delay_minutes': estimated_delay,
                'estimated_recovery_time_hrs': random.randint(2, 24),
                'estimated_cost_usd': random.randint(10000, 200000),
                'passenger_impact_score': pax_score,
                'cargo_impact_score': cargo_score,
                'network_impact_score': network_score,
                'total_business_score': round((pax_score + cargo_score + network_score) / 3, 1),
                'passenger_satisfaction_score': round(random.uniform(2, 5), 1),
                'operational_complexity': random.choice(['LOW', 'MEDIUM', 'HIGH']),
                'resource_requirements': json.dumps({'crew': random.randint(5, 20), 'aircraft': random.randint(1, 5)}),
                'requires_aircraft_swap': 'Y' if strategy == 'AIRCRAFT_SWAP' else 'N',
                'requires_crew_change': 'Y' if random.random() < 0.3 else 'N',
                'requires_passenger_reaccommodation': 'Y' if strategy in ['CANCEL_AND_REBOOK', 'OAL_TRANSFER'] else 'N',
                'safety_compliant': 'Y',
                'is_recommended': 'Y' if i == 0 else 'N',
                'implementation_status': 'PROPOSED',
                'approved_by': f"MGR-{random.randint(100, 999)}" if i == 0 else '',
                'approved_at': base_date.strftime('%Y-%m-%dT%H:%M:%SZ') if i == 0 else '',
                'execution_started_at': (base_date + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ') if i == 0 else '',
                'execution_completed_at': (base_date + timedelta(hours=random.randint(4, 12))).strftime('%Y-%m-%dT%H:%M:%SZ') if i == 0 else '',
            }
            recoveries.append(recovery)
    
    return pd.DataFrame(recoveries)

def generate_airport_slots():
    """Generate airport slot data"""
    slots = []
    
    for scenario in SCENARIOS:
        base_date = datetime.strptime(scenario['date'], '%Y-%m-%d')
        
        for airport in AIRPORTS.keys():
            for hour in range(6, 24):
                slot = {
                    'slot_id': f"SLT-{scenario['id']}-{airport}-{hour:02d}",
                    'scenario_id': scenario['id'],
                    'scenario_name': scenario['name'],
                    'airport_code': airport,
                    'airport_name': AIRPORTS[airport]['name'],
                    'slot_time': base_date.replace(hour=hour).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'slot_type': random.choice(['ARRIVAL', 'DEPARTURE']),
                    'total_slots': random.randint(20, 50),
                    'used_slots': random.randint(15, 45),
                    'available_slots': random.randint(0, 10),
                    'is_congested': 'Y' if random.random() < 0.3 else 'N',
                    'slot_restriction': 'NONE' if random.random() > 0.2 else random.choice(['NOISE', 'CAPACITY', 'WEATHER']),
                }
                slots.append(slot)
    
    return pd.DataFrame(slots)


def generate_airport_curfews():
    """Generate airport curfew data"""
    curfews = []
    
    CURFEW_AIRPORTS = {'LHR': (23, 6), 'CDG': (0, 5), 'FRA': (23, 5), 'SYD': (23, 6)}
    
    for scenario in SCENARIOS:
        for airport, (start, end) in CURFEW_AIRPORTS.items():
            curfew = {
                'curfew_id': f"CRF-{scenario['id']}-{airport}",
                'scenario_id': scenario['id'],
                'scenario_name': scenario['name'],
                'airport_code': airport,
                'airport_name': AIRPORTS.get(airport, {}).get('name', airport),
                'curfew_start_local': f"{start:02d}:00",
                'curfew_end_local': f"{end:02d}:00",
                'curfew_type': 'NOISE',
                'exceptions_allowed': 'Y' if random.random() < 0.3 else 'N',
                'exception_fee_usd': random.randint(5000, 50000),
                'is_active': 'Y',
            }
            curfews.append(curfew)
    
    return pd.DataFrame(curfews)


def generate_mct():
    """Generate Minimum Connection Times"""
    mcts = []
    
    for scenario in SCENARIOS:
        for airport in AIRPORTS.keys():
            for conn_type in ['DOM-DOM', 'DOM-INT', 'INT-DOM', 'INT-INT']:
                mct = {
                    'mct_id': f"MCT-{scenario['id']}-{airport}-{conn_type}",
                    'scenario_id': scenario['id'],
                    'scenario_name': scenario['name'],
                    'airport_code': airport,
                    'airport_name': AIRPORTS[airport]['name'],
                    'connection_type': conn_type,
                    'standard_mct_min': random.randint(45, 120),
                    'premium_mct_min': random.randint(30, 90),
                    'wheelchair_mct_min': random.randint(60, 150),
                    'is_same_terminal': 'Y' if random.random() > 0.5 else 'N',
                }
                mcts.append(mct)
    
    return pd.DataFrame(mcts)


def generate_safety_constraints():
    """Generate safety constraints"""
    constraints = []
    
    CONSTRAINT_TYPES = ['CREW_REST', 'FDP_LIMIT', 'DUTY_LIMIT', 'ETOPS', 'MEL', 'WEIGHT_BALANCE']
    
    for scenario in SCENARIOS:
        for ctype in CONSTRAINT_TYPES:
            constraint = {
                'constraint_id': f"SAF-{scenario['id']}-{ctype}",
                'scenario_id': scenario['id'],
                'scenario_name': scenario['name'],
                'constraint_type': ctype,
                'description': f"{ctype.replace('_', ' ').title()} safety constraint",
                'min_value': random.randint(8, 12) if 'REST' in ctype or 'LIMIT' in ctype else None,
                'max_value': random.randint(12, 16) if 'REST' in ctype or 'LIMIT' in ctype else None,
                'unit': 'hours' if 'REST' in ctype or 'LIMIT' in ctype else 'N/A',
                'is_waivable': 'N' if ctype in ['CREW_REST', 'FDP_LIMIT'] else 'Y',
                'regulatory_reference': f"GCAA-{random.randint(100, 999)}",
                'penalty_for_violation': random.choice(['GROUNDING', 'FINE', 'WARNING']),
            }
            constraints.append(constraint)
    
    return pd.DataFrame(constraints)


def generate_maintenance_staff():
    """Generate maintenance staff data"""
    staff = []
    
    SKILLS = ['B1', 'B2', 'C', 'Avionics', 'Engine', 'Structures']
    
    for scenario in SCENARIOS:
        base_date = datetime.strptime(scenario['date'], '%Y-%m-%d')
        
        for i in range(30):
            skill = random.choice(SKILLS)
            shift_start = base_date.replace(hour=random.choice([6, 14, 22]))
            
            person = {
                'staff_id': f"MNT-{scenario['id']}-{i+1}",
                'employee_id': f"EY-M{random.randint(10000, 99999)}",
                'scenario_id': scenario['id'],
                'scenario_name': scenario['name'],
                'first_name': random.choice(FIRST_NAMES),
                'last_name': random.choice(LAST_NAMES),
                'skill_type': skill,
                'license_number': f"GCAA-{skill}-{random.randint(1000, 9999)}",
                'license_expiry': f"{random.randint(2026, 2028)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                'shift_start': shift_start.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'shift_end': (shift_start + timedelta(hours=8)).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'is_available': random.choice(['Y', 'Y', 'Y', 'N']),
                'current_assignment': f"WO-{random.randint(10000, 19999)}" if random.random() < 0.5 else '',
                'base_location': 'AUH',
                'hourly_rate_usd': random.randint(50, 150),
            }
            staff.append(person)
    
    return pd.DataFrame(staff)

def main():
    """Generate all data files"""
    print("=" * 60)
    print("GENERATING COMPLETE SCENARIO DATA - ALL 11 SCENARIOS")
    print("=" * 60)
    
    # Generate flights first (base table)
    print("\n1. Generating Flights (43 columns)...")
    flights_df = generate_flights()
    flights_df.to_csv(f"{OUTPUT_DIR}/flights_enriched_scenarios.csv", index=False)
    print(f"   Created: {len(flights_df)} flights, {len(flights_df.columns)} columns")
    
    # Generate passengers (54 columns from DynamoDB)
    print("\n2. Generating Passengers (54 columns)...")
    passengers_df = generate_passengers(flights_df)
    passengers_df.to_csv(f"{OUTPUT_DIR}/passengers_enriched_final.csv", index=False)
    print(f"   Created: {len(passengers_df)} passengers, {len(passengers_df.columns)} columns")
    
    # Generate maintenance work orders (29 columns from DynamoDB)
    print("\n3. Generating MaintenanceWorkOrders (29 columns)...")
    workorders_df = generate_maintenance_workorders(flights_df)
    workorders_df.to_csv(f"{OUTPUT_DIR}/aircraft_maintenance_workorders.csv", index=False)
    print(f"   Created: {len(workorders_df)} work orders, {len(workorders_df.columns)} columns")
    
    # Generate bookings
    print("\n4. Generating Bookings...")
    bookings_df = generate_bookings(passengers_df)
    bookings_df.to_csv(f"{OUTPUT_DIR}/bookings_enriched.csv", index=False)
    print(f"   Created: {len(bookings_df)} bookings, {len(bookings_df.columns)} columns")
    
    # Generate crew roster
    print("\n5. Generating CrewRoster...")
    crew_df = generate_crew_roster(flights_df)
    crew_df.to_csv(f"{OUTPUT_DIR}/crew_roster_enriched.csv", index=False)
    print(f"   Created: {len(crew_df)} crew assignments, {len(crew_df.columns)} columns")
    
    # Generate weather
    print("\n6. Generating Weather...")
    weather_df = generate_weather(flights_df)
    weather_df.to_csv(f"{OUTPUT_DIR}/weather.csv", index=False)
    print(f"   Created: {len(weather_df)} weather records, {len(weather_df.columns)} columns")
    
    # Generate disruption events
    print("\n7. Generating DisruptionEvents...")
    events_df = generate_disruption_events(flights_df)
    events_df.to_csv(f"{OUTPUT_DIR}/disruption_events.csv", index=False)
    print(f"   Created: {len(events_df)} events, {len(events_df.columns)} columns")
    
    # Generate cargo shipments
    print("\n8. Generating CargoShipments...")
    cargo_df = generate_cargo_shipments(flights_df)
    cargo_df.to_csv(f"{OUTPUT_DIR}/cargo_shipments.csv", index=False)
    print(f"   Created: {len(cargo_df)} shipments, {len(cargo_df.columns)} columns")
    
    # Generate aircraft availability
    print("\n9. Generating AircraftAvailability...")
    avail_df = generate_aircraft_availability(flights_df)
    avail_df.to_csv(f"{OUTPUT_DIR}/aircraft_availability_enriched_mel.csv", index=False)
    print(f"   Created: {len(avail_df)} records, {len(avail_df.columns)} columns")
    
    # Generate reserve crew pool
    print("\n10. Generating ReserveCrewPool...")
    reserve_df = generate_reserve_crew_pool()
    reserve_df.to_csv(f"{OUTPUT_DIR}/reserve_crew_pool.csv", index=False)
    print(f"   Created: {len(reserve_df)} reserve crew, {len(reserve_df.columns)} columns")
    
    # Generate OAL rebooking options
    print("\n11. Generating OALRebookingOptions...")
    oal_df = generate_oal_rebooking_options(flights_df)
    oal_df.to_csv(f"{OUTPUT_DIR}/oal_rebooking_options.csv", index=False)
    print(f"   Created: {len(oal_df)} options, {len(oal_df.columns)} columns")
    
    # Generate aircraft swap options
    print("\n12. Generating AircraftSwapOptions...")
    swap_df = generate_aircraft_swap_options(flights_df)
    swap_df.to_csv(f"{OUTPUT_DIR}/aircraft_swap_options.csv", index=False)
    print(f"   Created: {len(swap_df)} swap options, {len(swap_df.columns)} columns")
    
    # Generate financial impact
    print("\n13. Generating FinancialImpact...")
    fin_df = generate_financial_impact(flights_df, passengers_df)
    fin_df.to_csv(f"{OUTPUT_DIR}/financial_impact.csv", index=False)
    print(f"   Created: {len(fin_df)} impact records, {len(fin_df.columns)} columns")
    
    # Generate recovery scenarios
    print("\n14. Generating RecoveryScenarios...")
    recovery_df = generate_recovery_scenarios(flights_df)
    recovery_df.to_csv(f"{OUTPUT_DIR}/recovery_scenarios.csv", index=False)
    print(f"   Created: {len(recovery_df)} recovery options, {len(recovery_df.columns)} columns")
    
    # Generate airport slots
    print("\n15. Generating AirportSlots...")
    slots_df = generate_airport_slots()
    slots_df.to_csv(f"{OUTPUT_DIR}/airport_slots.csv", index=False)
    print(f"   Created: {len(slots_df)} slot records, {len(slots_df.columns)} columns")
    
    # Generate airport curfews
    print("\n16. Generating AirportCurfews...")
    curfews_df = generate_airport_curfews()
    curfews_df.to_csv(f"{OUTPUT_DIR}/airport_curfews.csv", index=False)
    print(f"   Created: {len(curfews_df)} curfew records, {len(curfews_df.columns)} columns")
    
    # Generate MCT
    print("\n17. Generating MinimumConnectionTimes...")
    mct_df = generate_mct()
    mct_df.to_csv(f"{OUTPUT_DIR}/minimum_connection_times.csv", index=False)
    print(f"   Created: {len(mct_df)} MCT records, {len(mct_df.columns)} columns")
    
    # Generate safety constraints
    print("\n18. Generating SafetyConstraints...")
    safety_df = generate_safety_constraints()
    safety_df.to_csv(f"{OUTPUT_DIR}/safety_constraints.csv", index=False)
    print(f"   Created: {len(safety_df)} constraints, {len(safety_df.columns)} columns")
    
    # Generate maintenance staff
    print("\n19. Generating MaintenanceStaff...")
    maint_staff_df = generate_maintenance_staff()
    maint_staff_df.to_csv(f"{OUTPUT_DIR}/maintenance_staff.csv", index=False)
    print(f"   Created: {len(maint_staff_df)} staff records, {len(maint_staff_df.columns)} columns")
    
    # Summary
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE!")
    print("=" * 60)
    
    # Verify scenario coverage
    print("\nScenario Coverage Verification:")
    for scenario in SCENARIOS:
        s_flights = len(flights_df[flights_df['scenario_id'] == scenario['id']])
        s_pax = len(passengers_df[passengers_df['scenario_id'] == scenario['id']])
        print(f"  Scenario {scenario['id']}: {scenario['name'][:40]}")
        print(f"    - Flights: {s_flights}, Passengers: {s_pax}")
    
    print(f"\nTotal Files Generated: 19")
    print(f"Output Directory: {OUTPUT_DIR}")
    
    return {
        'flights': flights_df,
        'passengers': passengers_df,
        'workorders': workorders_df,
        'bookings': bookings_df,
        'crew': crew_df,
    }


if __name__ == '__main__':
    main()
