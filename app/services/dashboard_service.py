import json
from pathlib import Path

from app.models import DashboardViewModel

from app.models import HistoryDetailViewModel

from app.models import (
    DailyAnalysis,
    HistoryItem,
    RunStatus,
    SystemOverview,
    UsageInfo,
)


BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"

STATUS_FILE = LOG_DIR / "last_run.json"
USAGE_FILE = LOG_DIR / "latest_usage.json"


def read_json_file(path: Path) -> dict:
    """Read and decode a JSON file."""

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path.name}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def get_latest_file(pattern: str) -> Path:
    """Return the most recently modified file matching a pattern."""

    files = sorted(
        LOG_DIR.glob(pattern),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    if not files:
        raise FileNotFoundError(
            f"No files found matching {pattern}"
        )

    return files[0]


def get_run_status() -> RunStatus:
    """Return the most recent agent run status."""

    data = read_json_file(
        STATUS_FILE
    )

    return RunStatus(
        **data
    )


def get_latest_analysis() -> DailyAnalysis:
    """Return the latest structured AI analysis."""

    latest_file = get_latest_file(
        "analysis_*.json"
    )

    data = read_json_file(
        latest_file
    )

    return DailyAnalysis(
        **data
    )


def get_latest_briefing() -> str:
    """Return the latest human-readable briefing."""

    latest_file = get_latest_file(
        "briefing_*.txt"
    )

    return latest_file.read_text(
        encoding="utf-8"
    )


def get_latest_usage() -> UsageInfo:
    """Return the latest OpenAI usage statistics."""

    data = read_json_file(
        USAGE_FILE
    )

    return UsageInfo(
        **data
    )


def extract_run_id(
    path: Path,
    prefix: str,
    suffix: str,
) -> str:
    """Extract the run ID from an output filename."""

    return (
        path.name
        .removeprefix(prefix)
        .removesuffix(suffix)
    )


def get_history() -> list[HistoryItem]:
    """Return available historical analysis runs."""

    analysis_files = sorted(
        LOG_DIR.glob(
            "analysis_*.json"
        ),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    briefing_files = {
        extract_run_id(
            path,
            "briefing_",
            ".txt",
        ): path
        for path in LOG_DIR.glob(
            "briefing_*.txt"
        )
    }

    history = []

    for analysis_file in analysis_files:
        run_id = extract_run_id(
            analysis_file,
            "analysis_",
            ".json",
        )

        briefing_file = (
            briefing_files.get(
                run_id
            )
        )

        history.append(
            HistoryItem(
                timestamp=run_id,
                analysis_file=str(
                    analysis_file
                ),
                briefing_file=(
                    str(briefing_file)
                    if briefing_file
                    else None
                ),
            )
        )

    return history


def get_system_overview() -> SystemOverview:
    """Build a consolidated system overview."""

    last_run = None
    latest_usage = None

    if STATUS_FILE.exists():
        last_run = get_run_status()

    if USAGE_FILE.exists():
        latest_usage = get_latest_usage()

    history_count = len(
        list(
            LOG_DIR.glob(
                "analysis_*.json"
            )
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
    """Build the presentation model for the dashboard."""

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
        recent_history=history[:history_limit],
    )

def get_analysis_by_run_id(
    run_id: str,
) -> DailyAnalysis:
    """Return structured analysis for a specific run."""

    path = (
        LOG_DIR
        / f"analysis_{run_id}.json"
    )

    data = read_json_file(path)

    return DailyAnalysis(
        **data
    )

def get_briefing_by_run_id(
    run_id: str,
) -> str:
    """Return briefing text for a specific run."""

    path = (
        LOG_DIR
        / f"briefing_{run_id}.txt"
    )

    if not path.exists():
        raise FileNotFoundError(
            f"Briefing not found for run: {run_id}"
        )

    return path.read_text(
        encoding="utf-8"
    )

def get_history_detail(
    run_id: str,
) -> HistoryDetailViewModel:
    """Build the history detail view."""

    analysis = None
    briefing = None

    try:
        analysis = get_analysis_by_run_id(
            run_id
        )
    except FileNotFoundError:
        pass

    try:
        briefing = get_briefing_by_run_id(
            run_id
        )
    except FileNotFoundError:
        pass

    if analysis is None and briefing is None:
        raise FileNotFoundError(
            f"No history found for run: {run_id}"
        )

    return HistoryDetailViewModel(
        run_id=run_id,
        analysis=analysis,
        briefing=briefing,
    )

