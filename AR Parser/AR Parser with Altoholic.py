############################################################################################################################
#
#   █████╗ ██████╗     ██████╗  █████╗ ██████╗ ███████╗███████╗██████╗ 
#  ██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
#  ███████║██████╔╝    ██████╔╝███████║██████╔╝███████╗█████╗  ██████╔╝
#  ██╔══██║██╔══██╗    ██╔═══╝ ██╔══██║██╔══██╗╚════██║██╔══╝  ██╔══██╗
#  ██║  ██║██║  ██║    ██║     ██║  ██║██║  ██║███████║███████╗██║  ██║
#  ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
#
# Comprehensive FFXIV character data parser that aggregates information from AutoRetainer, Altoholic, and Lifestream
# plugins to generate detailed Excel reports with gil summaries, submarine tracking, FC data, and housing information.
#
# Core Features:
# • Multi-account AutoRetainer data parsing with character summaries
# • Submarine build tracking with gil earnings calculations (daily/monthly/annual)
# • Inventory tracking from DefaultConfig.json (tanks, kits, ventures, inventory spaces)
# • Altoholic database integration for treasure item tracking
# • Lifestream housing data integration for FC and private housing locations
# • Excel output with character details, retainer info, submarine data, and summary statistics
# • Automatic FC detection via FC name or housing data from Lifestream plugin
# • Restocking days calculation based on submarine build consumption rates
#
# AR Parser with Altoholic v1.14
# Created by: https://github.com/xa-io
# Last Updated: 2025-12-25 10:00:00
#
# ## Release Notes ##
#
# v1.14 - Added Last Online column from Altoholic database, shows days since character last logged in
# v1.13 - Added Inverse Supplier Formatting column with smart inventory-based distribution
#         New "Inverse Supplier Formatting" column generates format for XA Inverse Supplier v2.11 smart distribution
#         Format: {"Toon@World", fuel_needed, kits_needed}, where amounts show (threshold - current_inventory)
#         Added fuel_threshold and repair_mats_threshold parameters to acc() function (default 0)
#         When threshold > 0, calculates needed amount; when 0, outputs 0 (excludes from smart distribution)
#         Column width set to 45 spaces (10 less than Bagman Formatting)
# v1.12 - Added Restocking Days calculation and data source improvements
#         Added "Restocking Days" column showing days until restocking required based on submarine build consumption rates
#         Changed Tanks/Kits data source from Altoholic to DefaultConfig.json for consistency with Auto-AutoRetainer
#         Added default consumption rates (9 tanks/day, 1.33 kits/day) for unlisted builds (leveling submarines)
#         Restocking calculation: min(tanks/consumption, kits/consumption) rounded down, displays 0 for submarines with no inventory
#         Altoholic now only tracks treasure items, removed tank/kit scanning from scan_altoholic_db()
# v1.11 - Added Inventory Spaces, Ventures, and VentureCoffers columns sourced from AutoRetainer DefaultConfig.json
#         New column order around treasure data: Tanks → Kits → Inventory Spaces → Ventures → VentureCoffers → Treasure Value
# v1.10 - Improved submarine handling and FC statistics
#         Submarines now support custom names, map by OfflineSubmarineData index, and correctly resolve parts/levels/return times
#         FC counts use FC name or housing data, treat each submarine-owning character as one FC workshop,
#         correctly detect farming submarines, and include all submarine builds in the Total Submarines summary row
# v1.09 - Integrated Lifestream housing data into character summaries
# v1.08 - Formatting improvements for snd_nameworld string
# v1.07 - Per-account submarine control with include_submarines parameter
# v1.06 - Column layout updates
# v1.05 - Altoholic integration for inventory tracking
# v1.00 - Initial release with AutoRetainer data parsing
#
############################################################################################################################

import json
import xlsxwriter
import argparse
import os
import datetime
import sys
from pathlib import Path
import getpass
import sqlite3

# ===============================================
# Account locations + global data
# ===============================================
user = getpass.getuser()

def acc(nickname, pluginconfigs_path, include_altoholic=True, include_submarines=True, fuel_threshold=None, repair_mats_threshold=None):
    auto_path = os.path.join(pluginconfigs_path, "AutoRetainer", "DefaultConfig.json")
    alto_path = os.path.join(pluginconfigs_path, "Altoholic", "altoholic.db")
    lfstrm_path = os.path.join(pluginconfigs_path, "Lifestream", "DefaultConfig.json")
    
    # Use global inventory_needs if not explicitly specified per-account
    if fuel_threshold is None:
        fuel_threshold = inventory_needs.get("fuel_threshold", 0)
    if repair_mats_threshold is None:
        repair_mats_threshold = inventory_needs.get("repair_mats_threshold", 0)
    
    return {
        "nickname": nickname,
        "auto_path": auto_path,
        "alto_path": alto_path,
        "lfstrm_path": lfstrm_path,
        "include_altoholic": bool(include_altoholic),
        "include_submarines": bool(include_submarines),
        "fuel_threshold": int(fuel_threshold),
        "repair_mats_threshold": int(repair_mats_threshold),
    }

# You do not need to replace "{user}" with your username, the script will get that information.

# ===============================================
# Global Inventory Thresholds for Inverse Supplier
# Applied to all accounts unless overridden per-account
# ===============================================
inventory_needs = {
    "fuel_threshold": 3000,
    "repair_mats_threshold": 500
}

# Optional: Set fuel_threshold and repair_mats_threshold for Inverse Supplier smart distribution
# To override global settings per-account, add parameters to acc():
# Example: acc("Main", path, include_submarines=True, fuel_threshold=1000, repair_mats_threshold=1000)
account_locations = [
    acc("Main",       f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs", include_submarines=True),
    # acc("Acc1",    f"C:\\Users\\{user}\\AltData\\Acc1\\pluginConfigs", include_submarines=True),
    # acc("Acc2",    f"C:\\Users\\{user}\\AltData\\Acc2\\pluginConfigs", include_submarines=True),
]

all_fc_data = {}
all_characters = []

# ===============================================
# CONFIG: Altoholic integration (for treasure items only)
# Tanks and Kits are now read from DefaultConfig.json for consistency with Auto-AutoRetainer
# ===============================================
INCLUDE_ALTOHOLIC_BY_DEFAULT = True

# Treasure values (gil) per item id
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

# ===============================================
# Submarine Build Consumption Rates
# Based on Routes.xlsx - Tanks (Ceruleum) and Repair Kits per day for each route
# ===============================================
build_consumption_rates = {
    # OJ Route (24h) - Unmod: 9/1.33, Mod: 9/3.43
    "WSUC": {"tanks_per_day": 9.0, "kits_per_day": 1.33},
    "SSUC": {"tanks_per_day": 9.0, "kits_per_day": 1.33},
    "W+S+U+C+": {"tanks_per_day": 9.0, "kits_per_day": 3.43},  # WSUC++ (modified)
    "S+S+S+C+": {"tanks_per_day": 9.0, "kits_per_day": 3.43},  # SSSC++ (modified for OJ route)
    
    # MOJ Route (36h) - Unmod: 7.5/1.40, Mod: 10/3.07
    "YUUW": {"tanks_per_day": 7.5, "kits_per_day": 1.40},
    "Y+U+U+W+": {"tanks_per_day": 10.0, "kits_per_day": 3.07},  # YU+U+W+ (modified)
    
    # ROJ Route (36h) - Unmod: 10/1.67, Mod: 10/3.20
    "WCSU": {"tanks_per_day": 10.0, "kits_per_day": 1.67},
    "WUSS": {"tanks_per_day": 10.0, "kits_per_day": 1.67},
    "W+U+S+S+": {"tanks_per_day": 10.0, "kits_per_day": 3.20},  # WUSS++ (modified)
    
    # JOZ Route (36h) - Unmod: 10/2.50, Mod: 10/3.20
    "YSYC": {"tanks_per_day": 10.0, "kits_per_day": 2.50},
    "Y+S+Y+C+": {"tanks_per_day": 10.0, "kits_per_day": 3.20},  # YS+YC+ (modified)
    
    # MROJ Route (36h) - Unmod: 14/1.78, Mod: 14/4.00
    # SSUC appears on MROJ at rank 99 (unmodified)
    # SSSC++/SSUC++ are modified builds for MROJ
    
    # JORZ Route (36h) - Unmod: 14/1.78, Mod: 14/3.67
    "S+S+U+C": {"tanks_per_day": 14.0, "kits_per_day": 3.67},  # SSUC modified for JORZ
    
    # JORZ 48h Route - Unmod: 10.5/2.00, Mod: 10.5/3.00
    "WCYC": {"tanks_per_day": 10.5, "kits_per_day": 2.00},
    "WUWC": {"tanks_per_day": 10.5, "kits_per_day": 2.00},
    "W+U+W+C+": {"tanks_per_day": 10.5, "kits_per_day": 3.00},  # WUWC++ (modified)
    
    # MOJZ Route (36h) - Unmod: 14/1.78, Mod: 14/4.00
    "S+S+U+C+": {"tanks_per_day": 14.0, "kits_per_day": 4.0},  # SSUC++ (modified for MOJZ/MROJ)
    
    # MROJZ Route (48h) - Unmod: 9/1.67, Mod: 13.5/4.00
    "YSCU": {"tanks_per_day": 9.0, "kits_per_day": 1.67},
    "SCUS": {"tanks_per_day": 9.0, "kits_per_day": 1.67},
    "S+C+U+S+": {"tanks_per_day": 13.5, "kits_per_day": 4.0},  # SCUS++ (modified)
}

# ===============================================
# Region mapping by world
# ===============================================
NA_WORLDS = {
    "adamantoise","cactuar","faerie","gilgamesh","jenova","midgardsormr","sargatanas","siren",
    "balmung","brynhildr","coeurl","diabolos","goblin","malboro","mateus","zalera",
    "behemoth","excalibur","exodus","famfrit","hyperion","lamia","leviathan","ultros",
    "cuchulainn","golem","halicarnassus","kraken","maduin","marilith","rafflesia","seraph"
}
EU_WORLDS = {
    "cerberus","louisoix","moogle","omega","phantom","ragnarok","sagittarius","spriggan",
    "alpha","lich","odin","phoenix","raiden","shiva","twintania","zodiark"
}
OCE_WORLDS = {"bismarck","ravana","sephirot","sophia","zurvan"}
JP_WORLDS = {
    "aegis","atomos","carbuncle","garuda","gungnir","kujata","tonberry","typhon",
    "alexander","bahamut","durandal","fenrir","ifrit","ridill","tiamat","ultima",
    "anima","asura","chocobo","hades","ixion","masamune","pandaemonium","titan",
    "belias","mandragora","ramuh","shinryu","unicorn","valefor","yojimbo","zeromus"
}

def region_from_world(world: str) -> str:
    if not world:
        return ""
    w = str(world).strip().lower()
    if w in NA_WORLDS: return "NA"
    if w in EU_WORLDS: return "EU"
    if w in OCE_WORLDS: return "OCE"
    if w in JP_WORLDS: return "JP"
    return ""  # unknown/uncategorized

# ===============================================
# Submarine Part Constants
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

# Part type abbreviations for column headers
PART_TYPE_ABBREV = {
    "Bow": "BOW",
    "Bridge": "BRG",
    "Pressure Hull": "PH",
    "Stern": "STN"
}

# Generate ordered list of part column names (40 columns)
def generate_part_column_names():
    """Generate the 40 submarine part column names in order."""
    class_order = ["S", "U", "W", "C", "Y", "S+", "U+", "W+", "C+", "Y+"]
    part_order = ["BOW", "BRG", "PH", "STN"]
    columns = []
    for class_code in class_order:
        for part_code in part_order:
            columns.append(f"{class_code} {part_code}")
    return columns

PART_COLUMNS = generate_part_column_names()

# Map item IDs to part column names
def get_part_column_name(item_id):
    """Get the column name for a submarine part item ID."""
    if item_id not in SUB_PARTS_LOOKUP:
        return None
    
    full_name = SUB_PARTS_LOOKUP[item_id]
    
    # Find class
    class_code = None
    for class_name, code in CLASS_SHORTCUTS.items():
        if full_name.startswith(class_name):
            class_code = code
            break
    
    if not class_code:
        return None
    
    # Find part type
    part_code = None
    for part_name, abbrev in PART_TYPE_ABBREV.items():
        if part_name in full_name:
            part_code = abbrev
            break
    
    if not part_code:
        return None
    
    return f"{class_code} {part_code}"

# ===============================================
# Altoholic scanning helpers
# ===============================================
def _safe_json_load(s):
    if not s or s == "null":
        return None
    try:
        return json.loads(s)
    except Exception:
        return None

# Residential District mapping
RESIDENTIAL_DISTRICTS = {
    8: "Mist",
    9: "Goblet",
    2: "Lavender Beds",
    70: "Empyreum",
    111: "Shirogane"
}

# District abbreviations for Excel
DISTRICT_ABBREV = {
    "Mist": "M",
    "Goblet": "G",
    "Lavender Beds": "LB",
    "Empyreum": "E",
    "Shirogane": "S"
}

def load_lifestream_data(lifestream_path):
    """
    Load housing plot data from Lifestream config.
    Returns a dict mapping CID -> {'private': {'ward': int, 'plot': int, 'district': str}, 'fc': {'ward': int, 'plot': int, 'district': str}}
    Characters can have both a private house and FC house.
    """
    if not os.path.isfile(lifestream_path):
        return {}
    
    try:
        with open(lifestream_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        
        house_data = data.get('HousePathDatas', [])
        housing_map = {}
        
        for entry in house_data:
            cid = entry.get('CID')
            if cid:
                # Initialize character housing data if not exists
                if cid not in housing_map:
                    housing_map[cid] = {'private': None, 'fc': None}
                
                # Wards and plots are 0-indexed in Lifestream, add 1 for display
                ward = entry.get('Ward')
                plot = entry.get('Plot')
                if ward is not None:
                    ward = ward + 1
                if plot is not None:
                    plot = plot + 1
                
                # Get residential district
                district_id = entry.get('ResidentialDistrict')
                district_name = RESIDENTIAL_DISTRICTS.get(district_id, "")
                district_abbrev = DISTRICT_ABBREV.get(district_name, "")
                
                is_private = entry.get('IsPrivate', False)
                
                # Store in appropriate category with district info
                if is_private:
                    housing_map[cid]['private'] = {'ward': ward, 'plot': plot, 'district': district_abbrev}
                else:
                    housing_map[cid]['fc'] = {'ward': ward, 'plot': plot, 'district': district_abbrev}
        
        return housing_map
    except Exception as e:
        print(f"[WARNING] Failed to load Lifestream data from '{lifestream_path}': {e}")
        return {}

def scan_altoholic_db(db_path):
    """
    Scan a single Altoholic DB and return a mapping:
      { CharacterId: {"treasure_value": int, "parts": {"S BOW": qty, ...}, "last_online": int} }
    Note: Tanks and Kits are now sourced from DefaultConfig.json, not Altoholic.
    """
    result = {}
    if not os.path.isfile(db_path):
        return result

    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        rows = cur.execute("SELECT CharacterId, Inventory, Saddle, LastOnline FROM characters").fetchall()
        for char_id, inv_json, saddle_json, last_online_timestamp in rows:
            treasure_value = 0
            parts_count = {col: 0 for col in PART_COLUMNS}  # Initialize all 40 part columns to 0

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
                    
                    # Check for treasure items
                    if iid in TREASURE_IDS:
                        treasure_value += qty * TREASURE_VALUES[iid]
                    
                    # Check for submarine parts
                    if iid in SUB_PARTS_LOOKUP:
                        col_name = get_part_column_name(iid)
                        if col_name:
                            parts_count[col_name] += qty

            inv = _safe_json_load(inv_json)
            if isinstance(inv, list):
                consume(inv)
            sad = _safe_json_load(saddle_json)
            if isinstance(sad, list):
                consume(sad)
            
            # Calculate last online in days (rounded down)
            last_online_days = None
            if last_online_timestamp and last_online_timestamp > 0:
                current_timestamp = datetime.datetime.now().timestamp()
                days_ago = (current_timestamp - last_online_timestamp) / 86400  # 86400 seconds in a day
                last_online_days = int(days_ago)  # Round down to solid number

            # Only add to result if there's any data
            if treasure_value or any(parts_count.values()) or last_online_days is not None:
                result[int(char_id)] = {
                    "treasure_value": int(treasure_value),
                    "parts": parts_count,
                    "last_online_days": last_online_days
                }
        con.close()
    except Exception as e:
        print(f"[WARNING] Failed to scan Altoholic DB '{db_path}': {e}")
    return result

# ===============================================
# Existing helpers
# ===============================================
def extract_fc_data(full_data):
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
    for prefix, code in CLASS_SHORTCUTS.items():
        if full_name.startswith(prefix):
            return code
    return "?"

def get_sub_parts_string(sub_data: dict) -> str:
    parts = []
    for key in ["Part1", "Part2", "Part3", "Part4"]:
        part_id = sub_data.get(key, 0)
        if part_id != 0:
            full_part_name = SUB_PARTS_LOOKUP.get(part_id, f"Unknown({part_id})")
            short_code = shorten_part_name(full_part_name)
            parts.append(short_code)
    return "".join(parts)

def build_char_summaries(all_characters, fc_data, alto_map, account_configs, housing_map):
    char_summaries = []
    # Create a mapping of account nickname to config
    acc_config_map = {acc["nickname"]: acc for acc in account_configs}
    
    # Helper function to calculate Inverse Supplier needed amounts
    def calculate_inverse_supplier_amounts(current_tanks, current_kits, fuel_threshold, repair_mats_threshold):
        """Calculate needed amounts for Inverse Supplier v2.11 smart distribution"""
        # If threshold is 0, output 0 (excludes from smart distribution)
        # If threshold > 0, calculate: threshold - current_count (minimum 0)
        fuel_needed = max(0, fuel_threshold - current_tanks) if fuel_threshold > 0 else 0
        kits_needed = max(0, repair_mats_threshold - current_kits) if repair_mats_threshold > 0 else 0
        return fuel_needed, kits_needed
    
    for char in all_characters:
        cid = char.get("CID", 0)
        char_name = char.get("Name", "Unknown")
        world = char.get("World", "Unknown")
        char_gil = char.get("Gil", 0)
        nickname = char.get("AccountNickname", "UnknownAcct")

        retainer_data = char.get("RetainerData", [])
        total_ret_gil = 0
        for ret in retainer_data:
            gil = ret.get("Gil", 0)
            total_ret_gil += gil

            if "MBItems" not in ret:
                ret["MBItems"] = len(ret.get("MarketBoardItems", []))
            if isinstance(ret["MBItems"], bool):
                ret["MBItems"] = 1 if ret["MBItems"] else 0

            if "HasVenture" in ret:
                if isinstance(ret["HasVenture"], bool):
                    ret["HasVenture"] = 1 if ret["HasVenture"] else 0
            else:
                ret["HasVenture"] = 1 if ret.get("VentureID", 0) > 0 else 0

            ret["Level"] = ret.get("Level", 0)

        # Check if submarines should be included for this account
        include_subs = acc_config_map.get(nickname, {}).get("include_submarines", True)
        
        # Get Inverse Supplier thresholds for this account
        fuel_threshold = acc_config_map.get(nickname, {}).get("fuel_threshold", 0)
        repair_mats_threshold = acc_config_map.get(nickname, {}).get("repair_mats_threshold", 0)
        
        sub_data_map = {
            "Submersible-1": {"level": 0, "parts": "", "return_time": 0},
            "Submersible-2": {"level": 0, "parts": "", "return_time": 0},
            "Submersible-3": {"level": 0, "parts": "", "return_time": 0},
            "Submersible-4": {"level": 0, "parts": "", "return_time": 0},
        }
        
        if include_subs:
            sub_info = char.get("AdditionalSubmarineData", {})
            offline_sub_data = char.get("OfflineSubmarineData", [])
            current_time = datetime.datetime.now().timestamp()
            
            # Process submarines by matching OfflineSubmarineData index to slot, then lookup by name
            # OfflineSubmarineData is an array where index corresponds to submarine slot
            for idx, offline_sub in enumerate(offline_sub_data):
                # Map index to submarine slot key (0 -> "Submersible-1", 1 -> "Submersible-2", etc.)
                sub_slot_key = f"Submersible-{idx + 1}"
                if sub_slot_key in sub_data_map:
                    # Get the submarine name from OfflineSubmarineData
                    sub_name = offline_sub.get("Name", "")
                    
                    # Use the name to look up level/parts in AdditionalSubmarineData
                    if sub_name in sub_info:
                        sub_data_map[sub_slot_key]["level"] = sub_info[sub_name].get("Level", 0)
                        sub_data_map[sub_slot_key]["parts"] = get_sub_parts_string(sub_info[sub_name])
                    
                    # Get return time from OfflineSubmarineData
                    return_timestamp = offline_sub.get("ReturnTime", 0)
                    if return_timestamp > 0:
                        # Convert to hours remaining (can be negative if already returned)
                        hours_remaining = (return_timestamp - current_time) / 3600
                        sub_data_map[sub_slot_key]["return_time"] = round(hours_remaining, 2)
                    else:
                        sub_data_map[sub_slot_key]["return_time"] = 0

        fc_name = ""
        fc_points = 0
        if cid in fc_data:
            fc_name = fc_data[cid].get("Name", "")
            fc_points = fc_data[cid].get("FCPoints", 0)

        # Get tanks and kits from DefaultConfig.json (same source as Auto-AutoRetainer)
        # This ensures consistency with the submarine timer scripts
        tank = char.get("Ceruleum", 0)
        kits = char.get("RepairKits", 0)
        
        # Altoholic fields (treasure value, submarine parts, last online)
        treasure_value = 0
        parts_inventory = {col: 0 for col in PART_COLUMNS}  # Initialize all 40 part columns
        last_online_days = None
        if isinstance(cid, int) and cid in alto_map:
            treasure_value = alto_map[cid].get("treasure_value", 0)
            parts_inventory = alto_map[cid].get("parts", {col: 0 for col in PART_COLUMNS})
            last_online_days = alto_map[cid].get("last_online_days", None)
        
        # Calculate restocking days based on submarine builds
        restocking_days = None
        # Collect all submarine builds for this character
        char_builds = []
        for slot_num in range(1, 5):
            slot_key = f"Submersible-{slot_num}"
            parts = sub_data_map[slot_key]["parts"]
            if parts and parts != "":
                char_builds.append(parts)
        
        # Only calculate if character has submarines
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
            
            # Calculate days remaining (0 if no inventory)
            if total_tanks_per_day > 0 and total_kits_per_day > 0:
                days_from_tanks = tank / total_tanks_per_day if tank > 0 else 0
                days_from_kits = kits / total_kits_per_day if kits > 0 else 0
                restocking_days = int(min(days_from_tanks, days_from_kits))  # Round down to lowest solid number (will be 0 if either is 0)

        # Region is always derived from World
        region = region_from_world(world)
        
        # Housing data from Lifestream (separate private and FC)
        private_ward = None
        private_plot = None
        private_zone = None
        fc_ward = None
        fc_plot = None
        fc_zone = None
        if isinstance(cid, int) and cid in housing_map:
            private_house = housing_map[cid].get('private')
            fc_house = housing_map[cid].get('fc')
            if private_house:
                private_ward = private_house.get('ward')
                private_plot = private_house.get('plot')
                private_zone = private_house.get('district')
            if fc_house:
                fc_ward = fc_house.get('ward')
                fc_plot = fc_house.get('plot')
                fc_zone = fc_house.get('district')

        char_summaries.append({
            "cid": cid,
            "account_nickname": nickname,
            "char_name": char_name,
            "world": world,
            "char_gil": char_gil,
            "retainers": retainer_data,
            "retainer_count": len(retainer_data),
            "total_gil": char_gil + total_ret_gil,
            "fc_name": fc_name,
            "fc_points": fc_points,
            "sub1lvl": sub_data_map["Submersible-1"]["level"],
            "sub1parts": sub_data_map["Submersible-1"]["parts"],
            "sub1return": sub_data_map["Submersible-1"]["return_time"],
            "sub2lvl": sub_data_map["Submersible-2"]["level"],
            "sub2parts": sub_data_map["Submersible-2"]["parts"],
            "sub2return": sub_data_map["Submersible-2"]["return_time"],
            "sub3lvl": sub_data_map["Submersible-3"]["level"],
            "sub3parts": sub_data_map["Submersible-3"]["parts"],
            "sub3return": sub_data_map["Submersible-3"]["return_time"],
            "sub4lvl": sub_data_map["Submersible-4"]["level"],
            "sub4parts": sub_data_map["Submersible-4"]["parts"],
            "sub4return": sub_data_map["Submersible-4"]["return_time"],
            "tank": tank,
            "kits": kits,
            "restocking_days": restocking_days,
            "inventory_space": char.get("InventorySpace", 0),
            "ventures": char.get("Ventures", 0),
            "venture_coffers": char.get("VentureCoffers", 0),
            "treasure_value": treasure_value,
            "region": region,
            "last_online_days": last_online_days,
            "private_ward": private_ward,
            "private_plot": private_plot,
            "private_zone": private_zone,
            "fc_ward": fc_ward,
            "fc_plot": fc_plot,
            "fc_zone": fc_zone,
            "fuel_threshold": fuel_threshold,
            "repair_mats_threshold": repair_mats_threshold,
            "parts_inventory": parts_inventory,
        })
    return char_summaries

def write_excel(char_summaries, excel_output_path):
    char_summaries.sort(key=lambda x: x["total_gil"], reverse=True)

    try:
        workbook = xlsxwriter.Workbook(excel_output_path)
        worksheet = workbook.add_worksheet("FFXIV Gil Summary")
        summary_sheet = workbook.add_worksheet("Summary")

        header_format = workbook.add_format({
            "bold": True,
            "bg_color": "#CFCFCF",
            "border": 1,
            "align": "left",
            "valign": "vcenter"
        })
        money_format = workbook.add_format({"num_format": "#,##0", "align": "right"})
        total_format = workbook.add_format({
            "num_format": "#,##0",
            "bold": True,
            "align": "right",
            "bg_color": "#E6F2FF"
        })
        char_format = workbook.add_format({"bg_color": "#F2F2F2"})
        date_format = workbook.add_format({"num_format": "yyyy-mm-dd hh:mm:ss"})

        headers = [
            "CID",
            "Account Nickname",
            "Character Name",
            "World",
            "Region",
            "Last Online",
            "Private Ward",
            "Private Plot",
            "Private Zone",
            "FC Ward",
            "FC Plot",
            "FC Zone",
            "Character Gil",
            "Retainer Name",
            "MBItems",
            "HasVenture",
            "Level",
            "Retainer Gil",
            "Total Gil",
            "FC Name",
            "FC Points",
            "Lvl #1",
            "#1",
            "#1 Return",
            "Lvl #2",
            "#2",
            "#2 Return",
            "Lvl #3",
            "#3",
            "#3 Return",
            "Lvl #4",
            "#4",
            "#4 Return",
            "Tanks",
            "Kits",
            "Restocking Days",
            "Inventory Spaces",
            "Ventures",
            "VentureCoffers",
            "Treasure Value",
            "Plain Name",
            "List Formatting",
            "SND Formatting",
            "Bagman Formatting",
            "Inverse Supplier Formatting",
            "Tanks Needed",
            "Kits Needed"
        ] + PART_COLUMNS + ["Total Parts"]  # Add 40 part columns + Total Parts column
        for col_idx, head in enumerate(headers):
            worksheet.write(0, col_idx, head, header_format)

        TANK_COL = headers.index("Tanks")
        KITS_COL = headers.index("Kits")
        RESTOCK_COL = headers.index("Restocking Days")
        INV_SPACE_COL = headers.index("Inventory Spaces")
        VENTURES_COL = headers.index("Ventures")
        VENTURE_COFFERS_COL = headers.index("VentureCoffers")
        TREAS_COL = headers.index("Treasure Value")
        TANKS_NEEDED_COL = headers.index("Tanks Needed")
        KITS_NEEDED_COL = headers.index("Kits Needed")
        # Part columns start after Kits Needed
        PARTS_START_COL = KITS_NEEDED_COL + 1
        TOTAL_PARTS_COL = headers.index("Total Parts")

        row = 1
        for summary in char_summaries:
            cid = summary["cid"]
            nickname = summary["account_nickname"]
            char_name = summary["char_name"]
            world = summary["world"]
            region = summary.get("region", "")
            last_online_days = summary.get("last_online_days")
            private_ward = summary.get("private_ward")
            private_plot = summary.get("private_plot")
            private_zone = summary.get("private_zone")
            fc_ward = summary.get("fc_ward")
            fc_plot = summary.get("fc_plot")
            fc_zone = summary.get("fc_zone")
            char_gil = summary["char_gil"]
            total_gil = summary["total_gil"]
            fc_name = summary["fc_name"]
            fc_points = summary["fc_points"]

            sub1lvl = summary["sub1lvl"]
            sub1parts = summary["sub1parts"]
            sub1return = summary["sub1return"]
            sub2lvl = summary["sub2lvl"]
            sub2parts = summary["sub2parts"]
            sub2return = summary["sub2return"]
            sub3lvl = summary["sub3lvl"]
            sub3parts = summary["sub3parts"]
            sub3return = summary["sub3return"]
            sub4lvl = summary["sub4lvl"]
            sub4parts = summary["sub4parts"]
            sub4return = summary["sub4return"]

            tank = summary.get("tank", 0)
            kits = summary.get("kits", 0)
            restocking_days = summary.get("restocking_days")
            inventory_space = summary.get("inventory_space", 0)
            ventures = summary.get("ventures", 0)
            venture_coffers = summary.get("venture_coffers", 0)
            treasure_value = summary.get("treasure_value", 0)
            
            # Get parts inventory and calculate total
            parts_inventory = summary.get("parts_inventory", {col: 0 for col in PART_COLUMNS})
            total_parts = sum(parts_inventory.values())

            plain_nameworld = f"{char_name}@{world}"
            list_nameworld = f"\"{char_name}@{world}\","
            snd_nameworld = f"{{\"{char_name}@{world}\"}},"
            bagman_nameworld_tony = f"{{\"{char_name}@{world}\", 1, 69,\"Tony Name\"}},"
            
            # Calculate Inverse Supplier formatting with smart distribution
            fuel_threshold = summary.get("fuel_threshold", 0)
            repair_mats_threshold = summary.get("repair_mats_threshold", 0)
            
            # Helper function for smart distribution calculation
            def calc_needed(current, threshold):
                return max(0, threshold - current) if threshold > 0 else 0
            
            fuel_needed = calc_needed(tank, fuel_threshold)
            kits_needed = calc_needed(kits, repair_mats_threshold)
            inverse_supplier_formatting = f"{{\"{char_name}@{world}\", {fuel_needed}, {kits_needed}}},"

            retainers = summary["retainers"]

            if not retainers:
                worksheet.write_string(row, 0, str(cid))
                worksheet.write(row, 1, nickname)
                worksheet.write(row, 2, char_name)
                worksheet.write(row, 3, world)
                worksheet.write(row, 4, region)
                worksheet.write(row, 5, last_online_days if last_online_days is not None else "")
                worksheet.write(row, 6, private_ward if private_ward is not None else "")
                worksheet.write(row, 7, private_plot if private_plot is not None else "")
                worksheet.write(row, 8, private_zone if private_zone else "")
                worksheet.write(row, 9, fc_ward if fc_ward is not None else "")
                worksheet.write(row, 10, fc_plot if fc_plot is not None else "")
                worksheet.write(row, 11, fc_zone if fc_zone else "")
                worksheet.write_number(row, 12, char_gil, money_format)
                worksheet.write(row, 13, "")
                worksheet.write(row, 14, "")
                worksheet.write(row, 15, "")
                worksheet.write(row, 16, "")
                worksheet.write_number(row, 17, 0, money_format)
                worksheet.write_number(row, 18, total_gil, total_format)
                worksheet.write(row, 19, fc_name)
                worksheet.write_number(row, 20, fc_points, money_format)
                worksheet.write_number(row, 21, sub1lvl)
                worksheet.write(row, 22, sub1parts)
                worksheet.write_number(row, 23, sub1return, money_format)
                worksheet.write_number(row, 24, sub2lvl)
                worksheet.write(row, 25, sub2parts)
                worksheet.write_number(row, 26, sub2return, money_format)
                worksheet.write_number(row, 27, sub3lvl)
                worksheet.write(row, 28, sub3parts)
                worksheet.write_number(row, 29, sub3return, money_format)
                worksheet.write_number(row, 30, sub4lvl)
                worksheet.write(row, 31, sub4parts)
                worksheet.write_number(row, 32, sub4return, money_format)
                worksheet.write_number(row, TANK_COL, tank, money_format)
                worksheet.write_number(row, KITS_COL, kits, money_format)
                if restocking_days is not None:
                    worksheet.write_number(row, RESTOCK_COL, restocking_days, money_format)
                else:
                    worksheet.write(row, RESTOCK_COL, "")
                worksheet.write_number(row, INV_SPACE_COL, inventory_space, money_format)
                if ventures > 0:
                    worksheet.write_number(row, VENTURES_COL, ventures, money_format)
                else:
                    worksheet.write(row, VENTURES_COL, "")
                if venture_coffers > 0:
                    worksheet.write_number(row, VENTURE_COFFERS_COL, venture_coffers, money_format)
                else:
                    worksheet.write(row, VENTURE_COFFERS_COL, "")
                worksheet.write_number(row, TREAS_COL, treasure_value, total_format if treasure_value else money_format)
                worksheet.write(row, 40, plain_nameworld)
                worksheet.write(row, 41, list_nameworld)
                worksheet.write(row, 42, snd_nameworld)
                worksheet.write(row, 43, bagman_nameworld_tony)
                worksheet.write(row, 44, inverse_supplier_formatting)
                if fuel_needed > 0:
                    worksheet.write_number(row, TANKS_NEEDED_COL, fuel_needed, money_format)
                else:
                    worksheet.write(row, TANKS_NEEDED_COL, "")
                if kits_needed > 0:
                    worksheet.write_number(row, KITS_NEEDED_COL, kits_needed, money_format)
                else:
                    worksheet.write(row, KITS_NEEDED_COL, "")
                # Write submarine parts data (40 columns)
                for i, part_col in enumerate(PART_COLUMNS):
                    part_qty = parts_inventory.get(part_col, 0)
                    if part_qty > 0:
                        worksheet.write_number(row, PARTS_START_COL + i, part_qty, money_format)
                    else:
                        worksheet.write(row, PARTS_START_COL + i, "")
                # Write total parts
                worksheet.write_number(row, TOTAL_PARTS_COL, total_parts, money_format)
                row += 1
            else:
                for i, ret in enumerate(retainers):
                    ret_name = ret.get("Name", "Unknown")
                    ret_gil = ret.get("Gil", 0)
                    mb_items = ret.get("MBItems", 0)
                    has_venture = ret.get("HasVenture", 0)
                    ret_level = ret.get("Level", 0)

                    if i == 0:
                        worksheet.write_string(row, 0, str(cid))
                        worksheet.write(row, 1, nickname)
                        worksheet.write(row, 2, char_name, char_format)
                        worksheet.write(row, 3, world)
                        worksheet.write(row, 4, region)
                        worksheet.write(row, 5, last_online_days if last_online_days is not None else "")
                        worksheet.write(row, 6, private_ward if private_ward is not None else "")
                        worksheet.write(row, 7, private_plot if private_plot is not None else "")
                        worksheet.write(row, 8, private_zone if private_zone else "")
                        worksheet.write(row, 9, fc_ward if fc_ward is not None else "")
                        worksheet.write(row, 10, fc_plot if fc_plot is not None else "")
                        worksheet.write(row, 11, fc_zone if fc_zone else "")
                        worksheet.write_number(row, 12, char_gil, money_format)
                    else:
                        worksheet.write(row, 0, "")
                        worksheet.write(row, 1, "")
                        worksheet.write(row, 2, "")
                        worksheet.write(row, 3, "")
                        worksheet.write(row, 4, "")
                        worksheet.write(row, 5, "")
                        worksheet.write(row, 6, "")
                        worksheet.write(row, 7, "")
                        worksheet.write(row, 8, "")
                        worksheet.write(row, 9, "")
                        worksheet.write(row, 10, "")
                        worksheet.write(row, 11, "")
                        worksheet.write(row, 12, "")

                    worksheet.write(row, 13, ret_name)
                    if mb_items > 0:
                        worksheet.write_number(row, 14, mb_items, money_format)
                    else:
                        worksheet.write(row, 14, "")
                    if has_venture > 0:
                        worksheet.write_number(row, 15, has_venture, money_format)
                    else:
                        worksheet.write(row, 15, "")
                    if ret_level > 0:
                        worksheet.write_number(row, 16, ret_level, money_format)
                    else:
                        worksheet.write(row, 16, "")
                    worksheet.write_number(row, 17, ret_gil, money_format)

                    if i == 0:
                        worksheet.write_number(row, 18, total_gil, total_format)
                        worksheet.write(row, 19, fc_name)
                        worksheet.write_number(row, 20, fc_points, money_format)
                        worksheet.write_number(row, 21, sub1lvl)
                        worksheet.write(row, 22, sub1parts)
                        worksheet.write_number(row, 23, sub1return, money_format)
                        worksheet.write_number(row, 24, sub2lvl)
                        worksheet.write(row, 25, sub2parts)
                        worksheet.write_number(row, 26, sub2return, money_format)
                        worksheet.write_number(row, 27, sub3lvl)
                        worksheet.write(row, 28, sub3parts)
                        worksheet.write_number(row, 29, sub3return, money_format)
                        worksheet.write_number(row, 30, sub4lvl)
                        worksheet.write(row, 31, sub4parts)
                        worksheet.write_number(row, 32, sub4return, money_format)
                        worksheet.write_number(row, TANK_COL, tank, money_format)
                        worksheet.write_number(row, KITS_COL, kits, money_format)
                        if restocking_days is not None:
                            worksheet.write_number(row, RESTOCK_COL, restocking_days, money_format)
                        else:
                            worksheet.write(row, RESTOCK_COL, "")
                        worksheet.write_number(row, INV_SPACE_COL, inventory_space, money_format)
                        if ventures > 0:
                            worksheet.write_number(row, VENTURES_COL, ventures, money_format)
                        else:
                            worksheet.write(row, VENTURES_COL, "")
                        if venture_coffers > 0:
                            worksheet.write_number(row, VENTURE_COFFERS_COL, venture_coffers, money_format)
                        else:
                            worksheet.write(row, VENTURE_COFFERS_COL, "")
                        worksheet.write_number(row, TREAS_COL, treasure_value, total_format if treasure_value else money_format)
                        worksheet.write(row, 40, plain_nameworld)
                        worksheet.write(row, 41, list_nameworld)
                        worksheet.write(row, 42, snd_nameworld)
                        worksheet.write(row, 43, bagman_nameworld_tony)
                        worksheet.write(row, 44, inverse_supplier_formatting)
                        if fuel_needed > 0:
                            worksheet.write_number(row, TANKS_NEEDED_COL, fuel_needed, money_format)
                        else:
                            worksheet.write(row, TANKS_NEEDED_COL, "")
                        if kits_needed > 0:
                            worksheet.write_number(row, KITS_NEEDED_COL, kits_needed, money_format)
                        else:
                            worksheet.write(row, KITS_NEEDED_COL, "")
                        # Write submarine parts data (40 columns)
                        for j, part_col in enumerate(PART_COLUMNS):
                            part_qty = parts_inventory.get(part_col, 0)
                            if part_qty > 0:
                                worksheet.write_number(row, PARTS_START_COL + j, part_qty, money_format)
                            else:
                                worksheet.write(row, PARTS_START_COL + j, "")
                        # Write total parts
                        worksheet.write_number(row, TOTAL_PARTS_COL, total_parts, money_format)
                    else:
                        # Blank out all non-retainer columns for subsequent retainer rows
                        for c in (18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, TANK_COL, KITS_COL, RESTOCK_COL, INV_SPACE_COL, VENTURES_COL, VENTURE_COFFERS_COL, TREAS_COL, 40, 41, 42, 43, 44, TANKS_NEEDED_COL, KITS_NEEDED_COL):
                            worksheet.write(row, c, "")
                        # Blank out parts columns for subsequent retainer rows
                        for j in range(len(PART_COLUMNS)):
                            worksheet.write(row, PARTS_START_COL + j, "")
                        worksheet.write(row, TOTAL_PARTS_COL, "")

                    row += 1

        worksheet.set_column("A:A", 19)  # CID
        worksheet.set_column("B:B", 12)  # Account Nickname
        worksheet.set_column("C:C", 25)  # Character Name
        worksheet.set_column("D:D", 15)  # World
        worksheet.set_column("E:E", 5)   # Region
        worksheet.set_column("F:F", 4)  # Last Online
        worksheet.set_column("G:G", 3)  # Private Ward
        worksheet.set_column("H:H", 3)  # Private Plot
        worksheet.set_column("I:I", 3)  # Private Zone
        worksheet.set_column("J:J", 3)  # FC Ward
        worksheet.set_column("K:K", 3)  # FC Plot
        worksheet.set_column("L:L", 3)  # FC Zone
        worksheet.set_column("M:M", 15)  # Character Gil
        worksheet.set_column("N:N", 25)  # Retainer Name
        worksheet.set_column("O:O", 6)  # MBItems
        worksheet.set_column("P:P", 4)  # HasVenture
        worksheet.set_column("Q:Q", 7)  # Retainer Level
        worksheet.set_column("R:R", 15)  # Retainer Gil
        worksheet.set_column("S:S", 15)  # Total Gil
        worksheet.set_column("T:T", 25)  # FC Name
        worksheet.set_column("U:U", 13)  # FC Points
        worksheet.set_column("V:V", 7)   # Lvl #1
        worksheet.set_column("W:W", 9)   # #1
        worksheet.set_column("X:X", 3)   # #1 Return
        worksheet.set_column("Y:Y", 7)   # Lvl #2
        worksheet.set_column("Z:Z", 9)   # #2
        worksheet.set_column("AA:AA", 3)   # #2 Return
        worksheet.set_column("AB:AB", 7)   # Lvl #3
        worksheet.set_column("AC:AC", 9)   # #3
        worksheet.set_column("AD:AD", 3)   # #3 Return
        worksheet.set_column("AE:AE", 7)   # Lvl #4
        worksheet.set_column("AF:AF", 9)   # #4
        worksheet.set_column("AG:AG", 3)   # #4 Return
        worksheet.set_column(TANK_COL, TANK_COL, 9)   # Tanks
        worksheet.set_column(KITS_COL, KITS_COL, 9)   # Kits
        worksheet.set_column(RESTOCK_COL, RESTOCK_COL, 6)  # Restocking Days
        worksheet.set_column(INV_SPACE_COL, INV_SPACE_COL, 3.15) # Inventory Spaces
        worksheet.set_column(VENTURES_COL, VENTURES_COL, 7)   # Ventures
        worksheet.set_column(VENTURE_COFFERS_COL, VENTURE_COFFERS_COL, 5)   # VentureCoffers
        worksheet.set_column(TREAS_COL, TREAS_COL, 15) # Treasure Value
        worksheet.set_column(40, 40, 30)  # Plain Name
        worksheet.set_column(41, 41, 38)  # List Formatting
        worksheet.set_column(42, 42, 40)  # SND Formatting
        worksheet.set_column(43, 43, 55)  # Bagman Formatting
        worksheet.set_column(44, 44, 45)  # Inverse Supplier Formatting (10 spaces less than Bagman)
        worksheet.set_column(TANKS_NEEDED_COL, TANKS_NEEDED_COL, 9)  # Tanks Needed (same width as Tanks)
        worksheet.set_column(KITS_NEEDED_COL, KITS_NEEDED_COL, 9)  # Kits Needed (same width as Kits)
        # Set widths for all 40 submarine part columns (width 7)
        for i in range(len(PART_COLUMNS)):
            worksheet.set_column(PARTS_START_COL + i, PARTS_START_COL + i, 4)
        # Set width for Total Parts column (width 10)
        worksheet.set_column(TOTAL_PARTS_COL, TOTAL_PARTS_COL, 10)

        worksheet.autofilter(0, 0, 0, len(headers) - 1)
        worksheet.freeze_panes(1, 5)  # Freeze first row (headers) and columns A-E (through Region)

        summary_headers = ["Metric", "Value"]
        for col_idx, head in enumerate(summary_headers):
            summary_sheet.write(0, col_idx, head, header_format)
        summary_sheet.set_column("A:A", 30)
        summary_sheet.set_column("B:B", 20)

        total_gil_all = sum(c["total_gil"] for c in char_summaries)
        total_chars = len(char_summaries)
        total_retainers = sum(c["retainer_count"] for c in char_summaries)

        sub_parts_count = {}
        for summary in char_summaries:
            for part_str in [summary["sub1parts"], summary["sub2parts"], summary["sub3parts"], summary["sub4parts"]]:
                if part_str:
                    sub_parts_count[part_str] = sub_parts_count.get(part_str, 0) + 1
        sorted_parts = sorted(sub_parts_count.items(), key=lambda x: x[1], reverse=True)

        total_fc_points = sum(c["fc_points"] for c in char_summaries)
        
        # Total FC's: Count characters with submarine builds (each character = 1 FC workshop)
        # A character is considered an FC if they have FC name OR FC housing AND have at least one submarine
        total_fc_count = 0
        for c in char_summaries:
            has_fc_name = bool(c["fc_name"])
            has_fc_housing = bool(c.get("fc_ward") or c.get("fc_plot") or c.get("fc_zone"))
            has_sub_builds = bool(c["sub1parts"] or c["sub2parts"] or c["sub3parts"] or c["sub4parts"])
            
            if (has_fc_name or has_fc_housing) and has_sub_builds:
                total_fc_count += 1
        
        # Total FC's Farming Subs: Count characters with at least one farming submarine
        build_gil_rates_keys = {
            "WSUC", "SSUC", "W+S+U+C+", "S+S+S+C+", "YUUW", "Y+U+U+W+",
            "WCSU", "WUSS", "W+U+S+S+", "YSYC", "Y+S+Y+C+", "S+S+S+C+",
            "S+S+U+C+", "S+S+U+C", "WCYC", "WUWC", "W+U+W+C+", "YSCU",
            "SCUS", "S+C+U+S+"
        }
        total_fc_farming_subs = 0
        for c in char_summaries:
            has_fc_name = bool(c["fc_name"])
            has_fc_housing = bool(c.get("fc_ward") or c.get("fc_plot") or c.get("fc_zone"))
            
            if has_fc_name or has_fc_housing:
                # Check if ANY of the 4 sub builds are farming builds
                has_farming_build = any(
                    c[f"sub{i}parts"] in build_gil_rates_keys for i in [1, 2, 3, 4]
                )
                if has_farming_build:
                    total_fc_farming_subs += 1

        sub_levels = []
        for c in char_summaries:
            for i in [1, 2, 3, 4]:
                lvl = c.get(f"sub{i}lvl", 0)
                if lvl > 0:
                    sub_levels.append(lvl)
        lowest_sub_lvl = min(sub_levels) if sub_levels else 0
        highest_sub_lvl = max(sub_levels) if sub_levels else 0

        total_tanks = sum(c.get("tank", 0) for c in char_summaries)
        total_kits = sum(c.get("kits", 0) for c in char_summaries)
        total_treasure_value = sum(c.get("treasure_value", 0) for c in char_summaries)

        total_gil_value = total_gil_all + total_treasure_value

        summary_rows = [
            ["Total Characters", total_chars],
            ["Total Retainers", total_retainers],
            ["Total Gil (All Characters)", total_gil_all],
            ["Average Gil per Character", (total_gil_all / total_chars) if total_chars else 0],
            ["Total Tanks", total_tanks],
            ["Total Kits", total_kits],
            ["Total Treasure Value", total_treasure_value],
            ["Total Gil Value", total_gil_value],
        ]

        if char_summaries:
            summary_rows.extend([
                ["Richest Character", char_summaries[0]["char_name"]],
                ["Richest Character Gil", char_summaries[0]["total_gil"]],
                ["Total FC's", total_fc_count],
                ["Total FC's Farming Subs", total_fc_farming_subs],
                ["Total FC Points", total_fc_points],
                ["Lowest Sub Level", lowest_sub_lvl],
                ["Highest Sub Level", highest_sub_lvl]
            ])

        summary_rows.extend([
            ["Unique Submersible Parts", len(sub_parts_count)],
            ["Report Generated", datetime.datetime.now()],
        ])

        #
        # Define Gil rates for submarine builds
        # Based on Routes.xlsx - Gil/Sub/Day rates for each route
        #
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
        
        
        # Add submarine builds to summary with earnings info
        total_all_subs_count = 0
        if sorted_parts:
            summary_rows.insert(-1, ["Submarine Builds", ""])
            for i, (build, count) in enumerate(sorted_parts, 1):
                total_all_subs_count += count  # Count ALL submarines
                if build in build_gil_rates:
                    gil_per_day = build_gil_rates[build]
                    label = f"Build #{i} Earns: {gil_per_day:,} per sub"
                else:
                    label = f"Build #{i}"
                summary_rows.insert(-1, [label, f"{build} ({count} uses)"])
        
        # Calculate total gil farmed daily from all submarines
        gil_farmed_daily = 0
        for build, usage_count in sorted_parts:
            # Check if this build has a known gil farming rate
            if build in build_gil_rates:
                gil_per_day = build_gil_rates[build]
                gil_farmed_daily += gil_per_day * usage_count
                print(f"[INFO] Build {build} ({usage_count} subs) farms {gil_per_day:,} gil/day each = {gil_per_day * usage_count:,} gil/day total")

        # Add total submarines count (all builds, not just farming)
        if sorted_parts:
            summary_rows.insert(-1, ["Total Submarines", total_all_subs_count])
        
        if gil_farmed_daily > 0:
            summary_rows.insert(-1, ["Gil Farmed Annually", gil_farmed_daily * 365])
            summary_rows.insert(-1, ["Gil Farmed Every 30 Days", gil_farmed_daily * 30])
            summary_rows.insert(-1, ["Gil Farmed Each Day", gil_farmed_daily])

        r = 1
        for (label, value) in summary_rows:
            summary_sheet.write(r, 0, label)
            if isinstance(value, (int, float)):
                fmt = total_format if ("Gil" in label or "Points" in label or "Value" in label or "Tanks" in label or "Kits" in label) else None
                summary_sheet.write_number(r, 1, value, fmt)
            elif isinstance(value, datetime.datetime):
                summary_sheet.write_datetime(r, 1, value, date_format)
            else:
                summary_sheet.write(r, 1, value)
            r += 1

        workbook.close()
        print(f"[SUCCESS] Excel file created at: {os.path.abspath(excel_output_path)}")
        return excel_output_path

    except PermissionError:
        print(f"[ERROR] Permission denied writing '{excel_output_path}'. Is it open?")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to create Excel file: {e}")
        return None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description="Export FFXIV gil report with Regions by World and Altoholic inventory.")
    parser.add_argument("--no-altoholic", action="store_true", help="Disable Altoholic scanning for all accounts.")
    parser.add_argument("output", nargs="?", default="unused.xlsx", help="(Ignored) Legacy positional.")
    args = parser.parse_args()

    date_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    final_output_path = os.path.join(script_dir, f"{date_str} - ffxiv_gil_summary.xlsx")

    for entry in account_locations:
        nickname = entry["nickname"]
        auto_path = entry["auto_path"]
        if os.path.isfile(auto_path):
            print(f"[INFO] Found config for {nickname} at: {auto_path}")
            try:
                with open(auto_path, "r", encoding="utf-8-sig") as f:
                    data = json.load(f)
                fc_part = extract_fc_data(data)
                for holder, fc_info in fc_part.items():
                    all_fc_data[holder] = fc_info
                chars_part = collect_characters(data, account_nickname=nickname)
                all_characters.extend(chars_part)
            except Exception as e:
                print(f"[ERROR] Could not parse JSON from {auto_path}: {e}")
        else:
            print(f"[WARNING] No file found for {nickname} at {auto_path}. Skipping.")

    if not all_characters:
        print("[FAIL] No character data loaded from any path.]")
        # input("Press Enter to exit...")
        sys.exit(1)

    # Load Lifestream housing data from all accounts
    housing_map_global = {}
    for entry in account_locations:
        lfstrm_path = entry.get("lfstrm_path", "")
        if lfstrm_path and os.path.isfile(lfstrm_path):
            print(f"[INFO] Loading Lifestream housing data for {entry['nickname']}: {lfstrm_path}")
            partial_housing = load_lifestream_data(lfstrm_path)
            housing_map_global.update(partial_housing)
            print(f"[INFO] Loaded {len(partial_housing)} housing entries from {entry['nickname']}")
        else:
            print(f"[INFO] Lifestream config not found for {entry['nickname']}: {lfstrm_path}")
    
    alto_map_global = {}
    if not args.no_altoholic:
        for entry in account_locations:
            if not entry.get("include_altoholic", True):
                continue
            alto_path = entry.get("alto_path", "")
            if alto_path and os.path.isfile(alto_path):
                print(f"[INFO] Scanning Altoholic DB for {entry['nickname']}: {alto_path}")
                partial = scan_altoholic_db(alto_path)
                alto_map_global.update(partial)
            else:
                print(f"[INFO] Altoholic DB not found or disabled for {entry['nickname']}: {alto_path}")

    char_summaries = build_char_summaries(all_characters, all_fc_data, alto_map_global, account_locations, housing_map_global)
    result = write_excel(char_summaries, final_output_path)
    if result:
        print(f"[DONE] Wrote data to {result}")
        # input("Press Enter to exit...")
        sys.exit(0)
    else:
        print("[FAIL] Could not process data.")
        # input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
