import os
import csv
import json
import zipfile
import html

DIR = "/Users/jaidevprasad/.gemini/antigravity/scratch/telematics_risk_analytics"
os.makedirs(DIR, exist_ok=True)

# 15 Simple, Clean, Realistic records
DRIVERS = [
    {"id": "CAR-01", "name": "Aarav Sharma", "car": "Hyundai Creta", "km": 750, "brakes": 2, "speeding": 1, "night_hrs": 3, "health": "Good"},
    {"id": "CAR-02", "name": "Priya Nair", "car": "Maruti Brezza", "km": 1400, "brakes": 8, "speeding": 5, "night_hrs": 12, "health": "Alert"},
    {"id": "CAR-03", "name": "Rohan Mehta", "car": "Tata Nexon", "km": 500, "brakes": 1, "speeding": 0, "night_hrs": 2, "health": "Good"},
    {"id": "CAR-04", "name": "Sneha Kulkarni", "car": "Mahindra XUV700", "km": 1800, "brakes": 10, "speeding": 7, "night_hrs": 15, "health": "Alert"},
    {"id": "CAR-05", "name": "Vikram Singh", "car": "Honda City", "km": 900, "brakes": 4, "speeding": 2, "night_hrs": 5, "health": "Good"},
    {"id": "CAR-06", "name": "Ananya Roy", "car": "Kia Seltos", "km": 1100, "brakes": 5, "speeding": 3, "night_hrs": 6, "health": "Fair"},
    {"id": "CAR-07", "name": "Karan Patel", "car": "Tata Punch", "km": 650, "brakes": 2, "speeding": 1, "night_hrs": 2, "health": "Good"},
    {"id": "CAR-08", "name": "Neha Gupta", "car": "Maruti Baleno", "km": 1600, "brakes": 9, "speeding": 6, "night_hrs": 14, "health": "Alert"},
    {"id": "CAR-09", "name": "Aditya Verma", "car": "Toyota Hyryder", "km": 800, "brakes": 3, "speeding": 2, "night_hrs": 4, "health": "Good"},
    {"id": "CAR-10", "name": "Divya Menon", "car": "Hyundai Venue", "km": 1250, "brakes": 6, "speeding": 4, "night_hrs": 8, "health": "Fair"},
    {"id": "CAR-11", "name": "Siddharth Das", "car": "Mahindra Thar", "km": 1950, "brakes": 11, "speeding": 8, "night_hrs": 16, "health": "Alert"},
    {"id": "CAR-12", "name": "Pooja Reddy", "car": "Skoda Kushaq", "km": 600, "brakes": 1, "speeding": 1, "night_hrs": 2, "health": "Good"},
    {"id": "CAR-13", "name": "Rahul Deshmukh", "car": "Volkswagen Taigun", "km": 1050, "brakes": 5, "speeding": 3, "night_hrs": 7, "health": "Good"},
    {"id": "CAR-14", "name": "Tanvi Joshi", "car": "Tata Harrier", "km": 1700, "brakes": 9, "speeding": 7, "night_hrs": 13, "health": "Alert"},
    {"id": "CAR-15", "name": "Manish Chopra", "car": "Honda Elevate", "km": 850, "brakes": 3, "speeding": 1, "night_hrs": 4, "health": "Good"}
]

# Simple Calculations
# Base Premium = 15000
# Score = 100 - (brakes * 3) - (speeding * 4) - (night_hrs * 2)
# Category: >= 80 Safe (-3000 discount), 60-79 Average (0), < 60 Risky (+3000 penalty)
# Maintenance Fee: Alert (+1000), Good/Fair (0)
# Dynamic Premium = 15000 + Risk_Adj + Maint_Fee
# Standard Flat Premium = 18000
# Savings = 18000 - Dynamic Premium

PROCESSED = []
for d in DRIVERS:
    deduction = (d["brakes"] * 3) + (d["speeding"] * 4) + (d["night_hrs"] * 2)
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
        
    maint_fee = 1000 if d["health"] == "Alert" else 0
    dyn_prem = 15000 + risk_adj + maint_fee
    savings = 18000 - dyn_prem
    
    PROCESSED.append({
        **d,
        "score": score,
        "category": cat,
        "risk_adj": risk_adj,
        "maint_fee": maint_fee,
        "dyn_prem": dyn_prem,
        "flat_prem": 18000,
        "savings": savings
    })

# Fleet Averages
avg_km = round(sum(d["km"] for d in PROCESSED) / len(PROCESSED), 1)
avg_brakes = round(sum(d["brakes"] for d in PROCESSED) / len(PROCESSED), 1)
avg_speeding = round(sum(d["speeding"] for d in PROCESSED) / len(PROCESSED), 1)
avg_night = round(sum(d["night_hrs"] for d in PROCESSED) / len(PROCESSED), 1)
avg_score = round(sum(d["score"] for d in PROCESSED) / len(PROCESSED), 1)
avg_prem = round(sum(d["dyn_prem"] for d in PROCESSED) / len(PROCESSED), 0)
safe_count = sum(1 for d in PROCESSED if d["category"].startswith("Safe"))
risky_count = sum(1 for d in PROCESSED if d["category"].startswith("Risky"))
avg_count = len(PROCESSED) - safe_count - risky_count
alert_count = sum(1 for d in PROCESSED if d["health"] == "Alert")

print(f"Fleet Summary: Avg Score = {avg_score}, Avg Brakes = {avg_brakes}, Avg Speeding = {avg_speeding}, Avg Premium = ₹{avg_prem}")

# 1. Export Simple CSV
csv_path = os.path.join(DIR, "simple_telematics_data.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Car ID", "Driver Name", "Car Model", "Monthly KM",
        "Harsh Braking Count", "Speeding Incidents", "Late Night Driving (Hrs)",
        "Engine Health", "Driving Safety Score", "Risk Category",
        "Base Premium (₹)", "Risk Adjustment (₹)", "Maintenance Fee (₹)",
        "Dynamic Final Premium (₹)", "Standard Flat Premium (₹)", "Driver Savings (₹)"
    ])
    for r in PROCESSED:
        writer.writerow([
            r["id"], r["name"], r["car"], r["km"],
            r["brakes"], r["speeding"], r["night_hrs"],
            r["health"], r["score"], r["category"],
            15000, r["risk_adj"], r["maint_fee"],
            r["dyn_prem"], r["flat_prem"], r["savings"]
        ])

# 2. Build Super Clean Excel File
def build_simple_xlsx(filepath):
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
    <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
    <Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedString+xml"/>
</Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

    wb_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
    <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
    <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
</Relationships>"""

    workbook = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
    <sheets>
        <sheet name="Car Sensor &amp; Premium Data" sheetId="1" r:id="rId1"/>
        <sheet name="Simple Pricing Rules" sheetId="2" r:id="rId2"/>
    </sheets>
</workbook>"""

    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <fonts count="5">
        <font><name val="Calibri"/><sz val="11"/></font>
        <font><b/><name val="Calibri"/><sz val="11"/><color rgb="FFFFFFFF"/></font>
        <font><b/><name val="Calibri"/><sz val="11"/><color rgb="FF1E3A8A"/></font>
        <font><b/><name val="Calibri"/><sz val="12"/><color rgb="FF0F172A"/></font>
        <font><b/><name val="Calibri"/><sz val="11"/><color rgb="FF15803D"/></font>
    </fonts>
    <fills count="6">
        <fill><patternFill patternType="none"/></fill>
        <fill><patternFill patternType="gray125"/></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FF2563EB"/></fgColor></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FFF1F5F9"/></fgColor></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FFDCFCE7"/></fgColor></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FF0284C7"/></fgColor></patternFill></fill>
    </fills>
    <borders count="2">
        <border><left/><right/><top/><bottom/></border>
        <border>
            <left style="thin"><color rgb="FFCBD5E1"/></left>
            <right style="thin"><color rgb="FFCBD5E1"/></right>
            <top style="thin"><color rgb="FFCBD5E1"/></top>
            <bottom style="thin"><color rgb="FFCBD5E1"/></bottom>
        </border>
    </borders>
    <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
    <cellXfs count="6">
        <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0"/>
        <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
        <xf numFmtId="0" fontId="2" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"/>
        <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
        <xf numFmtId="0" fontId="4" fillId="4" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
        <xf numFmtId="0" fontId="1" fillId="5" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    </cellXfs>
</styleSheet>"""

    strings = []
    string_map = {}

    def get_str_id(s):
        s_clean = str(s)
        if s_clean not in string_map:
            string_map[s_clean] = len(strings)
            strings.append(s_clean)
        return string_map[s_clean]

    def col_letter(n):
        res = ""
        while n > 0:
            n, rem = divmod(n - 1, 26)
            res = chr(65 + rem) + res
        return res

    # Build Sheet 1 Data
    s1_rows = []
    headers = [
        "Car ID", "Driver Name", "Car Model", "Monthly KM",
        "Harsh Braking", "Speeding Events", "Night Driving (Hrs)", "Car Health",
        "Driving Safety Score", "Risk Category",
        "Base Premium (₹)", "Risk Adjustment (₹)", "Maintenance Fee (₹)",
        "Dynamic Final Premium (₹)", "Standard Flat Premium (₹)", "Driver Savings (₹)"
    ]

    # Header Row
    h_cells = ['<row r="1" ht="26">']
    for idx, h in enumerate(headers, start=1):
        h_cells.append(f'<c r="{col_letter(idx)}1" t="s" s="1"><v>{get_str_id(h)}</v></c>')
    h_cells.append('</row>')
    s1_rows.append("".join(h_cells))

    # Data Rows (2 to 16)
    for r_idx, r in enumerate(PROCESSED, start=2):
        row_cells = [f'<row r="{r_idx}">']
        row_cells.append(f'<c r="A{r_idx}" t="s" s="3"><v>{get_str_id(r["id"])}</v></c>')
        row_cells.append(f'<c r="B{r_idx}" t="s" s="0"><v>{get_str_id(r["name"])}</v></c>')
        row_cells.append(f'<c r="C{r_idx}" t="s" s="0"><v>{get_str_id(r["car"])}</v></c>')
        row_cells.append(f'<c r="D{r_idx}" s="3"><v>{r["km"]}</v></c>')
        row_cells.append(f'<c r="E{r_idx}" s="3"><v>{r["brakes"]}</v></c>')
        row_cells.append(f'<c r="F{r_idx}" s="3"><v>{r["speeding"]}</v></c>')
        row_cells.append(f'<c r="G{r_idx}" s="3"><v>{r["night_hrs"]}</v></c>')
        row_cells.append(f'<c r="H{r_idx}" t="s" s="3"><v>{get_str_id(r["health"])}</v></c>')
        # Score Formula: =100 - (E2*3) - (F2*4) - (G2*2)
        row_cells.append(f'<c r="I{r_idx}" s="3"><f>100 - (E{r_idx}*3) - (F{r_idx}*4) - (G{r_idx}*2)</f><v>{r["score"]}</v></c>')
        # Category: =IF(I2>=80, "Safe (Low Risk)", IF(I2>=60, "Average (Moderate Risk)", "Risky (High Risk)"))
        row_cells.append(f'<c r="J{r_idx}" t="s" s="3"><v>{get_str_id(r["category"])}</v></c>')
        # Base Premium
        row_cells.append(f'<c r="K{r_idx}" s="0"><v>15000</v></c>')
        # Risk Adjustment: =IF(I2>=80, -3000, IF(I2>=60, 0, 3000))
        row_cells.append(f'<c r="L{r_idx}" s="0"><f>IF(I{r_idx}&gt;=80, -3000, IF(I{r_idx}&gt;=60, 0, 3000))</f><v>{r["risk_adj"]}</v></c>')
        # Maint Fee: =IF(H2="Alert", 1000, 0)
        row_cells.append(f'<c r="M{r_idx}" s="0"><f>IF(H{r_idx}="Alert", 1000, 0)</f><v>{r["maint_fee"]}</v></c>')
        # Dynamic Premium: =K2+L2+M2
        row_cells.append(f'<c r="N{r_idx}" s="0"><f>K{r_idx}+L{r_idx}+M{r_idx}</f><v>{r["dyn_prem"]}</v></c>')
        # Flat Premium
        row_cells.append(f'<c r="O{r_idx}" s="0"><v>18000</v></c>')
        # Savings: =O2-N2
        row_cells.append(f'<c r="P{r_idx}" s="0"><f>O{r_idx}-N{r_idx}</f><v>{r["savings"]}</v></c>')
        
        row_cells.append('</row>')
        s1_rows.append("".join(row_cells))

    # Summary Row 17 (Fleet Averages)
    avg_row = ['<row r="18" ht="24">']
    avg_row.append(f'<c r="A18" t="s" s="2"><v>{get_str_id("FLEET AVERAGE")}</v></c>')
    avg_row.append(f'<c r="B18" s="2"/>')
    avg_row.append(f'<c r="C18" s="2"/>')
    avg_row.append(f'<c r="D18" s="2"><f>ROUND(AVERAGE(D2:D16), 1)</f><v>{avg_km}</v></c>')
    avg_row.append(f'<c r="E18" s="2"><f>ROUND(AVERAGE(E2:E16), 1)</f><v>{avg_brakes}</v></c>')
    avg_row.append(f'<c r="F18" s="2"><f>ROUND(AVERAGE(F2:F16), 1)</f><v>{avg_speeding}</v></c>')
    avg_row.append(f'<c r="G18" s="2"><f>ROUND(AVERAGE(G2:G16), 1)</f><v>{avg_night}</v></c>')
    avg_row.append(f'<c r="H18" s="2"/>')
    avg_row.append(f'<c r="I18" s="2"><f>ROUND(AVERAGE(I2:I16), 1)</f><v>{avg_score}</v></c>')
    avg_row.append(f'<c r="J18" s="2"/>')
    avg_row.append(f'<c r="K18" s="2"><v>15000</v></c>')
    avg_row.append(f'<c r="L18" s="2"/>')
    avg_row.append(f'<c r="M18" s="2"/>')
    avg_row.append(f'<c r="N18" s="2"><f>ROUND(AVERAGE(N2:N16), 0)</f><v>{avg_prem}</v></c>')
    avg_row.append(f'<c r="O18" s="2"><v>18000</v></c>')
    avg_row.append(f'<c r="P18" s="2"><f>SUM(P2:P16)</f><v>{sum(d["savings"] for d in PROCESSED)}</v></c>')
    avg_row.append('</row>')
    s1_rows.append("".join(avg_row))

    sheet1_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sheetFormatPr defaultRowHeight="20"/>
    <cols>
        <col min="1" max="1" width="12" customWidth="1"/>
        <col min="2" max="2" width="18" customWidth="1"/>
        <col min="3" max="3" width="20" customWidth="1"/>
        <col min="4" max="4" width="14" customWidth="1"/>
        <col min="5" max="7" width="16" customWidth="1"/>
        <col min="8" max="8" width="14" customWidth="1"/>
        <col min="9" max="9" width="18" customWidth="1"/>
        <col min="10" max="10" width="22" customWidth="1"/>
        <col min="11" max="16" width="18" customWidth="1"/>
    </cols>
    <sheetData>
        {"".join(s1_rows)}
    </sheetData>
</worksheet>"""

    # Sheet 2: Logic
    s2_rows = [
        '<row r="1" ht="24"><c r="A1" t="s" s="5"><v>' + str(get_str_id("Rule / Parameter")) + '</v></c><c r="B1" t="s" s="5"><v>' + str(get_str_id("Simple Formula / Condition")) + '</v></c><c r="C1" t="s" s="5"><v>' + str(get_str_id("Price Impact")) + '</v></c></row>',
        '<row r="2"><c r="A2" t="s" s="0"><v>' + str(get_str_id("1. Driving Safety Score")) + '</v></c><c r="B2" t="s" s="0"><v>' + str(get_str_id("100 - (Braking*3) - (Speeding*4) - (Night_Hours*2)")) + '</v></c><c r="C2" t="s" s="0"><v>' + str(get_str_id("Scores from 0 to 100")) + '</v></c></row>',
        '<row r="3"><c r="A3" t="s" s="0"><v>' + str(get_str_id("2. Safe Driver (Score >= 80)")) + '</v></c><c r="B3" t="s" s="0"><v>' + str(get_str_id("Score >= 80")) + '</v></c><c r="C3" t="s" s="0"><v>' + str(get_str_id("-₹3,000 Discount")) + '</v></c></row>',
        '<row r="4"><c r="A4" t="s" s="0"><v>' + str(get_str_id("3. Average Driver (Score 60-79)")) + '</v></c><c r="B4" t="s" s="0"><v>' + str(get_str_id("Score 60 to 79")) + '</v></c><c r="C4" t="s" s="0"><v>' + str(get_str_id("₹0 (Standard Base)")) + '</v></c></row>',
        '<row r="5"><c r="A5" t="s" s="0"><v>' + str(get_str_id("4. Risky Driver (Score < 60)")) + '</v></c><c r="B5" t="s" s="0"><v>' + str(get_str_id("Score < 60")) + '</v></c><c r="C5" t="s" s="0"><v>' + str(get_str_id("+₹3,000 Penalty")) + '</v></c></row>',
        '<row r="6"><c r="A6" t="s" s="0"><v>' + str(get_str_id("5. Car Health Alert")) + '</v></c><c r="B6" t="s" s="0"><v>' + str(get_str_id("Engine/Sensor Status = Alert")) + '</v></c><c r="C6" t="s" s="0"><v>' + str(get_str_id("+₹1,000 Maintenance Fee")) + '</v></c></row>',
        '<row r="7"><c r="A7" t="s" s="0"><v>' + str(get_str_id("6. Final Dynamic Premium")) + '</v></c><c r="B7" t="s" s="0"><v>' + str(get_str_id("Base Premium (₹15,000) + Risk Adj + Maintenance Fee")) + '</v></c><c r="C7" t="s" s="0"><v>' + str(get_str_id("Final customized price")) + '</v></c></row>',
        '<row r="8"><c r="A8" t="s" s="0"><v>' + str(get_str_id("7. Driver Savings")) + '</v></c><c r="B8" t="s" s="0"><v>' + str(get_str_id("Standard Flat Premium (₹18,000) - Dynamic Premium")) + '</v></c><c r="C8" t="s" s="0"><v>' + str(get_str_id("Shows savings for good driving")) + '</v></c></row>'
    ]

    sheet2_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sheetFormatPr defaultRowHeight="22"/>
    <cols>
        <col min="1" max="1" width="30" customWidth="1"/>
        <col min="2" max="2" width="45" customWidth="1"/>
        <col min="3" max="3" width="28" customWidth="1"/>
    </cols>
    <sheetData>
        {"".join(s2_rows)}
    </sheetData>
</worksheet>"""

    sst_items = "".join([f"<si><t>{html.escape(s)}</t></si>" for s in strings])
    sst_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{len(strings)}" uniqueCount="{len(strings)}">
    {sst_items}
</sst>"""

    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('xl/_rels/workbook.xml.rels', wb_rels)
        zf.writestr('xl/workbook.xml', workbook)
        zf.writestr('xl/styles.xml', styles)
        zf.writestr('xl/sharedStrings.xml', sst_xml)
        zf.writestr('xl/worksheets/sheet1.xml', sheet1_xml)
        zf.writestr('xl/worksheets/sheet2.xml', sheet2_xml)

    print("Simple Excel file created:", filepath)

excel_path = os.path.join(DIR, "Simple_Car_Sensor_Insurance_Analysis.xlsx")
build_simple_xlsx(excel_path)
