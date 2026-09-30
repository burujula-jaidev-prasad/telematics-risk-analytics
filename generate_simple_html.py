import os
import json
from generate_simple_excel import PROCESSED, DIR

json_data = json.dumps(PROCESSED)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Car Sensor & Insurance Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-dark: #0f172a;
            --text-muted: #64748b;
            --border-color: #e2e8f0;
            --primary-blue: #2563eb;
            --safe-green: #16a34a;
            --risky-red: #dc2626;
            --warning-amber: #d97706;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
        }}

        body {{
            background-color: var(--bg-color);
            color: var(--text-dark);
            line-height: 1.5;
            padding: 24px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        /* Header */
        header {{
            background: var(--card-bg);
            padding: 24px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}

        .header-title h1 {{
            font-size: 22px;
            color: var(--text-dark);
            margin-bottom: 4px;
        }}

        .header-title p {{
            color: var(--text-muted);
            font-size: 14px;
        }}

        .badge-team {{
            display: inline-block;
            background: #eff6ff;
            color: var(--primary-blue);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            margin-top: 6px;
        }}

        .btn-download {{
            background: var(--primary-blue);
            color: #fff;
            padding: 10px 18px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 13px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: background 0.2s;
        }}

        .btn-download:hover {{
            background: #1d4ed8;
        }}

        /* KPI Cards Grid */
        .kpi-title-bar {{
            font-size: 15px;
            font-weight: 700;
            color: var(--text-dark);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 14px;
            margin-bottom: 24px;
        }}

        .kpi-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 16px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        }}

        .kpi-card-header {{
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 6px;
        }}

        .kpi-val {{
            font-size: 24px;
            font-weight: 700;
            color: var(--text-dark);
            margin-bottom: 2px;
        }}

        .kpi-sub {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        /* Simulator & Charts Grid */
        .main-grid {{
            display: grid;
            grid-template-columns: 1.1fr 0.9fr;
            gap: 20px;
            margin-bottom: 24px;
        }}

        @media (max-width: 900px) {{
            .main-grid {{ grid-template-columns: 1fr; }}
        }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}

        .card-header-bar {{
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
            margin-bottom: 16px;
        }}

        .card-header-bar h2 {{
            font-size: 16px;
            font-weight: 700;
            color: var(--text-dark);
        }}

        .card-header-bar p {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        /* Controls */
        .slider-group {{
            margin-bottom: 14px;
        }}

        .slider-label {{
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 4px;
        }}

        .slider-val {{
            font-weight: 700;
            color: var(--primary-blue);
        }}

        input[type=range] {{
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: #cbd5e1;
            outline: none;
            -webkit-appearance: none;
        }}

        input[type=range]::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: var(--primary-blue);
            cursor: pointer;
        }}

        select {{
            width: 100%;
            padding: 8px 12px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            font-size: 13px;
            background: #fff;
            outline: none;
        }}

        /* Simulator Output Box */
        .sim-box {{
            background: #f1f5f9;
            border-radius: 8px;
            padding: 16px;
            margin-top: 14px;
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 16px;
            align-items: center;
        }}

        .score-circle {{
            width: 90px;
            height: 90px;
            border-radius: 50%;
            background: #fff;
            border: 5px solid var(--safe-green);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }}

        .score-val {{
            font-size: 26px;
            font-weight: 800;
            line-height: 1;
        }}

        .score-text {{
            font-size: 10px;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
            margin-top: 2px;
        }}

        .sim-details {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }}

        .sim-pill {{
            background: #fff;
            padding: 8px 10px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }}

        .sim-pill-lbl {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        .sim-pill-val {{
            font-size: 14px;
            font-weight: 700;
            color: var(--text-dark);
        }}

        .tag {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
        }}

        .tag-safe {{ background: #dcfce7; color: #15803d; }}
        .tag-avg {{ background: #fef3c7; color: #b45309; }}
        .tag-risk {{ background: #fee2e2; color: #b91c1c; }}

        /* Charts */
        .chart-container {{
            position: relative;
            height: 220px;
            margin-bottom: 16px;
        }}

        /* Table Section */
        .table-wrap {{
            overflow-x: auto;
            border: 1px solid var(--border-color);
            border-radius: 8px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
            background: #fff;
        }}

        th {{
            background: #f8fafc;
            color: var(--text-muted);
            font-weight: 600;
            padding: 10px 12px;
            border-bottom: 1px solid var(--border-color);
            white-space: nowrap;
        }}

        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #f1f5f9;
            white-space: nowrap;
        }}

        tr:hover td {{
            background: #f8fafc;
        }}

        tr.fleet-avg-row td {{
            background: #eff6ff !important;
            font-weight: 700;
            color: var(--primary-blue);
            border-top: 2px solid #bfdbfe;
        }}

        /* Simple Rule Explainer */
        .rule-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 14px;
            margin-top: 14px;
        }}

        .rule-card {{
            background: #f8fafc;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px 14px;
        }}

        .rule-card h3 {{
            font-size: 13px;
            font-weight: 700;
            color: var(--primary-blue);
            margin-bottom: 4px;
        }}

        .rule-card p {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        .formula-tag {{
            display: inline-block;
            background: #e2e8f0;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 11px;
            color: #1e293b;
            margin-top: 4px;
        }}

        footer {{
            text-align: center;
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 24px;
            padding-top: 14px;
            border-top: 1px solid var(--border-color);
        }}
    </style>
</head>
<body>

<div class="container">
    <!-- Header -->
    <header>
        <div class="header-title">
            <h1>🚗 Car Sensor & Dynamic Insurance Analytics</h1>
            <p>Simple sensor-based driving score, maintenance alerts, and dynamic premium model</p>
            <div class="badge-team">Presentation: Driving Risk & Insurance Analytics · Jaidev Prasad · Ruth Wilson · Bala Kiran</div>
        </div>
        <div>
            <a href="Simple_Car_Sensor_Insurance_Analysis.xlsx" class="btn-download" download>
                📥 Download Simple Excel (.xlsx)
            </a>
        </div>
    </header>

    <!-- Top Fleet Averages (Simple Summary) -->
    <div class="kpi-title-bar">📊 Fleet Average Statistics (15 Cars Monitored)</div>
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-card-header">Avg Driving Score</div>
            <div class="kpi-val" id="kpiScore">57.3 <span style="font-size: 14px; font-weight: normal; color: var(--text-muted);">/ 100</span></div>
            <div class="kpi-sub">Formula: 100 - Penalties</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-card-header">Avg Harsh Brakes</div>
            <div class="kpi-val" id="kpiBrakes">5.3</div>
            <div class="kpi-sub">Braking events per driver</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-card-header">Avg Speeding Events</div>
            <div class="kpi-val" id="kpiSpeed">3.4</div>
            <div class="kpi-sub">Speed violations recorded</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-card-header">Avg Dynamic Premium</div>
            <div class="kpi-val" id="kpiPrem">₹15,933</div>
            <div class="kpi-sub">vs ₹18,000 Standard flat rate</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-card-header">Total Safe Driver Savings</div>
            <div class="kpi-val" style="color: var(--safe-green);" id="kpiSavings">₹31,000</div>
            <div class="kpi-sub">Combined fleet discount</div>
        </div>
    </div>

    <!-- Simulator and Charts Section -->
    <div class="main-grid">
        <!-- Interactive Simulator -->
        <div class="card">
            <div class="card-header-bar">
                <h2>🎛️ Simple Driver & Premium Calculator</h2>
                <p>Move the sliders below to see how sensor readings instantly change driving score and insurance price</p>
            </div>

            <div class="slider-group">
                <div class="slider-label">
                    <span>Harsh Braking Count (-3 pts each)</span>
                    <span class="slider-val" id="valBrakes">2</span>
                </div>
                <input type="range" id="inputBrakes" min="0" max="15" value="2" oninput="calculateLive()">
            </div>

            <div class="slider-group">
                <div class="slider-label">
                    <span>Speeding Incidents (-4 pts each)</span>
                    <span class="slider-val" id="valSpeed">1</span>
                </div>
                <input type="range" id="inputSpeed" min="0" max="12" value="1" oninput="calculateLive()">
            </div>

            <div class="slider-group">
                <div class="slider-label">
                    <span>Late-Night Driving Hours (-2 pts/hr)</span>
                    <span class="slider-val" id="valNight">3 hrs</span>
                </div>
                <input type="range" id="inputNight" min="0" max="20" value="3" oninput="calculateLive()">
            </div>

            <div class="slider-group">
                <div class="slider-label">
                    <span>Car Health / Engine Diagnostics</span>
                    <span class="slider-val" id="valHealthText">Good (+₹0)</span>
                </div>
                <select id="inputHealth" onchange="calculateLive()">
                    <option value="Good">Good Condition (No Fee)</option>
                    <option value="Fair">Fair Condition (No Fee)</option>
                    <option value="Alert">Maintenance Alert (+₹1,000 inspection fee)</option>
                </select>
            </div>

            <!-- Simulator Output -->
            <div class="sim-box">
                <div class="score-circle" id="simCircle">
                    <div class="score-val" id="simScore">84</div>
                    <div class="score-text">Score</div>
                </div>
                <div class="sim-details">
                    <div class="sim-pill">
                        <div class="sim-pill-lbl">Driver Risk Category</div>
                        <div class="sim-pill-val"><span class="tag tag-safe" id="simTag">Safe Driver</span></div>
                    </div>
                    <div class="sim-pill">
                        <div class="sim-pill-lbl">Driving Adjustment</div>
                        <div class="sim-pill-val" id="simAdj" style="color: var(--safe-green);">-₹3,000 Discount</div>
                    </div>
                    <div class="sim-pill" style="grid-column: span 2; background: #eff6ff; border-color: #bfdbfe;">
                        <div class="sim-pill-lbl">Dynamic Final Premium</div>
                        <div class="sim-pill-val" style="font-size: 17px; color: var(--primary-blue);" id="simPrem">
                            ₹12,000 <span style="font-size: 12px; font-weight: normal; color: var(--safe-green);">(You Save ₹6,000)</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Visual Charts Card -->
        <div class="card">
            <div class="card-header-bar">
                <h2>📈 Simple Charts & Visuals</h2>
                <p>Driving score vs insurance pricing comparison</p>
            </div>
            <div class="chart-container">
                <canvas id="chartComparison"></canvas>
            </div>
            <div style="font-size: 12px; color: var(--text-muted); text-align: center;">
                💡 Safe drivers pay <strong>₹12,000</strong> while risky drivers pay <strong>₹18,000 - ₹19,000</strong> based on telematics sensor data.
            </div>
        </div>
    </div>

    <!-- Simple Table Section -->
    <div class="card" style="margin-bottom: 24px;">
        <div class="card-header-bar">
            <h2>📋 Fleet Telematics Dataset (15 Drivers + Fleet Average)</h2>
            <p>Every calculation uses basic arithmetic and simple averages</p>
        </div>

        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>Car ID</th>
                        <th>Driver Name</th>
                        <th>Car Model</th>
                        <th>Monthly KM</th>
                        <th>Harsh Brakes</th>
                        <th>Speeding</th>
                        <th>Night Hrs</th>
                        <th>Car Health</th>
                        <th>Safety Score</th>
                        <th>Risk Tier</th>
                        <th>Dynamic Premium</th>
                        <th>Driver Savings</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                    <!-- Loaded by JS -->
                </tbody>
            </table>
        </div>
    </div>

    <!-- Very Simple Logic Explainer -->
    <div class="card">
        <div class="card-header-bar">
            <h2>💡 Simple Analytical Logic Used in this Project</h2>
            <p>Clear, straightforward rules suitable for submission and academic evaluation</p>
        </div>

        <div class="rule-grid">
            <div class="rule-card">
                <h3>1. Driving Score Formula</h3>
                <p>Start at 100 points, subtract points for risky sensor triggers:</p>
                <div class="formula-tag">Score = 100 - (Brakes × 3) - (Speeding × 4) - (Night_Hrs × 2)</div>
            </div>

            <div class="rule-card">
                <h3>2. Risk Category Rules</h3>
                <p>Categorize drivers into 3 clear groups based on score:</p>
                <div class="formula-tag">Score ≥ 80: Safe · 60–79: Average · &lt; 60: Risky</div>
            </div>

            <div class="rule-card">
                <h3>3. Dynamic Insurance Pricing</h3>
                <p>Base rate is ₹15,000 with reward/penalty adjustments:</p>
                <div class="formula-tag">Safe: -₹3,000 | Average: ₹0 | Risky: +₹3,000</div>
            </div>

            <div class="rule-card">
                <h3>4. Quality & Maintenance Alert</h3>
                <p>If sensors detect engine/component issues, add inspection fee:</p>
                <div class="formula-tag">Alert Status: +₹1,000 Maintenance Fee</div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer>
        <p>Simple Car Sensor & Insurance Telematics Analytics · CIA 3 Submission</p>
        <p style="margin-top: 4px;">Jaidev Prasad (25121019) · Ruth Wilson (25121034) · Bala Kiran (25121012)</p>
    </footer>
</div>

<script>
    const data = {json_data};

    // Render Table
    function renderTable() {{{{
        const tbody = document.getElementById('tableBody');
        tbody.innerHTML = '';

        let totalKm = 0, totalBrakes = 0, totalSpeed = 0, totalNight = 0, totalScore = 0, totalPrem = 0, totalSavings = 0;

        data.forEach(r => {{{{
            totalKm += r.km;
            totalBrakes += r.brakes;
            totalSpeed += r.speeding;
            totalNight += r.night_hrs;
            totalScore += r.score;
            totalPrem += r.dyn_prem;
            totalSavings += r.savings;

            const tr = document.createElement('tr');
            const tagClass = r.score >= 80 ? 'tag-safe' : (r.score >= 60 ? 'tag-avg' : 'tag-risk');
            const savingsColor = r.savings >= 0 ? 'var(--safe-green)' : 'var(--risky-red)';
            const savingsText = r.savings >= 0 ? '+₹' + r.savings.toLocaleString('en-IN') : '-₹' + Math.abs(r.savings).toLocaleString('en-IN');

            tr.innerHTML = `
                <td><strong>${{{{r.id}}}}</strong></td>
                <td>${{{{r.name}}}}</td>
                <td>${{{{r.car}}}}</td>
                <td>${{{{r.km}}}} km</td>
                <td>${{{{r.brakes}}}}</td>
                <td>${{{{r.speeding}}}}</td>
                <td>${{{{r.night_hrs}}}} hrs</td>
                <td>${{{{r.health}}}}</td>
                <td><strong>${{{{r.score}}}}</strong></td>
                <td><span class="tag ${{{{tagClass}}}}">${{{{r.category}}}}</span></td>
                <td><strong>₹${{{{r.dyn_prem.toLocaleString('en-IN')}}}}</strong></td>
                <td style="color: ${{{{savingsColor}}}}; font-weight: 600;">${{{{savingsText}}}}</td>
            `;
            tbody.appendChild(tr);
        }}}});

        // Average Row
        const count = data.length;
        const avgRow = document.createElement('tr');
        avgRow.className = 'fleet-avg-row';
        avgRow.innerHTML = `
            <td><strong>FLEET AVG</strong></td>
            <td>-</td>
            <td>-</td>
            <td>${{{{(totalKm / count).toFixed(1)}}}} km</td>
            <td>${{{{(totalBrakes / count).toFixed(1)}}}}</td>
            <td>${{{{(totalSpeed / count).toFixed(1)}}}}</td>
            <td>${{{{(totalNight / count).toFixed(1)}}}} hrs</td>
            <td>-</td>
            <td><strong>${{{{(totalScore / count).toFixed(1)}}}}</strong></td>
            <td>-</td>
            <td><strong>₹${{{{Math.round(totalPrem / count).toLocaleString('en-IN')}}}}</strong></td>
            <td style="color: var(--safe-green); font-weight: 700;">Total: ₹${{{{totalSavings.toLocaleString('en-IN')}}}}</td>
        `;
        tbody.appendChild(avgRow);
    }}}}

    // Live Simulator Calculation
    function calculateLive() {{{{
        const brakes = parseInt(document.getElementById('inputBrakes').value);
        const speed = parseInt(document.getElementById('inputSpeed').value);
        const night = parseInt(document.getElementById('inputNight').value);
        const health = document.getElementById('inputHealth').value;

        // Labels
        document.getElementById('valBrakes').innerText = brakes;
        document.getElementById('valSpeed').innerText = speed;
        document.getElementById('valNight').innerText = night + ' hrs';
        document.getElementById('valHealthText').innerText = health === 'Alert' ? 'Alert (+₹1,000)' : health + ' (+₹0)';

        // Simple Score Calculation: 100 - (brakes*3) - (speed*4) - (night*2)
        const deduction = (brakes * 3) + (speed * 4) + (night * 2);
        let score = Math.max(20, Math.min(100, 100 - deduction));

        let category = 'Safe Driver';
        let tagClass = 'tag-safe';
        let circleBorder = 'var(--safe-green)';
        let riskAdj = -3000;
        let adjText = '-₹3,000 Discount';
        let adjColor = 'var(--safe-green)';

        if (score < 60) {{{{
            category = 'Risky Driver';
            tagClass = 'tag-risk';
            circleBorder = 'var(--risky-red)';
            riskAdj = 3000;
            adjText = '+₹3,000 Surcharge';
            adjColor = 'var(--risky-red)';
        }}}} else if (score < 80) {{{{
            category = 'Average Driver';
            tagClass = 'tag-avg';
            circleBorder = 'var(--warning-amber)';
            riskAdj = 0;
            adjText = '₹0 (Standard)';
            adjColor = 'var(--warning-amber)';
        }}}}

        const maintFee = health === 'Alert' ? 1000 : 0;
        const dynamicPrem = 15000 + riskAdj + maintFee;
        const standardFlat = 18000;
        const savings = standardFlat - dynamicPrem;

        // Update UI
        document.getElementById('simScore').innerText = score;
        const circle = document.getElementById('simCircle');
        circle.style.borderColor = circleBorder;

        const tag = document.getElementById('simTag');
        tag.className = 'tag ' + tagClass;
        tag.innerText = category;

        const adjElem = document.getElementById('simAdj');
        adjElem.innerText = adjText;
        adjElem.style.color = adjColor;

        const premElem = document.getElementById('simPrem');
        const savingsSpan = savings >= 0
            ? `<span style="font-size: 12px; font-weight: normal; color: var(--safe-green);">(You Save ₹${{{{savings.toLocaleString('en-IN')}}}})</span>`
            : `<span style="font-size: 12px; font-weight: normal; color: var(--risky-red);">(₹${{{{Math.abs(savings).toLocaleString('en-IN')}}}} higher than flat)</span>`;
        premElem.innerHTML = `₹${{{{dynamicPrem.toLocaleString('en-IN')}}}} ${{{{savingsSpan}}}}`;
    }}}}

    // Simple Bar Chart
    function initSimpleChart() {{{{
        const ctx = document.getElementById('chartComparison').getContext('2d');
        new Chart(ctx, {{{{
            type: 'bar',
            data: {{{{
                labels: ['Safe Driver (Score ≥ 80)', 'Average Driver (60-79)', 'Risky Driver (< 60)', 'Standard Flat Rate'],
                datasets: [{{{{
                    label: 'Annual Premium (₹)',
                    data: [12000, 15000, 18000, 18000],
                    backgroundColor: ['#22c55e', '#f59e0b', '#ef4444', '#94a3b8'],
                    borderRadius: 6
                }}}}]
            }}}},
            options: {{{{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{{{
                    legend: {{{{ display: false }}}}
                }}}},
                scales: {{{{
                    y: {{{{
                        beginAtZero: true,
                        max: 20000,
                        ticks: {{{{
                            callback: function(value) {{{{ return '₹' + value.toLocaleString('en-IN'); }}}}
                        }}}}
                    }}}}
                }}}}
            }}}}
        }});
    }}}}

    document.addEventListener('DOMContentLoaded', () => {{{{
        renderTable();
        calculateLive();
        initSimpleChart();
    }}}});
</script>

</body>
</html>
"""

html_path = os.path.join(DIR, "index.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Simple HTML dashboard written to:", html_path)
