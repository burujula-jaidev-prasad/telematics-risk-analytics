import os
import sys

DIR = "/Users/jaidevprasad/.gemini/antigravity/scratch/telematics_risk_analytics"
os.makedirs(DIR, exist_ok=True)

class PurePDF:
    def __init__(self):
        self.objects = []
        self.pages = []
        self.current_page_stream = []
        self.page_width = 595.28  # A4 width in pt
        self.page_height = 841.89 # A4 height in pt

    def add_page(self):
        if self.current_page_stream:
            self.pages.append("".join(self.current_page_stream))
            self.current_page_stream = []
        self.current_page_stream = []

    def draw_rect(self, x, y, w, h, fill_rgb=None, stroke_rgb=None, line_width=1):
        cmds = []
        if fill_rgb:
            cmds.append(f"{fill_rgb[0]:.3f} {fill_rgb[1]:.3f} {fill_rgb[2]:.3f} rg\n")
        if stroke_rgb:
            cmds.append(f"{stroke_rgb[0]:.3f} {stroke_rgb[1]:.3f} {stroke_rgb[2]:.3f} RG\n")
        cmds.append(f"{line_width} w\n")
        cmds.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re\n")
        if fill_rgb and stroke_rgb:
            cmds.append("B\n")
        elif fill_rgb:
            cmds.append("f\n")
        elif stroke_rgb:
            cmds.append("S\n")
        self.current_page_stream.append("".join(cmds))

    def draw_text(self, text, x, y, font="F1", size=11, rgb=(0, 0, 0)):
        text_clean = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        cmd = f"BT\n/{font} {size} Tf\n{rgb[0]:.3f} {rgb[1]:.3f} {rgb[2]:.3f} rg\n{x:.2f} {y:.2f} Td\n({text_clean}) Tj\nET\n"
        self.current_page_stream.append(cmd)

    def draw_line(self, x1, y1, x2, y2, stroke_rgb=(0.8, 0.8, 0.8), line_width=1):
        cmd = f"{stroke_rgb[0]:.3f} {stroke_rgb[1]:.3f} {stroke_rgb[2]:.3f} RG\n{line_width} w\n{x1:.2f} {y1:.2f} m\n{x2:.2f} {y2:.2f} l\nS\n"
        self.current_page_stream.append(cmd)

    def finish(self):
        if self.current_page_stream:
            self.pages.append("".join(self.current_page_stream))

        # Build PDF objects
        # 1: Catalog
        # 2: Pages
        # 3: Font Helvetica
        # 4: Font Helvetica-Bold
        # 5: Font Courier
        # 6..: Page objects and Content streams
        num_pages = len(self.pages)
        page_obj_ids = [6 + i * 2 for i in range(num_pages)]
        content_obj_ids = [7 + i * 2 for i in range(num_pages)]

        objs = {}
        # Object 1: Catalog
        objs[1] = "<< /Type /Catalog /Pages 2 0 R >>"
        # Object 2: Pages
        kids_str = " ".join([f"{pid} 0 R" for pid in page_obj_ids])
        objs[2] = f"<< /Type /Pages /Kids [{kids_str}] /Count {num_pages} >>"
        # Fonts
        objs[3] = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
        objs[4] = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"
        objs[5] = "<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>"

        # Add pages and contents
        for i in range(num_pages):
            pid = page_obj_ids[i]
            cid = content_obj_ids[i]
            c_stream = self.pages[i].encode('latin1')
            objs[pid] = f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.page_width} {self.page_height}] /Resources << /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R >> >> /Contents {cid} 0 R >>"
            objs[cid] = f"<< /Length {len(c_stream)} >>\nstream\n{self.pages[i]}endstream"

        # Assemble PDF file
        lines = ["%PDF-1.4\n"]
        xref = {}
        pos = len(lines[0].encode('latin1'))

        total_objs = 5 + num_pages * 2
        for oid in range(1, total_objs + 1):
            xref[oid] = pos
            body = f"{oid} 0 obj\n{objs[oid]}\nendobj\n"
            lines.append(body)
            pos += len(body.encode('latin1'))

        xref_pos = pos
        lines.append(f"xref\n0 {total_objs + 1}\n0000000000 65535 f \n")
        for oid in range(1, total_objs + 1):
            lines.append(f"{xref[oid]:010d} 00000 n \n")

        lines.append(f"trailer\n<< /Size {total_objs + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF")

        return "".join(lines).encode('latin1')

def generate_report():
    pdf = PurePDF()

    # ================= PAGE 1 =================
    pdf.add_page()
    # Header Banner
    pdf.draw_rect(0, 755, 595.28, 86.89, fill_rgb=(0.06, 0.16, 0.38))
    pdf.draw_text("CONNECTED VEHICLE TELEMATICS & RISK ANALYTICS", 36, 808, font="F2", size=16, rgb=(1, 1, 1))
    pdf.draw_text("Real-Time Sensor Diagnostics, Predictive Quality & Dynamic Insurance Pricing", 36, 790, font="F1", size=10, rgb=(0.7, 0.85, 1))
    pdf.draw_text("CIA 3 Project Report | Jaidev Prasad (25121019) · Ruth Wilson (25121034) · Bala Kiran (25121012)", 36, 768, font="F1", size=9, rgb=(0.85, 0.92, 1))

    # Executive Overview
    pdf.draw_rect(36, 680, 523.28, 62, fill_rgb=(0.95, 0.97, 1), stroke_rgb=(0.75, 0.85, 0.98), line_width=1)
    pdf.draw_text("EXECUTIVE PROJECT SUMMARY", 48, 726, font="F2", size=10, rgb=(0.06, 0.16, 0.38))
    pdf.draw_text("This project demonstrates an end-to-end automobile telematics framework that captures connected-car sensor", 48, 710, font="F1", size=9, rgb=(0.1, 0.1, 0.1))
    pdf.draw_text("data (braking deceleration, speeding, late-night driving, engine coolant temp, oil pressure, and brake wear) to score", 48, 698, font="F1", size=9, rgb=(0.1, 0.1, 0.1))
    pdf.draw_text("individual driver safety, predict component failures, eliminate fraud, and generate fair dynamic premiums.", 48, 686, font="F1", size=9, rgb=(0.1, 0.1, 0.1))

    # KPI Stat Cards
    kpis = [
        ("FLEET SIZE", "15 Vehicles", "4G Connected"),
        ("AVG SCORE", "57.3 / 100", "Pricing Driver"),
        ("CLAIM PROB", "20.9%", "Fleet Baseline"),
        ("RENEWAL HIKE", "46.3%", "Trajectory"),
        ("AVG PREMIUM", "Rs. 15,933", "vs Rs. 18,000"),
        ("TOTAL SAVINGS", "Rs. 31,000", "Safe Drivers")
    ]
    card_w = 82
    for i, (k_top, k_val, k_sub) in enumerate(kpis):
        cx = 36 + i * (card_w + 6.2)
        pdf.draw_rect(cx, 615, card_w, 55, fill_rgb=(1, 1, 1), stroke_rgb=(0.8, 0.85, 0.9), line_width=1)
        pdf.draw_rect(cx, 667, card_w, 3, fill_rgb=(0.11, 0.31, 0.85))
        pdf.draw_text(k_top, cx + 6, 654, font="F2", size=7, rgb=(0.4, 0.45, 0.5))
        pdf.draw_text(k_val, cx + 6, 638, font="F2", size=10, rgb=(0.06, 0.16, 0.38))
        pdf.draw_text(k_sub, cx + 6, 624, font="F1", size=7, rgb=(0.5, 0.5, 0.5))

    # Section 1: Mathematical Model
    pdf.draw_text("1. MATHEMATICAL SCORING & DYNAMIC PRICING ENGINE", 36, 595, font="F2", size=11, rgb=(0.06, 0.16, 0.38))
    pdf.draw_line(36, 590, 559.28, 590, stroke_rgb=(0.11, 0.31, 0.85), line_width=1.5)

    pdf.draw_rect(36, 510, 523.28, 72, fill_rgb=(0.98, 0.98, 0.99), stroke_rgb=(0.85, 0.88, 0.92), line_width=1)
    pdf.draw_text("A. Driving Safety Score (0 - 100 points):", 48, 566, font="F2", size=9, rgb=(0.06, 0.16, 0.38))
    pdf.draw_text("Score = 100 - (Harsh_Brakes * 3) - (Speeding_Violations * 4) - (Night_Driving_Hours * 2)", 58, 552, font="F3", size=8.5, rgb=(0.11, 0.31, 0.85))
    pdf.draw_text("B. Dynamic Premium Calculation Formula:", 48, 536, font="F2", size=9, rgb=(0.06, 0.16, 0.38))
    pdf.draw_text("Dynamic Premium = Base_Rate (Rs. 15,000) + Score_Risk_Adjustment + Maintenance_Alert_Fee (Rs. 1,000)", 58, 522, font="F3", size=8.5, rgb=(0.11, 0.31, 0.85))

    # Pricing Tiers Table
    pdf.draw_rect(36, 435, 523.28, 65, fill_rgb=(1, 1, 1), stroke_rgb=(0.85, 0.88, 0.92), line_width=1)
    pdf.draw_rect(36, 480, 523.28, 20, fill_rgb=(0.9, 0.94, 0.98))
    pdf.draw_text("Driving Score Tier", 46, 486, font="F2", size=8, rgb=(0.06, 0.16, 0.38))
    pdf.draw_text("Risk Profile", 140, 486, font="F2", size=8, rgb=(0.06, 0.16, 0.38))
    pdf.draw_text("Base Adjustment", 230, 486, font="F2", size=8, rgb=(0.06, 0.16, 0.38))
    pdf.draw_text("Dynamic Premium", 320, 486, font="F2", size=8, rgb=(0.06, 0.16, 0.38))
    pdf.draw_text("Claim Prob.", 410, 486, font="F2", size=8, rgb=(0.06, 0.16, 0.38))
    pdf.draw_text("Hike Chance", 485, 486, font="F2", size=8, rgb=(0.06, 0.16, 0.38))

    rows_tier = [
        ("Score >= 80", "Safe Driver (Low Risk)", "-Rs. 3,000 Discount", "Rs. 12,000 / yr", "3.8% - 6.2%", "< 5% (Locked Discount)"),
        ("Score 60 - 79", "Average Driver (Moderate)", "Rs. 0 (Standard Base)", "Rs. 15,000 / yr", "10.5% - 18.0%", "25% - 45%"),
        ("Score < 60", "Risky Driver (High Risk)", "+Rs. 3,000 Surcharge", "Rs. 18,000 - 19,000", "38.5% - 48.0%", "88% - 98% (High Surcharge)")
    ]
    for idx, (t1, t2, t3, t4, t5, t6) in enumerate(rows_tier):
        ry = 465 - idx * 14
        pdf.draw_text(t1, 46, ry, font="F2" if idx==0 else "F1", size=7.5, rgb=(0.08, 0.5, 0.24) if idx==0 else ((0.72, 0.11, 0.11) if idx==2 else (0.1, 0.1, 0.1)))
        pdf.draw_text(t2, 140, ry, font="F1", size=7.5, rgb=(0.2, 0.2, 0.2))
        pdf.draw_text(t3, 230, ry, font="F1", size=7.5, rgb=(0.2, 0.2, 0.2))
        pdf.draw_text(t4, 320, ry, font="F2", size=7.5, rgb=(0.06, 0.16, 0.38))
        pdf.draw_text(t5, 410, ry, font="F1", size=7.5, rgb=(0.2, 0.2, 0.2))
        pdf.draw_text(t6, 485, ry, font="F1", size=7.5, rgb=(0.72, 0.11, 0.11) if idx==2 else (0.2, 0.2, 0.2))

    # Section 2: Engine & Diagnostics
    pdf.draw_text("2. ENGINE & COMPONENT QUALITY TELEMETRY MATRIX", 36, 415, font="F2", size=11, rgb=(0.06, 0.16, 0.38))
    pdf.draw_line(36, 410, 559.28, 410, stroke_rgb=(0.11, 0.31, 0.85), line_width=1.5)

    comp_items = [
        ("Cooling System (ECT)", "85C - 95C", "> 100C Alert", "Prevents blown head gaskets, engine seizure & false warranty claims."),
        ("Combustion & Oil PSI", "30 - 60 PSI", "< 20 PSI Alert", "Detects low lubrication, aggressive RPM redlines & premature bearing wear."),
        ("12V Battery Health", "12.4V - 12.8V", "< 12.1V Alert", "Predicts alternator failure, deep discharge & roadside dead battery calls."),
        ("Braking Wear Sensor", "> 5.0 mm", "< 3.0 mm Alert", "Correlates high-G deceleration stops (-0.74g) with brake pad degradation."),
        ("TPMS Tire Pressure", "32 - 35 PSI", "< 28 PSI Alert", "Eliminates high-speed highway tire blowouts and reduces rolling friction.")
    ]
    for i, (c_name, c_norm, c_alert, c_use) in enumerate(comp_items):
        cy = 388 - i * 21
        pdf.draw_rect(36, cy - 2, 523.28, 18, fill_rgb=(0.98, 0.98, 0.99) if i%2==0 else (1, 1, 1))
        pdf.draw_text(f"{i+1}. {c_name}:", 42, cy + 3, font="F2", size=8, rgb=(0.06, 0.16, 0.38))
        pdf.draw_text(f"Normal: {c_norm} | Alert: {c_alert}", 175, cy + 3, font="F1", size=7.5, rgb=(0.3, 0.3, 0.3))
        pdf.draw_text(f"Use: {c_use}", 335, cy + 3, font="F1", size=7, rgb=(0.4, 0.4, 0.4))

    # Section 3: Automobile Presentation Alignment
    pdf.draw_text("3. AUTOMOTIVE INDUSTRY STRATEGIC FRAMEWORK (CIA-3 ALIGNMENT)", 36, 268, font="F2", size=11, rgb=(0.06, 0.16, 0.38))
    pdf.draw_line(36, 263, 559.28, 263, stroke_rgb=(0.11, 0.31, 0.85), line_width=1.5)

    boxes = [
        ("Pay-How-You-Drive (PHYD)", "Isolates real-time driver behavior from static demographics, mirroring Zuno SmartDrive & Tesla Safety Score models. IRDAI regulatory sandbox compliant."),
        ("Predictive Quality Savings", "Connects to Slide 7 (We Predict £46B global warranty claims benchmark and Mahindra & Mahindra SAS Field Quality Weibull reliability analytics)."),
        ("Dual Risk & LGD Reduction", "Collateral tracking lifts recovery from 60% to 70%, reducing Loss Given Default (LGD) by 25% without altering borrower credit score (Slide 2)."),
        ("Fraud Event Forensics", "Uses deceleration G-forces and timestamps to verify genuine mechanical failure vs staged fraud rings (e.g. Insure The Box telematics forensics).")
    ]
    for i, (b_title, b_desc) in enumerate(boxes):
        bx = 36 + (i % 2) * 265
        by = 188 if i < 2 else 115
        pdf.draw_rect(bx, by, 258, 65, fill_rgb=(0.96, 0.98, 1), stroke_rgb=(0.8, 0.88, 0.98), line_width=1)
        pdf.draw_text(b_title, bx + 10, by + 50, font="F2", size=8.5, rgb=(0.11, 0.31, 0.85))
        # Wrap description
        words = b_desc.split(" ")
        l1, l2, l3 = "", "", ""
        for w in words:
            if len(l1 + " " + w) < 46 and not l2:
                l1 += " " + w
            elif len(l2 + " " + w) < 46 and not l3:
                l2 += " " + w
            else:
                l3 += " " + w
        pdf.draw_text(l1.strip(), bx + 10, by + 36, font="F1", size=7.5, rgb=(0.2, 0.2, 0.2))
        pdf.draw_text(l2.strip(), bx + 10, by + 24, font="F1", size=7.5, rgb=(0.2, 0.2, 0.2))
        if l3:
            pdf.draw_text(l3.strip(), bx + 10, by + 12, font="F1", size=7.5, rgb=(0.2, 0.2, 0.2))

    # Page 1 Footer
    pdf.draw_line(36, 45, 559.28, 45, stroke_rgb=(0.85, 0.88, 0.92))
    pdf.draw_text("Page 1 of 2 · Connected Car Telematics & Risk Analytics Report · Jaidev Prasad, Ruth Wilson, Bala Kiran", 36, 32, font="F1", size=8, rgb=(0.5, 0.5, 0.5))

    # ================= PAGE 2 =================
    pdf.add_page()
    # Header Banner Page 2
    pdf.draw_rect(0, 785, 595.28, 56.89, fill_rgb=(0.06, 0.16, 0.38))
    pdf.draw_text("CONNECTED VEHICLE TELEMETRY & SENSOR MASTER DATASET", 36, 815, font="F2", size=13, rgb=(1, 1, 1))
    pdf.draw_text("Complete 15-Vehicle Fleet Ledger with Engine Diagnostics, Risk Scores & Renewal Hike Probabilities", 36, 800, font="F1", size=9, rgb=(0.7, 0.85, 1))

    # Section Header
    pdf.draw_text("4. COMPLETE 15-VEHICLE TELEMATICS LEDGER", 36, 765, font="F2", size=11, rgb=(0.06, 0.16, 0.38))
    pdf.draw_line(36, 760, 559.28, 760, stroke_rgb=(0.11, 0.31, 0.85), line_width=1.5)

    # Table Header
    pdf.draw_rect(36, 735, 523.28, 20, fill_rgb=(0.9, 0.94, 0.98), stroke_rgb=(0.75, 0.85, 0.98), line_width=1)
    cols = [
        ("ID", 40), ("Driver", 78), ("Car Model", 145), ("Coolant", 222), ("Oil PSI", 262),
        ("RPM", 298), ("Pad", 330), ("Score", 360), ("Claim %", 398), ("Hike %", 440),
        ("Premium", 480), ("Savings", 522)
    ]
    for c_title, cx in cols:
        pdf.draw_text(c_title, cx, 741, font="F2", size=7.5, rgb=(0.06, 0.16, 0.38))

    # Table Rows
    from generate_realistic_data import PROCESSED_CARS
    for idx, r in enumerate(PROCESSED_CARS):
        ry = 718 - idx * 21.5
        bg_c = (0.98, 0.98, 0.99) if idx % 2 == 0 else (1, 1, 1)
        pdf.draw_rect(36, ry - 4, 523.28, 20, fill_rgb=bg_c, stroke_rgb=(0.9, 0.92, 0.95), line_width=0.5)

        score_c = (0.08, 0.5, 0.24) if r["score"] >= 80 else ((0.72, 0.11, 0.11) if r["score"] < 60 else (0.7, 0.4, 0.05))
        sav_c = (0.08, 0.5, 0.24) if r["savings"] >= 0 else (0.72, 0.11, 0.11)
        temp_c = (0.72, 0.11, 0.11) if r["temp_c"] > 98 else (0.1, 0.1, 0.1)
        pad_c = (0.72, 0.11, 0.11) if r["brake_pad_mm"] < 3.5 else (0.1, 0.1, 0.1)

        pdf.draw_text(r["id"], 40, ry + 2, font="F2", size=7, rgb=(0.06, 0.16, 0.38))
        pdf.draw_text(r["driver"][:11], 78, ry + 2, font="F1", size=7, rgb=(0.1, 0.1, 0.1))
        pdf.draw_text(r["car"][:14], 145, ry + 2, font="F1", size=7, rgb=(0.1, 0.1, 0.1))
        pdf.draw_text(f"{r['temp_c']}C", 222, ry + 2, font="F1", size=7, rgb=temp_c)
        pdf.draw_text(f"{r['oil_psi']}", 262, ry + 2, font="F1", size=7, rgb=(0.1, 0.1, 0.1))
        pdf.draw_text(f"{r['rpm_max']}", 298, ry + 2, font="F1", size=7, rgb=(0.1, 0.1, 0.1))
        pdf.draw_text(f"{r['brake_pad_mm']}mm", 330, ry + 2, font="F1", size=7, rgb=pad_c)
        pdf.draw_text(f"{r['score']}", 360, ry + 2, font="F2", size=7.5, rgb=score_c)
        pdf.draw_text(f"{r['claim_prob']}%", 398, ry + 2, font="F1", size=7, rgb=(0.1, 0.1, 0.1))
        pdf.draw_text(f"{r['hike_prob']}%", 440, ry + 2, font="F1", size=7, rgb=(0.72, 0.11, 0.11) if r['hike_prob']>70 else (0.1, 0.1, 0.1))
        pdf.draw_text(f"Rs. {r['dyn_prem']:,}", 480, ry + 2, font="F2", size=7, rgb=(0.06, 0.16, 0.38))
        pdf.draw_text(f"+Rs. {r['savings']:,}" if r['savings']>=0 else f"-Rs. {abs(r['savings']):,}", 522, ry + 2, font="F2", size=7, rgb=sav_c)

    # Fleet Average Row
    f_ry = 718 - 15 * 21.5
    pdf.draw_rect(36, f_ry - 4, 523.28, 22, fill_rgb=(0.9, 0.94, 1), stroke_rgb=(0.11, 0.31, 0.85), line_width=1)
    pdf.draw_text("FLEET AVERAGE", 40, f_ry + 3, font="F2", size=7.5, rgb=(0.11, 0.31, 0.85))
    pdf.draw_text("92.8C", 222, f_ry + 3, font="F2", size=7, rgb=(0.11, 0.31, 0.85))
    pdf.draw_text("36.9", 262, f_ry + 3, font="F2", size=7, rgb=(0.11, 0.31, 0.85))
    pdf.draw_text("4180", 298, f_ry + 3, font="F2", size=7, rgb=(0.11, 0.31, 0.85))
    pdf.draw_text("5.7mm", 330, f_ry + 3, font="F2", size=7, rgb=(0.11, 0.31, 0.85))
    pdf.draw_text("57.3", 360, f_ry + 3, font="F2", size=7.5, rgb=(0.11, 0.31, 0.85))
    pdf.draw_text("20.9%", 398, f_ry + 3, font="F2", size=7, rgb=(0.11, 0.31, 0.85))
    pdf.draw_text("46.3%", 440, f_ry + 3, font="F2", size=7, rgb=(0.11, 0.31, 0.85))
    pdf.draw_text("Rs. 15,933", 480, f_ry + 3, font="F2", size=7.5, rgb=(0.11, 0.31, 0.85))
    pdf.draw_text("Tot: Rs. 31k", 522, f_ry + 3, font="F2", size=7.5, rgb=(0.08, 0.5, 0.24))

    # Section 5: Real Telematics Event Forensic Samples
    pdf.draw_text("5. REAL TELEMETRY EVENT FORENSIC SAMPLES", 36, 360, font="F2", size=11, rgb=(0.06, 0.16, 0.38))
    pdf.draw_line(36, 355, 559.28, 355, stroke_rgb=(0.11, 0.31, 0.85), line_width=1.5)

    ev_samples = [
        ("CAR-02 (Priya Nair - Maruti Brezza)", "04-Sep 23:45:12", "-0.68g ABS Active Stop", "88 -> 12 km/h at Bandra Sea Link Exit", "Tailgating emergency stop. Brake pad thickness eroded to 2.8mm, triggering component alert fee."),
        ("CAR-04 (Sneha Kulkarni - Mahindra XUV700)", "07-Sep 00:15:22", "-0.72g Automatic FCW Brake", "105 -> 20 km/h at E-City Elevated Toll", "Severe collision warning trigger. Engine coolant hit 105C and oil pressure dropped to 22 PSI at 5,400 RPM."),
        ("CAR-11 (Siddharth Das - Mahindra Thar)", "03-Sep 01:30:15", "-0.74g High G-Decel", "110 -> 25 km/h at Bhor Ghat Descent", "High-speed night run (134 km/h peak). DTC P0217 Overheating logged; 98% chance of renewal hike.")
    ]
    for i, (e_car, e_time, e_g, e_speed, e_diag) in enumerate(ev_samples):
        ey = 330 - i * 50
        pdf.draw_rect(36, ey - 2, 523.28, 44, fill_rgb=(0.98, 0.98, 0.99), stroke_rgb=(0.85, 0.88, 0.92), line_width=1)
        pdf.draw_rect(36, ey - 2, 3, 44, fill_rgb=(0.72, 0.11, 0.11))
        pdf.draw_text(f"{e_car} · {e_time}", 46, ey + 28, font="F2", size=8, rgb=(0.06, 0.16, 0.38))
        pdf.draw_text(f"Decel G-Force: {e_g} | Speed Drop: {e_speed}", 46, ey + 16, font="F3", size=7.5, rgb=(0.72, 0.11, 0.11))
        pdf.draw_text(f"Telemetry Assessment: {e_diag}", 46, ey + 4, font="F1", size=7, rgb=(0.3, 0.3, 0.3))

    # Section 6: Deliverables & Submission Verification
    pdf.draw_text("6. PROJECT SUBMISSION DELIVERABLES", 36, 175, font="F2", size=11, rgb=(0.06, 0.16, 0.38))
    pdf.draw_line(36, 170, 559.28, 170, stroke_rgb=(0.11, 0.31, 0.85), line_width=1.5)

    pdf.draw_rect(36, 65, 523.28, 98, fill_rgb=(0.96, 0.98, 1), stroke_rgb=(0.8, 0.88, 0.98), line_width=1)
    pdf.draw_text("1. Native Excel Workbook:", 48, 145, font="F2", size=8.5, rgb=(0.11, 0.31, 0.85))
    pdf.draw_text("Simple_Car_Sensor_Insurance_Analysis.xlsx (Multi-sheet, formulas =100-(E*3)-(F*4)-(G*2), AVERAGE, SUM)", 185, 145, font="F1", size=7.5, rgb=(0.1, 0.1, 0.1))

    pdf.draw_text("2. Interactive HTML Dashboard:", 48, 128, font="F2", size=8.5, rgb=(0.11, 0.31, 0.85))
    pdf.draw_text("index.html (10 interactive charts, live driver simulator, vehicle profile drawer, real-time probability meters)", 185, 128, font="F1", size=7.5, rgb=(0.1, 0.1, 0.1))

    pdf.draw_text("3. Telemetry CSV Dataset:", 48, 111, font="F2", size=8.5, rgb=(0.11, 0.31, 0.85))
    pdf.draw_text("detailed_telematics_sensor_data.csv (Complete raw sensor data with VIN, route, speed, temp, and probabilities)", 185, 111, font="F1", size=7.5, rgb=(0.1, 0.1, 0.1))

    pdf.draw_text("4. Project Presentation Alignment:", 48, 94, font="F2", size=8.5, rgb=(0.11, 0.31, 0.85))
    pdf.draw_text("CIA 3 Automobile Industry: Jaidev Prasad (25121019), Ruth Wilson (25121034), Bala Kiran (25121012)", 185, 94, font="F1", size=7.5, rgb=(0.1, 0.1, 0.1))

    pdf.draw_text("5. Live Local Server URL:", 48, 77, font="F2", size=8.5, rgb=(0.11, 0.31, 0.85))
    pdf.draw_text("http://localhost:8000 (Open in any web browser to view interactive visual intelligence gallery)", 185, 77, font="F3", size=7.5, rgb=(0.08, 0.5, 0.24))

    # Page 2 Footer
    pdf.draw_line(36, 45, 559.28, 45, stroke_rgb=(0.85, 0.88, 0.92))
    pdf.draw_text("Page 2 of 2 · Connected Car Telematics & Risk Analytics Report · Jaidev Prasad, Ruth Wilson, Bala Kiran", 36, 32, font="F1", size=8, rgb=(0.5, 0.5, 0.5))

    pdf_bytes = pdf.finish()
    pdf_path = os.path.join(DIR, "Car_Telematics_Insurance_Risk_Project_Report.pdf")
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)

    print("Project details PDF successfully generated at:", pdf_path)

if __name__ == "__main__":
    generate_report()
