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
# Auto-AutoRetainer v1.00
# Automated FFXIV Submarine Management System
# Created by: https://github.com/xa-io
# Last Updated: 2025-11-12 17:19:40
#
# ## Release Notes ##
#
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

# ===============================================
# Configuration Parameters
# ===============================================
NICKNAME_WIDTH = 5      # Column width for account nicknames
SUBS_COUNT_WIDTH = 11   # Column width for submarine count display
HOURS_WIDTH = 24        # Column width for hours/ready status display
STATUS_WIDTH = 10       # Column width for game status (Running/Closed)
TIMER_REFRESH_INTERVAL = 30   # Refresh submarine timers every 30 seconds
WINDOW_REFRESH_INTERVAL = 60  # Check game window status every 60 seconds

# Auto-close game settings
ENABLE_AUTO_CLOSE = True        # Enable automatic game closing when subs not ready soon
AUTO_CLOSE_THRESHOLD = 0.5      # Close game if soonest sub return time > this many hours

# Auto-launch game settings
ENABLE_AUTO_LAUNCH = True       # Enable automatic game launching when subs nearly ready
AUTO_LAUNCH_THRESHOLD = 0.15    # Launch game if soonest sub return time <= this many hours (9 minutes)
OPEN_DELAY_THRESHOLD = 60       # Minimum seconds between game launches (prevents opening multiple games too quickly)

# Window arrangement settings
ENABLE_WINDOW_LAYOUT = True     # Enable automatic window arrangement after launching games
WINDOW_LAYOUT = "main"          # Which layout to use: "left" or "main"
WINDOW_MOVER_DIR = Path(__file__).parent  # Local folder where window layout JSON files are stored

# Debug settings
DEBUG = False                   # Show debug output (auto-launch checks, window detection, etc.)

# ===============================================
# Account locations
# ===============================================
user = getpass.getuser()

def acc(nickname, pluginconfigs_path, include_submarines=True):
    auto_path = os.path.join(pluginconfigs_path, "AutoRetainer", "DefaultConfig.json")
    return {
        "nickname": nickname,
        "auto_path": auto_path,
        "include_submarines": bool(include_submarines),
    }

# In the splatoon script: Rename($"{Environment.ProcessId} - nickname"
# replace 'nickname' with "Main" of "Acc1" keep the space and dash

# Account configuration - matches AR Parser order
 account_locations = [
     acc("Main",   f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs", include_submarines=False),
     acc("Acc1",   f"C:\\Users\\{user}\\AltData\\Acc1\\pluginConfigs", include_submarines=True),
     # acc("Acc2",   f"C:\\Users\\{user}\\AltData\\Acc2\\pluginConfigs", include_submarines=True),
     # acc("Acc3",   f"C:\\Users\\{user}\\AltData\\Acc3\\pluginConfigs", include_submarines=True),
 ]

# # Game launcher paths for each account (update these paths to your actual game launchers)
 GAME_LAUNCHERS = {
     "Main":   rf"C:\Users\{user}\AppData\Local\XIVLauncher\XIVLauncher.exe",
     "Acc1":   rf"C:\Users\{user}\AltData\Acc1.bat",
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

def is_ffxiv_running_for_account(nickname):
    """
    Check if FFXIV is running for a specific account by looking for windows
    with titles matching the pattern: 'ProcessID - nickname'
    Returns tuple: (is_running, process_id)
    - is_running: True if a matching window is found, False otherwise
    - process_id: The process ID if running, None if not running
    """
    try:
        found_windows = []
        
        def enum_callback(hwnd, extra):
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title.strip():
                    found_windows.append(title)
        
        win32gui.EnumWindows(enum_callback, None)
        
        # Check if any window title matches the pattern: "ProcessID - nickname"
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
        "sub_builds": []  # Track submarine builds for gil calculation
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
        
        for char in chars:
            # Get submarine build data from AdditionalSubmarineData
            sub_info = char.get("AdditionalSubmarineData", {})
            for sub_key, sub_dict in sub_info.items():
                if sub_key.startswith("Submersible-"):
                    parts_str = get_sub_parts_string(sub_dict)
                    if parts_str:
                        result["sub_builds"].append(parts_str)
            
            # Get submarine data from OfflineSubmarineData
            offline_sub_data = char.get("OfflineSubmarineData", [])
            
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
    
    except Exception as e:
        print(f"[ERROR] Failed to process {nickname}: {e}")
    
    return result

def format_hours(hours, ready_count=0):
    """Format hours with + prefix for positive values and ready count"""
    if hours is None:
        return "N/A"
    if hours >= 0:
        return f"+{hours:.1f} hours"
    else:
        # Negative means already returned
        return f"{hours:.1f} hours ({ready_count} READY)"

def display_submarine_timers(game_status_dict=None):
    """Display submarine timers for all accounts"""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Use empty dict if none provided
    if game_status_dict is None:
        game_status_dict = {}
    
    print("=" * 65)
    print("FFXIV Submarine Timer Monitor")
    print("=" * 65)
    print(f"Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    print()
    
    account_data = []
    total_ready_subs = 0
    total_all_subs = 0
    all_builds = []
    
    for account_entry in account_locations:
        timer_data = get_submarine_timers_for_account(account_entry)
        account_data.append(timer_data)
        total_ready_subs += timer_data["ready_subs"]
        total_all_subs += timer_data["total_subs"]
        all_builds.extend(timer_data["sub_builds"])
    
    # Display results
    for data in account_data:
        nickname = data["nickname"]
        total_subs = data["total_subs"]
        ready_subs = data["ready_subs"]
        soonest_hours = data["soonest_hours"]
        
        if not data["include_submarines"]:
            # Don't show game status for accounts with submarines disabled
            disabled_str = "Submarines disabled"
            print(f"{nickname:{NICKNAME_WIDTH}s} {disabled_str:{SUBS_COUNT_WIDTH}s}")
        elif total_subs == 0:
            no_subs_str = "No submarines found"
            print(f"{nickname:{NICKNAME_WIDTH}s} {no_subs_str:{SUBS_COUNT_WIDTH}s}  {'':{HOURS_WIDTH}s}")
        else:
            # Get game status for this account (only show for enabled submarines)
            game_info = game_status_dict.get(nickname, (None, None))
            is_running = game_info[0]
            process_id = game_info[1]
            
            status_str = ""
            pid_str = ""
            if is_running is not None:
                if is_running:
                    status_str = f"{'[Running]':{STATUS_WIDTH}s}"
                    if process_id:
                        pid_str = f"PID: {process_id}"
                else:
                    status_str = f"{'[Closed]':{STATUS_WIDTH}s}"
            
            hours_str = format_hours(soonest_hours, ready_subs)
            subs_str = f"({total_subs} subs)"
            print(f"{nickname:{NICKNAME_WIDTH}s} {subs_str:{SUBS_COUNT_WIDTH}s}: {hours_str:{HOURS_WIDTH}s}{status_str}{pid_str}")
    
    print()
    print("=" * 65)
    
    # Calculate total daily gil earnings from submarine builds
    total_daily_gil = 0
    for build in all_builds:
        if build in build_gil_rates:
            total_daily_gil += build_gil_rates[build]
    
    # Display totals
    print(f"Total Subs: {total_ready_subs} / {total_all_subs}")
    if total_daily_gil > 0:
        print(f"Total Gil Per Day: {total_daily_gil:,}")
    
    print("=" * 65)
    print("Press Ctrl+C to exit")
    print("=" * 65)

def main():
    """Main loop - continuously update display with dual refresh rates"""
    try:
        # Track last window check time (set to negative to force immediate check on first run)
        last_window_check = -WINDOW_REFRESH_INTERVAL
        game_status_dict = {}
        closed_pids = set()  # Track PIDs we've already closed to avoid repeated attempts
        last_launch_time = {}  # Track last launch time for each account to enforce rate limiting
        initial_arrangement_done = False  # Track if we've done initial window arrangement
        
        while True:
            current_time = time.time()
            
            # Check if we need to refresh window status (every WINDOW_REFRESH_INTERVAL seconds)
            if current_time - last_window_check >= WINDOW_REFRESH_INTERVAL:
                # Update game status for all accounts (stores tuple: (is_running, process_id))
                for account_entry in account_locations:
                    nickname = account_entry["nickname"]
                    game_status_dict[nickname] = is_ffxiv_running_for_account(nickname)
                last_window_check = current_time
            
            # Display submarine timers with current game status FIRST
            display_submarine_timers(game_status_dict)
            
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
                for account_entry in account_locations:
                    nickname = account_entry["nickname"]
                    
                    # Skip if submarines are disabled for this account
                    if not account_entry.get("include_submarines", True):
                        if DEBUG:
                            print(f"[DEBUG] {nickname}: Submarines disabled, skipping")
                        continue
                    
                    # Get game status
                    game_info = game_status_dict.get(nickname, (None, None))
                    is_running = game_info[0]
                    
                    if DEBUG:
                        print(f"[DEBUG] {nickname}: is_running={is_running}, game_info={game_info}")
                    
                    # Only launch if game is NOT already running
                    if is_running:
                        if DEBUG:
                            print(f"[DEBUG] {nickname}: Already running, skipping")
                        continue
                    
                    # Get submarine timer data
                    timer_data = get_submarine_timers_for_account(account_entry)
                    soonest_hours = timer_data.get("soonest_hours")
                    
                    if DEBUG:
                        print(f"[DEBUG] {nickname}: soonest_hours={soonest_hours}, threshold={AUTO_LAUNCH_THRESHOLD}")
                    
                    # Check if we should launch the game
                    # Launch if soonest_hours <= AUTO_LAUNCH_THRESHOLD
                    # This includes submarines already ready (negative hours) or nearly ready (positive hours <= threshold)
                    if soonest_hours is not None and soonest_hours <= AUTO_LAUNCH_THRESHOLD:
                        if DEBUG:
                            print(f"[DEBUG] {nickname}: Passed threshold check!")
                        # Check rate limiting - only launch if it's been at least OPEN_DELAY_THRESHOLD seconds
                        last_launch = last_launch_time.get(nickname, 0)
                        time_since_last_launch = current_time - last_launch
                        
                        if time_since_last_launch < OPEN_DELAY_THRESHOLD:
                            # Too soon since last launch attempt, skip
                            continue
                        
                        # Attempt to launch the game
                        if soonest_hours < 0:
                            ready_count = timer_data.get("ready_subs", 0)
                            print(f"\n[AUTO-LAUNCH] Launching {nickname} - {ready_count} submarines ready")
                        else:
                            minutes_remaining = soonest_hours * 60
                            print(f"\n[AUTO-LAUNCH] Launching {nickname} - Sub ready in {minutes_remaining:.1f} minutes")
                        
                        if launch_game(nickname):
                            last_launch_time[nickname] = current_time
                            print(f"[AUTO-LAUNCH] Successfully launched {nickname}")
                            if DEBUG:
                                print(f"[AUTO-LAUNCH] Waiting 60 seconds for game to start...")
                            # Wait WINDOW_REFRESH_INTERVAL before next launch attempt to give it time to start
                            time.sleep(WINDOW_REFRESH_INTERVAL)
                            # Force window status refresh after launch and check if detected
                            if DEBUG:
                                print(f"[AUTO-LAUNCH] Checking if {nickname} is now detected...")
                            for acc_entry in account_locations:
                                acc_nickname = acc_entry["nickname"]
                                game_status_dict[acc_nickname] = is_ffxiv_running_for_account(acc_nickname)
                                if acc_nickname == nickname and DEBUG:
                                    new_status = game_status_dict[acc_nickname]
                                    print(f"[AUTO-LAUNCH] {nickname} window status: {new_status}")
                            last_window_check = current_time
                            
                            # Arrange all windows after launching and detecting (if enabled)
                            if ENABLE_WINDOW_LAYOUT:
                                arrange_ffxiv_windows()
                        else:
                            print(f"[AUTO-LAUNCH] Failed to launch {nickname}")
                            last_launch_time[nickname] = current_time  # Record failed attempt to enforce rate limit
            
            # Auto-close games if enabled and conditions are met
            if ENABLE_AUTO_CLOSE:
                for account_entry in account_locations:
                    nickname = account_entry["nickname"]
                    
                    # Skip if submarines are disabled for this account
                    if not account_entry.get("include_submarines", True):
                        continue
                    
                    # Get game status
                    game_info = game_status_dict.get(nickname, (None, None))
                    is_running = game_info[0]
                    process_id = game_info[1]
                    
                    # Only proceed if game is running and we have a PID
                    if not is_running or not process_id:
                        continue
                    
                    # Skip if we've already closed this PID
                    if process_id in closed_pids:
                        continue
                    
                    # Get submarine timer data
                    timer_data = get_submarine_timers_for_account(account_entry)
                    soonest_hours = timer_data.get("soonest_hours")
                    
                    # Check if we should close the game
                    # Close if soonest_hours > AUTO_CLOSE_THRESHOLD (submarines won't be ready soon)
                    if soonest_hours is not None and soonest_hours > AUTO_CLOSE_THRESHOLD:
                        print(f"\n[AUTO-CLOSE] Closing {nickname} (PID: {process_id}) - Next sub in {soonest_hours:.1f}h")
                        if kill_process_by_pid(process_id):
                            closed_pids.add(process_id)
                            print(f"[AUTO-CLOSE] Successfully closed {nickname}")
                            # Update game status immediately
                            game_status_dict[nickname] = (False, None)
                            # Reset launch time so it can be relaunched if subs become ready
                            if nickname in last_launch_time:
                                del last_launch_time[nickname]
                        else:
                            print(f"[AUTO-CLOSE] Failed to close {nickname}")
            
            # Wait for TIMER_REFRESH_INTERVAL seconds before next timer update
            time.sleep(TIMER_REFRESH_INTERVAL)
    except KeyboardInterrupt:
        print("\n\nExiting submarine timer monitor...")
        sys.exit(0)

if __name__ == "__main__":
    main()
