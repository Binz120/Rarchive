from typing import Callable, Optional

from .models import Post, FetchResult
from .reddit_client import RedditClient


SORT_METHODS = {
    "new": "new",
    "hot": "hot",
    "top": "top",
    "rising": "rising",
    "controversial": "controversial",
}


class InvalidSortTypeError(Exception):
    pass


class Fetcher:
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
        print(f"[{count}] {title[:50]}...")

    def fetch_posts(
        self,
        subreddit_name: str,
        sort: str = "new",
    ) -> FetchResult:
        subreddit = self.client.get_subreddit(subreddit_name)

        sort_method = SORT_METHODS.get(sort)
        if sort_method is None:
            raise InvalidSortTypeError(
                f"Unknown sort type '{sort}'. Valid options: {', '.join(SORT_METHODS)}"
            )

        generator = getattr(subreddit, sort_method, None)
        if generator is None:
            raise InvalidSortTypeError(f"Subreddit has no '{sort_method}' listing")

        posts: list[Post] = []

        for idx, praw_post in enumerate(generator(limit=self.limit), 1):
            post = Post.from_praw_post(praw_post)
            posts.append(post)
            self.progress_callback(idx, post.title)

        return FetchResult(
            posts=posts,
            subreddit=subreddit_name,
            sort_type=sort,
        )
