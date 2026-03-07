import time
from outreach_engine import send_outreach

leads = [
    {
        "lead_name": "Teresa",
        "lead_email": "info@gardenholistics.com",
        "business_name": "Garden Holistics",
        "business_type": "Landscaping",
        "custom_subject": "Scaling sustainable landscaping without the admin bottleneck",
        "custom_body": """Hey Teresa,

I've been following Garden Holistics and love your approach to sustainable and native-species landscaping. When you're managing custom builds and eco-friendly maintenance at scale, the operational back-end — scheduling consults, tracking client approvals, and follow-ups — usually becomes the bottleneck. 

I'm CC, founder of OASIS AI Solutions here in Collingwood. We build AI-powered systems that handle the operational middle: automated consultation scheduling, client follow-ups, and review requests. Our systems run quietly in the background so your horticultural specialists can focus on the soil, not the inbox.

I'd love to buy you a coffee and run a quick 15-minute "automation audit" for Garden Holistics — no pressure, just a look at where you're losing time. Let me know if you're open to it.

Only good things,

CC
OASIS AI Solutions
oasisaisolutions@gmail.com"""
    },
    {
        "lead_name": "Dr. Melissa",
        "lead_email": "thrive@drmelissa.ca",
        "business_name": "Thrive Chiropractic & Holistic Care",
        "business_type": "Chiropractor",
        "custom_subject": "The 10 hours/week your front desk is losing",
        "custom_body": """Hey Dr. Melissa,

Your approach to holistic, collaborative healthcare is exactly what Collingwood needs right now. But when a practice is thriving, the admin is usually the first thing to break. Missed follow-ups, intake forms that need manual entry, and patients who forget to re-book.

I'm CC, founder of OASIS AI Solutions local to Collingwood. We build automated patient engagement systems for chiropractors and wellness clinics. One of our setups handles appointment confirmations, intake forms, and reactivation campaigns for patients who haven't booked in 6+ months — all without your front desk lifting a finger.

I'd love to buy you a coffee (or tea) and run a quick 15-minute demo to show you how much time you could be saving. 

Only good things,

CC
OASIS AI Solutions
oasisaisolutions@gmail.com"""
    },
    {
        "lead_name": "Sunny",
        "lead_email": "info@fullrangephysio.ca",
        "business_name": "Full Range Physiotherapy and Wellness",
        "business_type": "Physiotherapy",
        "custom_subject": "Your 5-star patient experience shouldn't end at the door",
        "custom_body": """Hey Sunny,

A multidisciplinary clinic operating at the level of Full Range means juggling physio, chiro, massage, and ICBC claims simultaneously. Most clinics solve this admin overload by hiring more front-desk staff. We solve it with AI.

I'm CC from OASIS AI, right here in Collingwood. We build automated patient onboarding flows, appointment reminder systems, and review campaigns that run entirely in the background. It's like having a marketing and admin assistant who never sleeps and never forgets to follow up on a cancellation.

I'd love to grab you a coffee and show you exactly what this looks like in action. Takes 15 minutes, zero commitment.

Only good things,

CC
OASIS AI Solutions
oasisaisolutions@gmail.com"""
    },
    {
        "lead_name": "Jonathan",
        "lead_email": "Jonathan@basquelandscaping.com",
        "business_name": "Basque Landscaping",
        "business_type": "Landscaping",
        "custom_subject": "Engineering the perfect client follow-up system",
        "custom_body": """Hey Jonathan,

I saw the customized patio and hardscaping projects you're executing — incredible work. I know with your engineering background, you appreciate systems that are precise and highly efficient. But when you're out bringing backyard dreams to life, following up with past clients and managing new quote requests can easily slip through the cracks.

I'm CC from OASIS AI here in Collingwood. We build AI-automation systems for high-end service businesses. We can put your lead capture, quote follow-ups, and post-project review requests on complete autopilot, saving you 10+ hours a week.

Would love to buy you a coffee and run a quick "automation audit" for Basque Landscaping to see where you could be gaining leverage.

Only good things,

CC
OASIS AI Solutions
oasisaisolutions@gmail.com"""
    },
    {
        "lead_name": "Owner/Manager",
        "lead_email": "COLLINGWOOD@MASTERMECHANIC.CA",
        "business_name": "Master Mechanic Collingwood",
        "business_type": "Auto Repair",
        "custom_subject": "The 10 hours/week your front desk is losing",
        "custom_body": """Hey team,

Running a busy auto repair shop in Collingwood means juggling bay schedules, parts ordering, and keeping customers updated. Most shops solve the admin overload by hiring another service advisor. We solve it with AI.

I'm CC from OASIS AI, right here in Collingwood. We build automated shop engagement systems that handle appointment reminders, routine maintenance follow-ups, and post-service review requests on complete autopilot.

I'd love to grab you a coffee and show you exactly what this looks like in action. Takes 15 minutes, zero commitment.

Only good things,

CC
OASIS AI Solutions
oasisaisolutions@gmail.com"""
    },
    {
        "lead_name": "Jason",
        "lead_email": "info@jnroofing.ca",
        "business_name": "JN Roofing & Contracting",
        "business_type": "Roofing",
        "custom_subject": "Scaling premium roofing crews without the admin bottleneck",
        "custom_body": """Hey Jason,

When you're running expert roofing crews across the Georgian Triangle, the operational back-end — scheduling quotes, tracking approvals, and chasing follow-ups — usually becomes the bottleneck.

I'm CC, founder of OASIS AI Solutions here in Collingwood. We build AI-powered systems that handle the operational middle: automated quote follow-ups, client communications, and review requests. It runs quietly in the background so you can focus on the job site.

I'd love to buy you a coffee and run a quick 15-minute "automation audit" for JN Roofing.

Only good things,

CC
OASIS AI Solutions
oasisaisolutions@gmail.com"""
    },
    {
        "lead_name": "Owner/Manager",
        "lead_email": "hello@borhoelectric.com",
        "business_name": "Borho Electric Inc.",
        "business_type": "Electrician",
        "custom_subject": "What happens between the initial quote and the final project",
        "custom_body": """Hey team,

Being heavily booked across Simcoe County is the dream for an electrical contractor, but the gap between a customer inquiry, sending a quote, and finalizing the schedule is where most teams lose hours every week.

I'm CC from OASIS AI, local here in Collingwood. We build custom automation systems for local contractors. From automated quote follow-ups to post-project review requests, we put the administrative heavy-lifting on autopilot.

I'd love to grab a coffee and show you how it works. 15-minute call, zero commitment.

Only good things,

CC
OASIS AI Solutions
oasisaisolutions@gmail.com"""
    },
    {
        "lead_name": "Owner/Manager",
        "lead_email": "info@lyftmedicalaesthetics.ca",
        "business_name": "LYFT Medical Aesthetics",
        "business_type": "Med Spa",
        "custom_subject": "The retention problem nobody talks about",
        "custom_body": """Hey team,

For a medical spa offering the range of advanced treatments that LYFT does, patient experience is everything. But missed follow-ups, intake forms needing manual entry, and patients forgetting their next treatment cycle can stall your growth.

I'm CC, founder of OASIS AI Solutions local to Collingwood. We build automated patient engagement systems for med spas. A setup handles appointment confirmations, intake forms, and reactivation campaigns for patients who haven't booked in 6+ months — all without your front desk lifting a finger.

I'd love to buy you a coffee and run a quick 15-minute demo to show you how much time you could be saving.

Only good things,

CC
OASIS AI Solutions
oasisaisolutions@gmail.com"""
    },
    {
        "lead_name": "Owner/Manager",
        "lead_email": "optical@collingwoodoptometry.ca",
        "business_name": "Collingwood Optometry",
        "business_type": "Optometry",
        "custom_subject": "Your 5-star patient experience shouldn't end at the door",
        "custom_body": """Hey team,

Collingwood Optometry has an incredible legacy in town. However, when an optometry clinic is busy, the admin is usually the first thing to break. Missed eye-exam reminders, intake forms, and patients who forget their annual check-ups.

I'm CC from OASIS AI, right here in Collingwood. We build automated patient onboarding flows, appointment reminder systems, and review campaigns that run entirely in the background. It's like having a marketing and admin assistant who never sleeps.

I'd love to grab you a coffee and show you exactly what this looks like in action. Takes 15 minutes, zero commitment.

Only good things,

CC
OASIS AI Solutions
oasisaisolutions@gmail.com"""
    },
    {
        "lead_name": "Owner/Manager",
        "lead_email": "admin@cwoodeyecare.ca",
        "business_name": "Cwood Eyecare",
        "business_type": "Optometry",
        "custom_subject": "What happens between the exam and the next booking",
        "custom_body": """Hey team,

As a newer optometry clinic in Collingwood focused on comprehensive care, growth means more patients to manage. But when you're busy, the gap between a patient booking and their next annual exam is where most clinics lose retention.

I'm CC from OASIS AI. We build custom automation systems for local clinics. From automated exam follow-ups to post-visit review requests, we put the administrative heavy-lifting on autopilot.

I'd love to grab a coffee and show you how it works. 15-minute call, zero commitment.

Only good things,

CC
OASIS AI Solutions
oasisaisolutions@gmail.com"""
    }
]

# Set times for Thursday, March 5th, incrementing every 30 mins
base_time = "2026-03-05T10:00:00"

for idx, lead in enumerate(leads):
    # Just format it to advance an hour for each
    hour = 10 + idx
    meeting_time = f"2026-03-05T{hour:02d}:00:00"
    
    print(f"Sending to {lead['lead_email']} ({lead['business_name']})...")
    
    send_outreach(
        lead_name=lead["lead_name"],
        lead_email=lead["lead_email"],
        business_name=lead["business_name"],
        business_type=lead["business_type"],
        meeting_datetime=meeting_time,
        custom_subject=lead["custom_subject"],
        custom_body=lead["custom_body"],
        # dry_run=True  # Uncomment for true testing
    )
    time.sleep(1.5)
