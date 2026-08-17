import platform
import subprocess

from app.config import settings
from app.logger import get_logger


logger = get_logger("notification")


def notify(
    title: str,
    message: str,
) -> None:
    """
    Send a local desktop notification when supported.

    Cloud environments do not attempt desktop
    notifications. The event is written to logs
    instead.
    """

    if settings.is_cloud:
        logger.info(
            "Notification: %s - %s",
            title,
            message,
        )
        return

    if platform.system() != "Darwin":
        logger.info(
            "Notification skipped on unsupported "
            "platform: %s - %s",
            title,
            message,
        )
        return

    script = (
        f'display notification '
        f'{message!r} '
        f'with title {title!r}'
    )

    try:
        subprocess.run(
            [
                "osascript",
                "-e",
                script,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

    except Exception as exc:
        logger.warning(
            "Desktop notification failed: %s",
            exc,
        )