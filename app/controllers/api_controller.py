from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from app.models import (
    DailyAnalysis,
    HistoryItem,
    RunStatus,
    SystemOverview,
    UsageInfo,
)

from app.services.dashboard_service import (
    get_history,
    get_latest_analysis,
    get_latest_briefing,
    get_latest_usage,
    get_run_status,
    get_system_overview,
)


router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "personal-executive-ai",
    }


@router.get(
    "/api/status",
    response_model=RunStatus,
)
def api_status():
    try:
        return get_run_status()
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.get(
    "/api/latest-analysis",
    response_model=DailyAnalysis,
)
def api_latest_analysis():
    try:
        return get_latest_analysis()
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.get(
    "/api/latest-briefing",
    response_class=PlainTextResponse,
)
def api_latest_briefing():
    try:
        return get_latest_briefing()
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.get(
    "/api/history",
    response_model=list[HistoryItem],
)
def api_history():
    return get_history()


@router.get(
    "/api/usage",
    response_model=UsageInfo,
)
def api_usage():
    try:
        return get_latest_usage()
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.get(
    "/api/overview",
    response_model=SystemOverview,
)
def api_overview():
    return get_system_overview()