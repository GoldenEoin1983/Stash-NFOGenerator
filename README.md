# Stash NFO Converter/Generator

A command-line tool that converts Stash JSON metadata files into Kodi/Jellyfin compatible NFO files & 
A Stash plugin that generates Jellyfin-compatible NFO metadata files for all scenes in your library.

## Features

### Converter
- **Multiple Data Types**: Supports StashApp scenes, performers, and galleries
- **Auto-Detection**: Automatically detects the type of StashApp data
- **Kodi/Jellyfin Compatible**: Generates properly formatted NFO files with UTF-8 encoding
- **Field Mapping**: Maps StashApp fields to appropriate NFO XML tags
- **Error Handling**: Comprehensive error handling for invalid files and operations
- **Flexible Output**: Configurable output formatting and encoding
### Generator/Plugin
- ** Generates `.nfo` files next to each scene's video file
- ** Includes scene metadata: title, plot, studio, performers, tags, ratings
- ** Adds file info (video codec, resolution, duration)
- ** Progress tracking in StashApp task UI

## Installation

No installation required. Just ensure you have Python 3.6+ installed.
1. Copy the project to your StashApp plugins directory:

## Usage
```bash
   cp -r Stash-NFOGenerator \~/.stash/plugins/nfo\_generator
   ```

### Basic Usage
2. Install the Python dependency:

```bash
# Convert a scene JSON file
python stash_to_nfo.py scene.json
   pip install stashapp-tools
   ```

3. Reload plugins in StashApp: **Settings > Plugins > Reload Plugins**

## Usage

1. Go to **Settings > Tasks** in StashApp
2. Find **"Generate NFO for All Scenes"**
3. Click **Run** to generate NFO files for your entire library

NFO files are saved alongside each video file:

* `video.mp4` → `video.nfo`

# Specify output file
python stash_to_nfo.py scene.json output.nfo
## Requirements

# Convert performer data
python stash_to_nfo.py --type performer performer.json
* Python >= 3.12
* StashApp
* `stashapp-tools` Python package

# Convert gallery data
python stash_to_nfo.py --type gallery gallery.json