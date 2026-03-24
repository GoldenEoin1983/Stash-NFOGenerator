# StashApp NFO Generator

A StashApp plugin that generates Jellyfin-compatible NFO metadata files for all scenes in your library.

## Features

* Generates `.nfo` files next to each scene's video file
* Includes scene metadata: title, plot, studio, performers, tags, ratings
* Adds file info (video codec, resolution, duration)
* Progress tracking in StashApp task UI

## Installation

1. Copy the project to your StashApp plugins directory:

```bash
   cp -r Stash-NFOGenerator \~/.stash/plugins/nfo\_generator
   ```

2. Install the Python dependency:

```bash
   pip install stashapp-tools
   ```

3. Reload plugins in StashApp: **Settings > Plugins > Reload Plugins**

## Usage

1. Go to **Settings > Tasks** in StashApp
2. Find **"Generate NFO for All Scenes"**
3. Click **Run** to generate NFO files for your entire library

NFO files are saved alongside each video file:

* `video.mp4` → `video.nfo`

## Requirements

* Python >= 3.12
* StashApp
* `stashapp-tools` Python package

