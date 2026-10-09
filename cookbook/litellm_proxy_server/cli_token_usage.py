#!/usr/bin/env python3
"""
Example: Using CLI token with Waypoint SDK

This example shows how to use the CLI authentication token
in your Python scripts after running `lite login`.
"""

import sys

import waypoint

LITELLM_BASE_URL = "http://localhost:4000/"


def main():
    """Using CLI token with Waypoint SDK"""
    sys.stdout.write("🚀 Using CLI Token with Waypoint SDK" + "\n")
    sys.stdout.write(str("=" * 40) + "\n")
    # waypoint._turn_on_debug()

    # Get the CLI token
    api_key = waypoint.get_litellm_gateway_api_key()

    if not api_key:
        sys.stdout.write("❌ No CLI token found. Please run 'lite login' first." + "\n")
        return

    sys.stdout.write("✅ Found CLI token." + "\n")

    available_models = waypoint.get_valid_models(
        check_provider_endpoint=True,
        custom_llm_provider="litellm_proxy",
        api_key=api_key,
        api_base=LITELLM_BASE_URL,
    )

    sys.stdout.write("✅ Available models:" + "\n")
    if available_models:
        for i, model in enumerate(available_models, 1):
            sys.stdout.write(f"   {i:2d}. {model}" + "\n")
    else:
        sys.stdout.write("   No models available" + "\n")

    # Use with Waypoint
    try:
        response = waypoint.completion(
            model="litellm_proxy/gemini/gemini-2.5-flash",
            messages=[{"role": "user", "content": "Hello from CLI token!"}],
            api_key=api_key,
            base_url=LITELLM_BASE_URL,
        )
        sys.stdout.write(f"✅ LLM Response: {response.model_dump_json(indent=4)}" + "\n")
    except Exception as e:
        sys.stdout.write(f"❌ Error: {e}" + "\n")


if __name__ == "__main__":
    main()

    sys.stdout.write("\n💡 Tips:" + "\n")
    sys.stdout.write("1. Run 'lite login' to authenticate first" + "\n")
    sys.stdout.write("2. Replace 'https://your-proxy.com' with your actual proxy URL" + "\n")
    sys.stdout.write(
        "3. The token is stored in your OS keychain, or in ~/.waypoint/token.json when there is none" + "\n"
    )
