"""Reddit API client wrapper."""

from typing import Optional

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
        """Check if a subreddit exists."""
        try:
            sub = self._reddit.subreddit(name)
            return bool(sub.title)
        except Exception:
            return False