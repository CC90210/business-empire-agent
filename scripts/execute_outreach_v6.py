import asyncio
from playwright.async_api import async_playwright
import re
import json
import os
import csv
import time
import smtplib
from email.message import EmailMessage

# --- CONFIG & ENV ---
CITIES = ["Oakville", "Burlington", "Milton", "Mississauga", "Hamilton", "Kitchener", "London", "Guelph", "Barrie", "Collingwood"]
NICHES = [
    ("HVAC", "HVAC"),
    ("Plumbing", "Plumber"),
    ("Roofing", "Roofer"),
    ("Physiotherapy", "Physiotherapist"),
    ("Chiropractic", "Chiropractor"),
    ("Landscaping", "Landscaper"),
    ("Med Spa", "Medical Spa"),
    ("Electrical", "Electrician"),
    ("Auto Repair", "Auto Repair"),
    ("Dentist", "Dentist")
]

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memory", "LEAD_TRACKER.csv")
ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env.agents")

GMAIL_USER = ""
GMAIL_PASS = ""

if os.path.exists(ENV_PATH):
    with open(ENV_PATH, "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                if k == "GMAIL_USER": GMAIL_USER = v
                if k == "GMAIL_APP_PASSWORD": GMAIL_PASS = v

# --- UTILS ---
def get_existing_emails():
    emails = set()
    if os.path.exists(CSV_PATH):
        try:
            with open(CSV_PATH, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    email = row.get('Email/Contact', '').lower().strip()
                    if email: emails.add(email)
        except: pass
    return emails

def update_csv(lead_data):
    today = time.strftime("%Y-%m-%d")
    file_exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Lead Name", "Business Name", "Category", "Email/Contact", "Phone", "Status"])
        writer.writerow([today, lead_data['name'], lead_data['business'], lead_data['category'], lead_data['email'], "", "Sent"])

def send_email(to_email, subject, body):
    if not GMAIL_USER or not GMAIL_PASS:
        return False
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = GMAIL_USER
        msg['To'] = to_email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASS)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send to {to_email}: {e}")
        return False

async def get_emails_from_url(page, url):
    try:
        if not url.startswith('http'): url = 'https://' + url
        await page.goto(url, timeout=10000, wait_until='domcontentloaded')
        content = await page.content()
        mailto = re.findall(r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', content)
        regex = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
        emails = [e.lower() for e in list(set(mailto + regex)) if not e.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', 'sentry.io', 'email.com', 'example.com', 'wixpress.com', 'squarespace.com'))]
        return emails
    except: return []

async def handle_consent(page):
    try:
        # Check for Google consent screen
        buttons = await page.query_selector_all('button')
        for b in buttons:
            text = await b.inner_text()
            if "Accept all" in text or "I agree" in text or "Agree" in text:
                await b.click()
                await page.wait_for_timeout(2000)
                return True
    except: pass
    return False

# --- MAIN ENGINE ---
async def run_outreach(target=50):
    existing_emails = get_existing_emails()
    sent_count = 0
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = await context.new_page()
        
        # Initial navigation to handle consent
        await page.goto("https://www.google.com/maps")
        await handle_consent(page)
        
        for city in CITIES:
            if sent_count >= target: break
            for category_query, niche_label in NICHES:
                if sent_count >= target: break
                
                query = f"{category_query} in {city} Ontario"
                print(f"\n📍 Searching: {query}")
                try:
                    search_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
                    await page.goto(search_url, timeout=20000)
                    await page.wait_for_timeout(3000) # Wait for initial load
                    
                    # Try to find businesses by aria-label links
                    business_links = []
                    links = await page.query_selector_all('a[aria-label]')
                    for link in links:
                        label = await link.get_attribute('aria-label')
                        href = await link.get_attribute('href')
                        if label and href and "https://www.google.com/maps/place" in href:
                            business_links.append((label, href))
                    
                    if not business_links:
                        # Try another way to wait for the feed
                        try:
                            await page.wait_for_selector('a[href*="/maps/place/"]', timeout=5000)
                            links = await page.query_selector_all('a[href*="/maps/place/"]')
                            for link in links:
                                label = await link.get_attribute('aria-label')
                                href = await link.get_attribute('href')
                                if label and href:
                                    business_links.append((label, href))
                        except: pass

                    print(f"  Found {len(business_links)} potential businesses")
                    competitor_pool = [b[0].split('|')[0].split('-')[0].strip() for b in business_links if b[0]]
                    
                    for name, href in business_links:
                        if sent_count >= target: break
                        if not name: continue
                        clean_name = name.split('|')[0].split('-')[0].strip()
                        
                        try:
                            await page.goto(href, timeout=15000)
                            await page.wait_for_timeout(2000)
                            
                            # Website discovery
                            website_el = await page.query_selector('a[aria-label*="Website"]')
                            if not website_el:
                                # Fallback selectors
                                website_el = await page.query_selector('a[data-item-id="authority"]')
                                if not website_el:
                                    website_el = await page.query_selector('a[data-tooltip*="website"]')

                            if website_el:
                                url = await website_el.get_attribute('href')
                                email_page = await context.new_page()
                                emails = await get_emails_from_url(email_page, url)
                                await email_page.close()
                                
                                if emails:
                                    email = emails[0].lower().strip()
                                    if email not in existing_emails:
                                        # Personalization
                                        comp_name = "local competition"
                                        for c in competitor_pool:
                                            if c and c.lower() not in clean_name.lower() and clean_name.lower() not in c.lower():
                                                comp_name = c
                                                break
                                        
                                        subject = f"Question about {clean_name} / {city} {niche_label}"
                                        body = f"Hi there,\n\nI was looking at {clean_name} earlier — really great to see a local {niche_label} in {city} with such good reviews. I'm actually a local here in Ontario as well.\n\nI'm curious, as a business owner, how do you guys handle new lead inquiries when you're out on a job or after hours? I noticed {comp_name} has been ramping up their presence lately, and I was wondering if you've seen a shift in the local market.\n\nI ask because I'm actually helping a few other {niche_label} businesses in Ontario automate their follow-ups using AI so they don't miss any new business. It's been a game changer for them.\n\nI'd love to just show you what they're doing — no pitch, no pressure, just a 5-10 minute look at the data I'm seeing in the area.\n\nIf you're open to it, you can just hop on this link whenever works for you this week: https://meet.google.com/oqd-xpoq-fgw\n\nNo scheduling needed, just a quick neighborly chat. Would you be open to a 2-minute chat about it? I'd love to hear your perspective.\n\nBest,\nConaugh"
                                        
                                        print(f"  📧 Sending to {email} ({clean_name})...")
                                        if send_email(email, subject, body):
                                            sent_count += 1
                                            existing_emails.add(email)
                                            update_csv({"name": "there", "business": clean_name.title(), "category": niche_label, "email": email})
                                            print(f"  ✅ Sent! Total: {sent_count}/{target}")
                                            await asyncio.sleep(2)
                                        else:
                                            print(f"  ❌ Failed to send.")
                        except Exception as e:
                            # print(f"  Error on {clean_name}: {e}")
                            pass
                except Exception as e:
                    print(f"  Error on search {query}: {e}")
        await browser.close()
    print(f"\n🎉 Finished! Total sent: {sent_count}")

if __name__ == "__main__":
    asyncio.run(run_outreach(50))
