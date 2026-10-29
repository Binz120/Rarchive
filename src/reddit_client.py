"""Reddit API client wrapper."""

import praw

from .config import Config


class RedditClient:
    """Wrapper for PRAW Reddit client."""

    def __init__(self, config: Config):
        """Initialize the Reddit client."""
        self._reddit = praw.Reddit(
            client_id=config.client_id,
            client_secret=config.client_secret,
            user_agent=config.user_agent,
        )

    def get_subreddit(self, name: str) -> praw.models.Subreddit:
        """Get a subreddit by name."""
        return self._reddit.subreddit(name)

    def validate_subreddit(self, name: str) -> bool:
        """Check that a subreddit exists and exposes a title."""
        try:
            sub = self._reddit.subreddit(name)
            return bool(sub.title)
        except Exception:  # pylint: disable=broad-exception-caught
            # PRAW raises several unrelated types here (redirect, 403, 404).
            return False
