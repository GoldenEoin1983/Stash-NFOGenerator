# StashApp Plugin Development Guide

## Plugin Types

StashApp supports two plugin types:

| Type | Language | Use Case |
|------|----------|----------|
| **Embedded** | JavaScript (goja) | Simple tasks, runs inside StashApp process |
| **External** | Python, Go, etc. | Complex tasks, can use external libraries |

## Plugin Structure

A plugin requires a manifest file (`plugin.yml` or `<name>.yml`) in the plugin directory:

```
~/.stash/plugins/my_plugin/
├── my_plugin.yml      # Plugin manifest
├── my_plugin.py       # Entry point script
└── other_modules.py   # Additional code
```

## Plugin Manifest Format

```yaml
name: My Plugin Name
description: What the plugin does
version: 1.0
url: https://github.com/user/repo

exec:
  - python
  - "{pluginDir}/my_plugin.py"

interface: raw
errLog: error

tasks:
  - name: Task Display Name
    description: Task description shown in UI
    defaultArgs:
      mode: some_mode
```

### Key Fields

| Field | Description |
|-------|-------------|
| `name` | Display name in StashApp UI |
| `exec` | Command to run (use `{pluginDir}` for plugin path) |
| `interface` | `raw` for external plugins, `js` for embedded |
| `errLog` | Log level for stderr (`error`, `warn`, `debug`) |
| `tasks` | List of tasks shown in Settings > Tasks |

## External Python Plugin

### Input

Plugin receives JSON on stdin with server connection info:

```python
import json
import sys

raw_input = sys.stdin.read()
plugin_input = json.loads(raw_input)

server = plugin_input.get("server_connection", {})
# server contains: Scheme, Host, Port
```

### Connecting to StashApp

```python
from stashapi.stashapp import StashInterface
import stashapi.log as log

stash = StashInterface({
    "scheme": server.get("Scheme", "http"),
    "host": server.get("Host", "localhost"),
    "port": server.get("Port", 9999),
    "logger": log
})
```

### GraphQL Queries

```python
query = """
query FindScenes($filter: FindFilterType) {
    findScenes(filter: $filter) {
        count
        scenes { id, title }
    }
}
"""

variables = {"filter": {"page": 1, "per_page": 100}}
result = stash.call_GQL(query, variables)
```

### Logging & Progress

```python
import stashapi.log as log

log.info("Processing...")
log.debug("Debug message")
log.error("Error occurred")
log.progress(0.5)  # 50% progress (0.0 to 1.0)
```

### Output

Return JSON to stdout:

```python
output = {"Output": "Task completed successfully"}
print(json.dumps(output))
```

## Embedded JavaScript Plugin

For `interface: js`, use JavaScript with goja runtime:

```javascript
// Input available as global `input` object
var serverUrl = input.server_connection.Scheme + "://" +
                input.server_connection.Host + ":" +
                input.server_connection.Port;

// GraphQL
var result = gql.Do(query, variables);

// Logging
log.Info("Message");
log.Progress(0.5);

// Utility
util.Sleep(1000);  // milliseconds

// Return output
({
    Output: "Done"
});
```

## Common GraphQL Patterns

### Paginated Scene Query

```graphql
query FindScenes($filter: FindFilterType) {
    findScenes(filter: $filter) {
        count
        scenes {
            id
            title
            files { path }
        }
    }
}
```

Variables for pagination:
```json
{
    "filter": {
        "page": 1,
        "per_page": 100,
        "sort": "id",
        "direction": "ASC"
    }
}
```

### Filter Types

- `FindFilterType`: Pagination, sorting, text search (`q`)
- `SceneFilterType`: Scene-specific filters (path, rating, etc.)

## Dependencies

For Python plugins, users need:
```bash
pip install stashapp-tools
```

This provides `stashapi.stashapp.StashInterface` and `stashapi.log`.

## Installation Location

Plugins go in the StashApp plugins directory:
- Linux/Mac: `~/.stash/plugins/`
- Windows: `%USERPROFILE%\.stash\plugins\`

After adding/updating plugins: **Settings > Plugins > Reload Plugins**

Tasks appear in: **Settings > Tasks**
