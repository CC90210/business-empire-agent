import asyncio
from playwright.async_api import async_playwright
import re
import json
import os

CITIES = ["Collingwood", "Wasaga Beach", "Owen Sound", "Barrie", "Orillia", "Midland"]
NICHES = ["HVAC", "Plumber", "Roofing", "Physiotherapist", "Chiropractor", "Landscaping"]

def extract_emails(text):
    return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

async def scrape_google(city, niche):
    leads = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        query = f'{niche} "{city}" Ontario email "@gmail.com"'
        print(f"Scraping: {query}")
        await page.goto(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        
        # Wait for results or captcha
        try:
            await page.wait_for_selector('div#search', timeout=5000)
        except:
            print(f"Captcha or no results for {city} {niche}")
            await browser.close()
            return []
            
        # Extract text from the page
        content = await page.content()
        emails = extract_emails(content)
        
        # We need to find business names and map them to emails
        # This is tricky with raw HTML, but let's try finding <h3> tags near emails
        # For simplicity, let's just extract all emails and some context
        for email in set(emails):
            if email.lower().strip() not in ["sentry@google.com", "accounts@google.com"]:
                leads.append({
                    "email": email,
                    "city": city,
                    "category": niche,
                    "business": f"{city} {niche} Service" # Fallback
                })
        
        await browser.close()
    return leads

async def main():
    all_leads = []
    for city in CITIES:
        if len(all_leads) >= 50: break
        for niche in NICHES:
            if len(all_leads) >= 50: break
            city_leads = await scrape_google(city, niche)
            all_leads.extend(city_leads)
            print(f"Found {len(city_leads)} leads for {city} {niche}")
            await asyncio.sleep(2) # Avoid too fast scraping
            
    output_path = "tmp/scraped_leads_playwright.json"
    os.makedirs("tmp", exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(all_leads, f, indent=2)
    print(f"Total leads: {len(all_leads)}")

if __name__ == "__main__":
    asyncio.run(main())
