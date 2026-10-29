"""Post fetching logic."""

from typing import Callable, Optional

from .models import FetchResult, Post
from .reddit_client import RedditClient

SORT_METHODS = {
    "new": "new",
    "hot": "hot",
    "top": "top",
    "rising": "rising",
    "controversial": "controversial",
}


class InvalidSortTypeError(Exception):
    """Raised when a listing sort type is not supported."""


class Fetcher:
    """Fetch posts from a subreddit through a RedditClient."""

    def __init__(
        self,
        client: RedditClient,
        limit: int = 100,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ):
        self.client = client
        self.limit = limit
        self.progress_callback = progress_callback or self._default_progress

    @staticmethod
    def _default_progress(count: int, title: str) -> None:
        """Print one line per fetched post."""
        print(f"[{count}] {title[:50]}...")

    def fetch_posts(
        self,
        subreddit_name: str,
        sort: str = "new",
    ) -> FetchResult:
        """Fetch up to ``self.limit`` posts from ``subreddit_name``."""
        sort_method = SORT_METHODS.get(sort)
        if sort_method is None:
            raise InvalidSortTypeError(
                f"Unknown sort type '{sort}'. Valid options: {', '.join(SORT_METHODS)}"
            )

        subreddit = self.client.get_subreddit(subreddit_name)
        listing = getattr(subreddit, sort_method, None)
        if listing is None:
            raise InvalidSortTypeError(f"Subreddit has no '{sort_method}' listing")

        posts: list[Post] = []

        for idx, praw_post in enumerate(listing(limit=self.limit), 1):
            post = Post.from_praw_post(praw_post)
            posts.append(post)
            self.progress_callback(idx, post.title)

        return FetchResult(
            posts=posts,
            subreddit=subreddit_name,
            sort_type=sort,
        )
