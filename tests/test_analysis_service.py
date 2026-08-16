from unittest.mock import MagicMock, patch

from app.services.analysis_service import analyse_daily_context
from app.models import (
    CalendarEvent,
    DailyAnalysis,
    EmailAnalysis,
    EmailMessage,
)


def build_fake_context():
    return {
        "emails": [
            EmailMessage(
                id="msg-1",
                sender="Alice <alice@example.com>",
                subject="Project review",
                received_at="Mon, 10 Aug 2026 09:00:00 +0800",
                snippet="Please review before tomorrow's meeting.",
                is_unread=True,
                labels=["INBOX", "UNREAD"],
            )
        ],
        "calendar": [
            CalendarEvent(
                id="event-1",
                title="Project Meeting",
                start="2026-08-11T10:00:00+08:00",
                end="2026-08-11T11:00:00+08:00",
                location="Teams",
                description="Project review meeting",
                attendees=["alice@example.com"],
                all_day=False,
            )
        ],
    }


def build_fake_analysis():
    return DailyAnalysis(
        immediate_priorities=[
            "Review the project material before the meeting."
        ],
        emails=[
            EmailAnalysis(
                email_id="msg-1",
                category="action_required",
                priority="high",
                action_required=True,
                summary="Project material requires review.",
                suggested_action="Review before the scheduled meeting.",
                deadline="2026-08-11",
                confidence=0.95,
            )
        ],
        calendar_observations=[],
        suggested_next_actions=[
            "Prepare for the project meeting."
        ],
    )


@patch("app.services.analysis_service.collect_daily_context")
@patch("app.services.analysis_service.client")
def test_analyse_daily_context(
    mock_client,
    mock_collect_context,
):
    mock_collect_context.return_value = build_fake_context()

    fake_response = MagicMock()
    fake_response.output_parsed = build_fake_analysis()
    fake_response.usage = None

    mock_client.responses.parse.return_value = fake_response

    result = analyse_daily_context()

    assert isinstance(result, DailyAnalysis)

    assert result.immediate_priorities == [
        "Review the project material before the meeting."
    ]

    assert len(result.emails) == 1
    assert result.emails[0].priority == "high"
    assert result.emails[0].action_required is True

    mock_collect_context.assert_called_once()
    mock_client.responses.parse.assert_called_once()