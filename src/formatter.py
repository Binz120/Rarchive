"""JSON output formatting."""

import json
from datetime import datetime
from pathlib import Path

from .models import FetchResult


class Formatter:
    """Write a FetchResult to disk as JSON."""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)

    def save_fetch_result(self, result: FetchResult) -> Path:
        """Write ``result`` under the output directory with a timestamped name."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{result.subreddit}_posts_{timestamp}.json"
        output_path = self.output_dir / filename
        return self._write_json(result, output_path)

    def save_to_directory(self, result: FetchResult, custom_dir: Path) -> Path:
        """Write ``result`` into ``custom_dir`` using a fixed file name."""
        filename = f"{result.subreddit}_posts.json"
        output_path = custom_dir / filename
        return self._write_json(result, output_path)

    def _write_json(self, result: FetchResult, path: Path) -> Path:
        """Serialise ``result`` to ``path``, creating parent directories."""
        path.parent.mkdir(exist_ok=True, parents=True)
        data = self._convert_for_json(result)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
        return path

    def _convert_for_json(self, result: FetchResult) -> dict:
        """Return the JSON-ready document for ``result``."""
        return {
            "subreddit": result.subreddit,
            "sort_type": result.sort_type,
            "fetched_at": result.fetched_at,
            "post_count": len(result.posts),
            "posts": [post.to_dict() for post in result.posts],
        }
