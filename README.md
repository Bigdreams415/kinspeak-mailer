# KinSpeak Mailer

Sends personalised beta-welcome emails to testers via [Resend](https://resend.com).

---

## Setup

**1. Activate the virtual environment**
```bash
cd kinspeak-mailer
source venv/bin/activate
```

**2. Fill in `.env`**

| Variable | What to put |
|---|---|
| `RESEND_API_KEY` | Already set |
| `RESEND_TEMPLATE_ID` | ID from Resend dashboard (looks like `tmpl_xxxx`) |
| `FROM_EMAIL` | A sender address on a verified Resend domain |
| `INVITE_LINK` | Your Firebase App Distribution invite URL |
| `FEEDBACK_FORM_LINK` | Your Google Form URL |

> Make sure your Resend template uses these exact variable names: `firstName`, `inviteLink`, `feedbackFormLink`.

---

## Test — send to yourself first

```bash
# Sends to your own email with a generic greeting
python send_test.py

# Sends to a specific address
python send_test.py you@gmail.com

# Sends with a personalised name
python send_test.py you@gmail.com "Joshua"
```

Check your inbox, confirm everything looks right, then send to everyone.

---

## Bulk send — all testers in the CSV

```bash
python send.py
```

This reads `beta-tester.csv`, sends one email per tester, and prints a summary:

```
Sending to 13 tester(s)...

  ✓  ogudufavour41@gmail.com  (id: abc123)
  ✓  ngozichukwufrancis01@gmail.com  (id: abc124)
  ...

Done — 13 sent, 0 failed.
```

> A 0.6 s delay between sends keeps you within Resend's rate limit.

---

## Notes

- **First name extraction** — the script uses the first word of each tester's full name. If a name comes out wrong you can edit the `first_name()` function in `send.py`.
- **Re-sending to failed addresses** — if any sends fail, addresses are printed at the end. You can re-run `send_test.py` with that address to retry individually.
- **Free tier limit** — Resend free tier allows 100 emails/day and 3,000/month, which is well above the 13 testers in the CSV.
# kinspeak-mailer
