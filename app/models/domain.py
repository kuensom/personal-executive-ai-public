from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from typing import Literal, Optional


class EmailMessage(BaseModel):
    """Normalised representation of an email."""

    id: str

    sender: str = ""
    subject: str = ""
    received_at: Optional[str] = None

    snippet: str = ""

    is_unread: bool = False

    labels: list[str] = Field(default_factory=list)


class CalendarEvent(BaseModel):
    """Normalised representation of a calendar event."""

    id: str

    title: str = ""

    start: Optional[str] = None
    end: Optional[str] = None

    location: str = ""

    description: str = ""

    attendees: list[str] = Field(default_factory=list)

    all_day: bool = False

class EmailAnalysis(BaseModel):
    email_id: str

    category: Literal[
        "urgent",
        "action_required",
        "awaiting_response",
        "informational",
        "low_priority",
    ]

    priority: Literal[
        "high",
        "medium",
        "low",
    ]

    action_required: bool = False

    summary: str

    suggested_action: str = ""

    deadline: Optional[str] = None

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        default=0.5,
    )


class CalendarObservation(BaseModel):
    event_id: str

    observation_type: Literal[
        "conflict",
        "preparation",
        "tight_transition",
        "general",
    ]

    message: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        default=0.5,
    )


class DailyAnalysis(BaseModel):
    immediate_priorities: list[str] = Field(
        default_factory=list
    )

    emails: list[EmailAnalysis] = Field(
        default_factory=list
    )

    calendar_observations: list[
        CalendarObservation
    ] = Field(
        default_factory=list
    )

    suggested_next_actions: list[str] = Field(
        default_factory=list
    )

