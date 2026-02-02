"""
SkyMarshal Dashboard API & Web Interface
Flask-based REST API for multi-agent orchestrator
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import asyncio
from datetime import datetime
from pathlib import Path
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Global orchestrator instance
orchestrator = None
cached_dashboards = {}
last_refresh_time = {}


def initialize_app():
    """Initialize Flask app with orchestrator"""
    global orchestrator
    from skymarshal_orchestrator import Orchestrator
    
    orchestrator = Orchestrator(".")
    orchestrator.initialize()
    print("✓ Dashboard API initialized")


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }), 200


@app.route('/api/scenarios', methods=['GET'])
def list_scenarios():
    """List all 11 disruption scenarios"""
    scenarios = [
        {"id": 1, "name": "Bangkok Typhoon + Critical MEL Aircraft", "date": "2026-01-19"},
        {"id": 2, "name": "London Fog + Multiple Aircraft AOG", "date": "2026-01-20"},
        {"id": 3, "name": "Singapore Thunderstorms + MEL Expiry", "date": "2026-01-21"},
        {"id": 4, "name": "Paris Winter Storm + Cargo Crisis", "date": "2026-01-22"},
        {"id": 5, "name": "Dubai Sandstorm + Hub Congestion", "date": "2026-01-23"},
        {"id": 6, "name": "Multiple Aircraft AOG + Engine Failure", "date": "2026-01-24"},
        {"id": 7, "name": "Crew Out of Hours + Cabin Crew Crisis", "date": "2026-01-25"},
        {"id": 8, "name": "Runway Closure + Airspace Restrictions", "date": "2026-01-27"},
        {"id": 9, "name": "Security Threat + Airspace Diversion", "date": "2026-01-28"},
        {"id": 10, "name": "Medical Emergency + Tarmac Delay", "date": "2026-01-29"},
        {"id": 11, "name": "EY401 Typhoon → EY406 LIAC", "date": "2026-01-31"}
    ]
    return jsonify(scenarios), 200


@app.route('/api/dashboard/<int:scenario_id>', methods=['GET'])
def get_dashboard(scenario_id):
    """Get dashboard data for a scenario"""
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    # Check if we have cached data and it's recent
    if not force_refresh and scenario_id in cached_dashboards:
        cached_time = last_refresh_time.get(scenario_id, 0)
        if (datetime.now().timestamp() - cached_time) < 300:  # 5 min cache
            return jsonify(cached_dashboards[scenario_id]), 200
    
    # Execute scenario
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        dashboard = loop.run_until_complete(orchestrator.execute_scenario(scenario_id))
        loop.close()
        
        # Convert to JSON-serializable format
        dashboard_data = {
            "global_metrics": {
                "scenario_id": dashboard.global_metrics.scenario_id,
                "total_affected_passengers": dashboard.global_metrics.total_affected_passengers,
                "total_affected_flights": dashboard.global_metrics.total_affected_flights,
                "total_disruption_cost": dashboard.global_metrics.total_disruption_cost,
                "recovery_status": dashboard.global_metrics.recovery_status,
                "critical_risks_count": dashboard.global_metrics.critical_risks_count,
                "blocked_actions_count": dashboard.global_metrics.blocked_actions_count,
                "completion_percentage": dashboard.global_metrics.completion_percentage,
                "timestamp": dashboard.global_metrics.timestamp
            },
            "agents": [],
            "top_risks": [],
            "recommended_actions": [],
            "blocked_constraints": [],
            "scenario_summary": dashboard.scenario_summary,
            "last_refresh": dashboard.last_refresh
        }
        
        # Add agents
        for agent in dashboard.agents:
            agent_data = {
                "agent_type": agent.agent_type.value,
                "scenario_id": agent.scenario_id,
                "kpis": [
                    {
                        "metric_name": kpi.metric_name,
                        "current_value": kpi.current_value,
                        "target_value": kpi.target_value,
                        "status": kpi.status,
                        "unit": kpi.unit,
                        "timestamp": kpi.timestamp
                    }
                    for kpi in agent.kpis
                ],
                "risks": [
                    {
                        "risk_id": r.risk_id,
                        "category": r.category,
                        "description": r.description,
                        "severity": r.severity,
                        "affected_entity": r.affected_entity,
                        "mitigation": r.mitigation,
                        "agent_id": r.agent_id
                    }
                    for r in agent.risks
                ],
                "recommended_actions": [
                    {
                        "action_id": a.action_id,
                        "agent_id": a.agent_id,
                        "action_type": a.action_type,
                        "description": a.description,
                        "priority": a.priority,
                        "estimated_cost": a.estimated_cost,
                        "affected_entity_ids": a.affected_entity_ids,
                        "execution_status": a.execution_status
                    }
                    for a in agent.recommended_actions
                ],
                "constraints": [
                    {
                        "constraint_id": c.constraint_id,
                        "agent_id": c.agent_id,
                        "constraint_type": c.constraint_type,
                        "description": c.description,
                        "is_binding": c.is_binding,
                        "affected_actions": c.affected_actions or []
                    }
                    for c in agent.constraints
                ],
                "status": agent.status,
                "error_message": agent.error_message,
                "execution_time": agent.execution_time,
                "timestamp": agent.timestamp
            }
            dashboard_data["agents"].append(agent_data)
        
        # Add top risks
        for risk in dashboard.top_risks:
            dashboard_data["top_risks"].append({
                "risk_id": risk.risk_id,
                "category": risk.category,
                "description": risk.description,
                "severity": risk.severity,
                "affected_entity": risk.affected_entity,
                "mitigation": risk.mitigation,
                "agent_id": risk.agent_id
            })
        
        # Add recommended actions
        for action in dashboard.recommended_actions:
            dashboard_data["recommended_actions"].append({
                "action_id": action.action_id,
                "agent_id": action.agent_id,
                "action_type": action.action_type,
                "description": action.description,
                "priority": action.priority,
                "estimated_cost": action.estimated_cost,
                "affected_entity_ids": action.affected_entity_ids,
                "execution_status": action.execution_status
            })
        
        # Add blocked constraints
        for constraint in dashboard.blocked_constraints:
            dashboard_data["blocked_constraints"].append({
                "constraint_id": constraint.constraint_id,
                "agent_id": constraint.agent_id,
                "constraint_type": constraint.constraint_type,
                "description": constraint.description,
                "is_binding": constraint.is_binding,
                "affected_actions": constraint.affected_actions or []
            })
        
        # Cache the result
        cached_dashboards[scenario_id] = dashboard_data
        last_refresh_time[scenario_id] = datetime.now().timestamp()
        
        return jsonify(dashboard_data), 200
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "scenario_id": scenario_id,
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/api/dashboard/<int:scenario_id>/kpis', methods=['GET'])
def get_kpis(scenario_id):
    """Get KPIs for a scenario"""
    if scenario_id not in cached_dashboards:
        return jsonify({"error": "Scenario not loaded"}), 404
    
    dashboard = cached_dashboards[scenario_id]
    all_kpis = []
    
    for agent in dashboard["agents"]:
        all_kpis.extend(agent["kpis"])
    
    return jsonify({
        "scenario_id": scenario_id,
        "kpi_count": len(all_kpis),
        "kpis": all_kpis,
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/dashboard/<int:scenario_id>/risks', methods=['GET'])
def get_risks(scenario_id):
    """Get risks for a scenario"""
    if scenario_id not in cached_dashboards:
        return jsonify({"error": "Scenario not loaded"}), 404
    
    dashboard = cached_dashboards[scenario_id]
    
    return jsonify({
        "scenario_id": scenario_id,
        "risk_count": len(dashboard["top_risks"]),
        "risks": dashboard["top_risks"],
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/dashboard/<int:scenario_id>/actions', methods=['GET'])
def get_actions(scenario_id):
    """Get recommended actions for a scenario"""
    if scenario_id not in cached_dashboards:
        return jsonify({"error": "Scenario not loaded"}), 404
    
    dashboard = cached_dashboards[scenario_id]
    
    return jsonify({
        "scenario_id": scenario_id,
        "action_count": len(dashboard["recommended_actions"]),
        "actions": dashboard["recommended_actions"],
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/dashboard/<int:scenario_id>/agents', methods=['GET'])
def get_agents(scenario_id):
    """Get agent execution results for a scenario"""
    if scenario_id not in cached_dashboards:
        return jsonify({"error": "Scenario not loaded"}), 404
    
    dashboard = cached_dashboards[scenario_id]
    agents_summary = []
    
    for agent in dashboard["agents"]:
        agents_summary.append({
            "agent_type": agent["agent_type"],
            "status": agent["status"],
            "execution_time": agent["execution_time"],
            "kpi_count": len(agent["kpis"]),
            "risk_count": len(agent["risks"]),
            "action_count": len(agent["recommended_actions"]),
            "constraint_count": len(agent["constraints"])
        })
    
    return jsonify({
        "scenario_id": scenario_id,
        "agent_count": len(agents_summary),
        "agents": agents_summary,
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/export/scenario/<int:scenario_id>', methods=['GET'])
def export_scenario(scenario_id):
    """Export scenario data as JSON"""
    format_type = request.args.get('format', 'json')
    
    if scenario_id not in cached_dashboards:
        return jsonify({"error": "Scenario not loaded"}), 404
    
    dashboard = cached_dashboards[scenario_id]
    
    if format_type == 'json':
        response = app.response_class(
            response=json.dumps(dashboard, indent=2, default=str),
            status=200,
            mimetype='application/json'
        )
        response.headers['Content-Disposition'] = f'attachment;filename=scenario_{scenario_id}.json'
        return response
    
    elif format_type == 'csv':
        # Export KPIs as CSV
        kpis_list = []
        for agent in dashboard["agents"]:
            for kpi in agent["kpis"]:
                kpis_list.append({
                    "agent": agent["agent_type"],
                    **kpi
                })
        
        if kpis_list:
            df = pd.DataFrame(kpis_list)
            csv_data = df.to_csv(index=False)
            response = app.response_class(
                response=csv_data,
                status=200,
                mimetype='text/csv'
            )
            response.headers['Content-Disposition'] = f'attachment;filename=scenario_{scenario_id}_kpis.csv'
            return response
        else:
            return jsonify({"error": "No KPI data to export"}), 404
    
    else:
        return jsonify({"error": "Unsupported format"}), 400


@app.route('/api/comparison', methods=['POST'])
def compare_scenarios():
    """Compare multiple scenarios"""
    data = request.get_json()
    scenario_ids = data.get('scenario_ids', [])
    
    comparison = {
        "scenarios": [],
        "timestamp": datetime.now().isoformat()
    }
    
    for scenario_id in scenario_ids:
        if scenario_id in cached_dashboards:
            metrics = cached_dashboards[scenario_id]["global_metrics"]
            comparison["scenarios"].append({
                "scenario_id": scenario_id,
                "name": cached_dashboards[scenario_id]["scenario_summary"]["scenario_name"],
                "total_affected_passengers": metrics["total_affected_passengers"],
                "total_affected_flights": metrics["total_affected_flights"],
                "total_disruption_cost": metrics["total_disruption_cost"],
                "recovery_status": metrics["recovery_status"],
                "critical_risks_count": metrics["critical_risks_count"],
                "completion_percentage": metrics["completion_percentage"]
            })
    
    return jsonify(comparison), 200


# ============================================================================
# WEB DASHBOARD VIEWS
# ============================================================================

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/scenario/<int:scenario_id>')
def scenario_view(scenario_id):
    """Scenario detail view"""
    return render_template('scenario.html', scenario_id=scenario_id)


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    initialize_app()
    
    # Create templates directory
    os.makedirs('templates', exist_ok=True)
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
