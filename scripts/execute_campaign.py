
import sys
import os
import json
from datetime import datetime

# Add the scripts directory to the path so we can import outreach_engine
sys.path.append(os.path.join(os.getcwd(), "scripts"))
from outreach_engine import send_outreach

def run_outreach():
    print("🚀 Starting Professional Outreach Campaign...")
    
    # 1. Real Estate Batch (PropFlow / OASIS)
    re_leads = [
        {
            "name": "Jason Ruttan",
            "email": "jason@jasonruttan.com",
            "business": "RE/MAX By The Bay",
            "type": "Real Estate"
        },
        {
            "name": "Janet Piotrowski",
            "email": "janet@collingwoodliving.ca", 
            "business": "Royal LePage Locations North",
            "type": "Real Estate"
        },
        {
            "name": "Dave Elfassy",
            "email": "dave@teamelfassy.com",
            "business": "Team Elfassy Sutton Group",
            "type": "Real Estate"
        }
    ]
    
    # 2. Service Batch (OASIS AI)
    service_leads = [
        {
            "name": "Jessica Racioppa",
            "email": "Jessica@cedarwoodwellness.ca",
            "business": "Cedarwood Wellness Studio",
            "type": "Wellness"
        },
        {
            "name": "Sarah Applegarth",
            "email": "sarah@activelifeconditioning.com",
            "business": "Active Life Conditioning",
            "type": "Fitness"
        },
        {
            "name": "Russel Griffin",
            "email": "info@barrieheatingcooling.ca", # Best available
            "business": "Affordable Comfort HVAC",
            "type": "HVAC"
        },
        {
            "name": "Dr. Raf Bartosiak",
            "email": "georgianshoresdentalcentre@gmail.com",
            "business": "Georgian Shores Dental",
            "type": "Dental"
        },
        {
            "name": "Mark Kehr",
            "email": "info@thenorthwoodfitnessclub.com",
            "business": "The Northwood Club",
            "type": "Fitness"
        },
        {
            "name": "Daniel James",
            "email": "info@vortexwellness.ca",
            "business": "Vortex Wellness Studio",
            "type": "Wellness"
        },
        {
            "name": "Colin",
            "email": "colin@wilmecsystems.com",
            "business": "Wilmec Plumbing Systems",
            "type": "Plumbing"
        }
    ]
    
    # 3. DJ Batch (Nostalgic Requests)
    dj_leads = [
        {
            "name": "Engage Entertainment",
            "email": "info@engageweddingdjs.com",
            "business": "Engage Entertainment",
            "type": "DJ/Performer"
        },
        {
            "name": "Supreme DJs",
            "email": "info@supremedjs.ca", # Best available from research
            "business": "Supreme DJs",
            "type": "DJ/Performer"
        },
        {
            "name": "DJ Shayne",
            "email": "shaynewilley@live.com",
            "business": "DJ Shayne",
            "type": "DJ/Performer"
        }
    ]
    
    all_results = []
    
    # Send schedule (starting 2 days from now to give buffer)
    start_time = datetime(2026, 3, 5, 10, 0)
    
    for i, lead in enumerate(re_leads + service_leads + dj_leads):
        meet_time = start_time + __import__('datetime').timedelta(days=i//3, hours=(i%3)*2)
        iso_time = meet_time.isoformat()
        
        print(f"📧 Sending to {lead['name']} ({lead['email']})...")
        try:
            res = send_outreach(
                lead_name=lead["name"],
                lead_email=lead["email"],
                business_name=lead["business"],
                business_type=lead["type"],
                meeting_datetime=iso_time,
                dry_run=False
            )
            all_results.append(res)
        except Exception as e:
            print(f"❌ Failed to send to {lead['name']}: {e}")
            all_results.append({"status": "error", "lead": lead["name"], "error": str(e)})

    # Write log
    log_path = os.path.join(os.getcwd(), "memory", "daily", "2026-03-02_execution_log.json")
    with open(log_path, "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n✅ Campaign complete. {len(all_results)} leads processed. Log saved to {log_path}")

if __name__ == "__main__":
    run_outreach()
