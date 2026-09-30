import os
import csv
import json
import zipfile
import html

DIR = "/Users/jaidevprasad/.gemini/antigravity/scratch/telematics_risk_analytics"
os.makedirs(DIR, exist_ok=True)

# 15 Detailed Realistic Vehicles with Engine Sensors & Probability Analytics
CARS = [
    {
        "id": "CAR-01", "vin": "MBH1234567A8901", "reg": "KA-01-MJ-4521", "driver": "Aarav Sharma", "car": "Hyundai Creta SX (O)", "year": 2023, "odo": 14250,
        "route": "Bengaluru (ORR - Whitefield)", "km": 750, "brakes": 2, "max_decel_g": "-0.42g",
        "brake_events": [
            {"time": "14-Sep 08:42:10", "speed_drop": "62 → 18 km/h", "g_force": "-0.42g", "location": "Marathahalli Junction", "cause": "Pedestrian crossing"},
            {"time": "22-Sep 19:15:33", "speed_drop": "55 → 10 km/h", "g_force": "-0.39g", "location": "Silk Board Flyover", "cause": "Abrupt lane merger"}
        ],
        "speeding": 1, "max_speed": 86, "speed_limit": 80,
        "speed_events": [{"time": "18-Sep 21:10:05", "speed": "86 km/h (Limit: 80)", "duration": "4 mins", "location": "Airport Expressway"}],
        "night_hrs": 3,
        "night_trips": [{"date": "05-Sep", "time_window": "11:30 PM - 01:00 AM", "km": 42, "purpose": "Late commute"}],
        "temp_c": 88, "oil_psi": 45, "rpm_max": 3200, "batt_v": 12.6, "brake_pad_mm": 9.2, "tpms": {"fl": 33, "fr": 33, "rl": 33, "rr": 33},
        "dtc_code": "None (System Healthy)", "health": "Good",
        "claim_prob": 6.2, "hike_prob": 4.0,
        "maint_rec": "Normal servicing in 5,750 km. Engine thermal balance and oil pressure optimal."
    },
    {
        "id": "CAR-02", "vin": "MAT9876543B1234", "reg": "MH-02-DN-8842", "driver": "Priya Nair", "car": "Maruti Brezza ZXi+", "year": 2022, "odo": 28900,
        "route": "Mumbai (Western Express Hwy)", "km": 1400, "brakes": 8, "max_decel_g": "-0.68g (ABS Active)",
        "brake_events": [
            {"time": "04-Sep 23:45:12", "speed_drop": "88 → 12 km/h", "g_force": "-0.68g (ABS)", "location": "Bandra-Worli Sea Link Exit", "cause": "Tailgating hard emergency stop"},
            {"time": "11-Sep 01:20:40", "speed_drop": "76 → 20 km/h", "g_force": "-0.61g", "location": "Andheri Flyover", "cause": "Late reaction to roadblock"},
            {"time": "19-Sep 02:15:18", "speed_drop": "82 → 15 km/h", "g_force": "-0.64g (ABS)", "location": "Goregaon Hub", "cause": "High speed cut-in"}
        ],
        "speeding": 5, "max_speed": 112, "speed_limit": 80,
        "speed_events": [
            {"time": "04-Sep 23:30:10", "speed": "112 km/h (Limit: 80)", "duration": "14 mins", "location": "Sea Link Stretch"},
            {"time": "11-Sep 01:05:00", "speed": "104 km/h (Limit: 80)", "duration": "9 mins", "location": "WEH Northbound"}
        ],
        "night_hrs": 12,
        "night_trips": [
            {"date": "04-Sep", "time_window": "11:15 PM - 02:45 AM", "km": 110, "purpose": "Night highway run"},
            {"date": "11-Sep", "time_window": "12:30 AM - 03:15 AM", "km": 85, "purpose": "Late night travel"}
        ],
        "temp_c": 102, "oil_psi": 28, "rpm_max": 5100, "batt_v": 11.9, "brake_pad_mm": 2.8, "tpms": {"fl": 28, "fr": 27, "rl": 32, "rr": 31},
        "dtc_code": "P0128 (Coolant Temp Warning), P0562 (Low System Voltage)", "health": "Alert",
        "claim_prob": 38.5, "hike_prob": 88.0,
        "maint_rec": "CRITICAL: Brake pads worn to 2.8mm (<3.0mm limit). Engine coolant peaked at 102°C and battery voltage low (11.9V)."
    },
    {
        "id": "CAR-03", "vin": "TAT4567890C5678", "reg": "DL-08-CC-1902", "driver": "Rohan Mehta", "car": "Tata Nexon EV Max", "year": 2024, "odo": 6800,
        "route": "Delhi NCR (Noida Expressway)", "km": 500, "brakes": 1, "max_decel_g": "-0.32g",
        "brake_events": [{"time": "15-Sep 10:12:00", "speed_drop": "48 → 10 km/h", "g_force": "-0.32g", "location": "DND Toll Plaza", "cause": "Regenerative braking"}],
        "speeding": 0, "max_speed": 68, "speed_limit": 70, "speed_events": [],
        "night_hrs": 2, "night_trips": [{"date": "08-Sep", "time_window": "11:00 PM - 12:15 AM", "km": 28, "purpose": "Dinner return"}],
        "temp_c": 84, "oil_psi": 50, "rpm_max": 2800, "batt_v": 13.0, "brake_pad_mm": 10.5, "tpms": {"fl": 34, "fr": 34, "rl": 34, "rr": 34},
        "dtc_code": "None (All Systems Healthy)", "health": "Good",
        "claim_prob": 3.8, "hike_prob": 2.0,
        "maint_rec": "EV battery cell balance optimal. Brake regeneration preserving pad thickness."
    },
    {
        "id": "CAR-04", "vin": "MAH6789012D3456", "reg": "KA-05-NB-9011", "driver": "Sneha Kulkarni", "car": "Mahindra XUV700 AX7", "year": 2023, "odo": 31200,
        "route": "Bengaluru (Hosur Rd - E-City)", "km": 1800, "brakes": 10, "max_decel_g": "-0.72g (Emergency Braking)",
        "brake_events": [
            {"time": "07-Sep 00:15:22", "speed_drop": "105 → 20 km/h", "g_force": "-0.72g", "location": "E-City Elevated Toll", "cause": "FCW Automatic Emergency Brake trigger"},
            {"time": "14-Sep 02:40:11", "speed_drop": "94 → 15 km/h", "g_force": "-0.65g", "location": "Bommasandra Stretch", "cause": "Heavy truck obstacle avoidance"}
        ],
        "speeding": 7, "max_speed": 128, "speed_limit": 80,
        "speed_events": [
            {"time": "07-Sep 00:05:00", "speed": "128 km/h (Limit: 80)", "duration": "18 mins", "location": "Elevated Expressway"},
            {"time": "21-Sep 23:50:30", "speed": "118 km/h (Limit: 80)", "duration": "12 mins", "location": "Hosur Highway"}
        ],
        "night_hrs": 15,
        "night_trips": [
            {"date": "07-Sep", "time_window": "11:45 PM - 03:30 AM", "km": 160, "purpose": "Intercity night transit"},
            {"date": "21-Sep", "time_window": "12:10 AM - 02:50 AM", "km": 115, "purpose": "Late transit"}
        ],
        "temp_c": 105, "oil_psi": 22, "rpm_max": 5400, "batt_v": 11.8, "brake_pad_mm": 2.2, "tpms": {"fl": 30, "fr": 29, "rl": 31, "rr": 30},
        "dtc_code": "P0217 (Engine Overheat Condition), P0562 (Battery Voltage Low)", "health": "Alert",
        "claim_prob": 44.0, "hike_prob": 94.0,
        "maint_rec": "CRITICAL: Severe brake pad wear (2.2mm). Engine coolant hit 105°C and low oil pressure logged at high RPM."
    },
    {
        "id": "CAR-05", "vin": "MAK3456789E7890", "reg": "DL-03-AB-7744", "driver": "Vikram Singh", "car": "Honda City ZX", "year": 2022, "odo": 21500,
        "route": "Delhi (Ring Road - CP)", "km": 900, "brakes": 4, "max_decel_g": "-0.45g",
        "brake_events": [{"time": "10-Sep 18:30:15", "speed_drop": "60 → 15 km/h", "g_force": "-0.45g", "location": "Moti Bagh Junction", "cause": "Bumper traffic stop"}],
        "speeding": 2, "max_speed": 88, "speed_limit": 70,
        "speed_events": [{"time": "12-Sep 15:40:00", "speed": "88 km/h (Limit: 70)", "duration": "5 mins", "location": "Barapullah Elevated"}],
        "night_hrs": 5, "night_trips": [{"date": "16-Sep", "time_window": "11:15 PM - 12:45 AM", "km": 40, "purpose": "Weekend commute"}],
        "temp_c": 89, "oil_psi": 42, "rpm_max": 3400, "batt_v": 12.5, "brake_pad_mm": 6.8, "tpms": {"fl": 32, "fr": 32, "rl": 32, "rr": 32},
        "dtc_code": "None (All Systems Healthy)", "health": "Good",
        "claim_prob": 12.5, "hike_prob": 25.0,
        "maint_rec": "Vehicle in solid operating condition."
    },
    {
        "id": "CAR-06", "vin": "KNA1298347F4567", "reg": "TN-07-CD-3321", "driver": "Ananya Roy", "car": "Kia Seltos GTX+", "year": 2023, "odo": 18400,
        "route": "Chennai (OMR IT Corridor)", "km": 1100, "brakes": 5, "max_decel_g": "-0.50g",
        "brake_events": [{"time": "08-Sep 09:12:30", "speed_drop": "70 → 18 km/h", "g_force": "-0.50g", "location": "Sholinganallur Signal", "cause": "Amber light stop"}],
        "speeding": 3, "max_speed": 92, "speed_limit": 80,
        "speed_events": [{"time": "08-Sep 22:15:00", "speed": "92 km/h (Limit: 80)", "duration": "6 mins", "location": "ECR Link"}],
        "night_hrs": 6, "night_trips": [{"date": "12-Sep", "time_window": "11:20 PM - 01:10 AM", "km": 52, "purpose": "Late shift commute"}],
        "temp_c": 92, "oil_psi": 38, "rpm_max": 3900, "batt_v": 12.4, "brake_pad_mm": 5.4, "tpms": {"fl": 31, "fr": 31, "rl": 30, "rr": 30},
        "dtc_code": "None (Minor TPMS Notification)", "health": "Fair",
        "claim_prob": 16.0, "hike_prob": 35.0,
        "maint_rec": "Routine service due in 1,600 km. TPMS tire balancing advised."
    },
    {
        "id": "CAR-07", "vin": "TAT9988776G1122", "reg": "GJ-01-KP-5678", "driver": "Karan Patel", "car": "Tata Punch Creative", "year": 2023, "odo": 11200,
        "route": "Ahmedabad (SG Highway)", "km": 650, "brakes": 2, "max_decel_g": "-0.38g",
        "brake_events": [{"time": "17-Sep 17:45:10", "speed_drop": "58 → 20 km/h", "g_force": "-0.38g", "location": "Iskcon Crossroad", "cause": "Pedestrian signal"}],
        "speeding": 1, "max_speed": 84, "speed_limit": 80,
        "speed_events": [{"time": "20-Sep 16:30:00", "speed": "84 km/h (Limit: 80)", "duration": "2 mins", "location": "Gota Flyover"}],
        "night_hrs": 2, "night_trips": [{"date": "10-Sep", "time_window": "11:00 PM - 12:05 AM", "km": 24, "purpose": "Local transit"}],
        "temp_c": 87, "oil_psi": 44, "rpm_max": 3100, "batt_v": 12.7, "brake_pad_mm": 8.8, "tpms": {"fl": 33, "fr": 33, "rl": 33, "rr": 33},
        "dtc_code": "None (All Systems Healthy)", "health": "Good",
        "claim_prob": 5.5, "hike_prob": 5.0,
        "maint_rec": "All sensors well within optimal safety tolerances."
    },
    {
        "id": "CAR-08", "vin": "MAR5566778H8899", "reg": "DL-01-ZA-6632", "driver": "Neha Gupta", "car": "Maruti Baleno Alpha", "year": 2021, "odo": 36500,
        "route": "Gurugram (Cyber Hub - NH48)", "km": 1600, "brakes": 9, "max_decel_g": "-0.66g (ABS Active)",
        "brake_events": [
            {"time": "06-Sep 23:55:00", "speed_drop": "90 → 15 km/h", "g_force": "-0.66g (ABS)", "location": "Cyber City Underpass", "cause": "Tailgating sudden stop"},
            {"time": "18-Sep 01:45:10", "speed_drop": "80 → 10 km/h", "g_force": "-0.62g", "location": "Golf Course Road", "cause": "Speed bump late detection"}
        ],
        "speeding": 6, "max_speed": 116, "speed_limit": 80,
        "speed_events": [{"time": "06-Sep 23:40:00", "speed": "116 km/h (Limit: 80)", "duration": "11 mins", "location": "NH48 Highway"}],
        "night_hrs": 14, "night_trips": [{"date": "06-Sep", "time_window": "11:20 PM - 02:40 AM", "km": 98, "purpose": "Night commute"}],
        "temp_c": 100, "oil_psi": 25, "rpm_max": 4900, "batt_v": 12.0, "brake_pad_mm": 3.0, "tpms": {"fl": 29, "fr": 29, "rl": 31, "rr": 30},
        "dtc_code": "P0420 (Catalyst Efficiency), P0562 (Low System Voltage)", "health": "Alert",
        "claim_prob": 42.0, "hike_prob": 92.0,
        "maint_rec": "CRITICAL: Brake pad worn to 3.0mm limit. Catalyst efficiency error and voltage fluctuation detected."
    },
    {
        "id": "CAR-09", "vin": "TOY4433221I3344", "reg": "KA-03-MP-8120", "driver": "Aditya Verma", "car": "Toyota Urban Cruiser Hyryder", "year": 2023, "odo": 15800,
        "route": "Bengaluru (Koramangala - Indiranagar)", "km": 800, "brakes": 3, "max_decel_g": "-0.40g",
        "brake_events": [{"time": "12-Sep 18:20:10", "speed_drop": "52 → 14 km/h", "g_force": "-0.40g", "location": "Sony World Junction", "cause": "Traffic bottleneck"}],
        "speeding": 2, "max_speed": 85, "speed_limit": 80,
        "speed_events": [{"time": "15-Sep 20:45:00", "speed": "85 km/h (Limit: 80)", "duration": "3 mins", "location": "Old Airport Road"}],
        "night_hrs": 4, "night_trips": [{"date": "22-Sep", "time_window": "11:10 PM - 12:30 AM", "km": 30, "purpose": "Weekend transit"}],
        "temp_c": 88, "oil_psi": 46, "rpm_max": 3300, "batt_v": 12.6, "brake_pad_mm": 7.5, "tpms": {"fl": 33, "fr": 33, "rl": 33, "rr": 33},
        "dtc_code": "None (All Systems Healthy)", "health": "Good",
        "claim_prob": 10.5, "hike_prob": 18.0,
        "maint_rec": "Hybrid drive operating efficiently."
    },
    {
        "id": "CAR-10", "vin": "HYU8877665J2233", "reg": "KL-07-CB-9087", "driver": "Divya Menon", "car": "Hyundai Venue SX", "year": 2022, "odo": 24300,
        "route": "Kochi (MG Road - Bypass)", "km": 1250, "brakes": 6, "max_decel_g": "-0.54g",
        "brake_events": [{"time": "09-Sep 19:10:00", "speed_drop": "68 → 15 km/h", "g_force": "-0.54g", "location": "Edappally Toll", "cause": "Queue congestion"}],
        "speeding": 4, "max_speed": 96, "speed_limit": 70,
        "speed_events": [{"time": "14-Sep 22:30:00", "speed": "96 km/h (Limit: 70)", "duration": "8 mins", "location": "NH66 Bypass"}],
        "night_hrs": 8, "night_trips": [{"date": "14-Sep", "time_window": "11:30 PM - 01:50 AM", "km": 68, "purpose": "Late night run"}],
        "temp_c": 94, "oil_psi": 36, "rpm_max": 4100, "batt_v": 12.3, "brake_pad_mm": 4.8, "tpms": {"fl": 31, "fr": 31, "rl": 31, "rr": 31},
        "dtc_code": "None", "health": "Fair",
        "claim_prob": 22.0, "hike_prob": 60.0,
        "maint_rec": "Brake pads at 4.8mm. Safe for city driving, check before highway trip."
    },
    {
        "id": "CAR-11", "vin": "MAH9900112K4455", "reg": "MH-14-TH-4499", "driver": "Siddharth Das", "car": "Mahindra Thar LX 4x4", "year": 2022, "odo": 38100,
        "route": "Pune (Mumbai-Pune Expressway)", "km": 1950, "brakes": 11, "max_decel_g": "-0.74g (ABS Active)",
        "brake_events": [
            {"time": "03-Sep 01:30:15", "speed_drop": "110 → 25 km/h", "g_force": "-0.74g (ABS)", "location": "Bhor Ghat Descent", "cause": "Heavy brake fade avoidance"},
            {"time": "16-Sep 02:50:00", "speed_drop": "98 → 10 km/h", "g_force": "-0.68g", "location": "Khalapur Toll", "cause": "High speed approach"}
        ],
        "speeding": 8, "max_speed": 134, "speed_limit": 80,
        "speed_events": [
            {"time": "03-Sep 01:10:00", "speed": "134 km/h (Limit: 80)", "duration": "24 mins", "location": "Expressway Straight"},
            {"time": "16-Sep 02:20:00", "speed": "122 km/h (Limit: 80)", "duration": "16 mins", "location": "Lonavala Section"}
        ],
        "night_hrs": 16, "night_trips": [{"date": "03-Sep", "time_window": "12:00 AM - 04:00 AM", "km": 180, "purpose": "Expressway run"}],
        "temp_c": 106, "oil_psi": 18, "rpm_max": 5600, "batt_v": 11.7, "brake_pad_mm": 2.0, "tpms": {"fl": 28, "fr": 27, "rl": 30, "rr": 29},
        "dtc_code": "P0217 (Engine Overheat), P0562 (Low Voltage), P0571 (Brake Switch)", "health": "Alert",
        "claim_prob": 48.0, "hike_prob": 98.0,
        "maint_rec": "SEVERE RISK: Extreme brake wear (2.0mm), low oil pressure (18 PSI), and engine overheating (106°C). Immediate workshop visit required."
    },
    {
        "id": "CAR-12", "vin": "SKO3344556L7788", "reg": "TS-09-FA-8812", "driver": "Pooja Reddy", "car": "Skoda Kushaq Style 1.5", "year": 2024, "odo": 7400,
        "route": "Hyderabad (Gachibowli - Hitec City)", "km": 600, "brakes": 1, "max_decel_g": "-0.34g",
        "brake_events": [{"time": "21-Sep 11:20:00", "speed_drop": "50 → 12 km/h", "g_force": "-0.34g", "location": "Financial District", "cause": "Pedestrian crossing"}],
        "speeding": 1, "max_speed": 76, "speed_limit": 70,
        "speed_events": [{"time": "21-Sep 15:40:00", "speed": "76 km/h (Limit: 70)", "duration": "2 mins", "location": "Cable Bridge"}],
        "night_hrs": 2, "night_trips": [{"date": "18-Sep", "time_window": "11:00 PM - 12:10 AM", "km": 25, "purpose": "Late return"}],
        "temp_c": 86, "oil_psi": 48, "rpm_max": 3000, "batt_v": 12.8, "brake_pad_mm": 9.5, "tpms": {"fl": 33, "fr": 33, "rl": 33, "rr": 33},
        "dtc_code": "None (All Systems Healthy)", "health": "Good",
        "claim_prob": 4.5, "hike_prob": 3.0,
        "maint_rec": "Factory optimal telemetry."
    },
    {
        "id": "CAR-13", "vin": "WVW2233445M9900", "reg": "MH-01-DE-7711", "driver": "Rahul Deshmukh", "car": "Volkswagen Taigun GT", "year": 2022, "odo": 26800,
        "route": "Mumbai (Eastern Freeway)", "km": 1050, "brakes": 5, "max_decel_g": "-0.56g",
        "brake_events": [{"time": "13-Sep 22:40:15", "speed_drop": "82 → 20 km/h", "g_force": "-0.56g", "location": "Chembur Freeway Exit", "cause": "Late lane exit"}],
        "speeding": 3, "max_speed": 95, "speed_limit": 80,
        "speed_events": [{"time": "13-Sep 22:20:00", "speed": "95 km/h (Limit: 80)", "duration": "7 mins", "location": "Freeway Southbound"}],
        "night_hrs": 7, "night_trips": [{"date": "13-Sep", "time_window": "11:15 PM - 01:20 AM", "km": 60, "purpose": "Late transit"}],
        "temp_c": 91, "oil_psi": 40, "rpm_max": 3800, "batt_v": 12.4, "brake_pad_mm": 5.8, "tpms": {"fl": 32, "fr": 32, "rl": 32, "rr": 32},
        "dtc_code": "None (All Systems Healthy)", "health": "Good",
        "claim_prob": 18.0, "hike_prob": 45.0,
        "maint_rec": "Vehicle health normal. Scheduled service in 3,200 km."
    },
    {
        "id": "CAR-14", "vin": "TAT7766554N1133", "reg": "UP-16-BX-9944", "driver": "Tanvi Joshi", "car": "Tata Harrier Fearless", "year": 2023, "odo": 33400,
        "route": "Noida (Yamuna Expressway)", "km": 1700, "brakes": 9, "max_decel_g": "-0.70g (ABS Active)",
        "brake_events": [{"time": "05-Sep 02:15:30", "speed_drop": "115 → 25 km/h", "g_force": "-0.70g (ABS)", "location": "Jewar Toll Stretch", "cause": "Fog obstacle avoidance"}],
        "speeding": 7, "max_speed": 130, "speed_limit": 100,
        "speed_events": [{"time": "05-Sep 01:50:00", "speed": "130 km/h (Limit: 100)", "duration": "19 mins", "location": "Yamuna Expressway"}],
        "night_hrs": 13, "night_trips": [{"date": "05-Sep", "time_window": "12:30 AM - 03:45 AM", "km": 155, "purpose": "Intercity night run"}],
        "temp_c": 103, "oil_psi": 24, "rpm_max": 5000, "batt_v": 12.0, "brake_pad_mm": 2.9, "tpms": {"fl": 29, "fr": 28, "rl": 31, "rr": 30},
        "dtc_code": "P0128 (Coolant Temp Below Regulating), P0562 (Low System Voltage)", "health": "Alert",
        "claim_prob": 43.0, "hike_prob": 90.0,
        "maint_rec": "CRITICAL: Front brake pad replacement required (2.9mm). Engine cooling system inspection advised."
    },
    {
        "id": "CAR-15", "vin": "MAK1122334O5566", "reg": "HR-26-EE-3388", "driver": "Manish Chopra", "car": "Honda Elevate ZX", "year": 2024, "odo": 9200,
        "route": "Gurugram (Golf Course Extension)", "km": 850, "brakes": 3, "max_decel_g": "-0.41g",
        "brake_events": [{"time": "19-Sep 17:30:00", "speed_drop": "58 → 15 km/h", "g_force": "-0.41g", "location": "Sector 56 Circle", "cause": "Lane merge"}],
        "speeding": 1, "max_speed": 82, "speed_limit": 70,
        "speed_events": [{"time": "19-Sep 21:10:00", "speed": "82 km/h (Limit: 70)", "duration": "3 mins", "location": "Extension Road"}],
        "night_hrs": 4, "night_trips": [{"date": "23-Sep", "time_window": "11:15 PM - 12:40 AM", "km": 36, "purpose": "Late return"}],
        "temp_c": 88, "oil_psi": 44, "rpm_max": 3200, "batt_v": 12.7, "brake_pad_mm": 8.5, "tpms": {"fl": 33, "fr": 33, "rl": 33, "rr": 33},
        "dtc_code": "None (All Systems Healthy)", "health": "Good",
        "claim_prob": 8.0, "hike_prob": 10.0,
        "maint_rec": "Vehicle health optimal."
    }
]

# Simple Calculation Pipeline
PROCESSED_CARS = []
for c in CARS:
    deduction = (c["brakes"] * 3) + (c["speeding"] * 4) + (c["night_hrs"] * 2)
    score = max(20, min(100, 100 - deduction))
    
    if score >= 80:
        cat = "Safe (Low Risk)"
        risk_adj = -3000
    elif score >= 60:
        cat = "Average (Moderate Risk)"
        risk_adj = 0
    else:
        cat = "Risky (High Risk)"
        risk_adj = 3000
        
    maint_fee = 1000 if c["health"] == "Alert" else 0
    dyn_prem = 15000 + risk_adj + maint_fee
    savings = 18000 - dyn_prem
    
    PROCESSED_CARS.append({
        **c,
        "score": score,
        "category": cat,
        "risk_adj": risk_adj,
        "maint_fee": maint_fee,
        "dyn_prem": dyn_prem,
        "flat_prem": 18000,
        "savings": savings
    })

# Export CSV
csv_path = os.path.join(DIR, "detailed_telematics_sensor_data.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Car ID", "VIN", "Registration", "Driver Name", "Car Model", "Odometer (km)", "Primary Route",
        "Monthly KM", "Harsh Brakes", "Max Decel G-Force", "Speeding Events", "Max Speed (km/h)", "Night Driving (Hrs)",
        "Coolant Temp (°C)", "Oil Pressure (PSI)", "Max RPM", "Battery Voltage (V)", "Brake Pad (mm)", "OBD-II Faults", "Car Health",
        "Driving Safety Score", "Risk Tier", "Crash Claim Probability (%)", "Renewal Hike Probability (%)",
        "Base Premium (₹)", "Risk Adjustment (₹)", "Maintenance Fee (₹)", "Dynamic Final Premium (₹)", "Standard Flat Premium (₹)", "Driver Savings (₹)", "Diagnostic Recommendation"
    ])
    for r in PROCESSED_CARS:
        writer.writerow([
            r["id"], r["vin"], r["reg"], r["driver"], r["car"], r["odo"], r["route"],
            r["km"], r["brakes"], r["max_decel_g"], r["speeding"], r["max_speed"], r["night_hrs"],
            r["temp_c"], r["oil_psi"], r["rpm_max"], r["batt_v"], r["brake_pad_mm"], r["dtc_code"], r["health"],
            r["score"], r["category"], f"{r['claim_prob']}%", f"{r['hike_prob']}%",
            15000, r["risk_adj"], r["maint_fee"], r["dyn_prem"], r["flat_prem"], r["savings"], r["maint_rec"]
        ])

print("Detailed CSV with Probability & Engine Sensor Data written.")
