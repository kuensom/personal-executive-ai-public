from pydantic import BaseModel, Field

from app.models.api import (
    HistoryItem,
    RunStatus,
    UsageInfo,
)
from app.models.domain import DailyAnalysis


class DashboardViewModel(BaseModel):
    """Presentation-ready data for the main dashboard."""

    system_status: str = "ok"

    last_run: RunStatus | None = None

    analysis: DailyAnalysis | None = None

    usage: UsageInfo | None = None

    recent_history: list[HistoryItem] = Field(
        default_factory=list
    )