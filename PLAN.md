# Subreddit Post Downloader - Rewrite Plan

## Project Overview

A Python tool to archive posts from any public Reddit subreddit. Current implementation is a single 60-line script with hardcoded credentials and minimal features.

---

## Goals

- Modern, maintainable architecture with proper error handling
- Easy to use for casual users (interactive prompts)
- Enhanced reliability and config management

---

## Architecture

### Modules

```
src/
├── __init__.py
├── config.py         # Configuration management
├── reddit_client.py # Reddit API wrapper
├── fetcher.py      # Post fetching logic
├── formatter.py    # Output formatting (JSON)
└── main.py         # Entry point / CLI
```

### Class Design

**RedditClient** (`reddit_client.py`)
- Manages PRAW connection
- Handles authentication
- Exposes subreddit access

**PostFetcher** (`fetcher.py`)
- Fetches posts from a subreddit
- Filtering options (limit, sort)
- Progress tracking

**ConfigManager** (`config.py`)
- Loads credentials from environment
- Validates required settings
- Provides defaults

---

## Features

1. **Configuration**
   - Environment variable loading (`.env` support)
   - Validation on startup
   - Clear error messages for missing config

2. **User Interface**
   - Interactive prompts with defaults
   - Progress indicators during download
   - Summary output on completion

3. **Data Fetching**
   - Support for different post sorts (hot, new, top, rising)
   - Configurable post limit
   - Graceful handling of removed/deleted posts

4. **Output**
   - JSON format (preserved)
   - Timestamped directories
   - Rich metadata (more fields)

5. **Error Handling**
   - Network errors: retry with backoff
   - API errors: clear messages
   - Rate limiting: automatic handling

---

## Migration from Current Code

| Current | New |
|---------|-----|
| Single file | Modular package |
| Hardcoded credentials | Environment/`.env` |
| `subreddit.new(limit=None)` | Configurable sort + limit |
| Basic error print | Logging + graceful handling |
| No type hints | Full type annotations |
| No tests | Unit tests included |

---

## File Structure

```
/
├── .env.example       # Template for credentials
├── requirements.txt  # Updated dependencies
├── setup.py         # Package setup (optional)
├── README.md        # Updated documentation
└── src/
    ├── __init__.py
    ├── __main__.py
    ├── config.py
    ├── reddit_client.py
    ├── fetcher.py
    ├── formatter.py
    └── models.py    # Data classes
```

---

## Dependencies

- `praw>=7.7.0` - Reddit API
- `python-dotenv>=1.0.0` - Env loading
- ` typing` - Type hints (stdlib)

---

## Implementation Order

1. `models.py` - Data classes
2. `config.py` - Configuration management
3. `reddit_client.py` - API client
4. `fetcher.py` - Fetching logic
5. `formatter.py` - Output formatting
6. `__main__.py` - CLI / entry point
7. Update `requirements.txt`, `README.md`

---

## Testing

- Unit tests for each module
- Mock PRAW for API tests
- Validate JSON output structure