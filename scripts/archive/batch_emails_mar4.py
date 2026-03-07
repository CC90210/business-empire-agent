"""
Batch email send — Wednesday March 4 Cold Call Follow-ups + New Lead Outreach
Run: python scripts/batch_emails_mar4.py
"""
import os
import sys

# Load env vars from .env.agents
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env.agents")
with open(env_path, "r") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

from send_email import send_email

# ============================================================================
# WARM FOLLOW-UPS (spoke on phone today)
# ============================================================================

WARM_EMAILS = [
    {
        "to": "info@cedarwoodwellness.ca",
        "subject": "Conaugh from OASIS AI — Google Review Automation for Cedarwood",
        "body": """Hi Jessica,

My name is Conaugh McKenna — I just spoke with Mackie at the studio about a Google Review automation system that I think would be a great fit for Cedarwood Wellness.

Here's the quick version: I build AI-powered systems that automatically collect Google reviews from your clients after their appointments. No manual follow-up, no awkward "can you leave us a review?" conversations. It just happens.

Why it matters for Cedarwood specifically:
- More 5-star Google reviews = higher visibility when people search "wellness studio Collingwood"
- Automated review requests get 3-4x more responses than manual asks
- It runs completely in the background — zero extra work for your team

I'd love just 10 minutes of your time to walk you through exactly how it works. No pitch, no pressure — just a quick demo so you can see if it makes sense for the studio.

Would you have 10 minutes this week or early next week? Here's a quick meeting link — no scheduling needed, just hop on whenever works:
https://meet.google.com/oqd-xpoq-fgw

Thanks so much, and thank Mackie for the warm reception today!

Conaugh McKenna
Founder, OASIS AI Solutions
oasisaisolutions@gmail.com | oasisai.work
"""
    },
    {
        "to": "info@vortexwellness.ca",
        "subject": "Great chatting today, Daniel — OASIS AI agent setup",
        "body": """Hey Daniel,

Really enjoyed our conversation today — appreciate you taking the time.

As we discussed, I can help you set up your own AI agent environment — a personal IDE instance where you can build, customize, and deploy automations specific to Vortex Wellness. Think of it as your own AI operations hub that handles the repetitive stuff so you can focus on growing the studio.

A few things I can get running for you right away:
- Automated appointment reminders + follow-ups (reduce no-shows)
- Google review collection engine (boost your online visibility)
- Social media scheduling on autopilot
- Lead qualification from your website

I know this week is packed for you, so no rush at all. Whenever you're free next week, let's block 30 minutes and I'll walk you through the setup. I can have a working demo ready for you by then.

Here's a meeting link — no booking needed, just jump on whenever works for you:
https://meet.google.com/oqd-xpoq-fgw

Talk soon,

Conaugh McKenna
Founder, OASIS AI Solutions
oasisaisolutions@gmail.com | oasisai.work
"""
    },
]

# ============================================================================
# COLD OUTREACH (new leads from today's research)
# ============================================================================

COLD_EMAILS = [
    {
        "to": "thrive@drmelissa.ca",
        "name": "Dr. Melissa",
        "business": "Thrive Chiropractic & Holistic Care",
        "category": "Chiropractic",
        "hook": "I noticed Thrive has a strong online presence — but I think there's a big opportunity to automate your review collection and appointment reminders. Most chiropractic offices I've looked at lose 15-20% of appointments to no-shows. I can cut that in half with a simple AI reminder system."
    },
    {
        "to": "info@fullrangephysio.ca",
        "name": "Elliot",
        "business": "Full Range Physiotherapy and Wellness",
        "category": "Physiotherapy",
        "hook": "I took a quick look at Full Range's setup and saw a couple of opportunities — specifically around automated intake forms and appointment follow-ups. Most physio clinics I work with save 8-10 hours a week once we automate the admin side."
    },
    {
        "to": "info@lyftmedicalaesthetics.ca",
        "name": "there",
        "business": "LYFT Medical Aesthetics",
        "category": "Medical Aesthetics",
        "hook": "Med spas are one of the best businesses for AI automation — between booking confirmations, aftercare follow-ups, review requests, and seasonal promotions, there's easily 10+ hours a week of repetitive work that can run on autopilot. I'd love to show you what that looks like for LYFT specifically."
    },
    {
        "to": "info@jnroofing.ca",
        "name": "Jason",
        "business": "JN Roofing & Contracting",
        "category": "Roofing",
        "hook": "With spring coming up, roofing season is about to explode. I build AI systems that can automatically follow up with every quote request, send reminders, and collect Google reviews after each job — so you can focus on the work, not the admin. Most contractors I talk to are losing jobs simply because follow-ups slip through the cracks."
    },
    {
        "to": "hello@borhoelectric.com",
        "name": "there",
        "business": "Borho Electric Inc.",
        "category": "Electrical",
        "hook": "I was looking at Borho Electric's Google listing and thought of a couple of quick wins — automated quote follow-ups and a Google review engine that runs after every completed job. Electricians who automate their review collection typically see a 30-40% increase in Google reviews within the first month."
    },
    {
        "to": "Jonathan@basquelandscaping.com",
        "name": "Jonathan",
        "business": "Basque Landscaping",
        "category": "Landscaping",
        "hook": "Spring is right around the corner, and I imagine the phone is going to start ringing off the hook soon. I build AI systems that handle the overflow — automated quote follow-ups, scheduling confirmations, and Google review collection after each project. One landscaping company I worked with booked 3 extra months of work just by automating their follow-up process."
    },
    {
        "to": "info@gardenholistics.com",
        "name": "Teresa",
        "business": "Garden Holistics",
        "category": "Landscaping/Holistic",
        "hook": "I just had a look at Garden Holistics' online presence and had a few ideas for automating some of the admin work — especially around booking confirmations and seasonal campaign emails. I help service businesses save 10+ hours a week by putting the repetitive stuff on autopilot."
    },
    {
        "to": "COLLINGWOOD@MASTERMECHANIC.CA",
        "name": "there",
        "business": "Master Mechanic Collingwood",
        "category": "Auto Repair",
        "hook": "I noticed Master Mechanic Collingwood has solid Google reviews — but I think there's an opportunity to automate service reminders. An AI system that automatically reminds customers when their next oil change, tire rotation, or seasonal service is due can turn one-time visits into lifelong customers. Zero extra effort from your team."
    },
]

def build_cold_email(lead):
    """Build a personalized cold email from a lead dict."""
    subject = f"Quick idea for {lead['business']}"
    body = f"""Hey {lead['name']},

I'm Conaugh McKenna — I run OASIS AI Solutions here in Collingwood.

{lead['hook']}

I'd love to do a quick 10-minute call to show you exactly how it works — no commitment, no pitch. Just a quick walkthrough so you can see if it makes sense.

Would you have a few minutes this week or next?

If you're open to it, here's a quick meeting link — just hop on whenever works:
https://meet.google.com/oqd-xpoq-fgw

Have a great rest of your week,

Conaugh McKenna
Founder, OASIS AI Solutions
oasisaisolutions@gmail.com | oasisai.work
"""
    return subject, body


if __name__ == "__main__":
    print("=" * 60)
    print("📧 OASIS AI — Batch Email Send (March 4)")
    print("=" * 60)
    
    total = 0
    success = 0
    
    # Send warm follow-ups first
    print("\n🔥 WARM FOLLOW-UPS (spoke on phone today)")
    print("-" * 40)
    for email in WARM_EMAILS:
        print(f"\n→ Sending to: {email['to']}")
        print(f"  Subject: {email['subject']}")
        try:
            send_email(email["to"], email["subject"], email["body"])
            success += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
        total += 1
    
    # Send cold outreach
    print("\n\n❄️ COLD OUTREACH (new leads)")
    print("-" * 40)
    for lead in COLD_EMAILS:
        subject, body = build_cold_email(lead)
        print(f"\n→ Sending to: {lead['to']} ({lead['business']})")
        print(f"  Subject: {subject}")
        try:
            send_email(lead["to"], subject, body)
            success += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
        total += 1
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTS: {success}/{total} emails sent successfully")
    print("=" * 60)
