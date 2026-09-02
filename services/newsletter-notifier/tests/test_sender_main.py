from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from common.content import MissingSubjectError
from sender.main import parse_args, run

FIXTURES = Path(__file__).parent / "fixtures"
SENDER = {"email": "news@gunnargriese.com", "name": "Gunnar Griese"}


def make_bq_client(emails):
    bq_client = MagicMock()
    bq_client.query.return_value.result.return_value = [
        SimpleNamespace(email=email) for email in emails
    ]
    return bq_client


def run_kwargs(**overrides):
    kwargs = dict(
        content_path=FIXTURES / "sample_announcement.md",
        dry_run=False,
        bq_client=make_bq_client(["a@example.com", "b@example.com"]),
        email_client=MagicMock(),
        contacts_table="project.dataset.contact_form",
        unsubscribes_table="project.dataset.newsletter_unsubscribes",
        unsubscribe_base_url="https://gunnargriese.com/unsubscribe",
        unsubscribe_secret="secret",
        sender=SENDER,
    )
    kwargs.update(overrides)
    return kwargs


def test_parse_args_reads_content_and_dry_run_flag():
    args = parse_args(["--content", "announcements/x.md", "--dry-run"])

    assert args.content == "announcements/x.md"
    assert args.dry_run is True


def test_parse_args_dry_run_defaults_to_false():
    args = parse_args(["--content", "announcements/x.md"])

    assert args.dry_run is False


def test_dry_run_never_calls_the_email_client():
    email_client = MagicMock()

    run(**run_kwargs(dry_run=True, email_client=email_client))

    email_client.send_transac_email.assert_not_called()


def test_dry_run_prints_recipient_count_and_subject(capsys):
    run(**run_kwargs(dry_run=True))

    out = capsys.readouterr().out
    assert "2" in out
    assert "New post: Signal Engineering 101" in out


def test_real_run_sends_one_call_per_active_subscriber_and_logs_summary(capsys):
    email_client = MagicMock()

    run(**run_kwargs(dry_run=False, email_client=email_client))

    assert email_client.send_transac_email.call_count == 1
    message_versions = email_client.send_transac_email.call_args.kwargs["message_versions"]
    assert len(message_versions) == 2
    out = capsys.readouterr().out
    assert "2" in out


def test_run_raises_a_typed_error_when_subject_missing():
    with pytest.raises(MissingSubjectError):
        run(**run_kwargs(content_path=FIXTURES / "missing_subject_announcement.md", dry_run=True))
