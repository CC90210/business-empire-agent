from duckduckgo_search import DDGS
import re

ddgs = DDGS()
query = 'HVAC "Collingwood" Ontario email "@gmail.com"'
print(f"Testing query: {query}")
results = list(ddgs.text(query, max_results=10))
for r in results:
    text = (r.get('title', '') + " " + r.get('body', '')).lower()
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    if emails:
        print(f"Found: {emails} in {r.get('title')}")
    else:
        print(f"No emails in: {r.get('title')}")
