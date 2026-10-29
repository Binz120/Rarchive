"""Command line entry point for Rarchive."""

import argparse
import sys
from pathlib import Path

from .config import Config, ConfigurationError
from .fetcher import Fetcher, InvalidSortTypeError
from .formatter import Formatter
from .reddit_client import RedditClient

SORT_CHOICES = ["hot", "new", "top", "rising", "controversial"]


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the CLI."""
    parser = argparse.ArgumentParser(description="Archive Reddit posts")
    parser.add_argument("subreddit", nargs="?", help="Subreddit name")
    parser.add_argument(
        "--limit", type=int, default=None, help="Number of posts to fetch"
    )
    parser.add_argument("--sort", default="new", choices=SORT_CHOICES, help="Sort type")
    parser.add_argument("--output", default=None, help="Output directory")
    return parser


def load_config() -> Config:
    """Load configuration from ./.env when present, else from the environment."""
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        return Config.from_env(env_path)
    return Config.from_env()


def get_subreddit_name() -> str:
    """Prompt until a non-empty subreddit name is entered."""
    while True:
        name = input("Enter subreddit name: ").strip()
        if name:
            return name
        print("Please enter a subreddit name.")


def main() -> int:  # pylint: disable=too-many-return-statements
    """Run the CLI and return the process exit code.

    Each failure path prints its own message and exits non-zero, so the
    returns are the interface, not a refactoring accident.
    """
    args = build_parser().parse_args()

    print("Rarchive v2.0")
    print("-" * 40)

    try:
        config = load_config()
    except ConfigurationError as exc:
        print(f"Configuration error: {exc}")
        return 1

    if args.limit is not None:
        config.post_limit = args.limit
    if args.output is not None:
        config.output_dir = Path(args.output)

    subreddit = args.subreddit or get_subreddit_name()

    try:
        client = RedditClient(config)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(f"Failed to connect to Reddit: {exc}")
        return 1

    if not client.validate_subreddit(subreddit):
        print(f"Subreddit r/{subreddit} does not exist or is not accessible.")
        return 1

    print(f"\nFetching {config.post_limit} posts from r/{subreddit} ({args.sort})...")

    fetcher = Fetcher(
        client=client,
        limit=config.post_limit,
        progress_callback=lambda idx, title: print(f"[{idx}] {title[:50]}"),
    )

    try:
        result = fetcher.fetch_posts(subreddit, sort=args.sort)
    except InvalidSortTypeError as exc:
        print(f"Invalid sort type: {exc}")
        return 1
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(f"Failed to fetch posts: {exc}")
        return 1

    print(f"\nFetched {len(result.posts)} posts")

    output_dir = str(config.output_dir) if config.output_dir else "output"
    formatter = Formatter(output_dir=output_dir)
    try:
        output_path = formatter.save_fetch_result(result)
        print(f"Saved to: {output_path}")
    except OSError as exc:
        print(f"Failed to save results: {exc}")
        return 1

    print("\nDone!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
