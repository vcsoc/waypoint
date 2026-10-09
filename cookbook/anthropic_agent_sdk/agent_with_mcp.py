"""
Interactive Claude Agent SDK CLI with MCP Support

This example demonstrates an interactive CLI chat with the Anthropic Agent SDK using Waypoint as a proxy,
with MCP (Model Context Protocol) server integration for enhanced capabilities.
"""

import asyncio
import os
import sys

from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient
from common import (
    Config,
    fetch_available_models,
    handle_model_list,
    handle_model_switch,
    print_header,
    setup_litellm_env,
    stream_response,
)


async def interactive_chat_with_mcp():
    """
    Interactive CLI chat with the agent and MCP server
    """
    config = Config()

    # Configure Anthropic SDK to point to Waypoint gateway
    litellm_base_url = setup_litellm_env(config)

    # Fetch available models from proxy
    available_models = await fetch_available_models(
        litellm_base_url, config.LITELLM_API_KEY
    )

    current_model = config.LITELLM_MODEL

    # MCP server configuration
    mcp_server_url = f"{litellm_base_url}/mcp/deepwiki2"
    use_mcp = os.getenv("USE_MCP", "true").lower() == "true"

    if not use_mcp:
        sys.stdout.write("⚠️  MCP disabled via USE_MCP=false" + "\n")

    print_header(litellm_base_url, current_model, has_mcp=use_mcp)

    while True:
        # Configure agent options
        if use_mcp:
            try:
                # Try with MCP server (HTTP transport)
                # Using McpHttpServerConfig format from Agent SDK
                options = ClaudeAgentOptions(
                    system_prompt="You are a helpful AI assistant with access to DeepWiki for research. Be concise, accurate, and friendly.",
                    model=current_model,
                    max_turns=50,
                    mcp_servers={
                        "deepwiki2": {
                            "type": "http",
                            "url": mcp_server_url,
                            "headers": {
                                "Authorization": f"Bearer {config.LITELLM_API_KEY}"
                            },
                        }
                    },
                )
            except Exception as e:
                sys.stdout.write(f"⚠️  Warning: Could not configure MCP server: {e}" + "\n")
                sys.stdout.write("Continuing without MCP...\n" + "\n")
                use_mcp = False
                options = ClaudeAgentOptions(
                    system_prompt="You are a helpful AI assistant. Be concise, accurate, and friendly.",
                    model=current_model,
                    max_turns=50,
                )
        else:
            # Without MCP
            options = ClaudeAgentOptions(
                system_prompt="You are a helpful AI assistant. Be concise, accurate, and friendly.",
                model=current_model,
                max_turns=50,
            )

        # Create agent client
        try:
            async with ClaudeSDKClient(options=options) as client:
                conversation_active = True

                while conversation_active:
                    # Get user input
                    try:
                        user_input = input("\n👤 You: ").strip()
                    except (EOFError, KeyboardInterrupt):
                        sys.stdout.write("\n\n👋 Goodbye!" + "\n")
                        return

                    # Handle commands
                    if user_input.lower() in ["quit", "exit"]:
                        sys.stdout.write("\n👋 Goodbye!" + "\n")
                        return

                    if user_input.lower() == "clear":
                        sys.stdout.write("\n🔄 Starting new conversation...\n" + "\n")
                        conversation_active = False
                        continue

                    if user_input.lower() == "models":
                        handle_model_list(available_models, current_model)
                        continue

                    if user_input.lower() == "model":
                        new_model, should_restart = handle_model_switch(
                            available_models, current_model
                        )
                        if should_restart:
                            current_model = new_model
                            conversation_active = False
                        continue

                    if not user_input:
                        continue

                    # Stream response from agent
                    await stream_response(client, user_input)

        except Exception as e:
            sys.stdout.write(f"\n❌ Error creating agent client: {e}" + "\n")
            sys.stdout.write("This might be an MCP configuration issue. Try running without MCP:" + "\n")
            sys.stdout.write("  USE_MCP=false python agent_with_mcp.py" + "\n")
            sys.stdout.write("\nOr use the basic agent:" + "\n")
            sys.stdout.write("  python main.py" + "\n")
            return


def main():
    """Run interactive chat with MCP"""
    try:
        asyncio.run(interactive_chat_with_mcp())
    except KeyboardInterrupt:
        sys.stdout.write("\n\n👋 Goodbye!" + "\n")


if __name__ == "__main__":
    main()
