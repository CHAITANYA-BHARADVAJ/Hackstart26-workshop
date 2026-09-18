"""
Phishing Awareness Training - Workplan PDF Generator
Anonymous SDMCET
"""

from fpdf import FPDF
import os


class WorkplanPDF(FPDF):
    """Custom PDF with header/footer branding."""

    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, "Anonymous SDMCET  |  Phishing Awareness Training  |  Workplan", align="C")
        self.ln(4)
        self.set_draw_color(0, 180, 220)
        self.set_line_width(0.6)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(0, 180, 220)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(130, 130, 130)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}  |  Anonymous SDMCET - Cybersecurity Club",
                  align="C")

    def section_title(self, number, title):
        self.ln(4)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 150, 200)
        self.cell(0, 10, f"  {number}. {title}", ln=True)
        self.set_draw_color(0, 150, 200)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 120, self.get_y())
        self.ln(4)

    def sub_title(self, text):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(50, 50, 50)
        self.cell(0, 7, f"  {text}", ln=True)
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 5.5, f"    {text}")
        self.ln(1)

    def bullet(self, text, indent=12):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(60, 60, 60)
        x = self.get_x()
        self.set_x(x + indent)
        self.cell(4, 5.5, "-")
        self.multi_cell(0, 5.5, f"  {text}")
        self.ln(0.5)

    def checkbox(self, text, indent=12):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(60, 60, 60)
        x = self.get_x()
        y = self.get_y()
        self.set_draw_color(100, 100, 100)
        self.set_line_width(0.3)
        self.rect(x + indent, y + 0.5, 4, 4)
        self.set_x(x + indent + 6)
        self.multi_cell(0, 5.5, text)
        self.ln(0.5)

    def table_header(self, cols, widths):
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 150, 200)
        self.set_text_color(255, 255, 255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 7, f" {col}", border=1, fill=True)
        self.ln()

    def table_row(self, cols, widths, fill=False):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(50, 50, 50)
        if fill:
            self.set_fill_color(240, 248, 255)
        else:
            self.set_fill_color(255, 255, 255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 6.5, f" {col}", border=1, fill=True)
        self.ln()

    def info_box(self, title, text):
        self.ln(2)
        self.set_fill_color(230, 245, 255)
        self.set_draw_color(0, 150, 200)
        self.set_line_width(0.4)
        x = self.get_x() + 10
        y = self.get_y()
        self.set_x(x)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 120, 180)
        self.cell(180, 7, f"  {title}", ln=True, fill=True, border="LTR")
        self.set_x(x)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(50, 50, 50)
        self.multi_cell(180, 5, f"  {text}", fill=True, border="LBR")
        self.ln(3)

    def divider(self):
        self.ln(3)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.2)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)


def build_pdf():
    pdf = WorkplanPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ──────────────────────────────────────────
    # COVER PAGE
    # ──────────────────────────────────────────
    pdf.add_page()
    pdf.ln(45)

    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(0, 150, 200)
    pdf.cell(0, 14, "WORKPLAN", align="C", ln=True)

    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, "Phishing Awareness Training Session", align="C", ln=True)

    pdf.ln(6)
    pdf.set_draw_color(0, 180, 220)
    pdf.set_line_width(0.8)
    pdf.line(70, pdf.get_y(), 140, pdf.get_y())
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, "ANONYMOUS SDMCET", align="C", ln=True)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Cybersecurity Club", align="C", ln=True)

    pdf.ln(30)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(120, 120, 120)

    details = [
        "Session Type:   Interactive Workshop + Game",
        "Duration:         35 - 45 minutes",
        "Audience:         Students (Zero Prior Knowledge)",
        "Materials:         13-Slide PPTX + Teaching Guide + This Workplan",
    ]
    for d in details:
        pdf.cell(0, 7, d, align="C", ln=True)

    # ──────────────────────────────────────────
    # PAGE 2: PROJECT OVERVIEW
    # ──────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("1", "PROJECT OVERVIEW")

    pdf.sub_title("1.1  Objective")
    pdf.body_text(
        "Conduct an engaging, interactive phishing awareness training session for students "
        "with zero cybersecurity background. The goal is to equip attendees with practical "
        "skills to identify and avoid phishing attacks in emails, SMS, and social media."
    )

    pdf.sub_title("1.2  Deliverables")
    pdf.bullet("13-slide PowerPoint presentation (dark cybersecurity theme, 16:9 widescreen)")
    pdf.bullet("3 interactive 'Spot the Phish' game scenarios with reveal slides")
    pdf.bullet("Instructor preparation guide with slide-by-slide talking points")
    pdf.bullet("This workplan document (session planning & execution roadmap)")

    pdf.sub_title("1.3  Success Criteria")
    pdf.bullet("Students can identify at least 3 of the 4 red flags taught in the session")
    pdf.bullet("Active participation during the 'Spot the Phish' game (>70% hand raises)")
    pdf.bullet("Students leave with actionable steps (enable 2FA, check sender addresses)")
    pdf.bullet("Positive feedback / interest in future Anonymous SDMCET sessions")

    # ──────────────────────────────────────────
    # SECTION 2: WORKFLOW PHASES
    # ──────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("2", "WORKFLOW PHASES")

    pdf.info_box("WORKFLOW OVERVIEW",
                 "Phase 1: Pre-Session Preparation  ->  Phase 2: Session Delivery  ->  "
                 "Phase 3: Post-Session Follow-Up")

    # --- Phase 1 ---
    pdf.sub_title("PHASE 1: PRE-SESSION PREPARATION (1-2 Days Before)")
    pdf.ln(2)

    widths = [10, 75, 50, 40]
    pdf.table_header(["#", "Task", "Owner", "Status"], widths)
    tasks_p1 = [
        ("1", "Read the Teaching Guide cover-to-cover", "Presenter", ""),
        ("2", "Rehearse presentation at least once (with timer)", "Presenter", ""),
        ("3", "Test PPTX on the venue projector/screen", "Tech Lead", ""),
        ("4", "Verify Presenter View works (Alt+F5)", "Presenter", ""),
        ("5", "Prepare whiteboard/markers for the venue", "Coordinator", ""),
        ("6", "Send session invite/announcement to students", "Coordinator", ""),
        ("7", "Prepare backup: keep PPTX on USB + cloud drive", "Tech Lead", ""),
        ("8", "Review the 15+ Q&A section in Teaching Guide", "Presenter", ""),
        ("9", "Pick 3-4 real-world stats to mention casually", "Presenter", ""),
        ("10", "Optional: Prepare a printed 1-page handout", "Coordinator", ""),
    ]
    for i, row in enumerate(tasks_p1):
        pdf.table_row(row, widths, fill=(i % 2 == 0))

    pdf.ln(4)

    # --- Phase 2 ---
    pdf.sub_title("PHASE 2: SESSION DELIVERY (Day of Event)")
    pdf.ln(2)

    widths2 = [10, 70, 55, 40]
    pdf.table_header(["#", "Task", "Owner", "Status"], widths2)
    tasks_p2 = [
        ("1", "Arrive 20 min early, set up projector + audio", "Tech Lead", ""),
        ("2", "Open PPTX in Slideshow mode, test display", "Presenter", ""),
        ("3", "Welcome students, quick icebreaker", "Presenter", ""),
        ("4", "Deliver Slides 1-6 (Educational Content)", "Presenter", ""),
        ("5", "Deliver Slide 7 (Game Transition - build energy)", "Presenter", ""),
        ("6", "Run Game: Slides 8-13 (facilitate discussion)", "Presenter", ""),
        ("7", "Wrap up with key takeaways + action items", "Presenter", ""),
        ("8", "Open floor for Q&A (5-10 min)", "Presenter", ""),
        ("9", "Collect feedback (show of hands or form)", "Coordinator", ""),
        ("10", "Thank attendees, announce next session topic", "Coordinator", ""),
    ]
    for i, row in enumerate(tasks_p2):
        pdf.table_row(row, widths2, fill=(i % 2 == 0))

    pdf.ln(4)

    # --- Phase 3 ---
    pdf.sub_title("PHASE 3: POST-SESSION FOLLOW-UP (1-3 Days After)")
    pdf.ln(2)

    pdf.table_header(["#", "Task", "Owner", "Status"], widths)
    tasks_p3 = [
        ("1", "Share session summary/key takeaways with attendees", "Coordinator", ""),
        ("2", "Share the 4 Red Flags one-pager (digital/print)", "Coordinator", ""),
        ("3", "Collect and review written feedback", "Club Lead", ""),
        ("4", "Post session photos/highlights on club social media", "Social Media", ""),
        ("5", "Team debrief: what went well, what to improve", "All Members", ""),
        ("6", "Plan next session topic based on student interest", "Club Lead", ""),
    ]
    for i, row in enumerate(tasks_p3):
        pdf.table_row(row, widths, fill=(i % 2 == 0))

    # ──────────────────────────────────────────
    # SECTION 3: SESSION TIMELINE
    # ──────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("3", "SESSION TIMELINE (Minute-by-Minute)")

    widths3 = [25, 18, 57, 72]
    pdf.table_header(["Time", "Slide(s)", "Section", "Presenter Action"], widths3)
    timeline = [
        ("0:00 - 2:00", "1", "Title & Hook", "Ask: 'Who has gotten a suspicious email?'"),
        ("2:00 - 6:00", "2", "What is Phishing?", "FedEx uniform analogy, walk 3 columns"),
        ("6:00 - 10:00", "3", "Red Flag #1: Urgency", "Read examples aloud with drama"),
        ("10:00 - 15:00", "4", "Red Flag #2: Sender", "GO SLOW - explain @ domain structure"),
        ("15:00 - 20:00", "5", "Red Flag #3: Links", "Demo hovering, explain file extensions"),
        ("20:00 - 23:00", "6", "Red Flag #4: Greetings", "Quick - simple concept, don't linger"),
        ("23:00 - 25:00", "7", "Game Transition", "Build energy, explain rules"),
        ("25:00 - 28:00", "8", "Scenario 1: Question", "30 sec reading, then hand raise vote"),
        ("28:00 - 30:00", "9", "Scenario 1: Reveal", "Walk through 4 red flag annotations"),
        ("30:00 - 33:00", "10", "Scenario 2: Question", "Ask: 'Would you buy the gift cards?'"),
        ("33:00 - 35:00", "11", "Scenario 2: Reveal", "Gift cards = scam currency (universal)"),
        ("35:00 - 38:00", "12", "Scenario 3: Question", "Hardest one - let them debate"),
        ("38:00 - 41:00", "13", "Scenario 3: Reveal", "Introduce spoofing concept + .exe danger"),
        ("41:00 - 45:00", "--", "Q&A + Closing", "Open floor, share action items"),
    ]
    for i, row in enumerate(timeline):
        pdf.table_row(row, widths3, fill=(i % 2 == 0))

    pdf.info_box("TIMING TIP",
                 "Running short? Cut Q&A - never rush the game. Running long? Shorten slides 3-6; "
                 "the red flags get reinforced during the game anyway.")

    # ──────────────────────────────────────────
    # SECTION 4: ROLES & RESPONSIBILITIES
    # ──────────────────────────────────────────
    pdf.section_title("4", "ROLES & RESPONSIBILITIES")

    widths4 = [35, 135]
    pdf.table_header(["Role", "Responsibilities"], widths4)
    roles = [
        ("Presenter", "Deliver all 13 slides, facilitate game, handle Q&A, manage timing"),
        ("Tech Lead", "Projector setup, backup files, troubleshoot AV issues during session"),
        ("Coordinator", "Student invites, room booking, printed materials, feedback collection"),
        ("Social Media", "Pre-event promotion, live photos during event, post-event highlights"),
        ("Club Lead", "Overall oversight, debrief, plan future sessions based on feedback"),
    ]
    for i, row in enumerate(roles):
        pdf.table_row(row, widths4, fill=(i % 2 == 0))

    # ──────────────────────────────────────────
    # SECTION 5: MATERIALS CHECKLIST
    # ──────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("5", "MATERIALS & EQUIPMENT CHECKLIST")

    pdf.sub_title("5.1  Digital Materials")
    pdf.checkbox("Phishing_Awareness_Training.pptx (on laptop)")
    pdf.checkbox("Phishing_Awareness_Training.pptx (backup on USB drive)")
    pdf.checkbox("Phishing_Awareness_Training.pptx (backup on cloud - Google Drive/OneDrive)")
    pdf.checkbox("Phishing_Awareness_Teaching_Guide.txt (for presenter reference)")
    pdf.checkbox("This Workplan PDF (printed or on tablet for coordinator)")

    pdf.ln(2)
    pdf.sub_title("5.2  Physical Materials")
    pdf.checkbox("Laptop with PowerPoint installed")
    pdf.checkbox("Projector + HDMI/VGA cable (test before session)")
    pdf.checkbox("Whiteboard + markers (for impromptu explanations)")
    pdf.checkbox("Printed handouts - 4 Red Flags summary (optional)")
    pdf.checkbox("Feedback forms or QR code to online form (optional)")
    pdf.checkbox("Extension cord / power strip")
    pdf.checkbox("Clicker / presentation remote (optional but helpful)")

    pdf.ln(2)
    pdf.sub_title("5.3  Room Requirements")
    pdf.checkbox("Projector screen visible to all seats")
    pdf.checkbox("Room capacity matches expected attendance")
    pdf.checkbox("Power outlets accessible near presenter position")
    pdf.checkbox("Lights can be dimmed (dark theme slides work best with dimmed lights)")

    # ──────────────────────────────────────────
    # SECTION 6: CONTENT SUMMARY
    # ──────────────────────────────────────────
    pdf.section_title("6", "PRESENTATION CONTENT MAP")

    widths5 = [14, 42, 50, 66]
    pdf.table_header(["Slide", "Title", "Type", "Key Takeaway"], widths5)
    slides = [
        ("1", "Title Slide", "Introduction", "Hook: billions of phishing emails daily"),
        ("2", "What is Phishing?", "Education", "They hack psychology, not computers"),
        ("3", "Red Flag #1", "Education", "Urgency/panic = the attack itself"),
        ("4", "Red Flag #2", "Education", "Always check domain after @ symbol"),
        ("5", "Red Flag #3", "Education", "Hover before click, never open .exe"),
        ("6", "Red Flag #4", "Education", "Generic greeting = mass phishing"),
        ("7", "Game Transition", "Transition", "Build energy for interactive game"),
        ("8", "Scenario 1: Bank", "Game Question", "Fake Chase email with bit.ly link"),
        ("9", "Scenario 1: Reveal", "Game Answer", "4 red flags annotated on email"),
        ("10", "Scenario 2: CEO SMS", "Game Question", "Gift card fraud via text message"),
        ("11", "Scenario 2: Reveal", "Game Answer", "Gift cards = untraceable scam currency"),
        ("12", "Scenario 3: Package", "Game Question", "FedEx email with .exe attachment"),
        ("13", "Scenario 3: Reveal", "Game Answer", "Spoofing + malware via attachments"),
    ]
    for i, row in enumerate(slides):
        pdf.table_row(row, widths5, fill=(i % 2 == 0))

    # ──────────────────────────────────────────
    # SECTION 7: RISK MITIGATION
    # ──────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("7", "RISK MITIGATION")

    widths6 = [55, 55, 55]
    pdf.table_header(["Risk", "Impact", "Mitigation"], widths6)
    risks = [
        ("Projector fails", "Cannot display slides", "Keep backup on USB + phone hotspot for cloud"),
        ("Low attendance", "Empty room, low energy", "Promote 3+ days early on all club channels"),
        ("Audience too quiet", "Game falls flat", "Use think-pair-share, cold call gently"),
        ("Audience too advanced", "Content feels basic", "Mention spear phishing, DMARC, 2FA depth"),
        ("Running over time", "Lose audience attention", "Cut Q&A, shorten slides 3-6"),
        ("Tough Q&A question", "Presenter unsure", "Say 'Great question, let me research that'"),
        ("PowerPoint version issue", "Formatting breaks", "Test on venue laptop beforehand"),
    ]
    for i, row in enumerate(risks):
        pdf.table_row(row, widths6, fill=(i % 2 == 0))

    # ──────────────────────────────────────────
    # SECTION 8: POST-SESSION METRICS
    # ──────────────────────────────────────────
    pdf.section_title("8", "POST-SESSION METRICS TO TRACK")

    pdf.sub_title("8.1  Quantitative")
    pdf.bullet("Number of attendees vs. RSVPs (attendance rate)")
    pdf.bullet("Game participation rate (% hands raised per scenario)")
    pdf.bullet("Number of correct identifications per scenario")
    pdf.bullet("Feedback score (if using a rating form, e.g., 1-5 stars)")

    pdf.ln(2)
    pdf.sub_title("8.2  Qualitative")
    pdf.bullet("Most common questions asked during Q&A")
    pdf.bullet("Which scenario generated the most discussion")
    pdf.bullet("Student suggestions for future session topics")
    pdf.bullet("Areas where students seemed most confused or surprised")

    pdf.ln(2)
    pdf.sub_title("8.3  Follow-Up Actions")
    pdf.bullet("Share a recap post on the club's social media within 24 hours")
    pdf.bullet("Send a follow-up email/message with the 4 Red Flags summary")
    pdf.bullet("Announce the next session topic within 1 week")
    pdf.bullet("Incorporate feedback into the next session's preparation")

    # ──────────────────────────────────────────
    # SECTION 9: QUICK REFERENCE CARD
    # ──────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("9", "QUICK REFERENCE - THE 4 RED FLAGS")

    pdf.info_box("RED FLAG #1 - URGENCY",
                 "If a message creates panic or demands immediate action (account locked, legal "
                 "threat, prize expiring), STOP. Real organizations rarely demand panicked responses.")

    pdf.info_box("RED FLAG #2 - SENDER ADDRESS",
                 "Never trust the display name. Check the actual email address after the @ symbol. "
                 "Look for misspellings, extra subdomains, and unofficial domains.")

    pdf.info_box("RED FLAG #3 - LINKS & ATTACHMENTS",
                 "Hover before you click. If the URL doesn't match the claimed destination, don't click. "
                 "Never open unexpected .exe, .zip, .scr, or .docm attachments.")

    pdf.info_box("RED FLAG #4 - GENERIC GREETINGS",
                 "If a company has your account, they know your name. 'Dear Customer' or 'Dear User' "
                 "suggests a mass phishing campaign.")

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 150, 200)
    pdf.cell(0, 10, "THE GOLDEN RULE", align="C", ln=True)
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 8, "When in doubt:  Don't click.  Don't download.  Don't reply.", align="C", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "Verify through a separate, known channel (official website, saved phone number, in person).",
             align="C", ln=True)

    pdf.ln(12)
    pdf.set_draw_color(0, 180, 220)
    pdf.set_line_width(0.5)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 150, 200)
    pdf.cell(0, 8, "Anonymous SDMCET - Cybersecurity Club", align="C", ln=True)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(130, 130, 130)
    pdf.cell(0, 6, "Empowering students to stay safe in the digital world.", align="C", ln=True)

    # ── Save ──
    output = os.path.join(os.path.dirname(__file__), "..",
                          "Phishing_Awareness_Workplan.pdf")
    output = os.path.abspath(output)
    pdf.output(output)
    print(f"[OK] Workplan PDF saved to: {output}")
    print(f"     {pdf.page_no()} pages generated")


if __name__ == "__main__":
    build_pdf()
