# XIVLauncher Auto Updater

## Utility script for updating XIVLauncher across one or more FFXIV accounts automatically

This project is a maintenance helper for XIVLauncher profiles.

It launches each configured account, optionally sends a 2FA code, accepts the **"Out of date"** prompt, waits for **FINAL FANTASY XIV** to open, then closes the game so the account is updated and ready for later use.

---

## What Does This Script Do?

- Opens the configured launcher for each enabled account
- Validates the account's `launcherConfigV3.json` settings
- Automatically sends a one-time password (OTP) for 2FA-enabled accounts
- Detects the XIVLauncher **"Out of date"** popup and clicks **Yes**
- Waits for `ffxiv_dx11.exe` to launch
- Waits for a visible game window to appear
- Closes the launched game cleanly
- Closes active `DalamudCrashHandler.exe` processes if they appear
- Repeats the process for every enabled account in `config.json`

---

## When Should You Use This?

Use `auto-update.py` when:

- You want to update multiple XIVLauncher profiles in one pass
- You want to avoid manually opening and closing every account
- You want the launcher update popup handled automatically
- You want 2FA-enabled accounts to be supported during the update process

This script is meant for **updating and verifying launch readiness**, not for normal gameplay launching.

---

## Prerequisites

### Required

- Windows
- Python 3
- XIVLauncher installed
- One working XIVLauncher profile for each account you want to update
- Auto login enabled in XIVLauncher for each account

### Required Python packages

```bash
pip install psutil pyotp keyring requests
```

### Optional but recommended

```bash
pip install pywinauto
```

`pywinauto` improves reliability for clicking the WPF **"Out of date"** popup.

If `pywinauto` is not installed, the script will still try keyboard fallback methods such as `Alt+Y`, `Y`, and `Enter`.

---

## Important XIVLauncher Settings

For each account/profile you want to use with this updater:

### Always enable

- **Log in automatically**

### Enable if that account uses 2FA

- **Use One-Time-Passwords**
- **Enable XL Authenticator app/OTP macro support**

The script also checks the relevant `launcherConfigV3.json` file and will auto-fix:

- `AutologinEnabled`
- `OtpServerEnabled` for 2FA-enabled accounts

---

## Creating Alternative Launchers for Alt Accounts (Optional)

If you only use one account, you can skip this section.

If you use multiple accounts, the cleanest setup is to give each alt account its own XIVLauncher roaming path.

### Why do this?

This keeps each account isolated with its own:

- login state
- plugin configuration
- Dalamud config
- launcher config

### Example batch file launcher

Create a `.bat` file for each alt account, such as `Acc1.bat`, with content like this:

```batch
start "" /d "%USERPROFILE%\AppData\Local\XIVLauncher" "%USERPROFILE%\AppData\Local\XIVLauncher\XIVLauncher.exe" --roamingPath="%USERPROFILE%\AltData\Acc1"
```

### Recommended folder structure

```text
C:\Users\YourName\AppData\Roaming\XIVLauncher
C:\Users\YourName\AltData\Acc1
C:\Users\YourName\AltData\Acc2
C:\Users\YourName\AltData\Acc3
```

### Recommended first-time setup for alt profiles

Copy the following from your main XIVLauncher roaming folder into each alt roaming folder:

- `installedPlugins`
- `pluginConfigs`
- `accountsList`
- `dalamudConfig`
- `dalamudUI`
- `launcherConfigV3.json`

Then log into that alt account once manually so XIVLauncher saves the correct credentials for that profile.

---

## 2FA / OTP Setup

If an account uses 2FA, the updater can automatically send the OTP code to XIVLauncher.

### Requirements for 2FA accounts

- The account must have XIVLauncher OTP support enabled
- The OTP secret must be stored in Windows Credential Manager through `keyring`
- The `keyring_name` in `config.json` must match the stored entry

### Full 2FA setup guide

For a full walkthrough on obtaining the OTP secret, storing it safely, and validating OTP support, use the companion documentation in:

- `FFXIV - Auto 2FA/README.md`

That README covers:

- obtaining the Mogstation authentication key
- storing the key in Windows Credential Manager
- using `Set_2FA_Key.py`
- validating the XIVLauncher OTP API

---

## Configuration

The updater reads settings from `config.json` in the same folder as `auto-update.py`.

If `config.json` does not exist, the script falls back to its built-in defaults. For multi-account use, you should use `config.json`.

---

## Config File Structure

### Top-level timing and debug settings

```json
{
    "DEBUG": false,
    "OTP_LAUNCH_DELAY": 10,
    "OTP_RETRY_INTERVAL": 5,
    "POLL_INTERVAL": 2,
    "GAME_START_TIMEOUT": 3600,
    "GAME_WINDOW_TIMEOUT": 300,
    "CLOSE_GRACE_PERIOD": 15
}
```

### Account list

`account_locations` is the list of accounts the updater will process.

Each account supports:

- `enabled`
- `nickname`
- `pluginconfigs_path`
- `enable_2fa`
- `keyring_name`

### Launcher map

`game_launchers` maps the account nickname to the launcher path for that same account.

This can be:

- the main `XIVLauncher.exe`
- a `.bat` file that launches XIVLauncher with a custom `--roamingPath`

---

## Example config.json

```json
{
    "DEBUG": false,
    "OTP_LAUNCH_DELAY": 10,
    "OTP_RETRY_INTERVAL": 5,
    "POLL_INTERVAL": 2,
    "GAME_START_TIMEOUT": 3600,
    "GAME_WINDOW_TIMEOUT": 300,
    "CLOSE_GRACE_PERIOD": 15,
    "account_locations": [
        {
            "enabled": true,
            "nickname": "Main",
            "pluginconfigs_path": "C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs",
            "enable_2fa": true,
            "keyring_name": "ffxiv_main_2fa"
        },
        {
            "enabled": true,
            "nickname": "Acc1",
            "pluginconfigs_path": "C:\\Users\\{user}\\AltData\\Acc1\\pluginConfigs",
            "enable_2fa": false,
            "keyring_name": null
        }
    ],
    "game_launchers": {
        "Main": "C:\\Users\\{user}\\AppData\\Local\\XIVLauncher\\XIVLauncher.exe",
        "Acc1": "C:\\Users\\{user}\\AltData\\Acc1.bat"
    }
}
```

---

## What Each Config Field Means

### `pluginconfigs_path`

This should point to the account's `pluginConfigs` folder.

Examples:

- Main account:
  - `C:\Users\YourName\AppData\Roaming\XIVLauncher\pluginConfigs`
- Alt account:
  - `C:\Users\YourName\AltData\Acc1\pluginConfigs`

The script uses this path to derive the account's `launcherConfigV3.json` automatically.

### `enable_2fa`

- `true` if the account requires OTP/2FA
- `false` if the account does not use OTP

### `keyring_name`

The name used to retrieve the OTP secret from Windows Credential Manager.

Examples:

- `ffxiv_main_2fa`
- `ffxiv_acc1_2fa`
- `ffxiv_acc2_2fa`

### `game_launchers`

Each nickname must have a matching launcher entry.

Example:

```json
"game_launchers": {
    "Main": "C:\\Users\\{user}\\AppData\\Local\\XIVLauncher\\XIVLauncher.exe",
    "Acc1": "C:\\Users\\{user}\\AltData\\Acc1.bat"
}
```

### Timing values

- `OTP_LAUNCH_DELAY`
  - How long to wait after starting the launcher before first attempting OTP
- `OTP_RETRY_INTERVAL`
  - How often to retry OTP if XIVLauncher is not ready yet
- `POLL_INTERVAL`
  - Poll interval used while watching for popup, game process, and window state
- `GAME_START_TIMEOUT`
  - Maximum time to wait for `ffxiv_dx11.exe` to appear
- `GAME_WINDOW_TIMEOUT`
  - Maximum time to wait for a visible game window after process launch
- `CLOSE_GRACE_PERIOD`
  - How long to wait for the game to close cleanly before force-closing it

---

## How to Run

From the `FFXIV - Auto-Updater` folder:

```bash
python auto-update.py
```

The script will then process each enabled account in order.

---

## Expected Flow

For each enabled account, the updater will:

1. Validate launcher config
2. Start the configured launcher
3. Wait for XIVLauncher to initialize
4. Send OTP if `enable_2fa` is enabled
5. Detect the **"Out of date"** popup and accept it
6. Wait for a new `ffxiv_dx11.exe` process
7. Wait for a visible **FINAL FANTASY XIV** window
8. Close the game
9. Close any active `DalamudCrashHandler.exe`
10. Move on to the next account

If every account succeeds, the script exits successfully.

If any account fails, the script reports the failed account names and returns a non-zero exit code.

---

## Example output

```text
[ACCOUNT] Starting updater flow for Main
[CONFIG-CHECK] Launcher config OK for Main
[LAUNCH] Launcher started for Main
[2FA] OTP code accepted for Main
[UPDATE] Clicked 'Yes' on the out-of-date popup via Alt+Y
[GAME] Detected launched game process PID 58404 for Main
[GAME] Visible game window detected: FINAL FANTASY XIV
[CLOSE] Game PID 58404 closed cleanly
[ACCOUNT] Update flow completed successfully for Main
```

---

## Troubleshooting

### Launcher not found

**Problem:** The script says the launcher path is missing or invalid.

**Fix:**

- Check the matching entry in `game_launchers`
- Verify the `.exe` or `.bat` file exists
- Make sure the nickname in `account_locations` matches the nickname in `game_launchers`

### Launcher config validation failed

**Problem:** The script cannot validate `launcherConfigV3.json`.

**Fix:**

- Verify `pluginconfigs_path` points to the correct `pluginConfigs` folder
- Make sure the parent folder contains `launcherConfigV3.json`
- Open the JSON file manually to confirm it is not corrupted
- If the profile is brand new, run that launcher manually once first

### 2FA packages missing

**Problem:** A 2FA-enabled account fails immediately.

**Fix:**

Install the OTP-related packages:

```bash
pip install pyotp keyring requests
```

### OTP secret not found

**Problem:** The script cannot find the stored secret for a 2FA account.

**Fix:**

- Confirm the `keyring_name` is correct
- Check Windows Credential Manager for the stored entry
- Re-run your key storage helper if needed
- Make sure the secret was stored under the same Windows user account running the script

### Out-of-date popup was detected but not accepted

**Problem:** The launcher update popup appears, but the script does not successfully continue.

**Fix:**

- Install `pywinauto` to improve WPF popup interaction
- Ensure the popup is not blocked behind another window
- Try again with `DEBUG` enabled in `config.json`
- Verify the popup title is still **"Out of date"** on your system

### Game process never appears

**Problem:** The script times out waiting for `ffxiv_dx11.exe`.

**Fix:**

- Verify the launcher actually logged in successfully
- Increase `GAME_START_TIMEOUT`
- Increase `OTP_LAUNCH_DELAY` if the launcher is slow to initialize
- For 2FA accounts, confirm OTP support is enabled in XIVLauncher

### Game window never becomes visible

**Problem:** The game process launches, but the script times out waiting for a visible window.

**Fix:**

- Increase `GAME_WINDOW_TIMEOUT`
- Check whether the game is opening behind another window
- Confirm the account can launch normally outside of the updater
- Check for a crash handler window or game crash during startup

### Crash handler appears

**Behavior:** If a visible `DalamudCrashHandler.exe` window appears, the script will attempt to close it automatically.

If this keeps happening:

- open the affected launcher/profile manually
- let Dalamud update or repair as needed
- verify the profile can launch normally outside the updater

---

## Differences from the Auto 2FA launcher

`auto-update.py` is different from the standalone `Launch_With_2FA.py` tool.

### `Launch_With_2FA.py`

- launches one account
- focuses on getting into the game with automated OTP
- is meant as a normal convenience launcher

### `auto-update.py`

- processes multiple configured accounts
- handles the **"Out of date"** prompt
- waits for the game to fully open
- closes the game after launch
- is meant for update/maintenance passes

---

## Security Notes

- OTP secrets should be stored in **Windows Credential Manager**, not in plain text inside scripts
- Do not commit secret keys into `config.json`
- Keep each 2FA account's `keyring_name` unique
- Keep your Mogstation emergency removal password stored safely

---

## Support Notes

When diagnosing problems, start with:

- confirming the account can launch manually
- confirming the launcher path is correct
- confirming the profile's `launcherConfigV3.json` exists and is valid
- confirming OTP support is enabled for 2FA accounts
- enabling `DEBUG` in `config.json`

---

## Credits

- **AsunaPahlo**: For paving the way with 2FA implementations in AAR.

---

## Disclaimer

This script is provided as-is for personal use. Use at your own risk. The author is not responsible for account issues, bans, crashes, or data loss resulting from use of this software.

**Important:** Using automation tools may violate the FFXIV Terms of Service. Use responsibly and understand the risks.
