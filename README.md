# Rarchive

A Python tool to archive posts from any public subreddit using Reddit's API via PRAW.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Features

- Download Reddit posts with rich metadata
- Organised JSON output with timestamps
- Environment-based configuration
- Modular architecture

---

## Installation

```bash
git clone https://github.com/Binz120/rarchive.git
cd rarchive
pip install -r requirements.txt
```

### Configuration

1. Create a Reddit App:
   - Visit [Reddit App Preferences](https://www.reddit.com/prefs/apps)
   - Click "Create App" > choose **"Script"**
   - Set redirect URI: `http://localhost:8080`

2. Copy `.env.example` to `.env` and fill in:
   ```env
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=script:rarchive:v2.0 (by /u/yourusername)
   ```

---

## Usage

```bash
python -m src
```

Or run directly:
```bash
python src/__main__.py
```

---

## Output

Posts are saved to the `output/` directory as JSON files:
```json
{
  "subreddit": "python",
  "sort_type": "new",
  "fetched_at": "2024-01-15T10:30:00",
  "post_count": 100,
  "posts": [...]
}
```

---

## Project Structure

```
src/
├── __init__.py      # Package init
├── __main__.py      # Entry point
├── config.py        # Configuration management
├── reddit_client.py # Reddit API wrapper
├── fetcher.py       # Post fetching logic
├── formatter.py     # JSON output formatting
└── models.py        # Data classes
```

---

## API Compliance

- Respects Reddit's rate limits (60 req/min)
- Do not collect personal/private data
- Follow [Reddit API Terms](https://www.reddit.com/wiki/apiterms)