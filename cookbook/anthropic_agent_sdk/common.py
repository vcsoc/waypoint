"""
Common utilities for Claude Agent SDK examples
"""

import os
import sys

import httpx


class Config:
    """Configuration for Waypoint Gateway connection"""

    # Waypoint proxy URL (default to local instance)
    LITELLM_PROXY_URL = os.getenv("WAYPOINT_PROXY_URL", "http://localhost:4000")

    # Waypoint API key (master key or virtual key)
    LITELLM_API_KEY = os.environ["WAYPOINT_API_KEY"]

    # Model name as configured in Waypoint (e.g., "bedrock-claude-sonnet-4", "gpt-4", etc.)
    LITELLM_MODEL = os.getenv("WAYPOINT_MODEL", "bedrock-claude-sonnet-4.5")


async def fetch_available_models(base_url: str, api_key: str) -> list[str]:
    """
    Fetch available models from Waypoint proxy /models endpoint
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()
            return [model["id"] for model in data.get("data", [])]
    except Exception as e:
        sys.stdout.write(f"⚠️  Warning: Could not fetch models from proxy: {e}" + "\n")
        sys.stdout.write("Using default model list..." + "\n")
        # Fallback to default models
        return [
            "bedrock-claude-sonnet-3.5",
            "bedrock-claude-sonnet-4",
            "bedrock-claude-sonnet-4.5",
            "bedrock-claude-opus-4.5",
            "bedrock-nova-premier",
        ]


def setup_litellm_env(config: Config):
    """
    Configure environment variables to point Agent SDK to Waypoint
    """
    litellm_base_url = config.LITELLM_PROXY_URL.rstrip("/")
    os.environ["ANTHROPIC_BASE_URL"] = litellm_base_url
    os.environ["ANTHROPIC_API_KEY"] = config.LITELLM_API_KEY
    return litellm_base_url


def print_header(base_url: str, current_model: str, has_mcp: bool = False):
    """
    Print the chat header
    """
    mcp_indicator = " + MCP" if has_mcp else ""
    sys.stdout.write(str("=" * 70) + "\n")
    sys.stdout.write(f"🤖 Claude Agent SDK with LiteLLM Gateway{mcp_indicator} - Interactive Chat" + "\n")
    sys.stdout.write(str("=" * 70) + "\n")
    sys.stdout.write(f"🚀 Connected to: {base_url}" + "\n")
    sys.stdout.write(f"📦 Current model: {current_model}" + "\n")
    if has_mcp:
        sys.stdout.write("🔌 MCP: deepwiki2 enabled" + "\n")
    sys.stdout.write("\nType your messages below. Commands:" + "\n")
    sys.stdout.write("  - 'quit' or 'exit' to end the conversation" + "\n")
    sys.stdout.write("  - 'clear' to start a new conversation" + "\n")
    sys.stdout.write("  - 'model' to switch models" + "\n")
    sys.stdout.write("  - 'models' to list available models" + "\n")
    sys.stdout.write(str("=" * 70) + "\n")
    sys.stdout.write("" + "\n")


def handle_model_list(available_models: list[str], current_model: str):
    """
    Display available models
    """
    sys.stdout.write("\n📋 Available models:" + "\n")
    for i, model in enumerate(available_models, 1):
        marker = "✓" if model == current_model else " "
        sys.stdout.write(f"  {marker} {i}. {model}" + "\n")


def handle_model_switch(
    available_models: list[str], current_model: str
) -> tuple[str, bool]:
    """
    Handle model switching

    Returns:
        tuple: (new_model, should_restart_conversation)
    """
    sys.stdout.write("\n📋 Select a model:" + "\n")
    for i, model in enumerate(available_models, 1):
        marker = "✓" if model == current_model else " "
        sys.stdout.write(f"  {marker} {i}. {model}" + "\n")

    try:
        choice = input("\nEnter number (or press Enter to cancel): ").strip()
        if choice:
            idx = int(choice) - 1
            if 0 <= idx < len(available_models):
                new_model = available_models[idx]
                sys.stdout.write(f"\n✅ Switched to: {new_model}" + "\n")
                sys.stdout.write("🔄 Starting new conversation with new model...\n" + "\n")
                return new_model, True
            else:
                sys.stdout.write("❌ Invalid choice" + "\n")
    except (ValueError, IndexError):
        sys.stdout.write("❌ Invalid input" + "\n")

    return current_model, False


async def stream_response(client, user_input: str):
    """
    Stream response from the agent
    """
    sys.stdout.write("\n🤖 Assistant: ")
    sys.stdout.flush()

    try:
        await client.query(user_input)

        # Show loading indicator
        sys.stdout.write("⏳ thinking...")
        sys.stdout.flush()

        # Stream the response
        first_chunk = True
        async for msg in client.receive_response():
            # Clear loading indicator on first message
            if first_chunk:
                sys.stdout.write("\r🤖 Assistant: ")
                sys.stdout.flush()
                first_chunk = False

            # Handle different message types
            if hasattr(msg, "type"):
                if msg.type == "content_block_delta":
                    # Streaming text delta
                    if hasattr(msg, "delta") and hasattr(msg.delta, "text"):
                        sys.stdout.write(str(msg.delta.text))
                        sys.stdout.flush()
                elif msg.type == "content_block_start":
                    # Start of content block
                    if hasattr(msg, "content_block") and hasattr(
                        msg.content_block, "text"
                    ):
                        sys.stdout.write(str(msg.content_block.text))
                        sys.stdout.flush()

            # Fallback to original content handling
            if hasattr(msg, "content"):
                for content_block in msg.content:
                    if hasattr(content_block, "text"):
                        sys.stdout.write(str(content_block.text))
                        sys.stdout.flush()

        sys.stdout.write("" + "\n")  # New line after response

    except Exception as e:
        sys.stdout.write(f"\r\n❌ Error: {e}" + "\n")
        sys.stdout.write("Please check your Waypoint gateway is running and configured correctly." + "\n")
