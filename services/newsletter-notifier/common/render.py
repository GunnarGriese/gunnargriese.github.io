from dataclasses import dataclass
from urllib.parse import quote

import markdown as markdown_lib

from common.content import Announcement
from common.subscribers import Subscriber
from common.tokens import generate_token

UNSUBSCRIBE_PLACEHOLDER = "{{ params.unsubscribe_url }}"


@dataclass(frozen=True)
class RenderedContent:
    subject: str
    html: str
    text: str


def render_content(announcement: Announcement) -> RenderedContent:
    html_parts = [markdown_lib.markdown(announcement.body_md)]
    text_parts = [announcement.body_md.strip()]

    if announcement.post_url:
        html_parts.append(f'<p><a href="{announcement.post_url}">Read the full post</a></p>')
        text_parts.append(f"Read the full post: {announcement.post_url}")

    html_parts.append(
        f'<p style="font-size: 0.8em;"><a href="{UNSUBSCRIBE_PLACEHOLDER}">Unsubscribe</a></p>'
    )
    text_parts.append(f"Unsubscribe: {UNSUBSCRIBE_PLACEHOLDER}")

    return RenderedContent(
        subject=announcement.subject,
        html="\n".join(html_parts),
        text="\n\n".join(text_parts),
    )


def build_unsubscribe_params(subscriber: Subscriber, base_url: str, secret: str) -> dict[str, str]:
    token = generate_token(subscriber.email, secret)
    email = quote(subscriber.email)
    return {"unsubscribe_url": f"{base_url}?email={email}&token={token}"}
