import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)


def ask_ai(prompt):
    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return response.output_text