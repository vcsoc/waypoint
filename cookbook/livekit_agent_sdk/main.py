"""
Simple xAI Voice Agent using LiveKit SDK with Waypoint Gateway

This example shows how to use LiveKit's xAI realtime plugin through Waypoint proxy.
Waypoint acts as a unified interface, allowing you to switch between xAI, OpenAI, 
and Azure realtime APIs without changing your agent code.
"""

import asyncio
import json
import os
import sys

import websockets

# Configuration
PROXY_URL = os.getenv("WAYPOINT_PROXY_URL", "http://localhost:4000")
API_KEY = os.environ["WAYPOINT_API_KEY"]
MODEL = os.getenv("WAYPOINT_MODEL", "grok-voice-agent")


async def run_voice_agent():
    """
    Simple voice agent that:
    1. Connects to xAI realtime API through Waypoint proxy
    2. Sends a user message
    3. Streams back the response
    """

    url = f"ws://{PROXY_URL.replace('http://', '').replace('https://', '')}/v1/realtime?model={MODEL}"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    sys.stdout.write("🎙️  Connecting to voice agent..." + "\n")
    sys.stdout.write(f"   Model: {MODEL}" + "\n")
    sys.stdout.write(f"   Proxy: {PROXY_URL}" + "\n")
    sys.stdout.write("" + "\n")

    async with websockets.connect(url, additional_headers=headers) as ws:
        # Receive initial connection event
        initial = json.loads(await ws.recv())
        sys.stdout.write(f"✅ Connected! Event: {initial['type']}\n" + "\n")

        # Get user input
        user_message = input("💬 Your message: ").strip()
        if not user_message:
            user_message = "Tell me a fun fact about AI!"

        sys.stdout.write(f"\n🤖 Sending to {MODEL}...\n" + "\n")

        # Send user message
        await ws.send(
            json.dumps(
                {
                    "type": "conversation.item.create",
                    "item": {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": user_message}],
                    },
                }
            )
        )

        # Request response
        await ws.send(
            json.dumps(
                {
                    "type": "response.create",
                    "response": {"modalities": ["text", "audio"]},
                }
            )
        )

        # Stream response
        sys.stdout.write("🎤 Response: ")
        sys.stdout.flush()
        transcript = []

        try:
            while True:
                msg = await asyncio.wait_for(ws.recv(), timeout=15.0)
                event = json.loads(msg)

                # Capture transcript deltas
                if event["type"] == "response.output_audio_transcript.delta":
                    delta = event.get("delta", "")
                    if delta:
                        sys.stdout.write(str(delta))
                        sys.stdout.flush()
                        transcript.append(delta)

                # Done when response completes
                elif event["type"] == "response.done":
                    break

        except asyncio.TimeoutError:
            pass

        sys.stdout.write("\n" + "\n")

        if transcript:
            sys.stdout.write(f"✅ Complete response: {''.join(transcript)}" + "\n")

        await ws.close()


def main():
    """Run the voice agent"""
    sys.stdout.write(str("=" * 70) + "\n")
    sys.stdout.write("LiveKit xAI Voice Agent via Waypoint Proxy" + "\n")
    sys.stdout.write(str("=" * 70) + "\n")
    sys.stdout.write("" + "\n")

    try:
        asyncio.run(run_voice_agent())
    except KeyboardInterrupt:
        sys.stdout.write("\n\n👋 Goodbye!" + "\n")
    except Exception as e:
        sys.stdout.write(f"\n❌ Error: {e}" + "\n")
        sys.stdout.write("\nMake sure Waypoint proxy is running:" + "\n")
        sys.stdout.write("  litellm --config config.yaml --port 4000" + "\n")


if __name__ == "__main__":
    main()
