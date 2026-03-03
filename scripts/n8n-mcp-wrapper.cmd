@echo off
REM n8n MCP Wrapper — reads credentials from .env.agents
REM This script is safe to commit to Git (no hardcoded keys)

set "ENV_FILE=%~dp0..\.env.agents"

REM Parse .env.agents for n8n credentials
for /f "usebackq tokens=1,* delims==" %%A in ("%ENV_FILE%") do (
    if "%%A"=="N8N_API_URL" set "N8N_API_URL=%%B"
    if "%%A"=="N8N_API_KEY" set "N8N_API_KEY=%%B"
    if "%%A"=="N8N_BEARER_TOKEN" set "N8N_BEARER_TOKEN=%%B"
)

set MCP_MODE=stdio
set LOG_LEVEL=error
set DISABLE_CONSOLE_OUTPUT=true

npx -y n8n-mcp
