# Launch FFXIV With Automated 2FA - Standalone Launcher

**Quick launcher for FFXIV with automatic Two-Factor Authentication**

A simple standalone script that opens XIVLauncher and automatically sends your 2FA/OTP code. Perfect for quickly launching the game without running the full Auto-AutoRetainer automation suite.

---

## What Does This Script Do?

- Opens your configured XIVLauncher (main account or alt account)
- Waits for the launcher to initialize
- Automatically generates a one-time password (OTP) from your stored secret key
- Sends the OTP code to XIVLauncher via its API
- Launches your game without manual 2FA entry

---

## Prerequisites

**Required Packages:**
```bash
pip install pyotp keyring requests
```

**Required Setup:**
- Windows operating system
- XIVLauncher with Dalamud installed
- Your Square Enix account with 2FA enabled
- Your OTP secret key stored in Windows Credential Manager (see setup instructions below)

---

## Creating Alternative Dalamud Launchers for Alt Accounts (Optional)

If you only have one FFXIV account, skip this section and [start here](#complete-2fa-setup-guide).

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

**Note:** When you first log in with your alt launcher, it will show your previously logged-in account info. Simply enter your alt account credentials and they'll be saved for future launches. Make sure you hit tab after entering your username and password. If you just type your password and press enter it will not save the updated password.

---

### Launcher Path Examples

#### Main Account (Default XIVLauncher)

```python
LAUNCHER_PATH = rf"C:\Users\{user}\AppData\Local\XIVLauncher\XIVLauncher.exe"
LAUNCHER_CONFIG_PATH = rf"C:\Users\{user}\AppData\Roaming\XIVLauncher\launcherConfigV3.json"
```

#### Alt Accounts (Batch File Launchers)

```python
# For Acc1
LAUNCHER_PATH = rf"C:\Users\{user}\AltData\Acc1.bat"
LAUNCHER_CONFIG_PATH = rf"C:\Users\{user}\AltData\Acc1\launcherConfigV3.json"

# For Acc2
LAUNCHER_PATH = rf"C:\Users\{user}\AltData\Acc2.bat"
LAUNCHER_CONFIG_PATH = rf"C:\Users\{user}\AltData\Acc2\launcherConfigV3.json"
```

### Benefits

- ✓ No manual credential switching
- ✓ Separate plugin configurations per account
- ✓ No plugin conflicts between accounts
- ✓ Independent 2FA settings per account
- ✓ Clean separation of account data

---

## Complete 2FA Setup Guide

### ⚠️ Important Notes Before Starting

- **If your account already has 2FA enabled**, you must disable it first and re-enable it following these instructions
- **Do NOT navigate away** from the Mogstation during the key registration process - this will regenerate a new key
- **Keep your emergency removal password** in case you lose access to your authenticator

---

## Step 1: Disable Existing 2FA (If Applicable)

If your account already has 2FA enabled:
1. Log into your Square Enix account
2. Navigate to One-Time Password settings
3. Remove/disable the existing authenticator
4. Proceed to Step 2 once 2FA is fully disabled

---

## Step 2: Get Your Authentication Key

**⚠️ Critical:** Do not click the back button or navigate away during this process - doing so will regenerate a new key and invalidate the one you copied.

1. Log into your account on the [Mogstation website](https://www.mogstation.com)
2. Navigate to: https://secure.square-enix.com/account/app/svc/otpTop
3. Click on **"Software Authenticator"** option
4. Click **"Software Authenticator Registration"**
5. On the next page, you'll see a QR code - **do not scan it**
6. Click **"Unable to Scan QR Code"**
7. The next page will display your **Authentication Key** - this is the secret key you need
8. **Copy this key into a Notepad document** and remove any spaces from it

   **Example format:**
   ```
   ABCD EFGH IJKL MNOP QRST UVWX YZ12 3456
   ```
   
   **Remove spaces to get:**
   ```
   ABCDEFGHIJKLMNOPQRSTUVWXYZ123456
   ```

9. Open your phone's authenticator app (Google Authenticator, Authy, Microsoft Authenticator, etc.)
10. Choose "Add account" or "Enter manually"
11. Enter the following:
    - **Code Name:** FFXIV (or whatever you prefer)
    - **Your Key:** Paste the key with no spaces
    - **Type of key:** Time based
12. Click **Add** - your phone will now generate 6-digit codes
13. On the Mogstation site, press **Next** and enter the 2FA code your phone provides
14. It should now say you are set up for 2FA
15. Relog into Mogstation and it should show your **Emergency Removal Password** - **save this securely** (use this password to remove 2FA if you lose or damage your phone)

---

## Step 3: Configure XIVLauncher for 2FA

### Enable Main Launcher Settings

1. Open XIVLauncher
   - If your game auto-logs in, **hold SHIFT** when clicking your launcher icon to force it to open

2. On the main launcher window, enable the following:
   - ✅ **"Log in automatically"**
   - ✅ **"Use One-Time-Passwords"**

### Enable OTP Macro Support in Settings

3. In XIVLauncher, click on the **settings gear icon**

4. Navigate to the **main game tab**

5. Enable the following setting:
   - ✅ **"Enable XL Authenticator app/OTP macro support"**

6. Click the **Save checkmark**

7. Ensure all three settings are now enabled:
   - "Log in automatically" (main launcher window)
   - "Use One-Time-Passwords" (main launcher window)
   - "Enable XL Authenticator app/OTP macro support" (settings → game tab)

8. Close the launcher

### Test Manual Login (First Time)

1. Open XIVLauncher again
2. Enter your 2FA code from your phone
3. Verify you can log into the game successfully
4. Close the game

**⚠️ First Login Note:** The FIRST time you attempt to use the OTP macro support, you may get a Windows environment popup asking for permissions. If this happens, allow the permissions, then cancel the OTP window and try again if nothing happens.

---

## Step 4: Store the OTP Secret in Windows

Now you'll store your authentication key securely in Windows Credential Manager so the script can access it.

### Using Set_2FA_Key.py

1. Locate the `Set_2FA_Key.py` file in the same folder as this README

2. Open `Set_2FA_Key.py` in a text editor (Notepad, VS Code, etc.)

3. Configure the following values:

   ```python
   # Give your key a unique name (e.g., "ffxiv_main_2fa", "ffxiv_acc1_2fa")
   keyring_name = "ffxiv_main_2fa"

   # Paste your authentication key here (with spaces removed)
   secret_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"
   ```

4. **Save the file**

5. Run the script:
   ```bash
   python Set_2FA_Key.py
   ```

6. The window will flash and close quickly - this is normal
   - **Do NOT run it twice** - once is enough

7. **Verify the key was stored:**
   - Open **"Credential Manager"** in Windows (search for it in Start menu)
   - Click **"Windows Credentials"** at the top
   - Look for your key under **"Generic Credentials"**
   - You should see an entry matching your `keyring_name`

8. **Security Best Practice:**
   - After confirming the key works, **delete the secret_key value** from `Set_2FA_Key.py`
   - Leaving it in plain text is a security risk
   - The key is now safely stored in Windows Credential Manager

**Note:** Each FFXIV account with 2FA needs its own unique keyring name (e.g., "ffxiv_main_2fa", "ffxiv_acc1_2fa", "ffxiv_acc2_2fa").

---

## Step 5: Configure Launch_With_2FA.py

Open `Launch_With_2FA.py` in a text editor and configure the settings:

### Configuration Section

```python
# Account nickname to launch
ACCOUNT_NICKNAME = "Main"

# Launcher path for the account
# For main account: C:\Users\{user}\AppData\Local\XIVLauncher\XIVLauncher.exe
# For alt accounts: C:\Users\{user}\AltData\Acc1.bat
LAUNCHER_PATH = rf"C:\Users\{user}\AppData\Local\XIVLauncher\XIVLauncher.exe"

# 2FA Configuration
ENABLE_2FA = True                    # Set to True to send OTP code automatically
KEYRING_NAME = "ffxiv_main_2fa"      # Name of the keyring entry (must match Step 4)

# Launcher Config Path (launcherConfigV3.json location)
# For main account: C:\Users\{user}\AppData\Roaming\XIVLauncher\launcherConfigV3.json
# For alt accounts: C:\Users\{user}\AltData\Acc1\launcherConfigV3.json
LAUNCHER_CONFIG_PATH = rf"C:\Users\{user}\AppData\Roaming\XIVLauncher\launcherConfigV3.json"

# Timing
OTP_LAUNCH_DELAY = 10                # Seconds to wait before sending OTP (not recommended below 10)
```

### Configuration for Alt Accounts

If you're using an alt account with a batch file launcher:

```python
ACCOUNT_NICKNAME = "Acc1"
LAUNCHER_PATH = rf"C:\Users\{user}\AltData\Acc1.bat"
ENABLE_2FA = True
KEYRING_NAME = "ffxiv_acc1_2fa"
LAUNCHER_CONFIG_PATH = rf"C:\Users\{user}\AltData\Acc1\launcherConfigV3.json"
OTP_LAUNCH_DELAY = 10
```

---

## Step 6: Run the Launcher

1. Open a command prompt or PowerShell in the script folder or run the script directly and proceed to step 3.

2. Run the script:
   ```bash
   python Launch_With_2FA.py
   ```

3. The script will:
   - Validate your launcher configuration (checks AutologinEnabled and OtpServerEnabled settings)
   - Launch XIVLauncher
   - Wait 10 seconds (or your configured delay)
   - Automatically send your 2FA code
   - Launch the game

4. If successful, you should see output like:
   ```
   [CONFIG-CHECK] Launcher config OK (AutologinEnabled=true, OtpServerEnabled=true)
   [LAUNCH] Starting launcher for Main...
   [LAUNCH] Executable launcher started: C:\Users\...\XIVLauncher.exe
   [2FA] Waiting 10 seconds for launcher to initialize...
   [2FA] Sending OTP code to XIVLauncher...
   [2FA] OTP code accepted!
   [LAUNCH] Complete!
   ```

---

## Timing Configuration

### OTP_LAUNCH_DELAY Setting

The `OTP_LAUNCH_DELAY` controls how long the script waits after launching XIVLauncher before sending the OTP code.

**Default:** 10 seconds
**Minimum Recommended:** 10 seconds

**Why the delay matters:**
- XIVLauncher needs time to start up and initialize its API server
- If the code is sent too early, the launcher won't be ready to receive it
- If you get "Failed to send OTP code" errors, increase this value

**Tuning recommendations:**
- **Fast system:** 5-8 seconds may work
- **Average system:** 10 seconds is safe
- **Slow system or HDD:** 15+ seconds recommended
- **Alt accounts with batch files:** May need 12-15 seconds

**Testing your delay:**
1. Start with 10 seconds
2. If the OTP is sent too early (launcher not ready), increase by 5 seconds
3. If everything works, you can try reducing by 2-3 seconds for faster launches

---

## Troubleshooting

### OTP Code Rejected

**Problem:** The script sends the code but XIVLauncher doesn't accept it.

**Solutions:**
- Ensure your system clock is accurate (OTP codes are time-based)
- Verify the authentication key was copied correctly without extra spaces
- Check that the `KEYRING_NAME` in the script matches what you set in `Set_2FA_Key.py`
- Try generating a code on your phone and verify it works manually first

### Code Sent Too Early

**Problem:** Script says "Failed to send OTP code" or "Connection refused"

**Solutions:**
- Increase `OTP_LAUNCH_DELAY` to give the launcher more time to start
- Try 15-20 seconds if you have a slower system
- Make sure XIVLauncher is not already running when you start the script

### "Keyring not found" Error

**Problem:** Script can't find your stored OTP secret.

**Solutions:**
- Run `Set_2FA_Key.py` again to store the key
- Verify the `KEYRING_NAME` matches exactly (case-sensitive)
- Check Windows Credential Manager to confirm the entry exists
- Make sure you're using the same Windows user account that stored the key

### Key Became Invalid

**Problem:** The code no longer works, but it worked before.

**Solutions:**
- If you navigated away during Mogstation registration, the key was regenerated
- Disable 2FA on your account and start over from Step 2
- Make sure your phone's authenticator still has the correct entry

### Launcher Opens But Nothing Happens

**Problem:** XIVLauncher opens but no OTP code is sent.

**Solutions:**
- Verify `ENABLE_2FA = True` in the script
- Check that `OtpServerEnabled` is enabled in XIVLauncher settings
- Try running XIVLauncher manually and test the API:
  - Open a browser and go to: `http://localhost:4646/ffxivlauncher/123456`
  - If it says "Waiting for XIVLauncher", the API is working
- Verify the launcher config path is correct for your account type (main vs alt)

### Launcher Config Validation Failed

**Problem:** Script says "Launcher config validation failed"

**Solutions:**
- Check that `LAUNCHER_CONFIG_PATH` points to the correct `launcherConfigV3.json` file
- Verify the JSON file exists and is not corrupted
- Try opening the file in a text editor to check for syntax errors
- Let the script run anyway - it will create the config on first launch

---

## Security Considerations

### What This Script Stores

- Your OTP secret key is stored in **Windows Credential Manager** (encrypted by Windows)
- The secret is never stored in plain text in any script file (after initial setup)
- No passwords or login credentials are stored by this script

### Best Practices

1. **Delete the secret from Set_2FA_Key.py** after storing it successfully
2. **Keep your emergency removal password** in a secure location (password manager)
3. **Don't share** your authentication key or keyring with anyone
4. **Back up** your emergency removal password before storing the key in Windows
5. **Test your phone authenticator** before relying solely on the automated script

### If You Lose Access

If you lose access to both your phone authenticator AND the Windows-stored key:
1. Use your **Emergency Removal Password** from Mogstation to disable 2FA
2. Re-enable 2FA following the setup instructions from Step 2
3. Store the new key using `Set_2FA_Key.py`

---

## Creating Multiple Launchers

You can create multiple copies of `Launch_With_2FA.py` for different accounts:

### Example Setup

**Main Account Launcher (Launch_Main_2FA.py):**
```python
ACCOUNT_NICKNAME = "Main"
LAUNCHER_PATH = rf"C:\Users\{user}\AppData\Local\XIVLauncher\XIVLauncher.exe"
KEYRING_NAME = "ffxiv_main_2fa"
LAUNCHER_CONFIG_PATH = rf"C:\Users\{user}\AppData\Roaming\XIVLauncher\launcherConfigV3.json"
```

**Alt Account Launcher (Launch_Acc1_2FA.py):**
```python
ACCOUNT_NICKNAME = "Acc1"
LAUNCHER_PATH = rf"C:\Users\{user}\AltData\Acc1.bat"
KEYRING_NAME = "ffxiv_acc1_2fa"
LAUNCHER_CONFIG_PATH = rf"C:\Users\{user}\AltData\Acc1\launcherConfigV3.json"
```

### Desktop Shortcuts

Create desktop shortcuts for easy access:
1. Right-click on your desktop → New → Shortcut
2. For the location, enter:
   ```
   python.exe "C:\path\to\Launch_With_2FA.py"
   ```
3. Name it "Launch FFXIV (Main)" or similar
4. Click Finish

**Advanced:** Create a `.bat` file wrapper: (optional, can just run the python script)
```batch
@echo off
cd /d "C:\path\to\script\folder"
python Launch_With_2FA.py
pause
```

---

## Differences from Auto-AutoRetainer

This standalone launcher is a simplified version extracted from the full Auto-AutoRetainer automation suite.

### What This Script Does NOT Do

- ❌ Monitor submarine timers
- ❌ Automatically close games when idle
- ❌ Recover from crashes
- ❌ Manage multiple accounts simultaneously
- ❌ Arrange game windows
- ❌ Send notifications

### What This Script DOES Do

- ✅ Launch XIVLauncher
- ✅ Automatically send 2FA codes
- ✅ Validate launcher configuration
- ✅ Support both main and alt account launchers

### When to Use This vs Auto-AutoRetainer

**Use Launch_With_2FA.py when:**
- You want to manually launch the game with automatic 2FA
- You don't need full automation
- You want a quick launcher for a specific account

**Use Auto-AutoRetainer when:**
- You want full submarine automation
- You need crash recovery and monitoring
- You want multi-account management
- You need 24/7 operation with automatic restarts

---

## Additional Resources

### OTP/2FA Resources

- pyotp Documentation: https://pyauth.github.io/pyotp/
- Windows Credential Manager: Built into Windows (search "Credential Manager" in Start menu)

---

## Support

For issues specific to this launcher:
1. Check the Troubleshooting section above
2. Verify all prerequisites are installed correctly
3. Test your 2FA setup manually with XIVLauncher first
4. Check that your OTP secret is stored correctly in Windows Credential Manager

---

## Credits

- **AsunaPahlo**: For paving the way with 2FA implementations in AAR.

---

## Disclaimer

This script is provided as-is for personal use. Use at your own risk. The author is not responsible for any account issues, bans, or data loss resulting from the use of this software.

**Important:** Using automation tools may violate the FFXIV Terms of Service. Use responsibly and understand the risks.

## Version History

**v1.00** (2026-01-19) - Initial release - Standalone 2FA launcher extracted from Auto-AutoRetainer
