from unittest.mock import (
    MagicMock,
    patch,
)

from app.services.admin_service import (
    get_admin_overview,
)


@patch(
    "app.services.admin_service."
    "get_connected_google_account"
)
@patch(
    "app.services.admin_service."
    "get_storage_service"
)
@patch(
    "app.services.admin_service."
    "get_secret_service"
)
def test_admin_overview(
    mock_get_secret_service,
    mock_get_storage_service,
    mock_google_account,
):
    secret_service = MagicMock()

    secret_service.get_openai_api_key.return_value = (
        "fake-key"
    )

    mock_get_secret_service.return_value = (
        secret_service
    )

    storage_service = MagicMock()

    mock_get_storage_service.return_value = (
        storage_service
    )

    mock_google_account.return_value = {
        "email": "test@example.com",
        "messages_total": 100,
        "threads_total": 50,
    }

    result = get_admin_overview()

    assert (
        result["google"]["email"]
        == "test@example.com"
    )

    assert (
        result["google"]["status"]
        == "connected"
    )

    assert (
        result["openai"]["status"]
        == "configured"
    )