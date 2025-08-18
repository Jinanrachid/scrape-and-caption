import base64
import boto3
import json


# AWS Bedrock Client
client = boto3.client("bedrock-runtime", region_name="us-west-2")

# Vision-enabled Claude model
model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"

# Structured prompt for Fahion designer
prompt = f"""
Analyze this image and generate a professional caption for it.

Requirements:
1. Start by identifying the item (e.g., leather shoes, silk dress).
2. Provide a detailed description highlighting material, texture, color, and design details in a structured way.
3. Keep it professional, clear and accurate.
4. Use a formal tone suitable for fashion industry professionals.
5. Use simple readable symbols for CSV files:
    - Use dashes (-) or bullets (*) for lists
    - Avoid special characters like emojis or quotes
6. add these sections:
    -Item name (don't include the word "item name")
    -Product Details:
    -Key Design Features:
    -Construction Details:
    -Styling Notes:
"""

def creat_native_request(prompt, image_base64):
    # Build request payload
    native_request = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 512,  # short captions
    "temperature": 0.5,
    "system": "role:You are a professional fashion designer",
    "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image", "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_base64
                }},
            ],
        }],

}
    return native_request


def generate_caption(img_file, prompt=prompt):
    """Send image to Claude and get the caption."""
    try:
        image_base64 = base64.b64encode(img_file.read()).decode("utf-8")
        payload_model = creat_native_request(prompt, image_base64)

        # Invoke Claude
        request_body = json.dumps(payload_model)
        response = client.invoke_model(modelId=model_id, body=request_body)

        model_response = json.loads(response["body"].read())
        return model_response["content"][0]["text"]

    except Exception as e:
        print(f"Error processing {img_file}: {e}")
        return None


