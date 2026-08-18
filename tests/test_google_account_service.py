from unittest.mock import (
    MagicMock,
    patch,
)

from app.services.google_account_service import (
    get_connected_google_account,
)


@patch(
    "app.services.google_account_service.build"
)
@patch(
    "app.services.google_account_service."
    "get_google_credentials"
)
def test_get_connected_google_account(
    mock_get_credentials,
    mock_build,
):
    credentials = MagicMock()

    mock_get_credentials.return_value = (
        credentials
    )

    service = MagicMock()

    mock_build.return_value = service

    (
        service.users.return_value
        .getProfile.return_value
        .execute.return_value
    ) = {
        "emailAddress": (
            "test@example.com"
        ),
        "messagesTotal": 100,
        "threadsTotal": 50,
    }

    result = (
        get_connected_google_account()
    )

    assert (
        result["email"]
        == "test@example.com"
    )

    assert (
        result["messages_total"]
        == 100
    )