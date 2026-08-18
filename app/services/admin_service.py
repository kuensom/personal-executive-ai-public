from app.config import settings

from app.services.google_account_service import (
    get_connected_google_account,
)
from app.services.secret_service import (
    get_secret_service,
)
from app.services.storage_service import (
    get_storage_service,
)


def get_admin_overview() -> dict:
    """
    Build non-sensitive administration information.

    Secret values are never returned.
    """

    secret_service = (
        get_secret_service()
    )

    storage_service = (
        get_storage_service()
    )

    google_account = None
    google_status = "disconnected"

    try:
        google_account = (
            get_connected_google_account()
        )

        if google_account.get(
            "email"
        ):
            google_status = "connected"

    except Exception:
        google_status = "error"

    openai_status = "not_configured"

    try:
        api_key = (
            secret_service
            .get_openai_api_key()
        )

        if api_key:
            openai_status = "configured"

    except Exception:
        openai_status = "not_configured"

    return {
        "environment": (
            settings.environment
        ),

        "google": {
            "status": google_status,
            "email": (
                google_account.get(
                    "email"
                )
                if google_account
                else None
            ),
            "messages_total": (
                google_account.get(
                    "messages_total"
                )
                if google_account
                else None
            ),
            "threads_total": (
                google_account.get(
                    "threads_total"
                )
                if google_account
                else None
            ),
        },

        "openai": {
            "status": openai_status,
            "model": (
                settings.openai_model
            ),
        },

        "secrets": {
            "backend": (
                type(
                    secret_service
                ).__name__
            ),
        },

        "storage": {
            "backend": (
                type(
                    storage_service
                ).__name__
            ),
            "bucket": (
                settings.gcs_bucket_name
                if settings.is_cloud
                else None
            ),
        },

        "scheduler": {
            "status": (
                "not_configured"
            ),
        },
    }