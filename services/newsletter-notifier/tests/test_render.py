from urllib.parse import parse_qs, urlparse

from common.content import Announcement
from common.render import UNSUBSCRIBE_PLACEHOLDER, build_unsubscribe_params, render_content
from common.subscribers import Subscriber
from common.tokens import verify_token


def test_render_content_keeps_subject_unchanged():
    announcement = Announcement(subject="Hello subscribers", body_md="Some **bold** text.")

    rendered = render_content(announcement)

    assert rendered.subject == "Hello subscribers"


def test_render_content_converts_markdown_to_html():
    announcement = Announcement(subject="Subject", body_md="Some **bold** text.")

    rendered = render_content(announcement)

    assert "<strong>bold</strong>" in rendered.html


def test_render_content_keeps_plaintext_body_readable():
    announcement = Announcement(subject="Subject", body_md="Some **bold** text.")

    rendered = render_content(announcement)

    assert "Some **bold** text." in rendered.text


def test_render_content_includes_unsubscribe_placeholder_in_html_and_text():
    announcement = Announcement(subject="Subject", body_md="Body.")

    rendered = render_content(announcement)

    assert UNSUBSCRIBE_PLACEHOLDER in rendered.html
    assert UNSUBSCRIBE_PLACEHOLDER in rendered.text


def test_render_content_links_to_post_url_when_present():
    announcement = Announcement(subject="Subject", body_md="Body.", post_url="https://x.test/p")

    rendered = render_content(announcement)

    assert "https://x.test/p" in rendered.html
    assert "https://x.test/p" in rendered.text


def test_render_content_omits_post_link_when_absent():
    announcement = Announcement(subject="Subject", body_md="Body.")

    rendered = render_content(announcement)

    assert "Read the full post" not in rendered.html
    assert "Read the full post" not in rendered.text


def test_build_unsubscribe_params_url_is_verifiable_for_that_subscriber():
    subscriber = Subscriber(email="reader@example.com")

    params = build_unsubscribe_params(subscriber, "https://gunnargriese.com/unsubscribe", "secret")

    parsed = urlparse(params["unsubscribe_url"])
    query = parse_qs(parsed.query)
    assert query["email"] == ["reader@example.com"]
    assert verify_token("reader@example.com", query["token"][0], "secret") is True


def test_build_unsubscribe_params_rejects_token_for_a_different_secret():
    subscriber = Subscriber(email="reader@example.com")

    params = build_unsubscribe_params(subscriber, "https://gunnargriese.com/unsubscribe", "secret")

    query = parse_qs(urlparse(params["unsubscribe_url"]).query)
    assert verify_token("reader@example.com", query["token"][0], "wrong-secret") is False
