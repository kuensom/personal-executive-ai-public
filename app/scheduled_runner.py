from datetime import datetime
from pathlib import Path
import json
import time
import traceback

from app.logger import get_logger
from app.notification_service import notify

from app.services.analysis_service import (
    analyse_daily_context,
    save_analysis,
)

from app.services.briefing_service import render_morning_briefing


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
STATUS_FILE = LOG_DIR / "last_run.json"

logger = get_logger("scheduler")

def write_status(status_data: dict):
    """Persist the latest agent execution status."""
    STATUS_FILE.write_text(
        json.dumps(
            status_data,
            indent=2,
        ),
        encoding="utf-8",
    )


def run():
    """Run the scheduled Personal Executive AI briefing workflow."""

    LOG_DIR.mkdir(exist_ok=True)

    start_time = time.perf_counter()

    logger.info("Morning briefing started")

    try:
        # 1. Generate the briefing
        #---briefing = render_morning_briefing()
        # Run AI analysis once
        analysis = analyse_daily_context()

        # Persist the structured result
        analysis_file = save_analysis(analysis)

        # Render the human-readable briefing
        # from the SAME analysis
        briefing = render_morning_briefing(analysis)

        # 2. Create timestamped output filename
        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        output_file = (
            LOG_DIR
            / f"briefing_{timestamp}.txt"
        )

        # 3. Persist briefing
        output_file.write_text(
            briefing,
            encoding="utf-8",
        )

        # This is our operational SUCCESS POINT.
        # The AI workflow has completed and the briefing
        # has been successfully persisted.
        logger.info(
            "Briefing completed successfully: %s",
            output_file,
        )

        # 4. Measure execution time
        elapsed = (
            time.perf_counter()
            - start_time
        )

        logger.info(
            "Execution time: %.2f seconds",
            elapsed,
        )

        # 5. Record successful run status
        status = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "analysis_file": str(analysis_file),
            "briefing_file": str(output_file),
            "execution_seconds": round(
                elapsed,
                2,
            ),
        }

        write_status(status)

        # 6. Notify the user
        notify(
            "Personal Executive AI",
            "Your morning briefing is ready.",
        )

        # 7. Terminal / launchd output
        print(
            f"Briefing saved to: {output_file}"
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

        # Record failed run
        status = {
            "status": "failed",
            "timestamp": datetime.now().isoformat(),
            "execution_seconds": round(
                elapsed,
                2,
            ),
            "error": str(exc),
        }

        write_status(status)

        # Optional failure notification
        notify(
            "Personal Executive AI",
            "Morning briefing failed. Check agent.log.",
        )

        # Re-raise so launchd can see that
        # execution did not complete normally.
        raise


if __name__ == "__main__":
    run()