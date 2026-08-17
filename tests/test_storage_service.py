from app.services.storage_service import (
    LocalStorageService,
)


def test_write_and_read_text(
    tmp_path,
):
    storage = LocalStorageService(
        base_dir=tmp_path
    )

    storage.write_text(
        "test.txt",
        "Hello storage",
    )

    assert (
        storage.read_text("test.txt")
        == "Hello storage"
    )


def test_exists(
    tmp_path,
):
    storage = LocalStorageService(
        base_dir=tmp_path
    )

    assert (
        storage.exists("missing.txt")
        is False
    )

    storage.write_text(
        "exists.txt",
        "content",
    )

    assert (
        storage.exists("exists.txt")
        is True
    )


def test_missing_file_returns_none(
    tmp_path,
):
    storage = LocalStorageService(
        base_dir=tmp_path
    )

    assert (
        storage.read_text("missing.txt")
        is None
    )

def test_list_names(
    tmp_path,
):
    storage = LocalStorageService(
        base_dir=tmp_path
    )

    storage.write_text(
        "analysis_2026-08-17_08-00-00.json",
        "{}",
    )

    storage.write_text(
        "analysis_2026-08-17_09-00-00.json",
        "{}",
    )

    storage.write_text(
        "briefing_2026-08-17_09-00-00.txt",
        "briefing",
    )

    names = storage.list_names(
        prefix="analysis_",
        suffix=".json",
    )

    assert names == [
        "analysis_2026-08-17_09-00-00.json",
        "analysis_2026-08-17_08-00-00.json",
    ]

import pytest


def test_rejects_directory_traversal(
    tmp_path,
):
    storage = LocalStorageService(
        base_dir=tmp_path
    )

    with pytest.raises(
        ValueError,
    ):
        storage.write_text(
            "../secret.txt",
            "not allowed",
        )