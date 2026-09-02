from pathlib import Path

import pytest

from common.content import MissingSubjectError, parse_announcement

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_announcement_reads_subject_and_post_url():
    announcement = parse_announcement(FIXTURES / "sample_announcement.md")

    assert announcement.subject == "New post: Signal Engineering 101"
    assert announcement.post_url == "https://gunnargriese.com/posts/signal-engineering-101/"


def test_parse_announcement_reads_body_markdown():
    announcement = parse_announcement(FIXTURES / "sample_announcement.md")

    assert "signal engineering" in announcement.body_md
    assert "server-side tagging" in announcement.body_md


def test_parse_announcement_post_url_is_optional():
    announcement = parse_announcement(FIXTURES / "freestanding_announcement.md")

    assert announcement.subject == "A quick update"
    assert announcement.post_url is None


def test_parse_announcement_raises_typed_error_when_subject_missing():
    with pytest.raises(MissingSubjectError):
        parse_announcement(FIXTURES / "missing_subject_announcement.md")
