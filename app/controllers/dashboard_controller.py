from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates

from app.services.dashboard_service import (
    get_dashboard_view,
    get_history,
    get_history_detail,
    get_latest_briefing,
    get_latest_usage,
    get_system_overview,
)


BASE_DIR = Path(__file__).resolve().parent.parent.parent

TEMPLATE_DIR = (
    BASE_DIR
    / "app"
    / "templates"
)

templates = Jinja2Templates(
    directory=str(TEMPLATE_DIR)
)

router = APIRouter()


@router.get(
    "/",
    include_in_schema=False,
)
def dashboard(
    request: Request,
):
    dashboard_view = get_dashboard_view()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "dashboard": dashboard_view,
        },
    )
@router.get(
    "/history",
    include_in_schema=False,
)
def history_page(
    request: Request,
):
    history = get_history()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "history": history,
        },
    )
@router.get(
    "/usage",
    include_in_schema=False,
)
def usage_page(
    request: Request,
):
    usage = None

    try:
        usage = get_latest_usage()
    except FileNotFoundError:
        pass

    return templates.TemplateResponse(
        request=request,
        name="usage.html",
        context={
            "usage": usage,
        },
    )

@router.get(
    "/system",
    include_in_schema=False,
)
def system_page(
    request: Request,
):
    overview = get_system_overview()

    return templates.TemplateResponse(
        request=request,
        name="system.html",
        context={
            "overview": overview,
        },
    )

@router.get(
    "/briefing",
    include_in_schema=False,
)
def briefing_page(
    request: Request,
):
    briefing = None

    try:
        briefing = get_latest_briefing()

    except FileNotFoundError:
        pass

    return templates.TemplateResponse(
        request=request,
        name="briefing.html",
        context={
            "briefing": briefing,
        },
    )

@router.get(
    "/history/{run_id}",
    include_in_schema=False,
)
def history_detail_page(
    request: Request,
    run_id: str,
):
    try:
        history = get_history_detail(
            run_id
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return templates.TemplateResponse(
        request=request,
        name="history_detail.html",
        context={
            "history": history,
        },
    )