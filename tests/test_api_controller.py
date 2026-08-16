from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api import app
from app.models import (
    DailyAnalysis,
    HistoryItem,
    RunStatus,
    SystemOverview,
    UsageInfo,
)


client = TestClient(app)


def test_health_endpoint():
    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert (
        data["service"]
        == "personal-executive-ai"
    )


@patch(
    "app.controllers.api_controller.get_run_status"
)
def test_status_endpoint(
    mock_get_run_status,
):
    mock_get_run_status.return_value = (
        RunStatus(
            status="success",
            timestamp="2026-08-15T07:30:00",
            execution_seconds=5.2,
            analysis_file="analysis_test.json",
            briefing_file="briefing_test.txt",
        )
    )

    response = client.get(
        "/api/status"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert (
        data["timestamp"]
        == "2026-08-15T07:30:00"
    )

    assert (
        data["execution_seconds"]
        == 5.2
    )

    mock_get_run_status.assert_called_once()


@patch(
    "app.controllers.api_controller.get_latest_analysis"
)
def test_latest_analysis_endpoint(
    mock_get_latest_analysis,
):
    mock_get_latest_analysis.return_value = (
        DailyAnalysis(
            immediate_priorities=[
                "Prepare for the project meeting."
            ],
            emails=[],
            calendar_observations=[],
            suggested_next_actions=[
                "Review project notes."
            ],
        )
    )

    response = client.get(
        "/api/latest-analysis"
    )

    assert response.status_code == 200

    data = response.json()

    assert data[
        "immediate_priorities"
    ] == [
        "Prepare for the project meeting."
    ]

    assert data["emails"] == []

    assert (
        data["calendar_observations"]
        == []
    )

    assert data[
        "suggested_next_actions"
    ] == [
        "Review project notes."
    ]

    mock_get_latest_analysis.assert_called_once()


@patch(
    "app.controllers.api_controller.get_latest_briefing"
)
def test_latest_briefing_endpoint(
    mock_get_latest_briefing,
):
    mock_get_latest_briefing.return_value = (
        "PERSONAL EXECUTIVE AI ASSISTANT\n"
        "MORNING BRIEFING"
    )

    response = client.get(
        "/api/latest-briefing"
    )

    assert response.status_code == 200

    assert (
        "MORNING BRIEFING"
        in response.text
    )

    mock_get_latest_briefing.assert_called_once()


@patch(
    "app.controllers.api_controller.get_history"
)
def test_history_endpoint(
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
        "/api/history"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        list,
    )

    assert len(data) == 1

    assert (
        data[0]["timestamp"]
        == "2026-08-15_07-30-00"
    )

    mock_get_history.assert_called_once()


@patch(
    "app.controllers.api_controller.get_latest_usage"
)
def test_usage_endpoint(
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
        "/api/usage"
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["model"]
        == "gpt-5.6-luna"
    )

    assert (
        data["input_tokens"]
        == 1000
    )

    assert (
        data["output_tokens"]
        == 200
    )

    assert (
        data["total_tokens"]
        == 1200
    )

    mock_get_latest_usage.assert_called_once()


@patch(
    "app.controllers.api_controller.get_system_overview"
)
def test_overview_endpoint(
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
        "/api/overview"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert (
        data["history_count"]
        == 3
    )

    assert (
        data["last_run"]["status"]
        == "success"
    )

    assert (
        data["latest_usage"]["model"]
        == "gpt-5.6-luna"
    )

    mock_get_system_overview.assert_called_once()