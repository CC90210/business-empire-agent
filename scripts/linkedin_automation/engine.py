import os
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env.agents'))

# We will use a dedicated persistent profile so you don't have to keep logging in via CDP manually.
# Playwright will store your session data here automatically.
PROFILE_DIR = os.path.join(os.path.dirname(__file__), "chrome_profile")

async def authenticate_linkedin(page):
    """
    Checks if we are logged in. If not, pauses execution so the user can log in manually 
    through the open browser window. The session is then saved for future automated runs.
    """
    print("Navigating to LinkedIn...")
    await page.goto("https://www.linkedin.com/feed/")
    
    try:
        # Wait up to 5 seconds to see if we are already logged in
        await page.wait_for_selector('a[href*="/in/"]', timeout=5000)
        print("Successfully authenticated via saved session cookies.")
        return True
    except:
        print("\n" + "="*50)
        print("ACTION REQUIRED: Not logged in.")
        print("Please log in to LinkedIn in the browser window that just opened.")
        print("Waiting for you to log in manually...")
        print("="*50 + "\n")
        
        try:
            # Wait up to 5 minutes for manual login
            await page.wait_for_selector('a[href*="/in/"]', timeout=300000)
            print("Login detected! Session saved permanently.")
            return True
        except:
            print("Login timeout. Please run the script again.")
            return False

async def search_and_connect(page, search_query):
    """Search for the target demographic and send connection requests."""
    
    print(f"Searching for: {search_query}")
    # Navigate directly to the people search URL to save clicks
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query.replace(' ', '%20')}&origin=GLOBAL_SEARCH_HEADER"
    await page.goto(search_url)
    
    # Wait for results to load
    await page.wait_for_selector('ul.reusable-search__entity-result-list', timeout=10000)
    
    # Find active "Connect" buttons.
    # Note: We need complex selector logic because LinkedIn obfuscates button classes and IDs.
    print("Scanning for Connect buttons...")
    
    # We would loop through and click here, but we need to establish the connection strategy first.
    # Rate limits: Max 20-30/day to stay safe.
    
    pass

async def main():
    print("Initializing LinkedIn Automation Engine Blueprint...")
    async with async_playwright() as p:
        # Instead of CDP, we use a persistent context which is much easier to manage.
        # It creates a dedicated portable Chrome profile just for this agent.
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,  # Must be False so CC can log in manually
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        is_authed = await authenticate_linkedin(page)
        
        if is_authed:
            # Example search logic
            await search_and_connect(page, "Founder AI SaaS")
            
        else:
            print("Failed to authenticate. Exiting.")

        print("Automation cycle complete. Closing browser in 10 seconds...")
        await asyncio.sleep(10)
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
