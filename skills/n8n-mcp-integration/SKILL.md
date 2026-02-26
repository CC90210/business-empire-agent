---
name: n8n-mcp-integration
description: Utilize the connected n8n supergateway MCP server to interact with and manage n8n workflows.
---

# Instructions

You have access to an `n8n-mcp` server integrated via `supergateway` using the Model Context Protocol. This skill activates when you need to interact with n8n workflows, test automations, or pull data from the CC's centralized n8n cloud instance.

## Operating Principles

1. **Workflow Analysis**: Use MCP to read existing n8n workflows before designing new ones. Understand the current logic, error handling, and node configurations.
2. **Triggering**: You can use the MCP connection to test triggers or execute specific workflows remotely.
3. **Best Practices Compliance**: Adhere strictly to the n8n Architecture Patterns laid out in `AGENT_CORE_DIRECTIVES.md`:
   - Every workflow must have error handling.
   - Use webhook triggers for integrations.
   - Employ retry logic for external API calls.
   - Document clearly in the project's `APPS_CONTEXT/OASIS_WORKFLOWS.md`.

## MCP Connection Context
- The MCP Server is named `n8n-mcp`.
- The instance URL is `https://n8n.srv993801.hstgr.cloud`.
- You also have access to the `N8N_API_KEY` system environment variable for raw HTTP API calls if the MCP server lacks a specific capability.

## Execution
Whenever the user requests you to manage, build, or list n8n workflows, leverage your available `n8n-mcp` MCP tools. Make sure to clearly state what you are doing, verify output, and never hallucinate node names or structures.
