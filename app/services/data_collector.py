from app.integrations.gmail_client import (
    get_message,
    list_recent_messages,
    normalise_message,
)

from app.integrations.calendar_client import (
    get_today_events,
    normalise_event,
)


def collect_emails(max_results=10):
    """Collect and normalise recent emails."""

    message_refs = list_recent_messages(
        max_results=max_results
    )

    emails = []

    for message_ref in message_refs:
        raw_message = get_message(
            message_ref["id"]
        )

        emails.append(
            normalise_message(raw_message)
        )

    return emails


def collect_calendar_events():
    """Collect and normalise today's calendar."""

    raw_events = get_today_events()

    return [
        normalise_event(event)
        for event in raw_events
    ]


def collect_daily_context():
    """Collect information required for the daily briefing."""

    return {
        "emails": collect_emails(),
        "calendar": collect_calendar_events(),
    }


def main():
    context = collect_daily_context()

    print(
        f"Emails collected: "
        f"{len(context['emails'])}"
    )

    print(
        f"Calendar events collected: "
        f"{len(context['calendar'])}"
    )


if __name__ == "__main__":
    main()