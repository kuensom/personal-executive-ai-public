from unittest.mock import patch

from app.notification_service import notify


@patch(
    "app.notification_service.logger"
)
def test_cloud_notification_uses_logging(
    mock_logger,
    monkeypatch,
):
    monkeypatch.setattr(
        "app.notification_service."
        "settings.environment",
        "cloud",
    )

    notify(
        "Test",
        "Message",
    )

    mock_logger.info.assert_called_once()