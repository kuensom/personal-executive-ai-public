import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import (
    InstalledAppFlow,
)

from app.services.secret_service import (
    get_secret_service,
)


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
]


def get_google_credentials() -> Credentials:
    """
    Return valid Google OAuth credentials.

    Credential storage is delegated entirely to
    SecretService.

    This allows local development to use JSON files
    while cloud deployment can later use
    Google Secret Manager.
    """

    secret_service = get_secret_service()

    token_data = (
        secret_service.get_google_token_data()
    )

    creds = None

    if token_data:
        creds = Credentials.from_authorized_user_info(
            token_data,
            SCOPES,
        )

    if not creds or not creds.valid:
        if (
            creds
            and creds.expired
            and creds.refresh_token
        ):
            creds.refresh(
                Request()
            )

        else:
            client_config = (
                secret_service
                .get_google_client_config()
            )

            flow = (
                InstalledAppFlow
                .from_client_config(
                    client_config,
                    SCOPES,
                )
            )

            creds = flow.run_local_server(
                port=0
            )

        token_json = creds.to_json()

        secret_service.save_google_token_data(
            json.loads(token_json)
        )

    return creds


if __name__ == "__main__":
    credentials = (
        get_google_credentials()
    )

    print(
        "Google authentication successful."
    )

    print(
        f"Token valid: {credentials.valid}"
    )