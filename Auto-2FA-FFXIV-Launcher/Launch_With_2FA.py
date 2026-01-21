########################################################################################################################
#
#  ██╗      █████╗ ██╗   ██╗███╗   ██╗ ██████╗██╗  ██╗    ██╗    ██╗██╗████████╗██╗  ██╗    ██████╗ ███████╗ █████╗ 
#  ██║     ██╔══██╗██║   ██║████╗  ██║██╔════╝██║  ██║    ██║    ██║██║╚══██╔══╝██║  ██║    ╚════██╗██╔════╝██╔══██╗
#  ██║     ███████║██║   ██║██╔██╗ ██║██║     ███████║    ██║ █╗ ██║██║   ██║   ███████║     █████╔╝█████╗  ███████║
#  ██║     ██╔══██║██║   ██║██║╚██╗██║██║     ██╔══██║    ██║███╗██║██║   ██║   ██╔══██║    ██╔═══╝ ██╔══╝  ██╔══██║
#  ███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╗██║  ██║    ╚███╔███╔╝██║   ██║   ██║  ██║    ███████╗██║     ██║  ██║
#  ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝     ╚══╝╚══╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝    ╚══════╝╚═╝     ╚═╝  ╚═╝
#
# Standalone FFXIV Launcher with Automatic 2FA
#
# A simple standalone script that opens XIVLauncher and automatically sends the 2FA/OTP code.
# Useful for quickly launching the game with one-time password authentication without running the full automation suite.
#
# Core Features:
# • Opens configured game launcher (XIVLauncher.exe or batch file)
# • Automatically generates and sends OTP code via XIVLauncher API
# • Supports both direct .exe and .bat launcher files
# • Retrieves OTP secret securely from Windows Credential Manager
#
# Important Note: Requires pyotp, keyring, and requests packages. Your OTP secret must be stored using Set_2FA_Key.py
# before this script will work. XIVLauncher must have "Enable XL Authenticator app/OTP macro support" enabled.
#
# Launch With 2FA v1.00
# Standalone FFXIV Launcher with Automatic 2FA
# Created by: https://github.com/xa-io
# Last Updated: 2026-01-19 21:50:00
#
# ## Release Notes ##
#
# v1.00 - Initial release - Standalone 2FA launcher extracted from Auto-AutoRetainer
#
########################################################################################################################

###########################################
#### Start of Configuration Parameters ####
###########################################

import os
import sys
import time
import json
import getpass
import subprocess
from pathlib import Path

# Required packages for 2FA
try:
    import pyotp
    import keyring
    import requests
    PYOTP_AVAILABLE = True
except ImportError:
    PYOTP_AVAILABLE = False
    print("[ERROR] Required packages not installed!")
    print("[ERROR] Install with: pip install pyotp keyring requests")
    input("Press Enter to exit...")
    sys.exit(1)

# ===============================================
# Configuration
# ===============================================
user = getpass.getuser()

# Account nickname to launch
ACCOUNT_NICKNAME = "Main"

# Launcher path for the account
# For main account: C:\Users\{user}\AppData\Local\XIVLauncher\XIVLauncher.exe
# For alt accounts: C:\Users\{user}\AltData\Acc1.bat
LAUNCHER_PATH = rf"C:\Users\{user}\AppData\Local\XIVLauncher\XIVLauncher.exe"

# 2FA Configuration
ENABLE_2FA = True                    # Set to True to send OTP code automatically
KEYRING_NAME = "ffxiv_main_2fa"      # Name of the keyring entry storing your OTP secret (set via Set_2FA_Key.py)

# Launcher Config Path (launcherConfigV3.json location)
# For main account: C:\Users\{user}\AppData\Roaming\XIVLauncher\launcherConfigV3.json
# For alt accounts: C:\Users\{user}\AltData\Acc1\launcherConfigV3.json
LAUNCHER_CONFIG_PATH = rf"C:\Users\{user}\AppData\Roaming\XIVLauncher\launcherConfigV3.json"

# Timing
OTP_LAUNCH_DELAY = 5                # Seconds to wait after launching before sending OTP (not recommended below 10)

#########################################
#### End of Configuration Parameters ####
#########################################


def validate_launcher_config():
    """
    Validate and fix launcher configuration BEFORE launching game.
    Checks launcherConfigV3.json and ensures:
    1. AutologinEnabled is "true" (always)
    2. OtpServerEnabled is "true" (if ENABLE_2FA is True)
    
    Returns True if config is valid (or was fixed), False if critical error.
    """
    config_path = Path(LAUNCHER_CONFIG_PATH)
    
    if not config_path.exists():
        print(f"[CONFIG-CHECK] Launcher config not found: {config_path}")
        print(f"[CONFIG-CHECK] Continuing anyway - launcher may create it on first run")
        return True
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        config_updated = False
        
        # Check and fix AutologinEnabled
        autologin_value = data.get("AutologinEnabled", None)
        if autologin_value != "true":
            old_value = autologin_value
            data["AutologinEnabled"] = "true"
            config_updated = True
            print(f"[CONFIG-CHECK] Fixed AutologinEnabled: '{old_value}' -> 'true'")
        
        # Check and fix OtpServerEnabled (only if 2FA is enabled)
        if ENABLE_2FA:
            otp_value = data.get("OtpServerEnabled", None)
            if otp_value != "true":
                old_value = otp_value
                data["OtpServerEnabled"] = "true"
                config_updated = True
                print(f"[CONFIG-CHECK] Fixed OtpServerEnabled: '{old_value}' -> 'true'")
        
        # Write back if changes were made
        if config_updated:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"[CONFIG-CHECK] Launcher config updated successfully")
        else:
            print(f"[CONFIG-CHECK] Launcher config OK (AutologinEnabled=true, OtpServerEnabled=true)")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"[CONFIG-CHECK] Error parsing launcher config JSON: {e}")
        return False
    except Exception as e:
        print(f"[CONFIG-CHECK] Error checking launcher config: {e}")
        return False


def launch_game():
    """
    Launch the game and send 2FA code if enabled.
    """
    # Validate launcher config first
    if not validate_launcher_config():
        print(f"[ERROR] Launcher config validation failed - aborting launch")
        return False
    
    print(f"[LAUNCH] Starting launcher for {ACCOUNT_NICKNAME}...")
    
    if not os.path.exists(LAUNCHER_PATH):
        print(f"[ERROR] Launcher not found: {LAUNCHER_PATH}")
        return False
    
    try:
        # Check if it's a batch file
        is_batch_file = LAUNCHER_PATH.lower().endswith('.bat')
        
        if is_batch_file:
            # For batch files, use cmd.exe with /c to close CMD after execution
            subprocess.Popen(
                f'start "" /B "{LAUNCHER_PATH}"',
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            print(f"[LAUNCH] Batch file launcher started: {LAUNCHER_PATH}")
        else:
            # For executables, use normal Popen
            subprocess.Popen(
                [LAUNCHER_PATH],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            print(f"[LAUNCH] Executable launcher started: {LAUNCHER_PATH}")
        
        # Handle 2FA if enabled
        if ENABLE_2FA:
            if not KEYRING_NAME:
                print(f"[WARNING] 2FA enabled but no KEYRING_NAME specified - skipping OTP")
                return True
            
            # Wait for launcher to initialize
            print(f"[2FA] Waiting {OTP_LAUNCH_DELAY} seconds for launcher to initialize...")
            time.sleep(OTP_LAUNCH_DELAY)
            
            # Get OTP secret from keyring
            otp_secret = keyring.get_password(KEYRING_NAME, "otp_secret")
            if not otp_secret:
                print(f"[ERROR] OTP secret not found in keyring '{KEYRING_NAME}'")
                print(f"[ERROR] Please run Set_2FA_Key.py to store your OTP secret first")
                return False
            
            # Generate OTP code
            totp = pyotp.TOTP(otp_secret)
            code = totp.now()
            url = f"http://localhost:4646/ffxivlauncher/{code}"
            
            print(f"[2FA] Sending OTP code to XIVLauncher...")
            try:
                resp = requests.get(url, timeout=5)
                resp.raise_for_status()
                
                if resp.status_code == 200:
                    print(f"[2FA] OTP code accepted!")
                else:
                    print(f"[2FA] Unexpected response: {resp.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"[2FA] Failed to send OTP code: {e}")
                print(f"[2FA] You may need to enter the code manually")
                return False
        
        print(f"[LAUNCH] Complete!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to launch game: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("  Launch With 2FA - Standalone FFXIV Launcher")
    print("=" * 60)
    print()
    
    success = launch_game()
    
    print()
    if success:
        print("[DONE] Script completed successfully.")
    else:
        print("[DONE] Script completed with errors.")
