const dotenv = require('dotenv');
dotenv.config({ path: '.env.agents' });
const NOTION_API_KEY = process.env.NOTION_API_KEY;
const DAILY_TASKS_DB = process.env.NOTION_DAILY_TASKS_ID;

async function createPage(taskName, priority, dayType, instructions) {
  try {
    const response = await fetch(
      "https://api.notion.com/v1/pages",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${NOTION_API_KEY}`,
          "Content-Type": "application/json",
          "Notion-Version": "2022-06-28"
        },
        body: JSON.stringify({
          parent: { database_id: DAILY_TASKS_DB },
          properties: {
            "Task Name": { title: [{ text: { content: taskName } }] },
            Priority: { select: { name: priority } },
            "Day Type": { select: { name: dayType } },
            "Detailed Instructions": { rich_text: [{ text: { content: instructions } }] }
          }
        })
      }
    );
    if (!response.ok) {
      const errorData = await response.json();
      console.error(`Error creating ${taskName}:`, errorData);
    } else {
      console.log(`Created: ${taskName}`);
    }
  } catch (error) {
    console.error(`Error creating ${taskName}:`, error.message);
  }
}

async function sync() {
  await createPage(
    "Record 5 Short-form Content Pieces", 
    "🔴 Critical", 
    "MAKER",
    "Record the 5 scripts in memory/daily/2026-03-01_content_scripts.md. Focus on raw, handheld takes with natural lighting. Upload to media/raw/ once done."
  );
  await createPage(
    "Build Revenue Hunter n8n workflow", 
    "🟡 High", 
    "MAKER",
    "Create a new n8n workflow that monitors high-intent signals (e.g. specific LinkedIn interactions or website visits) and triggers a notification to Telegram. Ensure 3x exponential backoff on all API nodes."
  );
  await createPage(
    "Edit & Deploy First IG Reel", 
    "🟡 High", 
    "MANAGER",
    "Run scripts/edit_content.py on Monday's raw footage. Add screenshots/icons from media/raw to the overlay. Review draft for 'viral hooks' before scheduling via Late MCP."
  );
  await createPage(
    "PropFlow Feature Sprint", 
    "🟢 Medium", 
    "MAKER",
    "Refactor the property transaction engine for higher throughput. Optimize Supabase queries and add edge caching for public listings."
  );
  await createPage(
    "Weekly Empire Audit", 
    "🟡 High", 
    "MANAGER",
    "Run /monthly-audit command. Review all 3 brand financials in Stripe. Prune dead n8n workflows. Update brain/STATE.md for the new week."
  );
}

sync();
