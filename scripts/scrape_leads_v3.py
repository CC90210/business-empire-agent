import sys
import os
import re
import json
import time
import csv
from googlesearch import search

# Load environment variables for outreach_engine if needed
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env.agents")
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()

CITIES = ["Collingwood", "Wasaga Beach", "Stayner", "Owen Sound", "Meaford", "Thornbury", "Blue Mountains", "Barrie", "Orillia", "Midland", "Newmarket", "Vaughan", "Richmond Hill"]
NICHES = [
    ("HVAC", "HVAC"),
    ("Plumber", "Plumbing"),
    ("Roofing", "Roofing"),
    ("Physiotherapy", "Physiotherapy"),
    ("Chiropractor", "Chiropractic"),
    ("Landscaping", "Landscaping"),
    ("Med Spa", "Medical Aesthetics"),
    ("Electrician", "Electrical"),
    ("Auto Repair", "Auto Repair"),
    ("Dentist", "Dental")
]

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memory", "LEAD_TRACKER.csv")

def get_existing_emails():
    emails = set()
    if os.path.exists(CSV_PATH):
        try:
            with open(CSV_PATH, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    email = row.get('Email/Contact', '').lower().strip()
                    if email:
                        emails.add(email)
        except Exception as e:
            print(f"Warning: Could not read CSV: {e}")
    return emails

def extract_emails(text):
    return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

def run_scraper(target_count=50):
    existing_emails = get_existing_emails()
    leads = []
    seen_emails = set()
    
    print(f"Starting to scrape {target_count} NEW leads (excluding {len(existing_emails)} existing)...")
    
    for city in CITIES:
        if len(leads) >= target_count: break
        for niche, category in NICHES:
            if len(leads) >= target_count: break
            
            # Use broader query for better results
            query = f'{niche} "{city}" Ontario "{category}" "@gmail.com" OR "@hotmail.com" OR "@outlook.com"'
            print(f"Searching: {query}")
            try:
                # num_results=15 to get enough snippets
                for j in search(query, num_results=15, sleep_interval=2, advanced=True):
                    snippet = (j.title + " " + j.description).lower()
                    emails = extract_emails(snippet)
                    for email in emails:
                        clean_email = email.lower().strip()
                        if len(clean_email) < 8 or "example" in clean_email or clean_email.endswith(("png", "jpg", "jpeg", "gif", "webp")):
                            continue
                        if clean_email not in seen_emails and clean_email not in existing_emails:
                            seen_emails.add(clean_email)
                            
                            # Clean up business name
                            title = j.title.split('|')[0].split('-')[0].strip()
                            if len(title) > 45 or len(title) < 3:
                                title = f"{city} {category} Pros"
                            
                            # Guess a name from email if it's there, else 'there'
                            lead_name = "there"
                            username = clean_email.split('@')[0]
                            if '.' in username:
                                parts = username.split('.')
                                if len(parts[0]) > 2: lead_name = parts[0].title()
                            elif len(username) > 3 and username.isalpha():
                                lead_name = username.title()

                            # For competitor, just pick a generic or find another from results later
                            # For simplicity, we'll use a placeholder for now
                            
                            leads.append({
                                "email": clean_email,
                                "name": lead_name,
                                "business": title.title(),
                                "city": city,
                                "category": category,
                                "competitor": "local competition"
                            })
                            print(f"  Found NEW lead: {clean_email} | {title} in {city}")
                            if len(leads) >= target_count: break
                    if len(leads) >= target_count: break
                time.sleep(2) # Avoid rate limits
            except Exception as e:
                print(f"  Error on {query}: {e}")
                time.sleep(5)
                
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tmp", "scraped_leads_v3.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(leads, f, indent=2)
    print(f"\nTotal new leads found: {len(leads)}")
    return leads

if __name__ == "__main__":
    run_scraper(50)
