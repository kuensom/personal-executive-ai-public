from typing import Optional

from pydantic import BaseModel


class RunStatus(BaseModel):
    status: str
    timestamp: str
    execution_seconds: Optional[float] = None
    analysis_file: Optional[str] = None
    briefing_file: Optional[str] = None
    error: Optional[str] = None


class HistoryItem(BaseModel):
    timestamp: str
    analysis_file: Optional[str] = None
    briefing_file: Optional[str] = None


class UsageInfo(BaseModel):
    model: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class SystemOverview(BaseModel):
    status: str
    last_run: Optional[RunStatus] = None
    latest_usage: Optional[UsageInfo] = None
    history_count: int = 0