from dotenv import load_dotenv
import os
import base64
import requests

load_dotenv()

API_KEY = os.getenv("NVIDIA_API_KEY")

#test
print("API key loaded:", API_KEY is not None)
print("API key starts correctly:", API_KEY.startswith("nvapi-") if API_KEY else False)

def identify_food(image_path):

    with open(image_path, "rb") as image:
        image_data = base64.b64encode(image.read()).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta/llama-3.2-11b-vision-instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Identify the main food item in this image.

Return only the common food name.
Do not include explanations, punctuation, quantities, or nutritional information.

Examples:
Banana
Apple
Rice
Chicken biryani
Dosa
Idli
Chapati
Samosa
"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 50,
        "temperature": 0.2
    }

    response = requests.post(
        "https://integrate.api.nvidia.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    food = identify_food("test.jpg")
    print("Detected food:", food)