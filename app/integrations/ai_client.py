import os

from openai import OpenAI

from app.config import settings


MODEL = settings.openai_model


def get_openai_client() -> OpenAI:
    """
    Return an authenticated OpenAI client.

    Local development currently reads the API key
    from the environment.

    Cloud secret retrieval will be introduced through
    SecretService in Stage 3.0B.
    """

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured."
        )

    return OpenAI(
        api_key=api_key
    )


def test_connection():
    client = get_openai_client()

    response = client.responses.create(
        model=MODEL,
        input=(
            "Reply with exactly: "
            "AI connection successful"
        ),
    )

    print(
        response.output_text
    )


if __name__ == "__main__":
    test_connection()