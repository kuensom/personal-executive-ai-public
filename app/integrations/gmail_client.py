from googleapiclient.discovery import build

from app.integrations.google_auth import get_google_credentials

from app.models import EmailMessage

def get_gmail_service():
    """Create an authenticated Gmail API service."""
    credentials = get_google_credentials()

    service = build(
        "gmail",
        "v1",
        credentials=credentials,
    )

    return service

def normalise_message(message):
    """Convert a Gmail API response into our EmailMessage model."""

    headers = message.get("payload", {}).get("headers", [])

    header_map = {
        header["name"].lower(): header["value"]
        for header in headers
    }

    labels = message.get("labelIds", [])

    return EmailMessage(
        id=message.get("id", ""),
        sender=header_map.get("from", ""),
        subject=header_map.get("subject", ""),
        received_at=header_map.get("date"),
        snippet=message.get("snippet", ""),
        is_unread="UNREAD" in labels,
        labels=labels,
    )

def list_recent_messages(max_results=5):
    """Return IDs of the most recent Gmail messages."""
    service = get_gmail_service()

    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            maxResults=max_results,
        )
        .execute()
    )

    return response.get("messages", [])

""" Function to retrieve selected metadata for a Gmail message.

def get_message_details(message_id):
    
    service = get_gmail_service()

    message = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="metadata",
            metadataHeaders=[
                "From",
                "Subject",
                "Date",
            ],
        )
        .execute()
    )

    headers = message.get("payload", {}).get("headers", [])

    header_map = {
        header["name"]: header["value"]
        for header in headers
    }

    return {
        "id": message_id,
        "from": header_map.get("From", ""),
        "subject": header_map.get("Subject", ""),
        "date": header_map.get("Date", ""),
        "snippet": message.get("snippet", ""),
    }
 """

def get_message(message_id):
    """Retrieve Gmail metadata for one message."""

    service = get_gmail_service()

    return (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="metadata",
            metadataHeaders=[
                "From",
                "Subject",
                "Date",
            ],
        )
        .execute()
    )

def main():
    messages = list_recent_messages()

    print(f"Found {len(messages)} recent messages.\n")

    for message_ref in messages:
        raw_message = get_message(message_ref["id"])

        email = normalise_message(raw_message)

        print("-" * 60)
        print(f"ID:      {email.id}")
        print(f"From:    {email.sender}")
        print(f"Subject: {email.subject}")
        print(f"Date:    {email.received_at}")
        print(f"Unread:  {email.is_unread}")
        print(f"Snippet: {email.snippet}")


if __name__ == "__main__":
    main()