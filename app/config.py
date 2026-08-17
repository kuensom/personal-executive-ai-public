import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

# Local development only.
# In Cloud Run these values will normally come from
# runtime configuration / Secret Manager.
load_dotenv(BASE_DIR / ".env")


class Settings:
    """
    Central application configuration.

    This class contains non-secret configuration and
    references to locally stored secrets.

    Secret retrieval itself will be moved behind
    SecretService in Stage 3.0B.
    """

    def __init__(self):
        self.environment = os.getenv(
            "APP_ENV",
            "local",
        )

        self.openai_model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5.6-luna",
        )

        self.google_credentials_file = Path(
            os.getenv(
                "GOOGLE_CREDENTIALS_FILE",
                str(BASE_DIR / "credentials.json"),
            )
        )

        self.google_token_file = Path(
            os.getenv(
                "GOOGLE_TOKEN_FILE",
                str(BASE_DIR / "token.json"),
            )
        )

        self.log_dir = Path(
            os.getenv(
                "LOG_DIR",
                str(BASE_DIR / "logs"),
            )
        )
        self.gcp_project_id = os.getenv(
            "GCP_PROJECT_ID",
            "",
        )

        self.openai_secret_id = os.getenv(
            "OPENAI_SECRET_ID",
            "personal-executive-ai-openai-key",
        )

        self.google_client_secret_id = os.getenv(
            "GOOGLE_CLIENT_SECRET_ID",
            "personal-executive-ai-google-client",
        )

        self.google_token_secret_id = os.getenv(
            "GOOGLE_TOKEN_SECRET_ID",
            "personal-executive-ai-google-token",
        )

    @property
    def is_cloud(self) -> bool:
        return self.environment.lower() == "cloud"

    @property
    def is_local(self) -> bool:
        return not self.is_cloud


settings = Settings()