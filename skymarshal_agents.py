"""
SkyMarshal Specialized Agents
7 agents for airline disruption recovery
"""

import pandas as pd
import asyncio
from typing import List, Optional
from datetime import datetime
from skymarshal_orchestrator import (
    Agent, AgentType, AgentOutput, KPI, Risk, Action, Constraint, SharedMemory
)


# ============================================================================
# 1. FLIGHT OPERATIONS AGENT
# ============================================================================

class FlightOperationsAgent(Agent):
    """Manages flight schedules, delays, cancellations, aircraft swaps"""
    
    def __init__(self, data_loader):
        super().__init__(AgentType.FLIGHT_OPERATIONS, data_loader)
    
    async def execute(self, scenario_id: int, shared_memory: SharedMemory) -> AgentOutput:
        """Assess flight operations impact"""
        start_time = datetime.now()
        
        kpis = []
        risks = []
        actions = []
        constraints = []
        
        try:
            scenario_data = self.data_loader.get_scenario_data(scenario_id)
            
            # Get flights data
            flights_df = scenario_data.get("flights_enriched_scenarios.csv", pd.DataFrame())
            weather_df = scenario_data.get("weather.csv", pd.DataFrame())
            aircraft_df = scenario_data.get("aircraft_availability_enriched_mel.csv", pd.DataFrame())
            swap_options_df = scenario_data.get("aircraft_swap_options.csv", pd.DataFrame())
            disruption_df = scenario_data.get("disruption_events.csv", pd.DataFrame())
            
            # Count flights and impacts
            total_flights = len(flights_df)
            delayed_flights = len(flights_df[flights_df['status'] == 'Delayed']) if 'status' in flights_df.columns else 0
            cancelled_flights = len(flights_df[flights_df['status'] == 'Cancelled']) if 'status' in flights_df.columns else 0
            
            # KPI: On-time performance
            on_time_rate = ((total_flights - delayed_flights) / total_flights * 100) if total_flights > 0 else 0
            kpis.append(self._create_kpi(
                "On-Time Performance",
                on_time_rate,
                95.0,
                "%"
            ))
            
            # KPI: Flight availability
            available_aircraft = len(aircraft_df[aircraft_df.get('is_available', False) == True]) if 'is_available' in aircraft_df.columns else 0
            kpis.append(self._create_kpi(
                "Aircraft Availability",
                available_aircraft,
                len(aircraft_df),
                "aircraft"
            ))
            
            # Risk: Delay cascade
            if delayed_flights > total_flights * 0.2:
                risks.append(self._create_risk(
                    "FOPS-001",
                    "Operational",
                    f"{delayed_flights} flights delayed - potential cascade effect",
                    "high" if delayed_flights > total_flights * 0.3 else "medium",
                    "flights"
                ))
            
            # Risk: Aircraft AOG (Aircraft on Ground)
            aog_aircraft = len(aircraft_df[aircraft_df.get('status') == 'AOG']) if 'status' in aircraft_df.columns else 0
            if aog_aircraft > 0:
                risks.append(self._create_risk(
                    "FOPS-002",
                    "Maintenance",
                    f"{aog_aircraft} aircraft grounded (AOG)",
                    "critical" if aog_aircraft > 2 else "high",
                    "aircraft"
                ))
            
            # Risk: Weather impact
            if not weather_df.empty:
                severe_weather = weather_df[weather_df.get('severity', '') == 'severe']
                if len(severe_weather) > 0:
                    risks.append(self._create_risk(
                        "FOPS-003",
                        "Weather",
                        f"Severe weather at {len(severe_weather)} airport(s)",
                        "high",
                        "airports"
                    ))
            
            # Actions: Aircraft swap
            available_swaps = len(swap_options_df) if not swap_options_df.empty else 0
            if available_swaps > 0:
                for idx, row in swap_options_df.head(3).iterrows():
                    flight_id = row.get('flight_id', f'FLT-{idx}')
                    actions.append(self._create_action(
                        f"FOPS-ACT-{idx}",
                        "aircraft_swap",
                        f"Swap aircraft for {flight_id}",
                        "high",
                        5000.0,
                        [flight_id]
                    ))
            
            # Actions: Flight delay mitigation
            if delayed_flights > 0:
                actions.append(self._create_action(
                    "FOPS-ACT-DELAY",
                    "mitigate_delay",
                    "Reschedule connecting flights to accommodate delays",
                    "high",
                    2000.0,
                    list(flights_df[flights_df.get('status') == 'Delayed']['flight_id'].head(5).unique())
                ))
            
            status = "completed"
        except Exception as e:
            status = "failed"
            constraints.append(self._create_constraint(
                "FOPS-ERR-001",
                "operational",
                f"Error processing flight data: {str(e)}",
                False
            ))
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return AgentOutput(
            agent_type=AgentType.FLIGHT_OPERATIONS,
            scenario_id=scenario_id,
            kpis=kpis,
            risks=risks,
            recommended_actions=actions,
            constraints=constraints,
            status=status,
            execution_time=execution_time,
            timestamp=datetime.now().isoformat()
        )


# ============================================================================
# 2. PASSENGER SERVICES AGENT
# ============================================================================

class PassengerServicesAgent(Agent):
    """Handles passenger rebooking, compensation, special needs"""
    
    def __init__(self, data_loader):
        super().__init__(AgentType.PASSENGER_SERVICES, data_loader)
    
    async def execute(self, scenario_id: int, shared_memory: SharedMemory) -> AgentOutput:
        """Assess passenger impact and recovery options"""
        start_time = datetime.now()
        
        kpis = []
        risks = []
        actions = []
        constraints = []
        
        try:
            scenario_data = self.data_loader.get_scenario_data(scenario_id)
            
            passengers_df = scenario_data.get("passengers_enriched_final.csv", pd.DataFrame())
            bookings_df = scenario_data.get("bookings.csv", pd.DataFrame())
            rebooking_df = scenario_data.get("oal_rebooking_options.csv", pd.DataFrame())
            flights_df = scenario_data.get("flights_enriched_scenarios.csv", pd.DataFrame())
            
            # Count passengers
            total_passengers = len(passengers_df)
            affected_passengers = len(passengers_df[passengers_df.get('affected', False) == True]) if 'affected' in passengers_df.columns else 0
            
            # Identify special passengers
            vip_passengers = len(passengers_df[passengers_df.get('frequent_flyer_tier', '') == 'Gold']) if 'frequent_flyer_tier' in passengers_df.columns else 0
            wheelchair_passengers = len(passengers_df[passengers_df.get('special_requirements', '') == 'Wheelchair']) if 'special_requirements' in passengers_df.columns else 0
            
            # KPI: Passenger satisfaction (inverse of affected)
            satisfaction_rate = ((total_passengers - affected_passengers) / total_passengers * 100) if total_passengers > 0 else 100
            kpis.append(self._create_kpi(
                "Passenger Satisfaction Impact",
                satisfaction_rate,
                95.0,
                "%"
            ))
            
            # KPI: Rebooking options available
            rebooking_options = len(rebooking_df) if not rebooking_df.empty else 0
            kpis.append(self._create_kpi(
                "Rebooking Options Available",
                rebooking_options,
                affected_passengers * 0.5,  # Target: 50% of affected have options
                "options"
            ))
            
            # Risk: High impact on VIP
            if vip_passengers > 0 and affected_passengers > 0:
                vip_affected_ratio = vip_passengers / affected_passengers
                if vip_affected_ratio > 0.1:  # More than 10% of affected are VIP
                    risks.append(self._create_risk(
                        "PASS-001",
                        "Reputation",
                        f"{vip_passengers} VIP passengers affected - high reputation risk",
                        "high",
                        "passengers"
                    ))
            
            # Risk: Special needs not accommodated
            if wheelchair_passengers > 0 and affected_passengers > 0:
                risks.append(self._create_risk(
                    "PASS-002",
                    "Compliance",
                    f"{wheelchair_passengers} passengers with special needs require assistance",
                    "high",
                    "passengers"
                ))
            
            # Risk: Rebooking capacity
            if rebooking_options < affected_passengers * 0.3:
                risks.append(self._create_risk(
                    "PASS-003",
                    "Capacity",
                    f"Limited rebooking options: {rebooking_options} options for {affected_passengers} affected passengers",
                    "critical",
                    "passengers"
                ))
            
            # Actions: Rebook passengers
            if not rebooking_df.empty:
                for idx, row in rebooking_df.head(5).iterrows():
                    actions.append(self._create_action(
                        f"PASS-ACT-REBOOK-{idx}",
                        "rebooking",
                        f"Rebook passengers from {row.get('original_flight', 'unknown')} to {row.get('new_flight', 'unknown')}",
                        "high",
                        0.0,  # Rebooking at no cost
                        [row.get('passenger_id', f'PAX-{idx}')]
                    ))
            
            # Actions: Compensation
            if affected_passengers > 0:
                compensation_amount = min(affected_passengers * 600, 500000)  # Max €600 per passenger
                actions.append(self._create_action(
                    "PASS-ACT-COMP",
                    "compensation",
                    f"Issue compensation to {affected_passengers} affected passengers",
                    "high",
                    compensation_amount,
                    list(passengers_df[passengers_df.get('affected', False) == True]['passenger_id'].head(100).unique())
                ))
            
            # Actions: Special assistance
            if wheelchair_passengers > 0:
                actions.append(self._create_action(
                    "PASS-ACT-ASSIST",
                    "special_assistance",
                    f"Arrange special assistance for {wheelchair_passengers} passengers",
                    "critical",
                    wheelchair_passengers * 200,
                    list(passengers_df[passengers_df.get('special_requirements', '') == 'Wheelchair']['passenger_id'].unique())
                ))
            
            status = "completed"
        except Exception as e:
            status = "failed"
            constraints.append(self._create_constraint(
                "PASS-ERR-001",
                "operational",
                f"Error processing passenger data: {str(e)}",
                False
            ))
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return AgentOutput(
            agent_type=AgentType.PASSENGER_SERVICES,
            scenario_id=scenario_id,
            kpis=kpis,
            risks=risks,
            recommended_actions=actions,
            constraints=constraints,
            status=status,
            execution_time=execution_time,
            timestamp=datetime.now().isoformat()
        )


# ============================================================================
# 3. CREW MANAGEMENT AGENT
# ============================================================================

class CrewManagementAgent(Agent):
    """Manages crew assignments, duty hours, qualifications"""
    
    def __init__(self, data_loader):
        super().__init__(AgentType.CREW_MANAGEMENT, data_loader)
    
    async def execute(self, scenario_id: int, shared_memory: SharedMemory) -> AgentOutput:
        """Assess crew availability and constraints"""
        start_time = datetime.now()
        
        kpis = []
        risks = []
        actions = []
        constraints = []
        
        try:
            scenario_data = self.data_loader.get_scenario_data(scenario_id)
            
            crew_df = scenario_data.get("crew_roster_enriched.csv", pd.DataFrame())
            reserve_df = scenario_data.get("reserve_crew_pool.csv", pd.DataFrame())
            flights_df = scenario_data.get("flights_enriched_scenarios.csv", pd.DataFrame())
            safety_df = scenario_data.get("safety_constraints.csv", pd.DataFrame())
            
            # Crew metrics
            total_crew = len(crew_df)
            available_crew = len(crew_df[crew_df.get('status', '') == 'Available']) if 'status' in crew_df.columns else 0
            duty_limited = len(crew_df[crew_df.get('duty_hours_remaining', 0) < 2]) if 'duty_hours_remaining' in crew_df.columns else 0
            reserve_available = len(reserve_df[reserve_df.get('status', '') == 'Available']) if 'status' in reserve_df.columns else 0
            
            # KPI: Crew availability
            crew_availability_pct = (available_crew / total_crew * 100) if total_crew > 0 else 0
            kpis.append(self._create_kpi(
                "Crew Availability",
                crew_availability_pct,
                85.0,
                "%"
            ))
            
            # KPI: Reserve pool
            kpis.append(self._create_kpi(
                "Reserve Crew Available",
                reserve_available,
                int(total_crew * 0.1),  # Target: 10% of crew
                "crew_members"
            ))
            
            # Risk: Duty hour violations
            if duty_limited > 0:
                risks.append(self._create_risk(
                    "CREW-001",
                    "Regulatory",
                    f"{duty_limited} crew members approaching duty hour limits",
                    "critical",
                    "crew"
                ))
                # Add as constraint
                constraints.append(self._create_constraint(
                    "CREW-CST-001",
                    "safety",
                    f"{duty_limited} crew members have < 2 hours duty remaining (CASS violation)",
                    is_binding=True
                ))
            
            # Risk: Insufficient reserve
            if reserve_available < 5:
                risks.append(self._create_risk(
                    "CREW-002",
                    "Operational",
                    f"Low reserve pool: only {reserve_available} crew available",
                    "high",
                    "crew"
                ))
            
            # Risk: Crew qualification mismatch
            if not flights_df.empty:
                aircraft_types = flights_df['aircraft_type'].unique()
                for aircraft_type in aircraft_types[:2]:  # Check first 2 aircraft types
                    qualified = len(crew_df[crew_df.get('qualified_aircraft_types', '').str.contains(aircraft_type, na=False)])
                    if qualified < 3:  # Minimum 3 qualified crew for type
                        risks.append(self._create_risk(
                            f"CREW-003-{aircraft_type}",
                            "Capability",
                            f"Only {qualified} crew qualified for {aircraft_type}",
                            "medium",
                            "crew"
                        ))
            
            # Actions: Recall reserve crew
            if reserve_available > 0:
                actions.append(self._create_action(
                    "CREW-ACT-RECALL",
                    "recall_reserve",
                    f"Recall {min(reserve_available, 10)} reserve crew members",
                    "high",
                    reserve_available * 500,  # Recall costs
                    list(reserve_df[reserve_df.get('status', '') == 'Available']['crew_id'].head(10).unique())
                ))
            
            # Actions: Overtime authorization
            if duty_limited > 0:
                actions.append(self._create_action(
                    "CREW-ACT-OVERTIME",
                    "authorize_overtime",
                    "Authorize overtime for critical flights",
                    "medium",
                    duty_limited * 300,
                    list(crew_df[crew_df.get('duty_hours_remaining', 0) < 2]['crew_id'].head(10).unique())
                ))
            
            status = "completed"
        except Exception as e:
            status = "failed"
            constraints.append(self._create_constraint(
                "CREW-ERR-001",
                "operational",
                f"Error processing crew data: {str(e)}",
                False
            ))
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return AgentOutput(
            agent_type=AgentType.CREW_MANAGEMENT,
            scenario_id=scenario_id,
            kpis=kpis,
            risks=risks,
            recommended_actions=actions,
            constraints=constraints,
            status=status,
            execution_time=execution_time,
            timestamp=datetime.now().isoformat()
        )


# ============================================================================
# 4. MAINTENANCE AGENT
# ============================================================================

class MaintenanceAgent(Agent):
    """Handles aircraft maintenance, MEL items, AOG situations"""
    
    def __init__(self, data_loader):
        super().__init__(AgentType.MAINTENANCE, data_loader)
    
    async def execute(self, scenario_id: int, shared_memory: SharedMemory) -> AgentOutput:
        """Assess maintenance status and impacts"""
        start_time = datetime.now()
        
        kpis = []
        risks = []
        actions = []
        constraints = []
        
        try:
            scenario_data = self.data_loader.get_scenario_data(scenario_id)
            
            maintenance_df = scenario_data.get("aircraft_maintenance_workorders.csv", pd.DataFrame())
            aircraft_df = scenario_data.get("aircraft_availability_enriched_mel.csv", pd.DataFrame())
            staff_df = scenario_data.get("maintenance_staff.csv", pd.DataFrame())
            flights_df = scenario_data.get("flights_enriched_scenarios.csv", pd.DataFrame())
            
            # Maintenance metrics
            total_workorders = len(maintenance_df)
            pending_workorders = len(maintenance_df[maintenance_df.get('status', '') == 'Pending']) if 'status' in maintenance_df.columns else 0
            critical_issues = len(maintenance_df[maintenance_df.get('severity', '') == 'Critical']) if 'severity' in maintenance_df.columns else 0
            
            aog_aircraft = len(aircraft_df[aircraft_df.get('status', '') == 'AOG']) if 'status' in aircraft_df.columns else 0
            mel_items = len(aircraft_df[aircraft_df.get('mel_count', 0) > 0]) if 'mel_count' in aircraft_df.columns else 0
            available_technicians = len(staff_df[staff_df.get('status', '') == 'Available']) if 'status' in staff_df.columns else 0
            
            # KPI: Aircraft availability
            available_aircraft = len(aircraft_df[aircraft_df.get('is_available', False) == True]) if 'is_available' in aircraft_df.columns else 0
            aircraft_availability = (available_aircraft / len(aircraft_df) * 100) if len(aircraft_df) > 0 else 0
            kpis.append(self._create_kpi(
                "Aircraft Availability",
                aircraft_availability,
                90.0,
                "%"
            ))
            
            # KPI: Maintenance workload
            completion_rate = ((total_workorders - pending_workorders) / total_workorders * 100) if total_workorders > 0 else 100
            kpis.append(self._create_kpi(
                "Maintenance Completion",
                completion_rate,
                80.0,
                "%"
            ))
            
            # Risk: AOG aircraft
            if aog_aircraft > 0:
                risks.append(self._create_risk(
                    "MAINT-001",
                    "Operational",
                    f"{aog_aircraft} aircraft are AOG (Aircraft on Ground)",
                    "critical" if aog_aircraft > 2 else "high",
                    "aircraft"
                ))
            
            # Risk: Critical maintenance issues
            if critical_issues > 0:
                risks.append(self._create_risk(
                    "MAINT-002",
                    "Safety",
                    f"{critical_issues} critical maintenance issues identified",
                    "critical",
                    "aircraft"
                ))
                constraints.append(self._create_constraint(
                    "MAINT-CST-001",
                    "safety",
                    f"Aircraft with critical issues are grounded until resolved",
                    is_binding=True
                ))
            
            # Risk: MEL expiry
            mel_expiring = len(aircraft_df[aircraft_df.get('mel_expiry_hours', float('inf')) < 10]) if 'mel_expiry_hours' in aircraft_df.columns else 0
            if mel_expiring > 0:
                risks.append(self._create_risk(
                    "MAINT-003",
                    "Regulatory",
                    f"{mel_expiring} aircraft with MEL items expiring within 10 hours",
                    "high",
                    "aircraft"
                ))
            
            # Actions: Maintenance priority
            if pending_workorders > 0:
                for idx, row in maintenance_df[maintenance_df.get('status', '') == 'Pending'].head(3).iterrows():
                    actions.append(self._create_action(
                        f"MAINT-ACT-{idx}",
                        "priority_maintenance",
                        f"Prioritize maintenance for {row.get('aircraft_registration', 'aircraft')}",
                        "high",
                        row.get('estimated_cost', 5000),
                        [row.get('aircraft_registration', f'AC-{idx}')]
                    ))
            
            # Actions: Technician callout
            if aog_aircraft > 0 and available_technicians > 0:
                actions.append(self._create_action(
                    "MAINT-ACT-CALLOUT",
                    "technician_callout",
                    f"Activate on-call technicians for AOG aircraft",
                    "critical",
                    available_technicians * 400,
                    []
                ))
            
            status = "completed"
        except Exception as e:
            status = "failed"
            constraints.append(self._create_constraint(
                "MAINT-ERR-001",
                "operational",
                f"Error processing maintenance data: {str(e)}",
                False
            ))
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return AgentOutput(
            agent_type=AgentType.MAINTENANCE,
            scenario_id=scenario_id,
            kpis=kpis,
            risks=risks,
            recommended_actions=actions,
            constraints=constraints,
            status=status,
            execution_time=execution_time,
            timestamp=datetime.now().isoformat()
        )


# ============================================================================
# 5. CARGO AGENT
# ============================================================================

class CargoAgent(Agent):
    """Manages cargo shipments, dangerous goods, temperature-sensitive items"""
    
    def __init__(self, data_loader):
        super().__init__(AgentType.CARGO, data_loader)
    
    async def execute(self, scenario_id: int, shared_memory: SharedMemory) -> AgentOutput:
        """Assess cargo impact and recovery options"""
        start_time = datetime.now()
        
        kpis = []
        risks = []
        actions = []
        constraints = []
        
        try:
            scenario_data = self.data_loader.get_scenario_data(scenario_id)
            
            cargo_df = scenario_data.get("cargo_shipments.csv", pd.DataFrame())
            flights_df = scenario_data.get("flights_enriched_scenarios.csv", pd.DataFrame())
            aircraft_df = scenario_data.get("aircraft_availability_enriched_mel.csv", pd.DataFrame())
            
            # Cargo metrics
            total_shipments = len(cargo_df)
            affected_shipments = len(cargo_df[cargo_df.get('affected', False) == True]) if 'affected' in cargo_df.columns else 0
            dangerous_goods = len(cargo_df[cargo_df.get('cargo_type', '') == 'Dangerous']) if 'cargo_type' in cargo_df.columns else 0
            temp_sensitive = len(cargo_df[cargo_df.get('temperature_controlled', False) == True]) if 'temperature_controlled' in cargo_df.columns else 0
            
            total_cargo_weight = cargo_df['weight_kg'].sum() if 'weight_kg' in cargo_df.columns else 0
            affected_cargo_weight = cargo_df[cargo_df.get('affected', False) == True]['weight_kg'].sum() if 'affected' in cargo_df.columns and 'weight_kg' in cargo_df.columns else 0
            
            # KPI: Cargo delivery rate
            delivery_rate = ((total_shipments - affected_shipments) / total_shipments * 100) if total_shipments > 0 else 100
            kpis.append(self._create_kpi(
                "Cargo Delivery Rate",
                delivery_rate,
                95.0,
                "%"
            ))
            
            # KPI: Dangerous goods status
            kpis.append(self._create_kpi(
                "Dangerous Goods Secure",
                total_shipments - dangerous_goods,
                total_shipments,
                "shipments"
            ))
            
            # Risk: Dangerous goods in transit
            if dangerous_goods > 0 and affected_shipments > 0:
                dangerous_affected = len(cargo_df[(cargo_df.get('cargo_type', '') == 'Dangerous') & (cargo_df.get('affected', False) == True)])
                if dangerous_affected > 0:
                    risks.append(self._create_risk(
                        "CARGO-001",
                        "Safety",
                        f"{dangerous_affected} dangerous goods shipments affected",
                        "critical",
                        "cargo"
                    ))
                    constraints.append(self._create_constraint(
                        "CARGO-CST-001",
                        "safety",
                        "Dangerous goods must be handled with HAZMAT protocols",
                        is_binding=True
                    ))
            
            # Risk: Temperature-sensitive cargo spoilage
            if temp_sensitive > 0:
                temp_affected = len(cargo_df[(cargo_df.get('temperature_controlled', False) == True) & (cargo_df.get('affected', False) == True)])
                if temp_affected > 0:
                    risks.append(self._create_risk(
                        "CARGO-002",
                        "Quality",
                        f"{temp_affected} temperature-sensitive shipments at risk of spoilage",
                        "high",
                        "cargo"
                    ))
            
            # Risk: Revenue impact
            if affected_cargo_weight > 0:
                risks.append(self._create_risk(
                    "CARGO-003",
                    "Financial",
                    f"{affected_cargo_weight:,.0f} kg of cargo affected (revenue impact)",
                    "high",
                    "cargo"
                ))
            
            # Actions: Cargo reroute
            if affected_shipments > 0:
                actions.append(self._create_action(
                    "CARGO-ACT-REROUTE",
                    "reroute_cargo",
                    f"Reroute {affected_shipments} affected shipments via alternative flights",
                    "high",
                    affected_shipments * 500,
                    list(cargo_df[cargo_df.get('affected', False) == True]['shipment_id'].head(50).unique())
                ))
            
            # Actions: Temperature maintenance
            if temp_sensitive > 0:
                actions.append(self._create_action(
                    "CARGO-ACT-TEMP",
                    "maintain_temperature",
                    "Activate temperature-controlled storage for sensitive shipments",
                    "high",
                    temp_sensitive * 200,
                    list(cargo_df[cargo_df.get('temperature_controlled', False) == True]['shipment_id'].head(50).unique())
                ))
            
            status = "completed"
        except Exception as e:
            status = "failed"
            constraints.append(self._create_constraint(
                "CARGO-ERR-001",
                "operational",
                f"Error processing cargo data: {str(e)}",
                False
            ))
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return AgentOutput(
            agent_type=AgentType.CARGO,
            scenario_id=scenario_id,
            kpis=kpis,
            risks=risks,
            recommended_actions=actions,
            constraints=constraints,
            status=status,
            execution_time=execution_time,
            timestamp=datetime.now().isoformat()
        )


# ============================================================================
# 6. RECOVERY PLANNING AGENT
# ============================================================================

class RecoveryPlanningAgent(Agent):
    """Coordinates overall recovery, prioritizes actions, tracks progress"""
    
    def __init__(self, data_loader):
        super().__init__(AgentType.RECOVERY_PLANNING, data_loader)
    
    async def execute(self, scenario_id: int, shared_memory: SharedMemory) -> AgentOutput:
        """Coordinate recovery and prioritize actions"""
        start_time = datetime.now()
        
        kpis = []
        risks = []
        actions = []
        constraints = []
        
        try:
            scenario_data = self.data_loader.get_scenario_data(scenario_id)
            
            recovery_df = scenario_data.get("recovery_scenarios.csv", pd.DataFrame())
            financial_df = scenario_data.get("financial_impact.csv", pd.DataFrame())
            disruption_df = scenario_data.get("disruption_events.csv", pd.DataFrame())
            cost_df = scenario_data.get("disruption_costs.csv", pd.DataFrame())
            
            # Recovery metrics
            total_recovery_options = len(recovery_df) if not recovery_df.empty else 0
            total_cost = financial_df['total_cost'].sum() if not financial_df.empty and 'total_cost' in financial_df.columns else 0
            recovery_time_hours = disruption_df['expected_recovery_time_hours'].iloc[0] if not disruption_df.empty and 'expected_recovery_time_hours' in disruption_df.columns else 0
            
            # Breakdown costs
            operational_cost = cost_df[cost_df.get('cost_category', '') == 'Operational']['cost_amount'].sum() if not cost_df.empty else 0
            compensation_cost = cost_df[cost_df.get('cost_category', '') == 'Compensation']['cost_amount'].sum() if not cost_df.empty else 0
            
            # KPI: Recovery time
            kpis.append(self._create_kpi(
                "Estimated Recovery Time",
                recovery_time_hours,
                24.0,  # Target: 24 hours
                "hours"
            ))
            
            # KPI: Total disruption cost
            kpis.append(self._create_kpi(
                "Total Disruption Cost",
                total_cost,
                200000.0,  # Target: under €200k
                "€"
            ))
            
            # KPI: Recovery options available
            kpis.append(self._create_kpi(
                "Recovery Scenarios Available",
                total_recovery_options,
                3.0,  # Target: at least 3 options
                "scenarios"
            ))
            
            # Risk: Long recovery time
            if recovery_time_hours > 12:
                risks.append(self._create_risk(
                    "RECOV-001",
                    "Operational",
                    f"Estimated recovery time: {recovery_time_hours} hours (target: 12h)",
                    "high" if recovery_time_hours > 24 else "medium",
                    "operations"
                ))
            
            # Risk: High cost impact
            if total_cost > 300000:
                risks.append(self._create_risk(
                    "RECOV-002",
                    "Financial",
                    f"High total disruption cost: €{total_cost:,.2f}",
                    "high",
                    "financial"
                ))
            
            # Risk: Limited recovery options
            if total_recovery_options < 2:
                risks.append(self._create_risk(
                    "RECOV-003",
                    "Operational",
                    "Limited recovery scenario options available",
                    "high",
                    "operations"
                ))
            
            # Actions: Implement recovery plan
            if total_recovery_options > 0:
                for idx, row in recovery_df.head(2).iterrows():
                    plan_name = row.get('recovery_plan_name', f'Plan-{idx}')
                    plan_cost = row.get('estimated_cost', 10000)
                    actions.append(self._create_action(
                        f"RECOV-ACT-{idx}",
                        "implement_recovery",
                        f"Implement recovery plan: {plan_name}",
                        "critical",
                        plan_cost,
                        []
                    ))
            
            # Actions: Cost mitigation
            if compensation_cost > 100000:
                actions.append(self._create_action(
                    "RECOV-ACT-COST",
                    "cost_mitigation",
                    "Activate revenue protection measures",
                    "high",
                    0.0,
                    []
                ))
            
            status = "completed"
        except Exception as e:
            status = "failed"
            constraints.append(self._create_constraint(
                "RECOV-ERR-001",
                "operational",
                f"Error processing recovery data: {str(e)}",
                False
            ))
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return AgentOutput(
            agent_type=AgentType.RECOVERY_PLANNING,
            scenario_id=scenario_id,
            kpis=kpis,
            risks=risks,
            recommended_actions=actions,
            constraints=constraints,
            status=status,
            execution_time=execution_time,
            timestamp=datetime.now().isoformat()
        )


# ============================================================================
# 7. SAFETY & COMPLIANCE AGENT
# ============================================================================

class SafetyComplianceAgent(Agent):
    """Ensures regulatory compliance, safety constraints, duty limits"""
    
    def __init__(self, data_loader):
        super().__init__(AgentType.SAFETY_COMPLIANCE, data_loader)
    
    async def execute(self, scenario_id: int, shared_memory: SharedMemory) -> AgentOutput:
        """Validate safety and compliance constraints"""
        start_time = datetime.now()
        
        kpis = []
        risks = []
        actions = []
        constraints = []
        
        try:
            scenario_data = self.data_loader.get_scenario_data(scenario_id)
            
            safety_df = scenario_data.get("safety_constraints.csv", pd.DataFrame())
            crew_df = scenario_data.get("crew_roster_enriched.csv", pd.DataFrame())
            flights_df = scenario_data.get("flights_enriched_scenarios.csv", pd.DataFrame())
            curfews_df = scenario_data.get("airport_curfews.csv", pd.DataFrame())
            min_connect_df = scenario_data.get("minimum_connection_times.csv", pd.DataFrame())
            
            # Safety metrics
            total_safety_constraints = len(safety_df)
            violated_constraints = len(safety_df[safety_df.get('violated', False) == True]) if 'violated' in safety_df.columns else 0
            
            # Crew duty violations
            crew_duty_violations = len(crew_df[crew_df.get('duty_violation', False) == True]) if 'duty_violation' in crew_df.columns else 0
            
            # Curfew violations
            curfew_violations = len(flights_df[flights_df.get('curfew_violation', False) == True]) if 'curfew_violation' in flights_df.columns else 0
            
            # KPI: Safety compliance
            compliance_rate = ((total_safety_constraints - violated_constraints) / total_safety_constraints * 100) if total_safety_constraints > 0 else 100
            kpis.append(self._create_kpi(
                "Safety Compliance",
                compliance_rate,
                100.0,  # Target: 100%
                "%"
            ))
            
            # KPI: Crew duty compliance
            crew_compliance_rate = ((len(crew_df) - crew_duty_violations) / len(crew_df) * 100) if len(crew_df) > 0 else 100
            kpis.append(self._create_kpi(
                "Crew Duty Compliance",
                crew_compliance_rate,
                100.0,
                "%"
            ))
            
            # Risk: Safety constraint violations
            if violated_constraints > 0:
                risks.append(self._create_risk(
                    "SAFE-001",
                    "Safety",
                    f"{violated_constraints} safety constraints violated",
                    "critical",
                    "safety"
                ))
            
            # Risk: Crew duty violations
            if crew_duty_violations > 0:
                risks.append(self._create_risk(
                    "SAFE-002",
                    "Regulatory",
                    f"{crew_duty_violations} crew members in duty violation (CASS/FTL)",
                    "critical",
                    "crew"
                ))
                constraints.append(self._create_constraint(
                    "SAFE-CST-001",
                    "regulatory",
                    f"Crew duty violations must be resolved before flight dispatch",
                    is_binding=True
                ))
            
            # Risk: Airport curfew violations
            if curfew_violations > 0:
                risks.append(self._create_risk(
                    "SAFE-003",
                    "Regulatory",
                    f"{curfew_violations} flights attempting to operate during curfew hours",
                    "critical",
                    "flights"
                ))
                constraints.append(self._create_constraint(
                    "SAFE-CST-002",
                    "regulatory",
                    "Flights cannot operate outside designated airport curfew windows",
                    is_binding=True
                ))
            
            # Risk: Minimum connection time violations
            if not min_connect_df.empty:
                mct_violations = len(min_connect_df[min_connect_df.get('mct_violation', False) == True]) if 'mct_violation' in min_connect_df.columns else 0
                if mct_violations > 0:
                    risks.append(self._create_risk(
                        "SAFE-004",
                        "Operational",
                        f"{mct_violations} connections violate minimum connection time",
                        "high",
                        "passengers"
                    ))
            
            # Actions: Resolve crew duty violations
            if crew_duty_violations > 0:
                actions.append(self._create_action(
                    "SAFE-ACT-CREW",
                    "resolve_duty_violation",
                    f"Assign {crew_duty_violations} crew members to rest before reassignment",
                    "critical",
                    crew_duty_violations * 100,
                    list(crew_df[crew_df.get('duty_violation', False) == True]['crew_id'].head(50).unique())
                ))
            
            # Actions: Implement safety review
            if violated_constraints > 0:
                actions.append(self._create_action(
                    "SAFE-ACT-REVIEW",
                    "safety_review",
                    "Conduct safety review of all affected flights",
                    "critical",
                    5000.0,
                    []
                ))
            
            status = "completed"
        except Exception as e:
            status = "failed"
            constraints.append(self._create_constraint(
                "SAFE-ERR-001",
                "operational",
                f"Error processing safety data: {str(e)}",
                False
            ))
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return AgentOutput(
            agent_type=AgentType.SAFETY_COMPLIANCE,
            scenario_id=scenario_id,
            kpis=kpis,
            risks=risks,
            recommended_actions=actions,
            constraints=constraints,
            status=status,
            execution_time=execution_time,
            timestamp=datetime.now().isoformat()
        )
