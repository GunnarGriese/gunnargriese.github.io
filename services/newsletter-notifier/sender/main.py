import argparse
import json
import logging
import os
import sys
from pathlib import Path

import brevo
from dotenv import load_dotenv
from google.cloud import bigquery

from common.content import parse_announcement
from common.email_client import send_batch
from common.render import build_unsubscribe_params, render_content
from common.subscribers import get_active_subscribers


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Send a newsletter announcement to active subscribers."
    )
    parser.add_argument("--content", required=True, help="Path to the announcement Markdown file.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the send (recipient count + rendered content) without contacting Brevo.",
    )
    return parser.parse_args(argv)


def run(
    content_path: str | Path,
    dry_run: bool,
    bq_client,
    email_client,
    contacts_table: str,
    unsubscribes_table: str,
    unsubscribe_base_url: str,
    unsubscribe_secret: str,
    sender: dict[str, str],
) -> None:
    announcement = parse_announcement(content_path)
    rendered = render_content(announcement)
    subscribers = get_active_subscribers(bq_client, contacts_table, unsubscribes_table)
    recipients = [
        (
            subscriber,
            build_unsubscribe_params(subscriber, unsubscribe_base_url, unsubscribe_secret),
        )
        for subscriber in subscribers
    ]

    if dry_run:
        print(f"DRY RUN -- {len(recipients)} recipient(s) would receive this email:")
        print(f"Subject: {rendered.subject}")
        print("--- HTML preview ---")
        print(rendered.html)
        print("--- Text preview ---")
        print(rendered.text)
        return

    result = send_batch(email_client, sender, rendered, recipients)
    logging.info(
        json.dumps({"event": "send_complete", "sent": result.sent, "failed": result.failed})
    )
    print(f"Sent {result.sent}, failed {result.failed}.")
    if result.failed:
        sys.exit(1)


def main(argv=None) -> None:
    load_dotenv()
    args = parse_args(argv)

    bq_client = bigquery.Client()
    email_client = None
    sender = None
    if not args.dry_run:
        email_client = brevo.Brevo(api_key=os.environ["BREVO_API_KEY"]).transactional_emails
        sender = {"email": os.environ["SENDER_EMAIL"], "name": os.environ["SENDER_NAME"]}

    run(
        content_path=args.content,
        dry_run=args.dry_run,
        bq_client=bq_client,
        email_client=email_client,
        contacts_table=os.environ["BQ_CONTACTS_TABLE"],
        unsubscribes_table=os.environ["BQ_UNSUBSCRIBES_TABLE"],
        unsubscribe_base_url=os.environ["UNSUBSCRIBE_BASE_URL"],
        unsubscribe_secret=os.environ["UNSUBSCRIBE_SIGNING_KEY"],
        sender=sender,
    )


if __name__ == "__main__":
    main()
