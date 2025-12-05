# Auto-AutoRetainer v1.12 - FFXIV Submarine Automation System

**Automated FFXIV Submarine Management System**

A comprehensive automation script that monitors submarine return times across multiple FFXIV accounts and automatically manages game instances for optimal submarine collection. Integrates with AutoRetainer plugin data to track submarine voyages and calculates daily gil earnings.

## How It Works

**Script Operation Flow:**
- **Script Starts** and initializes monitoring system
- **Pulls AutoRetainer DefaultConfig** files for ETA and displays timers
- **Opens game** when there's 0.15 hours (9 minutes) from sub returning (or immediately for force247uptime accounts)
- **Closes game** once all rotated and submarines won't return for 0.5 hours (30 minutes) for submarine-only accounts
- **Keeps clients running** for accounts with `force247uptime=True` so AutoRetainer can process retainers continuously
- **Forces client restart** after 71 hours of uptime (`MAX_RUNTIME`) to avoid FFXIV 72-hour stability issues
- **Crash recovery**: If game crashes when subs are ready or 24/7 uptime is enabled, game automatically relaunches
- **Timers refresh** every 30 seconds
- **Client checkers refresh** every 60 seconds

## Why Do I Want This

- **Keeps your game closed by default** and only opens it when it actually needs to be running.
- **Auto-recovers from crashes** by relaunching the game whenever it should be open but has closed unexpectedly.
- **Avoids the 72-hour log-in issue** by restarting the client automatically at 71 hours of uptime.
- **Supports multiple play styles** whether you want the game open only when submarines are ready, running 24/7, or just throughout the day.

## Core Automation Features

- **Intelligent Game Launching**: Automatically opens game instances when submarines are nearly ready (9 minutes by default, configurable)
- **Smart Idle Management**: Closes games when submarines won't be ready for an extended period (30 minutes by default, configurable)
- **Crash Recovery**: Automatically detects and relaunches crashed game instances

## Features

### Real-Time Monitoring
- **Live Submarine Timers**: Displays soonest submarine return time for each account
- **Dual Refresh Rates**: 30-second timer updates, 60-second window status checks
- **Ready Status Detection**: Shows when submarines are already returned and ready
- **Gil Earnings Tracking**: Calculates total daily gil from all submarine builds
- **Process ID Tracking**: Monitors running game instances for each account (multi-client mode only)
- **Restocking Alerts**: Displays "Total Days Until Restocking Required" showing the lowest value across all characters
- **Build-Based Consumption**: Tracks Ceruleum tanks and Repair Kit usage per submarine build (9-14 tanks/day, 1.33-4 kits/day depending on route)
- **Default Consumption Rates**: Unlisted builds (leveling submarines like SSUS, SSSS) automatically use 9 tanks/day and 1.33 kits/day

### Intelligent Automation
- **Auto-Launch Games**: Automatically opens games when submarines are nearly ready (9 minutes by default)
- **Auto-Close Games**: Closes idle games when submarines won't be ready soon (30 minutes by default)
- **Smart Rate Limiting**: Prevents rapid game launches with configurable delays
- **Window Arrangement**: Automatically arranges game windows using customizable layouts

### Submarine Build Analysis
- **Build Detection**: Identifies submarine parts (WSUC, SSUC, YSYC, etc.)
- **Route Recognition**: Matches builds to known voyage routes (OJ, MOJ, ROJ, JOZ, JORZ, etc.)
- **Gil Calculations**: Displays total gil per day from all submarine builds
- **Multiple Build Support**: Handles all submarine classes (Shark, Unkiu, Whale, Coelacanth, Syldra, Modified variants)
- **Restocking Calculation**: Automatically calculates days until restocking required based on Ceruleum (tanks) and Repair Kits inventory
- **Inventory Tracking**: Monitors tank and kit consumption rates per submarine build (includes fallback rates for unlisted builds)
- **Proactive Alerts**: Shows minimum days remaining across all characters to prevent submarines from running dry
- **Universal Build Support**: All submarine builds tracked, including leveling builds not listed in consumption rate dictionary

---

## Quick Start

### 1. Prerequisites

**Required Software:**
- Python 3.12.4+
- FFXIV with XIVLauncher (Dalamud)
- AutoRetainer plugin (installed and configured)
- pywin32 package: `pip install pywin32`
- psutil package (recommended): `pip install psutil` - Enables accurate process uptime tracking. Optional but recommended for proper MAX_RUNTIME enforcement.

**Required Plugin Configuration:**
- **AutoRetainer Multi-Mode**: Must be enabled and set to auto-enable, enable Wait on login screen in common settings
- **No 2FA**: Two-factor authentication must be disabled on accounts
- **Autologging Enabled**: XIVLauncher must have autologin configured for each account

---

## Setup Instructions

### Step 1: Configure Account Locations

Edit the `account_locations` list in `Auto-AutoRetainer.py` (around line 56-65):

```python
account_locations = [
     acc("Main",   f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs", include_submarines=False, force247uptime=False),
     acc("Acc1",   f"C:\\Users\\{user}\\AltData\\Acc1\\pluginConfigs", include_submarines=True, force247uptime=True),
    # Add more accounts as needed
]
```

- **nickname**: Short identifier for the account (used in display and window detection)
- **pluginconfigs_path**: Path to the account's plugin configuration folder
- **include_submarines**: Set to `True` to monitor submarines, `False` to disable submarine monitoring
- **force247uptime**: Set to `True` to keep the game always running for this account so AutoRetainer can continuously rotate retainers (subject to `MAX_RUNTIME` safety restarts)

**Configuration Behavior Matrix:**

| include_submarines | force247uptime | Behavior |
|-------------------|----------------|----------|
| `False` | `False` | Client closes if detected running (no submarines or retainers, no need to stay online) |
| `False` | `True` | Client stays running with **[Up 24/7]** status (for Retainer rotation only) |
| `True` | `False` | Normal submarine monitoring with timer-based launch/close |
| `True` | `True` | Submarine monitoring + forced 24/7 uptime with **[Up 24/7]** status |

**Understanding the Flags:**
- Use `include_submarines=False, force247uptime=False` for accounts with no submarines and no Retainer rotation needs
- Use `include_submarines=False, force247uptime=True` for accounts that need 24/7 uptime for Retainer but have no submarines
- Use `include_submarines=True, force247uptime=False` for standard submarine farming accounts
- Use `include_submarines=True, force247uptime=True` for accounts that need both submarine monitoring and continuous Retainer rotation

### Step 2: Configure Game Launchers

Edit the `GAME_LAUNCHERS` dictionary in `Auto-AutoRetainer.py` (around line 68-77):

```python
GAME_LAUNCHERS = {
     "Main":   rf"C:\Users\{user}\AppData\Local\XIVLauncher\XIVLauncher.exe",
     "Acc1":   rf"C:\Users\{user}\AltData\Acc1.bat",
    # Add more launchers as needed
}
```

---

## Creating Alternative Dalamud Launchers for Alt Accounts

### Why Use Alternative Launchers?

If you're using **more than one account**, you may be dealing with:
- Having to manually change login credentials in the default launcher
- Different plugin configurations for each account
- Manually enabling/disabling plugins when switching accounts
- Triggering plugin collections or managing conflicts

**Solution:** Create secondary launchers that use separate plugin directories for each alt account. This keeps your main and alt accounts completely isolated with their own plugin configurations.

### Disclaimer

Each alt launcher needs its own plugin maintenance. When you update plugins on your main launcher, you'll need to repeat the update process for your alt launchers since they use separate directories.

---

### Step-by-Step Setup Guide

#### Step 1: Locate Your User Profile Directory

1. Right-click your current XIVLauncher shortcut → **Properties**
2. Note the path (should be something like `C:\Users\UserName\AppData\Roaming\XIVLauncher`)
3. Press **Windows + R** to open Run
4. Type `%USERPROFILE%` and press Enter
5. Verify this matches the user directory from the shortcut

#### Step 2: Create AltData Directory Structure

1. Inside your `%USERPROFILE%` folder (e.g., `C:\Users\YourName`), create a new folder named **`AltData`**
2. Inside `AltData`, create a folder for each alt account:
   - Example: `C:\Users\YourName\AltData\Acc1`
   - Example: `C:\Users\YourName\AltData\Acc2`
   - Name them whatever you want (these will be your alt data directories)

**Important:** If you have 2 accounts total, create only 1 alt folder. If you have 3 accounts, create 2 alt folders, etc.

#### Step 3: Create Batch File Launchers

1. While in your `AltData` folder, click **View** → Check **File Name Extensions**
2. Create a new text document
3. Rename it from `New Text Document.txt` to `Acc1.bat` (confirm file type change)
4. Right-click the `.bat` file → **Edit**
5. Add the following content:

```batch
start "" /d "%USERPROFILE%\AppData\Local\XIVLauncher" "%USERPROFILE%\AppData\Local\XIVLauncher\XIVLauncher.exe" --roamingPath="%USERPROFILE%\AltData\Acc1"
```

**Batch File Template:**
```batch
start "" /d "%USERPROFILE%\AppData\Local\XIVLauncher" "%USERPROFILE%\AppData\Local\XIVLauncher\XIVLauncher.exe" --roamingPath="%USERPROFILE%\AltData\[FolderName]"
```

6. Save and close the file
7. Create a shortcut of the `.bat` file on your desktop for easy access

**Repeat Steps 2-3 for each additional alt account (Acc2, Acc3, etc.)**

#### Step 4: Copy Existing Configuration (Optional but Recommended)

To preserve your existing plugin configurations:

1. Press **Windows + R** → Enter: `%USERPROFILE%\AppData\Roaming\XIVLauncher`
2. Copy the following items:
   - **Folders:** `installedPlugins`, `pluginConfigs`
   - **Files:** `accountsList`, `dalamudConfig`, `dalamudUI`, `launcherConfigV3`
3. Navigate to your alt data folder (e.g., `%USERPROFILE%\AltData\Acc1`)
4. Paste the copied items

**Note:** When you first log in with your alt launcher, it will show your previously logged-in account info. Simply enter your alt account credentials and they'll be saved for future launches. Make sure you hit tab after entering your username and password, if you just type your password and press enter it will not save the updated password. Enable Log in automatically and disable use one-time passwords.

---

### Launcher Options:

#### Option A: Direct XIVLauncher.exe (Main Account)

Use the standard launcher for your main account:

```python
"Main": r"C:\Users\YourName\AppData\Local\XIVLauncher\XIVLauncher.exe"
```

#### Option B: Batch File Launchers (Alt Accounts)

Use the `.bat` files you created for alt accounts:

```python
"Acc1": r"C:\Users\YourName\AltData\Acc1.bat"
"Acc2": r"C:\Users\YourName\AltData\Acc2.bat"
```

**Complete Example Configuration:**
```python
GAME_LAUNCHERS = {
    "Main": rf"C:\Users\{user}\AppData\Local\XIVLauncher\XIVLauncher.exe",
    "Acc1": rf"C:\Users\{user}\AltData\Acc1.bat",
    "Acc2": rf"C:\Users\{user}\AltData\Acc2.bat",
}
```

---

### Using Your Launchers

- **Main Account:** Use the default XIVLauncher shortcut on your desktop
- **Alt Accounts:** Use the `.bat` shortcuts you created in Step 3

Each launcher maintains its own:
- Plugin configurations
- Saved login credentials
- Dalamud settings
- AutoRetainer configurations

**Benefits:**
- ✓ No manual credential switching
- ✓ Separate plugin configurations per account
- ✓ No plugin conflicts between accounts
- ✓ Independent AutoRetainer settings
- ✓ Clean separation of account data

### Step 3: Label Game Windows (CRITICAL for Multi-Client Mode)

**⚠️ Note:** If you're using **single client mode** (`USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME = True`), you can **skip this entire step**. Single client mode uses the default "FINAL FANTASY XIV" window title and doesn't require window renaming. However, this mode **only supports 1 account** and **disables MAX_RUNTIME protection**.

**For Multi-Client Mode (Default):**

For the script to detect and manage game instances, **you must rename the FFXIV game window title** to follow this exact format:

```
ProcessID - nickname
```

**Examples of Final Window Titles:**
- `3056 - Main`
- `58696 - Acc1`
- `12345 - Acc2`

**📝 Quick Note:** The Process ID is **automatically generated** by the Splatoon script - you only need to enter your account nickname (Main, Acc1, etc.). The script handles everything else!

---

**How to Rename Game Windows:**

#### Recommended Method: Splatoon Plugin Script

**Splatoon** is a Dalamud plugin that allows custom scripting, including automatic window title renaming with process ID and nickname.

**Step 1: Install Splatoon**
1. Open Dalamud plugin installer in FFXIV (`/xlplugins`)
2. Go to "Settings" → "Experimental"
3. Add custom repository: `https://love.puni.sh/ment.json`
4. Search for "Splatoon" and install it

**Step 2: Install Window Rename Script**
1. Open Splatoon settings in-game
2. Click on the **"Scripts"** tab
3. Copy the following script code to your clipboard:

```csharp
using ECommons.Interop;
using ECommons.Logging;
using ECommons.Schedulers;
using Splatoon.SplatoonScripting;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SplatoonScriptsOfficial.Generic;
public unsafe sealed class RenameWindow : SplatoonScript
{
    public override Metadata Metadata { get; } = new(1, "NightmareXIV");
    public override HashSet<uint>? ValidTerritories { get; } = null;

    public override void OnEnable()
    {
        Rename($"{Environment.ProcessId} - Main");
    }

    public override void OnDisable()
    {
        Rename("FINAL FANTASY XIV");
    }

    void Rename(string name)
    {
        if(WindowFunctions.TryFindGameWindow(out var hwnd))
        {
            fixed(char* ptr = name)
            {
                TerraFX.Interop.Windows.Windows.SetWindowText(hwnd, (ushort*)ptr);
            }
        }
        else
        {
            PluginLog.Error($"Couldn't find game window!"); //retry it again
            new TickScheduler(() => Rename(name));
        }
    }
}
```

4. In Splatoon Scripts tab, click **"Install from Clipboard"**
5. **IMPORTANT - Edit the Nickname Only:**
   - In the script line: `Rename($"{Environment.ProcessId} - Main");`
   - **Replace ONLY the word after the dash** with your account nickname
   - The `Environment.ProcessId` part is **automatic** - DO NOT change it
   - **Keep the space-dash-space formatting:** ` - `
   
   **Examples:**
   - For "Main" account: `Rename($"{Environment.ProcessId} - Main");`
   - For "Acc1" account: `Rename($"{Environment.ProcessId} - Acc1");`
   - For "Acc2" account: `Rename($"{Environment.ProcessId} - Acc2");`

6. Enable the script by checking the box next to "RenameWindow"
7. The window title will automatically update to format: `ProcessID - nickname`
   - Example: `12345 - Main` (where 12345 is the auto-generated process ID)

**Benefits of Splatoon Method:**
- ✓ **Process ID is automatically generated** - you never need to manually enter it
- ✓ Persists across game restarts
- ✓ Works with XIVLauncher multi-account setups
- ✓ Automatically reverts to default title when disabled

**Step 3: Verify Each Account**
- Create a **separate Splatoon script** for EACH account with its unique nickname
- Launch each game instance and verify the window title shows correct format
  - Example: `3056 - Main` or `58696 - Acc1`
- The nickname MUST match exactly what you configured in `account_locations` in the Python script

---

### Step 4: Enable AutoRetainer Multi-Mode

**AutoRetainer Configuration Requirements:**

1. **Enable Multi-Mode:**
   - Open AutoRetainer settings Multi Mode > Commonn Settings
   - Enable Game Startup, Enable Multi Mode on Game Boot
   - This allows AutoRetainer to automatically handle sub processing across characters

2. **Configure Submarine Settings:**
   - Enable submarine voyage management in AutoRetainer
   - Set submarines to automatically redeploy when they return
   - Configure preferred routes for each submarine

3. **Test Multi-Mode:**
   - Log into a character with submarines
   - Verify AutoRetainer automatically handles all submarines
   - Ensure it moves to next character after completion

### Step 5: Configure Autologging (CRITICAL)

**For Full Automation, You MUST:**

1. **Disable 2FA (Two-Factor Authentication):**
   - Log into your Square Enix account management
   - Navigate to security settings
   - **Disable** One-Time Password (2FA) for each account
   - **Warning:** This reduces account security. Use at your own risk.

2. **Enable XIVLauncher Autologin:**
   - Open XIVLauncher settings
   - Enable "Log in automatically" option
   - Save your username and password
   - Test that the game launches and logs in automatically

3. **Configure Alt Account Autologin:**
   - Each alt account data folder must have its own saved credentials
   - Test each batch file launcher to verify autologin works
   - Game should launch and log in without any manual input

4. **Verify Full Automation:**
   - Close all FFXIV instances
   - Run one of your batch file launchers
   - Confirm the game:
     - Launches automatically
     - Logs in without prompts
     - Reaches main menu screen with Mutli Enabled

**Security Warning:**
- Disabling 2FA and saving passwords reduces account security
- Only use this on accounts you're willing to risk
- Consider using dedicated submarine farming accounts
- Never share your launcher files or credential data

### Step 6: Configure Window Layouts (Optional)

For automatic window arrangement, create layout JSON files:

**File: `window_layout_main.json`** (place in script folder)

```json
{
  "rules": [
    {
      "title_regex": "^\\d+\\s-\\sMain$",
      "x": 0,
      "y": 0,
      "width": 1040,
      "height": 760,
      "topmost": false,
      "activate": true,
      "order": 80,
      "comment": "Matches 'Main' - Moved LAST (top of stack)"
    },
    {
      "title_regex": "^\\d+\\s-\\sAcc1$",
      "x": 0,
      "y": 19,
      "width": 1040,
      "height": 760,
      "topmost": false,
      "activate": true,
      "order": 70,
      "comment": "Matches 'Acc1' - Moved FIRST (bottom of stack)"
    }
  ]
}
```

**Configuration Options:**
- **title_regex**: Pattern to match window titles (use `\\d+ - nickname` format)
- **x, y**: Window position coordinates
- **width, height**: Window dimensions
- **topmost**: Keep window always on top (true/false)
- **activate**: Focus this window after arrangement (true/false)
- **order**: Arrangement order (lower numbers arranged first)

---

## Configuration Parameters

### Timing Settings
```python
TIMER_REFRESH_INTERVAL = 30    # Update submarine timers every 30 seconds
WINDOW_REFRESH_INTERVAL = 60   # Check game window status every 60 seconds
```

### Auto-Close Settings
```python
ENABLE_AUTO_CLOSE = True        # Enable automatic game closing
AUTO_CLOSE_THRESHOLD = 0.5      # Close game if next sub > 0.5 hours (30 minutes)
MAX_RUNTIME = 71                # Maximum allowed client uptime in hours before a forced restart
```

### Auto-Launch Settings
```python
ENABLE_AUTO_LAUNCH = True       # Enable automatic game launching
AUTO_LAUNCH_THRESHOLD = 0.15    # Launch game if next sub <= 0.15 hours (9 minutes)
OPEN_DELAY_THRESHOLD = 60       # Minimum 60 seconds between game launches
MAX_CLIENTS = 0                 # Maximum concurrent running clients (0 = unlimited, N = limit to N clients)
```

**MAX_CLIENTS Behavior:**
- **When set to 0 (Default)**: No limit on concurrent clients, launches all ready accounts simultaneously
- **When set to N**: Limits to N concurrent running game clients at a time
- **Prioritizes force247uptime accounts**: Ensures 24/7 uptime clients launch first before submarine-ready clients
- **Sequential Processing**: Opens clients one at a time with OPEN_DELAY_THRESHOLD wait between each
- **Per-Client Workflow**: After launching each client, refreshes window status, waits OPEN_DELAY_THRESHOLD, arranges windows, then proceeds to next client
- **Terminal Display**: Shows "Max Clients: N" in the terminal output when set to 1 or above (hidden when 0)
- **Use Case**: Ideal for hardware-limited setups that can only run a set number of game instances due to RAM/CPU constraints

### Window Layout Settings
```python
ENABLE_WINDOW_LAYOUT = True     # Enable automatic window arrangement
WINDOW_LAYOUT = "main"          # Layout to use: "main" or "left"
WINDOW_MOVER_DIR = Path(__file__).parent  # Folder containing layout JSON files
```

### Debug Settings
```python
DEBUG = False                   # Show detailed debug output
```

### Single Client Mode Settings
```python
USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME = False  # Window detection mode
```

**When False (Default - Multi-Client Mode):**
- Uses "ProcessID - nickname" window title format
- Supports multiple accounts simultaneously
- Tracks individual process IDs for uptime monitoring
- Kills games by specific PID
- **MAX_RUNTIME enforcement enabled** (71h uptime limit)

**When True (Single Client Mode):**
- Uses default "FINAL FANTASY XIV" window title
- **Only supports 1 account** (validation enforced)
- Tracks uptime using `psutil` to detect `ffxiv_dx11.exe` process
- Kills game by process name (ffxiv_dx11.exe)
- **MAX_RUNTIME enforcement enabled** (71h uptime limit via process name detection)
- Useful for simple single-account setups without window title modification

**⚠️ Important Limitations in Single Client Mode:**
- Cannot run multiple accounts simultaneously
- Script will exit with error if multiple accounts are configured
- Requires `psutil` package for uptime tracking (install with: `pip install psutil`)

---

## Usage

### Running the Script

```bash
python Auto-AutoRetainer.py
```

### Display Output

```
=====================================================================================
FFXIV Submarine Timer Monitor
=====================================================================================
Updated: 2025-11-26 11:44:56
=====================================================================================

Main  (36 subs)  : -0.0 hours (7 READY)    [Running] PID: 11376 UPTIME: 1.6 hours

=====================================================================================
Total Subs: 0 / 36
Total Gil Per Day: 4,193,236
Total Subs Leveling: 0
Total Subs Farming: 36
Total Days Until Restocking Required: 11
=====================================================================================
Press Ctrl+C to exit
=====================================================================================
```

### Status Indicators

- **Positive hours** (`+2.3 hours`): Time remaining until submarine returns
- **Positive hours with (WAITING)** (`+0.0 hours (WAITING)`): Game is running with 0 ready subs, waiting for submarines within auto-close threshold
- **Negative hours** (`-0.5 hours (1 READY)`): Submarines already returned and waiting
- **Disabled**: Submarine monitoring is disabled for this account (include_submarines=False)
- **[Running]**: Game is currently open for this account
- **[Closed]**: Game is not running
- **[Up 24/7]**: Account has force247uptime=True enabled, client should remain running continuously
- **PID: xxxxx**: Process ID of the running game instance
- **UPTIME: x.x hours**: How long the game process has been running

### Automation Behavior

**Auto-Launch Example:**
```
[AUTO-LAUNCH] Launching Acc1 - submarines nearly ready (0.1h)
[AUTO-LAUNCH] Successfully launched Acc1, waiting 60 seconds before checking clients again.
[WINDOW-MOVER] Arranging windows with 'main' layout...
[WINDOW-MOVER] Moved: '3056 - Acc1' -> (1920,0,1280,720)
```

**Auto-Close Example:**
```
[AUTO-CLOSE] Closing Acc2 (PID: 58696) - Next sub in 2.3h
[AUTO-CLOSE] Successfully closed Acc2, waiting 30 seconds before checking clients again.
```

**Force247uptime Launch Example:**
```
[AUTO-LAUNCH] Launching Main - force247uptime enabled
[AUTO-LAUNCH] Successfully launched Main, waiting 60 seconds before checking clients again.
```

**MAX_RUNTIME Restart Example:**
```
[AUTO-CLOSE] Closing Acc1 (PID: 13728) - Uptime 71.2h exceeds MAX_RUNTIME 71h
[AUTO-CLOSE] Successfully closed Acc1 after 71.2h, waiting 30 seconds before checking clients again.
```

---

## Requirements

### Python Packages
```bash
pip install pywin32
```

### System Requirements
- **OS**: Windows 10/11 (script uses win32gui for window management)
- **Python**: 3.12.4 or higher
- **FFXIV**: With XIVLauncher and Dalamud, Auto-Open Game, No One Time Password, AutoRetainer Auto-Enable Multi when logging in

### Plugin Requirements
- **AutoRetainer**: For submarine data and automation
- **Splatoon** (Recommended): For automatic window title renaming with process ID
  - Repository: `https://love.puni.sh/ment.json`
  - Enables automatic window detection and management
- **Window Title Plugin**: (Alternative) For manual window title customization

---

## Data Sources

### AutoRetainer Configuration Files
- **Location**: `{account_path}/AutoRetainer/DefaultConfig.json`
- **Data Fields**:
  - `OfflineSubmarineData` → `ReturnTime` (Unix timestamp)
  - `AdditionalSubmarineData` → Submarine parts and builds

### Submarine Build Detection
The script identifies submarine builds by part IDs:
- **Shark-class** (S): Part IDs 21792-21795
- **Unkiu-class** (U): Part IDs 21796-21799
- **Whale-class** (W): Part IDs 22526-22529
- **Coelacanth-class** (C): Part IDs 23903-23906
- **Syldra-class** (Y): Part IDs 24344-24347
- **Modified variants** (S+, U+, W+, C+, Y+): Part IDs 24348-24367

### Gil Rate Calculations
Based on known voyage routes:
- **JORZ Route (36h)**: 140,404 gil/day (highest)
- **MOJZ Route (36h)**: 127,857 gil/day
- **MROJ Route (36h)**: 120,728 gil/day
- **OJ Route (24h)**: 118,661 gil/day
- **JOZ Route (36h)**: 113,321 gil/day
- **MROJZ Route (48h)**: 116,206 gil/day
- And more...

---

## Troubleshooting

### Game Not Launching
1. Verify launcher path in `GAME_LAUNCHERS` is correct
2. Check that batch files use correct `start "" ...` syntax
3. Ensure XIVLauncher autologin is configured
4. Test launcher manually before running script

### Window Not Detected
1. Confirm window title matches `ProcessID - nickname` format exactly
2. Check that nickname matches `account_locations` configuration
3. Use regex pattern `\d+ - nickname` (digits, space, dash, space, nickname)
4. Install a window title plugin if manual renaming is difficult

### Auto-Launch Not Working
1. Enable debug mode: `DEBUG = True`
2. Check submarine timer data is being read correctly
3. Verify `ENABLE_AUTO_LAUNCH = True`
4. Adjust `AUTO_LAUNCH_THRESHOLD` if submarines ready too early/late
5. Check `OPEN_DELAY_THRESHOLD` isn't preventing launches

### AutoRetainer Not Processing Submarines
1. Verify AutoRetainer multi-mode is enabled and set to auto-enable
2. Check submarine voyage settings in AutoRetainer configuration
3. Ensure characters have submarines unlocked and deployed
4. Test AutoRetainer manually before using automation

### 2FA/Login Issues
1. **Disable 2FA** on all accounts (required for full automation)
2. Ensure XIVLauncher has saved credentials for each account
3. Test autologin by running launcher manually
4. Check that no login prompts appear during launch

---

## Advanced Configuration

### Multiple Monitor Setups

You can create different window layout files for different monitor configurations. The script will use the layout specified in the `WINDOW_LAYOUT` configuration variable.

#### Configuration Variable

In `Auto-AutoRetainer.py`, set the layout to use:

```python
WINDOW_LAYOUT = "main"       # Uses window_layout_main.json
# OR
WINDOW_LAYOUT = "secondary"  # Uses window_layout_secondary.json
```

#### Primary Monitor Layout (window_layout_main.json)

For positioning windows on your primary monitor:

```json
{
  "rules": [
    {
      "title_regex": "^\\d+\\s-\\sMain$",
      "x": 0,
      "y": 0,
      "width": 1040,
      "height": 760,
      "topmost": false,
      "activate": true,
      "order": 80,
      "comment": "Primary monitor - Main account"
    },
    {
      "title_regex": "^\\d+\\s-\\sAcc1$",
      "x": 0,
      "y": 19,
      "width": 1040,
      "height": 760,
      "topmost": false,
      "activate": true,
      "order": 70,
      "comment": "Primary monitor - Acc1"
    }
  ]
}
```

#### Secondary Monitor Layout (window_layout_secondary.json)

For positioning windows on a **secondary monitor positioned to the LEFT** of your primary monitor, use **negative coordinates**:

```json
{
  "rules": [
    {
      "title_regex": "^\\d+\\s-\\sMain$",
      "x": -1920,
      "y": 0,
      "width": 1040,
      "height": 760,
      "topmost": false,
      "activate": true,
      "order": 80,
      "comment": "Secondary monitor (left) - Main account"
    },
    {
      "title_regex": "^\\d+\\s-\\sAcc1$",
      "x": -1920,
      "y": 19,
      "width": 1040,
      "height": 760,
      "topmost": false,
      "activate": true,
      "order": 70,
      "comment": "Secondary monitor (left) - Acc1"
    }
  ]
}
```

#### Monitor Coordinate System

**Understanding X and Y Coordinates:**

- **Primary Monitor (right):** X starts at `0`, Y starts at `0`
- **Secondary Monitor (left of primary):** X uses **negative values** (e.g., `-1920` for 1920px wide monitor)
- **Secondary Monitor (right of primary):** X uses **positive values beyond primary width** (e.g., `1920` if primary is 1920px wide)
- **Secondary Monitor (above primary):** Y uses **negative values**
- **Secondary Monitor (below primary):** Y uses **positive values beyond primary height**

**Examples:**

- **Left monitor (1920x1080):** `x: -1920, y: 0`
- **Right monitor (1920x1080):** `x: 1920, y: 0` (if primary is 1920px wide)
- **Above monitor (1920x1080):** `x: 0, y: -1080`
- **Below monitor (1920x1080):** `x: 0, y: 1080` (if primary is 1080px tall)

#### Switching Between Layouts

1. Create your layout files: `window_layout_main.json`, `window_layout_secondary.json`
2. Edit `Auto-AutoRetainer.py`
3. Change `WINDOW_LAYOUT = "main"` to `WINDOW_LAYOUT = "secondary"`
4. Restart the script

The script will automatically load `window_layout_{name}.json` based on the `WINDOW_LAYOUT` variable.

---

## Safety Notes

1. **Account Security**: Disabling 2FA and saving passwords reduces security
2. **Terms of Service**: Automation may violate FFXIV ToS - use at your own risk
3. **Process Management**: Script uses `taskkill /F` to force close games
4. **Rate Limiting**: Built-in delays prevent rapid launches but monitor CPU/disk usage
5. **Testing**: Always test with one account before enabling full automation

---

## Credits

- **Punish Community**: For all the help along the way
- **AutoRetainer Plugin**: For submarine data and automation framework
- **XIVLauncher**: For multi-account support and autologin functionality
- **Dalamud**: For plugin ecosystem

---

## Version History

**v1.12** (2025-12-05) - Enhanced auto-launch visual feedback with real-time client status display after each game launch, reducing console spam and improving visibility during sequential launches  
**v1.11** (2025-11-26) - Added MAX_CLIENTS configuration for hardware-limited setups with sequential client processing, force247uptime prioritization, and terminal display  
**v1.10** (2025-11-26) - Added restocking calculation with "Total Days Until Restocking Required" display  
**v1.09** (2025-11-15) - Fixed submarine build collection for custom-named submarines and enhanced console display  
**v1.08** (2025-11-15) - Enhanced configuration flag handling and status display improvements  
**v1.07** (2025-11-14) - Added (WAITING) status display for running games with 0 ready subs  
**v1.06** (2025-11-14) - Renamed 'rotatingretainers' parameter to 'force247uptime' for clarity  
**v1.05** (2025-11-14) - Fixed PID and UPTIME display in single client mode  
**v1.03** (2025-11-14) - Simplified for single account use with default window title  
**v1.02** (2025-11-13) - Fixed auto-launch not checking submarine timers for non-rotating accounts  
**v1.01** (2025-11-13) - Added per-account force247uptime flag and MAX_RUNTIME limits  
**v1.00** (2025-11-12) - Initial release with comprehensive submarine automation
