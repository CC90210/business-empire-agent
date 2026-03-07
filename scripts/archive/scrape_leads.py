from googlesearch import search
import re
import json
import time

CITIES = ["Kitchener", "London", "Guelph", "Barrie", "Kingston", "Brampton", "Mississauga", "Oakville", "Burlington", "Hamilton"]
NICHES = [
    ("HVAC", "HVAC"),
    ("Plumber", "Plumbing"),
    ("Roofing", "Roofing"),
    ("Physiotherapy", "Physiotherapy"),
    ("Chiropractor", "Chiropractic"),
    ("Landscaping", "Landscaping"),
    ("Med Spa", "Medical Aesthetics"),
    ("Electrician", "Electrical")
]

DOMAINS = ["@gmail.com", "@hotmail.com", "@yahoo.com"]

leads = []
seen_emails = set()

def extract_emails(text):
    return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

def run_scraper():
    for city in CITIES:
        for niche, category in NICHES:
            for domain in DOMAINS:
                if len(leads) >= 50:
                    break
                query = f'{niche} "{city}" Ontario "{domain}"'
                print(f"Searching: {query}")
                try:
                    for j in search(query, num_results=10, sleep_interval=2, advanced=True):
                        # Combine title and description to extract email
                        text = (j.title + " " + j.description).lower()
                        emails = extract_emails(text)
                        for email in emails:
                            if email.endswith("png") or email.endswith("jpg"): continue
                            if email not in seen_emails and city.lower() not in email:
                                seen_emails.add(email)
                                # We use a generic business name based on the email username or title if it contains it
                                username = email.split("@")[0]
                                clean_name = username.replace(".", " ").replace("_", " ").title()
                                business_name = j.title.split("-")[0].strip() if "-" in j.title else j.title.split("|")[0].strip()
                                
                                # Fallback business name if length is suspicious
                                if len(business_name) < 3 or len(business_name) > 40:
                                    business_name = f"{clean_name} {category}"
                                
                                leads.append({
                                    "email": email,
                                    "name": "there", 
                                    "business": business_name,
                                    "city": city,
                                    "category": category,
                                    "hook_modifier": f"I'm also here in {city} and was checking out local {category.lower()} businesses."
                                })
                                print(f"Found: {email} - {business_name} ({city})")
                                if len(leads) >= 50: break
                        if len(leads) >= 50: break
                except Exception as e:
                    print(f"Error on {query}: {e}")
                    time.sleep(10)
        if len(leads) >= 50:
            break

    with open("tmp/scraped_leads.json", "w") as f:
        json.dump(leads, f, indent=2)
    print(f"\nTotal leads found: {len(leads)}")

if __name__ == "__main__":
    run_scraper()
