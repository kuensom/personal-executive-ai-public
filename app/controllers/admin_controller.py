from pathlib import Path

from fastapi import (
    APIRouter,
    Request,
)
from fastapi.templating import (
    Jinja2Templates,
)

from app.services.admin_service import (
    get_admin_overview,
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

    admin = (
        get_admin_overview()
    )

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "admin": admin,
        },
    )