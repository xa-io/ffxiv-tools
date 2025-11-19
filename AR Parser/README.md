# FFXIV AR Parser with Altoholic

Excel report generator for FFXIV AutoRetainer data with integrated Altoholic inventory scanning.

## Features

- **Character Gil Tracking**: Aggregates gil across all characters and retainers
- **Altoholic Integration**: Scans Tanks, Kits, and Treasure items from Altoholic inventory
- **Lifestream Housing Integration**: Tracks both private and FC housing locations
  - Displays Ward, Plot, and District for each character
  - Separate columns for private house and FC house
  - District abbreviations: M (Mist), G (Goblet), LB (Lavender Beds), E (Empyreum), S (Shirogane)
- **Submarine Management**: Tracks submarine builds, levels, and return times across all accounts
  - Displays submarine part configurations (WSUC, SSUC, YUUW, etc.)
  - Shows hours remaining until submarine returns from voyages
  - Supports 10+ different submarine build configurations
- **Submarine Gil Farming Analysis**: Calculates daily/monthly/annual gil earnings based on submarine builds
  - OJ Route (24h): 118,661 gil/day
  - JORZ Route (36h): 140,404 gil/day (highest)
  - MROJ Route (36h): 120,728 gil/day
  - MOJ, ROJ, JOZ, MOJZ, MROJZ routes with specific rates
- **FC Data**: Displays FC names, FC points, and total FC statistics
- **Region Detection**: Automatically determines region (NA/EU/OCE/JP) based on world
- **Excel Export**: Generates formatted Excel reports with comprehensive summary statistics
- **Per-Account Control**: Individual control over Altoholic and submarine inclusion

## Configuration

### Account Setup

Each account is configured using the `acc()` function with the following parameters:

```python
acc(nickname, pluginconfigs_path, include_altoholic=True, include_submarines=True)
```

**Parameters:**
- `nickname`: Display name for the account in reports
- `pluginconfigs_path`: Path to the XIVLauncher pluginConfigs folder
- `include_altoholic`: Whether to scan Altoholic inventory data (default: True)
- `include_submarines`: Whether to include submarine builds/levels in output and calculations (default: True)

### Example Configuration

```python
account_locations = [
     acc("Main",   f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs", include_submarines=True),  # Include submarines
   # acc("Acc1",   f"C:\\Users\\{user}\\AltData\\Acc1\\pluginConfigs", include_submarines=True),   # Include submarines
   # acc("Acc2",   f"C:\\Users\\{user}\\AltData\\Acc2\\pluginConfigs", include_submarines=False),  # No submarines
   # acc("Acc3",   f"C:\\Users\\{user}\\AltData\\Acc3\\pluginConfigs", include_submarines=False),  # No submarines
]
```

### Submarine Inclusion Control

When `include_submarines=False` for an account:
- Submarine levels will display as 0
- Submarine build codes will be empty
- That account's submarines will NOT be included in:
  - Summary monthly gil calculations (Gil Farmed Daily/Monthly/Annually)
  - Submarine build statistics
  - Highest/lowest submarine level calculations

## Usage

### Basic Usage
```bash
python "AR Parser with Altoholic.py"
```

### Disable Altoholic Scanning
```bash
python "AR Parser with Altoholic.py" --no-altoholic
```

## Output

The script generates an Excel file with the following sheets:

### Main Sheet: FFXIV Gil Summary
- Character details (name, world, region, CID)
- Housing information (separate private and FC housing)
  - Private Ward, Private Plot, Private Zone
  - FC Ward, FC Plot, FC Zone
- Gil totals (character + retainers)
- Retainer information (name, level, ventures, market board items)
- FC information (name, points)
- Submarine builds, levels, and return times (if enabled for account)
  - Level for each submarine (#1-#4)
  - Build configuration (e.g., WSUC, SSUC, YUUW)
  - Hours until return from voyage (can be negative if already returned)
- Altoholic inventory (Tanks, Kits, Treasure value)
- Character resource tracking
  - Inventory Spaces remaining
  - Ventures count
  - VentureCoffers count
- Formatting options for various tools (Plain Name, List, SND, Bagman)

### Summary Sheet
- Total characters and retainers
- Total gil across all accounts
- Average gil per character
- **Richest character** (name and gil amount)
- Total Tanks, Kits, and Treasure value
- **Total Gil Value** (total gil + treasure value combined)
- **FC statistics**
  - Total FC's (count of characters with submarines, identified by FC name or FC housing data)
  - Total FC's Farming Subs (characters with at least one farming submarine build)
  - Total FC Points
- **Submarine statistics**
  - Lowest/Highest submarine level
  - Unique submersible parts count
  - Detailed submarine build list with usage counts
  - **Gil farming rates per build** (shows which builds earn what amount per day)
  - **Total Submarines** (count of all submarine builds including farming and leveling)
- **Gil farming calculations** (only includes accounts with `include_submarines=True`)
  - Gil Farmed Each Day (based on all submarine builds and their routes)
  - Gil Farmed Every 30 Days  
  - Gil Farmed Annually
- Report generation timestamp

## Submarine Build Codes

The script uses shorthand codes for submarine parts in the reports:

- **S** = Shark-class
- **U** = Unkiu-class
- **W** = Whale-class
- **C** = Coelacanth-class
- **Y** = Syldra-class
- **S+** = Modified Shark-class
- **U+** = Modified Unkiu-class
- **W+** = Modified Whale-class
- **C+** = Modified Coelacanth-class
- **Y+** = Modified Syldra-class

Each build code represents the 4 parts (Bow, Bridge, Pressure Hull, Stern) in order. For example:
- **WSUC** = Whale Bow + Shark Bridge + Unkiu Hull + Coelacanth Stern
- **S+S+U+C+** = Modified Shark Bow + Modified Shark Bridge + Modified Unkiu Hull + Modified Coelacanth Stern

### Supported Submarine Routes & Gil Rates

The script recognizes the following submarine builds and their gil farming rates (sorted by gil/day):

| Route | Duration | Gil/Day | Build Variants |
|-------|:--------:|--------:|----------------|
| **JORZ** | 36h | **140,404** | S+S+U+C+ / S+S+U+C |
| **MROJ** | 36h | **120,728** | S+S+S+C+ / S+S+U+C+ |
| **OJ** | 24h | **118,661** | WSUC / SSUC / W+S+U+C+ / S+S+U+C+ |
| **MROJZ** | 48h | **116,206** | YSCU / SCUS / S+C+U+S+ |
| **JOZ** | 36h | **113,321** | YSYC / Y+S+Y+C+ |
| **ROJ** | 36h | **106,191** | WCSU / WUSS / W+U+S+S+ |
| **JORZ 48h** | 48h | **105,303** | WCYC / WUWC / W+U+W+C+ |
| **MOJ** | 36h | **93,165** | YUUW / Y+U+U+W+ |

**Notes:**
- JORZ (36h) provides the highest gil/day rate at 140,404
- OJ route has the shortest duration (24h) making it easier to manage
- Multiple build variants can run the same route with identical gil rates
- The **Gil Farmed Daily/Monthly/Annually** calculations are based on these rates multiplied by the number of submarines using each build

## File Locations

- **AutoRetainer**: `pluginConfigs/AutoRetainer/DefaultConfig.json`
- **Altoholic**: `pluginConfigs/Altoholic/altoholic.db`
- **Lifestream**: `pluginConfigs/Lifestream/DefaultConfig.json`

## Requirements

- Python 3.12.4+
- xlsxwriter

## Installation

```bash
pip install xlsxwriter
```

## Output File Naming

Reports are automatically saved with timestamp format:
```
YYYY-MM-DD-HH-MM - ffxiv_gil_summary.xlsx
```

## Version History

**v1.11** (2025-11-18) - Added Inventory Spaces, Ventures, and VentureCoffers columns  
**v1.10** (2025-11-15) - Fixed submarine data extraction for custom-named submarines and FC counting logic  
**v1.09** (2025-11-11) - Integrated Lifestream housing data  
**v1.08** (2025-11-01) - Formatting improvements  
**v1.07** (2025-10-22) - Per-account submarine control  
**v1.06** (2025-10-13) - Column layout updates  
**v1.05** (2025-10-07) - Altoholic integration  
**v1.00** (2025-03-29) - Initial release

---

## Created by

https://github.com/xa-io

Last Updated: 2025-11-18 19:28:00
