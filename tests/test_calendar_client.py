from app.integrations.calendar_client import normalise_event


def test_normalise_event():
    raw_event = {
        "id": "event-123",
        "summary": "Project Meeting",
        "start": {
            "dateTime": "2026-08-10T10:00:00+08:00",
        },
        "end": {
            "dateTime": "2026-08-10T11:00:00+08:00",
        },
        "location": "Teams",
        "description": "Weekly project review",
        "attendees": [
            {
                "email": "alice@example.com",
            },
            {
                "email": "bob@example.com",
            },
        ],
    }

    event = normalise_event(raw_event)

    assert event.id == "event-123"
    assert event.title == "Project Meeting"
    assert event.location == "Teams"
    assert event.all_day is False

    assert event.attendees == [
        "alice@example.com",
        "bob@example.com",
    ]