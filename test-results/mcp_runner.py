import asyncio
import json
from pathlib import Path
from mcp.client.streamable_http import streamable_http_client, httpx2
from mcp import ClientSession

import os
import sys

def get_api_key():
    key = os.getenv("FORTYGUARD_API_KEY") or os.getenv("API_KEY")
    if not key:
        env_file = Path(__file__).resolve().parent.parent / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "api-key" in line.lower() or "api_key" in line.lower():
                    parts = line.split(":", 1) if ":" in line else line.split("=", 1)
                    if len(parts) == 2:
                        key = parts[1].strip().strip('"').strip("'")
                        break
            if not key:
                content = env_file.read_text(encoding="utf-8").strip()
                if not any(c in content for c in ("\n", " ")):
                    key = content.replace("api-key:", "").replace("api_key=", "").strip()
    if not key:
        print("Error: FORTYGUARD_API_KEY not found in environment or .env file.")
        print("To verify existing MCP tool execution traces offline, run:")
        print("  pytest tests/test_validation_suite.py")
        sys.exit(1)
    return key

MCP_URL = "https://tos-mcp.app.fortyguard.com/mcp"
API_KEY = get_api_key()
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
RESULTS_DIR = Path(__file__).resolve().parent

async def test_tools():
    # 1. credit_balance
    async with httpx2.AsyncClient(headers=HEADERS, timeout=60.0) as client:
        async with streamable_http_client(MCP_URL, http_client=client) as (r, w):
            async with ClientSession(r, w) as sess:
                await sess.initialize()
                res = await sess.call_tool("credit_balance", {})
                cb_texts = [getattr(c, "text", str(c)) for c in res.content]
                (RESULTS_DIR / "3.2_mcp_credit_balance.json").write_text(json.dumps({"content": cb_texts, "is_error": res.is_error}, indent=2))
                print("credit_balance:", cb_texts[0][:150])

    await asyncio.sleep(2)

    # 2. env_params
    async with httpx2.AsyncClient(headers=HEADERS, timeout=60.0) as client:
        async with streamable_http_client(MCP_URL, http_client=client) as (r, w):
            async with ClientSession(r, w) as sess:
                await sess.initialize()
                payload = {
                    "latitude": 33.4484,
                    "longitude": -112.074,
                    "temperature": 35.0,
                    "date_time": {
                        "start_date": "2024-07-15",
                        "start_time": "14:00",
                        "filter_type": 1
                    }
                }
                res = await sess.call_tool("env_params", payload)
                env_texts = [getattr(c, "text", str(c)) for c in res.content]
                (RESULTS_DIR / "3.3_mcp_env_params_result.json").write_text(json.dumps({"content": env_texts, "is_error": res.is_error}, indent=2))
                print("env_params:", env_texts[0][:150])

asyncio.run(test_tools())
