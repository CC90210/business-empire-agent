"""
LinkedIn Lead Outreach — Wednesday March 4 (Afternoon Batch)
Business owners in the Georgian Bay area found via LinkedIn research.
Run: python scripts/batch_linkedin_emails_mar4.py
"""
import os
import sys

# Load env vars
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env.agents")
with open(env_path, "r") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

from send_email import send_email

LINKEDIN_LEADS = [
    {
        "to": "info@collingwoodcharters.ca",
        "name": "Matt",
        "business": "Collingwood Charters",
        "category": "Tourism/Charters",
        "hook": "I was looking at Collingwood Charters and thought of something — charter booking confirmations, weather-based trip reminders, and automated review requests after each trip. These three automations alone could save you hours every week during peak season and keep your Google reviews climbing. Spring is coming fast and I imagine bookings are about to ramp up."
    },
    {
        "to": "info@peakliving.ca",
        "name": "Tom",
        "business": "Peak Living Inc.",
        "category": "Property/Living",
        "hook": "I came across Peak Living and had a couple of ideas around automating tenant communications and maintenance request routing. Property-related businesses that automate their intake and follow-up systems typically save 10-15 hours a week — and tenants love the instant response times."
    },
    {
        "to": "theironskilletwasaga@gmail.com",
        "name": "Patrick",
        "business": "The Iron Skillet",
        "category": "Restaurant",
        "hook": "Restaurants are one of my favourite businesses to automate — reservation confirmations, Google review requests after every meal, and social media content scheduling can all run on complete autopilot. I'd love to show you how The Iron Skillet could boost its Google visibility and fill more tables without adding any extra work for your team."
    },
    {
        "to": "david@wasaga.beer",
        "name": "David",
        "business": "Wasaga Beach Brewing Company",
        "category": "Brewery",
        "hook": "Really cool what you're building with Wasaga Beach Brewing. I had a few ideas — automated event promotion (taproom events, new releases), a Google review engine that runs after every visit, and seasonal email campaigns that go out on autopilot. Craft breweries that automate their marketing see 20-30% more repeat visits."
    },
    {
        "to": "collingwoodon@anytimefitness.com",
        "name": "Edward",
        "business": "Anytime Fitness Collingwood",
        "category": "Gym/Fitness",
        "hook": "January sign-ups slow down around this time of year — but the members who stuck around are your golden ones. I build AI systems that automate member retention (check-in reminders, milestone celebrations, re-engagement campaigns for inactive members) and Google review collection. Most gyms I talk to are leaving 20+ reviews on the table every month."
    },
    {
        "to": "info@thetremontcafe.com",
        "name": "Bev",
        "business": "The Tremont Cafe",
        "category": "Restaurant/Cafe",
        "hook": "I was looking at The Tremont and thought of a few quick wins — automated Google review requests after every visit, a loyalty program reminder system, and social media content scheduling. Cafes that automate their review collection typically climb 15-20 spots in local Google rankings within 3 months."
    },
    {
        "to": "info@rootedchiro.ca",
        "name": "Dr. Stephanie",
        "business": "Rooted Family Chiropractic",
        "category": "Chiropractic",
        "hook": "Family chiropractic is one of the best fits for AI automation — between appointment reminders (cuts no-shows by 40%), new patient intake automation, and post-visit care emails, there's easily 8-10 hours of weekly admin work that can run itself. I'd love to show you what that looks like for Rooted specifically."
    },
    {
        "to": "vanessa@studiov.me",
        "name": "Vanessa",
        "business": "Studio V",
        "category": "Beauty/Salon",
        "hook": "I came across Studio V and love what you've built. I had a few ideas — automated appointment reminders (reduces no-shows significantly), a Google review engine that asks clients for feedback right after their visit, and social media scheduling on autopilot. Beauty studios that automate their review collection see a huge jump in new client bookings from Google."
    },
]


def build_email(lead):
    subject = f"Quick idea for {lead['business']}"
    body = f"""Hey {lead['name']},

I'm Conaugh McKenna — I run OASIS AI Solutions here in Collingwood.

{lead['hook']}

I'd love just 10 minutes to walk you through exactly how it works — no commitment, no pitch. Just a quick demo so you can decide if it makes sense.

Would you have a few minutes this week or next? Here's a quick meeting link — just hop on whenever works:
https://meet.google.com/oqd-xpoq-fgw

Have a great rest of your week,

Conaugh McKenna
Founder, OASIS AI Solutions
oasisaisolutions@gmail.com | oasisai.work
"""
    return subject, body


if __name__ == "__main__":
    print("=" * 60)
    print("📧 LinkedIn Lead Outreach — March 4 Afternoon")
    print("=" * 60)
    
    total = 0
    success = 0
    
    for lead in LINKEDIN_LEADS:
        subject, body = build_email(lead)
        print(f"\n→ {lead['business']} ({lead['name']}) → {lead['to']}")
        print(f"  Subject: {subject}")
        try:
            send_email(lead["to"], subject, body)
            success += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
        total += 1
    
    print(f"\n{'=' * 60}")
    print(f"📊 RESULTS: {success}/{total} emails sent")
    print(f"{'=' * 60}")
