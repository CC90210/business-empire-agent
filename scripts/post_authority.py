import requests
import json
import os

# SURGICAL FIX FOR LATE MCP VALIDATION BUG (MAR 5)
# This script bypasses the Pydantic accountId dict-instead-of-string error

def post_now(content, platform):
    api_key = os.environ.get("LATE_API_KEY")
    if not api_key:
        # Load from .env.agents if not in env
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env.agents")
        with open(env_path, "r") as f:
            for line in f:
                if "LATE_API_KEY=" in line:
                    api_key = line.split("=")[1].strip()
                    break
    
    if not api_key:
        print("❌ LATE_API_KEY not found.")
        return

    # Use the raw REST API endpoint to avoid the Pydantic model issue in the MCP server
    # We'll use the IDs we got from accounts_list:
    # linkedin: 699c93508ab8ae478b3eeaee
    # twitter: 699c93608ab8ae478b3eeba1
    # threads: 699c93c58ab8ae478b3eec7e
    
    account_ids = {
        "linkedin": "699c93508ab8ae478b3eeaee",
        "twitter": "699c93608ab8ae478b3eeba1",
        "threads": "699c93c58ab8ae478b3eec7e"
    }

    if platform not in account_ids:
        print(f"❌ Unknown platform: {platform}")
        return

    url = "https://api.late.io/v1/posts"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "content": content,
        "platform": platform,
        "publish_now": True,
        "platforms": [
            {
                "platform": platform,
                "accountId": account_ids[platform] # Passing string directly, bypassing the dict bug
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            print(f"✅ Successfully posted to {platform}")
        else:
            print(f"❌ Failed to post to {platform}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error posting to {platform}: {e}")

if __name__ == "__main__":
    content = """Most local service businesses (HVAC, Plumbing, Dental) are losing 10-15 hours a week to "admin drag."

Things like:
- Manual Google Review requests
- Missed-call text-backs
- Appointment reminders

I've been working with local Ontario businesses to automate this entire side of their operations autonomously.

The result? 8-10 hours saved per week and 3-4x more reviews.

Check out what OASIS AI is building: oasisai.work #AI #Automation #OntarioBusiness #LocalService"""

    for platform in ["linkedin", "twitter", "threads"]:
        post_now(content, platform)
