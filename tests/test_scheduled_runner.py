from unittest.mock import MagicMock, patch

from app import scheduled_runner
from app.models import DailyAnalysis


def build_fake_analysis():
    return DailyAnalysis(
        immediate_priorities=[],
        emails=[],
        calendar_observations=[],
        suggested_next_actions=[],
    )


@patch(
    "app.scheduled_runner.notify"
)
@patch(
    "app.scheduled_runner.render_morning_briefing"
)
@patch(
    "app.scheduled_runner.save_analysis"
)
@patch(
    "app.scheduled_runner.analyse_daily_context"
)
@patch(
    "app.scheduled_runner.get_storage_service"
)
def test_scheduled_runner_success(
    mock_get_storage_service,
    mock_analyse,
    mock_save_analysis,
    mock_render,
    mock_notify,
):
    fake_analysis = build_fake_analysis()

    mock_analyse.return_value = (
        fake_analysis
    )

    mock_save_analysis.return_value = (
        "analysis_test.json"
    )

    mock_render.return_value = (
        "Test briefing"
    )

    mock_storage = MagicMock()

    mock_get_storage_service.return_value = (
        mock_storage
    )

    scheduled_runner.run()

    mock_analyse.assert_called_once()

    mock_save_analysis.assert_called_once()

    mock_render.assert_called_once_with(
        fake_analysis
    )

    mock_notify.assert_called_once()

    # Storage should contain:
    # - briefing
    # - last_run status
    assert (
        mock_storage.write_text.call_count
        == 2
    )

    first_call = (
        mock_storage
        .write_text
        .call_args_list[0]
    )

    briefing_name = (
        first_call.args[0]
    )

    briefing_content = (
        first_call.args[1]
    )

    assert briefing_name.startswith(
        "briefing_"
    )

    assert briefing_name.endswith(
        ".txt"
    )

    assert (
        briefing_content
        == "Test briefing"
    )

    second_call = (
        mock_storage
        .write_text
        .call_args_list[1]
    )

    assert (
        second_call.args[0]
        == "last_run.json"
    )

    status_content = (
        second_call.args[1]
    )

    assert '"status": "success"' in (
        status_content
    )

    assert (
        "analysis_test.json"
        in status_content
    )

    assert (
        briefing_name
        in status_content
    )


@patch(
    "app.scheduled_runner.notify"
)
@patch(
    "app.scheduled_runner.analyse_daily_context"
)
@patch(
    "app.scheduled_runner.get_storage_service"
)
def test_scheduled_runner_failure(
    mock_get_storage_service,
    mock_analyse,
    mock_notify,
):
    mock_analyse.side_effect = (
        RuntimeError(
            "Simulated failure"
        )
    )

    mock_storage = MagicMock()

    mock_get_storage_service.return_value = (
        mock_storage
    )

    try:
        scheduled_runner.run()

    except RuntimeError:
        pass

    mock_notify.assert_called_once()

    mock_storage.write_text\
        .assert_called_once()

    call = (
        mock_storage
        .write_text
        .call_args
    )

    assert (
        call.args[0]
        == "last_run.json"
    )

    status_content = (
        call.args[1]
    )

    assert (
        '"status": "failed"'
        in status_content
    )

    assert (
        "Simulated failure"
        in status_content
    )