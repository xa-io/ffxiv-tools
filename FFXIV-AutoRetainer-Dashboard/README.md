# FFXIV AutoRetainer Dashboard v1.02

A self-hosted web dashboard that displays FFXIV character data from AutoRetainer's DefaultConfig.json. Provides a modern, dark-themed UI accessible via browser showing characters, submarines, retainers, marketboard items, gil totals, and income/cost calculations.

<img width="807" height="430" alt="image" src="https://github.com/user-attachments/assets/32005cc8-a331-4ae8-a7f6-9c2109cada22" />

## Features

- **Self-Hosted Web Server**: Flask-based server with configurable host/port (default: `127.0.0.1:1234`)
- **Real-Time Data**: Parses AutoRetainer DefaultConfig.json on each page load
- **Altoholic Integration**: Reads treasure values from Altoholic's altoholic.db
- **Multi-Account Support**: Configure multiple accounts via config.json
- **Auto-Refresh**: Configurable auto-refresh interval (default: 60 seconds)
- **Modern UI**: Dark-themed responsive design with collapsible sections
- **Ready Status Indicators**: Visual highlighting when retainers/submarines are ready

### Data Displayed

#### Summary Cards
- Total Gil across all accounts
- Treasure Value (from Altoholic)
- Gil + Treasure combined total
- Total Submarines (ready/total)
- Total Retainers (ready/total)
- Total Marketboard items
- Monthly/Annual income estimates
- Monthly costs (supplies)
- Monthly profit calculations

#### Per-Character Information
- Character name, world, and FC
- Character gil + Retainer gil
- Treasure value (salvaged rings, bracelets, etc.)
- Ceruleum tanks and Repair kits inventory
- Daily income and cost estimates
- Ready status highlighting (red background when items ready)

#### Submarine Details
- Submarine name and level
- Build configuration (e.g., SSUC, WSUC)
- Return status (Ready! or time remaining)

#### Retainer Details
- Retainer name and level
- Gil held by retainer
- Marketboard items count
- Venture status

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install flask
   ```

## Configuration

### Option 1: Edit Script Directly

Modify the configuration section at the top of `Landing Page.py`:

```python
HOST = "127.0.0.1"      # Server address
PORT = 1234             # Server port
AUTO_REFRESH = 60       # Auto-refresh interval (0 to disable)

account_locations = [
    acc("Main", f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs"),
    # Add more accounts as needed
]
```

### Option 2: External Config File (recommended)

1. Copy `config.json.example` to `config.json`
2. Edit the settings as needed:

```json
{
    "HOST": "127.0.0.1",
    "PORT": 1234,
    "DEBUG": false,
    "AUTO_REFRESH": 60,
    "account_locations": [
        {
            "enabled": true,
            "nickname": "Main",
            "pluginconfigs_path": "C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs"
        },
        {
            "enabled": false,
            "nickname": "Alt1",
            "pluginconfigs_path": "C:\\Users\\{user}\\AltData\\Alt1\\pluginConfigs"
        }
    ]
}
```

**Note**: Use `{user}` as a placeholder for the current username - it will be replaced automatically.

## Usage

### Start the Server

```bash
python "Landing Page.py"
```

### Access the Dashboard

Open your browser and navigate to:
```
http://127.0.0.1:1234
```

### API Endpoints

- `GET /` - Main dashboard page
- `GET /api/data` - Raw JSON data for all accounts
- `GET /api/refresh` - Force data refresh and return status

## Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `HOST` | `127.0.0.1` | Server host address. Use `0.0.0.0` for network access |
| `PORT` | `1234` | Server port number |
| `DEBUG` | `false` | Flask debug mode |
| `AUTO_REFRESH` | `60` | Auto-refresh interval in seconds (0 to disable) |

## Income/Cost Calculations

The dashboard calculates income and costs based on submarine builds:

### Gil Rates (per day)
- **SSUC/WSUC**: 140,000 gil
- **S+S+U+C+/W+S+U+C+**: 180,000 gil
- **YUUW**: 120,000 gil
- And more...

### Supply Costs
- **Ceruleum Tank**: 350 gil each
- **Repair Kit**: 2,000 gil each

Consumption rates vary by submarine build and route.

## Network Access

To access the dashboard from other devices on your network:

1. Set `HOST` to `0.0.0.0`
2. Ensure your firewall allows connections on the configured port
3. Access via `http://<your-ip>:1234`

## Troubleshooting

### "Config not found" Error
- Verify the `pluginconfigs_path` points to your XIVLauncher pluginConfigs directory
- Ensure AutoRetainer plugin has been run at least once to create the config file

### No Submarine Data
- Make sure you have submarines registered in AutoRetainer
- Check that the character has workshop access

### Page Not Loading
- Verify Flask is installed: `pip install flask`
- Check that the port is not in use by another application

## File Structure

```
FFXIV - Landing Page/
├── Landing Page.py         # Main application
├── config.json.example     # Configuration template
└── README.md               # This file
```

## License

Created by: https://github.com/xa-io

## Version History

### v1.02 (2026-01-25)

- Changed account header bars from red gradient to lighter blue for better theme cohesion
- Character cards with ready items display light red background for visibility
- Account header stats turn red when retainers/subs are ready
- Stats stay white when nothing is ready

### v1.01 (2026-01-25)

- Fixed stale submarine display bug
- Submarines now validated against OfflineSubmarineData (source of truth)
- Stale/deleted submarines no longer appear in dashboard

### v1.00 (2026-01-25)

- Initial release with comprehensive dashboard features
- Flask-based web server with configurable host/port
- AutoRetainer and Altoholic data parsing
- Character, submarine, and retainer tracking
- Income and cost calculations
- Modern dark-themed responsive UI
