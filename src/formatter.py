import json
from datetime import datetime
from pathlib import Path

from .models import FetchResult


class Formatter:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)

    def save_fetch_result(self, result: FetchResult) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{result.subreddit}_posts_{timestamp}.json"
        output_path = self.output_dir / filename
        return self._write_json(result, output_path)

    def save_to_directory(self, result: FetchResult, custom_dir: Path) -> Path:
        filename = f"{result.subreddit}_posts.json"
        output_path = custom_dir / filename
        return self._write_json(result, output_path)

    def _write_json(self, result: FetchResult, path: Path) -> Path:
        path.parent.mkdir(exist_ok=True, parents=True)
        data = self._convert_for_json(result)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    def _convert_for_json(self, result: FetchResult) -> dict:
        return {
            "subreddit": result.subreddit,
            "sort_type": result.sort_type,
            "fetched_at": result.fetched_at,
            "post_count": len(result.posts),
            "posts": [post.to_dict() for post in result.posts],
        }
