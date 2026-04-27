import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


@dataclass
class Config:
    client_id: str
    client_secret: str
    user_agent: str
    post_limit: int = 100
    output_dir: Optional[Path] = None

    @classmethod
    def from_env(cls, env_path: Optional[Path] = None) -> "Config":
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
                "Please set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT. "
                "Copy .env.example to .env and fill in your values."
            )

        try:
            post_limit = int(post_limit_str)
        except ValueError:
            raise ConfigurationError(
                f"POST_LIMIT must be an integer, got '{post_limit_str}'"
            )

        return cls(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            post_limit=post_limit,
            output_dir=Path(output_dir_str) if output_dir_str else None,
        )


class ConfigurationError(Exception):
    pass
