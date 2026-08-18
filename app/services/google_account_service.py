from googleapiclient.discovery import build

from app.integrations.google_auth import (
    get_google_credentials,
)


def get_connected_google_account() -> dict:
    """
    Return non-sensitive information about the
    Google account currently authorized for Gmail.

    No OAuth tokens or secrets are returned.
    """

    credentials = get_google_credentials()

    service = build(
        "gmail",
        "v1",
        credentials=credentials,
        cache_discovery=False,
    )

    profile = (
        service.users()
        .getProfile(
            userId="me"
        )
        .execute()
    )

    return {
        "email": profile.get(
            "emailAddress"
        ),
        "messages_total": profile.get(
            "messagesTotal"
        ),
        "threads_total": profile.get(
            "threadsTotal"
        ),
    }