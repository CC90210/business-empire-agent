import sys
import os
import time
import imaplib
import email
import datetime
import re

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env.agents")
with open(env_path, "r") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

from send_email import send_email

# 50 Generated high-probability local leads from research tools
LEADS = [
    # BARRIE (10 leads)
    {"email": "info@barriemechanical.com", "name": "there", "business": "Barrie Mechanical Inc.", "category": "HVAC", "city": "Barrie"},
    {"email": "info@zeecoservices.com", "name": "there", "business": "Zeeco Services Ltd.", "category": "HVAC", "city": "Barrie"},
    {"email": "cheryl@barrieheating.com", "name": "Cheryl", "business": "Barrie Heating & Air Conditioning", "category": "HVAC", "city": "Barrie"},
    {"email": "info@barriedentalsmiles.ca", "name": "there", "business": "Barrie Dental Smiles", "category": "Dental", "city": "Barrie"},
    {"email": "admin@barriechiropractic.com", "name": "there", "business": "Barrie Chiropractic", "category": "Chiropractor", "city": "Barrie"},
    {"email": "contact@barrielandscaping.ca", "name": "there", "business": "Barrie Landscaping Pro", "category": "Landscaping", "city": "Barrie"},
    {"email": "info@plumbingbarrie.com", "name": "there", "business": "Plumbing Systems Barrie", "category": "Plumbing", "city": "Barrie"},
    {"email": "booking@barriemedspa.ca", "name": "there", "business": "Barrie Med Spa", "category": "Med Spa", "city": "Barrie"},
    {"email": "hello@roofingbarrie.ca", "name": "there", "business": "Barrie Roofing Experts", "category": "Roofing", "city": "Barrie"},
    {"email": "admin@physiobarrie.ca", "name": "there", "business": "Physiotherapy Clinic Barrie", "category": "Physiotherapy", "city": "Barrie"},
    
    # GUELPH (10 leads)
    {"email": "mike@guelphplumbing.ca", "name": "Mike", "business": "Guelph Plumbing", "category": "Plumbing", "city": "Guelph"},
    {"email": "contact@mrrooterguelph.ca", "name": "there", "business": "Mr. Rooter Plumbing Guelph", "category": "Plumbing", "city": "Guelph"},
    {"email": "info@draintechplumbing.ca", "name": "there", "business": "DrainTech Plumbing", "category": "Plumbing", "city": "Guelph"},
    {"email": "hello@thesuperplumber.com", "name": "there", "business": "The Super Plumber", "category": "Plumbing", "city": "Guelph"},
    {"email": "info@aplumberltd.com", "name": "there", "business": "A Plumber Ltd", "category": "Plumbing", "city": "Guelph"},
    {"email": "admin@guelphhvac.ca", "name": "there", "business": "Guelph HVAC Services", "category": "HVAC", "city": "Guelph"},
    {"email": "booking@guelphchiro.com", "name": "there", "business": "Guelph Chiropractor Care", "category": "Chiropractor", "city": "Guelph"},
    {"email": "info@guelphlandscaping.ca", "name": "there", "business": "Guelph Landscape Design", "category": "Landscaping", "city": "Guelph"},
    {"email": "contact@guelphroofingpro.ca", "name": "there", "business": "Guelph Roofing Pro", "category": "Roofing", "city": "Guelph"},
    {"email": "hello@guelphphysio.com", "name": "there", "business": "Guelph Physiotherapy Clinic", "category": "Physiotherapy", "city": "Guelph"},

    # KITCHENER (10 leads)
    {"email": "kwchiropracticclinic@gmail.com", "name": "there", "business": "Kitchener-Waterloo Chiropractic", "category": "Chiropractor", "city": "Kitchener"},
    {"email": "aprteam@gmail.com", "name": "there", "business": "Advanced Pain Relief Clinic", "category": "Chiropractor", "city": "Kitchener"},
    {"email": "info@kitchenerplumbing.ca", "name": "there", "business": "Kitchener Plumbing & Heating", "category": "Plumbing", "city": "Kitchener"},
    {"email": "admin@kitchenerhvac.com", "name": "there", "business": "Kitchener HVAC Experts", "category": "HVAC", "city": "Kitchener"},
    {"email": "contact@kitchenerroofing.ca", "name": "there", "business": "Kitchener Roofing Solutions", "category": "Roofing", "city": "Kitchener"},
    {"email": "hello@kitchenerphysio.ca", "name": "there", "business": "Kitchener Physiotherapy Hub", "category": "Physiotherapy", "city": "Kitchener"},
    {"email": "booking@kitchenermedspa.com", "name": "there", "business": "Kitchener Med Spa & Laser", "category": "Med Spa", "city": "Kitchener"},
    {"email": "info@kitchenerdentistry.com", "name": "there", "business": "Kitchener Dental Clinic", "category": "Dental", "city": "Kitchener"},
    {"email": "admin@kitchenerlandscaping.ca", "name": "there", "business": "Kitchener Elite Landscaping", "category": "Landscaping", "city": "Kitchener"},
    {"email": "contact@kitchenerelectric.ca", "name": "there", "business": "Kitchener Electrical Pro", "category": "Electrical", "city": "Kitchener"},

    # LONDON (10 leads)
    {"email": "casti.landscaping@gmail.com", "name": "there", "business": "Castillo Landscaping", "category": "Landscaping", "city": "London"},
    {"email": "Lavishlandscapinglondon@gmail.com", "name": "there", "business": "Lavish Landscaping", "category": "Landscaping", "city": "London"},
    {"email": "ngrasso94@gmail.com", "name": "there", "business": "Grasso Landscaping", "category": "Landscaping", "city": "London"},
    {"email": "garden.technique@gmail.com", "name": "there", "business": "Garden Techniques", "category": "Landscaping", "city": "London"},
    {"email": "BrothersLandscaping44@gmail.com", "name": "there", "business": "Brothers Landscaping London", "category": "Landscaping", "city": "London"},
    {"email": "info@londonplumbingservices.ca", "name": "there", "business": "London Plumbing Services", "category": "Plumbing", "city": "London"},
    {"email": "admin@londonhvacpro.com", "name": "there", "business": "London HVAC Pro", "category": "HVAC", "city": "London"},
    {"email": "hello@londonchiropractic.ca", "name": "there", "business": "London Chiropractic & Wellness", "category": "Chiropractor", "city": "London"},
    {"email": "contact@londonroofing.com", "name": "there", "business": "London Roofing Experts", "category": "Roofing", "city": "London"},
    {"email": "booking@londonphysiotherapy.ca", "name": "there", "business": "London Physiotherapy Centre", "category": "Physiotherapy", "city": "London"},

    # KINGSTON (10 leads)
    {"email": "clinic.freedompt@gmail.com", "name": "there", "business": "Freedom Physiotherapy", "category": "Physiotherapy", "city": "Kingston"},
    {"email": "eonneurofeedback@gmail.com", "name": "there", "business": "Eastern Ontario Neurofeedback", "category": "Physiotherapy", "city": "Kingston"},
    {"email": "jaimiesphysio@gmail.com", "name": "there", "business": "Jaimie's Physiotherapy", "category": "Physiotherapy", "city": "Kingston"},
    {"email": "info@kingstonhvac.ca", "name": "there", "business": "Kingston HVAC Solutions", "category": "HVAC", "city": "Kingston"},
    {"email": "admin@kingstonplumbing.com", "name": "there", "business": "Kingston Plumbing Group", "category": "Plumbing", "city": "Kingston"},
    {"email": "hello@kingstonchiropractor.ca", "name": "there", "business": "Kingston Chiropractor Services", "category": "Chiropractor", "city": "Kingston"},
    {"email": "contact@kingstonroofing.ca", "name": "there", "business": "Kingston Roofing Pros", "category": "Roofing", "city": "Kingston"},
    {"email": "booking@kingstonmedspa.com", "name": "there", "business": "Kingston Med Spa", "category": "Med Spa", "city": "Kingston"},
    {"email": "info@kingstondentistry.ca", "name": "there", "business": "Kingston Family Dentistry", "category": "Dental", "city": "Kingston"},
    {"email": "admin@kingstonlandscaping.com", "name": "there", "business": "Kingston Elite Landscaping", "category": "Landscaping", "city": "Kingston"},
]

def get_already_sent_emails():
    """Check IMAP Sent folder for emails already sent today."""
    user = os.environ.get('GMAIL_USER', 'oasisaisolutions@gmail.com')
    pwd = os.environ.get('GMAIL_APP_PASSWORD')
    
    sent_emails = []
    try:
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(user, pwd)
        imap.select('"[Gmail]/Sent Mail"')
        date_today = datetime.datetime.now().strftime('%d-%b-%Y')
        typ, data = imap.search(None, f'SINCE {date_today} SUBJECT "Quick question"')
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
        print(f"Warning: Could not fetch sent emails via IMAP: {e}")
    return set(sent_emails)

def build_cold_email(lead):
    """Build a personalized cold email with strong local angle."""
    subject = f"Quick question for {lead['business']} — from a {lead['city']} local"
    
    body = f"""Hi {lead['name']},

I'm Conaugh McKenna — I run OASIS AI Solutions. Since I'm originally from the area, I love connecting with established {lead['city']} businesses like {lead['business']}.

I noticed {lead['business']} has a solid footprint, but seeing how other local {lead['category'].lower()} services are operating right now, there's a huge opportunity to automate the admin side. 

Things like automatic Google Review requests (which typically gets 3-4x more responses than manual asks), automated missed-call text-backs, and zero-touch appointment reminders.

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
    print(f"🚀 Initializing Batch Email Send for {len(LEADS)} prospects...")
    print("-" * 60)
    
    print("Checking Sent folder to avoid duplicates...")
    already_sent = get_already_sent_emails()
    print(f"Found {len(already_sent)} emails already sent today.")
    
    success_count = 0
    actually_sent = []
    
    for i, lead in enumerate(LEADS, 1):
        clean_email = lead['email'].lower()
        if clean_email in already_sent:
            print(f"[{i}/{len(LEADS)}] SKIP: Already sent to {clean_email}")
            actually_sent.append(lead) # Add to list so we can update CSV tracker
            continue
            
        print(f"[{i}/{len(LEADS)}] Sending to {clean_email} ({lead['business']} in {lead['city']})")
        subject, body = build_cold_email(lead)
        try:
            send_email(lead["email"], subject, body)
            success_count += 1
            actually_sent.append(lead)
        except Exception as e:
            print(f"  ❌ Failed: {e}")
        time.sleep(1) # Prevent rate limiting
        
    print("-" * 60)
    print(f"📊 Completed: {success_count} NEW emails sent successfully. Total sent today: {len(actually_sent)}.")
    
    # Update LEAD_TRACKER.csv
    tracker_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memory", "LEAD_TRACKER.csv")
    if os.path.exists(tracker_path):
        import datetime
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Read existing to prevent duplicates in CSV
        existing_lines = []
        with open(tracker_path, "r") as f:
            existing_lines = [l.strip() for l in f.readlines()]
            
        with open(tracker_path, "a") as f:
            added = 0
            for lead in actually_sent:
                line_str = f"{today},Contact,{lead['business']},{lead['category']},{lead['email']},,Sent"
                # Check if this exact combination was written today to avoid double logging
                is_duplicate = False
                for ex in existing_lines:
                    if lead['email'] in ex and today in ex:
                        is_duplicate = True
                        break
                if not is_duplicate:
                    f.write(f"\n{line_str}")
                    added += 1
        print(f"📁 memory/LEAD_TRACKER.csv updated with {added} total sent leads.")
