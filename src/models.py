from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Post:
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
    retrieved_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @classmethod
    def from_praw_post(cls, post) -> "Post":
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
        return asdict(self)


@dataclass
class FetchResult:
    posts: list[Post]
    subreddit: str
    sort_type: str
    fetched_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
