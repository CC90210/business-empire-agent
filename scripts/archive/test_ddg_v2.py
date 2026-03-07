from duckduckgo_search import DDGS
import re

ddgs = DDGS()
# Try a more specific site search which often works better for emails
query = 'site:facebook.com "HVAC" "Collingwood" "@gmail.com"'
print(f"Testing query: {query}")
try:
    results = list(ddgs.text(query, max_results=10))
    for r in results:
        text = (r.get('title', '') + " " + r.get('body', '')).lower()
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        if emails:
            print(f"Found: {emails} in {r.get('title')}")
        else:
            print(f"No emails in: {r.get('title')}")
except Exception as e:
    print(f"Error: {e}")
