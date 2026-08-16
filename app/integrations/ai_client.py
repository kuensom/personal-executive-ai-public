from openai import OpenAI

from app.config import settings
from app.services.secret_service import (
    get_secret_service,
)


MODEL = settings.openai_model


def get_openai_client() -> OpenAI:
    """
    Return an authenticated OpenAI client.

    Secret retrieval is delegated to SecretService
    so this integration does not need to know where
    the API key is stored.
    """

    secret_service = get_secret_service()

    api_key = (
        secret_service.get_openai_api_key()
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