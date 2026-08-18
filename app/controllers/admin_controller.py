from pathlib import Path

import json
import os
import secrets

from fastapi import (
    APIRouter,
    Query,
    Request,
)
from fastapi.responses import (
    RedirectResponse,
)
from fastapi.templating import (
    Jinja2Templates,
)
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from app.config import settings
from app.integrations.google_auth import (
    SCOPES,
)
from app.services.admin_service import (
    get_admin_overview,
)
from app.services.secret_service import (
    get_secret_service,
)


router = APIRouter()


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)

TEMPLATES_DIR = (
    BASE_DIR
    / "app"
    / "templates"
)

templates = Jinja2Templates(
    directory=str(
        TEMPLATES_DIR
    )
)


# ============================================================
# HELPERS
# ============================================================

def _delete_oauth_cookies(
    response: RedirectResponse,
) -> None:
    """
    Remove temporary OAuth cookies.
    """

    response.delete_cookie(
        "google_oauth_state"
    )

    response.delete_cookie(
        "google_oauth_code_verifier"
    )

    response.delete_cookie(
        "google_oauth_expected_email"
    )


def _normalise_email(
    value: str | None,
) -> str | None:
    """
    Normalise an optional email address.
    """

    if value is None:
        return None

    value = value.strip().lower()

    if not value:
        return None

    if "@" not in value:
        return None

    return value


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@router.get(
    "/admin",
    include_in_schema=False,
)
def admin_dashboard(
    request: Request,
):
    """
    Display non-sensitive administration status.
    """

    admin = get_admin_overview()

    google_status = (
        request.query_params.get(
            "google_status"
        )
    )

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "admin": admin,
            "google_status": google_status,
        },
    )


# ============================================================
# GOOGLE OAUTH - CONNECT / SWITCH ACCOUNT
# ============================================================

@router.get(
    "/admin/google/connect",
    include_in_schema=False,
)
def connect_google_account(
    email: str | None = Query(
        default=None
    ),
):
    """
    Start Google Web OAuth.

    If an email address is supplied it is used as
    a login hint and later verified against the
    account Google actually authorized.

    If no email is supplied, Google account
    selection is still requested.
    """

    expected_email = _normalise_email(
        email
    )

    if (
        email is not None
        and email.strip()
        and expected_email is None
    ):
        return RedirectResponse(
            "/admin?google_status=invalid_email",
            status_code=303,
        )

    secret_service = (
        get_secret_service()
    )

    client_config = (
        secret_service
        .get_google_web_client_config()
    )

    state = secrets.token_urlsafe(32)

    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=(
            settings.google_oauth_redirect_uri
        ),
        autogenerate_code_verifier=True,
    )

    oauth_arguments = {
        "access_type": "offline",
        "include_granted_scopes": "true",
        "prompt": "select_account consent",
        "state": state,
    }

    if expected_email:
        oauth_arguments[
            "login_hint"
        ] = expected_email

    authorization_url, _ = (
        flow.authorization_url(
            **oauth_arguments
        )
    )

    response = RedirectResponse(
        authorization_url,
        status_code=302,
    )

    # CSRF state.
    response.set_cookie(
        key="google_oauth_state",
        value=state,
        httponly=True,
        secure=settings.is_cloud,
        samesite="lax",
        max_age=600,
    )

    # PKCE verifier.
    response.set_cookie(
        key="google_oauth_code_verifier",
        value=flow.code_verifier,
        httponly=True,
        secure=settings.is_cloud,
        samesite="lax",
        max_age=600,
    )

    # Optional intended account.
    if expected_email:
        response.set_cookie(
            key="google_oauth_expected_email",
            value=expected_email,
            httponly=True,
            secure=settings.is_cloud,
            samesite="lax",
            max_age=600,
        )

    return response


# ============================================================
# GOOGLE OAUTH - CALLBACK
# ============================================================

@router.get(
    "/admin/google/callback",
    include_in_schema=False,
)
def google_oauth_callback(
    request: Request,
):
    """
    Complete the Google OAuth flow.

    The newly issued credentials are verified
    against Gmail before they replace the current
    stored Google token.
    """

    query_state = (
        request.query_params.get(
            "state"
        )
    )

    cookie_state = (
        request.cookies.get(
            "google_oauth_state"
        )
    )

    code_verifier = (
        request.cookies.get(
            "google_oauth_code_verifier"
        )
    )

    expected_email = (
        request.cookies.get(
            "google_oauth_expected_email"
        )
    )

    # --------------------------------------------------------
    # Validate OAuth state / PKCE context
    # --------------------------------------------------------

    if (
        not query_state
        or not cookie_state
        or not code_verifier
        or not secrets.compare_digest(
            query_state,
            cookie_state,
        )
    ):
        response = RedirectResponse(
            "/admin?google_status=invalid_state",
            status_code=303,
        )

        _delete_oauth_cookies(
            response
        )

        return response

    # --------------------------------------------------------
    # Rebuild Web OAuth flow
    # --------------------------------------------------------

    secret_service = (
        get_secret_service()
    )

    client_config = (
        secret_service
        .get_google_web_client_config()
    )

    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        state=query_state,
        redirect_uri=(
            settings.google_oauth_redirect_uri
        ),
        code_verifier=code_verifier,
    )

    # OAuthlib requires HTTPS in production.
    # HTTP is allowed only for local development.
    if not settings.is_cloud:
        os.environ[
            "OAUTHLIB_INSECURE_TRANSPORT"
        ] = "1"

    # --------------------------------------------------------
    # Exchange authorization code
    # --------------------------------------------------------

    flow.fetch_token(
        authorization_response=str(
            request.url
        )
    )

    credentials = flow.credentials

    # --------------------------------------------------------
    # Determine the ACTUAL Google account authorized
    # --------------------------------------------------------

    gmail = build(
        "gmail",
        "v1",
        credentials=credentials,
        cache_discovery=False,
    )

    profile = (
        gmail.users()
        .getProfile(
            userId="me"
        )
        .execute()
    )

    actual_email = (
        profile.get(
            "emailAddress",
            ""
        )
        .strip()
        .lower()
    )

    if not actual_email:
        response = RedirectResponse(
            "/admin?google_status=profile_error",
            status_code=303,
        )

        _delete_oauth_cookies(
            response
        )

        return response

    # --------------------------------------------------------
    # If Admin specified an account, require an exact match.
    #
    # IMPORTANT:
    # Do not overwrite the existing token when Google
    # authorized a different account.
    # --------------------------------------------------------

    if (
        expected_email
        and actual_email
        != expected_email.strip().lower()
    ):
        response = RedirectResponse(
            "/admin?google_status=account_mismatch",
            status_code=303,
        )

        _delete_oauth_cookies(
            response
        )

        return response

    # --------------------------------------------------------
    # Persist only the verified credentials
    # --------------------------------------------------------

    token_data = json.loads(
        credentials.to_json()
    )

    secret_service.save_google_token_data(
        token_data
    )

    # --------------------------------------------------------
    # Successful account switch
    # --------------------------------------------------------

    response = RedirectResponse(
        "/admin?google_status=connected",
        status_code=303,
    )

    _delete_oauth_cookies(
        response
    )

    return response