import os
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()


class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.6-flash"

    def generate(self, prompt: str) -> str:

        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                return response.text

            except Exception as error:

                error_message = str(error)

                if "503" not in error_message:
                    raise

                if attempt == max_retries - 1:
                    raise

                wait_time = 2 ** attempt

                print(
                    f"Gemini unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

        raise RuntimeError("Gemini request failed.")
