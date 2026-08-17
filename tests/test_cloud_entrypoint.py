from unittest.mock import patch

from app.cloud_entrypoint import main


@patch(
    "app.cloud_entrypoint.uvicorn.run"
)
def test_cloud_entrypoint(
    mock_run,
    monkeypatch,
):
    monkeypatch.setenv(
        "PORT",
        "9090",
    )

    main()

    mock_run.assert_called_once_with(
        "app.api:app",
        host="0.0.0.0",
        port=9090,
    )