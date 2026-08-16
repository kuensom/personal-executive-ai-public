from pydantic import BaseModel

from app.models.domain import DailyAnalysis


class HistoryDetailViewModel(BaseModel):
    run_id: str

    analysis: DailyAnalysis | None = None

    briefing: str | None = None