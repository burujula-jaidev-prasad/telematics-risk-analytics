import zipfile
import xml.etree.ElementTree as ET
import os
import csv
import json

# Output directory
DIR = "/Users/jaidevprasad/.gemini/antigravity/scratch/telematics_risk_analytics"
os.makedirs(DIR, exist_ok=True)

# 25 Realistic Vehicle records
DATA = [
    {"id": "CAR-101", "driver": "Aarav Sharma", "model": "Hyundai Creta", "km": 650, "harsh_brake": 2, "speeding": 1, "night_pct": 5, "rapid_accel": 1, "eng_temp": 88, "batt_v": 12.6, "brake_wear": 25, "obd_faults": 0},
    {"id": "CAR-102", "driver": "Priya Nair", "model": "Maruti Brezza", "km": 1200, "harsh_brake": 8, "speeding": 6, "night_pct": 28, "rapid_accel": 5, "eng_temp": 94, "batt_v": 12.1, "brake_wear": 68, "obd_faults": 1},
    {"id": "CAR-103", "driver": "Rohan Mehta", "model": "Tata Nexon", "km": 480, "harsh_brake": 1, "speeding": 0, "night_pct": 2, "rapid_accel": 0, "eng_temp": 86, "batt_v": 12.7, "brake_wear": 18, "obd_faults": 0},
    {"id": "CAR-104", "driver": "Sneha Kulkarni", "model": "Mahindra XUV700", "km": 1850, "harsh_brake": 12, "speeding": 9, "night_pct": 35, "rapid_accel": 8, "eng_temp": 104, "batt_v": 11.9, "brake_wear": 82, "obd_faults": 2},
    {"id": "CAR-105", "driver": "Vikram Singh", "model": "Honda City", "km": 820, "harsh_brake": 4, "speeding": 2, "night_pct": 12, "rapid_accel": 2, "eng_temp": 89, "batt_v": 12.5, "brake_wear": 40, "obd_faults": 0},
    {"id": "CAR-106", "driver": "Ananya Roy", "model": "Kia Seltos", "km": 950, "harsh_brake": 3, "speeding": 2, "night_pct": 10, "rapid_accel": 2, "eng_temp": 90, "batt_v": 12.6, "brake_wear": 35, "obd_faults": 0},
    {"id": "CAR-107", "driver": "Karan Patel", "model": "Tata Punch", "km": 1400, "harsh_brake": 9, "speeding": 7, "night_pct": 22, "rapid_accel": 6, "eng_temp": 96, "batt_v": 12.3, "brake_wear": 60, "obd_faults": 0},
    {"id": "CAR-108", "driver": "Neha Gupta", "model": "Maruti Baleno", "km": 520, "harsh_brake": 1, "speeding": 1, "night_pct": 4, "rapid_accel": 1, "eng_temp": 87, "batt_v": 12.8, "brake_wear": 20, "obd_faults": 0},
    {"id": "CAR-109", "driver": "Aditya Verma", "model": "Toyota Hyryder", "km": 1100, "harsh_brake": 5, "speeding": 4, "night_pct": 15, "rapid_accel": 3, "eng_temp": 91, "batt_v": 12.4, "brake_wear": 45, "obd_faults": 0},
    {"id": "CAR-110", "driver": "Divya Menon", "model": "Hyundai Venue", "km": 780, "harsh_brake": 3, "speeding": 1, "night_pct": 8, "rapid_accel": 1, "eng_temp": 88, "batt_v": 12.5, "brake_wear": 30, "obd_faults": 0},
    {"id": "CAR-111", "driver": "Siddharth Das", "model": "Mahindra Thar", "km": 2100, "harsh_brake": 14, "speeding": 11, "night_pct": 40, "rapid_accel": 9, "eng_temp": 102, "batt_v": 12.0, "brake_wear": 88, "obd_faults": 2},
    {"id": "CAR-112", "driver": "Pooja Reddy", "model": "Skoda Kushaq", "km": 600, "harsh_brake": 2, "speeding": 0, "night_pct": 5, "rapid_accel": 1, "eng_temp": 89, "batt_v": 12.6, "brake_wear": 22, "obd_faults": 0},
    {"id": "CAR-113", "driver": "Rahul Deshmukh", "model": "Volkswagen Taigun", "km": 1300, "harsh_brake": 7, "speeding": 5, "night_pct": 18, "rapid_accel": 4, "eng_temp": 93, "batt_v": 12.3, "brake_wear": 55, "obd_faults": 0},
    {"id": "CAR-114", "driver": "Tanvi Joshi", "model": "Tata Harrier", "km": 1650, "harsh_brake": 10, "speeding": 8, "night_pct": 30, "rapid_accel": 7, "eng_temp": 98, "batt_v": 12.1, "brake_wear": 75, "obd_faults": 1},
    {"id": "CAR-115", "driver": "Manish Chopra", "model": "Honda Elevate", "km": 720, "harsh_brake": 2, "speeding": 1, "night_pct": 6, "rapid_accel": 1, "eng_temp": 88, "batt_v": 12.7, "brake_wear": 28, "obd_faults": 0},
    {"id": "CAR-116", "driver": "Ritu Saxena", "model": "Maruti Swift", "km": 900, "harsh_brake": 4, "speeding": 3, "night_pct": 14, "rapid_accel": 2, "eng_temp": 90, "batt_v": 12.4, "brake_wear": 38, "obd_faults": 0},
    {"id": "CAR-117", "driver": "Varun Iyer", "model": "Hyundai Verna", "km": 1750, "harsh_brake": 11, "speeding": 10, "night_pct": 32, "rapid_accel": 8, "eng_temp": 101, "batt_v": 11.8, "brake_wear": 79, "obd_faults": 1},
    {"id": "CAR-118", "driver": "Kavita Rao", "model": "Kia Sonet", "km": 550, "harsh_brake": 1, "speeding": 1, "night_pct": 3, "rapid_accel": 0, "eng_temp": 87, "batt_v": 12.8, "brake_wear": 15, "obd_faults": 0},
    {"id": "CAR-119", "driver": "Gaurav Bhatt", "model": "MG Hector", "km": 1250, "harsh_brake": 6, "speeding": 4, "night_pct": 16, "rapid_accel": 4, "eng_temp": 92, "batt_v": 12.3, "brake_wear": 50, "obd_faults": 0},
    {"id": "CAR-120", "driver": "Deepa Nambiar", "model": "Toyota Innova", "km": 1900, "harsh_brake": 13, "speeding": 8, "night_pct": 38, "rapid_accel": 7, "eng_temp": 103, "batt_v": 12.0, "brake_wear": 84, "obd_faults": 2},
    {"id": "CAR-121", "driver": "Arjun Sen", "model": "Tata Altroz", "km": 680, "harsh_brake": 2, "speeding": 1, "night_pct": 5, "rapid_accel": 1, "eng_temp": 88, "batt_v": 12.6, "brake_wear": 26, "obd_faults": 0},
    {"id": "CAR-122", "driver": "Meera Kapoor", "model": "Maruti Grand Vitara", "km": 880, "harsh_brake": 3, "speeding": 2, "night_pct": 9, "rapid_accel": 2, "eng_temp": 89, "batt_v": 12.5, "brake_wear": 34, "obd_faults": 0},
    {"id": "CAR-123", "driver": "Kunal Bansal", "model": "Hyundai i20", "km": 1450, "harsh_brake": 8, "speeding": 6, "night_pct": 24, "rapid_accel": 5, "eng_temp": 95, "batt_v": 12.2, "brake_wear": 65, "obd_faults": 0},
    {"id": "CAR-124", "driver": "Swati Tiwari", "model": "Mahindra Scorpio-N", "km": 1800, "harsh_brake": 11, "speeding": 9, "night_pct": 34, "rapid_accel": 7, "eng_temp": 99, "batt_v": 12.1, "brake_wear": 78, "obd_faults": 1},
    {"id": "CAR-125", "driver": "Nikhil Agarwal", "model": "Skoda Slavia", "km": 750, "harsh_brake": 2, "speeding": 1, "night_pct": 7, "rapid_accel": 1, "eng_temp": 88, "batt_v": 12.7, "brake_wear": 30, "obd_faults": 0}
]

def compute_row(r):
    # 1. Driving Safety Score (0-100)
    # 100 - (harsh_brake * 2.5) - (speeding * 3.0) - (night_pct * 0.5) - (rapid_accel * 1.5)
    deduction = (r["harsh_brake"] * 2.5) + (r["speeding"] * 3.0) + (r["night_pct"] * 0.5) + (r["rapid_accel"] * 1.5)
    safety_score = max(10, min(100, round(100 - deduction, 1)))
    
    # Risk Category
    if safety_score >= 80:
        risk_cat = "Low Risk"
        risk_mod = -0.20 # 20% discount
    elif safety_score >= 60:
        risk_cat = "Moderate Risk"
        risk_mod = 0.00 # Standard
    else:
        risk_cat = "High Risk"
        risk_mod = 0.25 # 25% surcharge
        
    # 2. Vehicle Health Score (0-100)
    v_health = 100
    if r["batt_v"] < 12.2:
        v_health -= 25
    elif r["batt_v"] < 12.4:
        v_health -= 10
        
    if r["eng_temp"] > 100:
        v_health -= 30
    elif r["eng_temp"] > 95:
        v_health -= 15
        
    if r["brake_wear"] >= 75:
        v_health -= 30
    elif r["brake_wear"] >= 50:
        v_health -= 15
        
    v_health -= (r["obd_faults"] * 15)
    v_health = max(15, min(100, v_health))
    
    if v_health >= 80:
        maint_status = "Good Condition"
        maint_buffer = 0
    elif v_health >= 60:
        maint_status = "Inspection Due"
        maint_buffer = 500
    else:
        maint_status = "Critical Maintenance"
        maint_buffer = 1500
        
    # 3. Dynamic Premium Calculation
    # Base: ₹15,000
    base_prem = 15000
    # Pay As You Drive Distance Factor: (km / 1000) * ₹2,000
    distance_fee = round((r["km"] / 1000) * 2000, 0)
    # Behavior Adjustment on Base
    behavior_adj = round(base_prem * risk_mod, 0)
    # Final Dynamic Premium
    dynamic_prem = round(base_prem + distance_fee + behavior_adj + maint_buffer, 0)
    # Traditional Flat Premium (Standard industry benchmark: ₹22,000)
    flat_prem = 22000
    savings = round(flat_prem - dynamic_prem, 0)
    
    return {
        **r,
        "safety_score": safety_score,
        "risk_cat": risk_cat,
        "v_health": v_health,
        "maint_status": maint_status,
        "distance_fee": distance_fee,
        "behavior_adj": behavior_adj,
        "maint_buffer": maint_buffer,
        "dynamic_prem": dynamic_prem,
        "flat_prem": flat_prem,
        "savings": savings
    }

PROCESSED_DATA = [compute_row(r) for r in DATA]

# 1. Save as CSV
csv_path = os.path.join(DIR, "telematics_insurance_data.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Vehicle ID", "Driver Name", "Car Model", "Monthly KM",
        "Harsh Braking /100km", "Speeding Instances /100km", "Late Night Driving %", "Rapid Accel Events",
        "Engine Temp (°C)", "Battery Voltage (V)", "Brake Wear %", "OBD Faults",
        "Driving Safety Score", "Risk Category", "Vehicle Health Score", "Maintenance Status",
        "Base Premium (₹)", "Distance Fee (₹)", "Driving Risk Adj (₹)", "Maint Buffer (₹)",
        "Dynamic Premium (₹)", "Traditional Flat Premium (₹)", "Driver Savings (₹)"
    ])
    for r in PROCESSED_DATA:
        writer.writerow([
            r["id"], r["driver"], r["model"], r["km"],
            r["harsh_brake"], r["speeding"], f"{r['night_pct']}%", r["rapid_accel"],
            r["eng_temp"], r["batt_v"], f"{r['brake_wear']}%", r["obd_faults"],
            r["safety_score"], r["risk_cat"], r["v_health"], r["maint_status"],
            15000, r["distance_fee"], r["behavior_adj"], r["maint_buffer"],
            r["dynamic_prem"], r["flat_prem"], r["savings"]
        ])

print("CSV generated successfully:", csv_path)
