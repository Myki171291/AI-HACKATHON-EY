"""
Generate financial_transactions.csv and disruption_costs.csv for all 11 scenarios
"""
import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
random.seed(42)

# Output directory
OUTPUT_DIR = '../complete_output'

def generate_financial_transactions():
    """Generate financial transactions linked to bookings and flights"""
    print("Generating financial_transactions.csv...")
    
    # Load bookings and flights
    bookings = pd.read_csv(f'{OUTPUT_DIR}/bookings.csv')
    flights = pd.read_csv(f'{OUTPUT_DIR}/flights_enriched_scenarios.csv')
    passengers = pd.read_csv(f'{OUTPUT_DIR}/passengers_enriched_final.csv')
    
    transactions = []
    transaction_id = 1
    
    # Transaction types and payment methods
    transaction_types = ['TICKET_PURCHASE', 'SEAT_UPGRADE', 'BAGGAGE_FEE', 'MEAL_PURCHASE', 
                         'LOUNGE_ACCESS', 'REFUND', 'COMPENSATION', 'REBOOKING_FEE']
    payment_methods = ['CREDIT_CARD', 'DEBIT_CARD', 'BANK_TRANSFER', 'CASH', 'LOYALTY_POINTS', 'VOUCHER']
    payment_statuses = ['COMPLETED', 'PENDING', 'REFUNDED', 'FAILED']
    
    # Get unique scenarios
    scenarios = sorted(bookings['scenario_id'].unique())
    
    for scenario_id in scenarios:
        scenario_bookings = bookings[bookings['scenario_id'] == scenario_id]
        scenario_flights = flights[flights['scenario_id'] == scenario_id]
        scenario_passengers = passengers[passengers['scenario_id'] == scenario_id]
        
        # Generate transactions for each booking
        for _, booking in scenario_bookings.iterrows():
            # Main ticket purchase
            base_amount = random.uniform(200, 2500)
            tax = base_amount * 0.12
            surcharge = random.uniform(20, 100)
            discount = random.uniform(0, base_amount * 0.15) if random.random() < 0.3 else 0
            
            transactions.append({
                'transaction_id': f'TXN-{transaction_id:06d}',
                'booking_id': booking['booking_id'],
                'flight_id': booking['flight_id'],
                'passenger_id': booking['passenger_id'],
                'pnr': booking['pnr'],
                'scenario_id': scenario_id,
                'transaction_type': 'TICKET_PURCHASE',
                'transaction_date': booking['booking_date'],
                'amount_usd': round(base_amount, 2),
                'amount_aed': round(base_amount * 3.67, 2),
                'amount_inr': round(base_amount * 83.5, 2),
                'currency': random.choice(['USD', 'AED', 'INR', 'EUR', 'GBP']),
                'payment_method': random.choice(payment_methods),
                'payment_status': 'COMPLETED',
                'tax_amount_usd': round(tax, 2),
                'surcharge_usd': round(surcharge, 2),
                'discount_usd': round(discount, 2),
                'promo_code': f'PROMO{random.randint(100,999)}' if discount > 0 else ''
            })
            transaction_id += 1
            
            # Additional transactions (upgrades, baggage, etc.)
            if random.random() < 0.4:  # 40% chance of additional transaction
                add_type = random.choice(['SEAT_UPGRADE', 'BAGGAGE_FEE', 'MEAL_PURCHASE', 'LOUNGE_ACCESS'])
                add_amount = random.uniform(30, 300)
                transactions.append({
                    'transaction_id': f'TXN-{transaction_id:06d}',
                    'booking_id': booking['booking_id'],
                    'flight_id': booking['flight_id'],
                    'passenger_id': booking['passenger_id'],
                    'pnr': booking['pnr'],
                    'scenario_id': scenario_id,
                    'transaction_type': add_type,
                    'transaction_date': booking['booking_date'],
                    'amount_usd': round(add_amount, 2),
                    'amount_aed': round(add_amount * 3.67, 2),
                    'amount_inr': round(add_amount * 83.5, 2),
                    'currency': random.choice(['USD', 'AED', 'INR']),
                    'payment_method': random.choice(payment_methods),
                    'payment_status': 'COMPLETED',
                    'tax_amount_usd': round(add_amount * 0.05, 2),
                    'surcharge_usd': 0,
                    'discount_usd': 0,
                    'promo_code': ''
                })
                transaction_id += 1
        
        # Generate refund/compensation transactions for disrupted flights
        disrupted_flights = scenario_flights[scenario_flights['delay_minutes'] > 120]
        for _, flight in disrupted_flights.iterrows():
            affected_bookings = scenario_bookings[scenario_bookings['flight_id'] == flight['flight_id']]
            for _, booking in affected_bookings.sample(min(3, len(affected_bookings))).iterrows():
                comp_amount = random.uniform(100, 600)
                transactions.append({
                    'transaction_id': f'TXN-{transaction_id:06d}',
                    'booking_id': booking['booking_id'],
                    'flight_id': booking['flight_id'],
                    'passenger_id': booking['passenger_id'],
                    'pnr': booking['pnr'],
                    'scenario_id': scenario_id,
                    'transaction_type': random.choice(['REFUND', 'COMPENSATION']),
                    'transaction_date': flight['scheduled_departure'][:10],
                    'amount_usd': round(-comp_amount, 2),  # Negative for refunds
                    'amount_aed': round(-comp_amount * 3.67, 2),
                    'amount_inr': round(-comp_amount * 83.5, 2),
                    'currency': 'USD',
                    'payment_method': 'BANK_TRANSFER',
                    'payment_status': random.choice(['COMPLETED', 'PENDING']),
                    'tax_amount_usd': 0,
                    'surcharge_usd': 0,
                    'discount_usd': 0,
                    'promo_code': ''
                })
                transaction_id += 1
    
    df = pd.DataFrame(transactions)
    df.to_csv(f'{OUTPUT_DIR}/financial_transactions.csv', index=False)
    print(f"  Generated {len(df)} transactions across {len(scenarios)} scenarios")
    return df

def generate_disruption_costs():
    """Generate disruption costs linked to disruption events"""
    print("Generating disruption_costs.csv...")
    
    # Load disruption events and flights
    disruptions = pd.read_csv(f'{OUTPUT_DIR}/disruption_events.csv')
    flights = pd.read_csv(f'{OUTPUT_DIR}/flights_enriched_scenarios.csv')
    
    costs = []
    cost_id = 1
    
    # Cost categories and subcategories
    cost_categories = {
        'PASSENGER_CARE': ['HOTEL_ACCOMMODATION', 'MEAL_VOUCHERS', 'GROUND_TRANSPORT', 'COMMUNICATION'],
        'COMPENSATION': ['EU261_COMPENSATION', 'GOODWILL_VOUCHER', 'MILES_CREDIT', 'REFUND'],
        'OPERATIONAL': ['CREW_OVERTIME', 'AIRCRAFT_REPOSITIONING', 'FUEL_SURCHARGE', 'GROUND_HANDLING'],
        'REBOOKING': ['OAL_REBOOKING', 'HOTEL_REBOOKING', 'UPGRADE_COST'],
        'MAINTENANCE': ['AOG_REPAIR', 'PARTS_EXPEDITE', 'CONTRACTOR_FEE']
    }
    
    scenarios = sorted(disruptions['scenario_id'].unique())
    
    for scenario_id in scenarios:
        scenario_disruptions = disruptions[disruptions['scenario_id'] == scenario_id]
        scenario_flights = flights[flights['scenario_id'] == scenario_id]
        
        for _, disruption in scenario_disruptions.iterrows():
            # Generate multiple cost items per disruption
            num_costs = random.randint(5, 15)
            
            for _ in range(num_costs):
                category = random.choice(list(cost_categories.keys()))
                subcategory = random.choice(cost_categories[category])
                
                # Determine quantity and unit cost based on category
                if category == 'PASSENGER_CARE':
                    quantity = random.randint(10, 200)
                    unit_cost = random.uniform(50, 300)
                elif category == 'COMPENSATION':
                    quantity = random.randint(5, 100)
                    unit_cost = random.uniform(200, 600)
                elif category == 'OPERATIONAL':
                    quantity = random.randint(1, 20)
                    unit_cost = random.uniform(500, 5000)
                elif category == 'REBOOKING':
                    quantity = random.randint(5, 50)
                    unit_cost = random.uniform(300, 1500)
                else:  # MAINTENANCE
                    quantity = random.randint(1, 5)
                    unit_cost = random.uniform(2000, 50000)
                
                total_cost = quantity * unit_cost
                
                # Get a flight from this scenario for flight_number
                flight = scenario_flights.sample(1).iloc[0] if len(scenario_flights) > 0 else None
                flight_number = flight['flight_number'] if flight is not None else f'EY{random.randint(100,999)}'
                
                costs.append({
                    'cost_id': f'COST-{cost_id:06d}',
                    'disruption_id': disruption['event_id'],
                    'scenario_id': scenario_id,
                    'flight_number': flight_number,
                    'cost_category': category,
                    'cost_subcategory': subcategory,
                    'description': f'{subcategory.replace("_", " ").title()} for {flight_number}',
                    'quantity': quantity,
                    'unit_cost_usd': round(unit_cost, 2),
                    'total_cost_usd': round(total_cost, 2),
                    'total_cost_aed': round(total_cost * 3.67, 2),
                    'total_cost_inr': round(total_cost * 83.5, 2),
                    'cost_date': disruption['start_time'][:10] if pd.notna(disruption['start_time']) else '2026-01-25',
                    'status': random.choice(['APPROVED', 'PENDING', 'SUBMITTED', 'REJECTED']),
                    'approved_by': f'MGR-{random.randint(100,999)}' if random.random() < 0.7 else '',
                    'notes': f'Cost incurred due to {disruption["event_type"]}'
                })
                cost_id += 1
    
    df = pd.DataFrame(costs)
    df.to_csv(f'{OUTPUT_DIR}/disruption_costs.csv', index=False)
    print(f"  Generated {len(df)} cost items across {len(scenarios)} scenarios")
    return df

def validate_generated_data():
    """Validate the generated files"""
    print("\n=== Validation ===")
    
    for filename in ['financial_transactions.csv', 'disruption_costs.csv']:
        df = pd.read_csv(f'{OUTPUT_DIR}/{filename}')
        scenarios = sorted(df['scenario_id'].unique())
        print(f"\n{filename}:")
        print(f"  Total rows: {len(df)}")
        print(f"  Columns: {len(df.columns)}")
        print(f"  Scenarios covered: {scenarios}")
        print(f"  All 11 scenarios: {'✅ YES' if scenarios == list(range(1, 12)) else '❌ NO'}")
        
        # Check for nulls in key fields
        key_fields = ['scenario_id']
        if 'flight_id' in df.columns:
            key_fields.append('flight_id')
        if 'disruption_id' in df.columns:
            key_fields.append('disruption_id')
        
        null_counts = {col: df[col].isnull().sum() for col in key_fields}
        print(f"  Null counts in key fields: {null_counts}")

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("=" * 60)
    print("Generating Financial Data for All 11 Scenarios")
    print("=" * 60)
    
    generate_financial_transactions()
    generate_disruption_costs()
    validate_generated_data()
    
    print("\n✅ Done! Files saved to complete_output/")
