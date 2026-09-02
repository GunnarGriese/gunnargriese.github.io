from unittest.mock import MagicMock

from brevo.core.api_error import ApiError

from common.email_client import BatchSendResult, send_batch
from common.render import RenderedContent
from common.subscribers import Subscriber

SENDER = {"email": "news@gunnargriese.com", "name": "Gunnar Griese"}
RENDERED = RenderedContent(subject="Subject", html="<p>Body</p>", text="Body")


def recipients(n):
    return [
        (Subscriber(email=f"reader{i}@example.com"), {"unsubscribe_url": f"https://x.test/u/{i}"})
        for i in range(n)
    ]


def test_sends_one_call_for_a_small_list():
    email_client = MagicMock()

    result = send_batch(email_client, SENDER, RENDERED, recipients(3))

    assert email_client.send_transac_email.call_count == 1
    assert result == BatchSendResult(sent=3, failed=0, failed_emails=[])


def test_message_versions_carry_per_recipient_to_and_params():
    email_client = MagicMock()

    send_batch(email_client, SENDER, RENDERED, recipients(2))

    kwargs = email_client.send_transac_email.call_args.kwargs
    message_versions = kwargs["message_versions"]
    assert message_versions[0]["to"] == [{"email": "reader0@example.com"}]
    assert message_versions[0]["params"] == {"unsubscribe_url": "https://x.test/u/0"}
    assert message_versions[1]["to"] == [{"email": "reader1@example.com"}]


def test_request_carries_sender_subject_and_content():
    email_client = MagicMock()

    send_batch(email_client, SENDER, RENDERED, recipients(1))

    kwargs = email_client.send_transac_email.call_args.kwargs
    assert kwargs["sender"] == SENDER
    assert kwargs["subject"] == "Subject"
    assert kwargs["html_content"] == "<p>Body</p>"
    assert kwargs["text_content"] == "Body"


def test_chunks_large_recipient_lists_into_multiple_calls():
    email_client = MagicMock()

    result = send_batch(email_client, SENDER, RENDERED, recipients(1500), chunk_size=1000)

    assert email_client.send_transac_email.call_count == 2
    first_chunk = email_client.send_transac_email.call_args_list[0].kwargs["message_versions"]
    second_chunk = email_client.send_transac_email.call_args_list[1].kwargs["message_versions"]
    assert len(first_chunk) == 1000
    assert len(second_chunk) == 500
    assert result == BatchSendResult(sent=1500, failed=0, failed_emails=[])


def test_a_failing_chunk_is_recorded_as_failed_without_stopping_other_chunks():
    email_client = MagicMock()
    email_client.send_transac_email.side_effect = [
        ApiError(status_code=500, body="boom"),
        None,
    ]

    result = send_batch(email_client, SENDER, RENDERED, recipients(1500), chunk_size=1000)

    assert result.sent == 500
    assert result.failed == 1000
    assert len(result.failed_emails) == 1000
    assert result.failed_emails[0] == "reader0@example.com"
