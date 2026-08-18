import json
import os

from abc import ABC, abstractmethod

from google.api_core.exceptions import NotFound
from google.cloud import secretmanager

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
    def get_google_web_client_config(
        self,
    ) -> dict:
        """
        Return Google Web OAuth client configuration.
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

    def get_google_web_client_config(
        self,
    ) -> dict:
        """
        Return Google Web OAuth client configuration
        from the local JSON file.
        """

        client_file = (
            settings.google_web_client_file
        )

        if not client_file.exists():
            raise FileNotFoundError(
                "Google Web OAuth client file "
                f"not found: {client_file}"
            )

        try:
            return json.loads(
                client_file.read_text(
                    encoding="utf-8"
                )
            )

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Google Web OAuth client file "
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
    Return the configured secret backend.

    APP_ENV=local
        -> LocalSecretService

    APP_ENV=cloud
        -> GoogleSecretService
    """

    global _secret_service

    if _secret_service is None:
        if settings.is_cloud:
            _secret_service = (
                GoogleSecretService()
            )
        else:
            _secret_service = (
                LocalSecretService()
            )

    return _secret_service

class GoogleSecretService(SecretService):
    """
    Google Cloud Secret Manager implementation.

    Authentication is provided through Google
    Application Default Credentials.

    In Cloud Run, this normally resolves to the
    service account attached to the service.
    """

    def __init__(
        self,
        client=None,
    ):
        if not settings.gcp_project_id:
            raise RuntimeError(
                "GCP_PROJECT_ID is not configured."
            )

        self.project_id = (
            settings.gcp_project_id
        )

        self.client = (
            client
            if client is not None
            else secretmanager.SecretManagerServiceClient()
        )

    def _secret_name(
        self,
        secret_id: str,
    ) -> str:
        """
        Return the resource name of a secret.
        """

        return (
            f"projects/{self.project_id}"
            f"/secrets/{secret_id}"
        )

    def _secret_version_name(
        self,
        secret_id: str,
        version: str = "latest",
    ) -> str:
        """
        Return the resource name of a secret version.
        """

        return (
            f"{self._secret_name(secret_id)}"
            f"/versions/{version}"
        )

    def _access_secret(
        self,
        secret_id: str,
    ) -> str:
        """
        Read the latest secret value.
        """

        response = (
            self.client.access_secret_version(
                request={
                    "name": self._secret_version_name(
                        secret_id
                    )
                }
            )
        )

        return (
            response.payload.data.decode(
                "utf-8"
            )
        )

    def _add_secret_version(
        self,
        secret_id: str,
        value: str,
    ) -> None:
        """
        Add a new version to an existing secret.
        """

        self.client.add_secret_version(
            request={
                "parent": self._secret_name(
                    secret_id
                ),
                "payload": {
                    "data": value.encode(
                        "utf-8"
                    )
                },
            }
        )

    def get_openai_api_key(
        self,
    ) -> str:
        """
        Return the OpenAI API key.
        """

        value = self._access_secret(
            settings.openai_secret_id
        )

        if not value.strip():
            raise RuntimeError(
                "OpenAI API key secret is empty."
            )

        return value.strip()

    def get_google_client_config(
        self,
    ) -> dict:
        """
        Return Google OAuth client configuration.
        """

        raw_value = self._access_secret(
            settings.google_client_secret_id
        )

        try:
            return json.loads(
                raw_value
            )

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Google OAuth client secret "
                "contains invalid JSON."
            ) from exc

    def get_google_web_client_config(
        self,
    ) -> dict:
        """
        Return Google Web OAuth client configuration
        from Google Secret Manager.
        """

        raw_value = self._access_secret(
            settings.google_web_client_secret_id
        )

        try:
            return json.loads(
                raw_value
            )

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Google Web OAuth client secret "
                "contains invalid JSON."
            ) from exc

    def get_google_token_data(
        self,
    ) -> dict | None:
        """
        Return Google OAuth token data.

        A missing token secret/version is treated as
        'not authorised yet'.

        Other Secret Manager failures are not hidden.
        """

        try:
            raw_value = self._access_secret(
                settings.google_token_secret_id
            )

        except NotFound:
            return None

        if not raw_value.strip():
            return None

        try:
            return json.loads(
                raw_value
            )

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Google OAuth token secret "
                "contains invalid JSON."
            ) from exc

    def save_google_token_data(
        self,
        token_data: dict,
    ) -> None:
        """
        Persist refreshed Google OAuth token data
        as a new Secret Manager version.
        """

        self._add_secret_version(
            settings.google_token_secret_id,
            json.dumps(
                token_data,
                separators=(",", ":"),
            ),
        )