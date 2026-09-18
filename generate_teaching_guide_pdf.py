"""
Phishing Awareness Training - Teaching Guide PDF Generator
Anonymous SDMCET
"""

from fpdf import FPDF
import os


class TeachingGuidePDF(FPDF):

    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, "Anonymous SDMCET  |  Phishing Awareness  |  Instructor Guide",
                  align="C")
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

    def sec_title(self, number, title):
        self.ln(3)
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(0, 150, 200)
        self.cell(0, 10, f"  {number}. {title}", ln=True)
        self.set_draw_color(0, 150, 200)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 130, self.get_y())
        self.ln(4)

    def sub(self, text):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(50, 50, 50)
        self.cell(0, 7, f"  {text}", ln=True)
        self.ln(1)

    def slide_header(self, slide_num, title, duration):
        self.ln(2)
        self.set_fill_color(0, 150, 200)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, f"  SLIDE {slide_num} -- {title}  ({duration})", fill=True, ln=True)
        self.ln(3)
        self.set_text_color(50, 50, 50)

    def body(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 5.5, f"    {text}")
        self.ln(1)

    def label_body(self, label, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 120, 170)
        self.cell(0, 6, f"    {label}", ln=True)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 5.5, f"      {text}")
        self.ln(2)

    def bullet(self, text, indent=12):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(60, 60, 60)
        x = self.get_x()
        self.set_x(x + indent)
        self.cell(4, 5.5, "-")
        self.multi_cell(0, 5.5, f"  {text}")
        self.ln(0.5)

    def quote_box(self, text):
        self.ln(1)
        self.set_fill_color(245, 245, 245)
        self.set_draw_color(0, 150, 200)
        self.set_line_width(0.8)
        x = self.get_x() + 14
        y = self.get_y()
        self.line(x, y, x, y + 12)
        self.set_x(x + 4)
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(80, 80, 80)
        self.multi_cell(165, 5.5, text, fill=True)
        self.ln(2)

    def info_box(self, title, text):
        self.ln(2)
        self.set_fill_color(230, 245, 255)
        self.set_draw_color(0, 150, 200)
        self.set_line_width(0.4)
        x = self.get_x() + 10
        self.set_x(x)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 120, 180)
        self.cell(180, 7, f"  {title}", ln=True, fill=True, border="LTR")
        self.set_x(x)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(50, 50, 50)
        self.multi_cell(180, 5, f"  {text}", fill=True, border="LBR")
        self.ln(3)

    def warning_box(self, text):
        self.ln(1)
        self.set_fill_color(255, 245, 230)
        self.set_draw_color(220, 140, 0)
        self.set_line_width(0.4)
        x = self.get_x() + 10
        self.set_x(x)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(180, 100, 0)
        self.multi_cell(180, 5.5, f"  {text}", fill=True, border=1)
        self.ln(2)

    def tip_box(self, text):
        self.ln(1)
        self.set_fill_color(230, 255, 235)
        self.set_draw_color(40, 180, 80)
        self.set_line_width(0.4)
        x = self.get_x() + 10
        self.set_x(x)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(30, 120, 50)
        self.multi_cell(180, 5.5, f"  TIP: {text}", fill=True, border=1)
        self.ln(2)

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

    def qa_item(self, question, answer):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 100, 160)
        self.set_x(10)
        self.multi_cell(190, 5.5, f"Q: {question}")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(60, 60, 60)
        self.set_x(10)
        self.multi_cell(190, 5.5, f"A: {answer}")
        self.ln(3)


def build_pdf():
    pdf = TeachingGuidePDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── COVER PAGE ──
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 30)
    pdf.set_text_color(0, 150, 200)
    pdf.cell(0, 14, "INSTRUCTOR", align="C", ln=True)
    pdf.cell(0, 14, "PREPARATION GUIDE", align="C", ln=True)
    pdf.ln(4)
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
    pdf.ln(25)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(120, 120, 120)
    for d in [
        "Audience:       Students with Zero Prior Knowledge",
        "Duration:        35 - 45 minutes",
        "Format:           13-Slide PPTX + Interactive Game",
        "Tone:              Conversational, Relatable, Zero Jargon",
    ]:
        pdf.cell(0, 7, d, align="C", ln=True)

    # ── SECTION 1: BEFORE YOU BEGIN ──
    pdf.add_page()
    pdf.sec_title("1", "BEFORE YOU BEGIN -- MINDSET & SETUP")

    pdf.sub("1.1  Your Goal")
    pdf.body(
        "You are NOT teaching students to become cybersecurity experts. You are teaching "
        "them ONE practical life skill: how to pause and think before clicking. If they walk "
        "away remembering 'hover before you click' and 'verify through a separate channel,' "
        "you have succeeded."
    )

    pdf.sub("1.2  Room Setup")
    pdf.bullet("Projector/screen clearly visible to all students")
    pdf.bullet("Open the .pptx in Slideshow mode (press F5 in PowerPoint)")
    pdf.bullet("Keep speaker notes visible on your laptop (Presenter View -- press Alt+F5)")
    pdf.bullet("Have a whiteboard/marker available for impromptu explanations")
    pdf.bullet("Keep a browser tab open with a real email inbox (for live demos if needed)")

    pdf.sub("1.3  Your Tone")
    pdf.bullet("DO NOT lecture. Talk like you're warning a younger sibling about a scam")
    pdf.bullet("Use phrases like 'Here's the thing...', 'This is the part most people miss...'")
    pdf.bullet("Admit vulnerability: 'I almost fell for one of these myself once'")
    pdf.bullet("Make it a conversation, not a monologue -- ask questions constantly")

    pdf.warning_box(
        "IMPORTANT RULE: Never make students feel stupid for not knowing something. Phishing works "
        "on CEOs, engineers, and security professionals. If a student says 'I would have clicked "
        "that,' respond with: 'That's exactly why we're here -- so you won't next time.'"
    )

    # ── SECTION 2: KEY CONCEPTS ──
    pdf.add_page()
    pdf.sec_title("2", "KEY CONCEPTS YOU MUST UNDERSTAND")

    pdf.body(
        "Before teaching, make sure YOU are comfortable with these ideas. You don't need to "
        "explain all of them -- but you need to understand them so you can answer follow-up "
        "questions confidently."
    )

    pdf.sub("2.1  What is Social Engineering?")
    pdf.bullet("Simple definition: Tricking a human instead of hacking a computer")
    pdf.bullet("Analogy: A burglar doesn't pick your lock -- they dress as a delivery person and you open the door")
    pdf.bullet("It exploits trust, fear, urgency, curiosity, and helpfulness")

    pdf.sub("2.2  What is Phishing?")
    pdf.bullet("A type of social engineering done through digital messages (email, SMS, social media, calls)")
    pdf.bullet("The name comes from 'fishing' -- casting bait and waiting for someone to bite")
    pdf.bullet("The 'ph' spelling is a nod to early hacker culture ('phreaking' = phone hacking)")

    pdf.sub("2.3  Types of Phishing (mention ONLY if asked)")
    w = [35, 65, 85]
    pdf.table_header(["Type", "What It Is", "Example"], w)
    types = [
        ("Phishing", "Mass emails to thousands", "'Dear Customer, verify your account'"),
        ("Spear Phishing", "Targeted at specific person", "Uses your name, job title, recent activity"),
        ("Whaling", "Targets executives (CEO/CFO)", "Fake legal notices or board requests"),
        ("Smishing", "Phishing via SMS text", "'Your package is delayed, click here'"),
        ("Vishing", "Phishing via phone calls", "Fake bank calls asking for your PIN"),
        ("Clone Phishing", "Copies a real email, swaps link", "Identical to a previous real email"),
    ]
    for i, r in enumerate(types):
        pdf.table_row(r, w, fill=(i % 2 == 0))

    pdf.sub("2.4  What Happens When Someone Falls for It?")
    pdf.bullet("Credential theft: Attacker gets your username + password, accesses email, bank, social media")
    pdf.bullet("Malware installation: Spyware, ransomware, or remote access tools installed on your device")
    pdf.bullet("Financial loss: Direct money transfers or gift card codes redeemed instantly")
    pdf.bullet("Identity theft: Attackers open credit cards, file taxes, take loans in your name")
    pdf.bullet("Organizational breach: One click can compromise an entire company's network")

    pdf.sub("2.5  How Email Addresses Work (you WILL need to explain this)")
    pdf.body(
        "Many students don't understand email structure. Break it down:\n\n"
        "    john.smith  @  company  .  com\n"
        "    ----------     --------     ---\n"
        "    Username       Domain       Top-Level Domain\n\n"
        "The DOMAIN (after @) is what matters -- it tells you WHO controls that email server.\n"
        "support@paypal.com = PayPal controls it [REAL]\n"
        "support@paypal-security-update.com = Someone random registered it [FAKE]"
    )

    pdf.sub("2.6  How Hovering Over Links Works")
    pdf.bullet("Hover your mouse cursor over a link (without clicking) to see the actual destination URL")
    pdf.bullet("This appears as a tooltip near the cursor or at the bottom-left of the browser")
    pdf.bullet("The displayed text of a link can say ANYTHING -- only the hover URL tells the truth")
    pdf.tip_box("Live demo suggestion: Open any email, hover over a link, and show the class the real URL.")

    # ── SECTION 3: SLIDE-BY-SLIDE GUIDE ──
    pdf.add_page()
    pdf.sec_title("3", "SLIDE-BY-SLIDE TEACHING GUIDE")

    # Slide 1
    pdf.slide_header("1", "Title Slide -- Hook & Introduction", "2 min")
    pdf.label_body("What to say:",
        "Open with: 'How many of you have ever received a suspicious email or text?' "
        "(Hands go up.) 'How many weren't sure if it was real or fake?' (More hands.) "
        "'That's exactly what we're fixing today.'")
    pdf.label_body("Key points:",
        "Billions of phishing emails are sent daily -- this isn't rare. This isn't about being "
        "tech-savvy -- it's about awareness. Frame it: 'By the end of this, you'll spot scams in seconds.'")
    pdf.warning_box("Don't start with definitions -- start with the real-world hook. Don't SAY 'this is important' -- SHOW them why.")

    # Slide 2
    pdf.slide_header("2", "What is Phishing?", "3-4 min")
    pdf.label_body("What to say:",
        "'Imagine someone puts on a FedEx uniform, walks up to your door, and says they need "
        "your signature -- but there's no package. They just wanted you to open the door. "
        "That's phishing, but online.'")
    pdf.label_body("Key points:",
        "They impersonate someone you trust (bank, boss, Netflix). They're not hacking your "
        "computer -- they're hacking YOUR BRAIN. Walk through the 3 columns: who they pretend "
        "to be, what emotions they target, what they want.")
    pdf.label_body("Interaction:",
        "Ask: 'If I wanted to trick someone in this room, what company would I pretend to be?' "
        "Students will say Instagram, WhatsApp, Netflix. Use their answers: 'Exactly -- attackers "
        "pick whatever YOU trust.'")
    pdf.warning_box("Jargon to avoid: Don't say 'social engineering' (say 'tricking people'). Don't say 'threat actor' (say 'attacker' or 'scammer').")

    # Slide 3
    pdf.slide_header("3", "Red Flag #1: The Sense of Urgency", "3-4 min")
    pdf.label_body("What to say:",
        "'Here's rule number one: if a message makes you feel panicked, that panic IS the attack.'")
    pdf.label_body("Teaching approach:",
        "Read each example phrase on the slide OUT LOUD with dramatic urgency -- then pause: "
        "'Did your heart rate go up? That's the point.' Explain: urgency bypasses critical thinking. "
        "When you're scared, you act first and think later.")
    pdf.label_body("Analogy:",
        "'If your bank detected fraud, they would FREEZE your account automatically. They wouldn't "
        "send a panicked email saying fix this yourself in 12 hours or else.'")

    # Slide 4
    pdf.slide_header("4", "Red Flag #2: The Sender Address", "4-5 min")
    pdf.warning_box("THIS IS THE MOST TECHNICAL SLIDE. GO SLOW. This is the most important skill you'll teach.")
    pdf.label_body("What to say:",
        "'This takes 3 seconds and catches 90% of phishing emails.'")
    pdf.label_body("Teaching approach:",
        "1) Explain display name vs actual address. Display name = name tag (anyone can write anything). "
        "Actual address = driver's license (harder to fake).\n"
        "2) Walk through FAKE examples: paypa1 (number 1 vs letter l), extra subdomains, weird TLDs.\n"
        "3) Walk through REAL examples: clean, simple, official domains.\n"
        "4) Read the tip at the bottom.")
    pdf.label_body("Analogy:",
        "'paypal.com is like 123 Main Street -- the real address. paypal-security-update.com is "
        "like 123 Main Street But Actually a Different Building -- sounds related but is completely different.'")
    pdf.tip_box("Live demo: Open your email, show a legitimate sender address, then describe what a spoofed one would look like.")

    # Slide 5
    pdf.add_page()
    pdf.slide_header("5", "Red Flag #3: Suspicious Links & Attachments", "4-5 min")
    pdf.label_body("What to say:",
        "'Even if the email looks perfect -- the link is where the trap is set.'")
    pdf.label_body("Links (left side):",
        "Explain hovering: 'Rest your cursor on a link without clicking. A tooltip shows the real URL.' "
        "Walk through the example: button says 'update billing' but URL goes to a sketchy site. "
        "Cover: shortened URLs (bit.ly), misspellings, HTTP vs HTTPS.")
    pdf.label_body("Attachments (right side):",
        "Explain file extensions: 'The letters after the dot tell your computer what type of file it is.' "
        "Emphasize .exe (runs a program), double extensions (.pdf.scr), .zip, .docm. "
        "'If a stranger on the street handed you a USB drive, you'd say no. An email attachment is the same.'")
    pdf.label_body("Analogy:",
        "'A door with a sign saying Free Pizza Inside -- but through the window you see a dark alley. "
        "The sign can say anything. You need to look through the window first.'")
    pdf.tip_box("Practical rule: 'If unsure about a link, open a NEW browser tab, type the company's URL yourself. Never use the link in the email.'")

    # Slide 6
    pdf.slide_header("6", "Red Flag #4: Generic Greetings", "2-3 min")
    pdf.label_body("What to say:",
        "'If Netflix sends you an email, they know your name. If it says Dear Customer, "
        "ask: why don't they know who I am?'")
    pdf.label_body("Teaching approach:",
        "Quick walkthrough of suspicious vs legitimate greetings. Mass phishing campaigns send "
        "millions of emails -- they can't personalize every one. BUT add the caveat: spear phishing "
        "CAN use your real name, so a personal greeting doesn't guarantee safety.")
    pdf.info_box("KEEP IT BRIEF", "This is the simplest concept. Don't over-explain. Move to the game transition.")

    # Slide 7
    pdf.slide_header("7", "Transition to Game", "1-2 min")
    pdf.label_body("What to say:",
        "'Okay, enough theory. Let's see if you can actually catch a phisher in the wild. "
        "We're going to play Spot the Phish.'")
    pdf.label_body("How to set it up:",
        "Build energy! 'I'll show you 3 real-world scenarios. Your job: safe or scam?' "
        "Explain format: message -> study -> vote -> reveal. Encourage participation: "
        "'No wrong answers -- even falling for it is the point of learning.' "
        "Optional: split into teams for competition.")

    # Slides 8-9
    pdf.add_page()
    pdf.slide_header("8-9", "Scenario 1: The Fake Bank Alert", "4-5 min")
    pdf.label_body("How to facilitate:",
        "1) Display slide 8: 'Take 30 seconds to study this email.'\n"
        "2) Let them read silently.\n"
        "3) Ask: 'Raise your hand if you think this is a phish.' (Most hands should go up.)\n"
        "4) Ask: 'WHO can tell me specifically what gives it away?'\n"
        "5) Let 2-3 students answer, then move to the reveal (slide 9).")
    pdf.label_body("If students struggle:",
        "Prompt: 'Look at the sender address. Look at how they greet you. Look at the link.'")
    pdf.label_body("Reveal -- walk through each flag:",
        "1) Fake domain: 'chase-secure-update12.com is NOT chase.com -- someone made it up.'\n"
        "2) Generic greeting: 'Dear Customer -- Chase would use your real name.'\n"
        "3) Urgency: '12 hours or permanently locked -- panic-mode manipulation.'\n"
        "4) Suspicious link: 'bit.ly is a URL shortener. Chase would never use that.'")
    pdf.tip_box("Drive home: 'If worried it's real, open a new tab, type chase.com yourself. If there's a problem, you'll see it there.'")

    # Slides 10-11
    pdf.slide_header("10-11", "Scenario 2: The CEO Gift Card Fraud (SMS)", "4-5 min")
    pdf.label_body("How to facilitate:",
        "1) Display slide 10: 'You get this text from your boss. Read it.'\n"
        "2) Ask: 'How many of you would buy the gift cards?'\n"
        "3) Some may say yes (wanting to help) -- that's the point.\n"
        "4) Ask: 'Why might you hesitate?' Let discussion happen, then reveal.")
    pdf.label_body("If everyone says 'obviously a scam':",
        "Challenge them: 'What if it was your actual boss's name? What if you just started a new "
        "job? What if they said this is urgent and I'll remember who helped? Pressure changes things.'")
    pdf.label_body("Reveal -- 3 key points:",
        "1) Gift cards = scam currency: 'ANY time someone asks for gift cards and codes, it is a scam. "
        "100%. No exceptions. No business uses gift cards as payment.'\n"
        "2) 'I can't talk': 'Prevents you from calling to verify. If you call, the scam is over.'\n"
        "3) Unknown number: 'Not even from a saved contact.'")
    pdf.tip_box("Practical rule: 'If anyone asks for money via text -- call them on their saved number. A 2-minute delay never causes a real business problem.'")

    # Slides 12-13
    pdf.slide_header("12-13", "Scenario 3: The Package Delivery", "5-6 min")
    pdf.warning_box("This is the HARDEST scenario and your MOST IMPORTANT teaching moment. It looks very convincing.")
    pdf.label_body("How to facilitate:",
        "1) Display slide 12: 'This one's trickier. Uses your name. Sender looks real.'\n"
        "2) Point out: 'Hi John -- not Dear Customer. Sender is no-reply@fedex.com.'\n"
        "3) Ask: 'Is it safe?' Let them debate.\n"
        "4) If nobody catches it, point to attachment: 'Look at the filename. What does it end with?'")
    pdf.label_body("Reveal -- 3 critical points:",
        "1) The .exe file: 'This is a PROGRAM, not a document. Opens = malware installed. FedEx sends "
        "tracking numbers, not programs.'\n"
        "2) Sender spoofing (NEW concept): 'Attackers can FAKE the From address. Like writing a fake "
        "return address on a letter -- the post office doesn't verify it.'\n"
        "3) Ultimate defense: 'The sender CAN be faked. Your name CAN be used. But the actual link URL "
        "and file extension never lie. Those are your ultimate defense.'")
    pdf.label_body("Closing statement:",
        "'Your ultimate defense is always the link and the attachment. When everything else looks "
        "perfect, those are the two things you can always verify. Thank you for participating!'")

    # ── SECTION 4: RUNNING THE GAME ──
    pdf.add_page()
    pdf.sec_title("4", "RUNNING THE 'SPOT THE PHISH' GAME")

    pdf.sub("4.1  Game Flow")
    pdf.body(
        "Question Slide --> 30 sec silent reading --> Ask 'Safe or Scam?' --> "
        "Discussion (2-3 students) --> Reveal Slide --> Walk through red flags"
    )

    pdf.sub("4.2  Engagement Techniques")
    w4 = [40, 145]
    pdf.table_header(["Technique", "How To Do It"], w4)
    techniques = [
        ("Hand Raise Vote", "'Raise hand if SAFE... now raise hand if SCAM'"),
        ("Think-Pair-Share", "'Turn to your neighbor, discuss 30 seconds, then share'"),
        ("Points / Teams", "Split room into 2 teams, award points per correct red flag"),
        ("Cold Calling", "'I saw your hand -- tell us what you noticed' (keep it friendly)"),
        ("Build Suspense", "Pause before reveal: 'Are you SURE...?'"),
    ]
    for i, r in enumerate(techniques):
        pdf.table_row(r, w4, fill=(i % 2 == 0))

    pdf.sub("4.3  If the Room Is Quiet")
    pdf.bullet("Don't wait too long -- awkward silence kills energy")
    pdf.bullet("Give a specific prompt: 'Look at the sender address. What do you notice?'")
    pdf.bullet("Share your own reaction: 'I almost thought this was real too. Here's what I missed...'")

    pdf.sub("4.4  If Students Disagree")
    pdf.bullet("Great! Let them debate briefly, then reveal")
    pdf.bullet("'Both sides had good reasoning. Let's see who's right...'")

    # ── SECTION 5: Q&A ──
    pdf.add_page()
    pdf.sec_title("5", "ANTICIPATED QUESTIONS & ANSWERS")

    pdf.sub("5.1  Basic Questions")
    pdf.qa_item(
        "What should I do if I accidentally clicked a phishing link?",
        "Don't panic. (1) Don't enter any info on the page -- close it. (2) Change your password "
        "for the account the email pretended to be from. (3) Run antivirus. (4) If work email, "
        "report to IT immediately. (5) Monitor accounts for unusual activity."
    )
    pdf.qa_item(
        "Can I get hacked just by opening an email?",
        "Generally no -- just reading is safe in modern email clients. The danger is clicking "
        "links and opening attachments. But keep software updated to patch vulnerabilities."
    )
    pdf.qa_item(
        "Is Gmail/Yahoo safer than other email?",
        "Major providers have strong phishing filters, but no filter is perfect. Phishing emails "
        "still get through daily. Filters are a safety net, not a guarantee."
    )
    pdf.qa_item(
        "How do scammers get my email address?",
        "Data breaches, public social media profiles, buying lists, guessing common formats "
        "(firstname.lastname@gmail.com), or scraping websites."
    )
    pdf.qa_item(
        "What if I'm on my phone and can't hover?",
        "Long-press (press and hold) the link. A preview pops up showing the real URL. If "
        "suspicious, don't open. Better yet, open the company's app directly."
    )

    pdf.sub("5.2  Intermediate Questions")
    pdf.qa_item(
        "What about phishing on social media or WhatsApp?",
        "Same rules apply. If a 'friend' sends a link with 'OMG is this you in this video??' "
        "-- their account may be hacked. Verify with them directly."
    )
    pdf.qa_item(
        "Can antivirus software protect me?",
        "It helps but isn't foolproof. It catches malware in attachments but can't stop you from "
        "typing your password into a fake website. Your brain is your best antivirus."
    )
    pdf.qa_item(
        "What is two-factor authentication (2FA)?",
        "A second login step -- like a code sent to your phone. Even if your password is stolen, "
        "they can't log in without the second factor. Highly recommended for all important accounts."
    )
    pdf.qa_item(
        "Are there phishing attempts via phone calls?",
        "Yes -- called 'vishing' (voice phishing). Fake bank, IRS, or tech support calls. Same "
        "rules: if they pressure you, hang up and call the company using their official number."
    )

    pdf.sub("5.3  Advanced Questions (if they come up)")
    pdf.qa_item(
        "How do attackers spoof email addresses?",
        "Email protocols (SMTP) were designed in the 1980s without authentication. The 'From' field "
        "is just text -- like a return address on a letter. Modern protections (SPF, DKIM, DMARC) "
        "help verify senders, but not all organizations have them configured."
    )
    pdf.qa_item(
        "What is ransomware?",
        "Malware that encrypts your files and demands payment (usually cryptocurrency) to unlock "
        "them. Often delivered via phishing attachments. Even if you pay, no guarantee of recovery."
    )

    # ── SECTION 6: MISCONCEPTIONS ──
    pdf.add_page()
    pdf.sec_title("6", "COMMON STUDENT MISCONCEPTIONS")

    pdf.body("Address these proactively or when they come up during the session:")
    pdf.ln(2)

    w6 = [60, 125]
    pdf.table_header(["Misconception", "Reality"], w6)
    misconceptions = [
        ("'I have nothing worth stealing'",
         "Your email can attack others. Your identity = credit cards, loans. Your PC = botnet."),
        ("'I'd never fall for that'",
         "Overconfidence is dangerous. These examples are obvious because we're studying them."),
        ("'My antivirus will catch it'",
         "Antivirus catches malware, not you typing your password into a fake website."),
        ("'Only old people fall for scams'",
         "Studies show 18-25 year olds fall for phishing at HIGHER rates (overconfidence)."),
        ("'If it uses HTTPS, it's safe'",
         "HTTPS = encrypted connection, NOT legitimate website. Attackers get HTTPS too."),
        ("'My company IT will protect me'",
         "IT filters catch most, but sophisticated attacks get through. You're the last defense."),
    ]
    for i, r in enumerate(misconceptions):
        pdf.table_row(r, w6, fill=(i % 2 == 0))

    # ── SECTION 7: STATS ──
    pdf.sec_title("7", "REAL-WORLD STATS TO DROP CASUALLY")

    pdf.body("Pick 3-4 that feel relevant in the moment. Don't list them all -- weave them naturally:")
    pdf.ln(1)
    stats = [
        "3.4 billion phishing emails are sent every single day worldwide",
        "91% of all cyberattacks start with a phishing email",
        "Average cost of a data breach in 2024: $4.88 million",
        "It takes an average of 194 days for a company to identify a breach",
        "1 in 3 employees click a phishing link in simulated tests",
        "Google blocks ~100 million phishing emails per day on Gmail alone",
        "FBI's IC3: $12.5 billion in cybercrime losses in 2023, phishing = #1 crime",
        "A single phishing email led to the 2016 DNC hack (affected U.S. election)",
        "Colonial Pipeline ransomware (2021): one compromised password caused gas shortages across U.S. East Coast",
    ]
    for s in stats:
        pdf.bullet(s)

    # ── SECTION 8: ANALOGIES ──
    pdf.add_page()
    pdf.sec_title("8", "ANALOGIES CHEAT SHEET")

    pdf.body("When a student looks confused, reach for an analogy:")
    pdf.ln(2)

    w8 = [42, 143]
    pdf.table_header(["Concept", "Analogy"], w8)
    analogies = [
        ("Phishing", "A con artist in a FedEx uniform at your door. They look real, but aren't."),
        ("Urgency tactics", "A street scammer yelling 'deal ends in 10 seconds!' -- decide before you think."),
        ("Fake sender", "Caller ID shows 'City Hospital' but it's a telemarketer who faked the number."),
        ("Hovering over links", "Checking the peephole before opening the door. Look before you open."),
        ("Malicious attachments", "A stranger handing you a USB: 'plug this in.' You'd say no in person."),
        ("Generic greetings", "A letter saying 'Dear Resident' -- clearly mass mail, not personal."),
        ("Spoofing", "Fake return address on an envelope. The post office doesn't verify it."),
        ("Gift card scams", "Gift cards are like cash -- once codes are shared, money is gone forever."),
        ("HTTPS on phish sites", "A burglar wearing a seatbelt. The seatbelt is real, driver is a criminal."),
        ("Two-factor auth", "A second lock on your door. Even if key is copied, they still can't enter."),
    ]
    for i, r in enumerate(analogies):
        pdf.table_row(r, w8, fill=(i % 2 == 0))

    # ── SECTION 9: TIMING ──
    pdf.sec_title("9", "TIMING GUIDE")

    w9 = [25, 16, 55, 75]
    pdf.table_header(["Time", "Slide", "Section", "Presenter Action"], w9)
    timeline = [
        ("0:00-2:00", "1", "Title & Hook", "Ask: 'Who got a suspicious email?'"),
        ("2:00-6:00", "2", "What is Phishing?", "FedEx analogy, walk 3 columns"),
        ("6:00-10:00", "3", "Red Flag #1: Urgency", "Read examples aloud dramatically"),
        ("10:00-15:00", "4", "Red Flag #2: Sender", "GO SLOW -- explain @ domains"),
        ("15:00-20:00", "5", "Red Flag #3: Links", "Demo hovering, file extensions"),
        ("20:00-23:00", "6", "Red Flag #4: Greetings", "Quick -- simple concept"),
        ("23:00-25:00", "7", "Game Transition", "Build energy, explain rules"),
        ("25:00-28:00", "8", "Scenario 1: Question", "30s reading, hand raise vote"),
        ("28:00-30:00", "9", "Scenario 1: Reveal", "Walk through 4 red flags"),
        ("30:00-33:00", "10", "Scenario 2: Question", "'Would you buy gift cards?'"),
        ("33:00-35:00", "11", "Scenario 2: Reveal", "Gift cards = scam currency"),
        ("35:00-38:00", "12", "Scenario 3: Question", "Hardest one -- let them debate"),
        ("38:00-41:00", "13", "Scenario 3: Reveal", "Spoofing + .exe malware danger"),
        ("41:00-45:00", "--", "Q&A + Closing", "Open floor, share action items"),
    ]
    for i, r in enumerate(timeline):
        pdf.table_row(r, w9, fill=(i % 2 == 0))

    pdf.info_box("TIMING TIP",
        "Running short? Cut Q&A -- never rush the game. "
        "Running long? Shorten slides 3-6; red flags get reinforced during the game.")

    # ── SECTION 10: POST-SESSION ──
    pdf.add_page()
    pdf.sec_title("10", "POST-SESSION CHECKLIST")

    pdf.sub("10.1  Actions to Recommend to Students (TODAY)")
    pdf.bullet("Enable 2FA on email, bank, and social media accounts")
    pdf.bullet("Check recent emails -- look at sender addresses they never checked before")
    pdf.bullet("Update devices -- OS, browser, and apps")
    pdf.bullet("Set up a password manager -- stop reusing passwords")
    pdf.bullet("Tell one other person what they learned -- teaching reinforces learning")

    pdf.sub("10.2  Quick Summary (Leave on Screen or Share)")
    pdf.info_box("THE 4 RED FLAGS OF PHISHING",
        "1) Creates urgency or panic\n"
        "2) Suspicious sender address (check domain after @)\n"
        "3) Suspicious links (hover first!) or unexpected attachments\n"
        "4) Generic greeting ('Dear Customer')\n\n"
        "When in doubt: Don't click. Don't download. Don't reply.\n"
        "Instead: Verify through a separate, known channel.")

    # ── FINAL NOTE ──
    pdf.ln(6)
    pdf.set_draw_color(0, 180, 220)
    pdf.set_line_width(0.5)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(0, 150, 200)
    pdf.cell(0, 8, "FINAL NOTE TO THE INSTRUCTOR", align="C", ln=True)
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6,
        "    You don't need to be a cybersecurity expert to teach this effectively.\n"
        "    You need to be:\n\n"
        "      1. PREPARED    -- you've read this guide\n"
        "      2. RELATABLE   -- you talk like a human, not a textbook\n"
        "      3. PATIENT     -- you let students discover red flags before telling them\n"
        "      4. HONEST      -- you admit that even you could be fooled\n\n"
        "    The most powerful moment will be when a student says 'Wait, I think I got one\n"
        "    of those emails last week...' -- that's when you know it clicked.\n\n"
        "    Good luck. You've got this."
    )

    pdf.ln(8)
    pdf.set_draw_color(0, 180, 220)
    pdf.set_line_width(0.5)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 150, 200)
    pdf.cell(0, 8, "Anonymous SDMCET - Cybersecurity Club", align="C", ln=True)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(130, 130, 130)
    pdf.cell(0, 6, "Empowering students to stay safe in the digital world.", align="C", ln=True)

    # Save
    output = os.path.join(os.path.dirname(__file__), "..",
                          "Phishing_Awareness_Teaching_Guide.pdf")
    output = os.path.abspath(output)
    pdf.output(output)
    print(f"[OK] Teaching Guide PDF saved to: {output}")
    print(f"     {pdf.page_no()} pages generated")


if __name__ == "__main__":
    build_pdf()
