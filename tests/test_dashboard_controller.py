from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api import app

from app.models import (
    DashboardViewModel,
    DailyAnalysis,
    HistoryDetailViewModel,
    HistoryItem,
    RunStatus,
    SystemOverview,
    UsageInfo,
)


client = TestClient(app)


def build_dashboard_view():
    """Create predictable dashboard data for tests."""

    return DashboardViewModel(
        system_status="ok",

        last_run=RunStatus(
            status="success",
            timestamp="2026-08-15T07:30:00",
            execution_seconds=5.2,
            analysis_file="analysis_test.json",
            briefing_file="briefing_test.txt",
        ),

        analysis=DailyAnalysis(
            immediate_priorities=[
                "Prepare for the project meeting.",
            ],
            emails=[],
            calendar_observations=[],
            suggested_next_actions=[
                "Review project notes.",
            ],
        ),

        usage=UsageInfo(
            model="gpt-5.6-luna",
            input_tokens=1000,
            output_tokens=200,
            total_tokens=1200,
        ),

        recent_history=[
            HistoryItem(
                timestamp="2026-08-15_07-30-00",
                analysis_file="analysis_test.json",
                briefing_file="briefing_test.txt",
            )
        ],
    )


@patch(
    "app.controllers.dashboard_controller.get_dashboard_view"
)
def test_dashboard_page(
    mock_get_dashboard_view,
):
    mock_get_dashboard_view.return_value = (
        build_dashboard_view()
    )

    response = client.get("/")

    assert response.status_code == 200

    assert "Executive Dashboard" in response.text
    assert "Personal Executive AI" in response.text

    assert (
        "Prepare for the project meeting."
        in response.text
    )

    assert "gpt-5.6-luna" in response.text

    mock_get_dashboard_view.assert_called_once()


@patch(
    "app.controllers.dashboard_controller.get_history"
)
def test_history_page(
    mock_get_history,
):
    mock_get_history.return_value = [
        HistoryItem(
            timestamp="2026-08-15_07-30-00",
            analysis_file="analysis_test.json",
            briefing_file="briefing_test.txt",
        )
    ]

    response = client.get(
        "/history"
    )

    assert response.status_code == 200

    assert "Execution History" in response.text
    assert "2026-08-15_07-30-00" in response.text

    mock_get_history.assert_called_once()


@patch(
    "app.controllers.dashboard_controller.get_latest_usage"
)
def test_usage_page(
    mock_get_latest_usage,
):
    mock_get_latest_usage.return_value = (
        UsageInfo(
            model="gpt-5.6-luna",
            input_tokens=1000,
            output_tokens=200,
            total_tokens=1200,
        )
    )

    response = client.get(
        "/usage"
    )

    assert response.status_code == 200

    assert "AI Usage" in response.text
    assert "gpt-5.6-luna" in response.text
    assert "1200" in response.text

    mock_get_latest_usage.assert_called_once()


@patch(
    "app.controllers.dashboard_controller.get_system_overview"
)
def test_system_page(
    mock_get_system_overview,
):
    mock_get_system_overview.return_value = (
        SystemOverview(
            status="ok",

            last_run=RunStatus(
                status="success",
                timestamp="2026-08-15T07:30:00",
                execution_seconds=5.2,
            ),

            latest_usage=UsageInfo(
                model="gpt-5.6-luna",
                input_tokens=1000,
                output_tokens=200,
                total_tokens=1200,
            ),

            history_count=3,
        )
    )

    response = client.get(
        "/system"
    )

    assert response.status_code == 200

    assert "System Status" in response.text
    assert "SUCCESS" in response.text
    assert "3" in response.text

    mock_get_system_overview.assert_called_once()

@patch(
    "app.controllers.dashboard_controller.get_latest_briefing"
)
def test_briefing_page(
    mock_get_latest_briefing,
):
    mock_get_latest_briefing.return_value = (
        "PERSONAL EXECUTIVE AI ASSISTANT\n\n"
        "MORNING BRIEFING\n\n"
        "Immediate priorities:\n"
        "1. Prepare for the project meeting.\n"
        "2. Review important emails."
    )

    response = client.get(
        "/briefing"
    )

    assert response.status_code == 200

    assert "Executive Briefing" in response.text

    assert (
        "MORNING BRIEFING"
        in response.text
    )

    assert (
        "Prepare for the project meeting."
        in response.text
    )

    mock_get_latest_briefing.assert_called_once()

@patch(
    "app.controllers.dashboard_controller.get_latest_briefing"
)
def test_briefing_page_without_briefing(
    mock_get_latest_briefing,
):
    mock_get_latest_briefing.side_effect = (
        FileNotFoundError(
            "No briefing available"
        )
    )

    response = client.get(
        "/briefing"
    )

    assert response.status_code == 200

    assert (
        "No executive briefing is currently available."
        in response.text
    )

    mock_get_latest_briefing.assert_called_once()

@patch(
    "app.controllers.dashboard_controller.get_history_detail"
)
def test_history_detail_page(
    mock_get_history_detail,
):
    mock_get_history_detail.return_value = (
        HistoryDetailViewModel(
            run_id="2026-08-15_07-30-00",

            analysis=DailyAnalysis(
                immediate_priorities=[
                    "Prepare for meeting."
                ],
                emails=[],
                calendar_observations=[],
                suggested_next_actions=[
                    "Review notes."
                ],
            ),

            briefing=(
                "MORNING BRIEFING\n"
                "Prepare for meeting."
            ),
        )
    )

    response = client.get(
        "/history/2026-08-15_07-30-00"
    )

    assert response.status_code == 200

    assert "Historical Run" in response.text

    assert (
        "Prepare for meeting."
        in response.text
    )

    assert (
        "MORNING BRIEFING"
        in response.text
    )

    mock_get_history_detail.assert_called_once_with(
        "2026-08-15_07-30-00"
    )

@patch(
    "app.controllers.dashboard_controller.get_history_detail"
)
def test_history_detail_not_found(
    mock_get_history_detail,
):
    mock_get_history_detail.side_effect = (
        FileNotFoundError(
            "No history found"
        )
    )

    response = client.get(
        "/history/missing-run"
    )

    assert response.status_code == 404