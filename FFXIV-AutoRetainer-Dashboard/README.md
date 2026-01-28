# FFXIV AutoRetainer Dashboard v1.15

A self-hosted web dashboard that displays FFXIV character data from AutoRetainer, Altoholic, and Lifestream configs. Provides a modern, dark-themed UI accessible via browser showing characters, submarines, retainers, housing locations, marketboard items, gil totals, inventory tracking, MSQ progression, job levels, currencies, income/cost calculations, and comprehensive supply tracking.


<p align="center">
  <img src="https://github.com/user-attachments/assets/cacd796e-2a01-45ab-938b-06ba9621446c" alt="3MnKqYLQaN">
</p>

<p align="center">
  <img width="1481" height="2238" alt="image" src="https://github.com/user-attachments/assets/4b4efbbd-99c6-4a06-ad08-fe1ee5c6235a" />
</p>


## Features

- **Self-Hosted Web Server**: Flask-based server with configurable host/port (default: `127.0.0.1:1234`)
- **Real-Time Data**: Parses AutoRetainer, Altoholic, and Lifestream configs on each page load
- **Altoholic Integration**: Reads treasure values, venture coins, coffers, dyes, and job levels from Altoholic's altoholic.db
- **Lifestream Integration**: Reads housing data (Personal House and FC House locations)
- **Submarine Plan Detection**: Automatically detects leveling vs farming submarines based on AutoRetainer plan names
- **Configurable Plan Earnings**: Set custom average earnings per submarine plan route
- **Supply Tracking**: Displays ceruleum tanks, repair kits, and days until restocking needed
- **Inventory Tracking**: Shows inventory space used per character with color-coded warnings
- **Multi-Account Support**: Configure multiple accounts via config.json
- **MSQ Progression Tracking**: Shows MSQ completion percentage with color coding (green ≥90%, yellow ≥50%, gray <50%)
- **Job Level Display**: Collapsible DoW/DoM and DoH/DoL sections showing all job levels
- **Currency Tracking**: Categorized currency display (Crystals, Common, Tomestones, Battle, Societies)
- **Player Name Copy**: Easy copy/paste of Name@World format
- **Sorting**: Sort characters by level, gil, treasure, FC points, ventures, inventory, MSQ%, retainer/submarine levels
- **Filtering**: Filter characters by retainers, submarines, personal house, or FC house
- **Hide Money Stats**: Privatize earnings for screenshots (replaces financial data with *****)
- **Anonymize**: Hides personal data for screenshots (names, worlds, FCs, housing addresses show TOP SECRET)
- **Expand All / Collapse All**: Expand or collapse all character cards
- **Character Search**: Search bar to filter characters by name across all accounts
- **Loading Overlay**: Animated progress bar during page load for large character counts
- **Color Themes**: 10 theme presets (Default, Ultra Dark, Dark Gray, Ocean Blue, Forest Green, Crimson Red, Purple Haze, Pastel Pink, Dark Orange, Brown)
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
- MSQ progress percentage with quest count and current quest name
- Player Name@World (for easy copy/paste)
- Personal House and FC House locations (from Lifestream)
- Character gil + Retainer gil
- Treasure value (salvaged rings, bracelets, etc.)
- Coffer + Dye estimated value
- FC Points, Venture Coins, and Coffer count
- Inventory space used (color-coded: red >= 130, yellow >= 100)
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

#### Job Levels (DoW/DoM & DoH/DoL)

- Collapsible sections showing all job levels
- Combat jobs: Tank, Healer, Melee DPS, Physical Ranged DPS, Magical Ranged DPS
- Crafters: All 8 Disciples of the Hand
- Gatherers: All 3 Disciples of the Land
- Base class levels mapped to final jobs (e.g., Gladiator → Paladin)

#### Currencies

- Categorized display with compact layout
- **Crystals**: Grid showing Shards, Crystals, Clusters for all 6 elements
- **Common**: Gil, Ventures, MGP, Bicolor Gemstones
- **Tomestones**: Poetics, Aesthetics, Heliometry
- **Battle**: Wolf Marks, Trophy Crystals, Allied Seals
- **Societies**: Tribal currencies, Skybuilders' Scrips
- Shortened verbose names for readability

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
    "MINIMUM_MSQ_QUESTS": 5,
    "SHOW_CLASSES": true,
    "SHOW_CURRENCIES": true,
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
| `MINIMUM_MSQ_QUESTS` | `5` | Min MSQ quests completed to show MSQ progress (0 = always show) |
| `SHOW_CLASSES` | `true` | Show DoW/DoM and DoH/DoL job sections |
| `SHOW_CURRENCIES` | `true` | Show Currencies section |
| `DEFAULT_THEME` | `default` | Color theme (see Available Themes below) |

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

### v1.15 (2026-01-27)

- **Color Theme System**: Added 10 color theme presets with theme selector buttons under search bar
- **Theme Presets**: Default (Blue), Ultra Dark, Dark Gray, Ocean Blue, Forest Green, Crimson Red, Purple Haze, Pastel Pink, Dark Orange, Brown
- **DEFAULT_THEME Config**: New configuration option to set default theme in script and config.json

#### Available Themes

| Theme | Description |
|-------|-------------|
| `default` | Blue accent (original) |
| `ultra-dark` | Near-black with subtle gray |
| `dark-gray` | Neutral grays |
| `ocean-blue` | Deep blues with cyan accent |
| `forest-green` | Dark greens |
| `crimson-red` | Dark reds |
| `purple-haze` | Dark purples |
| `pastel-pink` | Soft pink with hot pink accent |
| `dark-orange` | Warm orange/amber tones |
| `brown` | Earthy brown/sienna tones |

### v1.14 (2026-01-27)

- **Character Search Bar**: Added search input in header to filter characters by name across all accounts
- **Loading Overlay**: Full-screen loading overlay with animated progress bar for large character counts (1000+)
- **Loading Hint**: Header subtitle shows "Please wait for page to load, may take longer if importing hundreds of characters"
- **Anchor Favicon**: Added ⚓ emoji favicon for browser tab
- **Search Error Message**: Shows "No results match your search..." when no characters match
- **Auto-Expand on Search**: Accounts with matching characters automatically expand during search
- **Search Clear**: Clearing search restores original collapse states

### v1.13 (2026-01-27)

- **Current Class Fix**: Fixed to show last played job using LastJob/LastJobLevel from Altoholic
- **Lowest/Highest Class**: Added fields that only show when level differs from Current
- **Classes Sort Button**: Added "Classes" sort button (after Level, before Gil) - requires SHOW_CLASSES=true
- **Individual Dye Counts**: Shows Pure White, Jet Black, Pastel Pink counts after total dyes

### v1.12 (2026-01-27)

- **Hide Money Stats Button**: New 💰 button to privatize financial information for screenshots
- **Comprehensive Hiding**: Replaces values with ***** for:
  - **Summary Cards**: Total gil, FC points, treasure value, gil+treasure, coffers+dyes, subs, retainers, MB items, monthly income/cost/profit, annual income
  - **Account Tabs**: Total gil, treasure, subs, retainers, MB items
  - **Character Cards**: Gil, treasure value, FC points, venture coins, coffers, dyes, tanks, kits, restock days
  - **Expanded Details**: Character gil, retainer gil, coffer+dye value, FC points, venture coins, coffers, tanks, kits, daily income/cost
  - **Retainer Table**: Level and gil columns
  - **Submarine Table**: Level, build, and status columns
- **Currencies Unaffected**: Currencies dropdown displays normally (crystals, tomestones, etc.)
- **Toggle Behavior**: Button changes from 💰 to 💸 when active, click again to restore values

### v1.11 (2026-01-26)

- **Improved Currencies Display**: Categorized currencies (Crystals, Common, Tomestones, Battle, Societies, Other)
- **Shortened Currency Names**: Verbose names shortened for readability (e.g., "Allagan_Tomestone_Of_Poetics" → "Poetics")
- **Compact Flexbox Layout**: Currency display prevents overflow and saves space
- **Configurable Display Options**: New config parameters for controlling UI sections:
  - `MINIMUM_MSQ_QUESTS`: Control threshold for showing MSQ progress (default: 5)
  - `SHOW_CLASSES`: Toggle DoW/DoM and DoH/DoL sections (default: true)
  - `SHOW_CURRENCIES`: Toggle Currencies section (default: true)

### v1.10 (2026-01-26)

- **MSQ Progression Tracking**: Shows MSQ completion percentage after Lv/Class in character header
- **Color-Coded Progress**: Green (≥90%), Yellow (≥50%), Gray (<50%)
- **Quest Details**: Tooltip shows completed/total quest count and current quest name
- **Comprehensive Quest Data**: 1,041 trackable MSQ quests from ARR through Patch 7.4
- **Altoholic Integration**: Extracts completed quests from Altoholic database

### v1.09 (2026-01-26)

- **Player Name@World**: Added copyable Name@World row in expanded character section
- **DoW/DoM Section**: Collapsible section showing all combat job levels (Tank, Healer, Melee/Ranged/Magic DPS)
- **DoH/DoL Section**: Collapsible section showing all crafter and gatherer levels
- **Currencies Section**: Collapsible section showing all currencies the character has
- **Job Level Mapping**: Base class levels mapped to final jobs (e.g., Gladiator → Paladin)
- **Anonymize Enhancement**: Player name field shows "Toon X@Eorzea" when anonymized

### v1.08 (2026-01-26)

- **Housing Filter Buttons**: Added Personal House and FC House filter buttons to show only characters with houses
- **Level Sort Buttons**: Added Retainer Lv and Submarine Lv sort buttons for sorting by max retainer/submarine level
- **Compact Sort Buttons**: Renamed sort buttons to emojis for more compact display
- **Anonymization Improvements**: Housing addresses now show "TOP SECRET" in red when anonymized, housing icons preserved in character header

### v1.07 (2026-01-26)

- **Housing Information**: Added housing data from Lifestream DefaultConfig.json
- **Personal House Display**: Shows Personal House icon and location after character level/class
- **FC House Display**: Shows FC House icon and location for characters with FC housing
- **Housing Format**: Displays as "Mist W1 P15" for Ward 1, Plot 15 in Mist district

### v1.06 (2026-01-26)

- **Inventory Space Tracking**: Displays 🎒 X/140 in character summary card after FC name
- **Inventory Breakdown**: Added Inventory row in character expanded details with color coding (red >= 130, yellow >= 100)
- **Inventory Sorting**: Added "Inventory ▼" sort button to sort characters by inventory slots used

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
