#!/usr/bin/env python3
"""
Complete example for Veo video generation through Waypoint proxy.

This script demonstrates how to:
1. Generate videos using Google's Veo model
2. Poll for completion status
3. Download the generated video file

Requirements:
- Waypoint proxy running with Google AI Studio pass-through configured
- Google AI Studio API key with Veo access
"""

import json
import os
import sys
import time

import requests


class VeoVideoGenerator:
    """Complete Veo video generation client using Waypoint proxy."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "http://localhost:4000/gemini/v1beta",
    ):
        """
        Initialize the Veo video generator.

        Args:
            base_url: Base URL for the Waypoint proxy with Gemini pass-through
            api_key: API key for Waypoint proxy authentication
        """
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}

    def generate_video(self, prompt: str) -> str | None:
        """
        Initiate video generation with Veo.

        Args:
            prompt: Text description of the video to generate

        Returns:
            Operation name if successful, None otherwise
        """
        sys.stdout.write(f"🎬 Generating video with prompt: '{prompt}'" + "\n")

        url = f"{self.base_url}/models/veo-3.0-generate-preview:predictLongRunning"
        payload = {"instances": [{"prompt": prompt}]}

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()

            data = response.json()
            operation_name = data.get("name")

            if operation_name:
                sys.stdout.write(f"✅ Video generation started: {operation_name}" + "\n")
                return operation_name
            else:
                sys.stdout.write("❌ No operation name returned" + "\n")
                sys.stdout.write(f"Response: {json.dumps(data, indent=2)}" + "\n")
                return None

        except requests.RequestException as e:
            sys.stdout.write(f"❌ Failed to start video generation: {e}" + "\n")
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_data = e.response.json()
                    sys.stdout.write(f"Error details: {json.dumps(error_data, indent=2)}" + "\n")
                except ValueError:
                    sys.stdout.write(f"Error response: {e.response.text}" + "\n")
            return None

    def wait_for_completion(self, operation_name: str, max_wait_time: int = 600) -> str | None:
        """
        Poll operation status until video generation is complete.

        Args:
            operation_name: Name of the operation to monitor
            max_wait_time: Maximum time to wait in seconds (default: 10 minutes)

        Returns:
            Video URI if successful, None otherwise
        """
        sys.stdout.write("⏳ Waiting for video generation to complete..." + "\n")

        operation_url = f"{self.base_url}/{operation_name}"
        start_time = time.time()
        poll_interval = 10  # Start with 10 seconds

        while time.time() - start_time < max_wait_time:
            try:
                sys.stdout.write(f"🔍 Polling status... ({int(time.time() - start_time)}s elapsed)" + "\n")

                response = requests.get(operation_url, headers=self.headers, timeout=30)
                response.raise_for_status()

                data = response.json()

                # Check for errors
                if "error" in data:
                    sys.stdout.write("❌ Error in video generation:" + "\n")
                    sys.stdout.write(str(json.dumps(data["error"], indent=2)) + "\n")
                    return None

                # Check if operation is complete
                is_done = data.get("done", False)

                if is_done:
                    sys.stdout.write("🎉 Video generation complete!" + "\n")

                    try:
                        # Extract video URI from nested response
                        video_uri = data["response"]["generateVideoResponse"][
                            "generatedSamples"
                        ][0]["video"]["uri"]
                        sys.stdout.write(f"📹 Video URI: {video_uri}" + "\n")
                        return video_uri
                    except KeyError as e:
                        sys.stdout.write(f"❌ Could not extract video URI: {e}" + "\n")
                        sys.stdout.write("Full response:" + "\n")
                        sys.stdout.write(str(json.dumps(data, indent=2)) + "\n")
                        return None

                # Wait before next poll, with exponential backoff
                time.sleep(poll_interval)
                poll_interval = min(poll_interval * 1.2, 30)  # Cap at 30 seconds

            except requests.RequestException as e:
                sys.stdout.write(f"❌ Error polling operation status: {e}" + "\n")
                time.sleep(poll_interval)

        sys.stdout.write(f"⏰ Timeout after {max_wait_time} seconds" + "\n")
        return None

    def download_video(
        self, video_uri: str, output_filename: str = "generated_video.mp4"
    ) -> bool:
        """
        Download the generated video file.

        Args:
            video_uri: URI of the video to download (from Google's response)
            output_filename: Local filename to save the video

        Returns:
            True if download successful, False otherwise
        """
        sys.stdout.write("⬇️  Downloading video..." + "\n")
        sys.stdout.write(f"Original URI: {video_uri}" + "\n")

        # Convert Google URI to Waypoint proxy URI
        # Example: files/abc123 -> /gemini/v1beta/files/abc123:download?alt=media
        if video_uri.startswith("files/"):
            download_path = f"{video_uri}:download?alt=media"
        else:
            download_path = video_uri

        litellm_download_url = f"{self.base_url}/{download_path}"
        sys.stdout.write(f"Download URL: {litellm_download_url}" + "\n")

        try:
            # Download with streaming and redirect handling
            response = requests.get(
                litellm_download_url,
                headers=self.headers,
                stream=True,
                allow_redirects=True,  # Handle redirects automatically
                timeout=30,
            )
            response.raise_for_status()

            # Save video file
            with open(output_filename, "wb") as f:
                downloaded_size = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)

                        # Progress indicator for large files
                        if downloaded_size % (1024 * 1024) == 0:  # Every MB
                            sys.stdout.write(f"📦 Downloaded {downloaded_size / (1024 * 1024):.1f} MB..." + "\n")

            # Verify file was created and has content
            if os.path.exists(output_filename):
                file_size = os.path.getsize(output_filename)
                if file_size > 0:
                    sys.stdout.write("✅ Video downloaded successfully!" + "\n")
                    sys.stdout.write(f"📁 Saved as: {output_filename}" + "\n")
                    sys.stdout.write(f"📏 File size: {file_size / (1024 * 1024):.2f} MB" + "\n")
                    return True
                else:
                    sys.stdout.write("❌ Downloaded file is empty" + "\n")
                    os.remove(output_filename)
                    return False
            else:
                sys.stdout.write("❌ File was not created" + "\n")
                return False

        except requests.RequestException as e:
            sys.stdout.write(f"❌ Download failed: {e}" + "\n")
            if hasattr(e, "response") and e.response is not None:
                sys.stdout.write(f"Status code: {e.response.status_code}" + "\n")
                sys.stdout.write(f"Response headers: {dict(e.response.headers)}" + "\n")
            return False

    def generate_and_download(self, prompt: str, output_filename: str = None) -> bool:
        """
        Complete workflow: generate video and download it.

        Args:
            prompt: Text description for video generation
            output_filename: Output filename (auto-generated if None)

        Returns:
            True if successful, False otherwise
        """
        # Auto-generate filename if not provided
        if output_filename is None:
            timestamp = int(time.time())
            safe_prompt = "".join(
                c for c in prompt[:30] if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            output_filename = (
                f"veo_video_{safe_prompt.replace(' ', '_')}_{timestamp}.mp4"
            )

        sys.stdout.write(str("=" * 60) + "\n")
        sys.stdout.write("🎬 VEO VIDEO GENERATION WORKFLOW" + "\n")
        sys.stdout.write(str("=" * 60) + "\n")

        # Step 1: Generate video
        operation_name = self.generate_video(prompt)
        if not operation_name:
            return False

        # Step 2: Wait for completion
        video_uri = self.wait_for_completion(operation_name)
        if not video_uri:
            return False

        # Step 3: Download video
        success = self.download_video(video_uri, output_filename)

        if success:
            sys.stdout.write(str("=" * 60) + "\n")
            sys.stdout.write("🎉 SUCCESS! Video generation complete!" + "\n")
            sys.stdout.write(f"📁 Video saved as: {output_filename}" + "\n")
            sys.stdout.write(str("=" * 60) + "\n")
        else:
            sys.stdout.write(str("=" * 60) + "\n")
            sys.stdout.write("❌ FAILED! Video generation or download failed" + "\n")
            sys.stdout.write(str("=" * 60) + "\n")

        return success


def main():
    """
    Example usage of the VeoVideoGenerator.

    Configure these environment variables:
    - WAYPOINT_BASE_URL: Your Waypoint proxy URL (default: http://localhost:4000/gemini/v1beta)
    - WAYPOINT_API_KEY: API key for Waypoint proxy authentication
    """

    # Configuration from environment or defaults
    base_url = os.getenv("WAYPOINT_BASE_URL", "http://localhost:4000/gemini/v1beta")
    api_key = os.environ["WAYPOINT_API_KEY"]

    sys.stdout.write("🚀 Starting Veo Video Generation Example" + "\n")
    sys.stdout.write(f"📡 Using LiteLLM proxy at: {base_url}" + "\n")

    # Initialize generator
    generator = VeoVideoGenerator(base_url=base_url, api_key=api_key)

    # Example prompts - try different ones!
    example_prompts = [
        "A cat playing with a ball of yarn in a sunny garden",
        "Ocean waves crashing against rocky cliffs at sunset",
        "A bustling city street with people walking and cars passing by",
        "A peaceful forest with sunlight filtering through the trees",
    ]

    # Use first example or get from user
    prompt = example_prompts[0]
    sys.stdout.write(f"🎬 Using prompt: '{prompt}'" + "\n")

    # Generate and download video
    success = generator.generate_and_download(prompt)

    if success:
        sys.stdout.write("\n✅ Example completed successfully!" + "\n")
        sys.stdout.write("💡 Try modifying the prompt in the script for different videos!" + "\n")
    else:
        sys.stdout.write("\n❌ Example failed!" + "\n")
        sys.stdout.write("🔧 Check your Waypoint proxy configuration and Google AI Studio API key" + "\n")

        # Troubleshooting tips
        sys.stdout.write("\n🔍 Troubleshooting:" + "\n")
        sys.stdout.write("1. Ensure Waypoint proxy is running with Google AI Studio pass-through" + "\n")
        sys.stdout.write("2. Verify your Google AI Studio API key has Veo access" + "\n")
        sys.stdout.write("3. Check that your prompt meets Veo's content guidelines" + "\n")
        sys.stdout.write("4. Review the Waypoint proxy logs for detailed error information" + "\n")


if __name__ == "__main__":
    main()
