#!/usr/bin/env python3
"""
StashApp Plugin: Jellyfin NFO Generator

Generates Jellyfin-compatible NFO files for all scenes in the StashApp library.
NFO files are saved next to each scene's video file.
"""

import json
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import stashapi.log as log
from stashapi.stashapp import StashInterface

from converters import StashToNfoConverter
from nfo_generator import NfoGenerator


def get_all_scenes(stash: StashInterface, page_size: int = 100):
    """
    Fetch all scenes with file paths using pagination.

    Args:
        stash: StashInterface instance
        page_size: Number of scenes per page

    Returns:
        List of scene data dictionaries
    """
    # Query includes all fields needed for NFO generation
    query = """
    query FindScenes($filter: FindFilterType) {
        findScenes(filter: $filter) {
            count
            scenes {
                id
                title
                details
                date
                rating100
                studio {
                    name
                }
                performers {
                    name
                    gender
                }
                tags {
                    name
                }
                files {
                    path
                    duration
                    video_codec
                    audio_codec
                    width
                    height
                    frame_rate
                    bit_rate
                }
                created_at
                updated_at
            }
        }
    }
    """

    all_scenes = []
    page = 1

    while True:
        variables = {
            "filter": {
                "page": page,
                "per_page": page_size,
                "sort": "id",
                "direction": "ASC"
            }
        }

        result = stash.call_GQL(query, variables)
        scenes = result.get("findScenes", {}).get("scenes", [])

        if not scenes:
            break

        all_scenes.extend(scenes)

        total = result.get("findScenes", {}).get("count", 0)
        log.debug(f"Fetched page {page}: {len(scenes)} scenes ({len(all_scenes)}/{total})")

        if len(all_scenes) >= total:
            break

        page += 1

    return all_scenes


def main():
    """Main plugin entry point."""
    # Parse plugin input from stdin
    raw_input = sys.stdin.read()
    plugin_input = json.loads(raw_input)

    # Get server connection info
    server = plugin_input.get("server_connection", {})

    # Initialize Stash connection
    stash = StashInterface({
        "scheme": server.get("Scheme", "http"),
        "host": server.get("Host", "localhost"),
        "port": server.get("Port", 9999),
        "logger": log
    })

    # Initialize converters
    converter = StashToNfoConverter()
    generator = NfoGenerator(encoding='utf-8', pretty_print=True)

    log.info("Starting NFO generation for all scenes...")

    # Get all scenes with pagination
    all_scenes = get_all_scenes(stash)
    total_scenes = len(all_scenes)

    log.info(f"Found {total_scenes} scenes to process")

    processed = 0
    errors = 0
    skipped = 0

    for i, scene in enumerate(all_scenes):
        try:
            # Update progress
            progress = (i + 1) / total_scenes
            log.progress(progress)

            # Get file path
            files = scene.get("files", [])
            if not files:
                log.debug(f"Scene {scene['id']} has no files, skipping")
                skipped += 1
                continue

            video_path = Path(files[0]["path"])
            nfo_path = video_path.with_suffix(".nfo")

            # Convert scene data to NFO format
            nfo_data = converter.convert(scene, "scene")

            # Generate NFO XML
            nfo_xml = generator.generate(nfo_data, "scene")

            # Write NFO file
            with open(nfo_path, 'w', encoding='utf-8') as f:
                f.write(nfo_xml)

            processed += 1
            log.debug(f"Generated: {nfo_path}")

        except Exception as e:
            errors += 1
            log.error(f"Error processing scene {scene.get('id')}: {e}")

    log.info(f"NFO generation complete: {processed} processed, {skipped} skipped, {errors} errors")

    # Return plugin output
    output = {
        "Output": f"Generated {processed} NFO files ({errors} errors, {skipped} skipped)"
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
