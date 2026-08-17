from datetime import datetime

import json
import time
import traceback

from app.logger import get_logger
from app.notification_service import notify

from app.services.analysis_service import (
    analyse_daily_context,
    save_analysis,
)
from app.services.briefing_service import (
    render_morning_briefing,
)
from app.services.storage_service import (
    get_storage_service,
)


logger = get_logger("scheduler")


def write_status(
    status_data: dict,
) -> None:
    """Persist the latest agent execution status."""

    storage = get_storage_service()

    storage.write_text(
        "last_run.json",
        json.dumps(
            status_data,
            indent=2,
        ),
    )


def run():
    """
    Run the Personal Executive AI briefing workflow.

    Persistence is delegated to StorageService so
    the workflow works with either local filesystem
    or cloud storage.
    """

    storage = get_storage_service()

    start_time = time.perf_counter()

    logger.info(
        "Morning briefing started"
    )

    try:
        # One run ID is shared by analysis and briefing.
        run_id = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        # 1. Analyse current Gmail/Calendar context.
        analysis = analyse_daily_context()

        # 2. Persist structured analysis.
        analysis_artifact = save_analysis(
            analysis,
            run_id=run_id,
        )

        # 3. Render briefing from the SAME analysis.
        briefing = render_morning_briefing(
            analysis
        )

        # 4. Persist human-readable briefing.
        briefing_artifact = (
            f"briefing_{run_id}.txt"
        )

        storage.write_text(
            briefing_artifact,
            briefing,
        )

        logger.info(
            "Briefing completed successfully: %s",
            briefing_artifact,
        )

        elapsed = (
            time.perf_counter()
            - start_time
        )

        logger.info(
            "Execution time: %.2f seconds",
            elapsed,
        )

        # 5. Persist operational status.
        status = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "analysis_file": analysis_artifact,
            "briefing_file": briefing_artifact,
            "execution_seconds": round(
                elapsed,
                2,
            ),
        }

        write_status(
            status
        )

        # 6. Notify user / cloud log.
        notify(
            "Personal Executive AI",
            "Your morning briefing is ready.",
        )

        print(
            "Briefing saved to: "
            f"{briefing_artifact}"
        )

    except Exception as exc:
        elapsed = (
            time.perf_counter()
            - start_time
        )

        logger.error(
            "Morning briefing failed: %s",
            exc,
        )

        logger.error(
            "Failure after %.2f seconds",
            elapsed,
        )

        logger.debug(
            traceback.format_exc()
        )

        status = {
            "status": "failed",
            "timestamp": datetime.now().isoformat(),
            "execution_seconds": round(
                elapsed,
                2,
            ),
            "error": str(exc),
        }

        write_status(
            status
        )

        notify(
            "Personal Executive AI",
            "Morning briefing failed. "
            "Check application logs.",
        )

        raise


if __name__ == "__main__":
    run()