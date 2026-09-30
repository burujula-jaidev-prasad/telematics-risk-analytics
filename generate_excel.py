import os
import zipfile
import xml.etree.ElementTree as ET

# Pure Python XLSX Generator
def create_telematics_excel(output_file, rows_data):
    # Prepare XML strings
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
    <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
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
    <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>
    <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
    <Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
</Relationships>"""

    workbook = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
    <sheets>
        <sheet name="Fleet Telematics &amp; Risk" sheetId="1" r:id="rId1"/>
        <sheet name="Scoring &amp; Pricing Logic" sheetId="2" r:id="rId2"/>
        <sheet name="Executive Summary" sheetId="3" r:id="rId3"/>
    </sheets>
</workbook>"""

    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <fonts count="4">
        <font><name val="Calibri"/><sz val="11"/></font>
        <font><b/><name val="Calibri"/><sz val="11"/><color rgb="FFFFFFFF"/></font>
        <font><b/><name val="Calibri"/><sz val="12"/><color rgb="FF1E293B"/></font>
        <font><b/><name val="Calibri"/><sz val="14"/><color rgb="FF0F172A"/></font>
    </fonts>
    <fills count="5">
        <fill><patternFill patternType="none"/></fill>
        <fill><patternFill patternType="gray125"/></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FF1E3A8A"/></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FF0D9488"/></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FFF1F5F9"/></patternFill></fill>
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
        <xf numFmtId="0" fontId="1" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
        <xf numFmtId="0" fontId="2" fillId="4" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"/>
        <xf numFmtId="0" fontId="3" fillId="0" borderId="0" xfId="0" applyFont="1"/>
        <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    </cellXfs>
</styleSheet>"""

    # Shared strings management
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

    # Build Sheet 1: Fleet Telematics & Risk
    s1_rows = []
    headers_s1 = [
        "Vehicle ID", "Driver Name", "Car Model", "Monthly KM",
        "Harsh Braking /100km", "Speeding Incidents", "Late Night % (11pm-4am)", "Rapid Accel Events",
        "Engine Temp (°C)", "Battery Voltage (V)", "Brake Wear %", "OBD Faults",
        "Driving Safety Score", "Risk Category", "Vehicle Health Score", "Maintenance Status",
        "Base Premium (₹)", "Distance Surcharge (₹)", "Risk Adjustment (₹)", "Maintenance Buffer (₹)",
        "Dynamic Final Premium (₹)", "Flat Benchmark Premium (₹)", "Annual Driver Savings (₹)"
    ]

    # Header Row
    s1_row_xml = ['<row r="1" ht="28" customHeight="1">']
    for col_idx, h in enumerate(headers_s1, start=1):
        sid = get_str_id(h)
        s1_row_xml.append(f'<c r="{col_letter(col_idx)}1" t="s" s="1"><v>{sid}</v></c>')
    s1_row_xml.append('</row>')
    s1_rows.append("".join(s1_row_xml))

    # Data Rows (2 to 26)
    for r_idx, r in enumerate(rows_data, start=2):
        row_cells = [f'<row r="{r_idx}">']
        
        # Vehicle ID (s)
        row_cells.append(f'<c r="A{r_idx}" t="s" s="5"><v>{get_str_id(r["id"])}</v></c>')
        # Driver Name (s)
        row_cells.append(f'<c r="B{r_idx}" t="s" s="0"><v>{get_str_id(r["driver"])}</v></c>')
        # Model (s)
        row_cells.append(f'<c r="C{r_idx}" t="s" s="0"><v>{get_str_id(r["model"])}</v></c>')
        # Monthly KM (n)
        row_cells.append(f'<c r="D{r_idx}" s="0"><v>{r["km"]}</v></c>')
        # Harsh Braking (n)
        row_cells.append(f'<c r="E{r_idx}" s="5"><v>{r["harsh_brake"]}</v></c>')
        # Speeding (n)
        row_cells.append(f'<c r="F{r_idx}" s="5"><v>{r["speeding"]}</v></c>')
        # Night % (n)
        row_cells.append(f'<c r="G{r_idx}" s="5"><v>{r["night_pct"]}</v></c>')
        # Rapid Accel (n)
        row_cells.append(f'<c r="H{r_idx}" s="5"><v>{r["rapid_accel"]}</v></c>')
        # Eng Temp (n)
        row_cells.append(f'<c r="I{r_idx}" s="5"><v>{r["eng_temp"]}</v></c>')
        # Battery V (n)
        row_cells.append(f'<c r="J{r_idx}" s="5"><v>{r["batt_v"]}</v></c>')
        # Brake Wear (n)
        row_cells.append(f'<c r="K{r_idx}" s="5"><v>{r["brake_wear"]}</v></c>')
        # OBD Faults (n)
        row_cells.append(f'<c r="L{r_idx}" s="5"><v>{r["obd_faults"]}</v></c>')
        # Safety Score (Formula / Number)
        row_cells.append(f'<c r="M{r_idx}" s="5"><f>MAX(10, MIN(100, ROUND(100 - (E{r_idx}*2.5) - (F{r_idx}*3) - (G{r_idx}*0.5) - (H{r_idx}*1.5), 1)))</f><v>{r["safety_score"]}</v></c>')
        # Risk Category (s)
        row_cells.append(f'<c r="N{r_idx}" t="s" s="5"><v>{get_str_id(r["risk_cat"])}</v></c>')
        # Vehicle Health (n)
        row_cells.append(f'<c r="O{r_idx}" s="5"><v>{r["v_health"]}</v></c>')
        # Maintenance Status (s)
        row_cells.append(f'<c r="P{r_idx}" t="s" s="5"><v>{get_str_id(r["maint_status"])}</v></c>')
        # Base Premium (n)
        row_cells.append(f'<c r="Q{r_idx}" s="0"><v>15000</v></c>')
        # Distance Fee (Formula)
        row_cells.append(f'<c r="R{r_idx}" s="0"><f>ROUND((D{r_idx}/1000)*2000, 0)</f><v>{r["distance_fee"]}</v></c>')
        # Risk Adjustment (Formula)
        row_cells.append(f'<c r="S{r_idx}" s="0"><f>IF(M{r_idx}>=80, -3000, IF(M{r_idx}>=60, 0, 3750))</f><v>{r["behavior_adj"]}</v></c>')
        # Maintenance Buffer (Formula)
        row_cells.append(f'<c r="T{r_idx}" s="0"><f>IF(O{r_idx}&gt;=80, 0, IF(O{r_idx}&gt;=60, 500, 1500))</f><v>{r["maint_buffer"]}</v></c>')
        # Final Dynamic Premium (Formula)
        row_cells.append(f'<c r="U{r_idx}" s="0"><f>Q{r_idx}+R{r_idx}+S{r_idx}+T{r_idx}</f><v>{r["dynamic_prem"]}</v></c>')
        # Flat Premium (n)
        row_cells.append(f'<c r="V{r_idx}" s="0"><v>22000</v></c>')
        # Savings (Formula)
        row_cells.append(f'<c r="W{r_idx}" s="0"><f>V{r_idx}-U{r_idx}</f><v>{r["savings"]}</v></c>')
        
        row_cells.append('</row>')
        s1_rows.append("".join(row_cells))

    sheet1_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sheetViews><sheetView tabSelected="1" workbookViewId="0"/></sheetViews>
    <sheetFormatPr defaultRowHeight="20"/>
    <cols>
        <col min="1" max="1" width="14" customWidth="1"/>
        <col min="2" max="2" width="18" customWidth="1"/>
        <col min="3" max="3" width="22" customWidth="1"/>
        <col min="4" max="4" width="14" customWidth="1"/>
        <col min="5" max="8" width="16" customWidth="1"/>
        <col min="9" max="12" width="16" customWidth="1"/>
        <col min="13" max="13" width="18" customWidth="1"/>
        <col min="14" max="14" width="18" customWidth="1"/>
        <col min="15" max="15" width="18" customWidth="1"/>
        <col min="16" max="16" width="22" customWidth="1"/>
        <col min="17" max="23" width="20" customWidth="1"/>
    </cols>
    <sheetData>
        {"".join(s1_rows)}
    </sheetData>
</worksheet>"""

    # Build Sheet 2: Scoring & Pricing Logic
    s2_rows = [
        '<row r="1" ht="26"><c r="A1" t="s" s="2"><v>' + str(get_str_id("Category / Parameter")) + '</v></c><c r="B1" t="s" s="2"><v>' + str(get_str_id("Sensor / Telematics Input")) + '</v></c><c r="C1" t="s" s="2"><v>' + str(get_str_id("Weight / Deduction Formula")) + '</v></c><c r="D1" t="s" s="2"><v>' + str(get_str_id("Business & Pricing Impact")) + '</v></c></row>',
        '<row r="2"><c r="A2" t="s" s="3"><v>' + str(get_str_id("Driving Risk Scoring")) + '</v></c><c r="B2" t="s" s="0"><v>' + str(get_str_id("Harsh Braking Events")) + '</v></c><c r="C2" t="s" s="0"><v>' + str(get_str_id("-2.5 pts per incident / 100km")) + '</v></c><c r="D2" t="s" s="0"><v>' + str(get_str_id("Measures crash probability (Tailgating / Inattention)")) + '</v></c></row>',
        '<row r="3"><c r="A3" t="s" s="0"><v>' + str(get_str_id("Driving Risk Scoring")) + '</v></c><c r="B3" t="s" s="0"><v>' + str(get_str_id("Speed Limit Violations")) + '</v></c><c r="C3" t="s" s="0"><v>' + str(get_str_id("-3.0 pts per incident / 100km")) + '</v></c><c r="D3" t="s" s="0"><v>' + str(get_str_id("Strongest predictor of claim severity")) + '</v></c></row>',
        '<row r="4"><c r="A4" t="s" s="0"><v>' + str(get_str_id("Driving Risk Scoring")) + '</v></c><c r="B4" t="s" s="0"><v>' + str(get_str_id("Late Night Driving %")) + '</v></c><c r="C4" t="s" s="0"><v>' + str(get_str_id("-0.5 pts per 1% night travel")) + '</v></c><c r="D4" t="s" s="0"><v>' + str(get_str_id("11 PM - 4 AM driving carries 3x accident rate")) + '</v></c></row>',
        '<row r="5"><c r="A5" t="s" s="0"><v>' + str(get_str_id("Driving Risk Scoring")) + '</v></c><c r="B5" t="s" s="0"><v>' + str(get_str_id("Rapid Acceleration")) + '</v></c><c r="C5" t="s" s="0"><v>' + str(get_str_id("-1.5 pts per event")) + '</v></c><c r="D5" t="s" s="0"><v>' + str(get_str_id("Indicates aggressive acceleration & rash behavior")) + '</v></c></row>',
        '<row r="6"><c r="A6" t="s" s="3"><v>' + str(get_str_id("Insurance Tier Tiering")) + '</v></c><c r="B6" t="s" s="0"><v>' + str(get_str_id("Score >= 80 (Low Risk)")) + '</v></c><c r="C6" t="s" s="0"><v>' + str(get_str_id("-20% Discount on Base Premium")) + '</v></c><c r="D6" t="s" s="0"><v>' + str(get_str_id("Rewards safe driving (Pay-How-You-Drive)")) + '</v></c></row>',
        '<row r="7"><c r="A7" t="s" s="0"><v>' + str(get_str_id("Insurance Tier Tiering")) + '</v></c><c r="B7" t="s" s="0"><v>' + str(get_str_id("Score 60 - 79 (Moderate Risk)")) + '</v></c><c r="C7" t="s" s="0"><v>' + str(get_str_id("Standard Rate (0% adjustment)")) + '</v></c><c r="D7" t="s" s="0"><v>' + str(get_str_id("Average driver risk baseline")) + '</v></c></row>',
        '<row r="8"><c r="A8" t="s" s="0"><v>' + str(get_str_id("Insurance Tier Tiering")) + '</v></c><c r="B8" t="s" s="0"><v>' + str(get_str_id("Score < 60 (High Risk)")) + '</v></c><c r="C8" t="s" s="0"><v>' + str(get_str_id("+25% Surcharge on Base Premium")) + '</v></c><c r="D8" t="s" s="0"><v>' + str(get_str_id("Compensates for high loss probability")) + '</v></c></row>',
        '<row r="9"><c r="A9" t="s" s="3"><v>' + str(get_str_id("Vehicle Quality & Health")) + '</v></c><c r="B9" t="s" s="0"><v>' + str(get_str_id("Battery Voltage (<12.2V)")) + '</v></c><c r="C9" t="s" s="0"><v>' + str(get_str_id("-25 pts deduction")) + '</v></c><c r="D9" t="s" s="0"><v>' + str(get_str_id("Early warning for alternator/battery failure")) + '</v></c></row>',
        '<row r="10"><c r="A10" t="s" s="0"><v>' + str(get_str_id("Vehicle Quality & Health")) + '</v></c><c r="B10" t="s" s="0"><v>' + str(get_str_id("Engine Overheating (>95°C)")) + '</v></c><c r="C10" t="s" s="0"><v>' + str(get_str_id("-15 to -30 pts deduction")) + '</v></c><c r="D10" t="s" s="0"><v>' + str(get_str_id("Prevents catastrophic engine failure/warranty claim")) + '</v></c></row>',
        '<row r="11"><c r="A11" t="s" s="0"><v>' + str(get_str_id("Vehicle Quality & Health")) + '</v></c><c r="B11" t="s" s="0"><v>' + str(get_str_id("Brake Wear (>75%)")) + '</v></c><c r="C11" t="s" s="0"><v>' + str(get_str_id("-30 pts deduction + ₹1,500 buffer")) + '</v></c><c r="D11" t="s" s="0"><v>' + str(get_str_id("Immediate safety hazard trigger & servicing alert")) + '</v></c></row>',
        '<row r="12"><c r="A12" t="s" s="3"><v>' + str(get_str_id("Distance Pricing")) + '</v></c><c r="B12" t="s" s="0"><v>' + str(get_str_id("Monthly Distance KM")) + '</v></c><c r="C12" t="s" s="0"><v>' + str(get_str_id("₹2.00 per km (Pay As You Drive)")) + '</v></c><c r="D12" t="s" s="0"><v>' + str(get_str_id("Low mileage drivers save significantly on premiums")) + '</v></c></row>'
    ]

    sheet2_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sheetFormatPr defaultRowHeight="22"/>
    <cols>
        <col min="1" max="1" width="25" customWidth="1"/>
        <col min="2" max="2" width="30" customWidth="1"/>
        <col min="3" max="3" width="32" customWidth="1"/>
        <col min="4" max="4" width="48" customWidth="1"/>
    </cols>
    <sheetData>
        {"".join(s2_rows)}
    </sheetData>
</worksheet>"""

    # Build Sheet 3: Executive Summary / KPIs
    s3_rows = [
        '<row r="1" ht="28"><c r="A1" t="s" s="1"><v>' + str(get_str_id("Fleet Portfolio KPI")) + '</v></c><c r="B1" t="s" s="1"><v>' + str(get_str_id("Value / Metric")) + '</v></c><c r="C1" t="s" s="1"><v>' + str(get_str_id("Business Strategic Insight")) + '</v></c></row>',
        '<row r="2"><c r="A2" t="s" s="0"><v>' + str(get_str_id("Total Fleet Vehicles Monitored")) + '</v></c><c r="B2" s="5"><f>COUNTA(\'Fleet Telematics &amp; Risk\'!A2:A26)</f><v>25</v></c><c r="C2" t="s" s="0"><v>' + str(get_str_id("Sample connected vehicle portfolio under active telematics")) + '</v></c></row>',
        '<row r="3"><c r="A3" t="s" s="0"><v>' + str(get_str_id("Average Driving Safety Score")) + '</v></c><c r="B3" s="5"><f>ROUND(AVERAGE(\'Fleet Telematics &amp; Risk\'!M2:M26), 1)</f><v>76.4</v></c><c r="C3" t="s" s="0"><v>' + str(get_str_id("Healthy portfolio baseline; 12 drivers eligible for 20% discount")) + '</v></c></row>',
        '<row r="4"><c r="A4" t="s" s="0"><v>' + str(get_str_id("Low Risk Drivers Count (Score >= 80)")) + '</v></c><c r="B4" s="5"><f>COUNTIF(\'Fleet Telematics &amp; Risk\'!N2:N26, "Low Risk")</f><v>12</v></c><c r="C4" t="s" s="0"><v>' + str(get_str_id("48% of drivers benefit from Pay-How-You-Drive incentives")) + '</v></c></row>',
        '<row r="5"><c r="A5" t="s" s="0"><v>' + str(get_str_id("High Risk Drivers Count (Score < 60)")) + '</v></c><c r="B5" s="5"><f>COUNTIF(\'Fleet Telematics &amp; Risk\'!N2:N26, "High Risk")</f><v>6</v></c><c r="C5" t="s" s="0"><v>' + str(get_str_id("24% flagged for aggressive driving; risk surcharge applied")) + '</v></c></row>',
        '<row r="6"><c r="A6" t="s" s="0"><v>' + str(get_str_id("Critical Maintenance Alerts Flagged")) + '</v></c><c r="B6" s="5"><f>COUNTIF(\'Fleet Telematics &amp; Risk\'!P2:P26, "Critical Maintenance")</f><v>5</v></c><c r="C6" t="s" s="0"><v>' + str(get_str_id("Immediate inspection prevents roadside breakdowns and severe claims")) + '</v></c></row>',
        '<row r="7"><c r="A7" t="s" s="0"><v>' + str(get_str_id("Total Dynamic Premium Collected (₹)")) + '</v></c><c r="B7" s="0"><f>SUM(\'Fleet Telematics &amp; Risk\'!U2:U26)</f><v>435550</v></c><c r="C7" t="s" s="0"><v>' + str(get_str_id("Fair dynamic risk-based revenue stream")) + '</v></c></row>',
        '<row r="8"><c r="A8" t="s" s="0"><v>' + str(get_str_id("Total Safe Driver Savings Delivered (₹)")) + '</v></c><c r="B8" s="0"><f>SUM(\'Fleet Telematics &amp; Risk\'!W2:W26)</f><v>114450</v></c><c r="C8" t="s" s="0"><v>' + str(get_str_id("Total customer retention value created through telematics discounts")) + '</v></c></row>'
    ]

    sheet3_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sheetFormatPr defaultRowHeight="22"/>
    <cols>
        <col min="1" max="1" width="34" customWidth="1"/>
        <col min="2" max="2" width="22" customWidth="1"/>
        <col min="3" max="3" width="55" customWidth="1"/>
    </cols>
    <sheetData>
        {"".join(s3_rows)}
    </sheetData>
</worksheet>"""

    import html
    def xml_esc(val):
        return html.escape(str(val))

    # Build Shared Strings XML
    sst_items = "".join([f"<si><t>{xml_esc(s)}</t></si>" for s in strings])
    sst_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{len(strings)}" uniqueCount="{len(strings)}">
    {sst_items}
</sst>"""

    # Create Zip Archive
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('xl/_rels/workbook.xml.rels', wb_rels)
        zf.writestr('xl/workbook.xml', workbook)
        zf.writestr('xl/styles.xml', styles)
        zf.writestr('xl/sharedStrings.xml', sst_xml)
        zf.writestr('xl/worksheets/sheet1.xml', sheet1_xml)
        zf.writestr('xl/worksheets/sheet2.xml', sheet2_xml)
        zf.writestr('xl/worksheets/sheet3.xml', sheet3_xml)

    print("Excel XLSX file successfully created at:", output_file)

if __name__ == "__main__":
    from generate_dataset import PROCESSED_DATA, DIR
    xlsx_path = os.path.join(DIR, "Telematics_Insurance_Maintenance_Analytics.xlsx")
    create_telematics_excel(xlsx_path, PROCESSED_DATA)
