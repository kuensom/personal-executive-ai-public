import json

from app.models import (
    DailyAnalysis,
    DashboardViewModel,
    HistoryDetailViewModel,
    HistoryItem,
    RunStatus,
    SystemOverview,
    UsageInfo,
)
from app.services.storage_service import (
    get_storage_service,
)


def read_json_artifact(
    name: str,
) -> dict:
    """Read and decode a JSON artifact."""

    storage = get_storage_service()

    content = storage.read_text(
        name
    )

    if content is None:
        raise FileNotFoundError(
            f"Artifact not found: {name}"
        )

    return json.loads(
        content
    )


def get_latest_name(
    prefix: str,
    suffix: str,
) -> str:
    """Return newest matching artifact name."""

    storage = get_storage_service()

    names = storage.list_names(
        prefix=prefix,
        suffix=suffix,
    )

    if not names:
        raise FileNotFoundError(
            "No artifacts found matching "
            f"{prefix}*{suffix}"
        )

    return names[0]


def get_run_status() -> RunStatus:
    """Return most recent run status."""

    data = read_json_artifact(
        "last_run.json"
    )

    return RunStatus(
        **data
    )


def get_latest_analysis() -> DailyAnalysis:
    """Return latest structured analysis."""

    name = get_latest_name(
        "analysis_",
        ".json",
    )

    return DailyAnalysis(
        **read_json_artifact(name)
    )


def get_latest_briefing() -> str:
    """Return latest human-readable briefing."""

    storage = get_storage_service()

    name = get_latest_name(
        "briefing_",
        ".txt",
    )

    content = storage.read_text(
        name
    )

    if content is None:
        raise FileNotFoundError(
            f"Artifact not found: {name}"
        )

    return content


def get_latest_usage() -> UsageInfo:
    """Return latest OpenAI usage statistics."""

    data = read_json_artifact(
        "latest_usage.json"
    )

    return UsageInfo(
        **data
    )


def extract_run_id(
    name: str,
    prefix: str,
    suffix: str,
) -> str:
    """Extract run ID from an artifact name."""

    return (
        name
        .removeprefix(prefix)
        .removesuffix(suffix)
    )


def get_history() -> list[HistoryItem]:
    """Return available historical analysis runs."""

    storage = get_storage_service()

    analysis_names = storage.list_names(
        prefix="analysis_",
        suffix=".json",
    )

    briefing_names = (
        storage.list_names(
            prefix="briefing_",
            suffix=".txt",
        )
    )

    briefing_by_run = {
        extract_run_id(
            name,
            "briefing_",
            ".txt",
        ): name
        for name in briefing_names
    }

    history = []

    for analysis_name in analysis_names:
        run_id = extract_run_id(
            analysis_name,
            "analysis_",
            ".json",
        )

        briefing_name = (
            briefing_by_run.get(
                run_id
            )
        )

        history.append(
            HistoryItem(
                timestamp=run_id,
                analysis_file=analysis_name,
                briefing_file=briefing_name,
            )
        )

    return history


def get_system_overview() -> SystemOverview:
    """Build consolidated system overview."""

    storage = get_storage_service()

    last_run = None
    latest_usage = None

    if storage.exists(
        "last_run.json"
    ):
        last_run = get_run_status()

    if storage.exists(
        "latest_usage.json"
    ):
        latest_usage = (
            get_latest_usage()
        )

    history_count = len(
        storage.list_names(
            prefix="analysis_",
            suffix=".json",
        )
    )

    return SystemOverview(
        status="ok",
        last_run=last_run,
        latest_usage=latest_usage,
        history_count=history_count,
    )


def get_dashboard_view(
    history_limit: int = 5,
) -> DashboardViewModel:
    """Build presentation model for dashboard."""

    last_run = None
    analysis = None
    usage = None

    try:
        last_run = get_run_status()
    except FileNotFoundError:
        pass

    try:
        analysis = get_latest_analysis()
    except FileNotFoundError:
        pass

    try:
        usage = get_latest_usage()
    except FileNotFoundError:
        pass

    history = get_history()

    return DashboardViewModel(
        system_status="ok",
        last_run=last_run,
        analysis=analysis,
        usage=usage,
        recent_history=history[
            :history_limit
        ],
    )


def get_analysis_by_run_id(
    run_id: str,
) -> DailyAnalysis:
    """Return analysis for one run."""

    name = (
        f"analysis_{run_id}.json"
    )

    return DailyAnalysis(
        **read_json_artifact(name)
    )


def get_briefing_by_run_id(
    run_id: str,
) -> str:
    """Return briefing for one run."""

    storage = get_storage_service()

    name = (
        f"briefing_{run_id}.txt"
    )

    content = storage.read_text(
        name
    )

    if content is None:
        raise FileNotFoundError(
            "Briefing not found for run: "
            f"{run_id}"
        )

    return content


def get_history_detail(
    run_id: str,
) -> HistoryDetailViewModel:
    """Build historical run detail view."""

    analysis = None
    briefing = None

    try:
        analysis = (
            get_analysis_by_run_id(
                run_id
            )
        )
    except FileNotFoundError:
        pass

    try:
        briefing = (
            get_briefing_by_run_id(
                run_id
            )
        )
    except FileNotFoundError:
        pass

    if (
        analysis is None
        and briefing is None
    ):
        raise FileNotFoundError(
            "No history found for run: "
            f"{run_id}"
        )

    return HistoryDetailViewModel(
        run_id=run_id,
        analysis=analysis,
        briefing=briefing,
    )