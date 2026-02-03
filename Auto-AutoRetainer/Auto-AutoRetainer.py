########################################################################################################################
#
#   █████╗ ██╗   ██╗████████╗ ██████╗        █████╗ ██╗   ██╗████████╗ ██████╗ ██████╗ ███████╗████████╗ █████╗ ██╗███╗   ██╗███████╗██████╗ 
#  ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗      ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║████╗  ██║██╔════╝██╔══██╗
#  ███████║██║   ██║   ██║   ██║   ██║█████╗███████║██║   ██║   ██║   ██║   ██║██████╔╝█████╗     ██║   ███████║██║██╔██╗ ██║█████╗  ██████╔╝
#  ██╔══██║██║   ██║   ██║   ██║   ██║╚════╝██╔══██║██║   ██║   ██║   ██║   ██║██╔══██╗██╔══╝     ██║   ██╔══██║██║██║╚██╗██║██╔══╝  ██╔══██╗
#  ██║  ██║╚██████╔╝   ██║   ╚██████╔╝      ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║  ██║███████╗   ██║   ██║  ██║██║██║ ╚████║███████╗██║  ██║
#  ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝       ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
#
# Automated FFXIV Submarine Management System
#
# A comprehensive automation script that monitors submarine return times across multiple FFXIV accounts and intelligently
# manages game instances for hands-off submarine and retainer farming. Automatically launches games when submarines are ready,
# handles 2FA login, recovers from crashes and frozen clients, enforces stability restarts, tracks daily gil earnings and supply 
# levels, and closes games when idle, all without manual intervention.
#
# Core Features:
# • Real-time submarine timer monitoring across all configured accounts
# • Automatic game launching when submarines are nearly ready (configurable threshold)
# • Automatic game closing when submarines won't be ready soon (prevents idle instances)
# • Two-factor authentication (2FA/OTP) support with automatic code submission
# • Crash recovery with automatic game relaunch when clients close unexpectedly
# • Frozen client detection and force-crash after configurable inactivity period
# • 72-hour stability protection with automatic restart at MAX_RUNTIME (71 hours)
# • Supply level monitoring with restocking alerts for Ceruleum tanks and Repair Kits
# • Gil earnings and supply cost calculations based on submarine builds and routes
# • Multi-account support with flexible modes (submarine-only, 24/7 uptime, or both)
# • Intelligent window arrangement with customizable layouts
# • External configuration via config.json with notification support (Pushover/Discord)
#
# Important Note: This script requires properly configured game launchers (XIVLauncher.exe or batch files), game windows
# labeled with "ProcessID - nickname" format, autologin enabled, and AutoRetainer multi-mode auto-enabled
# for full automation. 2FA is supported via keyring integration. See README.md for complete setup instructions.
#
# Auto-AutoRetainer v1.31
# Automated FFXIV Submarine Management System
# Created by: https://github.com/xa-io
# Last Updated: 2026-01-31 10:30:00
#
# ## Release Notes ##
#
# v1.31 - Added config.json support for custom submarine plans, build rates, and supply costs
#         NEW CONFIG OPTIONS:
#         - submarine_plans: Configure leveling plan names and farming plans with daily earnings
#         - build_gil_rates: Add custom submarine builds not in the default list with gil/day
#         - build_consumption_rates: Add custom builds with tanks_per_day and kits_per_day
#         - ceruleum_tank_cost: Override default Ceruleum Tank cost (default: 350 gil)
#         - repair_kit_cost: Override default Repair Kit cost (default: 2000 gil)
# v1.30 - Added force-crash timer display in status output (X:xx format after UPTIME)
#         Shows minutes remaining before force-crash will trigger for each running client
#         Timer adapts to retainer mode (20min) or submarine mode (10min) threshold
#         Added script-crash reporting, can be used to report any script issues back to me.
#         Added notifications to be sent if the script crashes, and stop functioning.
# v1.29 - Fixed premature force-crash timer switch from retainer (20min) to submarine (10min) mode
#         When subs become ready while retainer processing is active, timer now stays at 20min
#         Timer only switches to 10min after actual submarine processing is detected
#         Added retainer_mode_active tracking dictionary to preserve timer mode during transitions
#         Prevents false force-crashes when GC turn-ins take longer than 10 minutes after subs become ready
#         Enhanced debug logging shows when timer mode is preserved during sub-ready transitions
# v1.28 - Added "Lowest Inventory Space (Sub-Only Farmers)" display line in terminal output
#         Added "Lowest Inventory Space (Retainer Farmers)" display line for characters with retainers
#         Added retainer readiness tracking and display for force247uptime accounts:
#         - When force247uptime=True and no subs ready but retainers ready, shows "(xx Ret.)" instead of "(WAITING)"
#         - When all retainers on ventures, shows return timer in minutes (e.g., "+17min" or "xx Ret.")
#         - Counts ready retainers (completed ventures) and total retainers on ventures
#         Added smart retainer processing detection similar to submarine tracking:
#         - Resets force-crash inactivity timer when retainers are processed
#         - Keeps monitoring active when force247uptime accounts have ready retainers
#         - Monitoring activates immediately when retainers are ready (no threshold delay)
#         Added FORCE_CRASH_RETAINER_MINUTES = 20 (separate from 10-min submarine timer)
#         - Longer timeout for retainer processing due to GC turn-ins after retainer ventures
#         Added force-crash notifications via Pushover/Discord when client is crashed
#         Added detect_retainer_processing() function with timer change detection
# v1.27 - Fixed batch file launcher leaving cmd.exe processes running after game launch
#         Added cleanup_batch_launcher_processes() to terminate lingering cmd.exe processes
#         Changed batch file launch from 'start /B' to direct cmd.exe /c execution
#         Added post-launch cleanup delay and process termination for batch file launchers
#         Batch files now properly close their cmd.exe shells after launching the game
# v1.26 - Added initial startup launcher check to close any stuck XIVLauncher on bootup
#         Code consolidation: Created generic helper functions to reduce redundant code
#         New helpers: kill_process_by_image_name(), is_process_running_with_visible_windows(),
#                      kill_game_client_and_cleanup(), get_process_start_time_by_name()
#         Refactored 11 process functions to use generic helpers for consistency
# v1.25 - Added pre-launch config validation for AutologinEnabled and OtpServerEnabled
#         Checks launcherConfigV3.json BEFORE launching game (not just after failures)
#         Automatically fixes AutologinEnabled to "true" if not set correctly
#         Automatically fixes OtpServerEnabled to "true" when account has enable_2fa=True
#         Prevents launcher from opening with login prompt instead of auto-logging in
#         Added validate_launcher_config_before_launch() function for pre-launch checks
#         Existing launcher stuck detection continues to close XIVLauncher if it gets stuck
# v1.24 - Added external configuration file support (config.json)
#         Settings can now be configured via config.json instead of editing the Python script
#         Any setting not in config.json falls back to built-in script defaults
#         Added 2FA/OTP support for accounts with two-factor authentication enabled
#         Automatically generates and sends OTP codes when launching games via XIVLauncher API
#         OTP secrets stored securely in Windows Credential Manager via keyring
#         Added OtpServerEnabled auto-fix: checks launcherConfigV3.json when 2FA enabled and launcher fails
#         Added Pushover notification support for logged issues (sends push to phone)
#         Added Discord webhook notification support for logged issues (sends to Discord channel)
#         Notification validation: halts script if enabled but credentials missing
#         Added OTP_LAUNCH_DELAY setting to control timing of OTP code submission
#         Added config.json.example with all settings documented
# v1.23 - Critical bug fix: Window title failure no longer kills all running game clients
#         In multi-client mode, failing to launch one account no longer closes other running games
#         Added ENABLE_AUTOLOGIN_UPDATER to auto-fix launcher config when game fails to open
#         Checks launcherConfigV3.json and updates AutologinEnabled from "false" to "true" before retry
#         Runs autologin check after launcher fail 1/3 and 2/3 (two chances to fix before final failure)
#         Added ENABLE_LOGGING and arr.log file for tracking major issues (17 logged events)
#         Logs process kills, game launches, config errors, window crashes, autologin updates, and launcher failures
#         Multi-client mode continues normal rotation when window title check fails
#         Game client checker retries failed accounts in WINDOW_REFRESH_INTERVAL (60) seconds
# v1.22 - Added robust window movement with retry logic and responsiveness checking
#         Implemented is_window_responding() to detect frozen windows before move attempts
#         Added MAX_WINDOW_MOVE_ATTEMPTS = 3 configuration for retry logic per window
#         Window position verification now only checks x,y coordinates (FFXIV controls own size via graphics settings)
#         Up to 3 move attempts per window with 1-second verification delay between attempts
#         Script skips unresponsive windows instead of freezing, continues processing remaining windows
#         Failed windows tracked separately with detailed failure reasons in debug output
#         Enhanced move_window_to_position() with MoveWindow API for reliable positioning
#         WINDOW_MOVE_VERIFICATION_DELAY = 1 second (reduced from 3 for faster processing)
#         Added MAX_FAILED_FORCE_CRASH = True to automatically crash clients after failed window moves
#         Failed clients will be relaunched on next cycle if they should be running (similar to inactivity timer)
#         Extracts PID from window title and force crashes using kill_process_by_pid()
#         Prevents script freeze when game clients become unresponsive during window arrangement
# v1.21 - Disabled force-close monitoring when all submarines are voyaging (idle state)
#         Force-close monitoring now only runs when ready_subs > 0 or account is in (WAITING) state
#         When all subs are voyaging with 0 ready (showing +hours without status), monitoring is disabled
#         Prevents false-positive crashes for force247uptime accounts idle between voyage completions
#         Monitoring activates when subs become ready, deactivates when all subs sent out
#         Ensures force-close only monitors accounts with actual work to process
# v1.20 - Enhanced force-close timer to extend when accounts are in (WAITING) state
#         Force-close inactivity timer now resets when game is in (WAITING) status
#         (WAITING) occurs when game is running with 0 ready subs and hours <= AUTO_CLOSE_THRESHOLD
#         Timer extension prevents force-close during legitimate wait periods (up to 0.5h default)
#         Inactivity timer resets on each scan when (WAITING) is active, similar to submarine processing
#         Ensures force-close only triggers for frozen/stuck clients, not idle waiting states
# v1.19 - Fixed force-crash monitoring to respect ENABLE_AUTO_CLOSE setting
#         Force-crash inactivity monitoring now only runs when ENABLE_AUTO_CLOSE = True
#         When ENABLE_AUTO_CLOSE = False, clients will never be force-closed due to inactivity
#         Resolves issue where frozen client detection would crash clients even when auto-close was disabled
#         Ensures user control over client lifecycle when auto-close features are not desired
# v1.18 - Improved Force-Close timer to start when game launches instead of when subs are processed
#         Force-Close monitoring now starts AUTO_LAUNCH_THRESHOLD minutes after game opens (matches game launch threshold)
#         Crash timer begins even if game boots stuck without processing any submarines (resolves stuck-at-boot issue)
#         After AUTO_LAUNCH_THRESHOLD delay, FORCE_CRASH_INACTIVITY_MINUTES timer activates (default: 10 minutes)
#         Timer still resets whenever submarines are processed (preserves existing behavior during active play)
#         Game launch timestamp tracked per account to determine when monitoring should activate
#         Eliminates issue where frozen games at boot would never trigger force-close because no subs were processed
# v1.17 - Added DalamudCrashHandler.exe detection and automatic closing
#         Monitors for active DalamudCrashHandler.exe windows (indicates game crash) every WINDOW_REFRESH_INTERVAL
#         Distinguishes between active crash handler windows (problem state) and background processes (normal state)
#         Automatically closes crash handler windows when detected to prevent user intervention requirement
#         Uses same detection methodology as XIVLauncher.exe check (has_visible_windows function)
#         Logs crash handler detection and closure status for visibility
# v1.16 - Added launcher detection with automatic retry and system bootup delay features
#         FORCE_LAUNCHER_RETRY = 3 attempts when XIVLauncher.exe opens as ACTIVE APP instead of game client
#         Detects XIVLauncher with visible windows (stuck at login screen) during game startup monitoring
#         Ignores XIVLauncher as background process (normal state when game running) to prevent false positives
#         Uses win32gui window enumeration to distinguish active launcher UI from background process
#         Kills launcher and retries game launch up to FORCE_LAUNCHER_RETRY times before marking account as [LAUNCHER]
#         Single client mode: stops monitoring account after max retries (script continues but won't launch)
#         Multi-client mode: marks failed account as [LAUNCHER] and continues processing other accounts
#         SYSTEM_BOOTUP_DELAY (configurable delay before script starts monitoring)
#         Shows countdown "ARR Processing Delay {x}s Set. Please Wait..." when delay is configured
#         Useful for auto-starting script on system boot (e.g., set to 20 for 20 second delay)
#         Enhanced wait_for_window_title_update() to detect launcher during both single and multi-client modes
# v1.15 - Enhanced submarine processing detection and added FORCE_CRASH_TIMER for frozen client detection
#         Submarine processing now accurately tracks subs sent per scan by counting decrease in ready submarines
#         Processing count = (previous ready count - current ready count) - eliminates false positives from total-ready calculations
#         Added detailed debug output showing ready subs, voyaging subs, and newly sent subs per scan
#         FORCE_CRASH_INACTIVITY_MINUTES = 30 minutes (configurable) - crashes client if DefaultConfig.json not modified
#         Monitoring activates CRASH_MONITOR_DELAY hours after submarines become ready (ensures game has fully loaded)
#         Automatically stops monitoring during (WAITING) status and restarts timer when subs become ready again
#         Checks every cycle if AR file hasn't been updated in 30+ minutes → crashes client
#         Deactivates monitoring when force247uptime=True and all subs processed (no ready subs)
#         Resets timer and starts new countdown when subs become ready again
#         Handles frozen clients, lost connections, stuck in character select, and other stuck scenarios
# v1.14 - Updated Daily Supply Cost Basis calculation and added to the display
#         Calculates total supply costs per day based on submarine consumption rates
#         Displays "Total Supply Cost Per Day" in terminal output (Ceruleum Tank = 350 gil, Repair Kit = 2000 gil)
#         Added version number display to terminal header for better tracking
#         Supply costs calculated using build_consumption_rates with default fallback (9 tanks/day, 1.33 kits/day)
# v1.13 - Added window title update checking after game launch for reliable window detection
#         After OPEN_DELAY_THRESHOLD wait, checks if default "FINAL FANTASY XIV" window title exists
#         Waits indefinitely for plugin to update window title from default to "ProcessID - nickname" format
#         Uses WINDOW_TITLE_RESCAN (5s) to poll for title updates until custom title appears
#         Ensures plugins have loaded and window can be identified before moving windows/launching next game
#         Only applies in multi-client mode (skipped when USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME=True)
#         Removed timeout - will keep waiting until window title updates (never skips)
# v1.12 - Enhanced auto-launch visual feedback with real-time client status display
#         After launching each client and waiting OPEN_DELAY_THRESHOLD, redisplays the submarine timer table
#         Shows newly opened client status before proceeding to launch next client
#         Provides clearer feedback during multi-client launches and reduces console message spam
#         Improves visibility of which clients are currently running during sequential launch process
# v1.11 - Added MAX_CLIENTS configuration for hardware-limited setups
#         MAX_CLIENTS = 0 (default): Unlimited clients, opens all ready clients simultaneously
#         MAX_CLIENTS = N: Limits to N concurrent running clients at a time
#         Prioritizes force247uptime clients first, then submarine-ready clients
#         Opens clients sequentially with OPEN_DELAY_THRESHOLD wait and window arrangement between each
#         Each [RUNNING] client counts toward the MAX_CLIENTS limit
#         Ensures proper processing order for 24/7 uptime requirements before submarine timers
# v1.10 - Added restocking calculation with "Total Days Until Restocking Required" display
#         Tracks Ceruleum tanks and Repair Kits inventory from DefaultConfig.json per character
#         Calculates consumption rates based on submarine builds (9-14 tanks/day, 1.33-4 kits/day depending on route)
#         Added default consumption rates (9 tanks/day, 1.33 kits/day) for unlisted builds (leveling submarines)
#         Displays minimum days until restocking across all characters to prevent running dry
#         Formula: min(tanks/consumption, kits/consumption) rounded down per character, showing account minimum
# v1.09 - Fixed submarine build collection for custom-named submarines and enhanced console display
#         Fixed submarine build detection to properly count custom-named submarines (e.g., "You Don't Pay My Sub")
#         Build collection now matches submarines by name from OfflineSubmarineData instead of filtering by "Submersible-" prefix
#         Added "Total Subs Leveling" display line showing count of submarines still being leveled
#         Added "Total Subs Farming" display line showing count of submarines on farming routes (build_gil_rates matches)
#         Gil calculation now includes all submarines regardless of custom names for accurate daily earnings
# v1.08 - Enhanced configuration flag handling and status display improvements
#         Fixed handling of include_submarines and force247uptime flag combinations
#         Display now shows game status even when include_submarines=False
#         Auto-close logic properly closes clients when include_submarines=False AND force247uptime=False
#         Status display shows [Up 24/7] when force247uptime=True instead of [Running]/[Closed]
#         Added informative wait time messages after all auto-launch and auto-close actions
#         Changed "Subs off" display text to "Disabled" for cleaner indication
#         Supports four distinct configuration behaviors for complete flexibility
# v1.07 - Added (WAITING) status display for running games with 0 ready subs
#         Shows "(WAITING)" when game is running with positive hours <= AUTO_CLOSE_THRESHOLD
#         Provides clear feedback when game is idle waiting for submarines to be ready
# v1.06 - Renamed 'rotatingretainers' parameter to 'force247uptime' for better clarity
#         Updated all references in code, comments, and documentation
#         Functionality remains identical - parameter name now better reflects its purpose
# v1.05 - Fixed PID and UPTIME display in single client mode
#         When USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME=True, display now correctly shows PID and UPTIME
#         Gets actual PID from running ffxiv_dx11.exe process for display purposes
#         Uses 'ffxiv_single' key to retrieve start time and calculate uptime
#         Resolves issue where PID/UPTIME were missing despite running process
# v1.04 - Enhanced single client mode with MAX_RUNTIME enforcement
#         Added get_ffxiv_process_start_time() to track ffxiv_dx11.exe uptime via psutil
#         Single client mode now supports 71h MAX_RUNTIME protection against 72h disconnect
#         Tracks uptime using 'ffxiv_single' key without requiring process ID
#         Proper cleanup of single client tracking when game closes or relaunches
# v1.03 - Added USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME configuration parameter
#         When True: Uses default "FINAL FANTASY XIV" window title (single account only, kills by process name)
#         When False: Uses "ProcessID - nickname" format (multiple accounts, kills by PID)
#         Added validation to prevent multiple accounts when single client mode is enabled
#         Added kill_ffxiv_process() function for single client mode (kills ffxiv_dx11.exe)
# v1.02 - Fixed auto-launch not checking submarine timers for non-rotating accounts
#         Added submarine timer checking logic to launch games when subs nearly ready (AUTO_LAUNCH_THRESHOLD)
# v1.01 - Added force247uptime per-account flag to keep clients running for AutoRetainer retainers
#         Added MAX_RUNTIME (71h) per-client uptime limit with forced restart to avoid 72h FFXIV uptime issue
# v1.00 - Initial release with comprehensive submarine automation
#         • Real-time submarine timer monitoring with dual refresh rates
#         • Auto-launch games when submarines nearly ready (configurable threshold)
#         • Auto-close games when submarines not ready soon (prevents idle instances)
#         • Automatic window arrangement with customizable layouts
#         • Process tracking and management for reliable game control
#         • Gil earnings calculation from submarine builds
#         • Rate limiting and intelligent launch/close logic
#
########################################################################################################################

import json
import os
import datetime
import sys
import getpass
import time
from pathlib import Path
import win32gui
import win32process
import subprocess
import ctypes
from ctypes import wintypes
import re
import win32con
import requests
import threading

# Try to import psutil for process information
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("[WARNING] psutil not installed. Install with: pip install psutil")
    print("[WARNING] Uptime will only be tracked from script start time.")

# Try to import pyotp and keyring for 2FA support
try:
    import pyotp
    import keyring
    PYOTP_AVAILABLE = True
except ImportError:
    PYOTP_AVAILABLE = False
    print("[WARNING] pyotp/keyring not installed. Install with: pip install pyotp keyring")
    print("[WARNING] 2FA features will be disabled.")

# ===============================================
# Configuration Parameters
# ===============================================
VERSION = "v1.31"     # Current script version
VERSION_SUFFIX = ""     # Custom text appended to version display (set via config.json, e.g., " - Main")

# Display settings
NICKNAME_WIDTH = 5      # Display column width for account nicknames in terminal output
SUBS_COUNT_WIDTH = 11   # Display column width for submarine count (e.g., "Subs: 4/4")
HOURS_WIDTH = 24        # Display column width for submarine return times/ready status
STATUS_WIDTH = 10       # Display column width for game status (Running/Closed/Up 24/7)
PID_WIDTH = 11          # Display column width for process ID (e.g., "PID: 12345")

# Timer settings
TIMER_REFRESH_INTERVAL = 30     # Main loop cycle time (seconds) - updates submarine timers and checks for launch/close conditions
WINDOW_REFRESH_INTERVAL = 60    # How often (seconds) to scan running processes to detect which game clients are open/closed

# Auto-close game settings
ENABLE_AUTO_CLOSE = True            # Enable automatic closing of game clients when submarines are not ready soon
AUTO_CLOSE_THRESHOLD = 0.5          # Close game if soonest submarine return time exceeds this many hours (0.5h = 30 minutes)
MAX_RUNTIME = 71                    # Force close any game client that has been running for this many hours (prevents indefinite uptime)
FORCE_CRASH_INACTIVITY_MINUTES = 10 # Force crash client if no submarine processing detected for this many minutes (after monitoring activates)
FORCE_CRASH_RETAINER_MINUTES = 20   # Force crash client if no retainer processing detected for this many minutes (longer due to GC turn-ins)
# Note: Monitoring activates AUTO_LAUNCH_THRESHOLD hours after game launches (not when subs become ready)
# This ensures crash detection works even if game boots stuck without processing any submarines

# Auto-launch game settings
ENABLE_AUTO_LAUNCH = True       # Enable automatic launching of game clients when submarines are nearly ready
OTP_LAUNCH_DELAY = 10           # For 2FA, delay in seconds between launching and sending OTP code (not recommended below 10)
AUTO_LAUNCH_THRESHOLD = 0.15    # Launch game if soonest submarine return time is at or below this many hours (0.15h = 9 minutes)
OPEN_DELAY_THRESHOLD = 60       # Minimum seconds to wait between launching the same account (rate limiting per account, prevents launch spam)
WINDOW_TITLE_RESCAN = 5         # Seconds to wait between each window title check after launch (polling interval for plugin to rename window)
MAX_WINDOW_TITLE_RESCAN = 20    # Maximum number of title check attempts before giving up (20 checks × 5s = 100s timeout, then kills stuck process and retries)
FORCE_LAUNCHER_RETRY = 3        # Maximum number of launcher retry attempts when XIVLauncher.exe opens instead of game (prevents stuck accounts)
ENABLE_AUTOLOGIN_UPDATER = True # Enable automatic updating of AutologinEnabled in launcherConfigV3.json when launcher opens instead of game
                                # When True: After launcher fail 1/3 or 2/3, checks and updates AutologinEnabled to "true" before retry
                                # This fixes rare cases where launcher opens because autologin was disabled in the config
MAX_CLIENTS = 0                 # Maximum concurrent running game clients allowed (0 = unlimited, N = caps at N clients for hardware-limited systems)
                                # When limit reached, prioritizes force247uptime accounts first, then submarine-ready accounts

# Window arrangement settings
ENABLE_WINDOW_LAYOUT = False                 # Enable automatic positioning/sizing of game windows after launch (requires window layout JSON files)
WINDOW_LAYOUT = "main"                       # Which layout configuration to use: "left" (window_layout_left) or "main" (window_layout_main)
WINDOW_MOVER_DIR = Path(__file__).parent     # Directory containing window layout JSON files (windows_layout_left.json / windows_layout_main.json)
MAX_WINDOW_MOVE_ATTEMPTS = 3                 # Maximum number of window move attempts per client (1-3 recommended, prevents script freeze on unresponsive windows)
WINDOW_MOVE_VERIFICATION_DELAY = 1           # Seconds to wait after window move before verifying position (allows window to settle)
MAX_FAILED_FORCE_CRASH = True                # Force crash client after MAX_WINDOW_MOVE_ATTEMPTS failures (script will relaunch on next cycle if game should be running)

# Debug settings
DEBUG = False                   # Show verbose debug output (auto-launch eligibility checks, window detection, process tracking, etc.)

# Logging settings
ENABLE_LOGGING = True          # Enable logging major issues to arr.log file
LOG_FILE = "arr.log"           # Log file name for major issues (created in script directory)

# System settings
SYSTEM_BOOTUP_DELAY = 0         # Seconds to delay before starting script monitoring (useful for auto-start on system boot, 0 = no delay)

# Pushover notification settings (optional)
ENABLE_PUSHOVER = False         # Enable Pushover notifications for logged issues
PUSHOVER_USER_KEY = ""          # Your Pushover user key (from https://pushover.net/)
PUSHOVER_API_TOKEN = ""         # Your Pushover application API token

# Discord webhook notification settings (optional)
ENABLE_DISCORD_WEBHOOK = False  # Enable Discord webhook notifications for logged issues
DISCORD_WEBHOOK_URL = ""        # Discord webhook URL for notifications

# Single client mode settings
USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME = True    # If True: uses default "FINAL FANTASY XIV" window title (single account mode, no Dalamud renaming needed)
                                              # If False: expects "ProcessID - nickname" window titles (multi-account mode, requires Dalamud plugin for window renaming)
                                              # Single client mode is intended for single-account setups where the game window title does not need to be customized

# External config file name (not required, leave as is if not using)
CONFIG_FILE = "config.json"

# ===============================================
# Supply Costs (configurable via config.json)
# ===============================================
CERULEUM_TANK_COST = 350   # Gil cost per Ceruleum Tank
REPAIR_KIT_COST = 2000     # Gil cost per Repair Kit

# ===============================================
# Submarine Plan Configuration (configurable via config.json)
# Leveling plans = no income counted, Farming plans = daily gil earnings
# ===============================================
submarine_plans = {
    "leveling": [
        "OJ Unlocker",
        "Overseer OJ Unlocker", 
        "XP Grind",
        "Level Up Default",
        "Unlock All Sectors"
    ],
    "farming": {
        "OJ": 118661,
        "Yummy OJ": 118661,
        "Overseer OJ": 118661,
        "JORZ": 140404,
        "MROJZ": 116206
    }
}

# ===============================================
# Submarine Build Gil Rates (from AR Parser)
# Gil/Sub/Day rates for each route
# ===============================================
build_gil_rates = {
    "WSUC": 118661, "SSUC": 118661, "W+S+U+C+": 118661, "S+S+S+C+": 118661,
    "YUUW": 93165, "Y+U+U+W+": 93165,
    "WCSU": 106191, "WUSS": 106191, "W+U+S+S+": 106191,
    "YSYC": 113321, "Y+S+Y+C+": 113321,
    "S+S+U+C": 140404, "S+S+U+C+": 140404,
    "WCYC": 105303, "WUWC": 105303, "W+U+W+C+": 105303,
    "YSCU": 116206, "SCUS": 116206, "S+C+U+S+": 116206,
}

# ===============================================
# Submarine Build Consumption Rates (from Routes.xlsx)
# ===============================================
build_consumption_rates = {
    "WSUC": {"tanks_per_day": 9.0, "kits_per_day": 1.33},
    "SSUC": {"tanks_per_day": 9.0, "kits_per_day": 1.33},
    "W+S+U+C+": {"tanks_per_day": 9.0, "kits_per_day": 3.43},
    "S+S+S+C+": {"tanks_per_day": 9.0, "kits_per_day": 3.43},
    "YUUW": {"tanks_per_day": 7.5, "kits_per_day": 1.40},
    "Y+U+U+W+": {"tanks_per_day": 10.0, "kits_per_day": 3.07},
    "WCSU": {"tanks_per_day": 10.0, "kits_per_day": 1.67},
    "WUSS": {"tanks_per_day": 10.0, "kits_per_day": 1.67},
    "W+U+S+S+": {"tanks_per_day": 10.0, "kits_per_day": 3.20},
    "YSYC": {"tanks_per_day": 10.0, "kits_per_day": 2.50},
    "Y+S+Y+C+": {"tanks_per_day": 10.0, "kits_per_day": 3.20},
    "S+S+U+C": {"tanks_per_day": 14.0, "kits_per_day": 3.67},
    "WCYC": {"tanks_per_day": 10.5, "kits_per_day": 2.00},
    "WUWC": {"tanks_per_day": 10.5, "kits_per_day": 2.00},
    "W+U+W+C+": {"tanks_per_day": 10.5, "kits_per_day": 3.00},
    "S+S+U+C+": {"tanks_per_day": 14.0, "kits_per_day": 4.0},
    "YSCU": {"tanks_per_day": 9.0, "kits_per_day": 1.67},
    "SCUS": {"tanks_per_day": 9.0, "kits_per_day": 1.67},
    "S+C+U+S+": {"tanks_per_day": 13.5, "kits_per_day": 4.0},
}

# Global plan name cache (GUID -> plan name)
submarine_plan_names = {}

def build_plan_name_cache(data):
    """Build a cache of plan GUIDs to plan names from AutoRetainer config."""
    global submarine_plan_names
    submarine_plan_names = {}
    
    # SubmarinePointPlans (farming routes)
    for plan in data.get("SubmarinePointPlans", []):
        guid = plan.get("GUID", "")
        name = plan.get("Name", "")
        if guid and name:
            submarine_plan_names[guid] = name
    
    # SubmarineUnlockPlans (leveling/unlock routes)
    for plan in data.get("SubmarineUnlockPlans", []):
        guid = plan.get("GUID", "")
        name = plan.get("Name", "")
        if guid and name:
            submarine_plan_names[guid] = name

def get_submarine_plan_name(sub_data):
    """Get the plan name for a submarine based on its selected plan GUID."""
    selected_point_plan = sub_data.get("SelectedPointPlan", "")
    selected_unlock_plan = sub_data.get("SelectedUnlockPlan", "")
    vessel_behavior = sub_data.get("VesselBehavior", 0)
    
    # VesselBehavior 4 = Use Point Plan, 3 = Unlock Sectors
    plan_guid = ""
    if vessel_behavior == 4:
        plan_guid = selected_point_plan
    elif vessel_behavior == 3:
        plan_guid = selected_unlock_plan
    
    return submarine_plan_names.get(plan_guid, "")

# ===============================================
# Account locations
# ===============================================
user = getpass.getuser()

def acc(nickname, pluginconfigs_path, include_submarines=True, force247uptime=False, enable_2fa=False, keyring_name=None):
    auto_path = os.path.join(pluginconfigs_path, "AutoRetainer", "DefaultConfig.json")
    return {
        "nickname": nickname,
        "auto_path": auto_path,
        "include_submarines": bool(include_submarines),
        "force247uptime": bool(force247uptime),
        "enable_2fa": bool(enable_2fa),
        "keyring_name": keyring_name,
    }

# In the splatoon script: Rename($"{Environment.ProcessId} - nickname"
# replace 'nickname' with "Main" of "Acc1" keep the space and dash

# Account configuration - matches AR Parser order
# 2FA: Set enable_2fa=True and keyring_name="your_keyring_name" for automatic OTP sending
account_locations = [
    acc("Main",   f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs", include_submarines=True, force247uptime=False, enable_2fa=False, keyring_name=None),
    # acc("Acc1",   f"C:\\Users\\{user}\\AltData\\Acc1\\pluginConfigs", include_submarines=True, force247uptime=False, enable_2fa=True, keyring_name="ffxiv_acc1"),
    # acc("Acc2",   f"C:\\Users\\{user}\\AltData\\Acc2\\pluginConfigs", include_submarines=True, force247uptime=True, enable_2fa=True, keyring_name="ffxiv_acc2"),
]

# # Game launcher paths for each account (update these paths to your actual game launchers)
GAME_LAUNCHERS = {
    "Main":   rf"C:\Users\{user}\AppData\Local\XIVLauncher\XIVLauncher.exe",
    # "Acc1":   rf"C:\Users\{user}\AltData\Acc1.bat",
    # "Acc2":   rf"C:\Users\{user}\AltData\Acc2.bat",
}

# ===============================================
# External Configuration Loading
# ===============================================
def load_external_config():
    """Load external config file if it exists and override settings."""
    global VERSION_SUFFIX, NICKNAME_WIDTH, SUBS_COUNT_WIDTH, HOURS_WIDTH, STATUS_WIDTH, PID_WIDTH
    global TIMER_REFRESH_INTERVAL, WINDOW_REFRESH_INTERVAL
    global ENABLE_AUTO_CLOSE, AUTO_CLOSE_THRESHOLD, MAX_RUNTIME, FORCE_CRASH_INACTIVITY_MINUTES, FORCE_CRASH_RETAINER_MINUTES
    global ENABLE_AUTO_LAUNCH, OTP_LAUNCH_DELAY, AUTO_LAUNCH_THRESHOLD, OPEN_DELAY_THRESHOLD
    global WINDOW_TITLE_RESCAN, MAX_WINDOW_TITLE_RESCAN, FORCE_LAUNCHER_RETRY, ENABLE_AUTOLOGIN_UPDATER, MAX_CLIENTS
    global ENABLE_WINDOW_LAYOUT, WINDOW_LAYOUT, WINDOW_MOVER_DIR, MAX_WINDOW_MOVE_ATTEMPTS
    global WINDOW_MOVE_VERIFICATION_DELAY, MAX_FAILED_FORCE_CRASH
    global DEBUG, ENABLE_LOGGING, LOG_FILE, SYSTEM_BOOTUP_DELAY, USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME
    global ENABLE_PUSHOVER, PUSHOVER_USER_KEY, PUSHOVER_API_TOKEN
    global ENABLE_DISCORD_WEBHOOK, DISCORD_WEBHOOK_URL
    global account_locations, GAME_LAUNCHERS
    global build_gil_rates, build_consumption_rates, submarine_plans
    global CERULEUM_TANK_COST, REPAIR_KIT_COST

    config_path = Path(__file__).parent / CONFIG_FILE
    if not config_path.exists():
        return

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"[CONFIG] Loaded configuration from {config_path}")
    except json.JSONDecodeError as e:
        print(f"[CONFIG] Error parsing {CONFIG_FILE}: {e}")
        print("[CONFIG] Please fix the JSON syntax error and try again.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"[CONFIG] Error reading {CONFIG_FILE}: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)

    # Helper function for compact config loading
    cfg = config.get

    # Override settings if present in config (using compact cfg() approach)
    VERSION_SUFFIX = cfg("VERSION_SUFFIX", VERSION_SUFFIX)
    NICKNAME_WIDTH = cfg("NICKNAME_WIDTH", NICKNAME_WIDTH)
    SUBS_COUNT_WIDTH = cfg("SUBS_COUNT_WIDTH", SUBS_COUNT_WIDTH)
    HOURS_WIDTH = cfg("HOURS_WIDTH", HOURS_WIDTH)
    STATUS_WIDTH = cfg("STATUS_WIDTH", STATUS_WIDTH)
    PID_WIDTH = cfg("PID_WIDTH", PID_WIDTH)
    TIMER_REFRESH_INTERVAL = cfg("TIMER_REFRESH_INTERVAL", TIMER_REFRESH_INTERVAL)
    WINDOW_REFRESH_INTERVAL = cfg("WINDOW_REFRESH_INTERVAL", WINDOW_REFRESH_INTERVAL)
    ENABLE_AUTO_CLOSE = cfg("ENABLE_AUTO_CLOSE", ENABLE_AUTO_CLOSE)
    AUTO_CLOSE_THRESHOLD = cfg("AUTO_CLOSE_THRESHOLD", AUTO_CLOSE_THRESHOLD)
    MAX_RUNTIME = cfg("MAX_RUNTIME", MAX_RUNTIME)
    FORCE_CRASH_INACTIVITY_MINUTES = cfg("FORCE_CRASH_INACTIVITY_MINUTES", FORCE_CRASH_INACTIVITY_MINUTES)
    FORCE_CRASH_RETAINER_MINUTES = cfg("FORCE_CRASH_RETAINER_MINUTES", FORCE_CRASH_RETAINER_MINUTES)
    ENABLE_AUTO_LAUNCH = cfg("ENABLE_AUTO_LAUNCH", ENABLE_AUTO_LAUNCH)
    OTP_LAUNCH_DELAY = cfg("OTP_LAUNCH_DELAY", OTP_LAUNCH_DELAY)
    AUTO_LAUNCH_THRESHOLD = cfg("AUTO_LAUNCH_THRESHOLD", AUTO_LAUNCH_THRESHOLD)
    OPEN_DELAY_THRESHOLD = cfg("OPEN_DELAY_THRESHOLD", OPEN_DELAY_THRESHOLD)
    WINDOW_TITLE_RESCAN = cfg("WINDOW_TITLE_RESCAN", WINDOW_TITLE_RESCAN)
    MAX_WINDOW_TITLE_RESCAN = cfg("MAX_WINDOW_TITLE_RESCAN", MAX_WINDOW_TITLE_RESCAN)
    FORCE_LAUNCHER_RETRY = cfg("FORCE_LAUNCHER_RETRY", FORCE_LAUNCHER_RETRY)
    ENABLE_AUTOLOGIN_UPDATER = cfg("ENABLE_AUTOLOGIN_UPDATER", ENABLE_AUTOLOGIN_UPDATER)
    MAX_CLIENTS = cfg("MAX_CLIENTS", MAX_CLIENTS)
    ENABLE_WINDOW_LAYOUT = cfg("ENABLE_WINDOW_LAYOUT", ENABLE_WINDOW_LAYOUT)
    WINDOW_LAYOUT = cfg("WINDOW_LAYOUT", WINDOW_LAYOUT)
    MAX_WINDOW_MOVE_ATTEMPTS = cfg("MAX_WINDOW_MOVE_ATTEMPTS", MAX_WINDOW_MOVE_ATTEMPTS)
    WINDOW_MOVE_VERIFICATION_DELAY = cfg("WINDOW_MOVE_VERIFICATION_DELAY", WINDOW_MOVE_VERIFICATION_DELAY)
    MAX_FAILED_FORCE_CRASH = cfg("MAX_FAILED_FORCE_CRASH", MAX_FAILED_FORCE_CRASH)
    DEBUG = cfg("DEBUG", DEBUG)
    ENABLE_LOGGING = cfg("ENABLE_LOGGING", ENABLE_LOGGING)
    LOG_FILE = cfg("LOG_FILE", LOG_FILE)
    ENABLE_PUSHOVER = cfg("ENABLE_PUSHOVER", ENABLE_PUSHOVER)
    PUSHOVER_USER_KEY = cfg("PUSHOVER_USER_KEY", PUSHOVER_USER_KEY)
    PUSHOVER_API_TOKEN = cfg("PUSHOVER_API_TOKEN", PUSHOVER_API_TOKEN)
    ENABLE_DISCORD_WEBHOOK = cfg("ENABLE_DISCORD_WEBHOOK", ENABLE_DISCORD_WEBHOOK)
    DISCORD_WEBHOOK_URL = cfg("DISCORD_WEBHOOK_URL", DISCORD_WEBHOOK_URL)
    SYSTEM_BOOTUP_DELAY = cfg("SYSTEM_BOOTUP_DELAY", SYSTEM_BOOTUP_DELAY)
    USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME = cfg("USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME", USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME)
    
    # Override supply costs if present
    CERULEUM_TANK_COST = cfg("ceruleum_tank_cost", CERULEUM_TANK_COST)
    REPAIR_KIT_COST = cfg("repair_kit_cost", REPAIR_KIT_COST)
    
    # Override submarine_plans if present (merge with defaults)
    if "submarine_plans" in config:
        config_plans = config["submarine_plans"]
        # Merge leveling plans (add to existing list, avoid duplicates)
        if "leveling" in config_plans:
            for plan in config_plans["leveling"]:
                if plan not in submarine_plans["leveling"]:
                    submarine_plans["leveling"].append(plan)
        # Merge farming plans (add new, override existing with same name)
        if "farming" in config_plans:
            submarine_plans["farming"].update(config_plans["farming"])
        print(f"[CONFIG] Loaded custom submarine plans")
    
    # Override build_gil_rates if present (merge with defaults)
    if "build_gil_rates" in config:
        build_gil_rates.update(config["build_gil_rates"])
        print(f"[CONFIG] Loaded {len(config['build_gil_rates'])} custom build gil rates")
    
    # Override build_consumption_rates if present (merge with defaults)
    if "build_consumption_rates" in config:
        build_consumption_rates.update(config["build_consumption_rates"])
        print(f"[CONFIG] Loaded {len(config['build_consumption_rates'])} custom build consumption rates")

    # Override account_locations if present
    if "account_locations" in config:
        new_locations = []
        for acc_config in config["account_locations"]:
            # Skip disabled accounts (enabled defaults to True if not specified)
            if not acc_config.get("enabled", True):
                continue
            nickname = acc_config.get("nickname", "Unknown")
            pluginconfigs_path = acc_config.get("pluginconfigs_path", "")
            pluginconfigs_path = os.path.expandvars(pluginconfigs_path)
            pluginconfigs_path = pluginconfigs_path.replace("{user}", user)
            new_locations.append(acc(
                nickname=nickname,
                pluginconfigs_path=pluginconfigs_path,
                include_submarines=acc_config.get("include_submarines", True),
                force247uptime=acc_config.get("force247uptime", False),
                enable_2fa=acc_config.get("enable_2fa", False),
                keyring_name=acc_config.get("keyring_name", None)
            ))
        account_locations = new_locations

    # Override game_launchers if present
    if "game_launchers" in config:
        new_launchers = {}
        for nickname, path in config["game_launchers"].items():
            path = os.path.expandvars(path)
            path = path.replace("{user}", user)
            new_launchers[nickname] = path
        GAME_LAUNCHERS = new_launchers

# Load external config if it exists
load_external_config()

# ===============================================
# Notification Credential Validation
# ===============================================
def validate_notification_credentials():
    """Validate notification credentials and halt if misconfigured."""
    if ENABLE_PUSHOVER:
        if not PUSHOVER_USER_KEY or not PUSHOVER_API_TOKEN:
            print("\n" + "=" * 80)
            print("[ERROR] Pushover is enabled but credentials are missing!")
            print("=" * 80)
            print("ENABLE_PUSHOVER = True requires both:")
            print("  - PUSHOVER_USER_KEY: Your Pushover user key")
            print("  - PUSHOVER_API_TOKEN: Your Pushover application API token")
            print("\nPlease either:")
            print(f"  1. Enter your Pushover credentials in the script or {CONFIG_FILE}")
            print("  2. Set ENABLE_PUSHOVER = False to disable Pushover notifications")
            print("=" * 80)
            input("\nPress Enter to exit...")
            sys.exit(1)
    
    if ENABLE_DISCORD_WEBHOOK:
        if not DISCORD_WEBHOOK_URL:
            print("\n" + "=" * 80)
            print("[ERROR] Discord webhook is enabled but URL is missing!")
            print("=" * 80)
            print("ENABLE_DISCORD_WEBHOOK = True requires:")
            print("  - DISCORD_WEBHOOK_URL: Your Discord webhook URL")
            print("\nPlease either:")
            print(f"  1. Enter your Discord webhook URL in the script or {CONFIG_FILE}")
            print("  2. Set ENABLE_DISCORD_WEBHOOK = False to disable Discord notifications")
            print("=" * 80)
            input("\nPress Enter to exit...")
            sys.exit(1)

# Validate notification credentials
validate_notification_credentials()

# ===============================================
# Notification Functions
# ===============================================
def send_pushover(message):
    """Send a Pushover notification. Only sends if enabled and configured."""
    if not ENABLE_PUSHOVER or not PUSHOVER_USER_KEY or not PUSHOVER_API_TOKEN:
        return
    try:
        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": PUSHOVER_API_TOKEN,
                "user": PUSHOVER_USER_KEY,
                "title": "Auto-AutoRetainer",
                "message": message,
            },
            timeout=10
        )
        if DEBUG:
            if response.status_code == 200:
                print(f"[DEBUG] Pushover notification sent successfully")
            else:
                print(f"[DEBUG] Pushover notification failed: {response.status_code}")
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Failed to send Pushover notification: {e}")

def send_discord_webhook(message):
    """Send a Discord webhook notification. Only sends if enabled and configured."""
    if not ENABLE_DISCORD_WEBHOOK or not DISCORD_WEBHOOK_URL:
        return
    try:
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json={
                "content": f"{message}",
            },
            timeout=10
        )
        if DEBUG:
            if response.status_code in [200, 204]:
                print(f"[DEBUG] Discord webhook notification sent successfully")
            else:
                print(f"[DEBUG] Discord webhook notification failed: {response.status_code}")
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Failed to send Discord webhook notification: {e}")

# ===============================================
# Logging Functions
# ===============================================
def log_error(message):
    """
    Log major issues to arr.log file with timestamp.
    Only logs if ENABLE_LOGGING is True.
    Also sends Pushover and Discord notifications if enabled.
    """
    if not ENABLE_LOGGING:
        return
    try:
        log_path = Path(__file__).parent / LOG_FILE
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Failed to write to log file: {e}")
    
    # Send notifications
    send_pushover(message)
    send_discord_webhook(message)

# ===============================================
# Autologin Updater Functions
# ===============================================
def get_launcher_config_path(nickname):
    """
    Get the launcherConfigV3.json path for a given account nickname.
    The launcher config is in the PARENT directory of pluginConfigs.
    Example: pluginConfigs = C:\\Users\\user\\AltData\\Acc1\\pluginConfigs
             launcher config = C:\\Users\\user\\AltData\\Acc1\\launcherConfigV3.json
    Returns None if account not found or path doesn't exist.
    """
    for account in account_locations:
        if account["nickname"] == nickname:
            # Get the pluginConfigs path from auto_path (remove AutoRetainer/DefaultConfig.json)
            auto_path = account["auto_path"]
            pluginconfigs_path = Path(auto_path).parent.parent  # Go up from AutoRetainer/DefaultConfig.json to pluginConfigs
            launcher_config_path = pluginconfigs_path.parent / "launcherConfigV3.json"
            return launcher_config_path
    return None

def check_and_update_autologin(nickname):
    """
    Check and update AutologinEnabled in launcherConfigV3.json for the given account.
    If AutologinEnabled is "false", updates it to "true".
    Returns True if update was made, False if no update needed or error occurred.
    """
    if not ENABLE_AUTOLOGIN_UPDATER:
        return False
    
    launcher_config_path = get_launcher_config_path(nickname)
    if launcher_config_path is None:
        if DEBUG:
            print(f"[AUTOLOGIN] Could not find launcher config path for {nickname}")
        return False
    
    if not launcher_config_path.exists():
        if DEBUG:
            print(f"[AUTOLOGIN] Launcher config file not found: {launcher_config_path}")
        log_error(f"AUTOLOGIN_FILE_NOT_FOUND: {nickname} - {launcher_config_path}")
        return False
    
    try:
        # Read the JSON file
        with open(launcher_config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check current AutologinEnabled value
        current_value = data.get("AutologinEnabled", None)
        
        if current_value == "false":
            # Update to "true"
            data["AutologinEnabled"] = "true"
            
            # Write back to file
            with open(launcher_config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            
            print(f"[AUTOLOGIN] Updated AutologinEnabled from 'false' to 'true' for {nickname}")
            log_error(f"AUTOLOGIN_UPDATED: {nickname} - Changed AutologinEnabled from 'false' to 'true' in {launcher_config_path}")
            return True
        elif current_value == "true":
            if DEBUG:
                print(f"[AUTOLOGIN] AutologinEnabled already 'true' for {nickname}")
            return False
        else:
            if DEBUG:
                print(f"[AUTOLOGIN] AutologinEnabled has unexpected value '{current_value}' for {nickname}")
            return False
            
    except json.JSONDecodeError as e:
        print(f"[AUTOLOGIN] Error parsing JSON for {nickname}: {e}")
        log_error(f"AUTOLOGIN_JSON_ERROR: {nickname} - {e}")
        return False
    except Exception as e:
        print(f"[AUTOLOGIN] Error updating config for {nickname}: {e}")
        log_error(f"AUTOLOGIN_ERROR: {nickname} - {e}")
        return False

def check_and_update_otp_server(nickname):
    """
    Check and update OtpServerEnabled in launcherConfigV3.json for accounts with 2FA enabled.
    If enable_2fa=True for the account and OtpServerEnabled is "false", updates it to "true".
    Returns True if update was made, False if no update needed or error occurred.
    """
    if not ENABLE_AUTOLOGIN_UPDATER:
        return False
    
    # Check if this account has 2FA enabled
    account_config = None
    for acc_item in account_locations:
        if acc_item["nickname"] == nickname:
            account_config = acc_item
            break
    
    if not account_config or not account_config.get("enable_2fa", False):
        # 2FA not enabled for this account, skip OTP server check
        return False
    
    launcher_config_path = get_launcher_config_path(nickname)
    if launcher_config_path is None:
        if DEBUG:
            print(f"[OTP-SERVER] Could not find launcher config path for {nickname}")
        return False
    
    if not launcher_config_path.exists():
        if DEBUG:
            print(f"[OTP-SERVER] Launcher config file not found: {launcher_config_path}")
        return False
    
    try:
        # Read the JSON file
        with open(launcher_config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check current OtpServerEnabled value
        current_value = data.get("OtpServerEnabled", None)
        
        if current_value == "false":
            # Update to "true"
            data["OtpServerEnabled"] = "true"
            
            # Write back to file
            with open(launcher_config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            
            print(f"[OTP-SERVER] Updated OtpServerEnabled from 'false' to 'true' for {nickname}")
            log_error(f"OTP_SERVER_UPDATED: {nickname} - Changed OtpServerEnabled from 'false' to 'true' in {launcher_config_path}")
            return True
        elif current_value == "true":
            if DEBUG:
                print(f"[OTP-SERVER] OtpServerEnabled already 'true' for {nickname}")
            return False
        else:
            if DEBUG:
                print(f"[OTP-SERVER] OtpServerEnabled has unexpected value '{current_value}' for {nickname}")
            return False
            
    except json.JSONDecodeError as e:
        print(f"[OTP-SERVER] Error parsing JSON for {nickname}: {e}")
        log_error(f"OTP_SERVER_JSON_ERROR: {nickname} - {e}")
        return False
    except Exception as e:
        print(f"[OTP-SERVER] Error updating config for {nickname}: {e}")
        log_error(f"OTP_SERVER_ERROR: {nickname} - {e}")
        return False

def validate_launcher_config_before_launch(nickname):
    """
    Validate and fix launcher configuration BEFORE launching game.
    Checks launcherConfigV3.json and ensures:
    1. AutologinEnabled is "true" (always)
    2. OtpServerEnabled is "true" (only if account has enable_2fa=True)
    
    This prevents the launcher from opening with login prompt instead of auto-logging in.
    Returns True if config is valid (or was fixed), False if critical error.
    """
    launcher_config_path = get_launcher_config_path(nickname)
    
    if launcher_config_path is None:
        print(f"[CONFIG-CHECK] Could not find launcher config path for {nickname}")
        return True  # Continue anyway, will fail at launch if path is wrong
    
    if not launcher_config_path.exists():
        print(f"[CONFIG-CHECK] Launcher config not found: {launcher_config_path}")
        return True  # Continue anyway, launcher may create it
    
    # Get account config to check if 2FA is enabled
    account_config = None
    for acc_item in account_locations:
        if acc_item["nickname"] == nickname:
            account_config = acc_item
            break
    
    enable_2fa = account_config.get("enable_2fa", False) if account_config else False
    
    try:
        with open(launcher_config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        config_updated = False
        
        # Check and fix AutologinEnabled
        autologin_value = data.get("AutologinEnabled", None)
        if autologin_value != "true":
            old_value = autologin_value
            data["AutologinEnabled"] = "true"
            config_updated = True
            print(f"[CONFIG-CHECK] Fixed AutologinEnabled: '{old_value}' -> 'true' for {nickname}")
            log_error(f"CONFIG_FIXED_AUTOLOGIN: {nickname} - Changed AutologinEnabled from '{old_value}' to 'true'")
        
        # Check and fix OtpServerEnabled (only if 2FA is enabled for this account)
        if enable_2fa:
            otp_value = data.get("OtpServerEnabled", None)
            if otp_value != "true":
                old_value = otp_value
                data["OtpServerEnabled"] = "true"
                config_updated = True
                print(f"[CONFIG-CHECK] Fixed OtpServerEnabled: '{old_value}' -> 'true' for {nickname}")
                log_error(f"CONFIG_FIXED_OTP: {nickname} - Changed OtpServerEnabled from '{old_value}' to 'true'")
        
        # Write back if changes were made
        if config_updated:
            with open(launcher_config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"[CONFIG-CHECK] Launcher config updated for {nickname}")
        elif DEBUG:
            print(f"[CONFIG-CHECK] Launcher config OK for {nickname}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"[CONFIG-CHECK] Error parsing launcher config JSON for {nickname}: {e}")
        log_error(f"CONFIG_CHECK_JSON_ERROR: {nickname} - {e}")
        return False
    except Exception as e:
        print(f"[CONFIG-CHECK] Error checking launcher config for {nickname}: {e}")
        log_error(f"CONFIG_CHECK_ERROR: {nickname} - {e}")
        return False

# Submarine Part Constants for build detection
SUB_PARTS_LOOKUP = {
    21792: "Shark-class Bow",
    21793: "Shark-class Bridge",
    21794: "Shark-class Pressure Hull",
    21795: "Shark-class Stern",
    21796: "Unkiu-class Bow",
    21797: "Unkiu-class Bridge",
    21798: "Unkiu-class Pressure Hull",
    21799: "Unkiu-class Stern",
    22526: "Whale-class Bow",
    22527: "Whale-class Bridge",
    22528: "Whale-class Pressure Hull",
    22529: "Whale-class Stern",
    23903: "Coelacanth-class Bow",
    23904: "Coelacanth-class Bridge",
    23905: "Coelacanth-class Pressure Hull",
    23906: "Coelacanth-class Stern",
    24344: "Syldra-class Bow",
    24345: "Syldra-class Bridge",
    24346: "Syldra-class Pressure Hull",
    24347: "Syldra-class Stern",
    24348: "Modified Shark-class Bow",
    24349: "Modified Shark-class Bridge",
    24350: "Modified Shark-class Pressure Hull",
    24351: "Modified Shark-class Stern",
    24352: "Modified Unkiu-class Bow",
    24353: "Modified Unkiu-class Bridge",
    24354: "Modified Unkiu-class Pressure Hull",
    24355: "Modified Unkiu-class Stern",
    24356: "Modified Whale-class Bow",
    24357: "Modified Whale-class Bridge",
    24358: "Modified Whale-class Pressure Hull",
    24359: "Modified Whale-class Stern",
    24360: "Modified Coelacanth-class Bow",
    24361: "Modified Coelacanth-class Bridge",
    24362: "Modified Coelacanth-class Pressure Hull",
    24363: "Modified Coelacanth-class Stern",
    24364: "Modified Syldra-class Bow",
    24365: "Modified Syldra-class Bridge",
    24366: "Modified Syldra-class Pressure Hull",
    24367: "Modified Syldra-class Stern"
}

CLASS_SHORTCUTS = {
    "Shark-class": "S",
    "Unkiu-class": "U",
    "Whale-class": "W",
    "Coelacanth-class": "C",
    "Syldra-class": "Y",
    "Modified Shark-class": "S+",
    "Modified Unkiu-class": "U+",
    "Modified Whale-class": "W+",
    "Modified Coelacanth-class": "C+",
    "Modified Syldra-class": "Y+"
}

def collect_characters(full_data, account_nickname):
    """Extract characters from AutoRetainer JSON data"""
    all_chars = []
    def assign_nickname(chara):
        chara["AccountNickname"] = account_nickname
        return chara

    if isinstance(full_data, dict):
        if "OfflineData" in full_data and isinstance(full_data["OfflineData"], list):
            for c in full_data["OfflineData"]:
                if isinstance(c, dict) and "CID" in c:
                    all_chars.append(assign_nickname(c))
        else:
            for _, value in full_data.items():
                if isinstance(value, dict) and "CID" in value:
                    all_chars.append(assign_nickname(value))
    elif isinstance(full_data, list):
        for item in full_data:
            if isinstance(item, dict) and "CID" in item:
                all_chars.append(assign_nickname(item))
    return all_chars

def shorten_part_name(full_name: str) -> str:
    """Convert full submarine part name to short code"""
    for prefix, code in CLASS_SHORTCUTS.items():
        if full_name.startswith(prefix):
            return code
    return "?"

def get_sub_parts_string(sub_data: dict) -> str:
    """Get submarine build string from part IDs"""
    parts = []
    for key in ["Part1", "Part2", "Part3", "Part4"]:
        part_id = sub_data.get(key, 0)
        if part_id != 0:
            full_part_name = SUB_PARTS_LOOKUP.get(part_id, f"Unknown({part_id})")
            short_code = shorten_part_name(full_part_name)
            parts.append(short_code)
    return "".join(parts)

# ===============================================
# Window Mover Functions
# ===============================================

# DPI awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

SW_RESTORE = 9
SetWindowPos = ctypes.windll.user32.SetWindowPos
SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND,
                         ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]

HWND_TOP = wintypes.HWND(0)
HWND_TOPMOST = wintypes.HWND(-1)
HWND_NOTOPMOST = wintypes.HWND(-2)

SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOZORDER = 0x0004
SWP_NOACTIVATE = 0x0010
SWP_FRAMECHANGED = 0x0020
SWP_SHOWWINDOW = 0x0040

GWL_STYLE = -16
GWL_EXSTYLE = -20
WS_MAXIMIZE = 0x01000000
WS_MINIMIZE = 0x20000000

# Window message constants for responsiveness checking
SMTO_ABORTIFHUNG = 0x0002
WM_NULL = 0x0000

def read_window_layout_config():
    """Read window layout JSON config based on WINDOW_LAYOUT setting"""
    layout_file = f"window_layout_{WINDOW_LAYOUT}.json"
    config_path = Path(WINDOW_MOVER_DIR) / layout_file
    
    if not config_path.exists():
        print(f"[ERROR] Window layout file not found: {config_path}")
        return None
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to read window layout: {e}")
        return None

def is_visible_top_window(hwnd):
    return win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd)

def restore_if_minimized(hwnd):
    style = win32gui.GetWindowLong(hwnd, GWL_STYLE)
    if style & WS_MINIMIZE:
        win32gui.ShowWindow(hwnd, SW_RESTORE)
        time.sleep(0.05)

def remove_maximize_state(hwnd):
    style = win32gui.GetWindowLong(hwnd, GWL_STYLE)
    if style & WS_MAXIMIZE:
        win32gui.ShowWindow(hwnd, SW_RESTORE)
        time.sleep(0.05)

def find_all_windows():
    wins = []
    def _enum(hwnd, extra):
        if is_visible_top_window(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title.strip():
                wins.append((hwnd, title))
    win32gui.EnumWindows(_enum, None)
    return wins

def is_window_responding(hwnd):
    """
    Check if a window is responding using SendMessageTimeout.
    Returns True if window is responding, False if frozen/not responding.
    """
    try:
        # Use SendMessageTimeout to check if window responds within 5 seconds
        SendMessageTimeout = ctypes.windll.user32.SendMessageTimeoutW
        SendMessageTimeout.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM, wintypes.UINT, wintypes.UINT, ctypes.POINTER(wintypes.DWORD)]
        
        result = wintypes.DWORD()
        ret = SendMessageTimeout(hwnd, WM_NULL, 0, 0, SMTO_ABORTIFHUNG, 5000, ctypes.byref(result))
        
        # ret == 0 means the window is not responding
        return ret != 0
    except Exception as e:
        if DEBUG:
            print(f"[WINDOW-MOVER] Error checking window responsiveness: {e}")
        return False

def get_window_position(hwnd):
    """
    Get the current position and size of a window.
    Returns dict with x, y, width, height or None if failed.
    """
    try:
        rect = win32gui.GetWindowRect(hwnd)
        return {
            'x': rect[0],
            'y': rect[1],
            'width': rect[2] - rect[0],
            'height': rect[3] - rect[1]
        }
    except Exception as e:
        if DEBUG:
            print(f"[WINDOW-MOVER] Error getting window position: {e}")
        return None

def verify_window_position(hwnd, expected_x, expected_y, expected_w, expected_h, tolerance=10):
    """
    Verify that a window moved to the expected position.
    Returns True if position matches within tolerance, False otherwise.
    tolerance: pixels of acceptable difference (default 10px for window borders/decorations)
    
    Note: Only verifies position (x,y), not size, as FFXIV windows control their own size
    via internal graphics settings and cannot be resized programmatically.
    """
    actual = get_window_position(hwnd)
    if not actual:
        return False
    
    x_match = abs(actual['x'] - expected_x) <= tolerance
    y_match = abs(actual['y'] - expected_y) <= tolerance
    
    # FFXIV windows control their own size via graphics settings, so we only verify position
    if DEBUG:
        if not (x_match and y_match):
            print(f"[WINDOW-MOVER] Position mismatch: Expected ({expected_x},{expected_y}), Got ({actual['x']},{actual['y']})")
        elif actual['width'] != expected_w or actual['height'] != expected_h:
            print(f"[WINDOW-MOVER] Note: Window size ({actual['width']}x{actual['height']}) differs from config ({expected_w}x{expected_h}) - FFXIV controls its own size via graphics settings")
    
    return x_match and y_match

def move_window_to_position(hwnd, x, y, w, h, topmost=False, activate=False):
    try:
        # Get current window style
        style = win32gui.GetWindowLong(hwnd, GWL_STYLE)
        
        # Remove styles that might prevent resizing (WS_MAXIMIZEBOX = 0x00010000, WS_THICKFRAME = 0x00040000)
        # But keep other important styles
        new_style = style | 0x00040000  # Ensure WS_THICKFRAME (resizable border) is set
        win32gui.SetWindowLong(hwnd, GWL_STYLE, new_style)
        
        # Set topmost state
        insert_after = HWND_TOPMOST if topmost else HWND_NOTOPMOST
        flags = SWP_FRAMECHANGED | SWP_SHOWWINDOW
        if not activate:
            flags |= SWP_NOACTIVATE
        
        SetWindowPos(hwnd, insert_after, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | flags)
        time.sleep(0.05)
        
        # Use MoveWindow for more direct resize control
        win32gui.MoveWindow(hwnd, x, y, w, h, True)  # True = repaint
        time.sleep(0.1)  # Give more time for resize to take effect
        
        # Restore original style
        win32gui.SetWindowLong(hwnd, GWL_STYLE, style)
        
        # Force redraw
        win32gui.RedrawWindow(hwnd, None, None, 0x0001 | 0x0004)
    except Exception as e:
        if DEBUG:
            print(f"[WINDOW-MOVER] Error in move_window_to_position: {e}")

def arrange_ffxiv_windows():
    """
    Arrange all FFXIV game windows according to the configured layout.
    Includes responsiveness checking, retry logic, and position verification.
    """
    layout = read_window_layout_config()
    if not layout:
        return False
    
    if DEBUG:
        print(f"\n[WINDOW-MOVER] Arranging windows with '{WINDOW_LAYOUT}' layout...")
    
    # Compile regexes
    rules = []
    for rule in layout.get("rules", []):
        rx = re.compile(rule["title_regex"], re.IGNORECASE)
        rules.append((rx, rule))
    rules.sort(key=lambda r: r[1].get("order", 0))
    
    windows = find_all_windows()
    
    # Match windows to rules
    assigned = []
    for rx, rule in rules:
        for hwnd, title in windows:
            if rx.match(title):
                assigned.append((rule, hwnd, title))
                windows = [(h, t) for (h, t) in windows if h != hwnd]
                break
    
    if not assigned:
        if DEBUG:
            print(f"[WINDOW-MOVER] No FFXIV windows found to arrange")
        return False
    
    # Track successful and failed moves
    successful_moves = []
    failed_moves = []
    
    # Apply moves with retry logic and verification
    for rule, hwnd, title in assigned:
        x = int(rule["x"])
        y = int(rule["y"])
        w = int(rule["width"])
        h = int(rule["height"])
        activate = bool(rule.get("activate", False))
        
        move_success = False
        
        # Check if window is responding before attempting move
        if not is_window_responding(hwnd):
            print(f"[WINDOW-MOVER] WARNING: Window '{title}' is not responding, skipping move")
            failed_moves.append((hwnd, title, "not responding"))
            continue
        
        # Attempt window move with retry logic
        for attempt in range(1, MAX_WINDOW_MOVE_ATTEMPTS + 1):
            try:
                if DEBUG:
                    print(f"[WINDOW-MOVER] Attempt {attempt}/{MAX_WINDOW_MOVE_ATTEMPTS} for '{title}'")
                
                restore_if_minimized(hwnd)
                remove_maximize_state(hwnd)
                move_window_to_position(hwnd, x, y, w, h, topmost=True, activate=activate)
                
                # Wait for window to settle
                time.sleep(WINDOW_MOVE_VERIFICATION_DELAY)
                
                # Verify window moved correctly
                if verify_window_position(hwnd, x, y, w, h):
                    print(f"[WINDOW-MOVER] SUCCESS: Moved '{title}' -> ({x},{y},{w},{h}) on attempt {attempt}")
                    successful_moves.append((hwnd, title))
                    move_success = True
                    break
                else:
                    if attempt < MAX_WINDOW_MOVE_ATTEMPTS:
                        print(f"[WINDOW-MOVER] Position verification failed for '{title}', retrying...")
                    else:
                        print(f"[WINDOW-MOVER] FAILED: Could not verify position for '{title}' after {MAX_WINDOW_MOVE_ATTEMPTS} attempts")
                        failed_moves.append((hwnd, title, "position verification failed"))
                
            except Exception as e:
                if attempt < MAX_WINDOW_MOVE_ATTEMPTS:
                    print(f"[WINDOW-MOVER] Error moving '{title}' (attempt {attempt}): {e}, retrying...")
                else:
                    print(f"[WINDOW-MOVER] FAILED: Could not move '{title}' after {MAX_WINDOW_MOVE_ATTEMPTS} attempts: {e}")
                    failed_moves.append((hwnd, title, str(e)))
        
        # Small delay between window moves
        if move_success:
            time.sleep(0.03)
    
    # Remove topmost from windows that shouldn't have it (only for successful moves)
    time.sleep(0.1)
    for hwnd, title in successful_moves:
        # Find the rule for this window
        rule = None
        for r, h, t in assigned:
            if h == hwnd:
                rule = r
                break
        
        if rule:
            topmost = bool(rule.get("topmost", False))
            try:
                if not topmost:
                    flags = SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_FRAMECHANGED
                    SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, flags)
            except Exception as e:
                if DEBUG:
                    print(f"[WINDOW-MOVER] Failed to set final topmost for '{title}': {e}")
    
    # Force crash failed windows if enabled
    if failed_moves and MAX_FAILED_FORCE_CRASH:
        for hwnd, title, reason in failed_moves:
            try:
                # Extract PID from window title (format: "ProcessID - nickname")
                pid_match = re.match(r'^(\d+)\s*-\s*.+', title)
                if pid_match:
                    pid = int(pid_match.group(1))
                    print(f"[WINDOW-MOVER] Force crashing failed window '{title}' (PID: {pid}) - {reason}")
                    log_error(f"WINDOW_FORCE_CRASH: {title} (PID: {pid}) - {reason}")
                    kill_process_by_pid(pid)
                else:
                    print(f"[WINDOW-MOVER] Could not extract PID from '{title}' for force crash")
                    log_error(f"WINDOW_FORCE_CRASH_FAILED: Could not extract PID from '{title}'")
            except Exception as e:
                print(f"[WINDOW-MOVER] Error force crashing '{title}': {e}")
                log_error(f"WINDOW_FORCE_CRASH_ERROR: {title} - {e}")
    
    # Summary
    print(f"[WINDOW-MOVER] Window arrangement complete: {len(successful_moves)} successful, {len(failed_moves)} failed")
    if failed_moves and DEBUG:
        for hwnd, title, reason in failed_moves:
            print(f"[WINDOW-MOVER]   Failed: '{title}' - {reason}")
    
    return len(successful_moves) > 0

def kill_process_by_pid(pid, error_tag="PROCESS"):
    """
    Kill a process by its Process ID using taskkill command.
    Returns True if successful, False otherwise.
    """
    try:
        result = subprocess.run(
            ["taskkill", "/F", "/PID", str(pid)],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Failed to kill process {pid}: {e}")
        log_error(f"{error_tag}_KILL_FAILED: PID {pid} - {e}")
        return False

def kill_process_by_image_name(image_name, error_tag="PROCESS"):
    """
    Kill a process by its image name using taskkill command.
    Returns True if successful, False otherwise.
    """
    try:
        result = subprocess.run(
            ["taskkill", "/F", "/IM", image_name],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Failed to kill {image_name}: {e}")
        log_error(f"{error_tag}_KILL_FAILED: {e}")
        return False

def cleanup_batch_launcher_processes(batch_file_path):
    """
    Clean up any lingering cmd.exe processes that were spawned to run a batch file.
    Finds cmd.exe processes with the batch file path in their command line and terminates them.
    This prevents accumulation of idle cmd.exe processes after game launches.
    
    Args:
        batch_file_path: Full path to the batch file that was launched
    """
    if not PSUTIL_AVAILABLE:
        return
    
    try:
        # Normalize the batch file path for comparison
        batch_path_lower = batch_file_path.lower()
        batch_filename = os.path.basename(batch_file_path).lower()
        killed_count = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Only check cmd.exe processes
                if proc.info['name'].lower() != 'cmd.exe':
                    continue
                
                cmdline = proc.info.get('cmdline', [])
                if not cmdline:
                    continue
                
                # Join command line and check if it contains the batch file path
                cmdline_str = ' '.join(cmdline).lower()
                
                # Check if this cmd.exe was spawned for our batch file
                if batch_path_lower in cmdline_str or batch_filename in cmdline_str:
                    proc.terminate()
                    killed_count += 1
                    if DEBUG:
                        print(f"[DEBUG] Cleaned up lingering cmd.exe (PID {proc.info['pid']}) for {batch_filename}")
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        if killed_count > 0 and DEBUG:
            print(f"[DEBUG] Cleaned up {killed_count} lingering cmd.exe process(es) for batch file launcher")
            
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error cleaning up batch launcher processes: {e}")

def is_process_running_with_visible_windows(process_name, return_pid=False):
    """
    Check if a process is running with visible windows (active app state).
    Background processes (no visible windows) are ignored.
    
    Args:
        process_name: Process name to check (e.g., 'XIVLauncher.exe')
        return_pid: If True, returns PID of first match; if False, returns bool
    
    Returns:
        If return_pid=False: True if process has visible windows, False otherwise
        If return_pid=True: PID of process with visible windows, or None if not found
    """
    if not PSUTIL_AVAILABLE:
        return None if return_pid else False
    
    try:
        process_pids = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() == process_name.lower():
                    process_pids.append(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if not process_pids:
            return None if return_pid else False
        
        for pid in process_pids:
            if has_visible_windows(pid):
                if DEBUG:
                    print(f"[DEBUG] {process_name} (PID {pid}) detected as ACTIVE APP with visible windows")
                return pid if return_pid else True
        
        if DEBUG:
            print(f"[DEBUG] {process_name} found as BACKGROUND PROCESS (no visible windows) - normal state")
        return None if return_pid else False
        
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error checking for {process_name}: {e}")
        return None if return_pid else False

def kill_ffxiv_process():
    """
    Kill FFXIV process by terminating ffxiv_dx11.exe.
    Used when USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME is True.
    Returns True if successful, False otherwise.
    """
    return kill_process_by_image_name("ffxiv_dx11.exe", "FFXIV")

def kill_game_client_and_cleanup(nickname, process_id, success_msg, fail_msg,
                                  closed_pids, game_status_dict, client_start_times,
                                  last_launch_time=None, set_launch_time=None,
                                  game_launch_timestamp=None, last_sub_processed=None,
                                  retainer_mode_active=None):
    """
    Kill a game client and perform cleanup of tracking dictionaries.
    Consolidates repeated kill/cleanup logic throughout main loop.
    
    Args:
        nickname: Account nickname
        process_id: Process ID (or None for single client mode)
        success_msg: Message to print on successful kill
        fail_msg: Message to print on failed kill
        closed_pids: Set to add process_id to on success
        game_status_dict: Dict to update with (False, None) on success
        client_start_times: Dict to clean up start time tracking
        last_launch_time: Dict to delete nickname from (if provided and not set_launch_time)
        set_launch_time: Tuple of (dict, value) to set last_launch_time[nickname] = value
        game_launch_timestamp: Dict to delete nickname from (if provided)
        last_sub_processed: Dict to delete nickname from (if provided)
        retainer_mode_active: Dict to delete nickname from (if provided)
    
    Returns:
        True if kill succeeded, False otherwise
    """
    # Use appropriate kill method based on mode
    if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
        kill_success = kill_ffxiv_process()
    else:
        kill_success = kill_process_by_pid(process_id)
    
    if kill_success:
        if process_id:
            closed_pids.add(process_id)
        print(success_msg)
        
        # Update game status immediately
        game_status_dict[nickname] = (False, None)
        
        # Handle last_launch_time (either set or delete)
        if set_launch_time:
            launch_dict, launch_value = set_launch_time
            launch_dict[nickname] = launch_value
        elif last_launch_time is not None and nickname in last_launch_time:
            del last_launch_time[nickname]
        
        # Clear force-crash tracking if provided
        if game_launch_timestamp is not None and nickname in game_launch_timestamp:
            del game_launch_timestamp[nickname]
        if last_sub_processed is not None and nickname in last_sub_processed:
            del last_sub_processed[nickname]
        if retainer_mode_active is not None and nickname in retainer_mode_active:
            del retainer_mode_active[nickname]
        
        # Clean up start time tracking
        if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
            if 'ffxiv_single' in client_start_times:
                del client_start_times['ffxiv_single']
        elif process_id and process_id in client_start_times:
            del client_start_times[process_id]
    else:
        print(fail_msg)
    
    return kill_success

def is_xivlauncher_running():
    """
    Check if XIVLauncher.exe is running as an ACTIVE APP (with visible windows).
    This is a problem state - indicates launcher UI is stuck/waiting for input.
    Background XIVLauncher process (no visible windows) is normal and ignored.
    Returns True if launcher has visible windows, False otherwise.
    """
    return is_process_running_with_visible_windows("XIVLauncher.exe", return_pid=False)

def has_visible_windows(pid):
    """
    Check if a process has any visible windows.
    Returns True if process has visible windows (is an active app), False if background only.
    """
    visible_windows = []
    all_windows_for_pid = []
    
    def enum_callback(hwnd, results):
        try:
            # Get window's process ID
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            
            # Check if this window belongs to our target process
            if window_pid == pid:
                # Get window info
                is_visible = win32gui.IsWindowVisible(hwnd)
                title = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)
                
                # Track all windows for this PID (for debug)
                all_windows_for_pid.append({
                    'hwnd': hwnd,
                    'visible': is_visible,
                    'title': title,
                    'class': class_name
                })
                
                # Check if window is visible (don't require title - some windows may not have titles yet)
                if is_visible:
                    results.append({
                        'title': title if title else '<no title>',
                        'class': class_name,
                        'hwnd': hwnd
                    })
        except Exception as e:
            if DEBUG:
                print(f"[DEBUG] Error enumerating window: {e}")
    
    try:
        win32gui.EnumWindows(enum_callback, visible_windows)
        
        if DEBUG and len(all_windows_for_pid) > 0:
            print(f"[DEBUG] Found {len(all_windows_for_pid)} total windows for PID {pid}")
            print(f"[DEBUG] Found {len(visible_windows)} visible windows for PID {pid}")
            for w in visible_windows:
                print(f"[DEBUG]   - Title: '{w['title']}', Class: {w['class']}, HWND: {w['hwnd']}")
        
        return len(visible_windows) > 0
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error in has_visible_windows: {e}")
        return False

def kill_xivlauncher_process():
    """
    Kill XIVLauncher.exe process.
    Returns True if successful, False otherwise.
    """
    return kill_process_by_image_name("XIVLauncher.exe", "LAUNCHER")

def is_dalamud_crash_handler_running():
    """
    Check if DalamudCrashHandler.exe is running as an ACTIVE APP (with visible windows).
    This is a problem state - indicates a game crash occurred with crash handler UI open.
    Background DalamudCrashHandler processes (no visible windows) are normal and ignored.
    Returns PID of crash handler with visible windows, or None if no active window found.
    """
    return is_process_running_with_visible_windows("DalamudCrashHandler.exe", return_pid=True)

def kill_dalamud_crash_handler_process(pid):
    """
    Kill a specific DalamudCrashHandler.exe process by PID.
    Only kills the crash handler with visible window, not background processes.
    Returns True if successful, False otherwise.
    """
    return kill_process_by_pid(pid, "CRASH_HANDLER")

def launch_game(nickname):
    """
    Launch the game for a specific account using the configured launcher path.
    If 2FA is enabled for the account, automatically sends the OTP code after launch.
    Returns True if successfully launched, False otherwise.
    """
    # Validate and fix launcher config BEFORE launching
    # This ensures AutologinEnabled and OtpServerEnabled are set correctly
    if ENABLE_AUTOLOGIN_UPDATER:
        validate_launcher_config_before_launch(nickname)
    
    launcher_path = GAME_LAUNCHERS.get(nickname)
    
    if not launcher_path:
        print(f"[ERROR] No launcher path configured for {nickname}")
        log_error(f"LAUNCH_FAILED_NO_PATH: {nickname} - No launcher path configured in GAME_LAUNCHERS")
        return False
    
    if not os.path.exists(launcher_path):
        print(f"[ERROR] Launcher not found: {launcher_path}")
        log_error(f"LAUNCH_FAILED_NOT_FOUND: {nickname} - Launcher not found at {launcher_path}")
        return False
    
    try:
        # Check if it's a batch file
        is_batch_file = launcher_path.lower().endswith('.bat')
        
        if is_batch_file:
            # For batch files, run via cmd.exe /c which closes after execution
            # DETACHED_PROCESS ensures the cmd.exe doesn't stay attached to Python
            # After a short delay, cleanup any lingering cmd.exe processes for this batch file
            DETACHED_PROCESS = 0x00000008
            subprocess.Popen(
                f'cmd.exe /c "{launcher_path}"',
                shell=False,
                creationflags=DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # Schedule cleanup of any lingering cmd.exe processes after game starts
            # This runs in a separate thread to not block the main script
            def delayed_cleanup():
                time.sleep(30)  # Wait for game to fully launch
                cleanup_batch_launcher_processes(launcher_path)
            cleanup_thread = threading.Thread(target=delayed_cleanup, daemon=True)
            cleanup_thread.start()
        else:
            # For executables, use normal Popen
            subprocess.Popen(
                [launcher_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )

        # Check if 2FA is enabled for this account
        account_config = None
        for acc_item in account_locations:
            if acc_item["nickname"] == nickname:
                account_config = acc_item
                break

        if account_config and account_config.get("enable_2fa", False):
            if not PYOTP_AVAILABLE:
                print(f"[WARNING] 2FA enabled for {nickname} but pyotp/keyring not installed - skipping OTP")
                log_error(f"2FA_NOT_AVAILABLE: {nickname} - pyotp/keyring not installed")
                return True  # Continue launch, let user manually enter OTP

            keyring_name = account_config.get("keyring_name")
            if not keyring_name:
                print(f"[WARNING] 2FA enabled for {nickname} but no keyring_name specified - skipping OTP")
                log_error(f"2FA_CONFIG_ERROR: {nickname} - no keyring_name specified")
                return True  # Continue launch, let user manually enter OTP

            # Wait for launcher to initialize
            print(f"[2FA] Waiting {OTP_LAUNCH_DELAY} seconds for launcher to initialize...")
            time.sleep(OTP_LAUNCH_DELAY)

            # Get OTP secret from keyring
            otp_secret = keyring.get_password(keyring_name, "otp_secret")
            if not otp_secret:
                print(f"[WARNING] OTP secret not found in keyring '{keyring_name}' for {nickname}")
                print(f"[WARNING] Aborting launch - please run Set_2FA_Key.py to store your OTP secret")
                log_error(f"2FA_KEYRING_ERROR: {nickname} - no OTP secret in keyring '{keyring_name}'")
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
                    print(f"[2FA] OTP code accepted for {nickname}")
                else:
                    print(f"[2FA] Unexpected response: {resp.status_code}")
                    log_error(f"2FA_UNEXPECTED_RESPONSE: {nickname} - Status {resp.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"[2FA] Failed to send OTP code: {e}")
                log_error(f"2FA_SEND_FAILED: {nickname} - {e}")
                # Don't return False - launcher may still accept manual input

        return True
    except Exception as e:
        print(f"[ERROR] Failed to launch game for {nickname}: {e}")
        log_error(f"LAUNCH_FAILED_EXCEPTION: {nickname} - {e}")
        return False

def get_process_start_time(pid):
    """
    Get the actual start time of a process from Windows using psutil.
    Returns the start time as a timestamp (seconds since epoch) or None if unavailable.
    """
    if not PSUTIL_AVAILABLE:
        return None
    
    try:
        process = psutil.Process(int(pid))
        # create_time() returns seconds since epoch
        return process.create_time()
    except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError) as e:
        if DEBUG:
            print(f"[DEBUG] Could not get start time for PID {pid}: {e}")
        return None

def get_process_start_time_by_name(process_name):
    """
    Get the start time of a process by its name using psutil.
    Returns the start time as a timestamp (seconds since epoch) or None if unavailable.
    """
    if not PSUTIL_AVAILABLE:
        return None
    
    try:
        for proc in psutil.process_iter(['name', 'create_time']):
            try:
                if proc.info['name'].lower() == process_name.lower():
                    return proc.info['create_time']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Could not find {process_name} process: {e}")
        return None

def get_ffxiv_process_start_time():
    """
    Get the start time of the ffxiv_dx11.exe process for single client mode.
    Returns the start time as a timestamp (seconds since epoch) or None if unavailable.
    Used when USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME is True.
    """
    return get_process_start_time_by_name("ffxiv_dx11.exe")


def is_ffxiv_running_for_account(nickname):
    """
    Check if FFXIV is running for a specific account.
    
    If USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME is True:
        - Looks for window with title "FINAL FANTASY XIV"
        - Returns (is_running, None) - process_id is always None
    
    If USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME is False:
        - Looks for windows with titles matching pattern: 'ProcessID - nickname'
        - Returns (is_running, process_id) - process_id extracted from window title
    
    Returns tuple: (is_running, process_id)
    - is_running: True if a matching window is found, False otherwise
    - process_id: The process ID if running (or None in single client mode)
    """
    try:
        found_windows = []
        
        def enum_callback(hwnd, extra):
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title.strip():
                    found_windows.append(title)
        
        win32gui.EnumWindows(enum_callback, None)
        
        if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
            # Single client mode: Check if any window title is exactly "FINAL FANTASY XIV"
            for title in found_windows:
                if title.strip() == "FINAL FANTASY XIV":
                    return (True, None)
            return (False, None)
        else:
            # Multi-client mode: Check if any window title matches the pattern: "ProcessID - nickname"
            # Example: "3056 - Main", "58696 - Acc1", etc.
            import re
            # Pattern: digits, space, dash, space, nickname
            pattern = re.compile(rf"^(\d+)\s-\s{re.escape(nickname)}$", re.IGNORECASE)
            
            for title in found_windows:
                match = pattern.match(title)
                if match:
                    process_id = match.group(1)  # Extract the process ID
                    return (True, process_id)
            
            return (False, None)
    except Exception as e:
        # If we can't check window status, assume not running
        return (False, None)

def check_for_default_ffxiv_window():
    """
    Check if any window has the default "FINAL FANTASY XIV" title.
    This indicates the plugin hasn't updated the window title yet.
    
    Returns True if default title found, False otherwise.
    """
    try:
        found_default = False
        
        def enum_callback(hwnd, extra):
            nonlocal found_default
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title.strip() == "FINAL FANTASY XIV":
                    found_default = True
        
        win32gui.EnumWindows(enum_callback, None)
        return found_default
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error checking for default FFXIV window: {e}")
        return False

def wait_for_window_title_update(nickname, launcher_retry_count):
    """
    Wait for a launched game's window title to update from "FINAL FANTASY XIV" to "ProcessID - nickname".
    This ensures plugins have loaded and the window can be properly identified.
    Also monitors for XIVLauncher.exe opening instead of the game.
    
    Args:
        nickname: The account nickname to wait for
        launcher_retry_count: Current launcher retry attempt count
    
    Returns: Tuple (success, needs_launcher_retry)
        - success: True when title successfully updates, False if max attempts reached
        - needs_launcher_retry: True if launcher detected and retry is needed
    """
    if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
        # Single client mode: still check for launcher even though we use default title
        check_count = 0
        while check_count < MAX_WINDOW_TITLE_RESCAN:
            # Check if launcher opened instead of game
            if is_xivlauncher_running():
                print(f"[LAUNCHER-CHECK] XIVLauncher.exe detected instead of game for {nickname}")
                return (False, True)  # Needs launcher retry
            
            # Check if game window exists (default title in single mode)
            has_default_title = check_for_default_ffxiv_window()
            if has_default_title:
                if DEBUG:
                    print(f"[WINDOW-TITLE] {nickname} game window detected (single client mode)")
                return (True, False)
            
            # Check if game process is running
            is_running, _ = is_ffxiv_running_for_account(nickname)
            if is_running:
                if DEBUG:
                    print(f"[WINDOW-TITLE] {nickname} game process detected")
                return (True, False)
            
            time.sleep(WINDOW_TITLE_RESCAN)
            check_count += 1
        
        # Max attempts reached - check one more time for launcher
        if is_xivlauncher_running():
            print(f"[LAUNCHER-CHECK] XIVLauncher.exe detected instead of game for {nickname}")
            return (False, True)
        
        print(f"[WINDOW-TITLE] Max attempts ({MAX_WINDOW_TITLE_RESCAN}) reached for {nickname}, will restart launch")
        return (False, False)
    
    # Multi-client mode
    check_count = 0
    
    while check_count < MAX_WINDOW_TITLE_RESCAN:
        # Check if launcher opened instead of game
        if is_xivlauncher_running():
            print(f"[LAUNCHER-CHECK] XIVLauncher.exe detected instead of game for {nickname}")
            return (False, True)  # Needs launcher retry
        
        # Check if default window exists
        has_default_title = check_for_default_ffxiv_window()
        
        if not has_default_title:
            # Default title is gone, check if our custom title exists
            is_running, process_id = is_ffxiv_running_for_account(nickname)
            if is_running and process_id:
                if DEBUG:
                    print(f"[WINDOW-TITLE] {nickname} window title updated to: {process_id} - {nickname}")
                return (True, False)
            elif DEBUG:
                print(f"[WINDOW-TITLE] Check #{check_count + 1}: Default title gone but custom title not found yet for {nickname}")
        else:
            if DEBUG:
                print(f"[WINDOW-TITLE] Check #{check_count + 1}: Default 'FINAL FANTASY XIV' title still active, waiting for plugin update...")
        
        # Wait before next check
        time.sleep(WINDOW_TITLE_RESCAN)
        check_count += 1
    
    # Max attempts reached - check one more time for launcher
    if is_xivlauncher_running():
        print(f"[LAUNCHER-CHECK] XIVLauncher.exe detected instead of game for {nickname}")
        return (False, True)
    
    # Max attempts reached without successful title update
    print(f"[WINDOW-TITLE] Max attempts ({MAX_WINDOW_TITLE_RESCAN}) reached for {nickname}, will restart launch")
    return (False, False)

def get_submarine_timers_for_account(account_entry):
    """
    Get all submarine timers for a single account.
    Returns dict with account info and submarine data.
    """
    nickname = account_entry["nickname"]
    auto_path = account_entry["auto_path"]
    include_subs = account_entry.get("include_submarines", True)
    
    result = {
        "nickname": nickname,
        "include_submarines": include_subs,
        "total_subs": 0,
        "ready_subs": 0,
        "soonest_hours": None,
        "characters": [],
        "sub_builds": [],  # Track submarine builds for gil calculation
        "sub_plans": [],   # Track submarine plan names for plan-based gil calculation
        "total_ceruleum": 0,  # Total tanks across all characters
        "total_repair_kits": 0,  # Total repair kits across all characters
        "days_until_restocking": None,  # Minimum days until restocking needed
        "lowest_inventory_space": None,  # Lowest inventory space among sub-only farmer characters
        "lowest_retainer_inventory_space": None,  # Lowest inventory space among retainer farmer characters
        "ready_retainers": 0,  # Count of retainers with completed ventures
        "total_retainers": 0,  # Total retainers on ventures
        "soonest_retainer_hours": None  # Soonest retainer venture completion time
    }
    
    if not include_subs:
        return result
    
    if not os.path.isfile(auto_path):
        return result
    
    try:
        with open(auto_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        
        # Build plan name cache from this config
        build_plan_name_cache(data)
        
        chars = collect_characters(data, account_nickname=nickname)
        current_time = datetime.datetime.now().timestamp()
        
        all_return_times = []
        
        # Collect inventory data for restocking calculation
        character_days_remaining = []
        farmer_inventory_spaces = []  # Track inventory spaces for characters with submarines (no retainers)
        retainer_farmer_inventory_spaces = []  # Track inventory spaces for characters with retainers
        all_retainer_times = []  # Track retainer venture completion times
        
        for char in chars:
            # Collect inventory from character
            ceruleum = char.get("Ceruleum", 0)
            repair_kits = char.get("RepairKits", 0)
            result["total_ceruleum"] += ceruleum
            result["total_repair_kits"] += repair_kits
            
            # Get submarine build data from AdditionalSubmarineData
            # Process all submarines (including renamed ones) by matching via OfflineSubmarineData
            sub_info = char.get("AdditionalSubmarineData", {})
            offline_sub_data = char.get("OfflineSubmarineData", [])
            
            # Collect builds for this character
            char_builds = []
            
            # First pass: Collect submarine builds and plan names from all submarines
            for offline_sub in offline_sub_data:
                sub_name = offline_sub.get("Name", "")
                # Look up build data using the submarine's actual name
                if sub_name in sub_info:
                    parts_str = get_sub_parts_string(sub_info[sub_name])
                    if parts_str:
                        result["sub_builds"].append(parts_str)
                        char_builds.append(parts_str)
                        # Get plan name for this submarine (only when build is found)
                        plan_name = get_submarine_plan_name(sub_info[sub_name])
                        result["sub_plans"].append(plan_name)
            
            # Calculate consumption rates for this character's submarines
            if char_builds:
                total_tanks_per_day = 0
                total_kits_per_day = 0
                for build in char_builds:
                    if build in build_consumption_rates:
                        total_tanks_per_day += build_consumption_rates[build]["tanks_per_day"]
                        total_kits_per_day += build_consumption_rates[build]["kits_per_day"]
                    else:
                        # Default consumption for unlisted builds (leveling submarines, etc.)
                        # Use basic OJ route consumption: 9 tanks/day, 1.33 kits/day
                        total_tanks_per_day += 9.0
                        total_kits_per_day += 1.33
                
                # Calculate days remaining for this character
                if total_tanks_per_day > 0 and total_kits_per_day > 0:
                    days_from_tanks = ceruleum / total_tanks_per_day if ceruleum > 0 else 0
                    days_from_kits = repair_kits / total_kits_per_day if repair_kits > 0 else 0
                    days_for_char = int(min(days_from_tanks, days_from_kits))  # Round down to lowest solid number
                    character_days_remaining.append(days_for_char)
                
                # Track inventory space for submarine-only farmers (excludes characters with retainers)
                # Characters with retainers have fluctuating inventory due to retainer item collection
                # InventorySpace is total 140, value shows remaining available slots
                retainer_data = char.get("RetainerData", [])
                inventory_space = char.get("InventorySpace", 0)
                if not retainer_data:  # Track sub-only farmers (no retainers)
                    farmer_inventory_spaces.append(inventory_space)
                else:  # Track retainer farmers
                    retainer_farmer_inventory_spaces.append(inventory_space)
            
            # Collect retainer venture data (retainer_data already fetched above if char_builds exists)
            if not char_builds:
                retainer_data = char.get("RetainerData", [])
            for ret in retainer_data:
                has_venture = ret.get("HasVenture", False)
                venture_ends_at = ret.get("VentureEndsAt", 0)
                
                if has_venture and venture_ends_at > 0:
                    result["total_retainers"] += 1
                    # Convert to hours remaining (can be negative if already returned)
                    hours_remaining = (venture_ends_at - current_time) / 3600
                    all_retainer_times.append(hours_remaining)
                    
                    # Count ready retainers (negative hours means venture completed)
                    if hours_remaining < 0:
                        result["ready_retainers"] += 1
            
            # Second pass: Get submarine return times
            for sub_dict in offline_sub_data:
                sub_name = sub_dict.get("Name", "")
                return_timestamp = sub_dict.get("ReturnTime", 0)
                
                if return_timestamp > 0:
                    # Convert to hours remaining (can be negative if already returned)
                    hours_remaining = (return_timestamp - current_time) / 3600
                    all_return_times.append(hours_remaining)
                    result["total_subs"] += 1
                    
                    # Count ready submarines (negative hours means already returned)
                    if hours_remaining < 0:
                        result["ready_subs"] += 1
        
        # Find the soonest submarine (minimum time)
        if all_return_times:
            result["soonest_hours"] = min(all_return_times)
        
        # Calculate minimum days until restocking across all characters
        if character_days_remaining:
            result["days_until_restocking"] = min(character_days_remaining)
        
        # Calculate lowest inventory space among farmer characters
        if farmer_inventory_spaces:
            result["lowest_inventory_space"] = min(farmer_inventory_spaces)
        
        # Calculate lowest inventory space among retainer farmer characters
        if retainer_farmer_inventory_spaces:
            result["lowest_retainer_inventory_space"] = min(retainer_farmer_inventory_spaces)
        
        # Find the soonest retainer venture completion
        if all_retainer_times:
            result["soonest_retainer_hours"] = min(all_retainer_times)
    
    except Exception as e:
        print(f"[ERROR] Failed to process {nickname}: {e}")
    
    return result

def detect_retainer_processing(account_entry, retainer_state_cache, current_time):
    """
    Detect retainer processing by comparing cached retainer venture times to current times.
    Similar to submarine processing detection - tracks changes in ready count and nearest timer.
    
    Args:
        account_entry: Dictionary with account information including auto_path
        retainer_state_cache: Dictionary caching previous retainer state by nickname
        current_time: Current timestamp for calculating venture times
    
    Returns:
        int: Number of retainers processed (detected by ready count decrease or timer change)
    """
    nickname = account_entry["nickname"]
    auto_path = account_entry["auto_path"]
    
    if not os.path.isfile(auto_path):
        return 0
    
    try:
        with open(auto_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        
        chars = collect_characters(data, account_nickname=nickname)
        current_retainer_times = []  # List of (retainer_name, hours_remaining) tuples
        
        for char in chars:
            retainer_data = char.get("RetainerData", [])
            
            for ret in retainer_data:
                ret_name = ret.get("Name", "")
                has_venture = ret.get("HasVenture", False)
                venture_ends_at = ret.get("VentureEndsAt", 0)
                
                if has_venture and venture_ends_at > 0:
                    # Convert to hours remaining (can be negative if already returned)
                    hours_remaining = (venture_ends_at - current_time) / 3600
                    current_retainer_times.append((ret_name, hours_remaining))
        
        # Count current retainer states
        ready_retainers = sum(1 for _, hours in current_retainer_times if hours < 0)
        on_venture_retainers = sum(1 for _, hours in current_retainer_times if hours > 0)
        
        # Find the nearest timer (soonest retainer)
        nearest_timer = min([hours for _, hours in current_retainer_times], default=None)
        
        # Get cached state for this account
        cached_state = retainer_state_cache.get(nickname, {})
        
        # If cache is empty, initialize it but don't count anything as processed
        if not cached_state:
            retainer_state_cache[nickname] = {
                'ready_count': ready_retainers,
                'on_venture_count': on_venture_retainers,
                'nearest_timer': nearest_timer
            }
            if DEBUG:
                print(f"[DEBUG] {nickname}: Initializing retainer cache - {ready_retainers} ready, {on_venture_retainers} on venture")
            return 0
        
        # Calculate processed count using multiple metrics:
        # 1. Decrease in ready retainers (retainers sent without new returns)
        # 2. Increase in on-venture retainers (retainers sent even if others returned)
        # 3. Change in nearest timer to a different character (indicates processing even if counts same)
        previous_ready = cached_state.get('ready_count', ready_retainers)
        previous_on_venture = cached_state.get('on_venture_count', on_venture_retainers)
        previous_nearest = cached_state.get('nearest_timer', nearest_timer)
        
        ready_decreased = max(0, previous_ready - ready_retainers)
        on_venture_increased = max(0, on_venture_retainers - previous_on_venture)
        
        # Detect timer change: if the nearest timer changed significantly (more than expected from time passing)
        # This catches cases where 20 retainers are processed and 20 come in (count stays same but timer changes)
        timer_change_detected = 0
        if previous_nearest is not None and nearest_timer is not None:
            # Expected change is just time passing (should be negative as time progresses)
            time_elapsed_hours = (current_time - cached_state.get('last_check_time', current_time)) / 3600
            expected_nearest = previous_nearest - time_elapsed_hours
            
            # If the nearest timer is significantly higher than expected, retainers were processed
            # (new retainer became the nearest, meaning previous nearest was sent out)
            if nearest_timer > expected_nearest + 0.1:  # 0.1 hour tolerance (6 min)
                timer_change_detected = 1
                if DEBUG:
                    print(f"[DEBUG] {nickname}: Retainer timer change detected - expected {expected_nearest:.2f}h, got {nearest_timer:.2f}h")
        
        # Use the LARGER of the metrics to detect activity
        processed_count = max(ready_decreased, on_venture_increased, timer_change_detected)
        
        # Update cache with current state
        retainer_state_cache[nickname] = {
            'ready_count': ready_retainers,
            'on_venture_count': on_venture_retainers,
            'nearest_timer': nearest_timer,
            'last_check_time': current_time
        }
        
        # Enhanced debug output
        if DEBUG and processed_count > 0:
            print(f"[DEBUG] {nickname}: {ready_retainers} ret. ready, {on_venture_retainers} on venture, {processed_count} processed this scan")
        
        return processed_count
    
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error detecting retainer processing for {nickname}: {e}")
        return 0

def detect_submarine_processing(account_entry, submarine_state_cache, current_time):
    """
    Detect submarine processing by comparing cached submarine return times to current times.
    Returns the number of submarines that transitioned from negative (ready) to positive (sent out) since last scan.
    
    Args:
        account_entry: Dictionary with account information including auto_path
        submarine_state_cache: Dictionary caching previous submarine return times by nickname
        current_time: Current timestamp for calculating return times
    
    Returns:
        int: Number of submarines processed (negative -> positive transitions)
    """
    nickname = account_entry["nickname"]
    auto_path = account_entry["auto_path"]
    
    if not os.path.isfile(auto_path):
        return 0
    
    try:
        with open(auto_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        
        chars = collect_characters(data, account_nickname=nickname)
        current_return_times = []  # List of (sub_name, hours_remaining) tuples
        
        for char in chars:
            offline_sub_data = char.get("OfflineSubmarineData", [])
            
            for sub_dict in offline_sub_data:
                sub_name = sub_dict.get("Name", "")
                return_timestamp = sub_dict.get("ReturnTime", 0)
                
                if return_timestamp > 0:
                    # Convert to hours remaining (can be negative if already returned)
                    hours_remaining = (return_timestamp - current_time) / 3600
                    current_return_times.append((sub_name, hours_remaining))
        
        # Count current submarine states
        ready_subs = sum(1 for _, hours in current_return_times if hours < 0)
        voyaging_subs = sum(1 for _, hours in current_return_times if hours > 0)
        
        # Get cached ready count for this account
        cached_state = submarine_state_cache.get(nickname, {})
        
        # If cache is empty, initialize it but don't count anything as processed
        if not cached_state:
            submarine_state_cache[nickname] = {
                'ready_count': ready_subs,
                'voyaging_count': voyaging_subs
            }
            if DEBUG:
                print(f"[DEBUG] {nickname}: Initializing cache - {ready_subs} ready, {voyaging_subs} voyaging, 0 newly sent")
            return 0
        
        # Calculate processed count using BOTH metrics:
        # 1. Decrease in ready submarines (subs sent without new returns)
        # 2. Increase in voyaging submarines (subs sent even if others returned)
        # This catches cases where subs return at same rate they're being sent
        previous_ready = cached_state.get('ready_count', ready_subs)
        previous_voyaging = cached_state.get('voyaging_count', voyaging_subs)
        
        ready_decreased = max(0, previous_ready - ready_subs)
        voyaging_increased = max(0, voyaging_subs - previous_voyaging)
        
        # Use the LARGER of the two metrics to detect activity
        # This handles both scenarios:
        # - Subs sent without returns: ready decreases
        # - Subs sent with simultaneous returns: voyaging increases
        processed_count = max(ready_decreased, voyaging_increased)
        
        # Update cache with current counts
        submarine_state_cache[nickname] = {
            'ready_count': ready_subs,
            'voyaging_count': voyaging_subs
        }
        
        # Enhanced debug output
        if DEBUG and processed_count > 0:
            print(f"[DEBUG] {nickname}: {ready_subs} ready, {voyaging_subs} voyaging, {processed_count} newly sent this scan")
        
        return processed_count
    
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error detecting submarine processing for {nickname}: {e}")
        return 0

def format_hours(hours, ready_count=0, is_running=False, force247uptime=False, ready_retainers=0, soonest_retainer_hours=None):
    """Format hours with + prefix for positive values and ready count.
    When force247uptime=True and no subs ready but retainers ready, show (xx Ret.) instead.
    When force247uptime=True and no retainers ready but retainers on ventures, show retainer timer.
    """
    if hours is None:
        return "N/A"
    if hours >= 0:
        # For force247uptime accounts with ready retainers but no ready subs, show retainer count
        # This shows (xx Ret.) regardless of hours threshold since retainers need processing
        if is_running and ready_count == 0 and force247uptime and ready_retainers > 0:
            return f"+{hours:.1f} hours ({ready_retainers} Ret.)"
        # For force247uptime accounts with no ready retainers but retainers on ventures, show retainer timer
        if is_running and ready_count == 0 and force247uptime and ready_retainers == 0 and soonest_retainer_hours is not None:
            # Convert hours to minutes for retainer timer display
            retainer_minutes = soonest_retainer_hours * 60
            if retainer_minutes < 0:
                return f"+{hours:.1f} hours ({int(retainer_minutes)}min)"
            else:
                return f"+{hours:.1f} hours (+{int(retainer_minutes)}min)"
        # Show (WAITING) when game is running with 0 ready subs and within threshold
        if is_running and ready_count == 0 and hours <= AUTO_CLOSE_THRESHOLD:
            return f"+{hours:.1f} hours (WAITING)"
        return f"+{hours:.1f} hours"
    else:
        # Negative means already returned
        return f"{hours:.1f} hours ({ready_count} READY)"

def display_submarine_timers(game_status_dict=None, client_start_times=None, launcher_failed_accounts=None, last_sub_processed=None, retainer_mode_active=None):
    """Display submarine timers for all accounts"""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Use empty dict/set if none provided
    if game_status_dict is None:
        game_status_dict = {}
    if client_start_times is None:
        client_start_times = {}
    if launcher_failed_accounts is None:
        launcher_failed_accounts = set()
    if last_sub_processed is None:
        last_sub_processed = {}
    if retainer_mode_active is None:
        retainer_mode_active = {}
    
    print("=" * 85)
    print(f"Auto-Autoretainer {VERSION}{VERSION_SUFFIX}\nFFXIV Game Instance Manager")
    print("=" * 85)
    print(f"Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 85)
    print()
    
    account_data = []
    total_ready_subs = 0
    total_all_subs = 0
    all_builds = []
    all_plans = []  # Track plan names for plan-based gil calculation
    all_days_remaining = []
    all_inventory_spaces = []  # Track inventory spaces for sub-only farmer characters
    all_retainer_inventory_spaces = []  # Track inventory spaces for retainer farmer characters
    
    for account_entry in account_locations:
        timer_data = get_submarine_timers_for_account(account_entry)
        account_data.append(timer_data)
        total_ready_subs += timer_data["ready_subs"]
        total_all_subs += timer_data["total_subs"]
        all_builds.extend(timer_data["sub_builds"])
        all_plans.extend(timer_data.get("sub_plans", []))
        if timer_data.get("days_until_restocking") is not None:
            all_days_remaining.append(timer_data["days_until_restocking"])
        if timer_data.get("lowest_inventory_space") is not None:
            all_inventory_spaces.append(timer_data["lowest_inventory_space"])
        if timer_data.get("lowest_retainer_inventory_space") is not None:
            all_retainer_inventory_spaces.append(timer_data["lowest_retainer_inventory_space"])
    
    # Display results
    for data in account_data:
        nickname = data["nickname"]
        total_subs = data["total_subs"]
        ready_subs = data["ready_subs"]
        soonest_hours = data["soonest_hours"]
        ready_retainers = data.get("ready_retainers", 0)
        soonest_retainer_hours = data.get("soonest_retainer_hours")
        
        if not data["include_submarines"]:
            # Show game status even with submarines disabled (for force247uptime monitoring)
            subs_disabled_str = "Disabled"
            
            # Check if account has launcher failures
            if nickname in launcher_failed_accounts:
                status_str = f"{'[LAUNCHER]':{STATUS_WIDTH}s}"
                print(f"{nickname:{NICKNAME_WIDTH}s} {subs_disabled_str:{SUBS_COUNT_WIDTH}s}:{'':{HOURS_WIDTH+1}s}{status_str}")
                continue
            
            # Get game status and force247uptime flag
            force247 = account_locations[[i for i, acc in enumerate(account_locations) if acc["nickname"] == nickname][0]].get("force247uptime", False)
            game_info = game_status_dict.get(nickname, (None, None))
            is_running = game_info[0]
            process_id = game_info[1]
            
            status_str = ""
            pid_uptime_str = ""
            if is_running is not None:
                if is_running:
                    # Show [Up 24/7] if force247uptime is True, otherwise [Running]
                    if force247:
                        status_str = f"{'[Up 24/7]':{STATUS_WIDTH}s}"
                    else:
                        status_str = f"{'[Running]':{STATUS_WIDTH}s}"
                    
                    # Handle PID and uptime display differently based on mode
                    if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
                        # Single client mode: get actual PID from process and use 'ffxiv_single' for start time
                        if PSUTIL_AVAILABLE:
                            try:
                                for proc in psutil.process_iter(['pid', 'name']):
                                    if proc.info['name'].lower() == 'ffxiv_dx11.exe':
                                        actual_pid = proc.info['pid']
                                        pid_part = f"PID: {actual_pid}"
                                        pid_formatted = f"{pid_part:{PID_WIDTH}s}"
                                        
                                        # Calculate uptime using 'ffxiv_single' key
                                        current_time = time.time()
                                        start_time = client_start_times.get('ffxiv_single')
                                        if start_time is not None:
                                            uptime_hours = (current_time - start_time) / 3600.0
                                            uptime_part = f"UPTIME: {uptime_hours:.1f} hrs"
                                            pid_uptime_str = f"{pid_formatted}{uptime_part}"
                                        else:
                                            pid_uptime_str = pid_formatted
                                        break
                            except Exception:
                                pass
                    else:
                        # Multi-client mode: use PID from window detection
                        if process_id:
                            pid_part = f"PID: {process_id}"
                            pid_formatted = f"{pid_part:{PID_WIDTH}s}"
                            
                            # Calculate uptime if we have start time
                            current_time = time.time()
                            start_time = client_start_times.get(process_id)
                            if start_time is not None:
                                uptime_hours = (current_time - start_time) / 3600.0
                                uptime_part = f"UPTIME: {uptime_hours:.1f} hrs"
                                pid_uptime_str = f"{pid_formatted}{uptime_part}"
                            else:
                                pid_uptime_str = pid_formatted
                else:
                    # Show [Up 24/7] if force247uptime is True, otherwise [Closed]
                    if force247:
                        status_str = f"{'[Up 24/7]':{STATUS_WIDTH}s}"
                    else:
                        status_str = f"{'[Closed]':{STATUS_WIDTH}s}"
            
            # Use same formatting structure as other entries for proper alignment
            print(f"{nickname:{NICKNAME_WIDTH}s} {subs_disabled_str:{SUBS_COUNT_WIDTH}s}:{'':{HOURS_WIDTH+1}s}{status_str}{pid_uptime_str}")
        elif total_subs == 0:
            no_subs_str = "No submarines found"
            print(f"{nickname:{NICKNAME_WIDTH}s} {no_subs_str:{SUBS_COUNT_WIDTH}s}  {'':{HOURS_WIDTH}s}")
        else:
            # Check if account has launcher failures
            if nickname in launcher_failed_accounts:
                # Get force247uptime flag for retainer display
                force247 = account_locations[[i for i, acc in enumerate(account_locations) if acc["nickname"] == nickname][0]].get("force247uptime", False)
                hours_str = format_hours(soonest_hours, ready_subs, is_running=False, force247uptime=force247, ready_retainers=ready_retainers, soonest_retainer_hours=soonest_retainer_hours)
                subs_str = f"({total_subs} subs)"
                status_str = f"{'[LAUNCHER]':{STATUS_WIDTH}s}"
                print(f"{nickname:{NICKNAME_WIDTH}s} {subs_str:{SUBS_COUNT_WIDTH}s}: {hours_str:{HOURS_WIDTH}s}{status_str}")
                continue
            
            # Get game status for this account (only show for enabled submarines)
            # Check force247uptime flag to determine status display
            force247 = account_locations[[i for i, acc in enumerate(account_locations) if acc["nickname"] == nickname][0]].get("force247uptime", False)
            game_info = game_status_dict.get(nickname, (None, None))
            is_running = game_info[0]
            process_id = game_info[1]
            
            status_str = ""
            pid_uptime_str = ""
            if is_running is not None:
                if is_running:
                    # Show [Up 24/7] if force247uptime is True, otherwise [Running]
                    if force247:
                        status_str = f"{'[Up 24/7]':{STATUS_WIDTH}s}"
                    else:
                        status_str = f"{'[Running]':{STATUS_WIDTH}s}"
                    
                    # Handle PID and uptime display differently based on mode
                    if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
                        # Single client mode: get actual PID from process and use 'ffxiv_single' for start time
                        if PSUTIL_AVAILABLE:
                            try:
                                for proc in psutil.process_iter(['pid', 'name']):
                                    if proc.info['name'].lower() == 'ffxiv_dx11.exe':
                                        actual_pid = proc.info['pid']
                                        pid_part = f"PID: {actual_pid}"
                                        pid_formatted = f"{pid_part:{PID_WIDTH}s}"
                                        
                                        # Calculate uptime using 'ffxiv_single' key
                                        current_time = time.time()
                                        start_time = client_start_times.get('ffxiv_single')
                                        if start_time is not None:
                                            uptime_hours = (current_time - start_time) / 3600.0
                                            uptime_part = f"UPTIME: {uptime_hours:.1f} hrs"
                                            pid_uptime_str = f"{pid_formatted}{uptime_part}"
                                        else:
                                            pid_uptime_str = pid_formatted
                                        
                                        # Add force-crash timer display (X:xx minutes remaining)
                                        if nickname in last_sub_processed:
                                            minutes_since = (current_time - last_sub_processed[nickname]) / 60
                                            currently_retainer = (ready_subs == 0 and force247 and ready_retainers > 0)
                                            in_retainer_mode = currently_retainer or (retainer_mode_active.get(nickname, False) and ready_subs > 0)
                                            threshold = FORCE_CRASH_RETAINER_MINUTES if in_retainer_mode else FORCE_CRASH_INACTIVITY_MINUTES
                                            remaining = threshold - minutes_since
                                            pid_uptime_str += f" X:{remaining:.0f}"
                                        break
                            except Exception:
                                pass
                    elif process_id:
                        # Multi-client mode: use process_id from window title
                        pid_part = f"PID: {process_id}"
                        pid_formatted = f"{pid_part:{PID_WIDTH}s}"
                        
                        # Calculate uptime in hours
                        current_time = time.time()
                        start_time = client_start_times.get(process_id)
                        if start_time is not None:
                            uptime_hours = (current_time - start_time) / 3600.0
                            uptime_part = f"UPTIME: {uptime_hours:.1f} hrs"
                            pid_uptime_str = f"{pid_formatted}{uptime_part}"
                        else:
                            pid_uptime_str = pid_formatted
                        
                        # Add force-crash timer display (X:xx minutes remaining)
                        if nickname in last_sub_processed:
                            minutes_since = (current_time - last_sub_processed[nickname]) / 60
                            # Determine threshold: retainer mode (20min) or submarine mode (10min)
                            currently_retainer = (ready_subs == 0 and force247 and ready_retainers > 0)
                            in_retainer_mode = currently_retainer or (retainer_mode_active.get(nickname, False) and ready_subs > 0)
                            threshold = FORCE_CRASH_RETAINER_MINUTES if in_retainer_mode else FORCE_CRASH_INACTIVITY_MINUTES
                            remaining = threshold - minutes_since
                            pid_uptime_str += f" X:{remaining:.0f}"
                else:
                    # Show [Up 24/7] if force247uptime is True, otherwise [Closed]
                    if force247:
                        status_str = f"{'[Up 24/7]':{STATUS_WIDTH}s}"
                    else:
                        status_str = f"{'[Closed]':{STATUS_WIDTH}s}"
            
            hours_str = format_hours(soonest_hours, ready_subs, is_running=(is_running if is_running is not None else False), force247uptime=force247, ready_retainers=ready_retainers, soonest_retainer_hours=soonest_retainer_hours)
            subs_str = f"({total_subs} subs)"
            print(f"{nickname:{NICKNAME_WIDTH}s} {subs_str:{SUBS_COUNT_WIDTH}s}: {hours_str:{HOURS_WIDTH}s}{status_str}{pid_uptime_str}")
    
    print()
    print("=" * 85)
    
    # Calculate total daily gil earnings and submarine counts
    # Priority: 1) Plan-based rates from submarine_plans["farming"]
    #           2) Build-based rates from build_gil_rates
    #           3) Count as leveling (0 gil)
    total_daily_gil = 0
    farming_subs_count = 0
    leveling_plans = submarine_plans.get("leveling", [])
    farming_plans = submarine_plans.get("farming", {})
    
    for i, build in enumerate(all_builds):
        plan_name = all_plans[i] if i < len(all_plans) else ""
        
        # Check if plan is a leveling plan (skip, no income)
        if plan_name and plan_name in leveling_plans:
            continue
        
        # Check if plan has a farming rate defined
        if plan_name and plan_name in farming_plans:
            total_daily_gil += farming_plans[plan_name]
            farming_subs_count += 1
            continue
        
        # Fall back to build-based rate
        if build in build_gil_rates:
            total_daily_gil += build_gil_rates[build]
            farming_subs_count += 1
    
    leveling_subs_count = total_all_subs - farming_subs_count
    
    # Calculate total supply cost per day (tanks and repair kits)
    total_tanks_per_day = 0
    total_kits_per_day = 0
    for build in all_builds:
        if build in build_consumption_rates:
            total_tanks_per_day += build_consumption_rates[build]["tanks_per_day"]
            total_kits_per_day += build_consumption_rates[build]["kits_per_day"]
        else:
            # Default consumption for unlisted builds (leveling submarines)
            total_tanks_per_day += 9.0
            total_kits_per_day += 1.33
    
    # Calculate costs using configurable supply costs
    total_supply_cost_per_day = int((total_tanks_per_day * CERULEUM_TANK_COST) + (total_kits_per_day * REPAIR_KIT_COST))
    
    # Calculate minimum days until restocking
    min_days_until_restocking = min(all_days_remaining) if all_days_remaining else None
    
    # Display totals
    print(f"Total Subs: {total_ready_subs} / {total_all_subs}")
    print(f"Total Gil Per Day: {total_daily_gil:,}")
    print(f"Total Subs Leveling: {leveling_subs_count}")
    print(f"Total Subs Farming: {farming_subs_count}")
    print(f"Total Supply Cost Per Day: {total_supply_cost_per_day:,}")
    if min_days_until_restocking is not None:
        print(f"Total Days Until Restocking Required: {min_days_until_restocking}")
    # Display lowest inventory space among submarine-only farmers (excludes characters with retainers)
    min_inventory_space = min(all_inventory_spaces) if all_inventory_spaces else None
    if min_inventory_space is not None:
        print(f"Lowest Inventory Space (Sub-Only Farmers): {min_inventory_space}")
    # Display lowest inventory space among retainer farmers (characters with retainers)
    min_retainer_inventory_space = min(all_retainer_inventory_spaces) if all_retainer_inventory_spaces else None
    if min_retainer_inventory_space is not None:
        print(f"Lowest Inventory Space (Retainer Farmers): {min_retainer_inventory_space}")
    if MAX_CLIENTS > 0:
        print(f"Max Clients: {MAX_CLIENTS}")
    
    print("=" * 85)
    print("Press Ctrl+C to exit")
    print("=" * 85)

def main():
    """Main loop - continuously update display with dual refresh rates"""
    try:
        # System bootup delay (if configured)
        if SYSTEM_BOOTUP_DELAY > 0:
            print(f"ARR Processing Delay {SYSTEM_BOOTUP_DELAY}s Set. Please Wait...")
            for remaining in range(SYSTEM_BOOTUP_DELAY, 0, -1):
                print(f"  Starting in {remaining} second{'s' if remaining != 1 else ''}...", end='\r')
                time.sleep(1)
            print("\n")  # Clear the countdown line
        
        # Initial launcher check - close any stuck XIVLauncher on startup
        if is_xivlauncher_running():
            print("[STARTUP] XIVLauncher.exe detected with visible windows - closing stuck launcher...")
            if kill_xivlauncher_process():
                print("[STARTUP] Successfully closed XIVLauncher.exe")
            else:
                print("[STARTUP] Failed to close XIVLauncher.exe - may need manual intervention")
            time.sleep(2)  # Brief wait after killing launcher
        
        # Validate configuration: single client mode requires only 1 account
        if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
            if len(account_locations) > 1:
                print("[ERROR] USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME is True but multiple accounts are configured.")
                print("[ERROR] Single client mode only supports 1 account.")
                print(f"[ERROR] Currently configured accounts: {len(account_locations)}")
                print("[ERROR] Please disable USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME or configure only 1 account.")
                log_error(f"CONFIG_VALIDATION_FAILED: Single client mode enabled but {len(account_locations)} accounts configured")
                sys.exit(1)
            print("[INFO] Running in single client mode (USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME=True)")
            print("[INFO] Using default FFXIV window title detection\n")
        
        # Track last window check time (set to negative to force immediate check on first run)
        last_window_check = -WINDOW_REFRESH_INTERVAL
        game_status_dict = {}
        closed_pids = set()  # Track PIDs we've already closed to avoid repeated attempts
        last_launch_time = {}  # Track last launch time for each account to enforce rate limiting
        client_start_times = {}  # Track process start times (will be populated with actual times)
        initial_arrangement_done = False  # Track if we've done initial window arrangement
        game_launch_timestamp = {}  # Track when game was launched for each account (for force crash monitoring)
        last_sub_processed = {}  # Track last time submarine was processed for each account (for force crash monitoring) (negative → positive transitions)
        submarine_state_cache = {}  # Cache submarine return times by nickname to detect processing (negative → positive transitions)
        retainer_state_cache = {}  # Cache retainer venture times by nickname to detect processing (for force247uptime accounts)
        retainer_mode_active = {}  # Track when retainer timer mode was active per account (prevents premature timer switch when subs become ready)
        launcher_retry_count = {}  # Track launcher retry attempts per account
        launcher_failed_accounts = set()  # Track accounts that have exceeded launcher retry limit
        
        # Initialize client_start_times with actual process start times for already-running games
        if PSUTIL_AVAILABLE:
            if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
                # Single client mode: track ffxiv_dx11.exe process start time
                ffxiv_start_time = get_ffxiv_process_start_time()
                if ffxiv_start_time:
                    client_start_times['ffxiv_single'] = ffxiv_start_time
                    if DEBUG:
                        print(f"[INIT] Found existing FFXIV process with start time: {datetime.datetime.fromtimestamp(ffxiv_start_time).strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                # Multi-client mode: track by PID
                for account_entry in account_locations:
                    nickname = account_entry["nickname"]
                    is_running, process_id = is_ffxiv_running_for_account(nickname)
                    if is_running and process_id:
                        actual_start_time = get_process_start_time(process_id)
                        if actual_start_time:
                            client_start_times[process_id] = actual_start_time
                            if DEBUG:
                                print(f"[INIT] Found existing process {nickname} (PID: {process_id}) with start time: {datetime.datetime.fromtimestamp(actual_start_time).strftime('%Y-%m-%d %H:%M:%S')}")
        
        while True:
            current_time = time.time()
            
            # Check if we need to refresh window status (every WINDOW_REFRESH_INTERVAL seconds)
            if current_time - last_window_check >= WINDOW_REFRESH_INTERVAL:
                if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
                    # Single client mode: track ffxiv_dx11.exe process
                    for account_entry in account_locations:
                        nickname = account_entry["nickname"]
                        status = is_ffxiv_running_for_account(nickname)
                        game_status_dict[nickname] = status
                        is_running, _ = status
                        
                        if is_running:
                            # Update process start time for single client
                            if 'ffxiv_single' not in client_start_times:
                                ffxiv_start_time = get_ffxiv_process_start_time()
                                if ffxiv_start_time:
                                    client_start_times['ffxiv_single'] = ffxiv_start_time
                                    if DEBUG:
                                        print(f"[DEBUG] Detected FFXIV process with start time")
                        else:
                            # Remove tracking if process not running
                            if 'ffxiv_single' in client_start_times:
                                del client_start_times['ffxiv_single']
                else:
                    # Multi-client mode: track by PID
                    running_pids = set()
                    for account_entry in account_locations:
                        nickname = account_entry["nickname"]
                        status = is_ffxiv_running_for_account(nickname)
                        game_status_dict[nickname] = status
                        is_running, process_id = status
                        if is_running and process_id:
                            running_pids.add(process_id)
                            if process_id not in client_start_times:
                                # Try to get actual process start time, fallback to current time
                                actual_start_time = get_process_start_time(process_id)
                                if actual_start_time:
                                    client_start_times[process_id] = actual_start_time
                                    if DEBUG:
                                        print(f"[DEBUG] Detected new process {nickname} (PID: {process_id}) with actual start time")
                                else:
                                    client_start_times[process_id] = current_time
                                    if DEBUG:
                                        print(f"[DEBUG] Detected new process {nickname} (PID: {process_id}) using current time")
                    # Remove entries for processes that are no longer running
                    for pid in list(client_start_times.keys()):
                        if pid not in running_pids:
                            del client_start_times[pid]
                
                # Check for active DalamudCrashHandler.exe windows (indicates a game crash)
                crash_handler_pid = is_dalamud_crash_handler_running()
                if crash_handler_pid:
                    print(f"\n[CRASH-HANDLER] DalamudCrashHandler.exe (PID {crash_handler_pid}) detected as ACTIVE APP - closing crash handler window...")
                    if kill_dalamud_crash_handler_process(crash_handler_pid):
                        print(f"[CRASH-HANDLER] Successfully closed DalamudCrashHandler.exe (PID {crash_handler_pid})")
                    else:
                        print(f"[CRASH-HANDLER] Failed to close DalamudCrashHandler.exe (PID {crash_handler_pid})")
                
                last_window_check = current_time
            
            # Display submarine timers with current game status FIRST
            display_submarine_timers(game_status_dict, client_start_times, launcher_failed_accounts, last_sub_processed, retainer_mode_active)
            
            # Initial window arrangement check (only on first run)
            if not initial_arrangement_done and ENABLE_WINDOW_LAYOUT:
                # Check if any games are already running
                any_games_running = any(
                    game_status_dict.get(acc["nickname"], (False, None))[0] 
                    for acc in account_locations 
                    if acc.get("include_submarines", True)
                )
                
                if any_games_running:
                    if DEBUG:
                        print(f"\n[WINDOW-MOVER] Detected games already running on startup")
                    arrange_ffxiv_windows()
                
                initial_arrangement_done = True
            
            # Then show debug output and auto-launch logic (won't be cleared)
            if ENABLE_AUTO_LAUNCH:
                if DEBUG:
                    print(f"\n[DEBUG] Auto-launch enabled, checking accounts...")
                
                # Count currently running clients
                running_count = sum(1 for acc in account_locations if game_status_dict.get(acc["nickname"], (False, None))[0])
                
                if DEBUG:
                    print(f"[DEBUG] Currently running clients: {running_count}")
                    if MAX_CLIENTS > 0:
                        print(f"[DEBUG] MAX_CLIENTS limit: {MAX_CLIENTS}")
                
                # Check if we've reached MAX_CLIENTS limit (0 = unlimited)
                if MAX_CLIENTS > 0 and running_count >= MAX_CLIENTS:
                    if DEBUG:
                        print(f"[DEBUG] MAX_CLIENTS limit reached ({running_count}/{MAX_CLIENTS}), skipping auto-launch")
                else:
                    # Build lists of accounts that need launching
                    force247_accounts = []
                    submarine_ready_accounts = []
                    
                    for account_entry in account_locations:
                        nickname = account_entry["nickname"]
                        include_subs = account_entry.get("include_submarines", True)
                        rotating_retainers = account_entry.get("force247uptime", False)
                        
                        # Skip if account has exceeded launcher retry limit
                        if nickname in launcher_failed_accounts:
                            if DEBUG:
                                print(f"[DEBUG] {nickname}: Launcher failed, skipping")
                            continue
                        
                        # Skip if submarines are disabled for this account and not force247uptime
                        if not include_subs and not rotating_retainers:
                            if DEBUG:
                                print(f"[DEBUG] {nickname}: Submarines disabled, skipping")
                            continue
                        
                        # Get game status
                        game_info = game_status_dict.get(nickname, (None, None))
                        is_running = game_info[0]
                        
                        # Skip if already running
                        if is_running:
                            if DEBUG:
                                debug_msg = f"[DEBUG] {nickname}: Already running, skipping"
                                
                                # Add force-close timer info if we have a launch timestamp
                                if nickname in game_launch_timestamp:
                                    launch_time = game_launch_timestamp[nickname]
                                    monitoring_start_time = launch_time + (AUTO_LAUNCH_THRESHOLD * 3600)
                                    
                                    if current_time >= monitoring_start_time:
                                        # Monitoring is active - show inactivity timer
                                        if nickname in last_sub_processed:
                                            minutes_since_processing = (current_time - last_sub_processed[nickname]) / 60
                                            # Determine if monitoring retainers or submarines
                                            timer_data = get_submarine_timers_for_account(account_entry)
                                            ready_subs = timer_data.get("ready_subs", 0)
                                            ready_rets = timer_data.get("ready_retainers", 0)
                                            # For force247 accounts with no subs ready, we're monitoring retainers
                                            # Use rotating_retainers flag (not current ready_rets) since ready_rets may be 0 after processing
                                            is_retainer_monitoring_account = (ready_subs == 0 and rotating_retainers)
                                            # Use appropriate threshold for retainers vs submarines
                                            inactivity_threshold = FORCE_CRASH_RETAINER_MINUTES if is_retainer_monitoring_account else FORCE_CRASH_INACTIVITY_MINUTES
                                            minutes_until_crash = max(0, inactivity_threshold - minutes_since_processing)
                                            if is_retainer_monitoring_account:
                                                debug_msg += f" [Force-Close] Last retainer processed {minutes_since_processing:.1f} minutes ago. Force close in {minutes_until_crash:.1f} minutes."
                                            else:
                                                debug_msg += f" [Force-Close] Last sub processed {minutes_since_processing:.1f} minutes ago. Force close in {minutes_until_crash:.1f} minutes."
                                        else:
                                            # No processing detected yet
                                            debug_msg += f" [Force-Close] Monitoring active, no submarine processing detected yet."
                                    else:
                                        # Still in countdown phase - show time until monitoring starts
                                        time_until_monitoring = (monitoring_start_time - current_time) / 60
                                        debug_msg += f" [Force-Close] Monitoring starts in {time_until_monitoring:.1f} minutes"
                                
                                print(debug_msg)
                            continue
                        
                        # Check rate limiting
                        last_launch = last_launch_time.get(nickname, 0)
                        time_since_last_launch = current_time - last_launch
                        if time_since_last_launch < OPEN_DELAY_THRESHOLD:
                            if DEBUG:
                                print(f"[DEBUG] {nickname}: Rate limited, {time_since_last_launch:.0f}s < {OPEN_DELAY_THRESHOLD}s")
                            continue
                        
                        # Categorize account by launch priority
                        if rotating_retainers:
                            force247_accounts.append((account_entry, "force247uptime enabled"))
                        elif include_subs:
                            timer_data = get_submarine_timers_for_account(account_entry)
                            soonest_hours = timer_data.get("soonest_hours")
                            if soonest_hours is not None and soonest_hours <= AUTO_LAUNCH_THRESHOLD:
                                force247_accounts.append((account_entry, f"submarines nearly ready ({soonest_hours:.1f}h)"))
                    
                    # Combine lists: force247uptime clients first, then submarine-ready clients
                    accounts_to_launch = force247_accounts + submarine_ready_accounts
                    
                    if DEBUG and accounts_to_launch:
                        print(f"[DEBUG] Accounts queued for launch: {len(accounts_to_launch)}")
                        print(f"[DEBUG]  - force247uptime: {len(force247_accounts)}")
                        print(f"[DEBUG]  - submarine-ready: {len(submarine_ready_accounts)}")
                    
                    # Launch accounts sequentially until MAX_CLIENTS limit reached
                    for account_entry, reason in accounts_to_launch:
                        # Recount running clients before each launch
                        running_count = sum(1 for acc in account_locations if game_status_dict.get(acc["nickname"], (False, None))[0])
                        
                        # Check if limit reached
                        if MAX_CLIENTS > 0 and running_count >= MAX_CLIENTS:
                            if DEBUG:
                                print(f"[DEBUG] MAX_CLIENTS limit reached ({running_count}/{MAX_CLIENTS}), stopping launches")
                            break
                        
                        nickname = account_entry["nickname"]
                        
                        # Initialize launcher retry count if not exists
                        if nickname not in launcher_retry_count:
                            launcher_retry_count[nickname] = 0
                        
                        # Track if this launch succeeded
                        launch_success = False
                        
                        while not launch_success and launcher_retry_count[nickname] < FORCE_LAUNCHER_RETRY:
                            print(f"\n[AUTO-LAUNCH] Launching {nickname} - {reason}")
                            if launcher_retry_count[nickname] > 0:
                                print(f"[AUTO-LAUNCH] Launcher retry attempt {launcher_retry_count[nickname]}/{FORCE_LAUNCHER_RETRY}")
                            
                            if launch_game(nickname):
                                last_launch_time[nickname] = current_time
                                print(f"[AUTO-LAUNCH] Successfully launched {nickname}, waiting {OPEN_DELAY_THRESHOLD} seconds for game startup...")
                                
                                # Wait OPEN_DELAY_THRESHOLD before checking window title
                                time.sleep(OPEN_DELAY_THRESHOLD)
                                
                                # Wait for window title to update and check for launcher
                                print(f"[AUTO-LAUNCH] Checking window/launcher status for {nickname}...")
                                title_updated, needs_launcher_retry = wait_for_window_title_update(nickname, launcher_retry_count[nickname])
                                
                                if title_updated:
                                    print(f"[AUTO-LAUNCH] Game successfully started for {nickname}")
                                    launch_success = True
                                    # Reset launcher retry count on success
                                    launcher_retry_count[nickname] = 0
                                    # Track game launch timestamp for force-close monitoring
                                    game_launch_timestamp[nickname] = current_time
                                    if DEBUG:
                                        print(f"[FORCE-CRASH] {nickname}: Game launched, crash monitoring will activate in {AUTO_LAUNCH_THRESHOLD * 60:.1f} minutes")
                                elif needs_launcher_retry:
                                    # Launcher detected - kill it and retry
                                    launcher_retry_count[nickname] += 1
                                    print(f"[AUTO-LAUNCH] Killing XIVLauncher.exe for {nickname}...")
                                    kill_xivlauncher_process()
                                    time.sleep(2)  # Brief wait after killing launcher
                                    
                                    if launcher_retry_count[nickname] >= FORCE_LAUNCHER_RETRY:
                                        # Max retries reached - log the failure
                                        log_error(f"LAUNCHER_FAILED: {nickname} - Max launcher retries ({FORCE_LAUNCHER_RETRY}) reached, marking as [LAUNCHER]")
                                        if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
                                            print(f"[AUTO-LAUNCH] Max launcher retries ({FORCE_LAUNCHER_RETRY}) reached for {nickname}")
                                            print(f"[AUTO-LAUNCH] Stopping script - single client mode cannot continue")
                                            launcher_failed_accounts.add(nickname)
                                        else:
                                            print(f"[AUTO-LAUNCH] Max launcher retries ({FORCE_LAUNCHER_RETRY}) reached for {nickname}")
                                            print(f"[AUTO-LAUNCH] Marking {nickname} as [LAUNCHER] - will skip this account")
                                            launcher_failed_accounts.add(nickname)
                                        break
                                    else:
                                        # Before retry, check and update AutologinEnabled and OtpServerEnabled if needed
                                        if ENABLE_AUTOLOGIN_UPDATER:
                                            print(f"[AUTOLOGIN] Checking AutologinEnabled for {nickname} before retry...")
                                            check_and_update_autologin(nickname)
                                            # Also check OtpServerEnabled for 2FA accounts
                                            check_and_update_otp_server(nickname)
                                        print(f"[AUTO-LAUNCH] Retrying {nickname} (attempt {launcher_retry_count[nickname] + 1}/{FORCE_LAUNCHER_RETRY})...")
                                        last_launch_time[nickname] = 0  # Allow immediate retry
                                else:
                                    # Title check failed without launcher detection
                                    # Log the error for troubleshooting
                                    log_error(f"WINDOW_TITLE_FAILED: {nickname} - Window title check failed after {MAX_WINDOW_TITLE_RESCAN} attempts")
                                    
                                    if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
                                        # Single client mode: safe to kill the single process
                                        print(f"[AUTO-LAUNCH] Window title check failed for {nickname}, killing process and will retry...")
                                        kill_ffxiv_process()
                                        last_launch_time[nickname] = 0  # Allow immediate retry
                                    else:
                                        # Multi-client mode: DO NOT kill all processes!
                                        # Just mark as failed and let normal rotation continue
                                        # The game client checker will retry in WINDOW_REFRESH_INTERVAL seconds
                                        print(f"[AUTO-LAUNCH] Window title check failed for {nickname}, continuing normal rotation...")
                                        print(f"[AUTO-LAUNCH] Game client checker will retry {nickname} in {WINDOW_REFRESH_INTERVAL} seconds")
                                        last_launch_time[nickname] = current_time  # Prevent immediate retry spam
                                    break  # Exit retry loop, continue normal operation
                            else:
                                print(f"[AUTO-LAUNCH] Failed to launch {nickname}")
                                last_launch_time[nickname] = current_time  # Record failed attempt to enforce rate limit
                                break  # Exit retry loop
                        
                        # Only proceed with post-launch actions if successful
                        if launch_success:
                            # Refresh window status for all accounts
                            if DEBUG:
                                print(f"[AUTO-LAUNCH] Refreshing window status...")
                            for acc_entry in account_locations:
                                acc_nickname = acc_entry["nickname"]
                                game_status_dict[acc_nickname] = is_ffxiv_running_for_account(acc_nickname)
                            last_window_check = current_time
                            
                            # Arrange all windows after launch (if enabled)
                            if ENABLE_WINDOW_LAYOUT:
                                arrange_ffxiv_windows()
                            
                            # Update process tracking for newly launched client
                            if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
                                ffxiv_start_time = get_ffxiv_process_start_time()
                                if ffxiv_start_time:
                                    client_start_times['ffxiv_single'] = ffxiv_start_time
                            else:
                                is_running, process_id = game_status_dict.get(nickname, (False, None))
                                if is_running and process_id and process_id not in client_start_times:
                                    actual_start_time = get_process_start_time(process_id)
                                    if actual_start_time:
                                        client_start_times[process_id] = actual_start_time
                                    else:
                                        client_start_times[process_id] = current_time
                            
                            # Redisplay submarine timers to show newly opened client status
                            print("")  # Empty line for spacing
                            display_submarine_timers(game_status_dict, client_start_times, launcher_failed_accounts, last_sub_processed, retainer_mode_active)
                            print("")  # Empty line for spacing
            
            # Auto-close games if enabled and conditions are met
            if ENABLE_AUTO_CLOSE:
                for account_entry in account_locations:
                    nickname = account_entry["nickname"]
                    include_subs = account_entry.get("include_submarines", True)
                    rotating_retainers = account_entry.get("force247uptime", False)
                    
                    # Get game status
                    game_info = game_status_dict.get(nickname, (None, None))
                    is_running = game_info[0]
                    process_id = game_info[1]
                    
                    # Only proceed if game is running
                    if not is_running:
                        continue
                    
                    # In multi-client mode, we need a valid process_id
                    if not USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME and not process_id:
                        continue
                    
                    # Skip if we've already closed this PID (multi-client mode only)
                    if process_id and process_id in closed_pids:
                        continue

                    # Enforce MAX_RUNTIME for all clients
                    uptime_hours = None
                    if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
                        # Single client mode: get uptime from ffxiv_single tracking
                        start_time = client_start_times.get('ffxiv_single')
                        if start_time is not None:
                            uptime_hours = (current_time - start_time) / 3600.0
                    elif process_id:
                        # Multi-client mode: get uptime from PID tracking
                        start_time = client_start_times.get(process_id)
                        if start_time is not None:
                            uptime_hours = (current_time - start_time) / 3600.0

                    if uptime_hours is not None and uptime_hours >= MAX_RUNTIME:
                        print(f"\n[AUTO-CLOSE] Closing {nickname} (PID: {process_id}) - Uptime {uptime_hours:.1f}h exceeds MAX_RUNTIME {MAX_RUNTIME}h")
                        
                        kill_game_client_and_cleanup(
                            nickname, process_id,
                            f"[AUTO-CLOSE] Successfully closed {nickname} after {uptime_hours:.1f}h, waiting {TIMER_REFRESH_INTERVAL} seconds before checking clients again.",
                            f"[AUTO-CLOSE] Failed to close {nickname}",
                            closed_pids, game_status_dict, client_start_times,
                            set_launch_time=(last_launch_time, current_time)
                        )
                        continue

                    # Do not auto-close force247uptime accounts based on submarine timers
                    if rotating_retainers:
                        continue

                    # Close game if submarines disabled AND force247uptime is False
                    # (no submarines and no reason to keep game running)
                    if not include_subs and not rotating_retainers:
                        print(f"\n[AUTO-CLOSE] Closing {nickname} (PID: {process_id}) - Submarines disabled, force247uptime=False")
                        
                        kill_game_client_and_cleanup(
                            nickname, process_id,
                            f"[AUTO-CLOSE] Successfully closed {nickname}, waiting {TIMER_REFRESH_INTERVAL} seconds before checking clients again.",
                            f"[AUTO-CLOSE] Failed to close {nickname}",
                            closed_pids, game_status_dict, client_start_times,
                            last_launch_time=last_launch_time
                        )
                        continue
                    
                    # Skip timer-based auto-close for accounts without submarines (but with force247uptime)
                    if not include_subs:
                        continue

                    # Get submarine timer data
                    timer_data = get_submarine_timers_for_account(account_entry)
                    soonest_hours = timer_data.get("soonest_hours")
                    
                    # Check if we should close the game
                    # Close if soonest_hours > AUTO_CLOSE_THRESHOLD (submarines won't be ready soon)
                    if soonest_hours is not None and soonest_hours > AUTO_CLOSE_THRESHOLD:
                        print(f"\n[AUTO-CLOSE] Closing {nickname} (PID: {process_id}) - Next sub in {soonest_hours:.1f}h")
                        
                        kill_game_client_and_cleanup(
                            nickname, process_id,
                            f"[AUTO-CLOSE] Successfully closed {nickname}, waiting {TIMER_REFRESH_INTERVAL} seconds before checking clients again.",
                            f"[AUTO-CLOSE] Failed to close {nickname}",
                            closed_pids, game_status_dict, client_start_times,
                            last_launch_time=last_launch_time
                        )
            
            # Force crash timer - check for frozen/stuck clients
            # Only run force-crash monitoring if ENABLE_AUTO_CLOSE is True
            if ENABLE_AUTO_CLOSE:
                for account_entry in account_locations:
                    nickname = account_entry["nickname"]
                    include_subs = account_entry.get("include_submarines", True)
                    force247 = account_entry.get("force247uptime", False)
                    auto_path = account_entry["auto_path"]
                    
                    # Skip if submarines disabled
                    if not include_subs:
                        continue
                    
                    # Get game status
                    game_info = game_status_dict.get(nickname, (None, None))
                    is_running = game_info[0]
                    process_id = game_info[1]
                    
                    # Only check if game is running
                    if not is_running:
                        # Clean up tracking if game not running
                        if nickname in game_launch_timestamp:
                            del game_launch_timestamp[nickname]
                        if nickname in last_sub_processed:
                            del last_sub_processed[nickname]
                        if nickname in retainer_mode_active:
                            del retainer_mode_active[nickname]
                        continue
                    
                    # Check if we have a game launch timestamp for this account
                    if nickname not in game_launch_timestamp:
                        # Game is running but we don't have launch timestamp (e.g., script restarted while game was running)
                        # Check actual uptime to determine appropriate launch timestamp
                        actual_uptime_hours = 0
                        if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
                            if 'ffxiv_single' in client_start_times:
                                actual_uptime_hours = (current_time - client_start_times['ffxiv_single']) / 3600
                        elif process_id and process_id in client_start_times:
                            actual_uptime_hours = (current_time - client_start_times[process_id]) / 3600
                        
                        # Check if subs or retainers are ready - if so, activate monitoring immediately
                        timer_data = get_submarine_timers_for_account(account_entry)
                        ready_subs = timer_data.get("ready_subs", 0)
                        ready_retainers = timer_data.get("ready_retainers", 0)
                        subs_or_retainers_ready = ready_subs > 0 or (force247 and ready_retainers > 0)
                        
                        # Activate monitoring immediately if:
                        # 1. Uptime exceeds AUTO_LAUNCH_THRESHOLD, OR
                        # 2. Submarines are ready (need processing), OR
                        # 3. force247uptime and retainers are ready (need processing)
                        if actual_uptime_hours >= AUTO_LAUNCH_THRESHOLD or subs_or_retainers_ready:
                            # Set launch timestamp in the past so monitoring activates now
                            game_launch_timestamp[nickname] = current_time - (AUTO_LAUNCH_THRESHOLD * 3600)
                            if DEBUG:
                                if subs_or_retainers_ready:
                                    ready_type = "subs" if ready_subs > 0 else "retainers"
                                    ready_count = ready_subs if ready_subs > 0 else ready_retainers
                                    print(f"[FORCE-CRASH] {nickname}: {ready_count} {ready_type} ready, activating monitoring immediately")
                                else:
                                    print(f"[FORCE-CRASH] {nickname}: Game running {actual_uptime_hours:.2f}h (>{AUTO_LAUNCH_THRESHOLD * 60:.0f}min threshold), activating monitoring immediately")
                        else:
                            # Set launch timestamp to current time, monitoring will activate after AUTO_LAUNCH_THRESHOLD
                            game_launch_timestamp[nickname] = current_time
                            if DEBUG:
                                print(f"[FORCE-CRASH] {nickname}: Game running {actual_uptime_hours:.2f}h (<{AUTO_LAUNCH_THRESHOLD * 60:.0f}min threshold), monitoring will activate in {(AUTO_LAUNCH_THRESHOLD - actual_uptime_hours) * 60:.1f} minutes")
                        continue
                    
                    # Calculate when monitoring should activate (AUTO_LAUNCH_THRESHOLD hours after game launched)
                    launch_time = game_launch_timestamp[nickname]
                    monitoring_start_time = launch_time + (AUTO_LAUNCH_THRESHOLD * 3600)  # Convert hours to seconds
                    
                    # Check if monitoring should be active yet
                    if current_time < monitoring_start_time:
                        # Not time to monitor yet - still within grace period
                        if DEBUG:
                            minutes_until_monitoring = (monitoring_start_time - current_time) / 60
                            print(f"[FORCE-CRASH] {nickname}: Monitoring will activate in {minutes_until_monitoring:.1f} minutes")
                        continue
                    
                    # Monitoring is now active - check for submarine processing activity
                    processed_count = detect_submarine_processing(account_entry, submarine_state_cache, datetime.datetime.now().timestamp())
                    
                    if processed_count > 0:
                        # Submarine processing detected - reset inactivity timer and clear retainer mode
                        last_sub_processed[nickname] = current_time
                        # Clear retainer mode flag since subs are now being processed
                        if nickname in retainer_mode_active:
                            if DEBUG:
                                print(f"[FORCE-CRASH] {nickname}: Subs now being processed, switching from retainer timer to submarine timer")
                            del retainer_mode_active[nickname]
                        if DEBUG:
                            print(f"[FORCE-CRASH] {nickname}: {processed_count} sub(s) processed, resetting inactivity timer")
                    
                    # For force247uptime accounts, also check retainer processing
                    if force247:
                        retainer_processed_count = detect_retainer_processing(account_entry, retainer_state_cache, datetime.datetime.now().timestamp())
                        
                        if retainer_processed_count > 0:
                            # Retainer processing detected - reset inactivity timer
                            last_sub_processed[nickname] = current_time
                            if DEBUG:
                                print(f"[FORCE-CRASH] {nickname}: {retainer_processed_count} retainer(s) processed, resetting inactivity timer")
                    
                    # Get submarine status to determine monitoring applicability
                    timer_data = get_submarine_timers_for_account(account_entry)
                    ready_subs = timer_data.get("ready_subs", 0)
                    ready_retainers = timer_data.get("ready_retainers", 0)
                    soonest_hours = timer_data.get("soonest_hours")
                    is_waiting = (ready_subs == 0 and soonest_hours is not None and 0 < soonest_hours <= AUTO_CLOSE_THRESHOLD)
                    
                    # Skip monitoring if all subs are voyaging (0 ready, not in WAITING)
                    # UNLESS force247uptime=True and retainers are ready (continue monitoring for retainer processing)
                    if ready_subs == 0 and not is_waiting:
                        # Check if force247uptime with ready retainers - keep monitoring active
                        if force247 and ready_retainers > 0:
                            # Retainers ready for processing - keep monitoring active
                            if DEBUG:
                                print(f"[FORCE-CRASH] {nickname}: All subs voyaging but {ready_retainers} retainer(s) ready, monitoring active")
                        else:
                            # All submarines voyaging, no ready subs, no retainers - disable monitoring for idle state
                            if nickname in last_sub_processed:
                                del last_sub_processed[nickname]  # Clear timer when entering idle
                            if DEBUG:
                                print(f"[FORCE-CRASH] {nickname}: All subs voyaging (0 ready), monitoring disabled")
                            continue
                    
                    # Check if account is in (WAITING) state - extend timer to prevent force-close during legitimate waiting
                    # UNLESS force247uptime=True and retainers are ready (should be processing retainers)
                    # For force247 accounts, also reset timer when no retainers are ready (waiting for retainers to return)
                    if is_waiting:
                        if force247 and ready_retainers > 0:
                            # Retainers are ready - don't reset timer, expect retainer processing
                            if DEBUG:
                                print(f"[FORCE-CRASH] {nickname}: Waiting for subs but {ready_retainers} retainer(s) ready, expecting retainer processing")
                        else:
                            # Account is in (WAITING) state - reset inactivity timer to prevent force-close
                            last_sub_processed[nickname] = current_time
                            if DEBUG:
                                print(f"[FORCE-CRASH] {nickname}: Sub is still waiting. Force close timer reset to {FORCE_CRASH_INACTIVITY_MINUTES} minutes")
                    elif force247 and ready_retainers == 0:
                        # force247 account with no retainers ready - also considered WAITING for retainers to return
                        last_sub_processed[nickname] = current_time
                        if DEBUG:
                            print(f"[FORCE-CRASH] {nickname}: Waiting for retainers to return. Force close timer reset to {FORCE_CRASH_RETAINER_MINUTES} minutes")
                    
                    # Initialize last_sub_processed if not set (first check after monitoring activates)
                    if nickname not in last_sub_processed:
                        # No processing detected yet, start fresh timer from current time
                        last_sub_processed[nickname] = current_time
                        if DEBUG:
                            print(f"[FORCE-CRASH] {nickname}: Monitoring activated, starting inactivity timer")
                    
                    # Check inactivity timer
                    minutes_since_processing = (current_time - last_sub_processed[nickname]) / 60
                    
                    # Determine if monitoring retainers (longer timeout) or submarines
                    # Use retainer timer when: (1) only retainers ready, OR (2) we were in retainer mode and subs became ready but haven't been processed yet
                    currently_retainer_mode = (ready_subs == 0 and force247 and ready_retainers > 0)
                    
                    # Track retainer mode state - set flag when in retainer mode
                    if currently_retainer_mode:
                        retainer_mode_active[nickname] = True
                    
                    # Use retainer timer if: currently in retainer mode OR was in retainer mode when subs became ready (not yet processed)
                    # The retainer_mode_active flag is only cleared when actual submarine processing is detected (above)
                    monitoring_retainers = currently_retainer_mode or (retainer_mode_active.get(nickname, False) and ready_subs > 0)
                    inactivity_threshold = FORCE_CRASH_RETAINER_MINUTES if monitoring_retainers else FORCE_CRASH_INACTIVITY_MINUTES
                    
                    if DEBUG and monitoring_retainers and ready_subs > 0:
                        print(f"[FORCE-CRASH] {nickname}: Subs ready but retainer mode still active (waiting for sub processing), using {FORCE_CRASH_RETAINER_MINUTES}m timer")
                    
                    # Force crash if no processing detected for the appropriate threshold
                    if minutes_since_processing > inactivity_threshold:
                        time_since_launch = (current_time - launch_time) / 3600
                        processing_type = "retainer" if monitoring_retainers else "submarine"
                        crash_message = f"[FORCE-CRASH] Crashing {nickname} (PID: {process_id}) - No {processing_type} processing for {minutes_since_processing:.1f}m (game running for {time_since_launch:.1f}h)"
                        print(f"\n{crash_message}")
                        
                        # Send notification about force-crash
                        log_error(crash_message)
                        
                        kill_game_client_and_cleanup(
                            nickname, process_id,
                            f"[FORCE-CRASH] Successfully crashed {nickname} - likely frozen/stuck, waiting {TIMER_REFRESH_INTERVAL} seconds before relaunch",
                            f"[FORCE-CRASH] Failed to crash {nickname}",
                            closed_pids, game_status_dict, client_start_times,
                            last_launch_time=last_launch_time,
                            game_launch_timestamp=game_launch_timestamp,
                            last_sub_processed=last_sub_processed,
                            retainer_mode_active=retainer_mode_active
                        )
            
            # Wait for TIMER_REFRESH_INTERVAL seconds before next timer update
            time.sleep(TIMER_REFRESH_INTERVAL)
    except KeyboardInterrupt:
        print("\n\nExiting submarine timer monitor...")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        error_msg = f"\n{'='*80}\n[CRITICAL ERROR] Script crashed with unhandled exception:\n{'='*80}\n"
        error_msg += f"Exception Type: {type(e).__name__}\n"
        error_msg += f"Exception Message: {e}\n"
        error_msg += f"\nFull Traceback:\n{traceback.format_exc()}"
        error_msg += f"{'='*80}\n"
        print(error_msg)
        
        # Try to log and send notification about the crash
        try:
            log_error(f"CRITICAL_CRASH: {type(e).__name__}: {e} - An unexpected crash occurred, please check the script and report any issues.")
        except:
            pass
        
        # Keep window open for debugging if DEBUG is enabled
        if DEBUG:
            print("\n[CRASH] Script has stopped. Window will remain open for debugging.")
            print("Press Enter to close this window...")
            input()
