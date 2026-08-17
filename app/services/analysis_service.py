import json

from datetime import datetime

from app.config import settings
from app.integrations.ai_client import (
    MODEL,
    get_openai_client,
)
from app.logger import get_logger
from app.models import DailyAnalysis
from app.services.data_collector import (
    collect_daily_context,
)
from app.services.storage_service import (
    get_storage_service,
)


logger = get_logger("ai")


SYSTEM_INSTRUCTIONS = """
You are a personal executive assistant.

Analyse the supplied email and calendar data.

For each email:
- classify it as one of:
  urgent,
  action_required,
  awaiting_response,
  informational,
  low_priority
- assign priority:
  high,
  medium,
  low
- determine whether action is required
- summarise the purpose
- suggest a next action
- identify a deadline only if supported by the supplied data
- provide a confidence score between 0 and 1

For calendar events:
- identify scheduling conflicts
- identify preparation requirements
- identify unusually tight transitions
- add general observations only when useful
- provide a confidence score between 0 and 1

For the daily analysis:
- identify the most important immediate priorities
- identify sensible next actions

Rules:
- Do not invent facts.
- Do not infer deadlines without evidence.
- Clearly distinguish uncertainty.
- Do not create, modify, delete, send,
  accept, decline, or cancel anything.
"""


def build_context_payload(
    context: dict,
) -> dict:
    """
    Convert collected domain models into a
    JSON-serialisable payload for AI analysis.
    """

    return {
        "emails": [
            email.model_dump()
            for email in context.get(
                "emails",
                [],
            )
        ],
        "calendar": [
            event.model_dump()
            for event in context.get(
                "calendar",
                [],
            )
        ],
    }


def save_usage(
    response,
) -> None:
    """Persist latest OpenAI token usage."""

    if not response.usage:
        return

    usage_data = {
        "model": MODEL,
        "input_tokens": (
            response.usage.input_tokens
        ),
        "output_tokens": (
            response.usage.output_tokens
        ),
        "total_tokens": (
            response.usage.total_tokens
        ),
    }

    storage = get_storage_service()

    storage.write_text(
        "latest_usage.json",
        json.dumps(
            usage_data,
            indent=2,
        ),
    )


def analyse_daily_context() -> DailyAnalysis:
    """
    Collect current email/calendar context and
    produce structured AI analysis.

    The OpenAI client is created lazily so that
    importing this module does not require an API key.
    """

    logger.info(
        "Collecting daily context for AI analysis."
    )

    context = collect_daily_context()

    payload = build_context_payload(
        context
    )

    client = get_openai_client()

    logger.info(
        "Submitting daily context for AI analysis."
    )

    response = client.responses.parse(
        model=MODEL,
        instructions=SYSTEM_INSTRUCTIONS,
        input=json.dumps(
            payload,
            indent=2,
        ),
        text_format=DailyAnalysis,
    )

    if response.output_parsed is None:
        raise RuntimeError(
            "OpenAI returned no structured DailyAnalysis."
        )

    save_usage(
        response
    )

    logger.info(
        "Daily AI analysis completed successfully."
    )

    return response.output_parsed


def save_analysis(
    analysis: DailyAnalysis,
    run_id: str | None = None,
) -> str:
    """
    Persist structured DailyAnalysis.

    Returns the storage-neutral artifact name.
    """

    if run_id is None:
        run_id = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

    artifact_name = (
        f"analysis_{run_id}.json"
    )

    storage = get_storage_service()

    storage.write_text(
        artifact_name,
        analysis.model_dump_json(
            indent=2
        ),
    )

    logger.info(
        "Structured analysis saved: %s",
        artifact_name,
    )

    return artifact_name


def main():
    """
    Run analysis directly from the command line.
    """

    analysis = analyse_daily_context()

    output_file = save_analysis(
        analysis
    )

    print(
        analysis.model_dump_json(
            indent=2
        )
    )

    print(
        f"\nAnalysis saved to: {output_file}"
    )


if __name__ == "__main__":
    main()