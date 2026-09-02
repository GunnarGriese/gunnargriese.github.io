import json
import logging
from dataclasses import dataclass, field

from brevo.core.api_error import ApiError

from common.render import RenderedContent
from common.subscribers import Subscriber

DEFAULT_CHUNK_SIZE = 1000


@dataclass(frozen=True)
class BatchSendResult:
    sent: int
    failed: int
    failed_emails: list[str] = field(default_factory=list)


def _chunks(items: list, size: int):
    for start in range(0, len(items), size):
        yield items[start : start + size]


def send_batch(
    email_client,
    sender: dict[str, str],
    rendered: RenderedContent,
    recipients: list[tuple[Subscriber, dict[str, str]]],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> BatchSendResult:
    sent = 0
    failed_emails: list[str] = []

    for chunk in _chunks(recipients, chunk_size):
        message_versions = [
            {"to": [{"email": subscriber.email}], "params": params} for subscriber, params in chunk
        ]
        try:
            email_client.send_transac_email(
                sender=sender,
                subject=rendered.subject,
                html_content=rendered.html,
                text_content=rendered.text,
                message_versions=message_versions,
            )
            sent += len(chunk)
        except ApiError as error:
            failed_emails.extend(subscriber.email for subscriber, _ in chunk)
            logging.error(
                json.dumps(
                    {
                        "event": "batch_send_chunk_failed",
                        "count": len(chunk),
                        "status_code": error.status_code,
                    }
                )
            )

    return BatchSendResult(sent=sent, failed=len(failed_emails), failed_emails=failed_emails)
