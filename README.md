# 🚗 Connected Vehicle Telematics & Risk Analytics Dashboard

> **Automobile Industry CIA 3 Project**  
> **Authors**: Jaidev Prasad (25121019) • Ruth Wilson (25121034) • Bala Kiran (25121012)

---

## 🌟 Live Interactive Dashboard
🌐 **[Click here to open the Live Dashboard](https://burujula-jaidev-prasad.github.io/telematics-risk-analytics/)**
*(Live on GitHub Pages — accessible from anywhere, any device)*

---

## 📌 Project Overview
This project presents an end-to-end connected vehicle telematics architecture combining real-time driver telemetry (harsh braking deceleration G-forces, speeding events, night driving duration) with OBD-II engine and component health sensors (coolant temperatures, oil pressure PSI, brake pad thickness wear, battery voltage, and TPMS tire pressure).

### Core Features:
- 📊 **10 Interactive Visualizations**: Speeding spectrum, G-force braking events, crash claim vs renewal hike probability curves, thermal engine scatter matrix, brake pad degradation, and battery health.
- 🧮 **Mathematical Actuarial Pricing Engine**: Dynamic Pay-How-You-Drive (PHYD) pricing formulas deducting points for risk behaviors and rewarding safe driving with premium discounts.
- 🚗 **15-Vehicle Fleet Ledger**: Live metrics, safety score, claim probability, hike chance, and dynamic pricing calculations.
- 🛠️ **Component Health Diagnostics**: Real-time OBD diagnostic trouble codes (DTCs), early warning detection, and maintenance cost forecasts.
- 🧪 **Interactive Driver Risk Simulator**: Real-time slider simulator recalculating scores, premiums, and risk probabilities on the fly.
- 🔍 **Interactive Vehicle Forensics Drawer**: Detailed event timelines, deceleration traces, and component gauges for individual vehicles.

---

## 📁 Repository Structure
```text
├── index.html                                    # Main single-file interactive web dashboard
├── Car_Telematics_Insurance_Risk_Project_Report.pdf # 2-Page technical & executive project summary report
├── Simple_Car_Sensor_Insurance_Analysis.xlsx     # Multi-sheet academic submission Excel workbook with formulas
├── detailed_telematics_sensor_data.csv           # Complete 28-feature master telemetry sensor dataset
├── generate_realistic_data.py                    # Python data pipeline generator
└── generate_pdf_report.py                        # Standalone PDF generation script
```

---

## 🧮 Mathematical Scoring & Pricing Engine
$$\text{Driving Safety Score} = 100 - (\text{Harsh Brakes} \times 3) - (\text{Speeding Violations} \times 4) - (\text{Night Driving Hours} \times 2)$$

$$\text{Dynamic Premium} = \text{Base Rate (₹15,000)} + \text{Risk Adjustment} + \text{Maintenance Alert Surcharge}$$
