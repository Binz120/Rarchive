import argparse
import sys
from pathlib import Path

from .config import Config, ConfigurationError
from .reddit_client import RedditClient
from .fetcher import Fetcher, InvalidSortTypeError
from .formatter import Formatter


def main():
    parser = argparse.ArgumentParser(description="Archive Reddit posts")
    parser.add_argument("subreddit", nargs="?", help="Subreddit name")
    parser.add_argument("--limit", type=int, default=None, help="Number of posts to fetch")
    parser.add_argument("--sort", default="new", choices=["hot", "new", "top", "rising", "controversial"], help="Sort type")
    parser.add_argument("--output", default=None, help="Output directory")
    args = parser.parse_args()

    print("Rarchive v2.0")
    print("-" * 40)

    try:
        config = load_config()
    except ConfigurationError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    if args.limit is not None:
        config.post_limit = args.limit
    if args.output is not None:
        config.output_dir = Path(args.output)

    subreddit = args.subreddit or get_subreddit_name()

    try:
        client = RedditClient(config)
    except Exception as e:
        print(f"Failed to connect to Reddit: {e}")
        sys.exit(1)

    if not client.validate_subreddit(subreddit):
        print(f"Subreddit r/{subreddit} does not exist or is not accessible.")
        sys.exit(1)

    print(f"\nFetching {config.post_limit} posts from r/{subreddit} ({args.sort})...")

    fetcher = Fetcher(
        client=client,
        limit=config.post_limit,
        progress_callback=lambda idx, title: print(f"[{idx}] {title[:50]}"),
    )

    try:
        result = fetcher.fetch_posts(subreddit, sort=args.sort)
    except InvalidSortTypeError as e:
        print(f"Invalid sort type: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to fetch posts: {e}")
        sys.exit(1)

    print(f"\nFetched {len(result.posts)} posts")

    output_dir = str(config.output_dir) if config.output_dir else "output"
    formatter = Formatter(output_dir=output_dir)
    try:
        output_path = formatter.save_fetch_result(result)
        print(f"Saved to: {output_path}")
    except Exception as e:
        print(f"Failed to save results: {e}")
        sys.exit(1)

    print("\nDone!")


def load_config() -> Config:
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        return Config.from_env(env_path)
    return Config.from_env()


def get_subreddit_name() -> str:
    while True:
        name = input("Enter subreddit name: ").strip()
        if name:
            return name
        print("Please enter a subreddit name.")


if __name__ == "__main__":
    main()
