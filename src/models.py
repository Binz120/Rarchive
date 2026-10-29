"""Data models for archived posts."""

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Optional


def _utc_now() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Post:
    """One archived Reddit post."""

    id: str
    title: str
    author: str
    score: int
    url: str
    created_utc: float
    selftext: str
    num_comments: int
    permalink: str
    flair: Optional[str] = None
    subreddit: Optional[str] = None
    retrieved_at: str = field(default_factory=_utc_now)

    @classmethod
    def from_praw_post(cls, post) -> "Post":
        """Build a Post from a PRAW submission object."""
        return cls(
            id=post.id,
            title=post.title,
            author=str(post.author) if post.author else "[deleted]",
            score=post.score,
            url=post.url,
            created_utc=post.created_utc,
            selftext=post.selftext or "",
            num_comments=post.num_comments,
            permalink=post.permalink,
            flair=post.link_flair_text,
            subreddit=str(post.subreddit),
        )

    def to_dict(self) -> dict:
        """Return the post as a plain dictionary."""
        return asdict(self)


@dataclass
class FetchResult:
    """The posts fetched from one subreddit listing."""

    posts: list[Post]
    subreddit: str
    sort_type: str
    fetched_at: str = field(default_factory=_utc_now)
