# FFXIV AutoRetainer Dashboard v1.05

A self-hosted web dashboard that displays FFXIV character data from AutoRetainer's DefaultConfig.json and Altoholic's altoholic.db. Provides a modern, dark-themed UI accessible via browser showing characters, submarines, retainers, marketboard items, gil totals, income/cost calculations, and comprehensive supply tracking.

<img width="773" height="453" alt="image" src="https://github.com/user-attachments/assets/ab887aeb-2797-4d71-b786-a97c0fdb930f" />

## Features

- **Self-Hosted Web Server**: Flask-based server with configurable host/port (default: `127.0.0.1:1234`)
- **Real-Time Data**: Parses AutoRetainer DefaultConfig.json on each page load
- **Altoholic Integration**: Reads treasure values, venture coins, coffers, dyes, and job levels from Altoholic's altoholic.db
- **Submarine Plan Detection**: Automatically detects leveling vs farming submarines based on AutoRetainer plan names
- **Configurable Plan Earnings**: Set custom average earnings per submarine plan route
- **Supply Tracking**: Displays ceruleum tanks, repair kits, and days until restocking needed
- **Multi-Account Support**: Configure multiple accounts via config.json
- **Anonymize**: Hides personal data for screenshots (names, worlds, FCs, retainers, subs)
- **Expand All / Collapse All**: Expand or collapse all character cards
- **Auto-Refresh**: Configurable auto-refresh interval (default: 60 seconds)
- **Modern UI**: Dark-themed responsive design with collapsible sections
- **Ready Status Indicators**: Visual highlighting when retainers/submarines are ready

### Data Displayed

#### Summary Cards

- Total Gil across all accounts
- Treasure Value (from Altoholic)
- Coffer + Dyes estimated value
- Gil + Treasure combined total
- Total Submarines (ready/total) with Leveling/Farming breakdown
- Total Retainers (ready/total) with Leveling/Farming breakdown
- Total Marketboard items
- Monthly/Annual income estimates
- Monthly costs (supplies)
- Monthly profit calculations

#### Per-Character Information

- Character name, world, and FC
- Current class and level (from Altoholic)
- Character gil + Retainer gil
- Treasure value (salvaged rings, bracelets, etc.)
- Coffer + Dye estimated value
- FC Points, Venture Coins, and Coffer count
- Ceruleum tanks and Repair kits inventory (for characters with submarines)
- Days until restocking needed (color-coded: red <7 days, yellow <14 days)
- Daily income and cost estimates
- Ready status highlighting (red background when items ready)

#### Submarine Details

- Submarine name and level
- Build configuration (e.g., SSUC, WSUC)
- Plan name (from AutoRetainer configuration)
- Leveling/Farming status (detected from plan or VesselBehavior)
- Return status (Ready! or time remaining)

#### Retainer Details

- Retainer name and level
- Gil held by retainer
- Marketboard items count
- Venture status
- Leveling/Farming status (Level <100 = Leveling, Level 100 = Farming)

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
    ],

    "submarine_plans": {
        "leveling": [
            "Level Up Default",
            "Unlock All Sectors",
            "XP Grind"
        ],
        "farming": {
            "OJ": 118661,
            "Yummy OJ": 118661,
            "Overseer OJ": 118661,
            "JORZ": 140404,
            "MROJZ": 116206,
            "Custom Route 1": 80000
        }
    },

    "item_values": {
        "venture_coffer": 18000,
        "pure_white_dye": 450000,
        "jet_black_dye": 600000,
        "pastel_pink_dye": 40000
    }
}
```

**Note**: Use `{user}` as a placeholder for the current username - it will be replaced automatically.

### Submarine Plans Configuration

The `submarine_plans` section allows you to configure which AutoRetainer plan names indicate leveling vs farming:

- **leveling**: Array of plan names that indicate submarines are leveling (no income counted)
- **farming**: Object mapping plan names to their average daily gil earnings

Plan names must match exactly as they appear in AutoRetainer's SubmarinePointPlans or SubmarineUnlockPlans.

### Item Values Configuration

The `item_values` section lets you override default market values for estimation:

| Item | Default Value | Description |
| ---- | ------------- | ----------- |
| `venture_coffer` | 18,000 | Venture Coffer market value |
| `pure_white_dye` | 450,000 | Pure White Dye market value |
| `jet_black_dye` | 600,000 | Jet Black Dye market value |
| `pastel_pink_dye` | 40,000 | Pastel Pink Dye market value |

## Usage

### Start the Server

```bash
python "Landing Page.py"
```

### Access the Dashboard

Open your browser and navigate to:

```text
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

### v1.05 (2026-01-26)

- **Anonymize Mode**: Hide personal data for screenshots - replaces character names, worlds, FC names, retainer names, and submarine names with generic placeholders
- **Expand/Collapse All**: Quick buttons to expand or collapse all character cards within an account

### v1.04 (2026-01-26)

- **Character Filtering**: Hide characters without submarines or retainers using toggle buttons in the sort bar

### v1.03 (2026-01-26)

- **Character Sorting**: Sort characters within each account by Level, Gil, Treasure, FC Points, Ventures, Coffers, Dyes, Tanks, Kits, Restock Days, Retainers, or Subs
- **Submarine Plan Detection**: Automatically detects leveling vs farming based on AutoRetainer plan names
- **Configurable Plan Earnings**: Set custom average gil/day per submarine route in config.json
- **Enhanced Altoholic Integration**: Now reads venture coins from Currencies, coffers, dyes, and job levels from Inventory, Saddle, ArmoryInventory, and Retainers
- **FC Points Display**: Shows FC points in character header and details with total in summary
- **Venture Coins Display**: Shows venture coin count from Altoholic Currencies
- **Coffer + Dye Tracking**: Counts coffers and dyes separately with total value estimate and configurable prices
- **Treasure Value Display**: Shows treasure value in character header with sort option
- **Character Class/Level**: Shows current highest-level class from Altoholic
- **Supply Tracking**: Displays ceruleum tanks, repair kits, and days until restocking in header
- **Days Until Restock**: Calculates based on submarine consumption rates (color-coded warnings) with lowest across all accounts shown in summary
- **Leveling/Farming Stats**: Summary cards show breakdown of leveling vs farming submarines and retainers
- **Retainer Status**: Retainers under level 100 shown as leveling, level 100 shown as farming

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
