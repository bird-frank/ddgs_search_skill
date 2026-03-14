# DuckDuckGo Web Search Skill

An Agent Skill for searching web content via DuckDuckGo. No API key required.

## Features

- **Web Search**: General web search with DuckDuckGo
- **News Search**: Dedicated news content search
- **JSON Output**: Programmatically parseable results
- **Flexible Filters**: Region, time limits, and safe search options

## Installation

### Via ClawHub (Recommended)

```bash
clawhub install ddgs-search
```

### Manual Installation

1. Clone or copy the `skills/ddgs-search` directory to your project
2. Install dependencies with `uv`:

```bash
cd skills/ddgs-search
uv pip install ddgs
```

Or run directly (uv will auto-install dependencies):

```bash
uv run scripts/ddgs_search.py "your search query"
```

## Dependencies

- Python 3.9+
- [uv](https://docs.astral.sh/uv/) package manager
- [ddgs](https://github.com/deedy5/ddgs) >= 8.0.0

## License

MIT
