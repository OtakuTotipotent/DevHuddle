import json
from google import genai
from django.conf import settings

# Initialize the key from configs
client = genai.Client(api_key=settings.GEMINI_API_KEY)


def gemini_response(system_prompt, user_data):
    try:
        combined_prompt = (
            f"{system_prompt}\n\nHere is the data:\n{json.dumps(user_data, indent=2)}"
        )

        # API Cal
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=combined_prompt,
        )
        return response.text

    except Exception as e:
        return (
            f"**Error connecting to AI Provider:** {str(e)}\n\nPlease try again later."
        )
