# SkyMarshal Multi-Agent Dashboard Prompt & Requirements

## Purpose

Create a dynamic multi-agent dashboard for airline disruption recovery
using 7 specialized agents across 11 scenarios.

## Core Requirements

-   Scenario-driven (scenario_id 1--11)
-   Real-time KPI refresh
-   Cross-agent orchestration
-   Linked via scenario_id, flight_id, aircraft_registration, crew_id,
    passenger_id, booking_id
-   No missing data claims

## Agents

1.  Flight Operations
2.  Passenger Services
3.  Crew Management
4.  Maintenance
5.  Cargo
6.  Recovery Planning
7.  Safety & Compliance

## Dashboard Sections

-   Global Metrics
-   Agent Panels
-   Risk Alerts
-   Action Recommendations

## Master Prompt

You are an AI Orchestrator responsible for managing 7 agents. Load
datasets dynamically based on scenario_id. Each agent returns KPIs,
risks, actions, constraints. Chain agents when blockers appear. Output
JSON with global_metrics, agents, top_risks, recommended_actions,
blocked_constraints.
