"""
send_test.py — Send a single beta-welcome email for personal testing.

Usage:
    python send_test.py                              # sends to your own email with name "there"
    python send_test.py you@gmail.com                # sends to that address
    python send_test.py you@gmail.com "Your Name"   # personalised name
"""

import os
import sys

import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.environ["RESEND_API_KEY"]

TEMPLATE_ID        = os.environ["RESEND_TEMPLATE_ID"]
FROM_EMAIL         = os.environ["FROM_EMAIL"]
INVITE_LINK        = os.environ["INVITE_LINK"]
FEEDBACK_FORM_LINK = os.environ["FEEDBACK_FORM_LINK"]

# Parse args or fall back to defaults in .env
TO_EMAIL   = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("TEST_EMAIL", "your-email@example.com")
FIRST_NAME = sys.argv[2] if len(sys.argv) > 2 else "there"


params: resend.Emails.SendParams = {
    "from": FROM_EMAIL,
    "to":   [TO_EMAIL],
    "template": {
        "id": TEMPLATE_ID,
        "variables": {
            "firstName":        FIRST_NAME,
            "inviteLink":       INVITE_LINK,
            "feedbackFormLink": FEEDBACK_FORM_LINK,
        },
    },
}

print(f"Sending test email to {TO_EMAIL} as '{FIRST_NAME}'...")

try:
    result = resend.Emails.send(params)
    print(f"Sent! Email id: {result.get('id')}")
except Exception as exc:
    print(f"Failed: {exc}")
