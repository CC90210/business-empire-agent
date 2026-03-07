
const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');
const dotenv = require('dotenv');

// Load env
const envPath = path.join(__dirname, '..', '.env.agents');
if (fs.existsSync(envPath)) {
    const envConfig = dotenv.parse(fs.readFileSync(envPath));
    for (const k in envConfig) {
        process.env[k] = envConfig[k];
    }
}

const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.GMAIL_USER || 'oasisaisolutions@gmail.com',
        pass: process.env.GMAIL_APP_PASSWORD
    }
});

function generateIcs(leadName, leadEmail, startIso, meetLink, organizerEmail) {
    const start = new Date(startIso);
    const end = new Date(start.getTime() + 30 * 60000);
    const fmt = (d) => d.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
    const uid = Math.random().toString(36).substring(2);

    return `BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//OASIS AI Solutions//Bravo Outreach//EN
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VEVENT
UID:${uid}
DTSTART:${fmt(start)}
DTEND:${fmt(end)}
DTSTAMP:${fmt(new Date())}
ORGANIZER;CN=OASIS AI Solutions:mailto:${organizerEmail}
ATTENDEE;CN=${leadName};RSVP=TRUE:mailto:${leadEmail}
SUMMARY:OASIS AI Solutions — Discovery Call with ${leadName}
DESCRIPTION:Quick intro call to explore how AI automation can save your team 10+ hours/week.\\n\\nJoin via Google Meet: ${meetLink}
LOCATION:${meetLink}
STATUS:CONFIRMED
SEQUENCE:0
END:VEVENT
END:VCALENDAR`;
}

async function sendOutreach(lead) {
    const meetLink = process.env.GOOGLE_MEET_LINK || 'https://meet.google.com/oqd-xpoq-fgw';
    const dateStr = new Date(lead.meeting_time).toLocaleString('en-US', { weekday: 'long', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', timeZoneName: 'short' });

    let body = "";
    let subject = `${lead.business} — Save 10+ Hours/Week with AI Automation`;

    if (lead.type === "DJ/Performer") {
        subject = `Nostalgic Requests — A special tool for ${lead.name}`;
        body = `Hi ${lead.name},

I’ve been watching the reviews come in for your local gigs — people are clearly loving the energy you're bringing to the Georgian Bay scene.

I’m CC, a software developer based in Collingwood. I’ve spent the last few months building **Nostalgic Requests** — a free song request and payment platform designed specifically for performers to make more money during their sets.

It’s simple: the audience scans a QR code, requests a song, and pays you instantly via Apple/Google Pay. You get the requests in a clean dashboard and keep 95% of the revenue. No more messy papers or people shouting in your ear.

I'm looking for a few local pros to start using it for free and give me some "in-the-trenches" feedback. It takes 2 minutes to set up.

I'd love to buy you a coffee at Nicky's and show you how it works:

    ${dateStr}
    Google Meet (or let's meet at Nicky's): ${meetLink}

Only good things,

Conaugh McKenna
Founder, Nostalgic Requests
nostalgicrequests.com`;
    } else {
        const hook = lead.hook || "I came across your business and was impressed by your local reputation.";
        body = `Hi ${lead.name},

${hook}

At OASIS AI Solutions, we build custom automation systems for ${lead.type} businesses. Our clients typically save 10-15 hours per week on manual tasks and see faster response times that directly improve close rates.

I'd love to show you exactly how this works for your business. No pitch, just a quick walkthrough.

I've set aside time for a 30-minute discovery call:

    ${dateStr}
    Google Meet: ${meetLink}

If that time doesn't work, just reply with what does.

Looking forward to connecting.

Conaugh McKenna
Founder, OASIS AI Solutions
oasisai.work`;
    }

    const ics = generateIcs(lead.name, lead.email, lead.meeting_time, meetLink, process.env.GMAIL_USER);

    const mailOptions = {
        from: `"OASIS AI Solutions" <${process.env.GMAIL_USER}>`,
        to: lead.email,
        bcc: process.env.GMAIL_USER, // Ensuring calendar congruence for the user
        subject: subject,
        text: body,
        attachments: [{
            filename: 'invite.ics',
            content: ics,
            contentType: 'text/calendar; charset=utf-8; method=REQUEST'
        }]
    };

    try {
        await transporter.sendMail(mailOptions);
        console.log(`✅ Sent to ${lead.name} (${lead.email})`);
        return { status: 'sent', lead: lead.name };
    } catch (error) {
        console.error(`❌ Failed ${lead.name}: ${error.message}`);
        return { status: 'error', lead: lead.name, error: error.message };
    }
}

async function main() {
    console.log("🚀 Starting Node-based Outreach...");
    const leads = [
        { name: "Jason Ruttan", email: "jason@jasonruttan.com", business: "RE/MAX By The Bay", type: "Real Estate", hook: "I've been following the massive volume RE/MAX By The Bay has been moving — $4B in sales volume is an incredible milestone for the Southern Georgian Bay market.", meeting_time: "2026-03-05T10:00:00" },
        { name: "Janet Piotrowski", email: "janet@collingwoodliving.ca", business: "Royal LePage Locations North", type: "Real Estate", hook: "I saw your focus on the luxury experience here in Collingwood. Premium listings deserve a premium client journey.", meeting_time: "2026-03-05T12:00:00" },
        { name: "Dave Elfassy", email: "dave@teamelfassy.com", business: "Team Elfassy Sutton Group", type: "Real Estate", hook: "You guys are winning the volume game in Ontario with the 1% model. To keep that margin healthy as you scale, I know admin efficiency is the bottleneck.", meeting_time: "2026-03-05T14:00:00" },
        { name: "Jessica Racioppa", email: "Jessica@cedarwoodwellness.ca", business: "Cedarwood Wellness Studio", type: "Wellness", hook: "I love the story of how you transitioned from musical theatre to opening Cedarwood — that fluid, intuitive approach really shows in the calm atmosphere you've built.", meeting_time: "2026-03-06T10:00:00" },
        { name: "Sarah Applegarth", email: "sarah@activelifeconditioning.com", business: "Active Life Conditioning", type: "Fitness", hook: "Big congrats on the 15th anniversary of Active Life this year! Seeing the expansion and the new pickleball space is awesome for the Collingwood community.", meeting_time: "2026-03-06T12:00:00" },
        { name: "Russel Griffin", email: "info@barrieheatingcooling.ca", business: "Affordable Comfort HVAC", type: "HVAC", hook: "I know you guys focus heavily on response time for service calls across Simcoe County.", meeting_time: "2026-03-06T14:00:00" },
        { name: "Dr. Raf Bartosiak", email: "georgianshoresdentalcentre@gmail.com", business: "Georgian Shores Dental", type: "Dental", hook: "A 5.0 rating with that many reviews is rare for dental — clearly the patient experience is the priority there.", meeting_time: "2026-03-07T10:00:00" },
        { name: "Mark Kehr", email: "info@thenorthwoodfitnessclub.com", business: "The Northwood Club", type: "Fitness", hook: "I've been watching the community you're building at Northwood. In a town as active as Collingwood, keeping that retention high is the ultimate game.", meeting_time: "2026-03-07T12:00:00" },
        { name: "Daniel James", email: "info@vortexwellness.ca", business: "Vortex Wellness Studio", type: "Wellness", hook: "I saw the co-founding story of Vortex. Bringing that level of wellness tech (float pods, etc.) to town was a huge move.", meeting_time: "2026-03-07T14:00:00" },
        { name: "Colin", email: "colin@wilmecsystems.com", business: "Wilmec Plumbing Systems", type: "Plumbing", hook: "I came across Wilmec and noticed the focus on high-quality systems for the local Collingwood builds.", meeting_time: "2026-03-08T10:00:00" },
        { name: "Engage Entertainment", email: "info@engageweddingdjs.com", business: "Engage Entertainment", type: "DJ/Performer", meeting_time: "2026-03-08T12:00:00" },
        { name: "Supreme DJs", email: "info@supremedjs.ca", business: "Supreme DJs", type: "DJ/Performer", meeting_time: "2026-03-08T14:00:00" },
        { name: "DJ Shayne", email: "shaynewilley@live.com", business: "DJ Shayne", type: "DJ/Performer", meeting_time: "2026-03-05T16:00:00" }
    ];

    const results = [];
    for (const lead of leads) {
        results.push(await sendOutreach(lead));
    }

    fs.writeFileSync(path.join(__dirname, '..', 'memory', 'daily', '2026-03-02_execution_log.json'), JSON.stringify(results, null, 2));
    console.log("🏁 Done.");
}

main();
