# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

StashApp to NFO Converter - A Python CLI tool that converts StashApp metadata into Jellyfin compatible NFO (XML) files. Supports input from JSON files or direct StashApp GraphQL API queries.

## Development Commands

```bash
# Setup environment (requires Python >= 3.12, uses uv)
uv sync

# Run converter from JSON file
uv run python stash_to_nfo.py scene.json --pretty

# Run converter from StashApp API
uv run python stash_to_nfo.py --stash-id 123 --verbose
uv run python stash_to_nfo.py --search "query" --stash-host localhost --stash-port 9999
```

## Architecture

The application follows a Parser-Converter-Generator pattern with linear data flow:

```
Input → StashParser → StashToNfoConverter → NfoGenerator → NFO XML
              ↑
        StashApiClient (alternative input via GraphQL)
```

### Core Components

| File | Purpose |
|------|---------|
| `stash_to_nfo.py` | CLI entry point, orchestrates input/output, handles arguments |
| `parsers.py` | `StashParser` - reads JSON files, auto-detects data type (scene/performer/gallery) |
| `converters.py` | `StashToNfoConverter` - transforms StashApp data → NFO dict format |
| `nfo_generator.py` | `NfoGenerator` - produces XML using ElementTree + minidom |
| `stash_api.py` | `StashApiClient` - wraps `stashapp-tools` for GraphQL API access |

### Adding a New Metadata Field

1. **Parser** (`parsers.py`): Update `detect_type()` if the field helps identify data type
2. **Converter** (`converters.py`): Map field in `_convert_scene()`, `_convert_performer()`, or `_convert_gallery()`
3. **Generator** (`nfo_generator.py`): Add XML element in `_generate_movie_nfo()` or `_generate_actor_nfo()`

### GraphQL Queries

Located in `stash_api.py`. When the `stashapp-tools` library doesn't provide a helper method, raw GraphQL queries are used (see `get_gallery()`, `find_scene_by_path()`, `search_scenes()`). To add fields:
- Edit the query string, keeping variable structure consistent
- Update corresponding converter/parser to handle new fields

## Code Style

- Include comments explaining functions
- Include TODO comments for potential improvements
- Use simple, everyday language in documentation
- Rating conversion: StashApp uses 1-5 scale, NFO uses 0-10 (multiply by 2)

## Dependencies

- `stashapp-tools>=0.2.58` - Official StashApp API client for GraphQL
- Python standard library: `xml.etree.ElementTree`, `xml.dom.minidom`, `json`, `argparse`, `pathlib`
