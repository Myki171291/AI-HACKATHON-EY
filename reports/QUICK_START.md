# SkyMarshal Quick Start Guide

## 🚀 Installation (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Verify Data
```bash
python validate_all_files_complete.py
```
Should show: ✓ All 21 files present for all 11 scenarios

### Step 3: Run System Test (Optional)
```bash
python test_system.py
```

## 📊 Option A: Web Dashboard (Recommended)

### Start Server
```bash
python skymarshal_dashboard_api.py
```

Expected output:
```
✓ Orchestrator initialized
 * Running on http://0.0.0.0:5000
```

### Open Dashboard
Open your browser to: **http://localhost:5000**

### Usage
1. Select a scenario from dropdown (1-11)
2. Click "Load" or refresh
3. View global metrics, risks, and actions
4. Export data as JSON or CSV

## 📝 Option B: Command Line

### Run Single Scenario
```bash
python skymarshal_orchestrator.py
```

Outputs: `dashboard_scenario_1.json`

### Run Custom Script
```python
import asyncio
from skymarshal_orchestrator import Orchestrator

async def main():
    orchestrator = Orchestrator(".")
    orchestrator.initialize()
    
    # Run scenario 5
    dashboard = await orchestrator.execute_scenario(5)
    
    # View results
    print(f"Affected: {dashboard.global_metrics.total_affected_passengers} passengers")
    print(f"Cost: €{dashboard.global_metrics.total_disruption_cost:,.0f}")
    print(f"Risks: {dashboard.global_metrics.critical_risks_count} critical")
    
    # Save results
    orchestrator.save_dashboard_data(dashboard, "scenario_5.json")

asyncio.run(main())
```

## 🔌 Option C: API Programmatic Access

### Health Check
```bash
curl http://localhost:5000/api/health
```

### List Scenarios
```bash
curl http://localhost:5000/api/scenarios | python -m json.tool
```

### Get Dashboard
```bash
curl http://localhost:5000/api/dashboard/1 | python -m json.tool
```

### Get KPIs Only
```bash
curl http://localhost:5000/api/dashboard/1/kpis | python -m json.tool
```

### Export as CSV
```bash
curl http://localhost:5000/api/export/scenario/1?format=csv > scenario_1.csv
```

## 📊 Understanding the Output

### Global Metrics
```json
{
  "total_affected_passengers": 1000,
  "total_affected_flights": 10,
  "total_disruption_cost": 500000.0,
  "recovery_status": "planning",
  "critical_risks_count": 5,
  "completion_percentage": 35.5
}
```

### Agent Output Example
```json
{
  "agent_type": "flight_operations",
  "status": "completed",
  "execution_time": 1.23,
  "kpis": [
    {
      "metric_name": "On-Time Performance",
      "current_value": 87.5,
      "target_value": 95.0,
      "status": "warning",
      "unit": "%"
    }
  ],
  "risks": [...],
  "recommended_actions": [...]
}
```

### Risk Severity Levels
- **CRITICAL** (🔴): Safety violation, cannot proceed
- **HIGH** (🟠): Major impact, requires immediate action
- **MEDIUM** (🟡): Moderate impact, should address
- **LOW** (🟢): Minor impact, informational

## 🎯 7 Agents Explained

1. **Flight Operations** 🛫
   - Manages flight schedules & aircraft availability
   - Identifies weather impacts & offers aircraft swaps

2. **Passenger Services** 👥
   - Tracks affected passengers
   - Recommends rebooking options
   - Calculates compensation

3. **Crew Management** 👨‍✈️
   - Monitors crew availability & duty hours
   - Checks qualifications & safety constraints
   - Manages reserve pool

4. **Maintenance** 🔧
   - Tracks aircraft AOG status
   - Monitors MEL (equipment list) expiry
   - Allocates technicians

5. **Cargo** 📦
   - Manages affected shipments
   - Checks dangerous goods compliance
   - Protects temp-sensitive cargo

6. **Recovery Planning** 📋
   - Coordinates overall recovery strategy
   - Prioritizes actions by cost/impact
   - Tracks financial impact

7. **Safety & Compliance** ✅
   - Validates regulatory constraints
   - Enforces crew duty limits
   - Checks curfew compliance

## 11 Scenarios at a Glance

| # | Scenario | Severity | Key Focus |
|---|----------|----------|-----------|
| 1 | Bangkok Typhoon | 🔴 CRITICAL | Weather + Equipment |
| 2 | London Fog | 🔴 CRITICAL | Visibility + AOG |
| 3 | Singapore Storms | 🟠 HIGH | Weather + Compliance |
| 4 | Paris Winter | 🟠 HIGH | Weather + Cargo |
| 5 | Dubai Sandstorm | 🟠 HIGH | Weather + Capacity |
| 6 | Multiple AOG | 🔴 CRITICAL | Equipment Failures |
| 7 | Crew Crisis | 🟠 HIGH | Staffing + Duty |
| 8 | Runway Closure | 🟠 HIGH | Infrastructure |
| 9 | Security Threat | 🔴 CRITICAL | Safety + Routing |
| 10 | Medical Emergency | 🟡 MEDIUM | Health + Delay |
| 11 | EY401 Typhoon | 🔴 CRITICAL | Complex Multi-leg |

## 💡 Tips & Tricks

### Refresh Data Faster
Use cached results for 5 minutes:
```
http://localhost:5000/api/dashboard/1
```

Force refresh:
```
http://localhost:5000/api/dashboard/1?refresh=true
```

### Compare Scenarios
```python
response = await client.post(
    "http://localhost:5000/api/comparison",
    json={"scenario_ids": [1, 2, 3]}
)
comparison = await response.json()
```

### Extract Top 5 Risks
```python
dashboard = await fetch("http://localhost:5000/api/dashboard/1")
top_risks = dashboard["top_risks"][:5]
```

### Get Cost Breakdown
```python
actions = dashboard["recommended_actions"]
by_priority = {}
for action in actions:
    priority = action["priority"]
    cost = action["estimated_cost"]
    by_priority[priority] = by_priority.get(priority, 0) + cost
```

## 🐛 Troubleshooting

### "Module not found" Error
```bash
pip install pandas flask flask-cors
```

### "CSV file not found" Error
Make sure you're running from the correct directory:
```bash
cd /path/to/AI-HACKATHON-EY-1
python skymarshal_dashboard_api.py
```

### Port 5000 Already in Use
Change the port in `skymarshal_dashboard_api.py`:
```python
app.run(port=5001)  # Use 5001 instead
```

### Slow Performance
- Clear browser cache
- Use `refresh=false` for API calls
- Reduce number of cached scenarios
- Use CSV export instead of JSON

## 📚 Documentation Files

- **README_SKYMARSHAL.md** - Complete documentation
- **AGENT_DATA_GUIDE.md** - Agent-dataset mapping
- **skymarshal_requirements.md** - Technical specs
- **skymarshal_architecture.md** - System architecture

## 📞 API Reference Summary

| Endpoint | Method | Returns |
|----------|--------|---------|
| `/api/health` | GET | System status |
| `/api/scenarios` | GET | All scenarios |
| `/api/dashboard/{id}` | GET | Full dashboard |
| `/api/dashboard/{id}/kpis` | GET | KPIs only |
| `/api/dashboard/{id}/risks` | GET | Risks only |
| `/api/dashboard/{id}/actions` | GET | Actions only |
| `/api/dashboard/{id}/agents` | GET | Agent status |
| `/api/export/scenario/{id}` | GET | JSON/CSV export |
| `/api/comparison` | POST | Scenario comparison |

## ✅ Next Steps

1. **Explore Dashboard**
   - Load different scenarios
   - Compare outputs
   - Review agent details

2. **Understand Constraints**
   - See which actions are blocked
   - Understand why constraints exist
   - Review safety rules

3. **Analyze Costs**
   - Track total disruption cost
   - See action cost breakdown
   - Compare scenarios

4. **Plan Recovery**
   - Review recommended actions
   - Prioritize by severity
   - Track completion

## 🎓 Learning Path

1. **Start with Scenario 10** (Medical Emergency) - smallest impact
2. **Try Scenario 1** (Bangkok Typhoon) - complex disruption
3. **Compare Scenarios 1, 5, 9** - different impact types
4. **Explore API** - programmatic access
5. **Extend System** - add custom agents or scenarios

---

**Enjoy exploring SkyMarshal! 🚀✈️**
