from pathlib import Path

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


def test_google_token_file_returns_path():
    service = LocalSecretService()

    token_file = (
        service.get_google_token_file()
    )

    assert isinstance(
        token_file,
        Path,
    )


def test_google_credentials_file_missing(
    monkeypatch,
    tmp_path,
):
    service = LocalSecretService()

    missing_file = (
        tmp_path / "credentials.json"
    )

    monkeypatch.setattr(
        "app.services.secret_service."
        "settings.google_credentials_file",
        missing_file,
    )

    with pytest.raises(
        FileNotFoundError,
        match="Google OAuth credentials",
    ):
        service.get_google_credentials_file()