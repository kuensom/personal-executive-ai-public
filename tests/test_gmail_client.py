from app.integrations.gmail_client import normalise_message


def test_normalise_message():
    raw_message = {
        "id": "msg-123",
        "snippet": "Please review the attached document.",
        "labelIds": ["INBOX", "UNREAD"],
        "payload": {
            "headers": [
                {
                    "name": "From",
                    "value": "Alice <alice@example.com>",
                },
                {
                    "name": "Subject",
                    "value": "Document review",
                },
                {
                    "name": "Date",
                    "value": "Mon, 10 Aug 2026 09:00:00 +0800",
                },
            ]
        },
    }

    email = normalise_message(raw_message)

    assert email.id == "msg-123"
    assert email.sender == "Alice <alice@example.com>"
    assert email.subject == "Document review"
    assert email.is_unread is True
    assert email.snippet == "Please review the attached document."