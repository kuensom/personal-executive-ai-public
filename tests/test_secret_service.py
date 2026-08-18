import json

import pytest

from app.services.secret_service import (
    LocalSecretService,
    SecretService,
)


def test_local_secret_service_is_secret_service():
    service = LocalSecretService()

    assert isinstance(
        service,
        SecretService,
    )


def test_get_openai_api_key(
    monkeypatch,
):
    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "test-api-key",
    )

    service = LocalSecretService()

    assert (
        service.get_openai_api_key()
        == "test-api-key"
    )


def test_missing_openai_api_key(
    monkeypatch,
):
    monkeypatch.delenv(
        "OPENAI_API_KEY",
        raising=False,
    )

    service = LocalSecretService()

    with pytest.raises(
        RuntimeError,
        match="OPENAI_API_KEY",
    ):
        service.get_openai_api_key()


def test_get_google_client_config(
    monkeypatch,
    tmp_path,
):
    credentials_file = (
        tmp_path / "credentials.json"
    )

    expected = {
        "installed": {
            "client_id": "test-client-id",
            "client_secret": "test-client-secret",
        }
    }

    credentials_file.write_text(
        json.dumps(expected),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.google_credentials_file",
        credentials_file,
    )

    service = LocalSecretService()

    result = (
        service.get_google_client_config()
    )

    assert result == expected


def test_missing_google_client_config(
    monkeypatch,
    tmp_path,
):
    missing_file = (
        tmp_path / "credentials.json"
    )

    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.google_credentials_file",
        missing_file,
    )

    service = LocalSecretService()

    with pytest.raises(
        FileNotFoundError,
        match="Google OAuth credentials",
    ):
        service.get_google_client_config()


def test_get_google_token_data_missing(
    monkeypatch,
    tmp_path,
):
    token_file = (
        tmp_path / "token.json"
    )

    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.google_token_file",
        token_file,
    )

    service = LocalSecretService()

    assert (
        service.get_google_token_data()
        is None
    )


def test_save_and_get_google_token_data(
    monkeypatch,
    tmp_path,
):
    token_file = (
        tmp_path / "secrets" / "token.json"
    )

    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.google_token_file",
        token_file,
    )

    expected = {
        "token": "fake-access-token",
        "refresh_token": "fake-refresh-token",
        "client_id": "test-client-id",
        "client_secret": "test-client-secret",
    }

    service = LocalSecretService()

    service.save_google_token_data(
        expected
    )

    assert token_file.exists()

    result = (
        service.get_google_token_data()
    )

    assert result == expected

def test_get_google_web_client_config(
    monkeypatch,
    tmp_path,
):
    web_client_file = (
        tmp_path
        / "google-web-client.json"
    )

    expected = {
        "web": {
            "client_id": "test-client-id",
            "client_secret": (
                "test-client-secret"
            ),
            "redirect_uris": [
                (
                    "http://127.0.0.1:8080/"
                    "admin/google/callback"
                )
            ],
        }
    }

    web_client_file.write_text(
        json.dumps(
            expected
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.google_web_client_file",
        web_client_file,
    )

    service = LocalSecretService()

    result = (
        service
        .get_google_web_client_config()
    )

    assert result == expected

def test_missing_google_web_client_config(
    monkeypatch,
    tmp_path,
):
    missing_file = (
        tmp_path
        / "google-web-client.json"
    )

    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.google_web_client_file",
        missing_file,
    )

    service = LocalSecretService()

    with pytest.raises(
        FileNotFoundError,
        match="Google Web OAuth",
    ):
        service.get_google_web_client_config()

