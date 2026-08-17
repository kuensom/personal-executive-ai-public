from unittest.mock import MagicMock

import pytest

from app.services.storage_service import (
    GoogleCloudStorageService,
)


def configure_cloud_storage(
    monkeypatch,
):
    monkeypatch.setattr(
        "app.services.storage_service."
        "settings.gcp_project_id",
        "test-project",
    )

    monkeypatch.setattr(
        "app.services.storage_service."
        "settings.gcs_bucket_name",
        "test-bucket",
    )


def test_write_text(
    monkeypatch,
):
    configure_cloud_storage(
        monkeypatch
    )

    client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()

    client.bucket.return_value = bucket
    bucket.blob.return_value = blob

    storage = GoogleCloudStorageService(
        client=client
    )

    result = storage.write_text(
        "test.txt",
        "hello",
    )

    assert result == "test.txt"

    blob.upload_from_string.assert_called_once_with(
        "hello",
        content_type=(
            "text/plain; charset=utf-8"
        ),
    )


def test_read_text(
    monkeypatch,
):
    configure_cloud_storage(
        monkeypatch
    )

    client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()

    client.bucket.return_value = bucket
    bucket.blob.return_value = blob

    blob.exists.return_value = True
    blob.download_as_text.return_value = (
        "hello"
    )

    storage = GoogleCloudStorageService(
        client=client
    )

    assert (
        storage.read_text("test.txt")
        == "hello"
    )


def test_read_missing_returns_none(
    monkeypatch,
):
    configure_cloud_storage(
        monkeypatch
    )

    client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()

    client.bucket.return_value = bucket
    bucket.blob.return_value = blob

    blob.exists.return_value = False

    storage = GoogleCloudStorageService(
        client=client
    )

    assert (
        storage.read_text(
            "missing.txt"
        )
        is None
    )


def test_exists(
    monkeypatch,
):
    configure_cloud_storage(
        monkeypatch
    )

    client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()

    client.bucket.return_value = bucket
    bucket.blob.return_value = blob

    blob.exists.return_value = True

    storage = GoogleCloudStorageService(
        client=client
    )

    assert (
        storage.exists("test.txt")
        is True
    )


def test_list_names(
    monkeypatch,
):
    configure_cloud_storage(
        monkeypatch
    )

    client = MagicMock()
    bucket = MagicMock()

    client.bucket.return_value = bucket

    blob1 = MagicMock()
    blob1.name = (
        "analysis_2026-08-17_08-00-00.json"
    )

    blob2 = MagicMock()
    blob2.name = (
        "analysis_2026-08-17_09-00-00.json"
    )

    blob3 = MagicMock()
    blob3.name = (
        "briefing_2026-08-17_09-00-00.txt"
    )

    client.list_blobs.return_value = [
        blob1,
        blob2,
        blob3,
    ]

    storage = GoogleCloudStorageService(
        client=client
    )

    result = storage.list_names(
        prefix="analysis_",
        suffix=".json",
    )

    assert result == [
        "analysis_2026-08-17_09-00-00.json",
        "analysis_2026-08-17_08-00-00.json",
    ]


def test_missing_project_id(
    monkeypatch,
):
    monkeypatch.setattr(
        "app.services.storage_service."
        "settings.gcp_project_id",
        "",
    )

    monkeypatch.setattr(
        "app.services.storage_service."
        "settings.gcs_bucket_name",
        "test-bucket",
    )

    with pytest.raises(
        RuntimeError,
        match="GCP_PROJECT_ID",
    ):
        GoogleCloudStorageService(
            client=MagicMock()
        )


def test_missing_bucket_name(
    monkeypatch,
):
    monkeypatch.setattr(
        "app.services.storage_service."
        "settings.gcp_project_id",
        "test-project",
    )

    monkeypatch.setattr(
        "app.services.storage_service."
        "settings.gcs_bucket_name",
        "",
    )

    with pytest.raises(
        RuntimeError,
        match="GCS_BUCKET_NAME",
    ):
        GoogleCloudStorageService(
            client=MagicMock()
        )