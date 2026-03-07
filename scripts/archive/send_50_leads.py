import sys
import os
import re
import json
import time

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env.agents")
with open(env_path, "r") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

from outreach_engine import send_outreach
from duckduckgo_search import DDGS

CITIES = ["Barrie", "Kitchener", "London", "Guelph", "Kingston", "Brampton", "Mississauga", "Oakville", "Hamilton", "Sudbury"]
NICHES = [
    ("HVAC", "HVAC"),
    ("Plumber", "Plumbing"),
    ("Roofing", "Roofing"),
    ("Physiotherapy", "Physiotherapy"),
    ("Chiropractor", "Chiropractic"),
]
leads = []
seen_emails = set()

def extract_emails(text):
    return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

print("Starting to scrape 50 leads...")
ddgs = DDGS()
count = 0
for city in CITIES:
    for search_term, category in NICHES:
        if count >= 50: break
        query = f'{search_term} {city} Ontario "@gmail.com" OR "@hotmail.com"'
        try:
            results = list(ddgs.text(query, max_results=3))
            for r in results:
                snippet = (r.get('title', '') + " " + r.get('body', '')).lower()
                emails = extract_emails(snippet)
                for email in emails:
                    if len(email) < 8 or "example" in email or email.endswith("png") or email.endswith("jpg"):
                        continue
                    if email not in seen_emails:
                        seen_emails.add(email)
                        title = r.get('title', '').split('|')[0].split('-')[0].strip()
                        if len(title) > 40 or len(title) < 4:
                            title = f"{city} {category} Services"
                            
                        leads.append({
                            "email": email,
                            "name": "there",
                            "business": title.title(),
                            "city": city,
                            "category": category
                        })
                        count += 1
                        print(f"Found: {email} | {title} in {city}")
                        if count >= 50: break
                if count >= 50: break
        except Exception as e:
            time.sleep(2)
        time.sleep(1)

print(f"\nFound {len(leads)} leads. Preparing to send outreach...")

success_count = 0
for lead in leads:
    print(f"\nSending to {lead['email']} ({lead['business']})...")
    # Personalized locally tailored body
    custom_subject = f"Quick question for {lead['business']} — from a local"
    custom_body = f"""Hi {lead['name']},

I'm Conaugh McKenna — I run OASIS AI Solutions and I'm somewhat local out here in {lead['city']}.

I noticed {lead['business']} has a solid footprint, but seeing how other {lead['category'].lower()} businesses are operating right now, there's typically a huge opportunity to use AI and automation to save time. Things like automatic Google Review requests (which gets 3-4x more reviews), automated missed-call text-backs, and easy appointment reminders.

Most service businesses save 8-10 hours a week once the admin side is automated.

I'd love just 10 minutes to walk you through exactly how it works. No pitch, no pressure — just a quick demo to see if it makes sense. 

If you're open to it, here's a meeting link — no scheduling needed, just hop on whenever works this week or next:
https://meet.google.com/oqd-xpoq-fgw

Talk soon,

Conaugh McKenna
Founder, OASIS AI Solutions
oasisai.work"""

    try:
        res = send_outreach(
            lead_name=lead["name"],
            lead_email=lead["email"],
            business_name=lead["business"],
            business_type=lead["category"],
            meeting_datetime="2026-03-05T15:00:00",
            dry_run=False,
            custom_subject=custom_subject,
            custom_body=custom_body
        )
        if res.get("status") == "sent":
            success_count += 1
            print(" -> Sent successfully!")
        else:
            print(f" -> Failed: {res.get('error')}")
    except Exception as e:
        print(f" -> Exception: {e}")
        
    time.sleep(1) # sleep between emails

print(f"\nFinished. Sent {success_count} emails successfully.")
