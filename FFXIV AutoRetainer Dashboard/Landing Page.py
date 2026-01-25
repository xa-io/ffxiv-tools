############################################################################################################################
#
#  ██╗      █████╗ ███╗   ██╗██████╗ ██╗███╗   ██╗ ██████╗     ██████╗  █████╗  ██████╗ ███████╗
#  ██║     ██╔══██╗████╗  ██║██╔══██╗██║████╗  ██║██╔════╝     ██╔══██╗██╔══██╗██╔════╝ ██╔════╝
#  ██║     ███████║██╔██╗ ██║██║  ██║██║██╔██╗ ██║██║  ███╗    ██████╔╝███████║██║  ███╗█████╗  
#  ██║     ██╔══██║██║╚██╗██║██║  ██║██║██║╚██╗██║██║   ██║    ██╔═══╝ ██╔══██║██║   ██║██╔══╝  
#  ███████╗██║  ██║██║ ╚████║██████╔╝██║██║ ╚████║╚██████╔╝    ██║     ██║  ██║╚██████╔╝███████╗
#  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
#
# FFXIV AutoRetainer Dashboard - Self-Hosted Web Interface
#
# A comprehensive web dashboard that displays FFXIV character data from AutoRetainer's DefaultConfig.json.
# Provides a beautiful, modern UI accessible via browser showing characters, submarines, retainers,
# marketboard items, gil totals, and income/cost calculations.
#
# Core Features:
# • Self-hosted Flask web server with configurable host/port
# • Real-time data parsing from AutoRetainer DefaultConfig.json
# • Character overview with gil, retainers, and submarine counts
# • Submarine tracking with builds, levels, and return times
# • Retainer details with venture status and marketboard items
# • Monthly income calculations based on submarine builds
# • Daily repair cost estimates based on consumption rates
# • Modern, responsive UI with dark theme
# • Multi-account support via config.json
#
# Landing Page v1.02
# FFXIV AutoRetainer Dashboard
# Created by: https://github.com/xa-io
# Last Updated: 2026-01-25 15:30:00
#
# ## Release Notes ##
#
# v1.02 - UI color refinements: blue account headers, red highlights for ready items
# v1.01 - Fixed stale submarine display bug (validates AdditionalSubmarineData against OfflineSubmarineData)
# v1.00 - Initial release with comprehensive dashboard features
#         Flask-based web server with configurable host/port
#         AutoRetainer DefaultConfig.json parsing
#         Character, submarine, and retainer data display
#         Income and cost calculations
#         Modern dark-themed responsive UI
#
############################################################################################################################

###########################################
#### Start of Configuration Parameters ####
###########################################

import json
import os
import datetime
import getpass
import sqlite3
from pathlib import Path
from flask import Flask, render_template_string, jsonify

# ===============================================
# Server Configuration
# ===============================================
HOST = "127.0.0.1"      # Server host address (use "0.0.0.0" for network access)
PORT = 1234             # Server port number
DEBUG = False           # Flask debug mode (set True for development)
AUTO_REFRESH = 60       # Auto-refresh interval in seconds (0 to disable)

# ===============================================
# External config file (optional)
# ===============================================
CONFIG_FILE = "config.json"

# ===============================================
# Account Configuration
# ===============================================
user = getpass.getuser()

def acc(nickname, pluginconfigs_path):
    """Create account configuration dictionary"""
    auto_path = os.path.join(pluginconfigs_path, "AutoRetainer", "DefaultConfig.json")
    alto_path = os.path.join(pluginconfigs_path, "Altoholic", "altoholic.db")
    return {
        "nickname": nickname,
        "auto_path": auto_path,
        "alto_path": alto_path,
    }

# Default account locations - update these paths for your setup
account_locations = [
    acc("Main", f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs"),
    # acc("Acc1", f"C:\\Users\\{user}\\AltData\\Acc1\\pluginConfigs"),
    # acc("Acc2", f"C:\\Users\\{user}\\AltData\\Acc2\\pluginConfigs"),
]

#########################################
#### End of Configuration Parameters ####
#########################################

# ===============================================
# Submarine Build Constants
# ===============================================
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

# Gil rates per submarine build per day (based on Routes.xlsx)
BUILD_GIL_RATES = {
    "WSUC": 118661,
    "SSUC": 118661,
    "W+S+U+C+": 118661,  # WSUC++ (modified)
    "S+S+S+C+": 118661,  # SSSC++ (modified for OJ route)
    
    # MOJ Route (36h) - 93,165 gil/day
    "YUUW": 93165,
    "Y+U+U+W+": 93165,  # YU+U+W+ (modified)
    
    # ROJ Route (36h) - 106,191 gil/day
    "WCSU": 106191,
    "WUSS": 106191,
    "W+U+S+S+": 106191,  # WUSS++ (modified)
    
    # JOZ Route (36h) - 113,321 gil/day
    "YSYC": 113321,
    "Y+S+Y+C+": 113321,  # YS+YC+ (modified)
    
    # MROJ Route (36h) - 120,728 gil/day
    "S+S+S+C+": 120728,  # SSSC++ (modified)
    "S+S+U+C+": 120728,  # SSUC++ (modified)
    
    # JORZ Route (36h) - 140,404 gil/day (highest gil/day)
    "S+S+U+C": 140404,
    "S+S+U+C+": 140404,  # SSUC++ variant for JORZ
    
    # JORZ 48h Route - 105,303 gil/day
    "WCYC": 105303,
    "WUWC": 105303,
    "W+U+W+C+": 105303,  # WUWC++ (modified)
    
    # MOJZ Route (36h) - 127,857 gil/day
    # MOJZ uses SSUC++ at rank 110
    
    # MROJZ Route (48h) - 116,206 gil/day
    "YSCU": 116206,
    "SCUS": 116206,
    "S+C+U+S+": 116206,  # SCUS++ (modified)
}

# Consumption rates per build per day
BUILD_CONSUMPTION_RATES = {
    "SSUC": {"tanks_per_day": 9.0, "kits_per_day": 1.33},
    "WSUC": {"tanks_per_day": 9.0, "kits_per_day": 1.33},
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

# Default consumption for leveling submarines
DEFAULT_CONSUMPTION = {"tanks_per_day": 9.0, "kits_per_day": 1.33}

# ===============================================
# Altoholic Treasure Values
# ===============================================
TREASURE_VALUES = {
    22500: 8000,   # Salvaged Ring
    22501: 9000,   # Salvaged Bracelet
    22502: 10000,  # Salvaged Earring
    22503: 13000,  # Salvaged Necklace
    22504: 27000,  # Extravagant Salvaged Ring
    22505: 28500,  # Extravagant Salvaged Bracelet
    22506: 30000,  # Extravagant Salvaged Earring
    22507: 34500,  # Extravagant Salvaged Necklace
}
TREASURE_IDS = set(TREASURE_VALUES.keys())

# Cost constants
CERULEUM_TANK_COST = 350   # Gil per tank
REPAIR_KIT_COST = 2000     # Gil per kit

# ===============================================
# Flask Application
# ===============================================
app = Flask(__name__)

# ===============================================
# Data Parsing Functions
# ===============================================
def load_external_config():
    """Load external config file if it exists"""
    global HOST, PORT, DEBUG, AUTO_REFRESH, account_locations
    
    config_path = Path(__file__).parent / CONFIG_FILE
    if not config_path.exists():
        return
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        HOST = config.get("HOST", HOST)
        PORT = config.get("PORT", PORT)
        DEBUG = config.get("DEBUG", DEBUG)
        AUTO_REFRESH = config.get("AUTO_REFRESH", AUTO_REFRESH)
        
        if "account_locations" in config:
            new_locations = []
            for acc_config in config["account_locations"]:
                if not acc_config.get("enabled", True):
                    continue
                nickname = acc_config.get("nickname", "Unknown")
                pluginconfigs_path = acc_config.get("pluginconfigs_path", "")
                pluginconfigs_path = os.path.expandvars(pluginconfigs_path)
                pluginconfigs_path = pluginconfigs_path.replace("{user}", user)
                new_locations.append(acc(nickname, pluginconfigs_path))
            account_locations = new_locations
        
        print(f"[CONFIG] Loaded configuration from {config_path}")
    except Exception as e:
        print(f"[CONFIG] Error loading config: {e}")


def shorten_part_name(full_name: str) -> str:
    """Convert full submarine part name to short code"""
    for prefix, code in CLASS_SHORTCUTS.items():
        if full_name.startswith(prefix):
            return code
    return "?"


def get_sub_build_string(sub_data: dict) -> str:
    """Get submarine build string from part IDs"""
    parts = []
    for key in ["Part1", "Part2", "Part3", "Part4"]:
        part_id = sub_data.get(key, 0)
        if part_id != 0:
            full_part_name = SUB_PARTS_LOOKUP.get(part_id, f"Unknown({part_id})")
            short_code = shorten_part_name(full_part_name)
            parts.append(short_code)
    return "".join(parts)


def format_time_remaining(unix_timestamp):
    """Format unix timestamp to human-readable time remaining"""
    if not unix_timestamp:
        return "Unknown"
    
    now = datetime.datetime.now()
    target = datetime.datetime.fromtimestamp(unix_timestamp)
    delta = target - now
    
    if delta.total_seconds() <= 0:
        return "Ready!"
    
    hours = int(delta.total_seconds() // 3600)
    minutes = int((delta.total_seconds() % 3600) // 60)
    
    if hours > 24:
        days = hours // 24
        hours = hours % 24
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def format_gil(amount):
    """Format gil amount with commas"""
    return f"{amount:,}"


def _safe_json_load(s):
    """Safely parse JSON string, handling null/empty values"""
    if not s or s == "null":
        return None
    try:
        return json.loads(s)
    except Exception:
        return None


def scan_altoholic_db(db_path):
    """
    Scan Altoholic DB and return treasure values per character.
    Returns: { CharacterId: {"treasure_value": int} }
    """
    result = {}
    if not os.path.isfile(db_path):
        return result
    
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        rows = cur.execute("SELECT CharacterId, Inventory, Saddle FROM characters").fetchall()
        
        for char_id, inv_json, saddle_json in rows:
            treasure_value = 0
            
            def consume(items):
                nonlocal treasure_value
                if not items:
                    return
                for it in items:
                    iid = it.get("ItemId", 0)
                    qty = it.get("Quantity", 1)
                    if not isinstance(qty, int):
                        try:
                            qty = int(qty)
                        except Exception:
                            qty = 1
                    
                    if iid in TREASURE_IDS:
                        treasure_value += qty * TREASURE_VALUES[iid]
            
            inv = _safe_json_load(inv_json)
            if isinstance(inv, list):
                consume(inv)
            sad = _safe_json_load(saddle_json)
            if isinstance(sad, list):
                consume(sad)
            
            if treasure_value > 0:
                result[int(char_id)] = {"treasure_value": int(treasure_value)}
        
        con.close()
    except Exception as e:
        print(f"[WARNING] Failed to scan Altoholic DB '{db_path}': {e}")
    
    return result


def extract_fc_data(full_data):
    """Extract Free Company data from AutoRetainer config"""
    fc_data = {}
    
    def recursive_search(obj):
        if isinstance(obj, dict):
            if "HolderChara" in obj:
                holder_id = obj["HolderChara"]
                fc_data[holder_id] = {
                    "Name": obj.get("Name", "Unknown FC"),
                    "FCPoints": obj.get("FCPoints", 0)
                }
            for v in obj.values():
                recursive_search(v)
        elif isinstance(obj, list):
            for item in obj:
                recursive_search(item)
    
    recursive_search(full_data)
    return fc_data


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
    
    return all_chars


def parse_submarine_data(char_data):
    """Parse submarine data from character"""
    submarines = []
    
    # Get offline submarine data for return times
    offline_subs = char_data.get("OfflineSubmarineData", [])
    offline_by_name = {}
    for sub in offline_subs:
        if isinstance(sub, dict):
            name = sub.get("Name", "")
            offline_by_name[name] = sub
    
    # Get additional submarine data for builds
    additional_subs = char_data.get("AdditionalSubmarineData", {})
    
    for sub_key, sub_data in additional_subs.items():
        if not isinstance(sub_data, dict):
            continue
        
        name = sub_data.get("Name", sub_key)
        
        # Skip stale submarines that no longer exist in OfflineSubmarineData
        # OfflineSubmarineData is the source of truth for active submarines (max 4)
        if name not in offline_by_name and sub_key not in offline_by_name:
            continue
        
        level = sub_data.get("Level", 0)
        build = get_sub_build_string(sub_data)
        
        # Get return time from offline data
        return_time = None
        if name in offline_by_name:
            return_time = offline_by_name[name].get("ReturnTime", 0)
        
        # Determine if submarine is ready (docked or returned)
        now_ts = datetime.datetime.now().timestamp()
        is_ready = (not return_time) or (return_time <= now_ts)
        
        # Calculate gil rate and consumption
        gil_rate = BUILD_GIL_RATES.get(build, 0)
        consumption = BUILD_CONSUMPTION_RATES.get(build, DEFAULT_CONSUMPTION)
        
        submarines.append({
            "name": name,
            "level": level,
            "build": build if build else "Leveling",
            "return_time": return_time,
            "return_formatted": format_time_remaining(return_time) if return_time else "Docked",
            "is_ready": is_ready,
            "daily_gil": gil_rate,
            "monthly_gil": gil_rate * 30,
            "tanks_per_day": consumption["tanks_per_day"],
            "kits_per_day": consumption["kits_per_day"],
            "daily_cost": (consumption["tanks_per_day"] * CERULEUM_TANK_COST) + 
                         (consumption["kits_per_day"] * REPAIR_KIT_COST),
        })
    
    return submarines


def parse_retainer_data(char_data):
    """Parse retainer data from character"""
    retainers = []
    retainer_data = char_data.get("RetainerData", [])
    
    for ret in retainer_data:
        if not isinstance(ret, dict):
            continue
        
        venture_ends = ret.get("VentureEndsAt", 0)
        
        # Determine if retainer is ready (no venture or venture complete)
        now_ts = datetime.datetime.now().timestamp()
        is_ready = (not venture_ends) or (venture_ends <= now_ts)
        
        retainers.append({
            "name": ret.get("Name", "Unknown"),
            "level": ret.get("Level", 0),
            "job": ret.get("Job", 0),
            "gil": ret.get("Gil", 0),
            "mb_items": ret.get("MBItems", 0),
            "has_venture": ret.get("HasVenture", False),
            "venture_ends": venture_ends,
            "venture_formatted": format_time_remaining(venture_ends) if venture_ends else "None",
            "is_ready": is_ready,
        })
    
    return retainers


def get_all_data():
    """Load and parse all account data"""
    all_accounts = []
    total_gil = 0
    total_subs = 0
    total_retainers = 0
    ready_subs = 0
    ready_retainers = 0
    total_mb_items = 0
    total_daily_income = 0
    total_daily_cost = 0
    total_treasure = 0
    
    for account in account_locations:
        account_data = {
            "nickname": account["nickname"],
            "characters": [],
            "total_gil": 0,
            "total_subs": 0,
            "total_retainers": 0,
            "ready_subs": 0,
            "ready_retainers": 0,
            "total_mb_items": 0,
            "total_treasure": 0,
        }
        
        auto_path = account["auto_path"]
        
        if not os.path.isfile(auto_path):
            account_data["error"] = f"Config not found: {auto_path}"
            all_accounts.append(account_data)
            continue
        
        try:
            with open(auto_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
        except Exception as e:
            account_data["error"] = f"Failed to load: {e}"
            all_accounts.append(account_data)
            continue
        
        fc_data = extract_fc_data(data)
        characters = collect_characters(data, account["nickname"])
        
        # Scan Altoholic database for treasure values
        alto_map = {}
        alto_path = account.get("alto_path", "")
        if alto_path:
            alto_map = scan_altoholic_db(alto_path)
        
        for char in characters:
            cid = char.get("CID", 0)
            char_gil = char.get("Gil", 0)
            
            # Parse submarines
            submarines = parse_submarine_data(char)
            sub_daily_income = sum(s["daily_gil"] for s in submarines)
            sub_daily_cost = sum(s["daily_cost"] for s in submarines)
            
            # Parse retainers
            retainers = parse_retainer_data(char)
            retainer_gil = sum(r["gil"] for r in retainers)
            mb_items = sum(r["mb_items"] for r in retainers)
            
            # Get FC info
            fc_name = ""
            if cid in fc_data:
                fc_name = fc_data[cid].get("Name", "")
            
            # Get treasure value from Altoholic
            treasure_value = 0
            if cid in alto_map:
                treasure_value = alto_map[cid].get("treasure_value", 0)
            
            char_data = {
                "cid": cid,
                "name": char.get("Name", "Unknown"),
                "world": char.get("World", "Unknown"),
                "gil": char_gil,
                "retainer_gil": retainer_gil,
                "total_gil": char_gil + retainer_gil,
                "treasure_value": treasure_value,
                "total_with_treasure": char_gil + retainer_gil + treasure_value,
                "submarines": submarines,
                "retainers": retainers,
                "fc_name": fc_name,
                "ceruleum": char.get("Ceruleum", 0),
                "repair_kits": char.get("RepairKits", 0),
                "ventures": char.get("Ventures", 0),
                "inventory_space": char.get("InventorySpace", 0),
                "gc_seals": char.get("GCSeals", 0),
                "daily_income": sub_daily_income,
                "monthly_income": sub_daily_income * 30,
                "daily_cost": sub_daily_cost,
                "mb_items": mb_items,
            }
            
            # Count ready submarines and retainers
            char_ready_subs = sum(1 for s in submarines if s["is_ready"])
            char_ready_retainers = sum(1 for r in retainers if r["is_ready"])
            
            # Add ready counts to character data
            char_data["ready_subs"] = char_ready_subs
            char_data["total_subs"] = len(submarines)
            char_data["ready_retainers"] = char_ready_retainers
            char_data["total_retainers"] = len(retainers)
            
            account_data["characters"].append(char_data)
            account_data["total_gil"] += char_data["total_gil"]
            account_data["total_subs"] += len(submarines)
            account_data["total_retainers"] += len(retainers)
            account_data["ready_subs"] += char_ready_subs
            account_data["ready_retainers"] += char_ready_retainers
            account_data["total_mb_items"] += mb_items
            account_data["total_treasure"] += treasure_value
            
            total_daily_income += sub_daily_income
            total_daily_cost += sub_daily_cost
        
        # Calculate max MB items for this account (20 per retainer)
        account_data["max_mb_items"] = account_data["total_retainers"] * 20
        
        total_gil += account_data["total_gil"]
        total_subs += account_data["total_subs"]
        total_retainers += account_data["total_retainers"]
        ready_subs += account_data["ready_subs"]
        ready_retainers += account_data["ready_retainers"]
        total_mb_items += account_data["total_mb_items"]
        total_treasure += account_data["total_treasure"]
        
        all_accounts.append(account_data)
    
    return {
        "accounts": all_accounts,
        "summary": {
            "total_gil": total_gil,
            "total_subs": total_subs,
            "total_retainers": total_retainers,
            "ready_subs": ready_subs,
            "ready_retainers": ready_retainers,
            "total_mb_items": total_mb_items,
            "max_mb_items": total_retainers * 20,
            "total_treasure": total_treasure,
            "total_with_treasure": total_gil + total_treasure,
            "daily_income": total_daily_income,
            "monthly_income": total_daily_income * 30,
            "annual_income": total_daily_income * 365,
            "daily_cost": total_daily_cost,
            "monthly_cost": total_daily_cost * 30,
            "daily_profit": total_daily_income - total_daily_cost,
            "monthly_profit": (total_daily_income - total_daily_cost) * 30,
        },
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# ===============================================
# HTML Template
# ===============================================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FFXIV AutoRetainer Dashboard</title>
    <style>
        :root {
            --bg-primary: #1a1a2e;
            --bg-secondary: #16213e;
            --bg-card: #0f3460;
            --bg-hover: #1a4a7a;
            --text-primary: #e8e8e8;
            --text-secondary: #a0a0a0;
            --accent: #e94560;
            --accent-light: #ff6b6b;
            --success: #00d26a;
            --warning: #ffc107;
            --border: #2a2a4a;
            --gold: #ffd700;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: var(--bg-card);
            padding: 20px 30px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border);
        }
        
        header h1 {
            color: var(--accent);
            font-size: 2em;
            margin-bottom: 5px;
        }
        
        header .subtitle {
            color: var(--text-secondary);
            font-size: 0.9em;
        }
        
        .summary-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 20px;
        }
        
        .summary-card {
            background: var(--bg-card);
            padding: 8px 15px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid var(--border);
            transition: transform 0.2s, box-shadow 0.2s;
            flex: 1 1 auto;
            min-width: 120px;
        }
        
        .summary-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }
        
        .summary-card .value {
            font-size: 1.1em;
            font-weight: bold;
            color: var(--gold);
        }
        
        .summary-card .value.profit {
            color: var(--success);
        }
        
        .summary-card .value.cost {
            color: var(--accent);
        }
        
        .summary-card .label {
            color: var(--text-secondary);
            font-size: 0.7em;
            margin-top: 2px;
        }
        
        .account-section {
            background: var(--bg-card);
            border-radius: 12px;
            margin-bottom: 25px;
            border: 1px solid var(--border);
            overflow: hidden;
        }
        
        .account-header {
            background: linear-gradient(90deg, #2a5a8a 0%, #3a7aaa 100%);
            padding: 15px 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            user-select: none;
            transition: opacity 0.2s;
        }
        
        .account-header:hover {
            opacity: 0.9;
        }
        
        .account-header h2 {
            font-size: 1.3em;
            color: white;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .account-header h2::before {
            content: '▼';
            font-size: 0.7em;
            transition: transform 0.3s;
        }
        
        .account-header.collapsed h2::before {
            transform: rotate(-90deg);
        }
        
        .account-content {
            overflow: hidden;
            transition: max-height 0.4s ease-out;
        }
        
        .account-content.collapsed {
            max-height: 0 !important;
        }
        
        .account-stats {
            display: flex;
            gap: 20px;
            color: white;
            font-size: 0.9em;
        }
        
        .account-stats span {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .character-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
            gap: 20px;
            padding: 20px;
        }
        
        .character-card {
            background: var(--bg-card);
            border-radius: 10px;
            border: 1px solid var(--border);
            overflow: hidden;
        }
        
        .character-card.expanded {
            background: var(--bg-secondary);
        }
        
        .character-header {
            background: var(--bg-hover);
            padding: 10px 15px;
            cursor: pointer;
            user-select: none;
        }
        
        .character-header:hover {
            background: #2a3a4a;
        }
        
        .character-header.has-available {
            background: rgba(233, 69, 96, 0.25);
        }
        
        .character-header.has-available:hover {
            background: rgba(233, 69, 96, 0.35);
        }
        
        .account-stats .stat-ready {
            color: #000000 !important;
        }
        
        .char-header-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85em;
            line-height: 1.4;
        }
        
        .char-header-row.name-row {
            font-size: 0.95em;
        }
        
        .character-name {
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .character-name::before {
            content: '▼';
            font-size: 0.7em;
            transition: transform 0.3s;
        }
        
        .character-header.collapsed .character-name::before {
            transform: rotate(-90deg);
        }
        
        .character-world {
            color: var(--text-secondary);
        }
        
        .character-gil {
            color: var(--gold);
            font-weight: bold;
        }
        
        .char-status {
            font-size: 0.8em;
        }
        
        .char-status.available {
            color: #e94560 !important;
        }
        
        .char-status.all-sent {
            color: var(--success) !important;
        }
        
        .character-body {
            padding: 15px 20px;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
        }
        
        .character-body.collapsed {
            max-height: 0 !important;
            padding: 0 20px;
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid var(--border);
        }
        
        .info-row:last-child {
            border-bottom: none;
        }
        
        .info-label {
            color: var(--text-secondary);
        }
        
        .info-value {
            font-weight: 500;
        }
        
        .info-value.success {
            color: var(--success);
        }
        
        .info-value.warning {
            color: var(--warning);
        }
        
        .section-title {
            font-size: 0.9em;
            color: var(--accent);
            margin: 15px 0 10px 0;
            padding-bottom: 5px;
            border-bottom: 1px solid var(--accent);
        }
        
        .sub-table, .ret-table {
            width: 100%;
            font-size: 0.85em;
        }
        
        .sub-table th, .ret-table th {
            text-align: left;
            color: var(--text-secondary);
            padding: 6px 8px;
            font-weight: normal;
        }
        
        .sub-table td, .ret-table td {
            padding: 6px 8px;
        }
        
        .sub-table tr:nth-child(even), .ret-table tr:nth-child(even) {
            background: rgba(255, 255, 255, 0.03);
        }
        
        .status-ready {
            color: var(--success);
            font-weight: bold;
        }
        
        .status-voyaging {
            color: var(--warning);
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            color: var(--text-secondary);
            font-size: 0.85em;
        }
        
        .error-message {
            background: rgba(233, 69, 96, 0.2);
            border: 1px solid var(--accent);
            padding: 15px;
            border-radius: 8px;
            margin: 20px;
            color: var(--accent-light);
        }
        
        .collapsible {
            cursor: pointer;
            user-select: none;
        }
        
        .collapsible::after {
            content: ' ▼';
            font-size: 0.7em;
        }
        
        .collapsible.collapsed::after {
            content: ' ▶';
        }
        
        .collapse-content {
            max-height: 500px;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
        }
        
        .collapse-content.collapsed {
            max-height: 0;
        }
        
        @media (max-width: 768px) {
            .character-grid {
                grid-template-columns: 1fr;
            }
            
            .summary-grid {
                justify-content: center;
            }
            
            .summary-card {
                min-width: 100px;
            }
            
            .account-header {
                flex-direction: column;
                gap: 10px;
            }
            
            .account-stats {
                flex-wrap: wrap;
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚓ FFXIV AutoRetainer Dashboard</h1>
            <div class="subtitle">Last Updated: <span id="last-updated">{{ data.last_updated }}</span> | Auto-refresh: {{ auto_refresh }}s</div>
        </header>
        
        <!-- Summary Cards -->
        <div class="summary-grid">
            <div class="summary-card">
                <div class="value" id="sum-total-gil">{{ "{:,}".format(data.summary.total_gil) }}</div>
                <div class="label">💰 Total Gil</div>
            </div>
            <div class="summary-card">
                <div class="value" id="sum-treasure">{{ "{:,}".format(data.summary.total_treasure) }}</div>
                <div class="label">💎 Treasure Value</div>
            </div>
            <div class="summary-card">
                <div class="value profit" id="sum-with-treasure">{{ "{:,}".format(data.summary.total_with_treasure) }}</div>
                <div class="label">🏆 Gil + Treasure</div>
            </div>
            <div class="summary-card">
                <div class="value"><span id="sum-ready-subs">{{ data.summary.ready_subs }}</span>/<span id="sum-total-subs">{{ data.summary.total_subs }}</span></div>
                <div class="label">🚢 Submarines</div>
            </div>
            <div class="summary-card">
                <div class="value"><span id="sum-ready-retainers">{{ data.summary.ready_retainers }}</span>/<span id="sum-total-retainers">{{ data.summary.total_retainers }}</span></div>
                <div class="label">👤 Retainers</div>
            </div>
            <div class="summary-card">
                <div class="value"><span id="sum-total-mb">{{ data.summary.total_mb_items }}</span>/<span id="sum-max-mb">{{ "{:,}".format(data.summary.max_mb_items) }}</span></div>
                <div class="label">📦 MB Items</div>
            </div>
            <div class="summary-card">
                <div class="value profit" id="sum-monthly-income">{{ "{:,}".format(data.summary.monthly_income|int) }}</div>
                <div class="label">📈 Monthly Income</div>
            </div>
            <div class="summary-card">
                <div class="value cost" id="sum-monthly-cost">{{ "{:,}".format(data.summary.monthly_cost|int) }}</div>
                <div class="label">📉 Monthly Cost</div>
            </div>
            <div class="summary-card">
                <div class="value profit" id="sum-monthly-profit">{{ "{:,}".format(data.summary.monthly_profit|int) }}</div>
                <div class="label">💎 Monthly Profit</div>
            </div>
            <div class="summary-card">
                <div class="value profit" id="sum-annual-income">{{ "{:,}".format(data.summary.annual_income|int) }}</div>
                <div class="label">🏆 Annual Income</div>
            </div>
        </div>
        
        <!-- Account Sections -->
        {% for account in data.accounts %}
        <div class="account-section" data-account="{{ account.nickname }}">
            <div class="account-header collapsed" onclick="toggleAccount(this)">
                <h2>{{ account.nickname }}</h2>
                <div class="account-stats">
                    <span>💰 <span class="acc-gil">{{ "{:,}".format(account.total_gil) }}</span> gil</span>
                    <span>💎 <span class="acc-treasure">{{ "{:,}".format(account.total_treasure) }}</span> treasure</span>
                    <span class="{% if account.ready_subs > 0 %}stat-ready{% endif %}">🚢 <span class="acc-ready-subs">{{ account.ready_subs }}</span>/<span class="acc-subs">{{ account.total_subs }}</span> subs</span>
                    <span class="{% if account.ready_retainers > 0 %}stat-ready{% endif %}">👤 <span class="acc-ready-retainers">{{ account.ready_retainers }}</span>/<span class="acc-retainers">{{ account.total_retainers }}</span> retainers</span>
                    <span>📦 <span class="acc-mb">{{ account.total_mb_items }}</span>/<span class="acc-max-mb">{{ "{:,}".format(account.max_mb_items) }}</span> MB</span>
                </div>
            </div>
            
            <div class="account-content collapsed">
            {% if account.error %}
            <div class="error-message">{{ account.error }}</div>
            {% else %}
            <div class="character-grid">
                {% for char in account.characters %}
                <div class="character-card" data-char="{{ char.cid }}">
                    <div class="character-header collapsed {% if char.ready_retainers > 0 or char.ready_subs > 0 %}has-available{% endif %}" onclick="toggleCharacter(this)">
                        <div class="char-header-row name-row">
                            <span class="character-name">{{ char.name }}</span>
                            <span class="char-status {% if char.ready_retainers > 0 %}available{% else %}all-sent{% endif %}">👤 {{ char.ready_retainers }}/{{ char.total_retainers }} retainers</span>
                        </div>
                        <div class="char-header-row">
                            <span class="character-world">{{ char.world }}{% if char.fc_name %} • {{ char.fc_name }}{% endif %}</span>
                            <span class="char-status {% if char.ready_subs > 0 %}available{% else %}all-sent{% endif %}">🚢 {{ char.ready_subs }}/{{ char.total_subs }} subs</span>
                        </div>
                        <div class="char-header-row">
                            <span></span>
                            <span class="character-gil">{{ "{:,}".format(char.total_gil) }} gil</span>
                        </div>
                    </div>
                    <div class="character-body collapsed">
                        <div class="info-row">
                            <span class="info-label">Character Gil</span>
                            <span class="info-value">{{ "{:,}".format(char.gil) }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Retainer Gil</span>
                            <span class="info-value">{{ "{:,}".format(char.retainer_gil) }}</span>
                        </div>
                        {% if char.treasure_value > 0 %}
                        <div class="info-row">
                            <span class="info-label">Treasure Value</span>
                            <span class="info-value" style="color: var(--gold);">{{ "{:,}".format(char.treasure_value) }}</span>
                        </div>
                        {% endif %}
                        <div class="info-row">
                            <span class="info-label">Ceruleum Tanks</span>
                            <span class="info-value">{{ "{:,}".format(char.ceruleum) }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Repair Kits</span>
                            <span class="info-value">{{ "{:,}".format(char.repair_kits) }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Daily Income</span>
                            <span class="info-value success">+{{ "{:,}".format(char.daily_income|int) }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Daily Cost</span>
                            <span class="info-value warning">-{{ "{:,}".format(char.daily_cost|int) }}</span>
                        </div>
                        
                        {% if char.submarines %}
                        <div class="section-title collapsible" onclick="toggleCollapse(this)">🚢 Submarines ({{ char.submarines|length }})</div>
                        <div class="collapse-content">
                            <table class="sub-table">
                                <tr>
                                    <th>Name</th>
                                    <th>Lvl</th>
                                    <th>Build</th>
                                    <th>Status</th>
                                </tr>
                                {% for sub in char.submarines %}
                                <tr>
                                    <td>{{ sub.name }}</td>
                                    <td>{{ sub.level }}</td>
                                    <td>{{ sub.build }}</td>
                                    <td class="{% if sub.return_formatted == 'Ready!' %}status-ready{% else %}status-voyaging{% endif %}">
                                        {{ sub.return_formatted }}
                                    </td>
                                </tr>
                                {% endfor %}
                            </table>
                        </div>
                        {% endif %}
                        
                        {% if char.retainers %}
                        <div class="section-title collapsible" onclick="toggleCollapse(this)">👤 Retainers ({{ char.retainers|length }})</div>
                        <div class="collapse-content">
                            <table class="ret-table">
                                <tr>
                                    <th>Name</th>
                                    <th>Lvl</th>
                                    <th>Gil</th>
                                    <th>MB</th>
                                    <th>Venture</th>
                                </tr>
                                {% for ret in char.retainers %}
                                <tr>
                                    <td>{{ ret.name }}</td>
                                    <td>{{ ret.level }}</td>
                                    <td>{{ "{:,}".format(ret.gil) }}</td>
                                    <td>{{ ret.mb_items }}</td>
                                    <td class="{% if ret.venture_formatted == 'Ready!' %}status-ready{% else %}status-voyaging{% endif %}">
                                        {{ ret.venture_formatted if ret.has_venture else "None" }}
                                    </td>
                                </tr>
                                {% endfor %}
                            </table>
                        </div>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endif %}
            </div>
        </div>
        {% endfor %}
        
        <div class="footer">
            FFXIV AutoRetainer Dashboard v1.02 | Data sourced from AutoRetainer DefaultConfig.json<br>
            <a href="https://github.com/xa-io/ffxiv-tools/tree/main/FFXIV-AutoRetainer-Dashboard" target="_blank" style="color: var(--accent); text-decoration: none;">github.com/xa-io/ffxiv-tools</a>
        </div>
    </div>
    
    <script>
        const REFRESH_INTERVAL = {{ auto_refresh }} * 1000;
        
        function formatNumber(num) {
            return num.toLocaleString('en-US');
        }
        
        function toggleCollapse(element) {
            element.classList.toggle('collapsed');
            const content = element.nextElementSibling;
            content.classList.toggle('collapsed');
        }
        
        function toggleAccount(header) {
            const accountSection = header.closest('.account-section');
            const accountName = accountSection.dataset.account;
            const isCollapsed = header.classList.toggle('collapsed');
            const content = header.nextElementSibling;
            content.classList.toggle('collapsed');
            
            // Save state to localStorage
            const collapsedAccounts = JSON.parse(localStorage.getItem('collapsedAccounts') || '{}');
            collapsedAccounts[accountName] = isCollapsed;
            localStorage.setItem('collapsedAccounts', JSON.stringify(collapsedAccounts));
        }
        
        function toggleCharacter(header) {
            const charCard = header.closest('.character-card');
            const charId = charCard.dataset.char;
            const isCollapsed = header.classList.toggle('collapsed');
            const body = header.nextElementSibling;
            body.classList.toggle('collapsed');
            charCard.classList.toggle('expanded', !isCollapsed);
            
            // Save state to localStorage
            const collapsedChars = JSON.parse(localStorage.getItem('collapsedChars') || '{}');
            collapsedChars[charId] = isCollapsed;
            localStorage.setItem('collapsedChars', JSON.stringify(collapsedChars));
        }
        
        function restoreCollapsedState() {
            const collapsedAccounts = JSON.parse(localStorage.getItem('collapsedAccounts') || '{}');
            document.querySelectorAll('.account-section').forEach(section => {
                const accountName = section.dataset.account;
                const header = section.querySelector('.account-header');
                const content = section.querySelector('.account-content');
                
                // Default to collapsed if not in localStorage
                const shouldBeCollapsed = collapsedAccounts[accountName] !== false;
                
                if (shouldBeCollapsed) {
                    header.classList.add('collapsed');
                    content.classList.add('collapsed');
                } else {
                    header.classList.remove('collapsed');
                    content.classList.remove('collapsed');
                }
            });
            
            // Restore character card collapsed states (default to collapsed)
            const collapsedChars = JSON.parse(localStorage.getItem('collapsedChars') || '{}');
            document.querySelectorAll('.character-card').forEach(card => {
                const charId = card.dataset.char;
                const header = card.querySelector('.character-header');
                const body = card.querySelector('.character-body');
                
                // Default to collapsed if not in localStorage
                const shouldBeCollapsed = collapsedChars[charId] !== false;
                
                if (shouldBeCollapsed) {
                    header.classList.add('collapsed');
                    body.classList.add('collapsed');
                    card.classList.remove('expanded');
                } else {
                    header.classList.remove('collapsed');
                    body.classList.remove('collapsed');
                    card.classList.add('expanded');
                }
            });
        }
        
        async function refreshData() {
            try {
                const response = await fetch('/api/data');
                const data = await response.json();
                
                // Update summary cards
                document.getElementById('last-updated').textContent = data.last_updated;
                document.getElementById('sum-total-gil').textContent = formatNumber(data.summary.total_gil);
                document.getElementById('sum-treasure').textContent = formatNumber(data.summary.total_treasure);
                document.getElementById('sum-with-treasure').textContent = formatNumber(data.summary.total_with_treasure);
                document.getElementById('sum-ready-subs').textContent = data.summary.ready_subs;
                document.getElementById('sum-total-subs').textContent = data.summary.total_subs;
                document.getElementById('sum-ready-retainers').textContent = data.summary.ready_retainers;
                document.getElementById('sum-total-retainers').textContent = data.summary.total_retainers;
                document.getElementById('sum-total-mb').textContent = data.summary.total_mb_items;
                document.getElementById('sum-max-mb').textContent = formatNumber(data.summary.max_mb_items);
                document.getElementById('sum-monthly-income').textContent = formatNumber(Math.floor(data.summary.monthly_income));
                document.getElementById('sum-monthly-cost').textContent = formatNumber(Math.floor(data.summary.monthly_cost));
                document.getElementById('sum-monthly-profit').textContent = formatNumber(Math.floor(data.summary.monthly_profit));
                document.getElementById('sum-annual-income').textContent = formatNumber(Math.floor(data.summary.annual_income));
                
                // Update account stats
                data.accounts.forEach(account => {
                    const section = document.querySelector(`[data-account="${account.nickname}"]`);
                    if (section) {
                        section.querySelector('.acc-gil').textContent = formatNumber(account.total_gil);
                        section.querySelector('.acc-treasure').textContent = formatNumber(account.total_treasure);
                        section.querySelector('.acc-ready-subs').textContent = account.ready_subs;
                        section.querySelector('.acc-subs').textContent = account.total_subs;
                        section.querySelector('.acc-ready-retainers').textContent = account.ready_retainers;
                        section.querySelector('.acc-retainers').textContent = account.total_retainers;
                        section.querySelector('.acc-mb').textContent = account.total_mb_items;
                        section.querySelector('.acc-max-mb').textContent = formatNumber(account.max_mb_items);
                    }
                });
                
                console.log('Data refreshed at', data.last_updated);
            } catch (error) {
                console.error('Failed to refresh data:', error);
            }
        }
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {
            restoreCollapsedState();
            
            // Start auto-refresh if enabled
            if (REFRESH_INTERVAL > 0) {
                setInterval(refreshData, REFRESH_INTERVAL);
            }
        });
    </script>
</body>
</html>
'''


# ===============================================
# Flask Routes
# ===============================================
@app.route('/')
def index():
    """Main dashboard page"""
    data = get_all_data()
    return render_template_string(HTML_TEMPLATE, data=data, auto_refresh=AUTO_REFRESH)


@app.route('/api/data')
def api_data():
    """API endpoint for raw JSON data"""
    data = get_all_data()
    return jsonify(data)


@app.route('/api/refresh')
def api_refresh():
    """Force data refresh"""
    data = get_all_data()
    return jsonify({"status": "ok", "last_updated": data["last_updated"]})


# ===============================================
# Main Entry Point
# ===============================================
if __name__ == "__main__":
    load_external_config()
    
    print("=" * 60)
    print("  FFXIV AutoRetainer Dashboard v1.00")
    print("=" * 60)
    print(f"  Server: http://{HOST}:{PORT}")
    print(f"  Accounts: {len(account_locations)}")
    print(f"  Auto-refresh: {AUTO_REFRESH}s" if AUTO_REFRESH > 0 else "  Auto-refresh: Disabled")
    print("=" * 60)
    print()
    
    app.run(host=HOST, port=PORT, debug=DEBUG)
