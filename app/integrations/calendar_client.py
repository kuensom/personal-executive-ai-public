from datetime import datetime, time, timezone

from googleapiclient.discovery import build

from app.integrations.google_auth import get_google_credentials

from app.models import CalendarEvent


def get_calendar_service():
    """Create an authenticated Google Calendar API service."""
    credentials = get_google_credentials()

    service = build(
        "calendar",
        "v3",
        credentials=credentials,
    )

    return service


def get_today_events():
    """Return today's calendar events from the primary calendar."""
    service = get_calendar_service()

    now = datetime.now().astimezone()

    start_of_day = datetime.combine(
        now.date(),
        time.min,
        tzinfo=now.tzinfo,
    )

    end_of_day = datetime.combine(
        now.date(),
        time.max,
        tzinfo=now.tzinfo,
    )

    response = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start_of_day.isoformat(),
            timeMax=end_of_day.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    return response.get("items", [])


def normalise_event(event):
    """Convert Google Calendar API data into our CalendarEvent model."""

    start_data = event.get("start", {})
    end_data = event.get("end", {})

    all_day = "date" in start_data

    start = start_data.get(
        "dateTime",
        start_data.get("date"),
    )

    end = end_data.get(
        "dateTime",
        end_data.get("date"),
    )

    attendees = [
        attendee.get("email", "")
        for attendee in event.get("attendees", [])
        if attendee.get("email")
    ]

    return CalendarEvent(
        id=event.get("id", ""),
        title=event.get("summary", "(No title)"),
        start=start,
        end=end,
        location=event.get("location", ""),
        description=event.get("description", ""),
        attendees=attendees,
        all_day=all_day,
    )

def main():
    events = get_today_events()

    for raw_event in events:
        event = normalise_event(raw_event)

        print("-" * 60)
        print(f"Title:     {event.title}")
        print(f"Start:     {event.start}")
        print(f"End:       {event.end}")
        print(f"Location:  {event.location}")
        print(f"All day:   {event.all_day}")
        print(f"Attendees: {event.attendees}")


if __name__ == "__main__":
    main()