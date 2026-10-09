import base64
import os
import sys
import time

from openai import OpenAI

client = OpenAI(base_url="http://0.0.0.0:4001", api_key=os.environ["WAYPOINT_MASTER_KEY"])


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "waypoint/proxy/logo.png"

# Getting the Base64 string
base64_image = encode_image(image_path)


response = client.responses.create(
    model="bedrock/us.anthropic.claude-haiku-4-5-20251001-v1:0",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "what color is the image"},
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{base64_image}",
                },
            ],
        }
    ],
)


sys.stdout.write(str(response.output_text) + "\n")
sys.stdout.write(" ".join(str(_output_value) for _output_value in ("response1 id===", response.id)) + "\n")
sys.stdout.write("sleeping for 20 seconds..." + "\n")
time.sleep(20)
sys.stdout.write("making follow up request for existing id" + "\n")
response2 = client.responses.create(
    model="bedrock/us.anthropic.claude-haiku-4-5-20251001-v1:0",
    previous_response_id=response.id,
    input="ok, and what objects are in the image?",
)

sys.stdout.write(str(response2.output_text) + "\n")
