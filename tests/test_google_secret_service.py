from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from google.api_core.exceptions import NotFound

from app.services.secret_service import (
    GoogleSecretService,
)


def build_payload(
    value: str,
):
    return SimpleNamespace(
        payload=SimpleNamespace(
            data=value.encode(
                "utf-8"
            )
        )
    )


def configure_project(
    monkeypatch,
):
    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.gcp_project_id",
        "test-project",
    )


def test_get_openai_api_key(
    monkeypatch,
):
    configure_project(
        monkeypatch
    )

    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.openai_secret_id",
        "openai-key",
    )

    client = MagicMock()

    client.access_secret_version.return_value = (
        build_payload(
            "fake-openai-key"
        )
    )

    service = GoogleSecretService(
        client=client
    )

    result = (
        service.get_openai_api_key()
    )

    assert result == "fake-openai-key"

    client.access_secret_version\
        .assert_called_once_with(
            request={
                "name": (
                    "projects/test-project/"
                    "secrets/openai-key/"
                    "versions/latest"
                )
            }
        )


def test_get_google_client_config(
    monkeypatch,
):
    configure_project(
        monkeypatch
    )

    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.google_client_secret_id",
        "google-client",
    )

    client = MagicMock()

    client.access_secret_version.return_value = (
        build_payload(
            '{"installed":{"client_id":"abc"}}'
        )
    )

    service = GoogleSecretService(
        client=client
    )

    result = (
        service.get_google_client_config()
    )

    assert result == {
        "installed": {
            "client_id": "abc"
        }
    }


def test_get_google_token_data(
    monkeypatch,
):
    configure_project(
        monkeypatch
    )

    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.google_token_secret_id",
        "google-token",
    )

    client = MagicMock()

    client.access_secret_version.return_value = (
        build_payload(
            '{"token":"abc"}'
        )
    )

    service = GoogleSecretService(
        client=client
    )

    assert (
        service.get_google_token_data()
        == {
            "token": "abc"
        }
    )


def test_missing_google_token_returns_none(
    monkeypatch,
):
    configure_project(
        monkeypatch
    )

    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.google_token_secret_id",
        "google-token",
    )

    client = MagicMock()

    client.access_secret_version.side_effect = (
        NotFound(
            "Secret not found"
        )
    )

    service = GoogleSecretService(
        client=client
    )

    assert (
        service.get_google_token_data()
        is None
    )


def test_save_google_token_data(
    monkeypatch,
):
    configure_project(
        monkeypatch
    )

    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.google_token_secret_id",
        "google-token",
    )

    client = MagicMock()

    service = GoogleSecretService(
        client=client
    )

    service.save_google_token_data(
        {
            "token": "abc"
        }
    )

    client.add_secret_version\
        .assert_called_once()

    request = (
        client
        .add_secret_version
        .call_args
        .kwargs["request"]
    )

    assert request["parent"] == (
        "projects/test-project/"
        "secrets/google-token"
    )

    assert request[
        "payload"
    ][
        "data"
    ] == b'{"token":"abc"}'


def test_invalid_google_client_json(
    monkeypatch,
):
    configure_project(
        monkeypatch
    )

    client = MagicMock()

    client.access_secret_version.return_value = (
        build_payload(
            "not-json"
        )
    )

    service = GoogleSecretService(
        client=client
    )

    with pytest.raises(
        RuntimeError,
        match="invalid JSON",
    ):
        service.get_google_client_config()


def test_missing_project_id(
    monkeypatch,
):
    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.gcp_project_id",
        "",
    )

    with pytest.raises(
        RuntimeError,
        match="GCP_PROJECT_ID",
    ):
        GoogleSecretService(
            client=MagicMock()
        )

def test_get_google_web_client_config(
    monkeypatch,
):
    configure_project(
        monkeypatch
    )

    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.google_web_client_secret_id",
        "google-web-client",
    )

    client = MagicMock()

    client.access_secret_version.return_value = (
        build_payload(
            (
                '{"web":'
                '{"client_id":"abc",'
                '"client_secret":"xyz"}}'
            )
        )
    )

    service = GoogleSecretService(
        client=client
    )

    result = (
        service
        .get_google_web_client_config()
    )

    assert result == {
        "web": {
            "client_id": "abc",
            "client_secret": "xyz",
        }
    }

def test_invalid_google_web_client_json(
    monkeypatch,
):
    configure_project(
        monkeypatch
    )

    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.google_web_client_secret_id",
        "google-web-client",
    )

    client = MagicMock()

    client.access_secret_version.return_value = (
        build_payload(
            "invalid-json"
        )
    )

    service = GoogleSecretService(
        client=client
    )

    with pytest.raises(
        RuntimeError,
        match="invalid JSON",
    ):
        service.get_google_web_client_config()