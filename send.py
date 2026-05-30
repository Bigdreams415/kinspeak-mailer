"""
send.py — Bulk beta-welcome emails to everyone in beta-tester.csv
"""

import csv
import os
import time

import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.environ["RESEND_API_KEY"]

TEMPLATE_ID       = os.environ["RESEND_TEMPLATE_ID"]
FROM_EMAIL        = os.environ["FROM_EMAIL"]
INVITE_LINK       = os.environ["INVITE_LINK"]
FEEDBACK_FORM_LINK = os.environ["FEEDBACK_FORM_LINK"]

CSV_FILE = "beta-tester.csv"

# Column names exactly as they appear in the CSV header
COL_NAME  = "What's your name?"
COL_EMAIL = "What's your email address?"


def first_name(full_name: str) -> str:
    """Return the first token of a name string, title-cased."""
    return full_name.strip().split()[0].title() if full_name.strip() else "there"


def send_to(email: str, name: str) -> dict:
    params: resend.Emails.SendParams = {
        "from": FROM_EMAIL,
        "to":   [email],
        "template": {
            "id": TEMPLATE_ID,
            "variables": {
                "firstName":        first_name(name),
                "inviteLink":       INVITE_LINK,
                "feedbackFormLink": FEEDBACK_FORM_LINK,
            },
        },
    }
    return resend.Emails.send(params)


def main():
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if r[COL_EMAIL].strip()]

    print(f"Sending to {len(rows)} tester(s)...\n")

    ok, failed = [], []

    for row in rows:
        email = row[COL_EMAIL].strip()
        name  = row[COL_NAME].strip()

        try:
            result = send_to(email, name)
            print(f"  ✓  {email}  (id: {result.get('id', '?')})")
            ok.append(email)
        except Exception as exc:
            print(f"  ✗  {email}  → {exc}")
            failed.append(email)

        # Stay within Resend's rate limit (2 req/s on free tier)
        time.sleep(0.6)

    print(f"\nDone — {len(ok)} sent, {len(failed)} failed.")
    if failed:
        print("Failed addresses:")
        for addr in failed:
            print(f"  {addr}")


if __name__ == "__main__":
    main()
