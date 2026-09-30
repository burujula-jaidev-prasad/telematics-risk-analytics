import os
import json
from generate_dataset import PROCESSED_DATA, DIR

json_data = json.dumps(PROCESSED_DATA)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telematics Risk & Dynamic Insurance Analytics Dashboard</title>
    <!-- Chart.js for interactive analytics charts -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: #1e293b;
            --bg-card-hover: #273549;
            --border-color: #334155;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-blue: #38bdf8;
            --accent-green: #22c55e;
            --accent-amber: #f59e0b;
            --accent-red: #ef4444;
            --accent-indigo: #6366f1;
            --accent-purple: #a855f7;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}

        body {{
            background-color: var(--bg-primary);
            color: var(--text-main);
            line-height: 1.5;
            padding: 24px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        /* Header */
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 24px;
            flex-wrap: wrap;
            gap: 16px;
        }}

        .header-title h1 {{
            font-size: 24px;
            font-weight: 700;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .header-title p {{
            color: var(--text-muted);
            font-size: 14px;
            margin-top: 4px;
        }}

        .team-badge {{
            display: inline-block;
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent-blue);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            border: 1px solid rgba(56, 189, 248, 0.3);
            margin-top: 6px;
        }}

        .header-actions {{
            display: flex;
            gap: 12px;
        }}

        .btn {{
            padding: 9px 16px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
            border: 1px solid transparent;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, #0284c7, #2563eb);
            color: white;
        }}

        .btn-primary:hover {{
            background: linear-gradient(135deg, #0369a1, #1d4ed8);
            transform: translateY(-1px);
        }}

        .btn-outline {{
            background: var(--bg-secondary);
            color: var(--text-main);
            border: 1px solid var(--border-color);
        }}

        .btn-outline:hover {{
            background: var(--bg-card-hover);
        }}

        /* KPI Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}

        .kpi-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s, border-color 0.2s;
        }}

        .kpi-card:hover {{
            transform: translateY(-2px);
            border-color: #475569;
        }}

        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
        }}

        .kpi-blue::before {{ background: var(--accent-blue); }}
        .kpi-green::before {{ background: var(--accent-green); }}
        .kpi-amber::before {{ background: var(--accent-amber); }}
        .kpi-red::before {{ background: var(--accent-red); }}
        .kpi-purple::before {{ background: var(--accent-purple); }}

        .kpi-label {{
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            margin-bottom: 8px;
        }}

        .kpi-value {{
            font-size: 26px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 4px;
        }}

        .kpi-subtext {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        /* Two column layout for Simulator and Charts */
        .analytics-section {{
            display: grid;
            grid-template-columns: 1.1fr 0.9fr;
            gap: 24px;
            margin-bottom: 28px;
        }}

        @media (max-width: 1024px) {{
            .analytics-section {{
                grid-template-columns: 1fr;
            }}
        }}

        .card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 22px;
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }}

        .card-title {{
            font-size: 16px;
            font-weight: 600;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .card-subtitle {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        /* Simulator Controls */
        .controls-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px 20px;
            margin-bottom: 20px;
        }}

        .control-group {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .control-label {{
            font-size: 13px;
            display: flex;
            justify-content: space-between;
            color: #cbd5e1;
        }}

        .control-value {{
            font-weight: 700;
            color: var(--accent-blue);
        }}

        input[type=range] {{
            width: 100%;
            height: 6px;
            background: #334155;
            border-radius: 4px;
            outline: none;
            -webkit-appearance: none;
            cursor: pointer;
        }}

        input[type=range]::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: var(--accent-blue);
            cursor: pointer;
            box-shadow: 0 0 6px rgba(56, 189, 248, 0.6);
        }}

        /* Simulator Results Box */
        .sim-results {{
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 16px;
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 20px;
            align-items: center;
        }}

        .score-circle {{
            width: 110px;
            height: 110px;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border: 6px solid var(--accent-green);
            background: rgba(34, 197, 94, 0.08);
            text-align: center;
            transition: all 0.3s;
        }}

        .score-num {{
            font-size: 32px;
            font-weight: 800;
            color: #fff;
            line-height: 1;
        }}

        .score-lbl {{
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            margin-top: 4px;
        }}

        .sim-metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 12px;
        }}

        .sim-metric-item {{
            background: rgba(255,255,255,0.03);
            padding: 10px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.05);
        }}

        .sim-metric-lbl {{
            font-size: 11px;
            color: var(--text-muted);
            margin-bottom: 2px;
        }}

        .sim-metric-val {{
            font-size: 16px;
            font-weight: 700;
            color: #fff;
        }}

        .tag {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
        }}

        .tag-low {{ background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.4); }}
        .tag-mod {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }}
        .tag-high {{ background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }}
        .tag-good {{ background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); }}
        .tag-warn {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }}
        .tag-crit {{ background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }}

        /* Charts Grid */
        .charts-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 28px;
        }}

        @media (max-width: 900px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .chart-box {{
            height: 250px;
            position: relative;
        }}

        /* Table Section */
        .table-section {{
            margin-bottom: 32px;
        }}

        .table-controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
            flex-wrap: wrap;
            gap: 12px;
        }}

        .search-box {{
            padding: 8px 14px;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: #fff;
            font-size: 13px;
            width: 260px;
            outline: none;
        }}

        .filter-buttons {{
            display: flex;
            gap: 8px;
        }}

        .filter-btn {{
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .filter-btn.active, .filter-btn:hover {{
            background: var(--accent-blue);
            color: #0f172a;
            border-color: var(--accent-blue);
            font-weight: 600;
        }}

        .table-responsive {{
            overflow-x: auto;
            border-radius: 10px;
            border: 1px solid var(--border-color);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
            background: var(--bg-card);
        }}

        th {{
            background: #172033;
            color: #cbd5e1;
            padding: 12px 14px;
            font-weight: 600;
            border-bottom: 1px solid var(--border-color);
            white-space: nowrap;
        }}

        td {{
            padding: 12px 14px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            white-space: nowrap;
        }}

        tr:hover td {{
            background: var(--bg-card-hover);
        }}

        .text-center {{ text-align: center; }}
        .text-right {{ text-align: right; }}

        .action-link {{
            color: var(--accent-blue);
            cursor: pointer;
            text-decoration: underline;
            font-weight: 500;
        }}

        /* Methodology & Context Section */
        .methodology-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 18px;
            margin-top: 14px;
        }}

        .method-card {{
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 8px;
            padding: 16px;
        }}

        .method-card h4 {{
            font-size: 14px;
            font-weight: 600;
            color: var(--accent-blue);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .method-card p {{
            font-size: 12px;
            color: #cbd5e1;
            line-height: 1.5;
        }}

        .formula-badge {{
            display: inline-block;
            background: #0f172a;
            padding: 4px 8px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 11px;
            color: #38bdf8;
            margin: 6px 0;
            border: 1px solid #334155;
        }}

        /* Footer */
        footer {{
            text-align: center;
            padding: 24px 0 12px;
            font-size: 12px;
            color: var(--text-muted);
            border-top: 1px solid var(--border-color);
            margin-top: 30px;
        }}
    </style>
</head>
<body>

<div class="container">
    <!-- Header -->
    <header>
        <div class="header-title">
            <h1>🚗 Telematics Risk & Dynamic Insurance Analytics</h1>
            <p>Predictive Driving Behavior Scoring, Sensor Quality Diagnostics & Pay-How-You-Drive Premium Modeling</p>
            <div class="team-badge">CIA 3 Automobile Industry Analytics · Jaidev Prasad (25121019) · Ruth Wilson (25121034) · Bala Kiran (25121012)</div>
        </div>
        <div class="header-actions">
            <a href="Telematics_Insurance_Maintenance_Analytics.xlsx" class="btn btn-primary" download>
                📥 Download Excel Workbook (.xlsx)
            </a>
            <a href="telematics_insurance_data.csv" class="btn btn-outline" download>
                📄 Export Raw CSV
            </a>
        </div>
    </header>

    <!-- KPI Summary Grid -->
    <div class="kpi-grid">
        <div class="kpi-card kpi-blue">
            <div class="kpi-label">Monitored Fleet Size</div>
            <div class="kpi-value">25 Vehicles</div>
            <div class="kpi-subtext">OBD-II & Sensor Telematics Feed</div>
        </div>
        <div class="kpi-card kpi-green">
            <div class="kpi-label">Avg Fleet Safety Score</div>
            <div class="kpi-value" id="kpiAvgScore">76.4 <span style="font-size: 16px; font-weight: normal;">/ 100</span></div>
            <div class="kpi-subtext">Based on braking, speed & night driving</div>
        </div>
        <div class="kpi-card kpi-amber">
            <div class="kpi-label">Low Risk (Discount Eligible)</div>
            <div class="kpi-value" id="kpiLowRisk">12 Drivers (48%)</div>
            <div class="kpi-subtext">Rewarded with -20% Base Premium discount</div>
        </div>
        <div class="kpi-card kpi-red">
            <div class="kpi-label">High Risk Flagged</div>
            <div class="kpi-value" id="kpiHighRisk">6 Drivers (24%)</div>
            <div class="kpi-subtext">+25% Risk Surcharge applied</div>
        </div>
        <div class="kpi-card kpi-purple">
            <div class="kpi-label">Critical Maintenance Alerts</div>
            <div class="kpi-value" id="kpiCritMaint">5 Vehicles</div>
            <div class="kpi-subtext">High temp / Low battery / Brake wear &gt;75%</div>
        </div>
        <div class="kpi-card kpi-green">
            <div class="kpi-label">Total Customer Savings</div>
            <div class="kpi-value" id="kpiSavings">₹1,14,450</div>
            <div class="kpi-subtext">Compared to flat ₹22,000 legacy premium</div>
        </div>
    </div>

    <!-- Simulator & Dynamic Engine Section -->
    <div class="analytics-section">
        <!-- Interactive Simulator Card -->
        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-title">🎛️ Live Driver Risk & Dynamic Premium Simulator</div>
                    <div class="card-subtitle">Adjust real-time sensor parameters to observe instant safety scoring & premium impact</div>
                </div>
                <button class="btn btn-outline" style="padding: 4px 10px; font-size: 11px;" onclick="resetSimulator()">Reset Defaults</button>
            </div>

            <div class="controls-grid">
                <div class="control-group">
                    <div class="control-label">
                        <span>Monthly Travel (PAYD)</span>
                        <span class="control-value" id="valKm">800 km</span>
                    </div>
                    <input type="range" id="inputKm" min="100" max="2500" step="50" value="800" oninput="updateSim()">
                </div>

                <div class="control-group">
                    <div class="control-label">
                        <span>Harsh Braking Events (/100km)</span>
                        <span class="control-value" id="valBrake">2</span>
                    </div>
                    <input type="range" id="inputBrake" min="0" max="15" step="1" value="2" oninput="updateSim()">
                </div>

                <div class="control-group">
                    <div class="control-label">
                        <span>Speeding Violations (/100km)</span>
                        <span class="control-value" id="valSpeed">1</span>
                    </div>
                    <input type="range" id="inputSpeed" min="0" max="12" step="1" value="1" oninput="updateSim()">
                </div>

                <div class="control-group">
                    <div class="control-label">
                        <span>Late-Night Travel % (11 PM - 4 AM)</span>
                        <span class="control-value" id="valNight">6%</span>
                    </div>
                    <input type="range" id="inputNight" min="0" max="50" step="1" value="6" oninput="updateSim()">
                </div>

                <div class="control-group">
                    <div class="control-label">
                        <span>Rapid Acceleration Events</span>
                        <span class="control-value" id="valAccel">1</span>
                    </div>
                    <input type="range" id="inputAccel" min="0" max="10" step="1" value="1" oninput="updateSim()">
                </div>

                <div class="control-group">
                    <div class="control-label">
                        <span>Battery Voltage (V)</span>
                        <span class="control-value" id="valBatt">12.6 V</span>
                    </div>
                    <input type="range" id="inputBatt" min="11.6" max="13.0" step="0.1" value="12.6" oninput="updateSim()">
                </div>

                <div class="control-group">
                    <div class="control-label">
                        <span>Engine Coolant Temp (°C)</span>
                        <span class="control-value" id="valTemp">88 °C</span>
                    </div>
                    <input type="range" id="inputTemp" min="80" max="115" step="1" value="88" oninput="updateSim()">
                </div>

                <div class="control-group">
                    <div class="control-label">
                        <span>Brake Pad Wear %</span>
                        <span class="control-value" id="valBrakeWear">25%</span>
                    </div>
                    <input type="range" id="inputBrakeWear" min="10" max="95" step="5" value="25" oninput="updateSim()">
                </div>
            </div>

            <!-- Live Simulator Output Box -->
            <div class="sim-results">
                <div class="score-circle" id="simScoreCircle">
                    <div class="score-num" id="simScoreNum">88.5</div>
                    <div class="score-lbl">Safety Score</div>
                </div>

                <div class="sim-metrics">
                    <div class="sim-metric-item">
                        <div class="sim-metric-lbl">Risk Tier</div>
                        <div class="sim-metric-val"><span class="tag tag-low" id="simRiskTag">Low Risk</span></div>
                    </div>
                    <div class="sim-metric-item">
                        <div class="sim-metric-lbl">Behavior Pricing</div>
                        <div class="sim-metric-val" id="simBehaviorAdj" style="color: #4ade80;">-20% (₹3,000 off)</div>
                    </div>
                    <div class="sim-metric-item">
                        <div class="sim-metric-lbl">Vehicle Health</div>
                        <div class="sim-metric-val"><span class="tag tag-good" id="simHealthTag">Good Condition (100)</span></div>
                    </div>
                    <div class="sim-metric-item">
                        <div class="sim-metric-lbl">PAYD Distance Surcharge</div>
                        <div class="sim-metric-val" id="simDistFee">+₹1,600</div>
                    </div>
                    <div class="sim-metric-item" style="grid-column: span 2; background: rgba(56, 189, 248, 0.08); border-color: rgba(56, 189, 248, 0.3);">
                        <div class="sim-metric-lbl">Dynamic Final Premium (vs ₹22,000 Flat)</div>
                        <div class="sim-metric-val" id="simFinalPrem" style="font-size: 20px; color: #38bdf8;">
                            ₹13,600 <span style="font-size: 13px; color: #4ade80; font-weight: normal;">(You Save ₹8,400 / yr)</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Real-Time Radar / Risk Breakdown Chart -->
        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-title">📊 Real-Time Driving Factor Analysis</div>
                    <div class="card-subtitle">Telemetry penalty distribution vs safe baseline benchmark</div>
                </div>
            </div>
            <div class="chart-box" style="height: 290px;">
                <canvas id="simRadarChart"></canvas>
            </div>
            <div style="font-size: 11px; color: var(--text-muted); margin-top: 10px; text-align: center;">
                💡 Low penalty areas indicate defensive driving; large spikes trigger insurance surcharges.
            </div>
        </div>
    </div>

    <!-- Analytics Charts Grid -->
    <div class="charts-grid">
        <div class="card">
            <div class="card-header">
                <div class="card-title">📈 Safety Score vs Dynamic Premium Trend (Pay-How-You-Drive)</div>
            </div>
            <div class="chart-box">
                <canvas id="chartScoreVsPrem"></canvas>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <div class="card-title">🛠️ Fleet Vehicle Health & Maintenance Diagnostic Distribution</div>
            </div>
            <div class="chart-box">
                <canvas id="chartHealthDonut"></canvas>
            </div>
        </div>
    </div>

    <!-- Interactive Data Table -->
    <div class="card table-section">
        <div class="card-header">
            <div>
                <div class="card-title">📋 Connected Fleet Telematics & Dynamic Pricing Ledger</div>
                <div class="card-subtitle">25 Telematics-Enabled Vehicles · Click "Inspect in Simulator" to load driver profile</div>
            </div>
        </div>

        <div class="table-controls">
            <input type="text" id="tableSearch" class="search-box" placeholder="🔍 Search driver, vehicle ID, or model..." oninput="filterTable()">
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="setTableFilter('all', this)">All (25)</button>
                <button class="filter-btn" onclick="setTableFilter('Low Risk', this)">Low Risk (12)</button>
                <button class="filter-btn" onclick="setTableFilter('Moderate Risk', this)">Moderate Risk (7)</button>
                <button class="filter-btn" onclick="setTableFilter('High Risk', this)">High Risk (6)</button>
                <button class="filter-btn" onclick="setTableFilter('Critical Maintenance', this)">Maintenance Due (5)</button>
            </div>
        </div>

        <div class="table-responsive">
            <table id="telematicsTable">
                <thead>
                    <tr>
                        <th>Vehicle ID</th>
                        <th>Driver</th>
                        <th>Model</th>
                        <th>Monthly KM</th>
                        <th>Harsh Brake</th>
                        <th>Speeding</th>
                        <th>Night %</th>
                        <th>Safety Score</th>
                        <th>Risk Tier</th>
                        <th>Health Score</th>
                        <th>Maintenance Status</th>
                        <th>Dynamic Premium</th>
                        <th>Driver Savings</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                    <!-- Populated by JS -->
                </tbody>
            </table>
        </div>
    </div>

    <!-- Analytical Methodology & Presentation Alignment -->
    <div class="card">
        <div class="card-header">
            <div class="card-title">🧠 Analytical Architecture & CIA-3 Automobile Industry Alignment</div>
        </div>
        <div class="methodology-grid">
            <div class="method-card">
                <h4>🎯 Pay-How-You-Drive (PHYD) Scoring</h4>
                <div class="formula-badge">Score = 100 - 2.5(Brake) - 3.0(Speed) - 0.5(Night%) - 1.5(Accel)</div>
                <p>Mirroring platforms like <strong>Zuno SmartDrive</strong> (Zuno Driving Quotient) and <strong>Tesla Safety Score</strong>, sensor telematics isolates individual driver behavior from static demographics, offering up to 20% renewal discounts.</p>
            </div>
            <div class="method-card">
                <h4>📏 Pay-As-You-Drive (PAYD) Distance Pricing</h4>
                <div class="formula-badge">Distance Surcharge = (Monthly KM / 1000) × ₹2,000</div>
                <p>Approved under IRDAI regulatory sandbox rules, distance-based pricing ensures fair premiums for low-mileage urban commuters, directly reducing claims exposure.</p>
            </div>
            <div class="method-card">
                <h4>🔧 Sensor-Based Predictive Maintenance</h4>
                <div class="formula-badge">Health = 100 - Battery_Deficit - Temp_Penalty - Wear_Penalty</div>
                <p>Tracking battery voltage, engine temperature, and brake wear enables early-warning interventions (aligned with <strong>Mahindra & Mahindra SAS Field Quality</strong> & Weibull reliability analytics), preventing costly warranty claims.</p>
            </div>
            <div class="method-card">
                <h4>🛡️ Dual Risk & Fraud Defense</h4>
                <div class="formula-badge">Expected Loss = PD × LGD × Exposure</div>
                <p>Telematics data preserves vehicle collateral value, lifting recovery from 60% to 70% (lowering Loss Given Default by 25%). Event telematics also eliminates staged crash claims (e.g. Insure The Box forensics).</p>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer>
        <p>Driving Risk Analytics & Connected Car Telematics Project · CIA 3 Automobile Industry Presentation</p>
        <p style="margin-top: 4px; color: #64748b;">Prepared by Jaidev Prasad (25121019) · Ruth Wilson (25121034) · Bala Kiran (25121012)</p>
    </footer>
</div>

<script>
    // Embedded Telematics Dataset
    const fleetData = {json_data};

    let currentFilter = 'all';

    // Populate Table
    function renderTable() {{{{
        const tbody = document.getElementById('tableBody');
        const searchTerm = document.getElementById('tableSearch').value.toLowerCase();
        tbody.innerHTML = '';

        const filtered = fleetData.filter(row => {{{{
            const matchesSearch = row.id.toLowerCase().includes(searchTerm) ||
                                  row.driver.toLowerCase().includes(searchTerm) ||
                                  row.model.toLowerCase().includes(searchTerm);
            if (!matchesSearch) return false;

            if (currentFilter === 'all') return true;
            if (currentFilter === 'Low Risk') return row.risk_cat === 'Low Risk';
            if (currentFilter === 'Moderate Risk') return row.risk_cat === 'Moderate Risk';
            if (currentFilter === 'High Risk') return row.risk_cat === 'High Risk';
            if (currentFilter === 'Critical Maintenance') return row.maint_status === 'Critical Maintenance';
            return true;
        }}}});

        filtered.forEach(r => {{{{
            const tr = document.createElement('tr');
            const riskClass = r.risk_cat === 'Low Risk' ? 'tag-low' : (r.risk_cat === 'Moderate Risk' ? 'tag-mod' : 'tag-high');
            const maintClass = r.maint_status === 'Good Condition' ? 'tag-good' : (r.maint_status === 'Inspection Due' ? 'tag-warn' : 'tag-crit');
            const savingsColor = r.savings >= 0 ? '#4ade80' : '#f87171';
            const savingsSign = r.savings >= 0 ? '+₹' + r.savings.toLocaleString('en-IN') : '-₹' + Math.abs(r.savings).toLocaleString('en-IN');

            tr.innerHTML = `
                <td><strong>${{{{r.id}}}}</strong></td>
                <td>${{{{r.driver}}}}</td>
                <td>${{{{r.model}}}}</td>
                <td>${{{{r.km}}}} km</td>
                <td class="text-center">${{{{r.harsh_brake}}}}</td>
                <td class="text-center">${{{{r.speeding}}}}</td>
                <td class="text-center">${{{{r.night_pct}}}}%</td>
                <td class="text-center"><strong>${{{{r.safety_score}}}}</strong></td>
                <td><span class="tag ${{{{riskClass}}}}">${{{{r.risk_cat}}}}</span></td>
                <td class="text-center">${{{{r.v_health}}}}</td>
                <td><span class="tag ${{{{maintClass}}}}">${{{{r.maint_status}}}}</span></td>
                <td><strong>₹${{{{r.dynamic_prem.toLocaleString('en-IN')}}}}</strong></td>
                <td style="color: ${{{{savingsColor}}}}; font-weight: 600;">${{{{savingsSign}}}}</td>
                <td><span class="action-link" onclick="loadToSim('${{{{r.id}}}}')">Simulate ⚙️</span></td>
            `;
            tbody.appendChild(tr);
        }}}});
    }}}}

    function filterTable() {{{{
        renderTable();
    }}}}

    function setTableFilter(filterVal, btn) {{{{
        currentFilter = filterVal;
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        renderTable();
    }}}}

    function loadToSim(vehicleId) {{{{
        const r = fleetData.find(v => v.id === vehicleId);
        if (!r) return;

        document.getElementById('inputKm').value = r.km;
        document.getElementById('inputBrake').value = r.harsh_brake;
        document.getElementById('inputSpeed').value = r.speeding;
        document.getElementById('inputNight').value = r.night_pct;
        document.getElementById('inputAccel').value = r.rapid_accel;
        document.getElementById('inputBatt').value = r.batt_v;
        document.getElementById('inputTemp').value = r.eng_temp;
        document.getElementById('inputBrakeWear').value = r.brake_wear;

        updateSim();
        window.scrollTo({{{{ top: 220, behavior: 'smooth' }}}});
    }}}}

    function resetSimulator() {{{{
        document.getElementById('inputKm').value = 800;
        document.getElementById('inputBrake').value = 2;
        document.getElementById('inputSpeed').value = 1;
        document.getElementById('inputNight').value = 6;
        document.getElementById('inputAccel').value = 1;
        document.getElementById('inputBatt').value = 12.6;
        document.getElementById('inputTemp').value = 88;
        document.getElementById('inputBrakeWear').value = 25;
        updateSim();
    }}}}

    // Dynamic Simulator Update Logic
    let radarChartInstance = null;

    function updateSim() {{{{
        const km = parseFloat(document.getElementById('inputKm').value);
        const brake = parseFloat(document.getElementById('inputBrake').value);
        const speed = parseFloat(document.getElementById('inputSpeed').value);
        const night = parseFloat(document.getElementById('inputNight').value);
        const accel = parseFloat(document.getElementById('inputAccel').value);
        const batt = parseFloat(document.getElementById('inputBatt').value);
        const temp = parseFloat(document.getElementById('inputTemp').value);
        const wear = parseFloat(document.getElementById('inputBrakeWear').value);

        // Update control labels
        document.getElementById('valKm').innerText = km + ' km';
        document.getElementById('valBrake').innerText = brake;
        document.getElementById('valSpeed').innerText = speed;
        document.getElementById('valNight').innerText = night + '%';
        document.getElementById('valAccel').innerText = accel;
        document.getElementById('valBatt').innerText = batt.toFixed(1) + ' V';
        document.getElementById('valTemp').innerText = temp + ' °C';
        document.getElementById('valBrakeWear').innerText = wear + '%';

        // 1. Safety Score
        const deduction = (brake * 2.5) + (speed * 3.0) + (night * 0.5) + (accel * 1.5);
        let safetyScore = Math.max(10, Math.min(100, Math.round((100 - deduction) * 10) / 10));

        // 2. Risk Tier & Modifier
        let riskCat = 'Low Risk';
        let riskMod = -0.20;
        let riskTagClass = 'tag-low';
        let riskColor = '#22c55e';
        let behaviorText = '-20% Discount (₹3,000 off)';
        let behaviorColor = '#4ade80';

        if (safetyScore < 60) {{{{
            riskCat = 'High Risk';
            riskMod = 0.25;
            riskTagClass = 'tag-high';
            riskColor = '#ef4444';
            behaviorText = '+25% Surcharge (+₹3,750)';
            behaviorColor = '#f87171';
        }}}} else if (safetyScore < 80) {{{{
            riskCat = 'Moderate Risk';
            riskMod = 0.00;
            riskTagClass = 'tag-mod';
            riskColor = '#f59e0b';
            behaviorText = 'Standard Rate (₹0)';
            behaviorColor = '#fbbf24';
        }}}}

        // 3. Vehicle Health
        let vHealth = 100;
        if (batt < 12.2) vHealth -= 25;
        else if (batt < 12.4) vHealth -= 10;

        if (temp > 100) vHealth -= 30;
        else if (temp > 95) vHealth -= 15;

        if (wear >= 75) vHealth -= 30;
        else if (wear >= 50) vHealth -= 15;

        vHealth = Math.max(15, Math.min(100, vHealth));

        let maintStatus = 'Good Condition';
        let maintBuffer = 0;
        let healthClass = 'tag-good';

        if (vHealth < 60) {{{{
            maintStatus = 'Critical Maintenance';
            maintBuffer = 1500;
            healthClass = 'tag-crit';
        }}}} else if (vHealth < 80) {{{{
            maintStatus = 'Inspection Due';
            maintBuffer = 500;
            healthClass = 'tag-warn';
        }}}}

        // 4. Premium Calculation
        const basePrem = 15000;
        const distFee = Math.round((km / 1000) * 2000);
        const behaviorAdj = Math.round(basePrem * riskMod);
        const dynamicPrem = basePrem + distFee + behaviorAdj + maintBuffer;
        const flatPrem = 22000;
        const savings = flatPrem - dynamicPrem;

        // Update UI
        document.getElementById('simScoreNum').innerText = safetyScore.toFixed(1);
        const circle = document.getElementById('simScoreCircle');
        circle.style.borderColor = riskColor;
        circle.style.backgroundColor = riskColor + '18';

        const riskTag = document.getElementById('simRiskTag');
        riskTag.className = 'tag ' + riskTagClass;
        riskTag.innerText = riskCat;

        const behElem = document.getElementById('simBehaviorAdj');
        behElem.innerText = behaviorText;
        behElem.style.color = behaviorColor;

        const healthTag = document.getElementById('simHealthTag');
        healthTag.className = 'tag ' + healthClass;
        healthTag.innerText = `${{{{maintStatus}}}} (${{{{vHealth}}}}/100)`;

        document.getElementById('simDistFee').innerText = '+₹' + distFee.toLocaleString('en-IN');

        const finalElem = document.getElementById('simFinalPrem');
        const savingsText = savings >= 0
            ? `<span style="font-size: 13px; color: #4ade80; font-weight: normal;">(You Save ₹${{{{savings.toLocaleString('en-IN')}}}} / yr)</span>`
            : `<span style="font-size: 13px; color: #f87171; font-weight: normal;">(₹${{{{Math.abs(savings).toLocaleString('en-IN')}}}} Surcharge over Flat)</span>`;
        finalElem.innerHTML = `₹${{{{dynamicPrem.toLocaleString('en-IN')}}}} ${{{{savingsText}}}}`;

        // Update Radar Chart
        updateRadar(brake, speed, night, accel, (100 - vHealth)/2);
    }}}}

    function updateRadar(brake, speed, night, accel, maintRisk) {{{{
        const ctx = document.getElementById('simRadarChart').getContext('2d');
        const currentData = [
            Math.min(100, brake * 7),
            Math.min(100, speed * 8),
            Math.min(100, night * 2),
            Math.min(100, accel * 10),
            Math.min(100, maintRisk * 2.5)
        ];

        if (radarChartInstance) {{{{
            radarChartInstance.data.datasets[0].data = currentData;
            radarChartInstance.update();
            return;
        }}}}

        radarChartInstance = new Chart(ctx, {{{{
            type: 'radar',
            data: {{{{
                labels: ['Harsh Braking', 'Speed Violations', 'Late Night Risk', 'Rapid Accel', 'Component Wear'],
                datasets: [
                    {{{{
                        label: 'Simulated Driver Risk',
                        data: currentData,
                        backgroundColor: 'rgba(56, 189, 248, 0.25)',
                        borderColor: '#38bdf8',
                        pointBackgroundColor: '#38bdf8',
                        borderWidth: 2
                    }}}},
                    {{{{
                        label: 'Safe Baseline (Target)',
                        data: [15, 10, 10, 15, 10],
                        backgroundColor: 'rgba(34, 197, 94, 0.1)',
                        borderColor: '#22c55e',
                        borderDash: [4, 4],
                        borderWidth: 1.5,
                        pointRadius: 0
                    }}}}
                ]
            }}}},
            options: {{{{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{{{
                    r: {{{{
                        min: 0,
                        max: 100,
                        ticks: {{{{ display: false }}}},
                        grid: {{{{ color: '#334155' }}}},
                        angleLines: {{{{ color: '#334155' }}}},
                        pointLabels: {{{{ color: '#cbd5e1', font: {{{{ size: 11 }}}} }}}}
                    }}}}
                }}}},
                plugins: {{{{
                    legend: {{{{
                        position: 'top',
                        labels: {{{{ color: '#cbd5e1', boxWidth: 12, font: {{{{ size: 11 }}}} }}}}
                    }}}}
                }}}}
            }}}}
        }});
    }}}}

    // Initialize Global Charts
    function initFleetCharts() {{{{
        // Chart 1: Safety Score vs Dynamic Premium
        const ctx1 = document.getElementById('chartScoreVsPrem').getContext('2d');
        const sortedFleet = [...fleetData].sort((a,b) => a.safety_score - b.safety_score);

        new Chart(ctx1, {{{{
            type: 'line',
            data: {{{{
                labels: sortedFleet.map(d => d.safety_score),
                datasets: [
                    {{{{
                        label: 'Dynamic Premium (₹)',
                        data: sortedFleet.map(d => d.dynamic_prem),
                        borderColor: '#38bdf8',
                        backgroundColor: 'rgba(56, 189, 248, 0.15)',
                        fill: true,
                        tension: 0.3,
                        pointRadius: 4,
                        pointBackgroundColor: sortedFleet.map(d => d.risk_cat === 'Low Risk' ? '#22c55e' : (d.risk_cat === 'Moderate Risk' ? '#f59e0b' : '#ef4444'))
                    }}}},
                    {{{{
                        label: 'Flat Benchmark Premium (₹22,000)',
                        data: sortedFleet.map(() => 22000),
                        borderColor: '#94a3b8',
                        borderDash: [5, 5],
                        fill: false,
                        pointRadius: 0
                    }}}}
                ]
            }}}},
            options: {{{{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{{{
                    x: {{{{
                        title: {{{{ display: true, text: 'Driving Safety Score (Low → High)', color: '#94a3b8' }}}},
                        grid: {{{{ color: '#1e293b' }}}},
                        ticks: {{{{ color: '#cbd5e1' }}}}
                    }}}},
                    y: {{{{
                        title: {{{{ display: true, text: 'Annual Premium (₹)', color: '#94a3b8' }}}},
                        grid: {{{{ color: '#334155' }}}},
                        ticks: {{{{ color: '#cbd5e1' }}}}
                    }}}}
                }}}},
                plugins: {{{{
                    legend: {{{{ labels: {{{{ color: '#cbd5e1', boxWidth: 12 }}}} }}}}
                }}}}
            }}}}
        }});

        // Chart 2: Vehicle Health Donut
        const ctx2 = document.getElementById('chartHealthDonut').getContext('2d');
        const goodCount = fleetData.filter(d => d.maint_status === 'Good Condition').length;
        const dueCount = fleetData.filter(d => d.maint_status === 'Inspection Due').length;
        const critCount = fleetData.filter(d => d.maint_status === 'Critical Maintenance').length;

        new Chart(ctx2, {{{{
            type: 'doughnut',
            data: {{{{
                labels: ['Good Condition (>=80)', 'Inspection Due (60-79)', 'Critical Maintenance (<60)'],
                datasets: [{{{{
                    data: [goodCount, dueCount, critCount],
                    backgroundColor: ['#22c55e', '#f59e0b', '#ef4444'],
                    borderColor: '#1e293b',
                    borderWidth: 2
                }}}}]
            }}}},
            options: {{{{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{{{
                    legend: {{{{
                        position: 'bottom',
                        labels: {{{{ color: '#cbd5e1', boxWidth: 12, font: {{{{ size: 11 }}}} }}}}
                    }}}}
                }}}}
            }}}}
        }});
    }}}}

    // Initialize everything on load
    document.addEventListener('DOMContentLoaded', () => {{{{
        renderTable();
        updateSim();
        initFleetCharts();
    }}}});
</script>

</body>
</html>
"""

html_path = os.path.join(DIR, "index.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Interactive HTML Dashboard successfully generated at:", html_path)
