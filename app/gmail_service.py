import json
import os
import sys
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from dotenv import load_dotenv

from .database import SessionLocal
from . import models


load_dotenv()

APPS_SCRIPT_URL = os.getenv("APPS_SCRIPT_URL")
APPS_SCRIPT_TOKEN = os.getenv("APPS_SCRIPT_TOKEN")


def send_email(to: str, subject: str, body: str):
    """
    Send an email through the deployed Google Apps Script Web App.
    """

    if not APPS_SCRIPT_URL:
        raise RuntimeError("APPS_SCRIPT_URL is missing from .env")

    if not APPS_SCRIPT_TOKEN:
        raise RuntimeError("APPS_SCRIPT_TOKEN is missing from .env")

    payload = {
        "token": APPS_SCRIPT_TOKEN,
        "to": to,
        "subject": subject,
        "body": body,
    }

    data = json.dumps(payload).encode("utf-8")

    request = Request(
        APPS_SCRIPT_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=30) as response:
            response_data = response.read().decode("utf-8")

        result = json.loads(response_data)

        if not result.get("success"):
            raise RuntimeError(
                result.get("error", "Google Apps Script returned an error.")
            )

        return result

    except HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Apps Script HTTP error {e.code}: {error_body}"
        ) from e

    except URLError as e:
        raise RuntimeError(
            f"Could not connect to Apps Script: {e.reason}"
        ) from e


def send_lead_email(lead_id: int):
    """
    Send outreach email for one lead and update the database.
    """

    db = SessionLocal()

    try:
        lead = (
            db.query(models.Lead)
            .filter(models.Lead.id == lead_id)
            .first()
        )

        if not lead:
            raise RuntimeError(f"Lead ID {lead_id} was not found.")

        if not lead.email:
            raise RuntimeError(
                f"Lead ID {lead_id} does not have an email address."
            )

        if lead.outreach_status == "SENT":
            raise RuntimeError(
                f"Lead ID {lead_id} has already been sent an email."
            )

        if not lead.outreach_subject or not lead.outreach_body:
            raise RuntimeError(
                f"Lead ID {lead_id} does not have prepared outreach content."
            )

        print()
        print("--------------------------------")
        print("API EXPORT GMAIL SENDER")
        print("--------------------------------")
        print(f"Lead ID:    {lead.id}")
        print(f"Company:    {lead.company_name}")
        print(f"Recipient:  {lead.email}")
        print(f"Subject:    {lead.outreach_subject}")
        print()

        result = send_email(
            to=lead.email,
            subject=lead.outreach_subject,
            body=lead.outreach_body,
        )

        lead.outreach_status = "SENT"
        lead.sent_at = datetime.utcnow()

        db.commit()

        print("EMAIL SENT SUCCESSFULLY")
        print(f"Recipient: {lead.email}")
        print(f"Response:  {result}")

        return result

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def main():
    if len(sys.argv) != 2:
        print()
        print("Usage:")
        print("python -m app.gmail_service LEAD_ID")
        print()
        print("Example:")
        print("python -m app.gmail_service 5")
        print()
        sys.exit(1)

    try:
        lead_id = int(sys.argv[1])
    except ValueError:
        print("Lead ID must be a number.")
        sys.exit(1)

    try:
        send_lead_email(lead_id)
    except Exception as e:
        print()
        print("EMAIL SENDING FAILED")
        print(f"Error: {e}")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()