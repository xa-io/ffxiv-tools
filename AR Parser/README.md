# FFXIV AR Parser

A comprehensive Python tool for parsing and analyzing Final Fantasy XIV character data from AutoRetainer and Altoholic plugins, generating detailed Excel reports with gil tracking, retainer management, submarine operations, and inventory analysis.

## Overview

The FFXIV AR Parser extracts data from XIVLauncher plugin configurations (AutoRetainer and Altoholic) across multiple FFXIV accounts and consolidates everything into a single, sortable Excel workbook. Perfect for players managing multiple characters and retainers who want to track their wealth, optimize retainer ventures, monitor submarine operations, and analyze inventory across their entire account network.

## Features

### Core Functionality
- **Multi-Account Support**: Parse data from unlimited FFXIV accounts/alt data folders
- **AutoRetainer Integration**: Extracts character data from DefaultConfig.json files
- **Altoholic Integration**: Reads inventory and saddlebag data from altoholic.db SQLite databases
- **Excel Report Generation**: Creates comprehensive, formatted Excel workbooks with multiple sheets

### Character Tracking
- **Gil Management**: Character gil + retainer gil = total gil per character
- **World & Region Detection**: Automatic region assignment (NA/EU/OCE/JP) based on world
- **FC Information**: Free Company names and FC points tracking
- **Submarine Operations**: Level and part configuration for up to 4 submarines per character

### Retainer Management
- **Retainer Details**: Name, level, gil amounts
- **Market Board Tracking**: Number of active market board items per retainer
- **Venture Status**: Active venture detection for each retainer
- **Multi-Retainer Display**: Clean formatting with character information grouped by retainers

### Inventory Analysis (Altoholic)
- **Submarine Parts Inventory**: Tracks tanks (Item ID: 10155) and kits (Item ID: 10373) across all inventories and saddlebags
- **Treasure Tracking**: Monitors salvaged rings, bracelets, earrings, and necklaces with gil value calculations
- **Total Treasure Value**: Calculates total gil value of all treasure items across all characters

### Submarine Operations
- **Level Tracking**: Monitors submarine levels (1-130) for all 4 submarine slots
- **Part Configuration**: Displays submarine builds using shorthand notation (e.g., WSUC, SSUC)
- **Supported Classes**: Shark (S), Unkiu (U), Whale (W), Coelacanth (C), Syldra (Y), Modified (+)
- **Gil Farming Calculations**: Automatic daily/monthly/annual gil farming estimates for known builds

### Summary Statistics
- Total characters and retainers
- Total gil across all characters
- Average gil per character
- Total tanks, kits, and treasure values
- Total gil value (gil + treasure)
- Richest character identification
- FC statistics (total FCs, FCs with submarines, total FC points)
- Submarine level ranges (lowest/highest)
- Submarine build frequency analysis
- Gil farming projections (daily/monthly/annual)
- Report generation timestamp

## Installation

### Requirements
- Python 3.12.4 or higher
- Required packages:
  ```
  xlsxwriter
  ```

### Setup
1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install xlsxwriter
   ```

3. Configure account locations in the script:
   ```python
   account_locations = [
       acc("Main",   f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs"),
       acc("Alt1",   f"C:\\Users\\{user}\\AltData\\account1\\pluginConfigs"),
       # Add more accounts as needed
   ]
   ```

## Usage

### Basic Usage
Run the script to generate a timestamped Excel report:
```bash
python json_to_excel.py
```

This creates a file named `YYYY-MM-DD-HH-MM - ffxiv_gil_summary.xlsx` in the script directory.

### Command-Line Options
```bash
# Generate report without timestamp in filename
python json_to_excel.py --no-timestamp

# Custom output filename
python json_to_excel.py --output my_report.xlsx

# Disable Altoholic integration globally
python json_to_excel.py --no-altoholic
```

### Account Configuration

Each account can be configured individually with Altoholic integration enabled or disabled:

```python
# Enable Altoholic for this account (default)
acc("Main", f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs", include_altoholic=True)

# Disable Altoholic for this account (faster processing)
acc("Alt1", f"C:\\Users\\{user}\\AltData\\account1\\pluginConfigs", include_altoholic=False)
```

Set the global default behavior:
```python
INCLUDE_ALTOHOLIC_BY_DEFAULT = True  # Enable by default
INCLUDE_ALTOHOLIC_BY_DEFAULT = False # Disable by default
```

## Excel Report Structure

### Main Sheet: "FFXIV Gil Summary"
Sorted by total gil (highest to lowest), includes:
- **CID**: Character ID
- **Account Nickname**: Your configured account label
- **Character Name**: In-game character name
- **World**: Home world server
- **Region**: NA, EU, OCE, or JP
- **Character Gil**: Gil on character
- **Retainer Name**: Each retainer on separate row
- **MBItems**: Market board item count
- **HasVenture**: Venture active status (1/0)
- **Level**: Retainer level
- **Retainer Gil**: Gil on retainer
- **Total Gil**: Character + all retainer gil
- **FC Name**: Free Company name
- **FC Points**: FC points amount
- **Submarine Data**: Levels and parts for 4 submarines
- **Overseer Name Formatting**: Ready-to-use format for Overseer plugin
- **SND Name Formatting**: Ready-to-use format for SND plugin
- **Tanks**: Total tanks in inventory/saddlebag
- **Kits**: Total kits in inventory/saddlebag
- **Treasure Value**: Total gil value of treasure items

### Summary Sheet: "Summary"
Quick statistics including:
- Total characters, retainers, gil
- Average gil per character
- Total tanks, kits, treasure values
- Total gil value (gil + treasure)
- Richest character details
- FC statistics
- Submarine level ranges
- Unique submarine builds with usage counts
- Gil farming projections for known builds
- Report generation timestamp

## Submarine Part Codes

The script uses shorthand notation for submarine parts:

### Standard Classes
- **S**: Shark-class
- **U**: Unkiu-class
- **W**: Whale-class
- **C**: Coelacanth-class
- **Y**: Syldra-class

### Modified Classes
- **S+**: Modified Shark-class
- **U+**: Modified Unkiu-class
- **W+**: Modified Whale-class
- **C+**: Modified Coelacanth-class
- **Y+**: Modified Syldra-class

### Build Format
Submarine builds are displayed as 4-character codes representing: Bow, Bridge, Pressure Hull, Stern

**Example**: `WSUC` = Whale Bow + Shark Bridge + Unkiu Hull + Coelacanth Stern

## Treasure Items Tracked

The script monitors these salvaged treasure items with their gil values:

| Item ID | Item Name | Gil Value |
|---------|-----------|-----------|
| 22500 | Salvaged Ring | 8,000 |
| 22501 | Salvaged Bracelet | 9,000 |
| 22502 | Salvaged Earring | 10,000 |
| 22503 | Salvaged Necklace | 13,000 |
| 22504 | Extravagant Salvaged Ring | 27,000 |
| 22505 | Extravagant Salvaged Bracelet | 28,500 |
| 22506 | Extravagant Salvaged Earring | 30,000 |
| 22507 | Extravagant Salvaged Necklace | 34,500 |

## Configuration

### Item IDs
```python
TANK_ITEM_ID = 10155   # Submarine ceruleum tanks
KITS_ITEM_ID = 10373   # Submarine repair kits
```

### Treasure Values
Modify `TREASURE_VALUES` dictionary to add/update treasure items:
```python
TREASURE_VALUES = {
    22500: 8000,   # Item ID: Gil Value
    # Add more items as needed
}
```

### Region Detection
World assignments are automatically detected. To add new worlds:
```python
NA_WORLDS = {
    "world1", "world2", # Add new NA worlds here
}
# Similar for EU_WORLDS, OCE_WORLDS, JP_WORLDS
```

## Technical Details

### Data Sources
- **AutoRetainer**: `{pluginConfigs}/AutoRetainer/DefaultConfig.json`
  - Character information (name, world, CID, gil)
  - Retainer details (name, gil, level, ventures, market board items)
  - FC information (name, points, holder character)
  - Submarine data (levels, part configurations)

- **Altoholic**: `{pluginConfigs}/Altoholic/altoholic.db`
  - SQLite database with character inventory data
  - Inventory items with ItemId and Quantity
  - Saddlebag items (additional storage)
  - Character IDs for data matching

### Processing Flow
1. Load account configurations with Altoholic preferences
2. Scan Altoholic databases (if enabled) for inventory data
3. Parse AutoRetainer JSON files for character/retainer data
4. Extract FC information from nested JSON structures
5. Match Altoholic inventory data to characters by CID
6. Calculate totals and derive regions from worlds
7. Build character summaries with all data combined
8. Sort by total gil (descending)
9. Generate formatted Excel workbook with two sheets
10. Apply column widths, number formats, and filters

### Excel Formatting
- **Header Row**: Bold, gray background, borders, frozen pane
- **Money Columns**: Comma-separated thousands format
- **Total Gil**: Bold, blue background highlight
- **Character Rows**: Light gray background for character name column
- **Auto-filter**: Enabled on all columns
- **Column Widths**: Optimized for content visibility
- **Date/Time**: Formatted as `yyyy-mm-dd hh:mm:ss`

## Use Cases

### Multi-Character Management
- Track wealth across dozens of characters and retainers
- Identify which characters need gil transfers
- Monitor total account wealth growth over time

### Retainer Optimization
- Quickly see which retainers are idle (HasVenture = 0)
- Track market board item distribution across retainers
- Identify low-level retainers that need leveling

### Submarine Operations
- Monitor submarine progression (levels 1-130)
- Track submarine build configurations across FCs
- Calculate gil farming potential from optimal builds
- Identify which characters have incomplete submarine fleets

### Inventory Management
- Track submarine tanks and kits across all characters
- Monitor treasure item stockpiles and their gil value
- Calculate total inventory value for wealth assessment
- Identify characters with excess materials for distribution

### FC Management
- Track FC points across multiple Free Companies
- Identify which FCs have active submarine operations
- Monitor wealth generation from FC activities

## Troubleshooting

### Missing AutoRetainer Data
**Issue**: Script reports "AutoRetainer file not found"

**Solution**: Verify the path to `DefaultConfig.json` is correct for each account:
```python
auto_path = os.path.join(pluginconfigs_path, "AutoRetainer", "DefaultConfig.json")
```

### Missing Altoholic Data
**Issue**: Tanks/kits/treasure columns show zeros

**Solution**: 
- Verify Altoholic plugin is installed and has scanned characters
- Check altoholic.db file exists at configured path
- Ensure `include_altoholic=True` for the account
- Set `INCLUDE_ALTOHOLIC_BY_DEFAULT = True` if needed

### Characters Missing from Report
**Issue**: Some characters don't appear in the report

**Solution**:
- Ensure AutoRetainer has been opened in-game for those characters
- Check that the character data exists in DefaultConfig.json
- Verify the account location is configured correctly
- Characters must have CID (Character ID) in the JSON data

### Excel File Won't Open
**Issue**: Generated Excel file is corrupted or won't open

**Solution**:
- Ensure xlsxwriter is installed: `pip install xlsxwriter`
- Check disk space is available
- Verify write permissions in the output directory
- Try running with `--no-timestamp` flag

### Wrong Region Detected
**Issue**: Character shows wrong region or blank region

**Solution**: Add the world to the appropriate region set:
```python
NA_WORLDS = {
    "your_world_here",  # Add missing NA world
    # ... existing worlds
}
```

### Submarine Parts Show "?"
**Issue**: Submarine part codes display as "?" instead of class letter

**Solution**: The part ID is not recognized. Add it to `SUB_PARTS_LOOKUP`:
```python
SUB_PARTS_LOOKUP = {
    12345: "YourPart-class Bow",  # Add new part ID
    # ... existing parts
}
```

## Performance Considerations

- **Large Account Networks**: Processing 50+ characters with Altoholic enabled may take 30-60 seconds
- **Altoholic Overhead**: SQLite database scans add ~0.5-1 second per account
- **Excel Generation**: Writing the workbook typically takes <1 second
- **Optimization**: Disable Altoholic for accounts that don't need inventory tracking

## File Structure

```
FFXIV - AR Parser/
├── json_to_excel.py    # Main script
├── README.md                      # This file
└── YYYY-MM-DD-HH-MM - ffxiv_gil_summary.xlsx  # Generated reports
```

## Requirements

### Required Plugins
- **AutoRetainer** (XIVLauncher/Dalamud plugin)
- **Altoholic** (XIVLauncher/Dalamud plugin) - Optional but recommended

### Python Packages
- **xlsxwriter**: Excel file generation

### System Requirements
- Windows (due to default XIVLauncher paths)
- Python 3.12.4+
- Read access to XIVLauncher pluginConfigs directories

## Future Enhancements

Potential features for future versions:
- Additional inventory item tracking
- Historical gil tracking over time
- Retainer venture completion time tracking
- Airship data integration
- Cross-world price comparisons for treasure items
- Gil transfer recommendations
- Retainer leveling priority suggestions
- Submarine route optimization data

## Contributing

This tool is part of the [xa-io/ffxiv-tools](https://github.com/xa-io/ffxiv-tools) repository.

For bug reports, feature requests, or contributions:
1. Open an issue describing the problem or feature
2. Include error messages and Python version
3. Provide sample data structure (with sensitive info removed)
4. Submit pull requests for improvements

## License

This tool is provided as-is for personal use. Not affiliated with Square Enix or Final Fantasy XIV.

## Disclaimer

This tool reads data from local plugin configuration files and does not interact with the FFXIV game client or servers.

---

**Last Updated**: 2025-10-07
**Created by**: https://github.com/xa-io
**Repository**: https://github.com/xa-io/ffxiv-tools/tree/main/AR%20Parser
