# FFXIV AR Parser with Altoholic

Excel report generator for FFXIV AutoRetainer data with integrated Altoholic inventory scanning.

## Features

- **Character Gil Tracking**: Aggregates gil across all characters and retainers
- **Inventory Tracking**: Tracks Tanks and Kits from DefaultConfig.json, Treasure items and Submarine Parts from Altoholic
- **Inverse Supplier Integration**: Generates formatted toon list with smart inventory-based distribution for XA Inverse Supplier v2.11
  - Calculates needed amounts: (threshold - current_inventory)
  - Copy-paste ready format for Lua toon_list configuration
  - Global inventory_needs configuration applies to all accounts
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
acc(nickname, pluginconfigs_path, include_altoholic=True, include_submarines=True, 
    fuel_threshold=None, repair_mats_threshold=None)
```

**Parameters:**
- `nickname`: Display name for the account in reports
- `pluginconfigs_path`: Path to the XIVLauncher pluginConfigs folder
- `include_altoholic`: Whether to scan Altoholic inventory data for treasure items and submarine parts (default: True)
- `include_submarines`: Whether to include submarine builds/levels in output and calculations (default: True)
- `fuel_threshold`: Override global inventory_needs fuel threshold for this account (default: None, uses global)
- `repair_mats_threshold`: Override global inventory_needs repair threshold for this account (default: None, uses global)

### Inverse Supplier Configuration (v1.13+)

Configure global inventory thresholds for XA Inverse Supplier v2.11 smart distribution:

```python
# Global thresholds applied to all accounts
inventory_needs = {
    "fuel_threshold": 1000,          # Ceruleum Tanks target
    "repair_mats_threshold": 1000    # Repair Kits target
}

account_locations = [
    acc("Main",   f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs", include_submarines=True),
    acc("Acc1",   f"C:\\Users\\{user}\\AltData\\Acc1\\pluginConfigs", include_submarines=True),
]
```

**How It Works:**
- Script reads current Tanks/Kits inventory from DefaultConfig.json
- Calculates needed amount: `max(0, threshold - current_inventory)`
- Generates "Inverse Supplier Formatting" column with format: `{"Toon@World", fuel_needed, kits_needed},`
- Copy column to XA Inverse Supplier v2.11 toon_list for automated smart distribution

**Examples:**

**Same thresholds for all accounts:**
```python
inventory_needs = {
    "fuel_threshold": 1000,
    "repair_mats_threshold": 1000
}

account_locations = [
    acc("Main", path1, include_submarines=True),  # Uses 1000/1000
    acc("Acc1", path2, include_submarines=True),  # Uses 1000/1000
]
```

**Per-account overrides:**
```python
inventory_needs = {
    "fuel_threshold": 1000,
    "repair_mats_threshold": 1000
}

account_locations = [
    acc("Main", path1, include_submarines=True),  # Uses 1000/1000 (global)
    acc("Alt1", path2, include_submarines=True, fuel_threshold=500),  # Uses 500/1000 (override fuel only)
    acc("Floater", path3, fuel_threshold=0, repair_mats_threshold=0),  # Uses 0/0 (no smart distribution)
]
```

**Disable smart distribution:**
```python
inventory_needs = {
    "fuel_threshold": 0,
    "repair_mats_threshold": 0
}
# All accounts excluded from Inverse Supplier formatting
```

### Standard Account Configuration

```python
account_locations = [
     acc("Main",   f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs", include_submarines=True),  # Include submarines
   # acc("Acc1",   f"C:\\Users\\{user}\\AltData\\Acc1\\pluginConfigs", include_submarines=True),   # Include submarines
   # acc("Acc2",   f"C:\\Users\\{user}\\AltData\\Acc2\\pluginConfigs", include_submarines=False),  # No submarines
   # acc("Acc3",   f"C:\\Users\\{user}\\AltData\\Acc3\\pluginConfigs", include_submarines=False),  # No submarines
]
```

### Restocking Days Calculation

The script automatically calculates days until restocking based on:
- **Inventory Data**: Ceruleum tanks and Repair Kits from DefaultConfig.json
- **Submarine Builds**: Consumption rates per build (9-14 tanks/day, 1.33-4 kits/day)
- **Default Rates**: Unlisted builds (leveling submarines) use 9 tanks/day, 1.33 kits/day
- **Formula**: Days = min(tanks/consumption, kits/consumption) rounded down
- **Display**: Shows 0 if character has submarines but no inventory (immediate restocking needed)

### Submarine Inclusion Control

When `include_submarines=False` for an account:
- Submarine levels will display as 0
- Submarine build codes will be empty
- Restocking days will not be calculated
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
- **Last Online** Days since character last logged in (from Altoholic database)
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
- Inventory tracking from DefaultConfig.json
  - Tanks (Ceruleum) quantity
  - Kits (Repair Kits) quantity
  - **Restocking Days** - Calculated days until restocking required based on submarine build consumption rates
  - Inventory Spaces remaining
  - Ventures count
  - VentureCoffers count
- Altoholic inventory tracking
  - Treasure value (gil from salvaged accessories)
  - **40 Submarine Part Columns** - Tracks all submarine parts by class (S, U, W, C, Y, S+, U+, W+, C+, Y+) and type (BOW, BRG, PH, STN)
  - **Total Parts** - Sum of all submarine parts in inventory
- Formatting options for various tools:
  - **Plain Name** - Simple "Character@World" format
  - **List Formatting** - List format with quotes
  - **SND Formatting** - SomethingNeedDoing format
  - **Bagman Formatting** - XA Inverse Bagman format with Tony placeholder
  - **Inverse Supplier Formatting** (v1.13+) - XA Inverse Supplier v2.11 smart distribution format
    - Shows calculated needed amounts: `{"Character@World", fuel_needed, kits_needed},`
    - Based on inventory_needs thresholds minus current inventory
    - Ready to copy directly into Inverse Supplier toon_list
  - **Tanks Needed** (v1.13+) - Numeric fuel needed value (threshold - current tanks)
  - **Kits Needed** (v1.13+) - Numeric kits needed value (threshold - current kits)

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

### Submarine Parts Tracking (Altoholic)

The script tracks all submarine parts stored in character inventories via Altoholic. Parts are organized in **40 columns** by class and type:

**Part Classes (10 total):**
- Base: S, U, W, C, Y
- Modified: S+, U+, W+, C+, Y+

**Part Types (4 per class):**
- **BOW** - Bow part
- **BRG** - Bridge part  
- **PH** - Pressure Hull part
- **STN** - Stern part

**Column Format:** Each column is labeled as `{CLASS} {TYPE}` (e.g., "S BOW", "W+ PH", "Y STN")

**Total Parts Column:** Displays the sum of all 40 submarine parts for quick inventory overview.

This comprehensive tracking helps identify which characters have spare parts for building or upgrading submarines.

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

## Integration with XA Inverse Supplier v2.11

The **Inverse Supplier Formatting** column (v1.13+) integrates seamlessly with XA Inverse Supplier's smart distribution:

**Workflow:**

1. **Configure thresholds** in AR Parser:
   ```python
   inventory_needs = {
       "fuel_threshold": 1000,
       "repair_mats_threshold": 1000
   }
   ```

2. **Run AR Parser** to generate Excel report with current inventory data

3. **Copy Column AR** (Inverse Supplier Formatting) from Excel

4. **Paste into Inverse Supplier** toon_list:
   ```lua
   local toon_list = {
       {"Toon One@World", 500, 200},   -- Needs 500 tanks, 200 kits
       {"Toon Two@World", 0, 0},       -- Already stocked
       {"Toon Three@World", 150, 80},  -- Needs 150 tanks, 80 kits
   }
   ```

5. **Run Inverse Supplier** - automatically distributes only what each character needs!

**Example Calculation:**
- Character has 500 Ceruleum Tanks, 800 Repair Kits
- Thresholds set to 1000/1000
- Inverse Supplier Formatting column shows: `{"Character@World", 500, 200},`
- Tanks Needed column shows: 500
- Kits Needed column shows: 200
- Supplier gives: 500 tanks (to reach 1000), 200 kits (to reach 1000)

## Version History

**v1.14** (2025-12-25) - Added Last Online column from Altoholic database shows days since character last logged in  
**v1.13** (2025-11-26) - Added Inverse Supplier Formatting column with smart inventory-based distribution  
**v1.12** (2025-11-26) - Added Restocking Days calculation and improved data sources  
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

Last Updated: 2025-12-25 10:09:00
