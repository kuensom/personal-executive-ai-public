from unittest.mock import MagicMock, patch

from app.integrations.google_auth import (
    get_google_credentials,
)


@patch(
    "app.integrations.google_auth."
    "get_secret_service"
)
def test_existing_valid_google_credentials(
    mock_get_secret_service,
):
    secret_service = MagicMock()

    mock_get_secret_service.return_value = (
        secret_service
    )

    secret_service.get_google_token_data.return_value = {
        "token": "fake-token",
        "refresh_token": "fake-refresh-token",
        "token_uri": (
            "https://oauth2.googleapis.com/token"
        ),
        "client_id": "fake-client-id",
        "client_secret": "fake-client-secret",
        "scopes": [
            "https://www.googleapis.com/"
            "auth/gmail.readonly",
            "https://www.googleapis.com/"
            "auth/calendar.readonly",
        ],
    }

    with patch(
        "app.integrations.google_auth."
        "Credentials.from_authorized_user_info"
    ) as mock_from_info:

        fake_credentials = MagicMock()
        fake_credentials.valid = True

        mock_from_info.return_value = (
            fake_credentials
        )

        result = (
            get_google_credentials()
        )

    assert result is fake_credentials

    secret_service.get_google_token_data\
        .assert_called_once()

    secret_service.save_google_token_data\
        .assert_not_called()