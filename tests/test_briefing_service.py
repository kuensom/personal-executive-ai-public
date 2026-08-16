from app.services.briefing_service import render_morning_briefing
from app.models import (
    CalendarObservation,
    DailyAnalysis,
    EmailAnalysis,
)


def build_fake_analysis():
    return DailyAnalysis(
        immediate_priorities=[
            "Prepare for the project meeting.",
        ],
        emails=[
            EmailAnalysis(
                email_id="msg-1",
                category="action_required",
                priority="high",
                action_required=True,
                summary="Review project document.",
                suggested_action="Read and respond before the meeting.",
                deadline="2026-08-11",
                confidence=0.95,
            ),
            EmailAnalysis(
                email_id="msg-2",
                category="informational",
                priority="low",
                action_required=False,
                summary="General newsletter.",
                suggested_action="",
                deadline=None,
                confidence=0.99,
            ),
        ],
        calendar_observations=[
            CalendarObservation(
                event_id="event-1",
                observation_type="preparation",
                message="Review project material before the meeting.",
                confidence=0.90,
            ),
        ],
        suggested_next_actions=[
            "Review the project document.",
            "Prepare notes for the meeting.",
        ],
    )


def test_render_morning_briefing():
    analysis = build_fake_analysis()

    briefing = render_morning_briefing(analysis)

    assert "MORNING BRIEFING" in briefing
    assert "Prepare for the project meeting." in briefing
    assert "Review project document." in briefing
    assert "Read and respond before the meeting." in briefing
    assert "Review project material before the meeting." in briefing

    # Low-priority informational email should not appear
    # in the attention section.
    assert "General newsletter." not in briefing