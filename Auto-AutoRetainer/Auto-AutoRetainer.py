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
# A comprehensive automation script that monitors submarine return times across multiple FFXIV accounts and automatically
# manages game instances for optimal submarine collection. Integrates with AutoRetainer plugin data to track submarine
# voyages and calculates daily gil earnings from submarine builds.
#
# Core Features:
# • Real-time submarine timer monitoring across all configured accounts
# • Automatic game launching when submarines are nearly ready (configurable threshold)
# • Automatic game closing when submarines won't be ready soon (prevents idle instances)
# • Intelligent window arrangement with customizable layouts (main/left configurations)
# • Process ID tracking and management for reliable game instance control
# • Gil earnings calculation based on submarine builds and voyage routes
# • Rate limiting to prevent rapid game launches and API throttling
# • Dual refresh rate system (30s timers, 60s window status) for optimal performance
#
# Important Note: This script requires properly configured game launchers (XIVLauncher.exe or batch files), game windows
# labeled with "ProcessID - nickname" format, autologging enabled without 2FA, and AutoRetainer multi-mode auto-enabled
# for full automation. See README.md for complete setup instructions.
#
# Auto-AutoRetainer v1.12
# Automated FFXIV Submarine Management System
# Created by: https://github.com/xa-io
# Last Updated: 2025-12-05 07:15:00
#
# ## Release Notes ##
#
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
import subprocess
import ctypes
from ctypes import wintypes
import re
import win32con

# Try to import psutil for process information
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("[WARNING] psutil not installed. Install with: pip install psutil")
    print("[WARNING] Uptime will only be tracked from script start time.")

# ===============================================
# Configuration Parameters
# ===============================================
NICKNAME_WIDTH = 5      # Column width for account nicknames
SUBS_COUNT_WIDTH = 11   # Column width for submarine count display
HOURS_WIDTH = 24        # Column width for hours/ready status display
STATUS_WIDTH = 10       # Column width for game status (Running/Closed)
PID_WIDTH = 11          # Column width for PID display (e.g., "PID: 12345 ")
TIMER_REFRESH_INTERVAL = 30   # Refresh submarine timers every 30 seconds
WINDOW_REFRESH_INTERVAL = 60  # Check game window status every 60 seconds

# Auto-close game settings
ENABLE_AUTO_CLOSE = True        # Enable automatic game closing when subs not ready soon
AUTO_CLOSE_THRESHOLD = 0.5      # Close game if soonest sub return time > this many hours
MAX_RUNTIME = 71

# Auto-launch game settings
ENABLE_AUTO_LAUNCH = True       # Enable automatic game launching when subs nearly ready
AUTO_LAUNCH_THRESHOLD = 0.15    # Launch game if soonest sub return time <= this many hours (9 minutes)
OPEN_DELAY_THRESHOLD = 60       # Minimum seconds between game launches (prevents opening multiple games too quickly)
MAX_CLIENTS = 0                 # Maximum concurrent running clients (0 = unlimited, N = limit to N clients)
                                # Used for hardware-limited setups that can only run a set number of game instances

# Window arrangement settings
ENABLE_WINDOW_LAYOUT = False     # Enable automatic window arrangement after launching games
WINDOW_LAYOUT = "main"          # Which layout to use: "left" or "main"
WINDOW_MOVER_DIR = Path(__file__).parent  # Local folder where window layout JSON files are stored

# Debug settings
DEBUG = False                   # Show debug output (auto-launch checks, window detection, etc.)

# Single client mode settings
USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME = False  # If True, uses default FFXIV window title (single account only)
                                             # If False, uses "ProcessID - nickname" format (multiple accounts)

# ===============================================
# Account locations
# ===============================================
user = getpass.getuser()

def acc(nickname, pluginconfigs_path, include_submarines=True, force247uptime=False):
    auto_path = os.path.join(pluginconfigs_path, "AutoRetainer", "DefaultConfig.json")
    return {
        "nickname": nickname,
        "auto_path": auto_path,
        "include_submarines": bool(include_submarines),
        "force247uptime": bool(force247uptime),
    }

# In the splatoon script: Rename($"{Environment.ProcessId} - nickname"
# replace 'nickname' with "Main" of "Acc1" keep the space and dash

# # Account configuration - matches AR Parser order
account_locations = [
    acc("Main",   f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs", include_submarines=True, force247uptime=False),
    # acc("Acc1",   f"C:\\Users\\{user}\\AltData\\Acc1\\pluginConfigs", include_submarines=True, force247uptime=False),
    # acc("Acc2",   f"C:\\Users\\{user}\\AltData\\Acc2\\pluginConfigs", include_submarines=True, force247uptime=False),
    # acc("Acc3",   f"C:\\Users\\{user}\\AltData\\Acc3\\pluginConfigs", include_submarines=True, force247uptime=False),
]

# # Game launcher paths for each account (update these paths to your actual game launchers)
GAME_LAUNCHERS = {
    "Main":   rf"C:\Users\{user}\AppData\Local\XIVLauncher\XIVLauncher.exe",
    # "Acc1":   rf"C:\Users\{user}\AltData\Acc1.bat",
    # "Acc2":   rf"C:\Users\{user}\AltData\Acc2.bat",
    # "Acc3":   rf"C:\Users\{user}\AltData\Acc3.bat",
}

# ===============================================
# Submarine Build Gil Rates (from AR Parser)
# Gil/Sub/Day rates for each route
# ===============================================
build_gil_rates = {
    # OJ Route (24h) - 118,661 gil/day
    "WSUC": 118661,
    "SSUC": 118661,
    "W+S+U+C+": 118661,  # WSUC++
    "S+S+S+C+": 118661,  # SSSC++
    
    # MOJ Route (36h) - 93,165 gil/day
    "YUUW": 93165,
    "Y+U+U+W+": 93165,  # YU+U+W+
    
    # ROJ Route (36h) - 106,191 gil/day
    "WCSU": 106191,
    "WUSS": 106191,
    "W+U+S+S+": 106191,  # WUSS++
    
    # JOZ Route (36h) - 113,321 gil/day
    "YSYC": 113321,
    "Y+S+Y+C+": 113321,  # YS+YC+
    
    # MROJ Route (36h) - 120,728 gil/day
    "S+S+S+C+": 120728,  # SSSC++
    "S+S+U+C+": 120728,  # SSUC++
    
    # JORZ Route (36h) - 140,404 gil/day (highest gil/day)
    "S+S+U+C": 140404,
    "S+S+U+C+": 140404,  # SSUC++ variant for JORZ
    
    # JORZ 48h Route - 105,303 gil/day
    "WCYC": 105303,
    "WUWC": 105303,
    "W+U+W+C+": 105303,  # WUWC++
    
    # MOJZ Route (36h) - 127,857 gil/day
    # MOJZ uses SSUC++ at rank 110
    
    # MROJZ Route (48h) - 116,206 gil/day
    "YSCU": 116206,
    "SCUS": 116206,
    "S+C+U+S+": 116206,  # SCUS++
}

# ===============================================
# Submarine Build Consumption Rates (from Routes.xlsx)
# Tanks (Ceruleum) and Repair Kits per day for each build
# ===============================================
build_consumption_rates = {
    # OJ Route (24h) - 9 tanks/day, 1.33 kits/day
    "WSUC": {"tanks_per_day": 9.0, "kits_per_day": 1.33},
    "SSUC": {"tanks_per_day": 9.0, "kits_per_day": 1.33},
    "W+S+U+C+": {"tanks_per_day": 9.0, "kits_per_day": 1.33},  # WSUC++
    "S+S+S+C+": {"tanks_per_day": 9.0, "kits_per_day": 1.33},  # SSSC++ (for OJ route)
    
    # MOJ Route (36h) - 10 tanks/day, 1.6 kits/day
    "YUUW": {"tanks_per_day": 10.0, "kits_per_day": 1.6},
    "Y+U+U+W+": {"tanks_per_day": 10.0, "kits_per_day": 1.6},  # YU+U+W+
    
    # ROJ Route (36h) - 10 tanks/day, 1.67 kits/day
    "WCSU": {"tanks_per_day": 10.0, "kits_per_day": 1.67},
    "WUSS": {"tanks_per_day": 10.0, "kits_per_day": 1.67},
    "W+U+S+S+": {"tanks_per_day": 10.0, "kits_per_day": 1.67},  # WUSS++
    
    # JOZ Route (36h) - 10 tanks/day, 2.5 kits/day
    "YSYC": {"tanks_per_day": 10.0, "kits_per_day": 2.5},
    "Y+S+Y+C+": {"tanks_per_day": 10.0, "kits_per_day": 2.5},  # YS+YC+
    
    # WCYC builds (JORZ 48h) - 10.5 tanks/day, 3 kits/day
    "WCYC": {"tanks_per_day": 10.5, "kits_per_day": 3.0},
    "WUWC": {"tanks_per_day": 10.5, "kits_per_day": 3.0},
    "W+U+W+C+": {"tanks_per_day": 10.5, "kits_per_day": 3.0},  # WUWC++
    
    # YSCU/SCUS builds (MROJZ 48h) - 13.5 tanks/day, 4 kits/day
    "YSCU": {"tanks_per_day": 13.5, "kits_per_day": 4.0},
    "SCUS": {"tanks_per_day": 13.5, "kits_per_day": 4.0},
    "S+C+U+S+": {"tanks_per_day": 13.5, "kits_per_day": 4.0},  # SCUS++
}

# For builds that can be on multiple routes, use the highest consumption rate
# SSSC++ and SSUC++ appear in multiple routes - use MROJ/JORZ rates (14 tanks, 1.78-4 kits)
if "S+S+S+C+" not in build_consumption_rates or build_consumption_rates["S+S+S+C+"]["tanks_per_day"] < 14:
    build_consumption_rates["S+S+S+C+"] = {"tanks_per_day": 14.0, "kits_per_day": 1.78}  # MROJ rate
if "S+S+U+C+" not in build_consumption_rates or build_consumption_rates["S+S+U+C+"]["tanks_per_day"] < 14:
    build_consumption_rates["S+S+U+C+"] = {"tanks_per_day": 14.0, "kits_per_day": 4.0}  # MOJZ rate (highest kit usage)

# SSUC unmodified appears in multiple routes - use JORZ rate (14 tanks, 1.78 kits)
build_consumption_rates["S+S+U+C"] = {"tanks_per_day": 14.0, "kits_per_day": 1.78}

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

def move_window_to_position(hwnd, x, y, w, h, topmost=False, activate=False):
    insert_after = HWND_TOPMOST if topmost else HWND_NOTOPMOST
    flags = SWP_FRAMECHANGED | SWP_SHOWWINDOW
    if not activate:
        flags |= SWP_NOACTIVATE
    SetWindowPos(hwnd, insert_after, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | flags)
    SetWindowPos(hwnd, HWND_TOP, x, y, w, h, SWP_NOACTIVATE | SWP_FRAMECHANGED | SWP_SHOWWINDOW)

def arrange_ffxiv_windows():
    """Arrange all FFXIV game windows according to the configured layout"""
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
    
    # Apply moves with temporary topmost
    for rule, hwnd, title in assigned:
        x = int(rule["x"])
        y = int(rule["y"])
        w = int(rule["width"])
        h = int(rule["height"])
        activate = bool(rule.get("activate", False))
        
        try:
            restore_if_minimized(hwnd)
            remove_maximize_state(hwnd)
            move_window_to_position(hwnd, x, y, w, h, topmost=True, activate=activate)
            if DEBUG:
                print(f"[WINDOW-MOVER] Moved: '{title}' -> ({x},{y},{w},{h})")
            time.sleep(0.03)
        except Exception as e:
            if DEBUG:
                print(f"[WINDOW-MOVER] Failed to move '{title}': {e}")
    
    # Remove topmost from windows that shouldn't have it
    time.sleep(0.1)
    for rule, hwnd, title in assigned:
        topmost = bool(rule.get("topmost", False))
        try:
            if not topmost:
                flags = SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_FRAMECHANGED
                SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, flags)
        except Exception as e:
            if DEBUG:
                print(f"[WINDOW-MOVER] Failed to set final topmost for '{title}': {e}")
    
    if DEBUG:
        print(f"[WINDOW-MOVER] Window arrangement complete")
    return True

def kill_process_by_pid(pid):
    """
    Kill a process by its Process ID using taskkill command.
    Returns True if successful, False otherwise.
    """
    try:
        # Use taskkill /F /PID to force terminate the process
        result = subprocess.run(
            ["taskkill", "/F", "/PID", str(pid)],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Failed to kill process {pid}: {e}")
        return False

def kill_ffxiv_process():
    """
    Kill FFXIV process by terminating ffxiv_dx11.exe.
    Used when USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME is True.
    Returns True if successful, False otherwise.
    """
    try:
        # Use taskkill /F /IM to force terminate the process by image name
        result = subprocess.run(
            ["taskkill", "/F", "/IM", "ffxiv_dx11.exe"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Failed to kill ffxiv_dx11.exe: {e}")
        return False

def launch_game(nickname):
    """
    Launch the game for a specific account using the configured launcher path.
    Returns True if successfully launched, False otherwise.
    """
    launcher_path = GAME_LAUNCHERS.get(nickname)
    
    if not launcher_path:
        print(f"[ERROR] No launcher path configured for {nickname}")
        return False
    
    if not os.path.exists(launcher_path):
        print(f"[ERROR] Launcher not found: {launcher_path}")
        return False
    
    try:
        # Check if it's a batch file
        is_batch_file = launcher_path.lower().endswith('.bat')
        
        if is_batch_file:
            # For batch files, use cmd.exe with /c to close CMD after execution
            # Using shell=True with the proper command avoids lingering CMD windows
            subprocess.Popen(
                f'start "" /B "{launcher_path}"',
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            # For executables, use normal Popen
            subprocess.Popen(
                [launcher_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        return True
    except Exception as e:
        print(f"[ERROR] Failed to launch game for {nickname}: {e}")
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

def get_ffxiv_process_start_time():
    """
    Get the start time of the ffxiv_dx11.exe process for single client mode.
    Returns the start time as a timestamp (seconds since epoch) or None if unavailable.
    Used when USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME is True.
    """
    if not PSUTIL_AVAILABLE:
        return None
    
    try:
        # Search for ffxiv_dx11.exe process
        for proc in psutil.process_iter(['name', 'create_time']):
            try:
                if proc.info['name'].lower() == 'ffxiv_dx11.exe':
                    return proc.info['create_time']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Could not find ffxiv_dx11.exe process: {e}")
        return None

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
        "total_ceruleum": 0,  # Total tanks across all characters
        "total_repair_kits": 0,  # Total repair kits across all characters
        "days_until_restocking": None  # Minimum days until restocking needed
    }
    
    if not include_subs:
        return result
    
    if not os.path.isfile(auto_path):
        return result
    
    try:
        with open(auto_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        
        chars = collect_characters(data, account_nickname=nickname)
        current_time = datetime.datetime.now().timestamp()
        
        all_return_times = []
        
        # Collect inventory data for restocking calculation
        character_days_remaining = []
        
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
            
            # First pass: Collect submarine builds from all submarines
            for offline_sub in offline_sub_data:
                sub_name = offline_sub.get("Name", "")
                # Look up build data using the submarine's actual name
                if sub_name in sub_info:
                    parts_str = get_sub_parts_string(sub_info[sub_name])
                    if parts_str:
                        result["sub_builds"].append(parts_str)
                        char_builds.append(parts_str)
            
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
    
    except Exception as e:
        print(f"[ERROR] Failed to process {nickname}: {e}")
    
    return result

def format_hours(hours, ready_count=0, is_running=False):
    """Format hours with + prefix for positive values and ready count"""
    if hours is None:
        return "N/A"
    if hours >= 0:
        # Show (WAITING) when game is running with 0 ready subs and positive hours
        if is_running and ready_count == 0 and hours <= AUTO_CLOSE_THRESHOLD:
            return f"+{hours:.1f} hours (WAITING)"
        return f"+{hours:.1f} hours"
    else:
        # Negative means already returned
        return f"{hours:.1f} hours ({ready_count} READY)"

def display_submarine_timers(game_status_dict=None, client_start_times=None):
    """Display submarine timers for all accounts"""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Use empty dict if none provided
    if game_status_dict is None:
        game_status_dict = {}
    if client_start_times is None:
        client_start_times = {}
    
    print("=" * 85)
    print("FFXIV Submarine Timer Monitor")
    print("=" * 85)
    print(f"Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 85)
    print()
    
    account_data = []
    total_ready_subs = 0
    total_all_subs = 0
    all_builds = []
    all_days_remaining = []
    
    for account_entry in account_locations:
        timer_data = get_submarine_timers_for_account(account_entry)
        account_data.append(timer_data)
        total_ready_subs += timer_data["ready_subs"]
        total_all_subs += timer_data["total_subs"]
        all_builds.extend(timer_data["sub_builds"])
        if timer_data.get("days_until_restocking") is not None:
            all_days_remaining.append(timer_data["days_until_restocking"])
    
    # Display results
    for data in account_data:
        nickname = data["nickname"]
        total_subs = data["total_subs"]
        ready_subs = data["ready_subs"]
        soonest_hours = data["soonest_hours"]
        
        if not data["include_submarines"]:
            # Show game status even with submarines disabled (for force247uptime monitoring)
            subs_disabled_str = "Disabled"
            
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
                                            uptime_part = f"UPTIME: {uptime_hours:.1f} hours"
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
                                uptime_part = f"UPTIME: {uptime_hours:.1f} hours"
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
                                            uptime_part = f"UPTIME: {uptime_hours:.1f} hours"
                                            pid_uptime_str = f"{pid_formatted}{uptime_part}"
                                        else:
                                            pid_uptime_str = pid_formatted
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
                            uptime_part = f"UPTIME: {uptime_hours:.1f} hours"
                            pid_uptime_str = f"{pid_formatted}{uptime_part}"
                        else:
                            pid_uptime_str = pid_formatted
                else:
                    # Show [Up 24/7] if force247uptime is True, otherwise [Closed]
                    if force247:
                        status_str = f"{'[Up 24/7]':{STATUS_WIDTH}s}"
                    else:
                        status_str = f"{'[Closed]':{STATUS_WIDTH}s}"
            
            hours_str = format_hours(soonest_hours, ready_subs, is_running=(is_running if is_running is not None else False))
            subs_str = f"({total_subs} subs)"
            print(f"{nickname:{NICKNAME_WIDTH}s} {subs_str:{SUBS_COUNT_WIDTH}s}: {hours_str:{HOURS_WIDTH}s}{status_str}{pid_uptime_str}")
    
    print()
    print("=" * 85)
    
    # Calculate total daily gil earnings and submarine counts
    total_daily_gil = 0
    farming_subs_count = 0
    for build in all_builds:
        if build in build_gil_rates:
            total_daily_gil += build_gil_rates[build]
            farming_subs_count += 1
    
    leveling_subs_count = total_all_subs - farming_subs_count
    
    # Calculate minimum days until restocking
    min_days_until_restocking = min(all_days_remaining) if all_days_remaining else None
    
    # Display totals
    print(f"Total Subs: {total_ready_subs} / {total_all_subs}")
    print(f"Total Gil Per Day: {total_daily_gil:,}")
    print(f"Total Subs Leveling: {leveling_subs_count}")
    print(f"Total Subs Farming: {farming_subs_count}")
    if min_days_until_restocking is not None:
        print(f"Total Days Until Restocking Required: {min_days_until_restocking}")
    if MAX_CLIENTS > 0:
        print(f"Max Clients: {MAX_CLIENTS}")
    
    print("=" * 85)
    print("Press Ctrl+C to exit")
    print("=" * 85)

def main():
    """Main loop - continuously update display with dual refresh rates"""
    try:
        # Validate configuration: single client mode requires only 1 account
        if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
            if len(account_locations) > 1:
                print("[ERROR] USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME is True but multiple accounts are configured.")
                print("[ERROR] Single client mode only supports 1 account.")
                print(f"[ERROR] Currently configured accounts: {len(account_locations)}")
                print("[ERROR] Please disable USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME or configure only 1 account.")
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
                last_window_check = current_time
            
            # Display submarine timers with current game status FIRST
            display_submarine_timers(game_status_dict, client_start_times)
            
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
                                print(f"[DEBUG] {nickname}: Already running, skipping")
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
                        print(f"\n[AUTO-LAUNCH] Launching {nickname} - {reason}")
                        
                        if launch_game(nickname):
                            last_launch_time[nickname] = current_time
                            print(f"[AUTO-LAUNCH] Successfully launched {nickname}, waiting {OPEN_DELAY_THRESHOLD} seconds before next client...")
                            
                            # Wait OPEN_DELAY_THRESHOLD before next launch
                            time.sleep(OPEN_DELAY_THRESHOLD)
                            
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
                            display_submarine_timers(game_status_dict, client_start_times)
                            print("")  # Empty line for spacing
                        else:
                            print(f"[AUTO-LAUNCH] Failed to launch {nickname}")
                            last_launch_time[nickname] = current_time  # Record failed attempt to enforce rate limit
            
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
                        
                        # Use appropriate kill method based on mode
                        kill_success = False
                        if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
                            kill_success = kill_ffxiv_process()
                        else:
                            kill_success = kill_process_by_pid(process_id)
                        
                        if kill_success:
                            closed_pids.add(process_id) if process_id else None
                            print(f"[AUTO-CLOSE] Successfully closed {nickname} after {uptime_hours:.1f}h, waiting {TIMER_REFRESH_INTERVAL} seconds before checking clients again.")
                            # Update game status immediately
                            game_status_dict[nickname] = (False, None)
                            # Enforce launch delay after runtime-based restart
                            last_launch_time[nickname] = current_time
                            # Clean up start time tracking
                            if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
                                if 'ffxiv_single' in client_start_times:
                                    del client_start_times['ffxiv_single']
                            elif process_id and process_id in client_start_times:
                                del client_start_times[process_id]
                        else:
                            print(f"[AUTO-CLOSE] Failed to close {nickname}")
                        continue

                    # Do not auto-close force247uptime accounts based on submarine timers
                    if rotating_retainers:
                        continue

                    # Close game if submarines disabled AND force247uptime is False
                    # (no submarines and no reason to keep game running)
                    if not include_subs and not rotating_retainers:
                        print(f"\n[AUTO-CLOSE] Closing {nickname} (PID: {process_id}) - Submarines disabled, force247uptime=False")
                        
                        # Use appropriate kill method based on mode
                        kill_success = False
                        if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
                            kill_success = kill_ffxiv_process()
                        else:
                            kill_success = kill_process_by_pid(process_id)
                        
                        if kill_success:
                            closed_pids.add(process_id) if process_id else None
                            print(f"[AUTO-CLOSE] Successfully closed {nickname}, waiting {TIMER_REFRESH_INTERVAL} seconds before checking clients again.")
                            # Update game status immediately
                            game_status_dict[nickname] = (False, None)
                            # Reset launch time
                            if nickname in last_launch_time:
                                del last_launch_time[nickname]
                            # Clean up start time tracking
                            if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
                                if 'ffxiv_single' in client_start_times:
                                    del client_start_times['ffxiv_single']
                            elif process_id and process_id in client_start_times:
                                del client_start_times[process_id]
                        else:
                            print(f"[AUTO-CLOSE] Failed to close {nickname}")
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
                        
                        # Use appropriate kill method based on mode
                        kill_success = False
                        if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
                            kill_success = kill_ffxiv_process()
                        else:
                            kill_success = kill_process_by_pid(process_id)
                        
                        if kill_success:
                            closed_pids.add(process_id) if process_id else None
                            print(f"[AUTO-CLOSE] Successfully closed {nickname}, waiting {TIMER_REFRESH_INTERVAL} seconds before checking clients again.")
                            # Update game status immediately
                            game_status_dict[nickname] = (False, None)
                            # Reset launch time so it can be relaunched if subs become ready
                            if nickname in last_launch_time:
                                del last_launch_time[nickname]
                            # Clean up start time tracking
                            if USE_SINGLE_CLIENT_FFIXV_NO_NICKNAME:
                                if 'ffxiv_single' in client_start_times:
                                    del client_start_times['ffxiv_single']
                            elif process_id and process_id in client_start_times:
                                del client_start_times[process_id]
                        else:
                            print(f"[AUTO-CLOSE] Failed to close {nickname}")
            
            # Wait for TIMER_REFRESH_INTERVAL seconds before next timer update
            time.sleep(TIMER_REFRESH_INTERVAL)
    except KeyboardInterrupt:
        print("\n\nExiting submarine timer monitor...")
        sys.exit(0)

if __name__ == "__main__":
    main()
