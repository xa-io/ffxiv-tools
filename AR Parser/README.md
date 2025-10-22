# FFXIV AR Parser with Altoholic

Excel report generator for FFXIV AutoRetainer data with integrated Altoholic inventory scanning.

## Features

- **Character Gil Tracking**: Aggregates gil across all characters and retainers
- **Altoholic Integration**: Scans Tanks, Kits, and Treasure items from Altoholic inventory
- **Submarine Management**: Tracks submarine builds and levels across all accounts
- **FC Data**: Displays FC names and FC points
- **Region Detection**: Automatically determines region (NA/EU/OCE/JP) based on world
- **Excel Export**: Generates formatted Excel reports with summary statistics
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
- Gil totals (character + retainers)
- Retainer information (name, level, ventures, market board items)
- FC information (name, points)
- Submarine builds and levels (if enabled for account)
- Altoholic inventory (Tanks, Kits, Treasure value)
- Formatting options for various tools

### Summary Sheet
- Total characters and retainers
- Total gil across all accounts
- Average gil per character
- Total Tanks, Kits, and Treasure value
- FC statistics
- Submarine build statistics
- **Gil farming calculations** (only includes accounts with `include_submarines=True`)
  - Gil Farmed Each Day
  - Gil Farmed Every 30 Days  
  - Gil Farmed Annually

## File Locations

- **AutoRetainer**: `pluginConfigs/AutoRetainer/DefaultConfig.json`
- **Altoholic**: `pluginConfigs/Altoholic/altoholic.db`

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

## Created by

https://github.com/xa-io

Last Updated: 2025-10-21 20:10:20
