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
# Landing Page v1.03
# FFXIV AutoRetainer Dashboard
# Created by: https://github.com/xa-io
# Last Updated: 2026-01-26 08:35:00
#
# ## Release Notes ##
#
# v1.03 - Major feature update with Altoholic integration and enhanced submarine tracking
#         Added submarine plan detection (leveling vs farming) from AutoRetainer config
#         Added FC Points, Venture Coins, Coffers to character title bar
#         Added Coffer + Dyes estimated value button at top
#         Added character class/level display from Altoholic
#         Added Leveling/Farming stats at top for submarines and retainers
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
# Coffer and Dye Values (for estimation)
# ===============================================
COFFER_DYE_VALUES = {
    32161: 18000,   # Venture Coffer
    13114: 450000,  # General-purpose Pure White Dye
    13115: 600000,  # General-purpose Jet Black Dye
    13708: 40000,   # General-purpose Pastel Pink Dye
}
COFFER_DYE_IDS = set(COFFER_DYE_VALUES.keys())

# ===============================================
# Job Class Abbreviations (for character class display)
# ===============================================
JOB_ABBREVIATIONS = {
    "Adventurer": "ADV", "Paladin": "PLD", "Gladiator": "GLA", "Warrior": "WAR",
    "Marauder": "MRD", "DarkKnight": "DRK", "Gunbreaker": "GNB", "WhiteMage": "WHM",
    "Conjurer": "CNJ", "Scholar": "SCH", "Astrologian": "AST", "Sage": "SGE",
    "Monk": "MNK", "Pugilist": "PGL", "Dragoon": "DRG", "Lancer": "LNC",
    "Ninja": "NIN", "Rogue": "ROG", "Samurai": "SAM", "Reaper": "RPR",
    "Viper": "VPR", "Bard": "BRD", "Archer": "ARC", "Machinist": "MCH",
    "Dancer": "DNC", "Pictomancer": "PCT", "BlackMage": "BLM", "Thaumaturge": "THM",
    "Summoner": "SMN", "Arcanist": "ACN", "RedMage": "RDM", "BlueMage": "BLU",
    "Carpenter": "CRP", "Blacksmith": "BSM", "Armorer": "ARM", "Goldsmith": "GSM",
    "Leatherworker": "LTW", "Weaver": "WVR", "Alchemist": "ALC", "Culinarian": "CUL",
    "Miner": "MIN", "Botanist": "BTN", "Fisher": "FSH",
}

# ===============================================
# Submarine VesselBehavior Plan Types
# ===============================================
# VesselBehavior values from AutoRetainer:
# 0 = Finalize (docked/idle)
# 1 = Use Specified Path (farming route)
# 2 = Level Up (leveling mode)
# 3 = Unlock Sectors
# 4 = Use Point Plan
VESSEL_BEHAVIOR_FARMING = {1, 4}  # These indicate farming mode
VESSEL_BEHAVIOR_LEVELING = {2, 3}  # These indicate leveling mode

# ===============================================
# Plan Configuration (loaded from config.json)
# ===============================================
# These can be overridden in config.json
submarine_plans = {
    "leveling": [],
    "farming": {}  # name: average_earnings
}
# Retainer leveling/farming is purely level-based: < 100 = leveling, >= 100 = farming
item_values = {
    "venture_coffer": 18000,
    "pure_white_dye": 450000,
    "jet_black_dye": 600000,
    "pastel_pink_dye": 40000
}
# Plan GUID to Name lookup (built from DefaultConfig.json)
submarine_plan_names = {}  # GUID -> Name

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
    global submarine_plans, retainer_plans, item_values
    
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
        
        # Load plan configurations
        if "submarine_plans" in config:
            submarine_plans.update(config["submarine_plans"])
        if "item_values" in config:
            item_values.update(config["item_values"])
        
        print(f"[CONFIG] Loaded configuration from {config_path}")
    except Exception as e:
        print(f"[CONFIG] Error loading config: {e}")


def build_plan_name_lookup(data):
    """Build GUID to plan name lookup from AutoRetainer config"""
    global submarine_plan_names
    submarine_plan_names = {}
    
    # SubmarinePointPlans
    for plan in data.get("SubmarinePointPlans", []):
        guid = plan.get("GUID", "")
        name = plan.get("Name", "")
        if guid and name:
            submarine_plan_names[guid] = name
    
    # SubmarineUnlockPlans
    for plan in data.get("SubmarineUnlockPlans", []):
        guid = plan.get("GUID", "")
        name = plan.get("Name", "")
        if guid and name:
            submarine_plan_names[guid] = name


def get_submarine_plan_info(sub_data):
    """
    Determine submarine leveling/farming status and earnings based on plan name.
    Returns: (is_leveling, is_farming, plan_name, plan_earnings)
    """
    # Get the plan GUID being used
    selected_point_plan = sub_data.get("SelectedPointPlan", "")
    selected_unlock_plan = sub_data.get("SelectedUnlockPlan", "")
    vessel_behavior = sub_data.get("VesselBehavior", 0)
    
    # Determine which plan to look up based on VesselBehavior
    plan_guid = ""
    if vessel_behavior == 4:  # Use Point Plan
        plan_guid = selected_point_plan
    elif vessel_behavior == 3:  # Unlock Sectors
        plan_guid = selected_unlock_plan
    
    # Get plan name from GUID lookup
    plan_name = submarine_plan_names.get(plan_guid, "")
    
    # Check if plan name matches config leveling plans
    leveling_plans = submarine_plans.get("leveling", [])
    farming_plans = submarine_plans.get("farming", {})
    
    if plan_name and plan_name in leveling_plans:
        return True, False, plan_name, 0
    
    if plan_name and plan_name in farming_plans:
        plan_earnings = farming_plans.get(plan_name, 0)
        return False, True, plan_name, plan_earnings
    
    # Fallback to VesselBehavior detection
    if vessel_behavior in VESSEL_BEHAVIOR_FARMING:
        # Check if we can match the plan name to get earnings
        if plan_name and plan_name in farming_plans:
            return False, True, plan_name, farming_plans[plan_name]
        return False, True, plan_name if plan_name else "Unknown Plan", 0
    elif vessel_behavior in VESSEL_BEHAVIOR_LEVELING:
        return True, False, plan_name if plan_name else "Leveling", 0
    
    # Default fallback
    return True, False, "", 0


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
    Scan Altoholic DB and return comprehensive character data.
    Returns: { CharacterId: {
        "treasure_value": int,
        "coffer_dye_value": int,
        "coffer_count": int,
        "venture_coins": int,
        "current_job": str,
        "current_level": int,
    }}
    """
    result = {}
    if not os.path.isfile(db_path):
        return result
    
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        rows = cur.execute(
            "SELECT CharacterId, Inventory, Saddle, ArmoryInventory, Retainers, Jobs, Currencies FROM characters"
        ).fetchall()
        
        for char_id, inv_json, saddle_json, armory_json, retainers_json, jobs_json, currencies_json in rows:
            treasure_value = 0
            coffer_dye_value = 0
            coffer_count = 0
            dye_count = 0
            venture_coins = 0
            
            def consume(items):
                nonlocal treasure_value, coffer_dye_value, coffer_count, dye_count
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
                    
                    if iid in COFFER_DYE_IDS:
                        # Use configurable item_values if available, else fall back to defaults
                        if iid == 32161:  # Venture Coffer
                            coffer_dye_value += qty * item_values.get("venture_coffer", COFFER_DYE_VALUES[iid])
                            coffer_count += qty
                        elif iid == 13114:  # Pure White Dye
                            coffer_dye_value += qty * item_values.get("pure_white_dye", COFFER_DYE_VALUES[iid])
                            dye_count += qty
                        elif iid == 13115:  # Jet Black Dye
                            coffer_dye_value += qty * item_values.get("jet_black_dye", COFFER_DYE_VALUES[iid])
                            dye_count += qty
                        elif iid == 13708:  # Pastel Pink Dye
                            coffer_dye_value += qty * item_values.get("pastel_pink_dye", COFFER_DYE_VALUES[iid])
                            dye_count += qty
                        else:
                            coffer_dye_value += qty * COFFER_DYE_VALUES[iid]
            
            inv = _safe_json_load(inv_json)
            if isinstance(inv, list):
                consume(inv)
            sad = _safe_json_load(saddle_json)
            if isinstance(sad, list):
                consume(sad)
            
            # Process ArmoryInventory (nested dict with slot arrays like MainHand, OffHand, etc.)
            armory = _safe_json_load(armory_json)
            if isinstance(armory, dict):
                for slot_name, slot_items in armory.items():
                    if isinstance(slot_items, list):
                        consume(slot_items)
            
            # Process Retainers inventories
            retainers = _safe_json_load(retainers_json)
            if isinstance(retainers, list):
                for retainer in retainers:
                    if isinstance(retainer, dict):
                        ret_inv = retainer.get("Inventory", [])
                        if isinstance(ret_inv, list):
                            consume(ret_inv)
            
            # Parse Jobs to find current/highest level job
            current_job = ""
            current_level = 0
            jobs = _safe_json_load(jobs_json)
            if isinstance(jobs, dict):
                for job_name, job_data in jobs.items():
                    if isinstance(job_data, dict):
                        level = job_data.get("Level", 0)
                        if level > current_level:
                            current_level = level
                            current_job = JOB_ABBREVIATIONS.get(job_name, job_name[:3].upper())
            
            # Parse Currencies to get Venture coins
            currencies = _safe_json_load(currencies_json)
            if isinstance(currencies, dict):
                venture_coins = currencies.get("Venture", 0)
                if not isinstance(venture_coins, int):
                    try:
                        venture_coins = int(venture_coins)
                    except Exception:
                        venture_coins = 0
            
            result[int(char_id)] = {
                "treasure_value": int(treasure_value),
                "coffer_dye_value": int(coffer_dye_value),
                "coffer_count": int(coffer_count),
                "dye_count": int(dye_count),
                "venture_coins": int(venture_coins),
                "current_job": current_job,
                "current_level": current_level,
            }
        
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
        vessel_behavior = sub_data.get("VesselBehavior", 0)
        
        # Get plan info from config-based detection
        is_leveling, is_farming, plan_name, plan_earnings = get_submarine_plan_info(sub_data)
        
        # If no plan match and no VesselBehavior detection, use level/build fallbacks
        if not plan_name and vessel_behavior == 0:
            if level >= 100:
                is_leveling = False
                is_farming = True
            elif build and build in BUILD_GIL_RATES:
                is_leveling = False
                is_farming = True
            else:
                is_leveling = True
                is_farming = False
        
        # Get return time from offline data
        return_time = None
        if name in offline_by_name:
            return_time = offline_by_name[name].get("ReturnTime", 0)
        
        # Determine if submarine is ready (docked or returned)
        now_ts = datetime.datetime.now().timestamp()
        is_ready = (not return_time) or (return_time <= now_ts)
        
        # Calculate gil rate - use plan earnings if available, otherwise use build rates
        if plan_earnings > 0:
            gil_rate = plan_earnings
        else:
            gil_rate = BUILD_GIL_RATES.get(build, 0)
        
        consumption = BUILD_CONSUMPTION_RATES.get(build, DEFAULT_CONSUMPTION)
        
        submarines.append({
            "name": name,
            "level": level,
            "build": build if build else "Leveling",
            "plan_name": plan_name,
            "return_time": return_time,
            "return_formatted": format_time_remaining(return_time) if return_time else "Docked",
            "is_ready": is_ready,
            "is_leveling": is_leveling,
            "is_farming": is_farming,
            "vessel_behavior": vessel_behavior,
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
    total_coffer_dye_value = 0
    total_coffer_count = 0
    total_dye_count = 0
    total_venture_coins = 0
    total_fc_points = 0
    total_subs_leveling = 0
    total_subs_farming = 0
    total_retainers_leveling = 0
    total_retainers_farming = 0
    min_restock_days = None  # Track lowest restock days across all accounts (excluding 0)
    
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
            "total_coffer_dye_value": 0,
            "total_coffer_count": 0,
            "total_dye_count": 0,
            "total_venture_coins": 0,
            "total_fc_points": 0,
            "subs_leveling": 0,
            "subs_farming": 0,
            "retainers_leveling": 0,
            "retainers_farming": 0,
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
        
        # Build plan name lookup from this config
        build_plan_name_lookup(data)
        
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
            
            # Calculate days until restocking needed
            total_tanks_per_day = sum(s.get("tanks_per_day", 0) for s in submarines)
            total_kits_per_day = sum(s.get("kits_per_day", 0) for s in submarines)
            ceruleum = char.get("Ceruleum", 0)
            repair_kits = char.get("RepairKits", 0)
            
            days_until_restock = None
            if submarines and total_tanks_per_day > 0 and total_kits_per_day > 0:
                days_from_tanks = ceruleum / total_tanks_per_day if ceruleum > 0 else 0
                days_from_kits = repair_kits / total_kits_per_day if repair_kits > 0 else 0
                days_until_restock = int(min(days_from_tanks, days_from_kits))
            
            # Count leveling vs farming submarines
            char_subs_leveling = sum(1 for s in submarines if s.get("is_leveling", False))
            char_subs_farming = sum(1 for s in submarines if s.get("is_farming", False))
            
            # Parse retainers
            retainers = parse_retainer_data(char)
            retainer_gil = sum(r["gil"] for r in retainers)
            mb_items = sum(r["mb_items"] for r in retainers)
            
            # Count leveling vs farming retainers (< 100 = leveling, 100 = farming)
            char_retainers_leveling = sum(1 for r in retainers if r["level"] < 100)
            char_retainers_farming = sum(1 for r in retainers if r["level"] >= 100)
            
            # Get FC info and FC points
            fc_name = ""
            fc_points = 0
            if cid in fc_data:
                fc_name = fc_data[cid].get("Name", "")
                fc_points = fc_data[cid].get("FCPoints", 0)
            
            # Get Altoholic data (treasure, coffers, dyes, job, etc.)
            treasure_value = 0
            coffer_dye_value = 0
            coffer_count = 0
            dye_count = 0
            venture_coins = 0
            current_job = ""
            current_level = 0
            if cid in alto_map:
                treasure_value = alto_map[cid].get("treasure_value", 0)
                coffer_dye_value = alto_map[cid].get("coffer_dye_value", 0)
                coffer_count = alto_map[cid].get("coffer_count", 0)
                dye_count = alto_map[cid].get("dye_count", 0)
                venture_coins = alto_map[cid].get("venture_coins", 0)
                current_job = alto_map[cid].get("current_job", "")
                current_level = alto_map[cid].get("current_level", 0)
            
            # Get venture coffers from AutoRetainer if Altoholic doesn't have it
            venture_coffers_ar = char.get("VentureCoffers", 0)
            if coffer_count == 0 and venture_coffers_ar > 0:
                coffer_count = venture_coffers_ar
                coffer_dye_value += venture_coffers_ar * COFFER_DYE_VALUES.get(32161, 18000)
            
            char_data = {
                "cid": cid,
                "name": char.get("Name", "Unknown"),
                "world": char.get("World", "Unknown"),
                "gil": char_gil,
                "retainer_gil": retainer_gil,
                "total_gil": char_gil + retainer_gil,
                "treasure_value": treasure_value,
                "coffer_dye_value": coffer_dye_value,
                "coffer_count": coffer_count,
                "dye_count": dye_count,
                "venture_coins": venture_coins,
                "total_with_treasure": char_gil + retainer_gil + treasure_value,
                "submarines": submarines,
                "retainers": retainers,
                "fc_name": fc_name,
                "fc_points": fc_points,
                "ceruleum": char.get("Ceruleum", 0),
                "repair_kits": char.get("RepairKits", 0),
                "ventures": char.get("Ventures", 0),
                "inventory_space": char.get("InventorySpace", 0),
                "gc_seals": char.get("GCSeals", 0),
                "daily_income": sub_daily_income,
                "monthly_income": sub_daily_income * 30,
                "daily_cost": sub_daily_cost,
                "mb_items": mb_items,
                "current_job": current_job,
                "current_level": current_level,
                "subs_leveling": char_subs_leveling,
                "subs_farming": char_subs_farming,
                "retainers_leveling": char_retainers_leveling,
                "retainers_farming": char_retainers_farming,
                "days_until_restock": days_until_restock,
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
            account_data["total_coffer_dye_value"] += coffer_dye_value
            account_data["total_coffer_count"] += coffer_count
            account_data["total_dye_count"] += dye_count
            account_data["total_venture_coins"] += venture_coins
            account_data["total_fc_points"] += fc_points
            
            # Track minimum restock days (excluding 0 and None)
            if days_until_restock is not None and days_until_restock > 0:
                if min_restock_days is None or days_until_restock < min_restock_days:
                    min_restock_days = days_until_restock
            
            account_data["subs_leveling"] += char_subs_leveling
            account_data["subs_farming"] += char_subs_farming
            account_data["retainers_leveling"] += char_retainers_leveling
            account_data["retainers_farming"] += char_retainers_farming
            
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
        total_coffer_dye_value += account_data["total_coffer_dye_value"]
        total_coffer_count += account_data["total_coffer_count"]
        total_dye_count += account_data["total_dye_count"]
        total_venture_coins += account_data["total_venture_coins"]
        total_fc_points += account_data["total_fc_points"]
        total_subs_leveling += account_data["subs_leveling"]
        total_subs_farming += account_data["subs_farming"]
        total_retainers_leveling += account_data["retainers_leveling"]
        total_retainers_farming += account_data["retainers_farming"]
        
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
            "total_coffer_dye_value": total_coffer_dye_value,
            "total_coffer_count": total_coffer_count,
            "total_dye_count": total_dye_count,
            "total_venture_coins": total_venture_coins,
            "total_fc_points": total_fc_points,
            "subs_leveling": total_subs_leveling,
            "subs_farming": total_subs_farming,
            "retainers_leveling": total_retainers_leveling,
            "retainers_farming": total_retainers_farming,
            "daily_income": total_daily_income,
            "monthly_income": total_daily_income * 30,
            "annual_income": total_daily_income * 365,
            "daily_cost": total_daily_cost,
            "monthly_cost": total_daily_cost * 30,
            "daily_profit": total_daily_income - total_daily_cost,
            "monthly_profit": (total_daily_income - total_daily_cost) * 30,
            "min_restock_days": min_restock_days,
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
            gap: 6px;
            margin-bottom: 20px;
        }
        
        .summary-card {
            background: var(--bg-card);
            padding: 6px 10px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid var(--border);
            transition: transform 0.2s, box-shadow 0.2s;
            flex: 1 1 auto;
            min-width: 90px;
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
        
        .summary-card .sublabel {
            color: var(--text-secondary);
            font-size: 0.6em;
            margin-top: 1px;
            opacity: 0.8;
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
        
        .sort-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            padding: 10px;
            margin-bottom: 10px;
            background: var(--bg-secondary);
            border-radius: 8px;
            align-items: center;
        }
        
        .sort-label {
            color: var(--text-secondary);
            font-size: 0.85em;
            margin-right: 5px;
        }
        
        .sort-btn {
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.75em;
            transition: all 0.2s;
        }
        
        .sort-btn:hover {
            background: var(--border);
            color: var(--text-primary);
        }
        
        .sort-btn.active {
            background: var(--accent);
            color: white;
            border-color: var(--accent);
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
                <div class="sublabel">🪙 {{ "{:,}".format(data.summary.total_fc_points) }} FC</div>
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
                <div class="value" id="sum-coffer-dye">{{ "{:,}".format(data.summary.total_coffer_dye_value) }}</div>
                <div class="label">📦 Coffer + Dyes</div>
                <div class="sublabel">📦 {{ data.summary.total_coffer_count }} | 🎨 {{ data.summary.total_dye_count }}</div>
            </div>
            <div class="summary-card">
                <div class="value">
                    <span id="sum-ready-subs">{{ data.summary.ready_subs }}</span>/<span id="sum-total-subs">{{ data.summary.total_subs }}</span>
                    <div style="font-size: 0.7em; color: var(--text-secondary);">
                        <span style="color: var(--warning);">Lvl: {{ data.summary.subs_leveling }}</span> |
                        <span style="color: var(--success);">Farm: {{ data.summary.subs_farming }}</span>
                    </div>
                </div>
                <div class="label">🚢 Submarines</div>
            </div>
            <div class="summary-card">
                <div class="value">
                    <span id="sum-ready-retainers">{{ data.summary.ready_retainers }}</span>/<span id="sum-total-retainers">{{ data.summary.total_retainers }}</span>
                    <div style="font-size: 0.7em; color: var(--text-secondary);">
                        <span style="color: var(--warning);">Lvl: {{ data.summary.retainers_leveling }}</span> |
                        <span style="color: var(--success);">Farm: {{ data.summary.retainers_farming }}</span>
                    </div>
                </div>
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
                <div class="sublabel" style="{% if data.summary.min_restock_days is not none and data.summary.min_restock_days < 7 %}color: var(--danger);{% elif data.summary.min_restock_days is not none and data.summary.min_restock_days < 14 %}color: var(--warning);{% endif %}">🔄 {% if data.summary.min_restock_days is not none %}{{ data.summary.min_restock_days }}d lowest{% else %}N/A{% endif %}</div>
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
            <div class="sort-bar">
                <span class="sort-label">Sort by:</span>
                <button class="sort-btn" data-sort="level" data-order="desc" onclick="sortCharacters(this)">Level ▼</button>
                <button class="sort-btn" data-sort="gil" data-order="desc" onclick="sortCharacters(this)">Gil ▼</button>
                <button class="sort-btn" data-sort="treasure" data-order="desc" onclick="sortCharacters(this)">Treasure ▼</button>
                <button class="sort-btn" data-sort="fc_points" data-order="desc" onclick="sortCharacters(this)">FC Pts ▼</button>
                <button class="sort-btn" data-sort="venture_coins" data-order="desc" onclick="sortCharacters(this)">Ventures ▼</button>
                <button class="sort-btn" data-sort="coffers" data-order="desc" onclick="sortCharacters(this)">Coffers ▼</button>
                <button class="sort-btn" data-sort="dyes" data-order="desc" onclick="sortCharacters(this)">Dyes ▼</button>
                <button class="sort-btn" data-sort="tanks" data-order="desc" onclick="sortCharacters(this)">Tanks ▼</button>
                <button class="sort-btn" data-sort="kits" data-order="desc" onclick="sortCharacters(this)">Kits ▼</button>
                <button class="sort-btn" data-sort="restock" data-order="asc" onclick="sortCharacters(this)">Restock ▲</button>
                <button class="sort-btn" data-sort="retainers" data-order="desc" onclick="sortCharacters(this)">Retainers ▼</button>
                <button class="sort-btn" data-sort="subs" data-order="desc" onclick="sortCharacters(this)">Subs ▼</button>
            </div>
            <div class="character-grid">
                {% for char in account.characters %}
                <div class="character-card" data-char="{{ char.cid }}" data-level="{{ char.current_level }}" data-gil="{{ char.total_gil }}" data-treasure="{{ char.treasure_value }}" data-fc-points="{{ char.fc_points }}" data-venture-coins="{{ char.venture_coins }}" data-coffers="{{ char.coffer_count }}" data-dyes="{{ char.dye_count }}" data-tanks="{{ char.ceruleum }}" data-kits="{{ char.repair_kits }}" data-restock="{{ char.days_until_restock if char.days_until_restock is not none else 9999 }}" data-retainers="{{ char.ready_retainers }}" data-subs="{{ char.ready_subs }}">
                    <div class="character-header collapsed {% if char.ready_retainers > 0 or char.ready_subs > 0 %}has-available{% endif %}" onclick="toggleCharacter(this)">
                        <div class="char-header-row name-row">
                            <span class="character-name">{{ char.name }}{% if char.current_level > 0 %} <span style="font-size: 0.8em; color: var(--text-secondary);">(Lv {{ char.current_level }}, {{ char.current_job }})</span>{% endif %}</span>
                            <span class="char-status {% if char.ready_retainers > 0 %}available{% else %}all-sent{% endif %}">👤 {{ char.ready_retainers }}/{{ char.total_retainers }}</span>
                        </div>
                        <div class="char-header-row">
                            <span class="character-world">{{ char.world }}{% if char.fc_name %} • {{ char.fc_name }}{% endif %}</span>
                            <span class="char-status {% if char.ready_subs > 0 %}available{% else %}all-sent{% endif %}">🚢 {{ char.ready_subs }}/{{ char.total_subs }}</span>
                        </div>
                        <div class="char-header-row">
                            <span style="font-size: 0.8em; color: var(--text-secondary);">🪙 {{ "{:,}".format(char.fc_points) }} | 🛒 {{ char.venture_coins }} | 📦 {{ char.coffer_count }} | 🎨 {{ char.dye_count }}</span>
                            <span class="character-gil">{{ "{:,}".format(char.total_gil) }} gil</span>
                        </div>
                        {% if char.total_subs > 0 %}
                        <div class="char-header-row">
                            <span style="font-size: 0.8em; color: var(--text-secondary);">⛽ {{ "{:,}".format(char.ceruleum) }} | 🔧 {{ "{:,}".format(char.repair_kits) }} | <span style="{% if char.days_until_restock is not none and char.days_until_restock < 7 %}color: var(--danger);{% elif char.days_until_restock is not none and char.days_until_restock < 14 %}color: var(--warning);{% endif %}">🔄 {% if char.days_until_restock is not none %}{{ char.days_until_restock }}d{% else %}N/A{% endif %}</span></span>
                            <span style="font-size: 0.8em; color: var(--gold);">💎 {{ "{:,}".format(char.treasure_value) }}</span>
                        </div>
                        {% endif %}
                    </div>
                    <div class="character-body collapsed">
                        {% if char.current_level > 0 %}
                        <div class="info-row">
                            <span class="info-label">Current Class</span>
                            <span class="info-value">{{ char.current_job }} Lv {{ char.current_level }}</span>
                        </div>
                        {% endif %}
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
                        {% if char.coffer_dye_value > 0 %}
                        <div class="info-row">
                            <span class="info-label">Coffer + Dye Value</span>
                            <span class="info-value" style="color: var(--accent-light);">{{ "{:,}".format(char.coffer_dye_value) }}</span>
                        </div>
                        {% endif %}
                        <div class="info-row">
                            <span class="info-label">FC Points 🪙</span>
                            <span class="info-value">{{ "{:,}".format(char.fc_points) }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Venture Coins 🛒</span>
                            <span class="info-value">{{ char.venture_coins }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Coffers 📦</span>
                            <span class="info-value">{{ char.coffer_count }}</span>
                        </div>
                        {% if char.total_subs > 0 %}
                        <div class="info-row">
                            <span class="info-label">Ceruleum Tanks ⛽</span>
                            <span class="info-value">{{ "{:,}".format(char.ceruleum) }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Repair Kits 🔧</span>
                            <span class="info-value">{{ "{:,}".format(char.repair_kits) }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Days Until Restock 🔄</span>
                            <span class="info-value" style="{% if char.days_until_restock is not none and char.days_until_restock < 7 %}color: var(--danger);{% elif char.days_until_restock is not none and char.days_until_restock < 14 %}color: var(--warning);{% else %}color: var(--success);{% endif %}">{% if char.days_until_restock is not none %}{{ char.days_until_restock }} days{% else %}N/A{% endif %}</span>
                        </div>
                        {% endif %}
                        <div class="info-row">
                            <span class="info-label">Daily Income</span>
                            <span class="info-value success">+{{ "{:,}".format(char.daily_income|int) }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Daily Cost</span>
                            <span class="info-value warning">-{{ "{:,}".format(char.daily_cost|int) }}</span>
                        </div>
                        
                        {% if char.submarines %}
                        <div class="section-title collapsible" onclick="toggleCollapse(this)">🚢 Submarines ({{ char.submarines|length }}) - <span style="color: var(--warning);">Lvl: {{ char.subs_leveling }}</span> | <span style="color: var(--success);">Farm: {{ char.subs_farming }}</span></div>
                        <div class="collapse-content">
                            <table class="sub-table">
                                <tr>
                                    <th>Name</th>
                                    <th>Lvl</th>
                                    <th>Build</th>
                                    <th>Plan</th>
                                    <th>Status</th>
                                </tr>
                                {% for sub in char.submarines %}
                                <tr>
                                    <td>{{ sub.name }}</td>
                                    <td>{{ sub.level }}</td>
                                    <td>{{ sub.build }}</td>
                                    <td style="{% if sub.is_farming %}color: var(--success);{% else %}color: var(--warning);{% endif %}">
                                        {% if sub.plan_name %}{{ sub.plan_name }}{% elif sub.is_farming %}Farm{% else %}Lvl{% endif %}
                                    </td>
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
            FFXIV AutoRetainer Dashboard v1.03 | Data sourced from AutoRetainer DefaultConfig.json & Altoholic<br>
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
        
        function sortCharacters(btn) {
            const sortBar = btn.closest('.sort-bar');
            const accountContent = btn.closest('.account-content');
            const grid = accountContent.querySelector('.character-grid');
            const cards = Array.from(grid.querySelectorAll('.character-card'));
            
            const sortKey = btn.dataset.sort;
            let order = btn.dataset.order;
            
            // Toggle order if clicking same button
            if (btn.classList.contains('active')) {
                order = order === 'asc' ? 'desc' : 'asc';
                btn.dataset.order = order;
            }
            
            // Update button text with arrow
            const btnText = btn.textContent.replace(/ [▲▼]$/, '');
            btn.textContent = btnText + (order === 'asc' ? ' ▲' : ' ▼');
            
            // Remove active from other buttons, add to this one
            sortBar.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Map sort keys to data attributes
            const attrMap = {
                'level': 'level',
                'gil': 'gil',
                'treasure': 'treasure',
                'fc_points': 'fc-points',
                'venture_coins': 'venture-coins',
                'coffers': 'coffers',
                'dyes': 'dyes',
                'tanks': 'tanks',
                'kits': 'kits',
                'restock': 'restock',
                'retainers': 'retainers',
                'subs': 'subs'
            };
            
            const attr = attrMap[sortKey];
            
            // Sort cards
            cards.sort((a, b) => {
                const aVal = parseFloat(a.dataset[attr.replace(/-([a-z])/g, (g) => g[1].toUpperCase())]) || 0;
                const bVal = parseFloat(b.dataset[attr.replace(/-([a-z])/g, (g) => g[1].toUpperCase())]) || 0;
                
                if (order === 'asc') {
                    return aVal - bVal;
                } else {
                    return bVal - aVal;
                }
            });
            
            // Re-append in sorted order
            cards.forEach(card => grid.appendChild(card));
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
