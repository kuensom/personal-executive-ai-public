from unittest.mock import patch

from app import scheduled_runner
from app.models import DailyAnalysis


def build_fake_analysis():
    """Return deterministic fake analysis for scheduler tests."""

    return DailyAnalysis(
        immediate_priorities=[],
        emails=[],
        calendar_observations=[],
        suggested_next_actions=[],
    )


@patch("app.scheduled_runner.notify")
@patch("app.scheduled_runner.render_morning_briefing")
@patch("app.scheduled_runner.save_analysis")
@patch("app.scheduled_runner.analyse_daily_context")
def test_scheduled_runner_success(
    mock_analyse,
    mock_save_analysis,
    mock_render,
    mock_notify,
    tmp_path,
    monkeypatch,
):
    fake_analysis = build_fake_analysis()

    mock_analyse.return_value = fake_analysis

    mock_render.return_value = (
        "Test briefing"
    )

    mock_analysis_file = (
        tmp_path
        / "analysis_test.json"
    )

    mock_save_analysis.return_value = (
        mock_analysis_file
    )

    monkeypatch.setattr(
        scheduled_runner,
        "LOG_DIR",
        tmp_path,
    )

    monkeypatch.setattr(
        scheduled_runner,
        "STATUS_FILE",
        tmp_path / "last_run.json",
    )

    scheduled_runner.run()

    # Analysis should run once.
    mock_analyse.assert_called_once()

    # Structured result should be persisted once.
    mock_save_analysis.assert_called_once()

    # Briefing must use the same analysis object.
    mock_render.assert_called_once_with(
        fake_analysis
    )

    # User notification should be issued.
    mock_notify.assert_called_once()

    # Status file should exist.
    status_file = (
        tmp_path
        / "last_run.json"
    )

    assert status_file.exists()

    status_text = (
        status_file.read_text(
            encoding="utf-8"
        )
    )

    assert '"status": "success"' in status_text

    # One briefing should have been created.
    briefing_files = list(
        tmp_path.glob(
            "briefing_*.txt"
        )
    )

    assert len(briefing_files) == 1

    assert (
        briefing_files[0].read_text(
            encoding="utf-8"
        )
        == "Test briefing"
    )


@patch("app.scheduled_runner.notify")
@patch("app.scheduled_runner.analyse_daily_context")
def test_scheduled_runner_failure(
    mock_analyse,
    mock_notify,
    tmp_path,
    monkeypatch,
):
    mock_analyse.side_effect = RuntimeError(
        "Simulated failure"
    )

    monkeypatch.setattr(
        scheduled_runner,
        "LOG_DIR",
        tmp_path,
    )

    monkeypatch.setattr(
        scheduled_runner,
        "STATUS_FILE",
        tmp_path / "last_run.json",
    )

    try:
        scheduled_runner.run()

    except RuntimeError:
        pass

    # Failure notification should occur.
    mock_notify.assert_called_once()

    # Failed run status must still be persisted.
    status_file = (
        tmp_path
        / "last_run.json"
    )

    assert status_file.exists()

    status_text = (
        status_file.read_text(
            encoding="utf-8"
        )
    )

    assert '"status": "failed"' in status_text

    assert (
        "Simulated failure"
        in status_text
    )