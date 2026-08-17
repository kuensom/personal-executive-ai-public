from abc import ABC, abstractmethod
from pathlib import Path

from app.config import settings
from google.cloud import storage

class StorageService(ABC):
    """
    Abstract storage interface for application artifacts.

    Artifact names are storage-neutral strings such as:

        analysis_2026-08-17_08-00-00.json
        briefing_2026-08-17_08-00-00.txt
        last_run.json
        latest_usage.json
    """

    @abstractmethod
    def write_text(
        self,
        name: str,
        content: str,
    ) -> str:
        """Persist text and return its artifact name."""
        raise NotImplementedError

    @abstractmethod
    def read_text(
        self,
        name: str,
    ) -> str | None:
        """Return stored text, or None if missing."""
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        name: str,
    ) -> bool:
        """Return whether an artifact exists."""
        raise NotImplementedError

    @abstractmethod
    def list_names(
        self,
        prefix: str = "",
        suffix: str = "",
    ) -> list[str]:
        """
        Return matching artifact names.

        Newest names are returned first.

        Our run IDs are timestamp-based, so reverse
        lexical ordering also produces newest-first
        ordering.
        """
        raise NotImplementedError


class LocalStorageService(StorageService):
    """Local filesystem implementation."""

    def __init__(
        self,
        base_dir: Path | None = None,
    ):
        self.base_dir = (
            base_dir
            if base_dir is not None
            else settings.log_dir
        )

        self.base_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _path(
        self,
        name: str,
    ) -> Path:
        """
        Resolve an artifact name safely inside
        the configured storage directory.
        """

        clean_name = Path(name).name

        if clean_name != name:
            raise ValueError(
                "Artifact name must not contain directories."
            )

        return self.base_dir / clean_name

    def write_text(
        self,
        name: str,
        content: str,
    ) -> str:
        self._path(name).write_text(
            content,
            encoding="utf-8",
        )

        return name

    def read_text(
        self,
        name: str,
    ) -> str | None:
        path = self._path(name)

        if not path.exists():
            return None

        return path.read_text(
            encoding="utf-8",
        )

    def exists(
        self,
        name: str,
    ) -> bool:
        return self._path(name).exists()

    def list_names(
        self,
        prefix: str = "",
        suffix: str = "",
    ) -> list[str]:
        names = [
            path.name
            for path in self.base_dir.iterdir()
            if (
                path.is_file()
                and path.name.startswith(prefix)
                and path.name.endswith(suffix)
            )
        ]

        return sorted(
            names,
            reverse=True,
        )

class GoogleCloudStorageService(StorageService):
    """
    Google Cloud Storage implementation.

    Application artifacts are stored as private
    objects inside one configured bucket.
    """

    def __init__(
        self,
        client=None,
    ):
        if not settings.gcp_project_id:
            raise RuntimeError(
                "GCP_PROJECT_ID is not configured."
            )

        if not settings.gcs_bucket_name:
            raise RuntimeError(
                "GCS_BUCKET_NAME is not configured."
            )

        self.client = (
            client
            if client is not None
            else storage.Client(
                project=settings.gcp_project_id
            )
        )

        self.bucket = self.client.bucket(
            settings.gcs_bucket_name
        )

    def write_text(
        self,
        name: str,
        content: str,
    ) -> str:
        blob = self.bucket.blob(
            name
        )

        blob.upload_from_string(
            content,
            content_type="text/plain; charset=utf-8",
        )

        return name

    def read_text(
        self,
        name: str,
    ) -> str | None:
        blob = self.bucket.blob(
            name
        )

        if not blob.exists():
            return None

        return blob.download_as_text(
            encoding="utf-8"
        )

    def exists(
        self,
        name: str,
    ) -> bool:
        blob = self.bucket.blob(
            name
        )

        return blob.exists()

    def list_names(
        self,
        prefix: str = "",
        suffix: str = "",
    ) -> list[str]:
        blobs = self.client.list_blobs(
            self.bucket,
            prefix=prefix,
        )

        names = [
            blob.name
            for blob in blobs
            if blob.name.endswith(
                suffix
            )
        ]

        return sorted(
            names,
            reverse=True,
        )
    
_storage_service: StorageService | None = None


def get_storage_service() -> StorageService:
    """
    Return the configured storage backend.

    APP_ENV=local
        -> LocalStorageService

    APP_ENV=cloud
        -> GoogleCloudStorageService
    """

    global _storage_service

    if _storage_service is None:
        if settings.is_cloud:
            _storage_service = (
                GoogleCloudStorageService()
            )
        else:
            _storage_service = (
                LocalStorageService()
            )

    return _storage_service