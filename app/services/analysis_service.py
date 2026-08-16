import json

from app.integrations.ai_client import client, MODEL
from app.services.data_collector import collect_daily_context
from app.models import DailyAnalysis

from app.logger import get_logger

from datetime import datetime
from pathlib import Path

logger = get_logger("ai")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"
USAGE_FILE = LOG_DIR / "latest_usage.json"


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


def build_context_payload(context):
    return {
        "emails": [
            email.model_dump()
            for email in context["emails"]
        ],
        "calendar": [
            event.model_dump()
            for event in context["calendar"]
        ],
    }


def analyse_daily_context() -> DailyAnalysis:
    context = collect_daily_context()

    payload = build_context_payload(context)

    response = client.responses.parse(
        model=MODEL,
        instructions=SYSTEM_INSTRUCTIONS,
        input=json.dumps(payload, indent=2),
        text_format=DailyAnalysis,
    )

    if response.usage:
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

        USAGE_FILE.write_text(
            json.dumps(
                usage_data,
                indent=2,
            ),
            encoding="utf-8",
        )

    return response.output_parsed

def save_analysis(
    analysis: DailyAnalysis,
    output_dir: Path = LOG_DIR,
    run_id: str | None = None,
) -> Path:
    """Persist structured DailyAnalysis as JSON."""

    output_dir.mkdir(exist_ok=True)

    if run_id is None:
        run_id = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

    output_file = (
        output_dir
        / f"analysis_{run_id}.json"
    )

    output_file.write_text(
        analysis.model_dump_json(
            indent=2
        ),
        encoding="utf-8",
    )

    return output_file

def main():
    analysis = analyse_daily_context()

    output_file = save_analysis(analysis)

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