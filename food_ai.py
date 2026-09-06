from dotenv import load_dotenv
import os
import base64
import requests
import json

load_dotenv()

API_KEY = os.getenv("NVIDIA_API_KEY")

# Test API key
print("API key loaded:", API_KEY is not None)
print(
    "API key starts correctly:",
    API_KEY.startswith("nvapi-") if API_KEY else False
)


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

                        "text": """
You are an AI food analysis assistant.

Analyze the food in this image.

Your job is to identify the main dish and estimate its visible components.

IMPORTANT:
- Identify the main dish as ONE food.
- If the image contains chicken biryani, the dish name should be "Chicken biryani".
- Do not treat the ingredients as separate dishes.
- Identify the major visible components that make up the dish.
- Estimate the approximate weight in grams of each visible component.
- The weights are estimates only.
- The component weights should approximately add up to the total edible food portion.
- Do not invent tiny ingredients that cannot reasonably be seen.
- Do not include spices or invisible ingredients.
- Do not include the plate, bowl, cutlery, or other objects.
- Return ONLY valid JSON.
- Do not include explanations or markdown.

Return this exact JSON structure:

{
    "dish": "Chicken biryani",
    "estimated_total_weight_g": 300,
    "components": [
        {
            "name": "Rice",
            "estimated_weight_g": 220
        },
        {
            "name": "Chicken",
            "estimated_weight_g": 60
        },
        {
            "name": "Cashews",
            "estimated_weight_g": 5
        },
        {
            "name": "Raisins",
            "estimated_weight_g": 5
        },
        {
            "name": "Onion",
            "estimated_weight_g": 10
        }
    ]
}

If the image contains only one simple food such as a banana, return:

{
    "dish": "Banana",
    "estimated_total_weight_g": 120,
    "components": [
        {
            "name": "Banana",
            "estimated_weight_g": 120
        }
    ]
}
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

        "max_tokens": 300,
        "temperature": 0.2
    }

    response = requests.post(
        "https://integrate.api.nvidia.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    response.raise_for_status()

    result = response.json()

    text = result["choices"][0]["message"]["content"].strip()

    # Remove markdown code fences if the model adds them
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    data = json.loads(text)

    return data


if __name__ == "__main__":

    result = identify_food("test.jpg")

    print("\nDetected dish:")
    print(result["dish"])

    print("\nEstimated total weight:")
    print(result["estimated_total_weight_g"], "g")

    print("\nEstimated components:")

    for component in result["components"]:
        print(
            "-",
            component["name"],
            "~",
            component["estimated_weight_g"],
            "g"
        )