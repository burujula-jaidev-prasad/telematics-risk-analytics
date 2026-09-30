# 🚗 Connected Vehicle Telematics, Engine Sensors & Insurance Intelligence

> **Automobile Industry CIA 3 Project**  
> **Authors**: Jaidev Prasad (25121019) • Ruth Wilson (25121034) • Bala Kiran (25121012)

---

## 🌟 Live Interactive Web Dashboard
🌐 **[Click here to open the Live Dashboard](https://burujula-jaidev-prasad.github.io/telematics-risk-analytics/)**  
*(Hosted live on GitHub Pages — 100% interactive on any phone, laptop, or browser)*

---

## 📌 Project Overview
This project presents an end-to-end connected vehicle telematics framework combining real-time driver behavioral telemetry (harsh braking deceleration G-forces, speeding violations, night driving hours) with OBD-II engine and component health diagnostics (coolant temperature, combustion oil pressure PSI, brake pad wear, battery voltage, and TPMS tire pressure) to create transparent, fair, dynamic **Pay-How-You-Drive (PHYD)** insurance premiums.

---

## 🧮 Mathematical Scoring, Pricing & Actuarial Probability Engine

### 1. Driving Safety Score Formula ($0 - 100\text{ points}$)
$$\text{Safety Score} = \max\Big(20, \, \min\big(100, \, 100 - (3 \times \text{Harsh Brakes}) - (4 \times \text{Speeding Violations}) - (2 \times \text{Night Driving Hours})\big)\Big)$$

#### Why These Specific Penalty Weights?
* **Harsh Deceleration Stops ($-3\text{ pts/event}$)**:
  - Telematics accelerometers detect emergency braking exceeding $-0.40\text{g}$ (and $-0.65\text{g}$ ABS lockups).
  - High deceleration frequency directly correlates with aggressive tailgating, distracted driving, and delayed hazard perception.
* **Speeding Violations ($-4\text{ pts/violation}$)**:
  - Carries the highest penalty weight because kinetic impact energy scales with the square of velocity ($E_k = \frac{1}{2}mv^2$).
  - High-speed driving drastically compresses human reaction distance and amplifies accident severity.
* **Late-Night Driving ($-2\text{ pts/hr}$)**:
  - Telematics tracks cumulative operating hours between 11:00 PM and 05:00 AM.
  - Actuarial fatality risk during this window is $3.2\times$ higher due to circadian fatigue, reduced illumination, and higher frequency of impaired drivers on the road.

---

### 2. Dynamic PHYD Insurance Premium Formula
$$\text{Dynamic Annual Premium} = \text{Base Standard Rate (₹15,000)} + \text{Safety Score Adjustment} + \text{Component Health Alert Fee}$$

| Driving Score Tier | Risk Profile | Score Risk Adjustment | Diagnostic Alert Fee | Final Dynamic Premium | Savings vs ₹18k Flat Benchmark |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Score $\ge 80$** | **Safe (Low Risk)** | **$-₹3,000$ (Discount)** | ₹0 | **₹12,000 / yr** | **+₹6,000 (33% Savings)** |
| **Score $60 - 79$** | **Average (Moderate)** | **₹0 (Standard Base)** | ₹0 | **₹15,000 / yr** | **+₹3,000 (17% Savings)** |
| **Score $< 60$** | **Risky (High Risk)** | **$+₹3,000$ (Surcharge)** | ₹0 | **₹18,000 / yr** | **₹0 (Par with Flat)** |
| **Score $< 60$ + Alert** | **Severe Dual Risk** | **$+₹3,000$ (Surcharge)** | **$+₹1,000$** | **₹19,000 / yr** | **$-₹1,000$ (Net Penalty)** |

---

### 3. Actuarial Crash Claim Probability (%) Formula
$$\text{Crash Claim Probability (\%)} = \text{Base Frequency (3.5\%)} + \left[(100 - \text{Score}) \times 0.55\%\right] + \text{Deceleration Severity Factor}$$

* **Safe Drivers ($\text{Score } 80 - 100$)**: Baseline claim probability remains low between **$3.8\% - 6.2\%$**.
* **Moderate Drivers ($\text{Score } 60 - 79$)**: Controlled claim likelihood between **$10.5\% - 18.0\%$**.
* **High-Risk Drivers ($\text{Score } < 60$)**: Steep exponential escalation between **$38.5\% - 48.0\%$** due to compound tailgating and high-speed telemetry triggers.

---

### 4. Annual Policy Renewal Hike Chance (%) Formula
$$\text{Renewal Hike Chance (\%)} = \frac{100}{1 + e^{0.10 \times (\text{Score} - 55)}} + \text{OBD-II Fault Loading}$$

* **Safe Drivers ($\text{Score } \ge 80$)**: **$< 5\%$** (Guaranteed eligibility for locked safe driver discounts).
* **Average Drivers ($\text{Score } 60 - 79$)**: **$25\% - 45\%$** (Standard baseline renewal indexed to normal inflation).
* **Risky Drivers ($\text{Score } < 60$)**: **$88\% - 98\%$** (High certainty of premium loading and rate escalation).

---

## 🔧 OBD-II Engine & Component Diagnostics Health Matrix

| Sensor Component | Normal Operating Tolerance | Critical Alert Trigger | Telematics Actuarial Rationale |
| :--- | :--- | :--- | :--- |
| **Engine Coolant Temp (ECT)** | $85^\circ\text{C} - 95^\circ\text{C}$ | $> 100^\circ\text{C}$ (Overheat) | Prevents blown cylinder head gaskets, engine seizure, and fraudulent breakdown claims. |
| **Combustion Oil Pressure** | $30 - 60\text{ PSI}$ | $< 20\text{ PSI}$ (Low Pressure) | Detects oil starvation, aggressive RPM redlining, and premature crankshaft bearing wear. |
| **12V Electrical Battery** | $12.4\text{V} - 12.8\text{V}$ | $< 12.1\text{V}$ (Low Voltage) | Predicts alternator degradation and roadside dead battery service calls. |
| **Brake Pad Thickness** | $> 5.0\text{ mm}$ | $< 3.0\text{ mm}$ (Worn Pad) | Correlates high-G deceleration stops ($-0.74\text{g}$) with friction pad wear, preventing catastrophic brake failure. |
| **TPMS Tire Pressure** | $32 - 35\text{ PSI}$ | $< 28\text{ PSI}$ (Low Pressure) | Eliminates high-speed expressway blowouts and optimizes rolling fuel efficiency. |

---

## 🔍 Concrete Worked Example (Safe vs High-Risk)

### Case A: `CAR-03` (Rohan Mehta - Tata Nexon EV Max)
- **Sensor Inputs**: 1 Harsh Brake, 0 Speeding Violations, 2 Night Driving Hours.
- **Engine Diagnostics**: Temp $84^\circ\text{C}$, Oil $50\text{ PSI}$, Battery $13.0\text{V}$, Brake Pad $10.5\text{ mm}$ (Status: Good).
- **Calculations**:
  $$\text{Score} = 100 - (1 \times 3) - (0 \times 4) - (2 \times 2) = 100 - 3 - 0 - 4 = 93\text{ (Safe Tier)}$$
  $$\text{Dynamic Premium} = ₹15,000 - ₹3,000 + ₹0 = ₹12,000\text{/yr}\quad (\text{Saves } ₹6,000)$$
  $$\text{Claim Probability} = 3.8\% \quad\mid\quad \text{Renewal Hike Chance} = 2.0\%$$

### Case B: `CAR-11` (Siddharth Das - Mahindra Thar LX 4x4)
- **Sensor Inputs**: 11 Harsh Brakes ($-0.74\text{g}$ ABS), 8 Speeding Violations ($134\text{ km/h}$ peak), 16 Night Hours.
- **Engine Diagnostics**: Temp $106^\circ\text{C}$ (Overheat), Oil $18\text{ PSI}$ (Low), Battery $11.7\text{V}$, Brake Pad $2.0\text{ mm}$ (Alert).
- **Calculations**:
  $$\text{Score} = 100 - (11 \times 3) - (8 \times 4) - (16 \times 2) = 100 - 33 - 32 - 32 = 3 \implies \text{Floor at } 20\text{ (Risky Tier)}$$
  $$\text{Dynamic Premium} = ₹15,000 + ₹3,000 + ₹1,000 = ₹19,000\text{/yr}\quad (\text{Penalty } ₹1,000)$$
  $$\text{Claim Probability} = 48.0\% \quad\mid\quad \text{Renewal Hike Chance} = 98.0\%$$

---

## 📁 Repository Deliverables
```text
├── index.html                                    # Main interactive single-file dashboard (Chart.js, simulator, modals)
├── Car_Telematics_Insurance_Risk_Project_Report.pdf # 2-Page technical & executive project summary report
├── Simple_Car_Sensor_Insurance_Analysis.xlsx     # Multi-sheet academic submission Excel workbook with formulas
├── detailed_telematics_sensor_data.csv           # Complete 28-feature master telemetry sensor dataset
├── generate_realistic_data.py                    # Python data pipeline generator
└── generate_pdf_report.py                        # Standalone PDF generation script
```
