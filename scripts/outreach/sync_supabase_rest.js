const https = require('https');
const fs = require('fs');
const path = require('path');
const dotenv = require('dotenv');

// Load env
const envPath = path.join(__dirname, '..', '.env.agents');
const envConfig = dotenv.parse(fs.readFileSync(envPath));

const SUPABASE_URL = envConfig.BRAVO_SUPABASE_URL;
const SUPABASE_KEY = envConfig.BRAVO_SUPABASE_SERVICE_ROLE_KEY;

const leads = [
    { name: "Jason Ruttan", email: "jason@jasonruttan.com", business: "RE/MAX By The Bay", type: "Real Estate", status: "SENT", outreach_date: "2026-03-02" },
    { name: "Janet Piotrowski", email: "janet@collingwoodliving.ca", business: "Royal LePage Locations North", type: "Real Estate", status: "SENT", outreach_date: "2026-03-02" },
    { name: "Dave Elfassy", email: "dave@teamelfassy.com", business: "Team Elfassy Sutton Group", type: "Real Estate", status: "SENT", outreach_date: "2026-03-02" },
    { name: "Jessica Racioppa", email: "Jessica@cedarwoodwellness.ca", business: "Cedarwood Wellness Studio", type: "Wellness", status: "SENT", outreach_date: "2026-03-02" },
    { name: "Sarah Applegarth", email: "sarah@activelifeconditioning.com", business: "Active Life Conditioning", type: "Fitness", status: "SENT", outreach_date: "2026-03-02" },
    { name: "Russel Griffin", email: "info@barrieheatingcooling.ca", business: "Affordable Comfort HVAC", type: "HVAC", status: "SENT", outreach_date: "2026-03-02" },
    { name: "Dr. Raf Bartosiak", email: "georgianshoresdentalcentre@gmail.com", business: "Georgian Shores Dental", type: "Dental", status: "SENT", outreach_date: "2026-03-02" },
    { name: "Mark Kehr", email: "info@thenorthwoodfitnessclub.com", business: "The Northwood Club", type: "Fitness", status: "SENT", outreach_date: "2026-03-02" },
    { name: "Daniel James", email: "info@vortexwellness.ca", business: "Vortex Wellness Studio", type: "Wellness", status: "SENT", outreach_date: "2026-03-02" },
    { name: "Colin", email: "colin@wilmecsystems.com", business: "Wilmec Plumbing Systems", type: "Plumbing", status: "SENT", outreach_date: "2026-03-02" },
    { name: "Engage Entertainment", email: "info@engageweddingdjs.com", business: "Engage Entertainment", type: "DJ/Performer", status: "SENT", outreach_date: "2026-03-02" },
    { name: "Supreme DJs", email: "info@supremedjs.ca", business: "Supreme DJs", type: "DJ/Performer", status: "SENT", outreach_date: "2026-03-02" },
    { name: "DJ Shayne", email: "shaynewilley@live.com", business: "DJ Shayne", type: "DJ/Performer", status: "SENT", outreach_date: "2026-03-02" }
];

async function syncLeads() {
    console.log("🛠️ Syncing leads to Supabase via REST...");

    for (const lead of leads) {
        const data = JSON.stringify(lead);
        const options = {
            hostname: SUPABASE_URL.replace('https://', '').split('.')[0] + '.' + SUPABASE_URL.split('.')[2],
            path: '/rest/v1/leads_outreach',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'apikey': SUPABASE_KEY,
                'Authorization': `Bearer ${SUPABASE_KEY}`,
                'Prefer': 'resolution=merge-duplicates'
            }
        };

        // Correct hostname logic
        const urlObj = new URL(SUPABASE_URL);
        options.hostname = urlObj.hostname;

        const req = https.request(options, (res) => {
            if (res.statusCode >= 200 && res.statusCode < 300) {
                console.log(`✅ Synced ${lead.name}`);
            } else {
                console.error(`❌ Error syncing ${lead.name}: Status ${res.statusCode}`);
            }
        });

        req.on('error', (e) => {
            console.error(`❌ Request error for ${lead.name}: ${e.message}`);
        });

        req.write(data);
        req.end();
    }
}

syncLeads();
