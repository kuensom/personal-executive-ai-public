import os
from abc import ABC, abstractmethod
from pathlib import Path

from app.config import settings


class SecretService(ABC):
    """
    Interface for accessing application secrets.

    Application code should depend on this interface
    rather than directly accessing environment
    variables or secret files.
    """

    @abstractmethod
    def get_openai_api_key(self) -> str:
        """
        Return the OpenAI API key.
        """
        raise NotImplementedError

    @abstractmethod
    def get_google_credentials_file(self) -> Path:
        """
        Return the Google OAuth client credentials file.
        """
        raise NotImplementedError

    @abstractmethod
    def get_google_token_file(self) -> Path:
        """
        Return the Google OAuth token file.
        """
        raise NotImplementedError


class LocalSecretService(SecretService):
    """
    Local-development secret provider.

    OpenAI:
        Read from the environment/.env.

    Google:
        Use local credentials.json and token.json.

    This preserves the application's existing
    local-development behaviour.
    """

    def get_openai_api_key(self) -> str:
        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        return api_key

    def get_google_credentials_file(self) -> Path:
        credentials_file = (
            settings.google_credentials_file
        )

        if not credentials_file.exists():
            raise FileNotFoundError(
                "Google OAuth credentials file "
                f"not found: {credentials_file}"
            )

        return credentials_file

    def get_google_token_file(self) -> Path:
        return settings.google_token_file


_secret_service: SecretService | None = None


def get_secret_service() -> SecretService:
    """
    Return the configured SecretService.

    Stage 3.0B currently supports local secrets.

    A Google Secret Manager implementation will
    be added for cloud deployment.
    """

    global _secret_service

    if _secret_service is None:
        _secret_service = LocalSecretService()

    return _secret_service