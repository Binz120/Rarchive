# Rarchive

Archive posts from any public subreddit through Reddit's API with PRAW.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://github.com/Binz120/Rarchive/actions/workflows/ci.yml/badge.svg)

---

## Features

- Fetch `new`, `hot`, `top`, `rising` and `controversial` listings
- Rich post metadata: score, author, flair, selftext, comments, permalinks
- One timestamped JSON file per run
- Environment-based configuration, no credentials in the code
- Small, testable modules with a linted CI

---

## Requirements

- Python 3.10 or newer
- [`praw`](https://praw.readthedocs.io/) >= 7.7
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) >= 1.0

---

## Installation

```bash
git clone https://github.com/Binz120/Rarchive.git
cd Rarchive
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuration

1. Create a Reddit app:
   - Open [Reddit app preferences](https://www.reddit.com/prefs/apps)
   - **Create app** → type **script**
   - Redirect URI: `http://localhost:8080`

2. Copy the example file and fill it in:

   ```bash
   cp .env.example .env
   ```

   ```env
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=script:rarchive:v2.0 (by /u/yourusername)

   # optional
   POST_LIMIT=100
   OUTPUT_DIR=output
   ```

`.env` is git-ignored. Never commit it.

---

## Usage

Run from the repository root — the package and the `.env` lookup are both
relative to it.

```bash
python -m src                       # asks for the subreddit
python -m src python                # r/python, 100 posts, sort=new
python -m src python --limit 250 --sort top
python -m src rust --sort controversial --output ~/archives/rust
```

| flag | default | |
| --- | --- | --- |
| positional `subreddit` | prompt | subreddit name without `r/` |
| `--limit` | `POST_LIMIT` (100) | posts to fetch |
| `--sort` | `new` | `hot`, `new`, `top`, `rising`, `controversial` |
| `--output` | `OUTPUT_DIR` (output) | where the JSON file is written |

`python -m src --help` lists everything.

---

## Output

Each run writes `output/<subreddit>_posts_<YYYYmmdd_HHMMSS>.json`:

```json
{
  "subreddit": "python",
  "sort_type": "new",
  "fetched_at": "2026-04-27T20:31:04+00:00",
  "post_count": 100,
  "posts": [
    {
      "id": "1abc2de",
      "title": "Example post",
      "author": "someone",
      "score": 42,
      "url": "https://example.com",
      "created_utc": 1714000000.0,
      "selftext": "",
      "num_comments": 7,
      "permalink": "/r/python/comments/1abc2de/example_post/",
      "flair": null,
      "subreddit": "python",
      "retrieved_at": "2026-04-27T20:31:04.5512+00:00"
    }
  ]
}
```

---

## Project structure

```
src/
├── __init__.py      # package version
├── __main__.py      # CLI entry point and exit codes
├── config.py        # .env / environment handling
├── reddit_client.py # PRAW wrapper
├── fetcher.py       # listing → Post objects
├── formatter.py     # JSON output
└── models.py        # Post / FetchResult dataclasses
tests/
└── test_smoke.py    # CLI smoke tests, no network needed
```

---

## Development

```bash
pip install -r requirements.txt pylint
pylint $(git ls-files '*.py')
python -m unittest discover -s tests -v
```

CI runs both on Python 3.10, 3.11 and 3.12 for every push and pull request.

---

## API compliance

- Read-only, unauthenticated-user access; no posting, voting or messaging
- One listing request per page, well inside Reddit's rate limits
- Public data only — nothing private, nothing from private subreddits
- Follows the [Reddit API terms](https://www.reddit.com/wiki/apiterms)
