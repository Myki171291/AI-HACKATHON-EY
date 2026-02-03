"""
SkyMarshal Multi-Agent Orchestrator
Master orchestrator for airline disruption recovery with 7 specialized agents
Manages 11 disruption scenarios with real-time KPI refresh
"""

import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
from pathlib import Path

# ============================================================================
# DATA MODELS
# ============================================================================

class ScenarioID(Enum):
    """11 Disruption Scenarios"""
    BANGKOK_TYPHOON = 1
    LONDON_FOG = 2
    SINGAPORE_STORMS = 3
    PARIS_WINTER = 4
    DUBAI_SANDSTORM = 5
    MULTIPLE_AOG = 6
    CREW_CRISIS = 7
    RUNWAY_CLOSURE = 8
    SECURITY_THREAT = 9
    MEDICAL_EMERGENCY = 10
    EY401_TYPHOON = 11


class AgentType(Enum):
    """7 Specialized Agents"""
    FLIGHT_OPERATIONS = "flight_operations"
    PASSENGER_SERVICES = "passenger_services"
    CREW_MANAGEMENT = "crew_management"
    MAINTENANCE = "maintenance"
    CARGO = "cargo"
    RECOVERY_PLANNING = "recovery_planning"
    SAFETY_COMPLIANCE = "safety_compliance"


@dataclass
class KPI:
    """Key Performance Indicator for agents"""
    metric_name: str
    current_value: Any
    target_value: Any
    status: str  # "on_track", "warning", "critical"
    unit: str
    timestamp: str


@dataclass
class Risk:
    """Risk identification and severity"""
    risk_id: str
    category: str
    description: str
    severity: str  # "low", "medium", "high", "critical"
    affected_entity: str  # flight, passenger, crew, etc
    mitigation: Optional[str] = None
    agent_id: str = ""


@dataclass
class Action:
    """Recommended action from agents"""
    action_id: str
    agent_id: str
    action_type: str  # "rebooking", "swap", "delay", "cancel", etc
    description: str
    priority: str  # "low", "medium", "high", "critical"
    estimated_cost: float
    affected_entity_ids: List[str]
    execution_status: str = "pending"  # "pending", "in_progress", "completed", "rejected"


@dataclass
class Constraint:
    """Safety/regulatory constraints"""
    constraint_id: str
    agent_id: str
    constraint_type: str  # "safety", "regulatory", "operational"
    description: str
    is_binding: bool  # Cannot be overridden
    affected_actions: List[str] = None  # Action IDs this blocks


@dataclass
class AgentOutput:
    """Standard output from each agent"""
    agent_type: AgentType
    scenario_id: int
    kpis: List[KPI]
    risks: List[Risk]
    recommended_actions: List[Action]
    constraints: List[Constraint]
    status: str  # "completed", "partial", "failed"
    error_message: Optional[str] = None
    execution_time: float = 0.0
    timestamp: str = ""


@dataclass
class GlobalMetrics:
    """Aggregated metrics across all agents"""
    scenario_id: int
    total_affected_passengers: int
    total_affected_flights: int
    total_disruption_cost: float
    recovery_status: str  # "initial_assessment", "planning", "executing", "resolved"
    critical_risks_count: int
    blocked_actions_count: int
    completion_percentage: float
    timestamp: str


@dataclass
class DashboardData:
    """Complete dashboard state"""
    global_metrics: GlobalMetrics
    agents: List[AgentOutput]
    top_risks: List[Risk]
    recommended_actions: List[Action]
    blocked_constraints: List[Constraint]
    scenario_summary: Dict[str, Any]
    last_refresh: str


# ============================================================================
# SHARED MEMORY MANAGEMENT
# ============================================================================

class SharedMemory:
    """Centralized state management for all agents"""
    
    def __init__(self, scenario_id: int):
        self.scenario_id = scenario_id
        self.agent_outputs: Dict[AgentType, AgentOutput] = {}
        self.safety_constraints: List[Constraint] = []
        self.all_risks: List[Risk] = []
        self.all_actions: List[Action] = []
        self.execution_log: List[Dict[str, Any]] = []
        self.created_at = datetime.now().isoformat()
        
    def add_agent_output(self, output: AgentOutput):
        """Record agent execution result"""
        self.agent_outputs[output.agent_type] = output
        self.all_risks.extend(output.risks)
        self.all_actions.extend(output.recommended_actions)
        if output.constraints:
            self.safety_constraints.extend(output.constraints)
        self._log_event(f"Agent {output.agent_type.value} completed", output.status)
    
    def get_agent_output(self, agent_type: AgentType) -> Optional[AgentOutput]:
        """Retrieve agent output from memory"""
        return self.agent_outputs.get(agent_type)
    
    def get_all_kpis(self) -> List[KPI]:
        """Aggregate all KPIs from all agents"""
        kpis = []
        for output in self.agent_outputs.values():
            kpis.extend(output.kpis)
        return kpis
    
    def get_critical_risks(self) -> List[Risk]:
        """Get only critical and high-severity risks"""
        return [r for r in self.all_risks if r.severity in ["critical", "high"]]
    
    def get_blocked_actions(self) -> List[Action]:
        """Get actions blocked by constraints"""
        blocked = []
        blocked_action_ids = set()
        for constraint in self.safety_constraints:
            if constraint.affected_actions:
                blocked_action_ids.update(constraint.affected_actions)
        
        for action in self.all_actions:
            if action.action_id in blocked_action_ids:
                blocked.append(action)
        
        return blocked
    
    def _log_event(self, event: str, status: str):
        """Log execution events"""
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "status": status
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert memory to dictionary"""
        return {
            "scenario_id": self.scenario_id,
            "agent_outputs": {k.value: asdict(v) for k, v in self.agent_outputs.items()},
            "safety_constraints": [asdict(c) for c in self.safety_constraints],
            "all_risks": [asdict(r) for r in self.all_risks],
            "all_actions": [asdict(a) for a in self.all_actions],
            "execution_log": self.execution_log,
            "created_at": self.created_at
        }


# ============================================================================
# DATA LOADER
# ============================================================================

class DataLoader:
    """Load and manage CSV data files"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.data_cache: Dict[str, pd.DataFrame] = {}
    
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """Load all required CSV files"""
        files = [
            "flights_enriched_scenarios.csv",
            "passengers_enriched_final.csv",
            "bookings.csv",
            "crew_roster_enriched.csv",
            "cargo_shipments.csv",
            "aircraft_availability_enriched_mel.csv",
            "aircraft_maintenance_workorders.csv",
            "aircraft_swap_options.csv",
            "weather.csv",
            "disruption_events.csv",
            "recovery_scenarios.csv",
            "safety_constraints.csv",
            "maintenance_staff.csv",
            "reserve_crew_pool.csv",
            "oal_rebooking_options.csv",
            "airport_slots.csv",
            "airport_curfews.csv",
            "minimum_connection_times.csv",
            "financial_impact.csv",
            "financial_transactions.csv",
            "disruption_costs.csv"
        ]
        
        for filename in files:
            filepath = self.base_path / filename
            if filepath.exists():
                self.data_cache[filename] = pd.read_csv(filepath)
                print(f"✓ Loaded {filename}: {len(self.data_cache[filename])} rows")
            else:
                print(f"⚠ Missing {filename}")
        
        return self.data_cache
    
    def get_scenario_data(self, scenario_id: int) -> Dict[str, pd.DataFrame]:
        """Get all data filtered for specific scenario"""
        scenario_data = {}
        
        for name, df in self.data_cache.items():
            if 'scenario_id' in df.columns:
                scenario_data[name] = df[df['scenario_id'] == scenario_id]
            else:
                scenario_data[name] = df
        
        return scenario_data


# ============================================================================
# AGENT BASE CLASS
# ============================================================================

class Agent:
    """Base class for all specialized agents"""
    
    def __init__(self, agent_type: AgentType, data_loader: DataLoader):
        self.agent_type = agent_type
        self.data_loader = data_loader
        self.datasets_used = []
    
    async def execute(self, scenario_id: int, shared_memory: SharedMemory) -> AgentOutput:
        """Execute agent logic - to be overridden by subclasses"""
        raise NotImplementedError
    
    def _create_kpi(self, metric_name: str, current_value: Any, 
                   target_value: Any, unit: str = "") -> KPI:
        """Helper to create KPI"""
        # Determine status
        if isinstance(current_value, (int, float)):
            if current_value >= target_value * 0.9:
                status = "on_track"
            elif current_value >= target_value * 0.7:
                status = "warning"
            else:
                status = "critical"
        else:
            status = "on_track"
        
        return KPI(
            metric_name=metric_name,
            current_value=current_value,
            target_value=target_value,
            status=status,
            unit=unit,
            timestamp=datetime.now().isoformat()
        )
    
    def _create_risk(self, risk_id: str, category: str, description: str,
                    severity: str, affected_entity: str) -> Risk:
        """Helper to create risk"""
        return Risk(
            risk_id=risk_id,
            category=category,
            description=description,
            severity=severity,
            affected_entity=affected_entity,
            agent_id=self.agent_type.value
        )
    
    def _create_action(self, action_id: str, action_type: str, 
                      description: str, priority: str, cost: float,
                      affected_ids: List[str]) -> Action:
        """Helper to create action"""
        return Action(
            action_id=action_id,
            agent_id=self.agent_type.value,
            action_type=action_type,
            description=description,
            priority=priority,
            estimated_cost=cost,
            affected_entity_ids=affected_ids
        )
    
    def _create_constraint(self, constraint_id: str, constraint_type: str,
                          description: str, is_binding: bool = True) -> Constraint:
        """Helper to create constraint"""
        return Constraint(
            constraint_id=constraint_id,
            agent_id=self.agent_type.value,
            constraint_type=constraint_type,
            description=description,
            is_binding=is_binding
        )


# ============================================================================
# MASTER ORCHESTRATOR
# ============================================================================

class Orchestrator:
    """Master orchestrator managing 7 agents and 11 scenarios"""
    
    def __init__(self, base_path: str = "."):
        self.data_loader = DataLoader(base_path)
        self.shared_memory: Dict[int, SharedMemory] = {}
        self.agents: Dict[AgentType, Agent] = {}
        self.execution_history: List[Dict[str, Any]] = []
    
    def initialize(self):
        """Initialize orchestrator with data and agents"""
        print("🚀 Initializing SkyMarshal Orchestrator...")
        self.data_loader.load_all_data()
        self._initialize_agents()
        print("✓ Orchestrator initialized successfully")
    
    def _initialize_agents(self):
        """Initialize all 7 agents"""
        from skymarshal_agents import (
            FlightOperationsAgent,
            PassengerServicesAgent,
            CrewManagementAgent,
            MaintenanceAgent,
            CargoAgent,
            RecoveryPlanningAgent,
            SafetyComplianceAgent
        )
        
        self.agents = {
            AgentType.FLIGHT_OPERATIONS: FlightOperationsAgent(self.data_loader),
            AgentType.PASSENGER_SERVICES: PassengerServicesAgent(self.data_loader),
            AgentType.CREW_MANAGEMENT: CrewManagementAgent(self.data_loader),
            AgentType.MAINTENANCE: MaintenanceAgent(self.data_loader),
            AgentType.CARGO: CargoAgent(self.data_loader),
            AgentType.RECOVERY_PLANNING: RecoveryPlanningAgent(self.data_loader),
            AgentType.SAFETY_COMPLIANCE: SafetyComplianceAgent(self.data_loader),
        }
    
    async def execute_scenario(self, scenario_id: int) -> DashboardData:
        """Execute all agents for a scenario and return aggregated results"""
        print(f"\n📊 Executing scenario {scenario_id}...")
        
        # Create shared memory for this scenario
        shared_memory = SharedMemory(scenario_id)
        self.shared_memory[scenario_id] = shared_memory
        
        # Execute agents in orchestrated sequence
        agent_execution_order = [
            AgentType.FLIGHT_OPERATIONS,      # Phase 1: Identify disruption
            AgentType.PASSENGER_SERVICES,     # Phase 2: Assess passenger impact
            AgentType.CREW_MANAGEMENT,        # Phase 2: Assess crew impact
            AgentType.MAINTENANCE,            # Phase 2: Assess maintenance impact
            AgentType.CARGO,                  # Phase 3: Assess cargo impact
            AgentType.RECOVERY_PLANNING,      # Phase 4: Coordinate recovery
            AgentType.SAFETY_COMPLIANCE,      # Phase 5: Validate constraints
        ]
        
        for agent_type in agent_execution_order:
            agent = self.agents[agent_type]
            try:
                print(f"  ▶ Executing {agent_type.value}...", end=" ")
                output = await agent.execute(scenario_id, shared_memory)
                shared_memory.add_agent_output(output)
                print(f"✓ ({len(output.kpis)} KPIs, {len(output.risks)} risks)")
            except Exception as e:
                print(f"✗ Error: {str(e)}")
        
        # Generate dashboard data
        dashboard = self._generate_dashboard(scenario_id, shared_memory)
        self.execution_history.append({
            "scenario_id": scenario_id,
            "timestamp": datetime.now().isoformat(),
            "agents_executed": len(self.agents),
            "status": "completed"
        })
        
        return dashboard
    
    def _generate_dashboard(self, scenario_id: int, shared_memory: SharedMemory) -> DashboardData:
        """Generate dashboard data from shared memory"""
        
        # Get scenario summary
        scenario_data = self.data_loader.get_scenario_data(scenario_id)
        
        disruption_event = scenario_data.get("disruption_events.csv", pd.DataFrame())
        financial_impact = scenario_data.get("financial_impact.csv", pd.DataFrame())
        flights_data = scenario_data.get("flights_enriched_scenarios.csv", pd.DataFrame())
        passengers_data = scenario_data.get("passengers_enriched_final.csv", pd.DataFrame())
        
        # Calculate global metrics
        total_affected_passengers = len(passengers_data)
        total_affected_flights = len(flights_data)
        total_cost = financial_impact['total_cost'].sum() if not financial_impact.empty else 0.0
        
        critical_risks = shared_memory.get_critical_risks()
        blocked_actions = shared_memory.get_blocked_actions()
        
        # Determine recovery status
        if len(critical_risks) > 0:
            recovery_status = "initial_assessment"
        elif len(blocked_actions) > 0:
            recovery_status = "planning"
        else:
            recovery_status = "executing"
        
        # Calculate completion percentage
        total_actions = len(shared_memory.all_actions)
        completed_actions = sum(1 for a in shared_memory.all_actions if a.execution_status == "completed")
        completion_percentage = (completed_actions / total_actions * 100) if total_actions > 0 else 0
        
        global_metrics = GlobalMetrics(
            scenario_id=scenario_id,
            total_affected_passengers=total_affected_passengers,
            total_affected_flights=total_affected_flights,
            total_disruption_cost=total_cost,
            recovery_status=recovery_status,
            critical_risks_count=len(critical_risks),
            blocked_actions_count=len(blocked_actions),
            completion_percentage=completion_percentage,
            timestamp=datetime.now().isoformat()
        )
        
        # Get top risks (sorted by severity)
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        top_risks = sorted(shared_memory.all_risks, 
                          key=lambda r: severity_order.get(r.severity, 4))[:10]
        
        # Get recommended actions (sorted by priority)
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        recommended_actions = sorted(shared_memory.all_actions,
                                     key=lambda a: priority_order.get(a.priority, 4))[:15]
        
        return DashboardData(
            global_metrics=global_metrics,
            agents=list(shared_memory.agent_outputs.values()),
            top_risks=top_risks,
            recommended_actions=recommended_actions,
            blocked_constraints=shared_memory.safety_constraints,
            scenario_summary={
                "scenario_id": scenario_id,
                "scenario_name": self._get_scenario_name(scenario_id),
                "event_description": disruption_event['event_description'].iloc[0] if not disruption_event.empty else "",
                "disruption_cause": disruption_event['disruption_cause'].iloc[0] if not disruption_event.empty else "",
            },
            last_refresh=datetime.now().isoformat()
        )
    
    def get_dashboard_data(self, scenario_id: int) -> Optional[DashboardData]:
        """Retrieve cached dashboard data"""
        return getattr(self, f"_dashboard_{scenario_id}", None)
    
    def save_dashboard_data(self, dashboard: DashboardData, filepath: str):
        """Save dashboard data to JSON"""
        data = {
            "global_metrics": asdict(dashboard.global_metrics),
            "agents": [asdict(a) for a in dashboard.agents],
            "top_risks": [asdict(r) for r in dashboard.top_risks],
            "recommended_actions": [asdict(a) for a in dashboard.recommended_actions],
            "blocked_constraints": [asdict(c) for c in dashboard.blocked_constraints],
            "scenario_summary": dashboard.scenario_summary,
            "last_refresh": dashboard.last_refresh
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"✓ Dashboard saved to {filepath}")
    
    @staticmethod
    def _get_scenario_name(scenario_id: int) -> str:
        """Get human-readable scenario name"""
        names = {
            1: "Bangkok Typhoon + Critical MEL Aircraft",
            2: "London Fog + Multiple Aircraft AOG",
            3: "Singapore Thunderstorms + MEL Expiry",
            4: "Paris Winter Storm + Cargo Crisis",
            5: "Dubai Sandstorm + Hub Congestion",
            6: "Multiple Aircraft AOG + Engine Failure",
            7: "Crew Out of Hours + Cabin Crew Crisis",
            8: "Runway Closure + Airspace Restrictions",
            9: "Security Threat + Airspace Diversion",
            10: "Medical Emergency + Tarmac Delay",
            11: "EY401 Typhoon → EY406 LIAC"
        }
        return names.get(scenario_id, f"Scenario {scenario_id}")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

async def main():
    """Main execution"""
    orchestrator = Orchestrator(".")
    orchestrator.initialize()
    
    # Execute scenario 1 as example
    dashboard = await orchestrator.execute_scenario(1)
    
    # Save results
    orchestrator.save_dashboard_data(
        dashboard,
        "dashboard_scenario_1.json"
    )
    
    # Print summary
    print("\n" + "="*60)
    print("DASHBOARD SUMMARY")
    print("="*60)
    print(f"Scenario: {dashboard.scenario_summary['scenario_name']}")
    print(f"Status: {dashboard.global_metrics.recovery_status}")
    print(f"Affected Passengers: {dashboard.global_metrics.total_affected_passengers}")
    print(f"Affected Flights: {dashboard.global_metrics.total_affected_flights}")
    print(f"Disruption Cost: ${dashboard.global_metrics.total_disruption_cost:,.2f}")
    print(f"Critical Risks: {dashboard.global_metrics.critical_risks_count}")
    print(f"Blocked Actions: {dashboard.global_metrics.blocked_actions_count}")
    print(f"Recovery Progress: {dashboard.global_metrics.completion_percentage:.1f}%")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
