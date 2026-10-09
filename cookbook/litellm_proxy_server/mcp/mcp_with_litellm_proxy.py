"""
Use Waypoint Proxy MCP Gateway to call MCP tools.

When using Waypoint Proxy, you can use the same MCP tools across all your LLM providers.
"""

import os
import sys

import openai

client = openai.OpenAI(
    api_key=os.environ["WAYPOINT_MASTER_KEY"],
    base_url="http://localhost:4000",  # paste your litellm proxy base url here
)
sys.stdout.write("Making API request to Responses API with MCP tools" + "\n")

response = client.responses.create(
    model="gpt-5",
    input=[
        {
            "role": "user",
            "content": "give me TLDR of what BerriAI/litellm repo is about",
            "type": "message",
        }
    ],
    tools=[
        {
            "type": "mcp",
            "server_label": "waypoint",
            "server_url": "litellm_proxy",
            "require_approval": "never",
        }
    ],
    stream=True,
    tool_choice="required",
)

for chunk in response:
    sys.stdout.write(" ".join(str(_output_value) for _output_value in ("response chunk: ", chunk)) + "\n")
