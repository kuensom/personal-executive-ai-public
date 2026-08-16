from unittest.mock import patch

from app import scheduled_runner


@patch("app.scheduled_runner.notify")
@patch("app.scheduled_runner.render_morning_briefing")
def test_scheduled_runner_success(
    mock_render,
    mock_notify,
    tmp_path,
    monkeypatch,
):
    mock_render.return_value = "Test briefing"

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

    status_file = tmp_path / "last_run.json"

    assert status_file.exists()

    status_text = status_file.read_text()

    assert '"status": "success"' in status_text

    briefing_files = list(
        tmp_path.glob("briefing_*.txt")
    )

    assert len(briefing_files) == 1

    assert (
        briefing_files[0].read_text()
        == "Test briefing"
    )

    mock_render.assert_called_once()

    mock_notify.assert_called_once_with(
        "Personal Executive AI",
        "Your morning briefing is ready.",
    )

@patch("app.scheduled_runner.notify")
@patch("app.scheduled_runner.render_morning_briefing")
def test_scheduled_runner_failure(
    mock_render,
    mock_notify,
    tmp_path,
    monkeypatch,
):
    mock_render.side_effect = RuntimeError(
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

    status_file = tmp_path / "last_run.json"

    assert status_file.exists()

    status_text = status_file.read_text()

    assert '"status": "failed"' in status_text
    assert "Simulated failure" in status_text

    mock_notify.assert_called_once_with(
        "Personal Executive AI",
        "Morning briefing failed. Check agent.log.",
    )