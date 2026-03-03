import requests
import json
import os

N8N_WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL", "https://n8n.srv993801.hstgr.cloud/webhook/google-calendar-bridge")
N8N_BEARER_TOKEN = os.environ.get("N8N_BEARER_TOKEN")
if not N8N_BEARER_TOKEN:
    raise ValueError("N8N_BEARER_TOKEN not set. Load from .env.agents.")

def manage_calendar(action, event_data=None):
    """
    Bravo Google Calendar Bridge via n8n.
    actions: 'list', 'create', 'update', 'delete'
    """
    print(f"📅 Calendar Bridge: {action}...")
    
    headers = {
        "Authorization": f"Bearer {N8N_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "action": action,
        "data": event_data,
        "user": "oasisaisolutions@gmail.com"
    }
    
    try:
        response = requests.post(N8N_WEBHOOK_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        print(f"✅ Calendar operation successful.")
        return result
    except Exception as e:
        print(f"❌ Calendar Bridge Error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example:
    # event = {"summary": "Revenue Hunter Meeting", "start": "2026-03-02T10:00:00Z", "end": "2026-03-02T11:00:00Z"}
    # manage_calendar("create", event)
    pass
