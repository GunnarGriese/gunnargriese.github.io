from dataclasses import dataclass
from pathlib import Path

import frontmatter


class MissingSubjectError(ValueError):
    pass


@dataclass(frozen=True)
class Announcement:
    subject: str
    body_md: str
    post_url: str | None = None


def parse_announcement(path: str | Path) -> Announcement:
    post = frontmatter.load(path)
    subject = post.get("subject")
    if not subject:
        raise MissingSubjectError(f"{path}: frontmatter is missing required 'subject' field")
    return Announcement(subject=subject, body_md=post.content, post_url=post.get("post_url"))
