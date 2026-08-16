import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

if not API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is not configured in the .env file."
    )

client = OpenAI(api_key=API_KEY)


def test_connection():
    response = client.responses.create(
        model=MODEL,
        input="Reply with exactly: AI connection successful",
    )

    print(response.output_text)


if __name__ == "__main__":
    test_connection()