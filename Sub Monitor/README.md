# FFXIV Submarine Timer Monitor

A real-time monitoring script that displays the soonest submarine return time for each FFXIV account.

## Features

- **Live Updates**: Refreshes every 30 seconds automatically
- **Soonest Submarine Only**: Shows only the next submarine to return for each account
- **Account Order**: Displays accounts in the same order as AR Parser
- **Total Count**: Shows total number of submarines per account
- **Ready Status**: Indicates when submarines are already returned

## How It Works

1. Reads AutoRetainer plugin configuration files from each account
2. Extracts submarine return times from `OfflineSubmarineData`
3. Calculates hours remaining until return (negative = already returned)
4. Displays only the **soonest** submarine for each account
5. Updates display every 30 seconds

## Configuration

Account locations are configured in the script (lines 23-32):

```python
account_locations = [
    acc("Main",   f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs", include_submarines=False),
    acc("Acc1",   f"C:\\Users\\{user}\\AltData\\Acc1\\pluginConfigs", include_submarines=True),
    acc("Acc2",   f"C:\\Users\\{user}\\AltData\\Acc2\\pluginConfigs", include_submarines=True),
    acc("Acc3",   f"C:\\Users\\{user}\\AltData\\Acc3\\pluginConfigs", include_submarines=True)
]
```

Set `include_submarines=False` to exclude accounts from submarine monitoring.

## Output Format

```
Main:           Submarines disabled
Acc1:        +2.3 hours           (4 subs)
Acc2:        -0.5 hours (READY)   (4 subs)
Acc3:        +5.7 hours           (4 subs)
```

## Usage

```bash
python SubTimers.py
```

Press `Ctrl+C` to exit.

## Requirements

- Python 3.12.4+
- AutoRetainer plugin data files
- Standard library only (no external dependencies)

## Data Source

This script reads the same AutoRetainer configuration files used by the AR Parser:
- Location: `{account_path}/AutoRetainer/DefaultConfig.json`
- Data field: `OfflineSubmarineData` → `ReturnTime` (Unix timestamp)

## Notes

- Return times are in hours
- Positive hours = time until return
- Negative hours = already returned (READY)
- Screen clears and refreshes every 30 seconds
- Only shows one ETA per account (the soonest submarine)
