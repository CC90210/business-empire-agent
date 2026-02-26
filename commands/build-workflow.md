Build an n8n workflow for the following use case: $ARGUMENTS

Follow this process:

1. Check existing workflows via n8n-mcp MCP — do NOT duplicate existing workflows
2. Read `skills/n8n-patterns.md` for pattern reference
3. Clarify the automation goal — what triggers it, what it does, what the output is
4. Design the node flow (list each node in order with its type and purpose)
5. Write the complete workflow JSON with:
   - Descriptive node naming ("Fetch Lead from ClearBit" not "HTTP Request 1")
   - Error Trigger → notification node
   - Retry logic on API calls (3 attempts, 1000ms exponential backoff)
   - Credential placeholders (NEVER actual keys)
   - Start sticky note explaining purpose and expected behavior
   - Timeout on HTTP nodes (30s default)
6. Save the JSON to `workflows/[name].json`
7. Update `APPS_CONTEXT/OASIS_WORKFLOWS.md` with the new entry
8. Write a brief README: trigger, inputs, outputs, credentials needed, setup steps

If the workflow involves AI/LLM calls, include proper prompt engineering with system prompts and output parsing.
If ANY step fails, stop and report why.
