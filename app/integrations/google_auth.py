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

    Secret file locations are obtained through
    SecretService rather than being hard-coded
    inside this integration.
    """

    secret_service = get_secret_service()

    credentials_file = (
        secret_service.get_google_credentials_file()
    )

    token_file = (
        secret_service.get_google_token_file()
    )

    creds = None

    if token_file.exists():
        creds = (
            Credentials.from_authorized_user_file(
                token_file,
                SCOPES,
            )
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
            flow = (
                InstalledAppFlow
                .from_client_secrets_file(
                    credentials_file,
                    SCOPES,
                )
            )

            creds = flow.run_local_server(
                port=0
            )

        token_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        token_file.write_text(
            creds.to_json(),
            encoding="utf-8",
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