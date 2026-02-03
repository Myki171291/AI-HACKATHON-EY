#!/usr/bin/env python3
"""
SkyMarshal System Test & Quick Start
Validates the complete multi-agent orchestration system
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime
from skymarshal_orchestrator import Orchestrator, AgentType


def print_header(text):
    """Print section header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def print_success(text):
    """Print success message"""
    print(f"✓ {text}")


def print_error(text):
    """Print error message"""
    print(f"✗ {text}")


def print_warning(text):
    """Print warning message"""
    print(f"⚠ {text}")


def test_initialization():
    """Test orchestrator initialization"""
    print_header("TEST 1: Orchestrator Initialization")
    
    try:
        orchestrator = Orchestrator(".")
        orchestrator.initialize()
        print_success("Orchestrator initialized")
        
        # Check all agents created
        if len(orchestrator.agents) == 7:
            print_success(f"All 7 agents created: {', '.join([a.value for a in AgentType])}")
        else:
            print_error(f"Expected 7 agents, got {len(orchestrator.agents)}")
            return False
        
        # Check data loader
        if len(orchestrator.data_loader.data_cache) > 0:
            print_success(f"Loaded {len(orchestrator.data_loader.data_cache)} CSV files")
        else:
            print_error("No CSV files loaded")
            return False
        
        return True
    except Exception as e:
        print_error(f"Initialization failed: {str(e)}")
        return False


async def test_single_scenario():
    """Test execution of a single scenario"""
    print_header("TEST 2: Single Scenario Execution")
    
    try:
        orchestrator = Orchestrator(".")
        orchestrator.initialize()
        
        print("Executing Scenario 1 (Bangkok Typhoon)...")
        dashboard = await orchestrator.execute_scenario(1)
        
        # Validate output
        if not dashboard:
            print_error("Dashboard is None")
            return False
        
        print_success(f"Scenario executed in {(datetime.now()).isoformat()}")
        
        # Check global metrics
        metrics = dashboard.global_metrics
        print(f"\nGlobal Metrics:")
        print(f"  • Affected Passengers: {metrics.total_affected_passengers}")
        print(f"  • Affected Flights: {metrics.total_affected_flights}")
        print(f"  • Disruption Cost: €{metrics.total_disruption_cost:,.2f}")
        print(f"  • Recovery Status: {metrics.recovery_status}")
        print(f"  • Critical Risks: {metrics.critical_risks_count}")
        print(f"  • Blocked Actions: {metrics.blocked_actions_count}")
        print(f"  • Completion: {metrics.completion_percentage:.1f}%")
        
        if metrics.total_affected_passengers == 0:
            print_warning("No affected passengers detected")
        else:
            print_success(f"{metrics.total_affected_passengers} passengers impacted")
        
        # Check agents
        print(f"\nAgent Execution Summary:")
        for agent in dashboard.agents:
            status_emoji = "✓" if agent.status == "completed" else "⚠"
            print(f"  {status_emoji} {agent.agent_type.value}: {agent.status} ({agent.execution_time:.2f}s)")
            print(f"     • {len(agent.kpis)} KPIs, {len(agent.risks)} Risks, {len(agent.recommended_actions)} Actions")
        
        # Check results
        print(f"\nRisk & Action Summary:")
        print(f"  • Total Risks Identified: {len(dashboard.top_risks)}")
        if len(dashboard.top_risks) > 0:
            severities = {}
            for risk in dashboard.top_risks:
                severities[risk.severity] = severities.get(risk.severity, 0) + 1
            for severity, count in sorted(severities.items(), reverse=True):
                print(f"    - {severity.upper()}: {count}")
        
        print(f"  • Recommended Actions: {len(dashboard.recommended_actions)}")
        if len(dashboard.recommended_actions) > 0:
            total_cost = sum(a.estimated_cost for a in dashboard.recommended_actions)
            print(f"    - Total Action Cost: €{total_cost:,.2f}")
        
        print(f"  • Blocked Constraints: {len(dashboard.blocked_constraints)}")
        
        return True
    except Exception as e:
        print_error(f"Scenario execution failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_multiple_scenarios():
    """Test execution of multiple scenarios"""
    print_header("TEST 3: Multiple Scenarios Execution")
    
    try:
        orchestrator = Orchestrator(".")
        orchestrator.initialize()
        
        scenario_ids = [1, 2, 3]
        results = {}
        
        for scenario_id in scenario_ids:
            print(f"\nExecuting Scenario {scenario_id}...")
            dashboard = await orchestrator.execute_scenario(scenario_id)
            results[scenario_id] = {
                "passengers": dashboard.global_metrics.total_affected_passengers,
                "flights": dashboard.global_metrics.total_affected_flights,
                "cost": dashboard.global_metrics.total_disruption_cost,
                "risks": dashboard.global_metrics.critical_risks_count
            }
            print_success(f"Scenario {scenario_id} completed")
        
        # Summary
        print("\nScenario Comparison:")
        print(f"{'Scenario':<12} {'Passengers':<15} {'Flights':<12} {'Cost':<18} {'Risks':<10}")
        print("-" * 65)
        for scenario_id, data in results.items():
            print(f"{scenario_id:<12} {data['passengers']:<15} {data['flights']:<12} €{data['cost']:<17,.0f} {data['risks']:<10}")
        
        return True
    except Exception as e:
        print_error(f"Multiple scenarios test failed: {str(e)}")
        return False


async def test_data_consistency():
    """Test data consistency across scenarios"""
    print_header("TEST 4: Data Consistency Check")
    
    try:
        orchestrator = Orchestrator(".")
        orchestrator.initialize()
        
        # Check data loader coverage
        print("Checking data coverage for each scenario...")
        
        all_good = True
        for scenario_id in range(1, 12):
            scenario_data = orchestrator.data_loader.get_scenario_data(scenario_id)
            
            # Check key datasets
            required_datasets = [
                "flights_enriched_scenarios.csv",
                "passengers_enriched_final.csv",
                "disruption_events.csv"
            ]
            
            for dataset_name in required_datasets:
                if dataset_name in scenario_data:
                    df = scenario_data[dataset_name]
                    if len(df) == 0:
                        print_warning(f"Scenario {scenario_id}: {dataset_name} is empty")
                        all_good = False
                else:
                    print_error(f"Scenario {scenario_id}: {dataset_name} missing")
                    all_good = False
        
        if all_good:
            print_success("All scenarios have required data")
        
        return all_good
    except Exception as e:
        print_error(f"Data consistency test failed: {str(e)}")
        return False


async def test_api_output_format():
    """Test API output format consistency"""
    print_header("TEST 5: API Output Format Validation")
    
    try:
        orchestrator = Orchestrator(".")
        orchestrator.initialize()
        
        dashboard = await orchestrator.execute_scenario(1)
        
        # Validate structure
        required_fields = [
            ("global_metrics", dict),
            ("agents", list),
            ("top_risks", list),
            ("recommended_actions", list),
            ("blocked_constraints", list),
            ("scenario_summary", dict),
            ("last_refresh", str)
        ]
        
        all_valid = True
        for field_name, field_type in required_fields:
            if hasattr(dashboard, field_name):
                value = getattr(dashboard, field_name)
                if isinstance(value, field_type):
                    print_success(f"{field_name}: {field_type.__name__} ✓")
                else:
                    print_error(f"{field_name}: expected {field_type.__name__}, got {type(value).__name__}")
                    all_valid = False
            else:
                print_error(f"{field_name}: missing")
                all_valid = False
        
        # Validate agent outputs
        print(f"\nValidating {len(dashboard.agents)} agent outputs...")
        for agent in dashboard.agents:
            agent_type = agent.agent_type.value
            if len(agent.kpis) > 0 and len(agent.recommended_actions) > 0:
                print_success(f"{agent_type}: has KPIs and actions")
            else:
                print_warning(f"{agent_type}: limited output (KPIs: {len(agent.kpis)}, Actions: {len(agent.recommended_actions)})")
        
        return all_valid
    except Exception as e:
        print_error(f"API format validation failed: {str(e)}")
        return False


async def test_export_functionality():
    """Test export to JSON"""
    print_header("TEST 6: Export Functionality")
    
    try:
        orchestrator = Orchestrator(".")
        orchestrator.initialize()
        
        dashboard = await orchestrator.execute_scenario(1)
        
        # Save to JSON
        output_file = "test_export_scenario_1.json"
        orchestrator.save_dashboard_data(dashboard, output_file)
        
        # Verify file
        if Path(output_file).exists():
            file_size = Path(output_file).stat().st_size
            print_success(f"JSON export created: {output_file} ({file_size:,} bytes)")
            
            # Load and validate
            with open(output_file, 'r') as f:
                data = json.load(f)
            
            if "global_metrics" in data and "agents" in data:
                print_success("JSON structure is valid")
                return True
            else:
                print_error("JSON structure is invalid")
                return False
        else:
            print_error("Export file not created")
            return False
    except Exception as e:
        print_error(f"Export test failed: {str(e)}")
        return False


async def run_all_tests():
    """Run all system tests"""
    print_header("SkyMarshal Multi-Agent Orchestrator - System Test Suite")
    print(f"Started: {datetime.now().isoformat()}")
    
    tests = [
        ("Initialization", test_initialization()),
        ("Single Scenario", test_single_scenario()),
        ("Multiple Scenarios", test_multiple_scenarios()),
        ("Data Consistency", test_data_consistency()),
        ("API Output Format", test_api_output_format()),
        ("Export Functionality", test_export_functionality())
    ]
    
    results = {}
    for test_name, test_coroutine in tests:
        try:
            if asyncio.iscoroutine(test_coroutine):
                results[test_name] = await test_coroutine
            else:
                results[test_name] = test_coroutine
        except Exception as e:
            print_error(f"Test {test_name} crashed: {str(e)}")
            results[test_name] = False
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASSED ✓" if result else "FAILED ✗"
        print(f"{test_name:<30} {status}")
    
    print("-" * 50)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready for use.")
        print("\nNext steps:")
        print("  1. Run: python skymarshal_dashboard_api.py")
        print("  2. Open: http://localhost:5000")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Check output above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
