import json
import os

from abc import ABC, abstractmethod

from app.config import settings


class SecretService(ABC):
    """
    Interface for retrieving and persisting
    application secrets.

    Application and integration code should not
    need to know where secrets are physically stored.
    """

    @abstractmethod
    def get_openai_api_key(self) -> str:
        """Return the OpenAI API key."""
        raise NotImplementedError

    @abstractmethod
    def get_google_client_config(self) -> dict:
        """
        Return the Google OAuth client configuration.
        """
        raise NotImplementedError

    @abstractmethod
    def get_google_token_data(self) -> dict | None:
        """
        Return stored Google OAuth token data.

        Returns None when no token has yet been stored.
        """
        raise NotImplementedError

    @abstractmethod
    def save_google_token_data(
        self,
        token_data: dict,
    ) -> None:
        """
        Persist Google OAuth token data.
        """
        raise NotImplementedError


class LocalSecretService(SecretService):
    """
    Secret provider for local development.

    OpenAI secrets are read from the environment.

    Google OAuth client configuration and token data
    are read from and written to local JSON files.

    The cloud implementation will use Google
    Secret Manager instead.
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

    def get_google_client_config(self) -> dict:
        credentials_file = (
            settings.google_credentials_file
        )

        if not credentials_file.exists():
            raise FileNotFoundError(
                "Google OAuth credentials file "
                f"not found: {credentials_file}"
            )

        try:
            return json.loads(
                credentials_file.read_text(
                    encoding="utf-8"
                )
            )
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Google OAuth credentials file "
                "contains invalid JSON."
            ) from exc

    def get_google_token_data(
        self,
    ) -> dict | None:
        token_file = (
            settings.google_token_file
        )

        if not token_file.exists():
            return None

        try:
            return json.loads(
                token_file.read_text(
                    encoding="utf-8"
                )
            )
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Google OAuth token file "
                "contains invalid JSON."
            ) from exc

    def save_google_token_data(
        self,
        token_data: dict,
    ) -> None:
        token_file = (
            settings.google_token_file
        )

        token_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        token_file.write_text(
            json.dumps(
                token_data,
                indent=2,
            ),
            encoding="utf-8",
        )


_secret_service: SecretService | None = None


def get_secret_service() -> SecretService:
    """
    Return the configured SecretService.

    LocalSecretService is currently used for local
    development.

    Environment-based selection will be introduced
    when GoogleSecretService is implemented.
    """

    global _secret_service

    if _secret_service is None:
        _secret_service = LocalSecretService()

    return _secret_service