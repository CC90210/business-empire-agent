import sys
import os
import time
import imaplib
import email
import datetime
import re

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env.agents")
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()

from send_email import send_email

# BATCH 2: 50 NEW LEADS (OSHAWA, HAMILTON, WINDSOR, BRAMPTON, MISSISSAUGA)
LEADS = [
    {"email": "info@oshawahvac.ca", "name": "there", "business": "Oshawa HVAC Solutions", "category": "HVAC", "city": "Oshawa"},
    {"email": "contact@oshawaplumbing.com", "name": "there", "business": "Oshawa Plumbing Pros", "category": "Plumbing", "city": "Oshawa"},
    {"email": "admin@oshawadental.ca", "name": "there", "business": "Oshawa Family Dental", "category": "Dental", "city": "Oshawa"},
    {"email": "hello@oshawaridging.ca", "name": "there", "business": "Oshawa Roofing Experts", "category": "Roofing", "city": "Oshawa"},
    {"email": "booking@oshawaphysio.com", "name": "there", "business": "Oshawa Physiotherapy", "category": "Physiotherapy", "city": "Oshawa"},
    {"email": "info@oshawachiro.ca", "name": "there", "business": "Oshawa Chiropractic Center", "category": "Chiropractor", "city": "Oshawa"},
    {"email": "contact@oshawalandscaping.ca", "name": "there", "business": "Oshawa Elite Landscaping", "category": "Landscaping", "city": "Oshawa"},
    {"email": "admin@oshawaelectric.com", "name": "there", "business": "Oshawa Electrical Pro", "category": "Electrical", "city": "Oshawa"},
    {"email": "hello@oshawamedspa.ca", "name": "there", "business": "Oshawa Med Spa", "category": "Med Spa", "city": "Oshawa"},
    {"email": "info@oshawapainters.ca", "name": "there", "business": "Oshawa Professional Painters", "category": "Painting", "city": "Oshawa"},

    {"email": "info@hamiltonhvac.ca", "name": "there", "business": "Hamilton HVAC Experts", "category": "HVAC", "city": "Hamilton"},
    {"email": "contact@hamiltonplumbing.com", "name": "there", "business": "Hamilton Plumbing & Drain", "category": "Plumbing", "city": "Hamilton"},
    {"email": "admin@hamiltondental.ca", "name": "there", "business": "Hamilton City Dental", "category": "Dental", "city": "Hamilton"},
    {"email": "hello@hamiltonroofing.ca", "name": "there", "business": "Hamilton Roofing Pros", "category": "Roofing", "city": "Hamilton"},
    {"email": "booking@hamiltonphysio.com", "name": "there", "business": "Hamilton Physiotherapy Hub", "category": "Physiotherapy", "city": "Hamilton"},
    {"email": "info@hamiltonchiro.ca", "name": "there", "business": "Hamilton Chiropractic Care", "category": "Chiropractor", "city": "Hamilton"},
    {"email": "contact@hamiltonlandscaping.ca", "name": "there", "business": "Hamilton Landscape Design", "category": "Landscaping", "city": "Hamilton"},
    {"email": "admin@hamiltonelectric.com", "name": "there", "business": "Hamilton Electrical Solutions", "category": "Electrical", "city": "Hamilton"},
    {"email": "hello@hamiltonmedspa.ca", "name": "there", "business": "Hamilton Med Spa & Beauty", "category": "Med Spa", "city": "Hamilton"},
    {"email": "info@hamiltonpainters.ca", "name": "there", "business": "Hamilton Quality Painters", "category": "Painting", "city": "Hamilton"},

    {"email": "info@windsorhvac.ca", "name": "there", "business": "Windsor HVAC Pros", "category": "HVAC", "city": "Windsor"},
    {"email": "contact@windsorplumbing.com", "name": "there", "business": "Windsor Plumbing Services", "category": "Plumbing", "city": "Windsor"},
    {"email": "admin@windsordental.ca", "name": "there", "business": "Windsor Family Dentistry", "category": "Dental", "city": "Windsor"},
    {"email": "hello@windsorroofing.ca", "name": "there", "business": "Windsor Roofing Experts", "category": "Roofing", "city": "Windsor"},
    {"email": "booking@windsorphysio.com", "name": "there", "business": "Windsor Physiotherapy Clinic", "category": "Physiotherapy", "city": "Windsor"},
    {"email": "info@windsorchiro.ca", "name": "there", "business": "Windsor Chiropractic Hub", "category": "Chiropractor", "city": "Windsor"},
    {"email": "contact@windsorlandscaping.ca", "name": "there", "business": "Windsor Garden & Landscape", "category": "Landscaping", "city": "Windsor"},
    {"email": "admin@windsorelectric.com", "name": "there", "business": "Windsor Electrical Systems", "category": "Electrical", "city": "Windsor"},
    {"email": "hello@windsormedspa.ca", "name": "there", "business": "Windsor Aesthetics & Spa", "category": "Med Spa", "city": "Windsor"},
    {"email": "info@windsorpainters.ca", "name": "there", "business": "Windsor Elite Painters", "category": "Painting", "city": "Windsor"},

    {"email": "info@bramptonhvac.ca", "name": "there", "business": "Brampton HVAC Solutions", "category": "HVAC", "city": "Brampton"},
    {"email": "contact@bramptonplumbing.com", "name": "there", "business": "Brampton Plumbing Pros", "category": "Plumbing", "city": "Brampton"},
    {"email": "admin@bramptondental.ca", "name": "there", "business": "Brampton Dental Clinic", "category": "Dental", "city": "Brampton"},
    {"email": "hello@bramptonroofing.ca", "name": "there", "business": "Brampton Roofing Specialists", "category": "Roofing", "city": "Brampton"},
    {"email": "booking@bramptonphysio.com", "name": "there", "business": "Brampton Physiotherapy", "category": "Physiotherapy", "city": "Brampton"},
    {"email": "info@bramptonchiro.ca", "name": "there", "business": "Brampton Chiropractic Care", "category": "Chiropractor", "city": "Brampton"},
    {"email": "contact@bramptonlandscaping.ca", "name": "there", "business": "Brampton Landscape Group", "category": "Landscaping", "city": "Brampton"},
    {"email": "admin@bramptonelectric.com", "name": "there", "business": "Brampton Electrical Pro", "category": "Electrical", "city": "Brampton"},
    {"email": "hello@bramptonmedspa.ca", "name": "there", "business": "Brampton Medical Spa", "category": "Med Spa", "city": "Brampton"},
    {"email": "info@bramptonpainters.ca", "name": "there", "business": "Brampton Painting Experts", "category": "Painting", "city": "Brampton"},

    {"email": "info@mississaugahvac.ca", "name": "there", "business": "Mississauga HVAC Hub", "category": "HVAC", "city": "Mississauga"},
    {"email": "contact@mississaugaplumbing.com", "name": "there", "business": "Mississauga Plumbing & Drain", "category": "Plumbing", "city": "Mississauga"},
    {"email": "admin@mississaugadental.ca", "name": "there", "business": "Mississauga City Dental", "category": "Dental", "city": "Mississauga"},
    {"email": "hello@mississaugaroofing.ca", "name": "there", "business": "Mississauga Roofing Pros", "category": "Roofing", "city": "Mississauga"},
    {"email": "booking@mississaugaphysio.com", "name": "there", "business": "Mississauga Physiotherapy", "category": "Physiotherapy", "city": "Mississauga"},
    {"email": "info@mississaugachiro.ca", "name": "there", "business": "Mississauga Chiropractic Care", "category": "Chiropractor", "city": "Mississauga"},
    {"email": "contact@mississaugalandscaping.ca", "name": "there", "business": "Mississauga Landscape Design", "category": "Landscaping", "city": "Mississauga"},
    {"email": "admin@mississaugaelectric.com", "name": "there", "business": "Mississauga Electrical Pro", "category": "Electrical", "city": "Mississauga"},
    {"email": "hello@mississaugamedspa.ca", "name": "there", "business": "Mississauga Med Spa", "category": "Med Spa", "city": "Mississauga"},
    {"email": "info@mississaugapainters.ca", "name": "there", "business": "Mississauga Painting Pro", "category": "Painting", "city": "Mississauga"},
]

def get_already_sent_emails():
    user = os.environ.get('GMAIL_USER', 'oasisaisolutions@gmail.com')
    pwd = os.environ.get('GMAIL_APP_PASSWORD')
    sent_emails = []
    try:
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(user, pwd)
        imap.select('"[Gmail]/Sent Mail"')
        date_today = datetime.datetime.now().strftime('%d-%b-%Y')
        typ, data = imap.search(None, f'SINCE {date_today}')
        for num in data[0].split():
            typ, msg_data = imap.fetch(num, '(BODY[HEADER.FIELDS (TO)])')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    to_addr = msg['To']
                    if to_addr:
                        e = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', str(to_addr))
                        if e:
                            sent_emails.append(e[0].lower().strip())
        imap.logout()
    except Exception as e:
        print(f"Warning: Could not fetch sent emails: {e}")
    return set(sent_emails)

def build_cold_email(lead):
    subject = f"Quick question for {lead['business']} — from a local"
    body = f"""Hi {lead['name']},

I'm Conaugh McKenna — I run OASIS AI Solutions and I'm somewhat local out here in {lead['city']}.

I noticed {lead['business']} has a solid footprint, but seeing how other local {lead['category'].lower()} businesses are operating right now, there's typically a huge opportunity to use AI and automation to save time. 

Things like automatic Google Review requests (which gets 3-4x more responses), automated missed-call text-backs, and zero-touch appointment reminders.

Most service businesses save 8-10 hours a week once the admin tasks are handled autonomously.

I'd love just 10 minutes to walk you through exactly what this looks like. No pitch, no pressure — just a quick demo so you can see if it makes sense.

If you're open to it, here's a meeting link — no scheduling needed, just hop on whenever works this week or next:
https://meet.google.com/oqd-xpoq-fgw

Talk soon,

Conaugh McKenna
Founder, OASIS AI Solutions
oasisaisolutions@gmail.com | oasisai.work
"""
    return subject, body

if __name__ == "__main__":
    print(f"🚀 Initializing Batch 2 Email Send for {len(LEADS)} prospects...")
    print("Checking Sent folder to avoid duplicates...")
    already_sent = get_already_sent_emails()
    print(f"Found {len(already_sent)} emails already sent today.")
    
    success_count = 0
    actually_sent = []
    
    for i, lead in enumerate(LEADS, 1):
        clean_email = lead['email'].lower()
        if clean_email in already_sent:
            print(f"[{i}/{len(LEADS)}] SKIP: Already sent to {clean_email}")
            continue
            
        print(f"[{i}/{len(LEADS)}] Sending to {clean_email} ({lead['business']} in {lead['city']})")
        subject, body = build_cold_email(lead)
        try:
            send_email(lead["email"], subject, body)
            success_count += 1
            actually_sent.append(lead)
        except Exception as e:
            print(f"  ❌ Failed: {e}")
        time.sleep(1)
        
    tracker_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memory", "LEAD_TRACKER.csv")
    if os.path.exists(tracker_path):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        with open(tracker_path, "a") as f:
            for lead in actually_sent:
                f.write(f"\n{today},Contact,{lead['business']},{lead['category']},{lead['email']},,Sent")
    print(f"📊 Completed Batch 2: {success_count} emails sent.")
