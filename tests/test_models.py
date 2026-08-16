from app.models import EmailMessage, CalendarEvent


def test_email_message_model():
    email = EmailMessage(
        id="123",
        sender="test@example.com",
        subject="Test",
        snippet="Example email",
        is_unread=True,
    )

    assert email.id == "123"
    assert email.sender == "test@example.com"
    assert email.is_unread is True


def test_calendar_event_model():
    event = CalendarEvent(
        id="event-1",
        title="Test Meeting",
        start="2026-08-11T09:00:00+08:00",
        end="2026-08-11T10:00:00+08:00",
    )

    assert event.id == "event-1"
    assert event.title == "Test Meeting"