import sys
import re
import json
import time
from duckduckgo_search import DDGS

CITIES = ["Barrie", "Guelph", "Kitchener", "London", "Kingston", "Mississauga", "Oakville", "Burlington", "Hamilton", "Oshawa"]
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

count = 0
with DDGS() as ddgs:
    for city in CITIES:
        for search_term, category in NICHES:
            if count >= 50:
                break
            query = f'"{search_term}" "{city}" Ontario "@gmail.com" OR "@hotmail.com" OR "@yahoo.ca"'
            print(f"Searching: {query}")
            try:
                # Use duckduckgo text search
                results = list(ddgs.text(query, max_results=5))
                for r in results:
                    snippet = (r.get('title', '') + " " + r.get('body', '')).lower()
                    emails = extract_emails(snippet)
                    
                    for email in emails:
                        if email.endswith("png") or email.endswith("jpg") or "example" in email: 
                            continue
                        if email not in seen_emails and city.lower() not in email:
                            seen_emails.add(email)
                            username = email.split("@")[0]
                            clean_name = username.replace(".", " ").replace("_", " ").title()
                            # Use title as business but clean it
                            title = r.get('title', '').split('|')[0].split('-')[0].strip()
                            if len(title) > 40 or len(title) < 4:
                                title = f"{clean_name} {category}"
                                
                            leads.append({
                                "email": email,
                                "name": "there",
                                "business": title,
                                "city": city,
                                "category": category
                            })
                            count += 1
                            print(f" -> Found email: {email} | {title}")
                            if count >= 50: break
                    if count >= 50: break
            except Exception as e:
                print(f"Error on {query}: {e}")
                time.sleep(2)
            time.sleep(1)

with open("tmp/leads_mar5.json", "w") as f:
    json.dump(leads, f, indent=2)
print(f"Total leads: {len(leads)}")
