# DuckDuckGo Web Search Skill

An Agent Skill for searching web content via DuckDuckGo. No API key required.

## Features

- **Web Search**: General web search with DuckDuckGo
- **News Search**: Dedicated news content search
- **JSON Output**: Programmatically parseable results
- **Flexible Filters**: Region, time limits, and safe search options
- **Proxy Support**: HTTP/HTTPS/SOCKS5 proxy support via CLI args or environment variables

## Installation

### Via ClawHub (Recommended)

```bash
clawhub install ddgs-search-api
```

### Manual Installation

1. Clone the project locally, then copy the `skills/ddgs-search` directory to a common Agent Skill installation directory:
   - **OpenClaw**: `~/.openclaw/skills/`
   - **Claude Code**: `~/.claude/skills/` (global) or `<YourProject>/.claude/skills/` (project-local)
   - **General**: `~/.agents/skills/`

2. Install dependencies with `uv`:

```bash
cd skills/ddgs-search
uv pip install ddgs
```

Or run directly (uv will auto-install dependencies):

```bash
uv run scripts/ddgs_search.py "your search query"
```

## Usage Examples

```bash
# Basic search
uv run scripts/ddgs_search.py "Python tutorial"

# Use proxy via command line
uv run scripts/ddgs_search.py "query" --proxy http://1.2.3.4:8080

# Use proxy via environment variable
export HTTP_PROXY="http://proxy.example.com:8080"
uv run scripts/ddgs_search.py "query"
```

### Proxy Configuration

Proxy settings are resolved in the following priority order:
1. Command line: `--proxy` / `-p`
2. Environment variable: `HTTP_PROXY` or `http_proxy`
3. Environment variable: `DDGS_PROXY`

Supported proxy protocols: `http`, `https`, `socks5`, `socks5h`

## Dependencies

- Python 3.9+
- [uv](https://docs.astral.sh/uv/) package manager
- [ddgs](https://github.com/deedy5/ddgs) >= 8.0.0

## License

MIT
