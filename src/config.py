"""Configuration loading for Rarchive."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - python-dotenv is a hard requirement
    load_dotenv = None


class ConfigurationError(Exception):
    """Raised when required configuration is missing or malformed."""


@dataclass
class Config:
    """Reddit API credentials and run settings."""

    client_id: str
    client_secret: str
    user_agent: str
    post_limit: int = 100
    output_dir: Optional[Path] = None

    @classmethod
    def from_env(cls, env_path: Optional[Path] = None) -> "Config":
        """Build a config from the environment, optionally loading a .env file."""
        if load_dotenv and env_path:
            load_dotenv(env_path)
        elif load_dotenv:
            load_dotenv()

        client_id = os.getenv("REDDIT_CLIENT_ID") or ""
        client_secret = os.getenv("REDDIT_CLIENT_SECRET") or ""
        user_agent = os.getenv("REDDIT_USER_AGENT") or ""
        post_limit_str = os.getenv("POST_LIMIT", "100")
        output_dir_str = os.getenv("OUTPUT_DIR") or None

        if not client_id or not client_secret or not user_agent:
            raise ConfigurationError(
                "Missing required environment variables. "
                "Please set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and "
                "REDDIT_USER_AGENT. Copy .env.example to .env and fill in "
                "your values."
            )

        try:
            post_limit = int(post_limit_str)
        except ValueError as exc:
            raise ConfigurationError(
                f"POST_LIMIT must be an integer, got '{post_limit_str}'"
            ) from exc

        return cls(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            post_limit=post_limit,
            output_dir=Path(output_dir_str) if output_dir_str else None,
        )
