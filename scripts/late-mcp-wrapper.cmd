@echo off
REM Late MCP Wrapper — reads credentials from .env.agents
REM This script is safe to commit to Git (no hardcoded keys)

set "ENV_FILE=%~dp0..\.env.agents"

REM Parse .env.agents for Late API key
for /f "usebackq tokens=1,* delims==" %%A in ("%ENV_FILE%") do (
    if "%%A"=="LATE_API_KEY" set "LATE_API_KEY=%%B"
)

uvx --from "late-sdk[mcp]" python "%~dp0late_mcp_patched.py"
