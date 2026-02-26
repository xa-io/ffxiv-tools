############################################################################################################################
#
#  ██╗      █████╗ ███╗   ██╗██████╗ ██╗███╗   ██╗ ██████╗     ██████╗  █████╗  ██████╗ ███████╗
#  ██║     ██╔══██╗████╗  ██║██╔══██╗██║████╗  ██║██╔════╝     ██╔══██╗██╔══██╗██╔════╝ ██╔════╝
#  ██║     ███████║██╔██╗ ██║██║  ██║██║██╔██╗ ██║██║  ███╗    ██████╔╝███████║██║  ███╗█████╗  
#  ██║     ██╔══██║██║╚██╗██║██║  ██║██║██║╚██╗██║██║   ██║    ██╔═══╝ ██╔══██║██║   ██║██╔══╝  
#  ███████╗██║  ██║██║ ╚████║██████╔╝██║██║ ╚████║╚██████╔╝    ██║     ██║  ██║╚██████╔╝███████╗
#  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
#
# AutoRetainer Dashboard - Self-Hosted Web Interface
#
# A comprehensive web dashboard that displays FFXIV character data from AutoRetainer, Altoholic, and Lifestream.
# Provides a modern, dark-themed UI accessible via browser showing characters, submarines, retainers,
# housing locations, marketboard items, gil totals, inventory tracking, MSQ progression (disabled), job levels,
# currencies, income/cost calculations, and comprehensive supply tracking.
#
# Core Features:
# • Self-hosted Flask web server with configurable host/port
# • Real-time data parsing from AutoRetainer, Altoholic, and Lifestream configs
# • Character overview with gil, FC points, venture coins, coffers, dyes, and inventory
# • MSQ progression tracking with color-coded percentage (green ≥90%, yellow ≥50%, gray <50%)
# • Job level display: DoW/DoM and DoH/DoL collapsible sections with all job levels
# • Currency tracking: Categorized display (Crystals, Common, Tomestones, Battle, Societies)
# • Submarine tracking with builds, levels, plans (leveling/farming), and return times
# • Retainer details with venture status, levels, and marketboard items
# • Housing display showing Personal House and FC House locations
# • Sorting by level, gil, treasure, FC points, ventures, inventory, MSQ%, retainer/sub levels
# • Filtering by retainers, submarines, personal house, and FC house
# • Anonymize mode for screenshots (hides names, addresses with TOP SECRET)
# • Configurable display options (SHOW_CLASSES, SHOW_CURRENCIES)
# • Monthly income and daily repair cost calculations
# • Modern, responsive dark-themed UI with multi-account support
#
# Landing Page v1.28
# AutoRetainer Dashboard
# Created by: https://github.com/xa-io
# Last Updated: 2026-02-26 13:00:00
#
# ## Release Notes This Update ##
#
# v1.28 - FC Data & Data page overhaul
#         Sub Planner bidirectional sorting, Name@World display, ETA column, inventory stats
#         Data page: Excel export, sticky filters/headers, dark scrollbars, full-viewport layout
#         Unique FC count summary card, compact summary cards, integer formatting
#         FC Detection Diagnostic gated behind DEBUG flag
# v1.27 - Added /data/ page: Data Master List across all accounts
#         Sortable table with character name, world, account, sub 1-4 levels/builds/plans/returns
#         Character-level data: gil, ceruleum, repair kits, days to restock, inventory, treasure
#         Click any column header to sort ascending/descending
#         Summary cards: total subs, farming/leveling counts, daily income, supply costs
# v1.26 - Added /fcdata/ page: Plot Map & FC Capacity Planner
#         Visual housing plot overview with 5-column district grid (Goblet, LB, Mist, Empyreum, Shirogane)
#         Per-ward plot dots (green=FC, gold=Personal) with hover tooltips
#         FC Capacity Planner with per-account/region breakdown and world-level bars
#         Enhanced summary cards: Total Chars, In FC, Can Join FC, FC/Personal Plots
#         FC detection uses submarines + Lifestream FC house (not stale fc_name)
#         Disclaimer explaining sub-based FC detection and OCE 39/40 max capacity
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

# Display options
VERSION = "v1.28"       # Version number shown in footer and startup
SHOW_CLASSES = True     # Show DoW/DoM and DoH/DoL job sections, disable to speed up page load
SHOW_CURRENCIES = True  # Show currencies section, disable to speed up page load
SHOW_MSQ_PROGRESSION = True  # Show MSQ progression (disabled until Altoholic tracking works)
DEFAULT_THEME = "default"  # Theme preset for dashboard
HIGHLIGHT_IDLE_RETAINERS = True  # Cyan outline on character cards with idle retainers
HIGHLIGHT_IDLE_SUBS = True       # Pink outline on character cards with idle submarines
HIGHLIGHT_READY_ITEMS = True     # Red background on character cards with ready retainers/subs
HIGHLIGHT_MAX_MB = True          # Gold outline on character cards with max (20) MB listings
HIGHLIGHT_POTENTIAL_RETAINER = True  # Brown outline on characters with MSQ 66060 done but 0 retainers
HIGHLIGHT_POTENTIAL_SUBS = True  # Black outline on characters Lv 25+ not in FC (potential sub farmers)
HONOR_AR_EXCLUSIONS = True  # Honor AutoRetainer's ExcludeRetainer/ExcludeWorkshop settings per character

# Highlight Colors (customizable)
HIGHLIGHT_COLOR_IDLE_RETAINERS = "cyan"       # Cyan for idle retainers
HIGHLIGHT_COLOR_IDLE_SUBS = "#FFB6C1"         # Pink for idle subs
HIGHLIGHT_COLOR_MAX_MB = "#FFD700"            # Gold for max MB listings
HIGHLIGHT_COLOR_POTENTIAL_RETAINER = "#8B4513"  # Brown for potential retainers
HIGHLIGHT_COLOR_POTENTIAL_SUBS = "#1a1a1a"    # Black for potential sub farmers
# Available themes:
#   default      - Blue accent (original)
#   ultra-dark   - Near-black with subtle gray
#   dark-gray    - Neutral grays
#   ocean-blue   - Deep blues with cyan accent
#   forest-green - Dark greens
#   crimson-red  - Dark reds
#   purple-haze  - Dark purples
#   pastel-pink  - Soft pink with hot pink accent
#   dark-orange  - Warm orange/amber tones
#   brown        - Earthy brown/sienna tones

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
    lfstrm_path = os.path.join(pluginconfigs_path, "Lifestream", "DefaultConfig.json")
    return {
        "nickname": nickname,
        "auto_path": auto_path,
        "alto_path": alto_path,
        "lfstrm_path": lfstrm_path,
    }

# Default account locations - update these paths for your setup
# Supports both local paths (C:\Users\...) and network/UNC paths (\\server\share\...)
account_locations = [
    acc("Main", f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs"),
    # acc("Acc1", f"C:\\Users\\{user}\\AltData\\Acc1\\pluginConfigs"),
    # acc("Acc2", f"C:\\Users\\{user}\\AltData\\Acc2\\pluginConfigs"),
    # Network/UNC path examples:
    # acc("NetworkAcc", f"\\\\server\\share\\Users\\{user}\\pluginConfigs"),
    # acc("NAS-Acc", r"\\NAS\FFXIVData\pluginConfigs"),
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
# World Region Mappings (for region filtering)
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
    """Return region code (NA/EU/OCE/JP) for a given world name."""
    if not world:
        return ""
    w = str(world).strip().lower()
    if w in NA_WORLDS: return "NA"
    if w in EU_WORLDS: return "EU"
    if w in OCE_WORLDS: return "OCE"
    if w in JP_WORLDS: return "JP"
    return ""

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

# ClassJob ID to Abbreviation mapping (FFXIV internal job IDs)
CLASSJOB_ID_TO_ABBR = {
    0: "ADV",   # Adventurer
    1: "GLA", 2: "PGL", 3: "MRD", 4: "LNC", 5: "ARC", 6: "CNJ", 7: "THM",
    8: "CRP", 9: "BSM", 10: "ARM", 11: "GSM", 12: "LTW", 13: "WVR", 14: "ALC", 15: "CUL",
    16: "MIN", 17: "BTN", 18: "FSH",
    19: "PLD", 20: "MNK", 21: "WAR", 22: "DRG", 23: "BRD", 24: "WHM", 25: "BLM",
    26: "ACN", 27: "SMN", 28: "SCH", 29: "ROG", 30: "NIN", 31: "MCH", 32: "DRK",
    33: "AST", 34: "SAM", 35: "RDM", 36: "BLU", 37: "GNB", 38: "DNC", 39: "RPR",
    40: "SGE", 41: "VPR", 42: "PCT",
}

# ===============================================
# Job Categories for DoW/DoM and DoH/DoL display
# Shows only final job classes (not starter classes)
# ===============================================
JOB_CATEGORIES = {
    "Tank": ["Paladin", "Warrior", "DarkKnight", "Gunbreaker"],
    "Healer": ["WhiteMage", "Scholar", "Astrologian", "Sage"],
    "MeleeDPS": ["Monk", "Dragoon", "Ninja", "Samurai", "Reaper", "Viper"],
    "PhysRangedDPS": ["Bard", "Machinist", "Dancer"],
    "MagicRangedDPS": ["BlackMage", "Summoner", "RedMage", "Pictomancer", "BlueMage"],
    "DoH": ["Carpenter", "Blacksmith", "Armorer", "Goldsmith", "Leatherworker", "Weaver", "Alchemist", "Culinarian"],
    "DoL": ["Miner", "Botanist", "Fisher"],
}

# Map base classes to their upgraded jobs (for level lookup)
# If a character has Gladiator level but not Paladin, use Gladiator level for Paladin display
JOB_BASE_CLASS = {
    "Paladin": "Gladiator",
    "Warrior": "Marauder",
    "WhiteMage": "Conjurer",
    "BlackMage": "Thaumaturge",
    "Bard": "Archer",
    "Dragoon": "Lancer",
    "Monk": "Pugilist",
    "Summoner": "Arcanist",
    "Scholar": "Arcanist",
    "Ninja": "Rogue",
}

# Combat jobs only (for MSQ level validation - excludes DoH/DoL)
COMBAT_JOBS = set(
    JOB_CATEGORIES["Tank"] + JOB_CATEGORIES["Healer"] + 
    JOB_CATEGORIES["MeleeDPS"] + JOB_CATEGORIES["PhysRangedDPS"] + 
    JOB_CATEGORIES["MagicRangedDPS"]
)

# Map job names to display names (handles CamelCase to spaced names)
JOB_DISPLAY_NAMES = {
    "Paladin": "Paladin", "Warrior": "Warrior", "DarkKnight": "Dark Knight", "Gunbreaker": "Gunbreaker",
    "WhiteMage": "White Mage", "Scholar": "Scholar", "Astrologian": "Astrologian", "Sage": "Sage",
    "Monk": "Monk", "Dragoon": "Dragoon", "Ninja": "Ninja", "Samurai": "Samurai", "Reaper": "Reaper", "Viper": "Viper",
    "Bard": "Bard", "Machinist": "Machinist", "Dancer": "Dancer",
    "BlackMage": "Black Mage", "Summoner": "Summoner", "RedMage": "Red Mage", "Pictomancer": "Pictomancer", "BlueMage": "Blue Mage",
    "Carpenter": "Carpenter", "Blacksmith": "Blacksmith", "Armorer": "Armorer", "Goldsmith": "Goldsmith",
    "Leatherworker": "Leatherworker", "Weaver": "Weaver", "Alchemist": "Alchemist", "Culinarian": "Culinarian",
    "Miner": "Miner", "Botanist": "Botanist", "Fisher": "Fisher",
}

# ===============================================
# Currency Categories and Display Names
# ===============================================
# Categories for organizing currencies in the UI
CURRENCY_CATEGORIES = {
    "Crystals": [
        "Fire_Shard", "Fire_Crystal", "Fire_Cluster",
        "Ice_Shard", "Ice_Crystal", "Ice_Cluster",
        "Wind_Shard", "Wind_Crystal", "Wind_Cluster",
        "Earth_Shard", "Earth_Crystal", "Earth_Cluster",
        "Lightning_Shard", "Lightning_Crystal", "Lightning_Cluster",
        "Water_Shard", "Water_Crystal", "Water_Cluster",
    ],
    "Common": [
        "Gil", "MGP", "Venture", "Bicolor_Gemstone",
    ],
    "Tomestones": [
        "Allagan_Tomestone_Of_Poetics", "Allagan_Tomestone_Of_Aesthetics",
        "Allagan_Tomestone_Of_Heliometry", "Allagan_Tomestone_Of_Causality",
        "Allagan_Tomestone_Of_Comedy", "Allagan_Tomestone_Of_Astronomy",
        "Allagan_Tomestone_Of_Aphorism", "Allagan_Tomestone_Of_Revelation",
        "Allagan_Tomestone_Of_Allegory", "Allagan_Tomestone_Of_Phantasmagoria",
        "Allagan_Tomestone_Of_Goetia", "Allagan_Tomestone_Of_Genesis",
        "Allagan_Tomestone_Of_Mendacity", "Allagan_Tomestone_Of_Creation",
        "Allagan_Tomestone_Of_Verity", "Allagan_Tomestone_Of_Scripture",
        "Allagan_Tomestone_Of_Lore", "Allagan_Tomestone_Of_Esoterics",
        "Allagan_Tomestone_Of_Law", "Allagan_Tomestone_Of_Soldiery",
        "Allagan_Tomestone_Of_Poetics", "Allagan_Tomestone_Of_Mythology",
        "Allagan_Tomestone_Of_Philosophy", "Allagan_Tomestone_Of_Mnemosyne",
        "Allagan_Tomestone_Of_Mathematics",
    ],
    "Battle": [
        "Wolf_Mark", "Trophy_Crystal", "Allied_Seal", "Centurio_Seal",
        "Sack_Of_Nuts", "Faux_Leaf", "Bozjan_Cluster", "Flame_Seal",
        "Serpent_Seal", "Storm_Seal", "Achievement_Certificate",
    ],
    "Societies": [
        "Fae_Fancy", "Hammered_Frogment", "Carved_Kupo_Nut",
        "Loporrit_Carat", "Omicron_Omnitoken", "Seafarer's_Cowrie",
        "Ananta_Dreamstaff", "Arkasodara_Pana", "Black_Copper_Gil",
        "Kojin_Sango", "Namazu_Koban", "Pixie_Locket", "Qitari_Compliment",
        "Steel_Amalj'ok", "Sylphic_Goldleaf", "Titan_Cobaltpiece",
        "Tribal_Quest_Allowance",
    ],
}

# Shorten currency names for display
CURRENCY_SHORT_NAMES = {
    # Tomestones - remove "Allagan_Tomestone_Of_"
    "Allagan_Tomestone_Of_Poetics": "Poetics",
    "Allagan_Tomestone_Of_Aesthetics": "Aesthetics",
    "Allagan_Tomestone_Of_Heliometry": "Heliometry",
    "Allagan_Tomestone_Of_Causality": "Causality",
    "Allagan_Tomestone_Of_Comedy": "Comedy",
    "Allagan_Tomestone_Of_Astronomy": "Astronomy",
    "Allagan_Tomestone_Of_Aphorism": "Aphorism",
    "Allagan_Tomestone_Of_Revelation": "Revelation",
    "Allagan_Tomestone_Of_Allegory": "Allegory",
    "Allagan_Tomestone_Of_Phantasmagoria": "Phantasmagoria",
    "Allagan_Tomestone_Of_Goetia": "Goetia",
    "Allagan_Tomestone_Of_Genesis": "Genesis",
    "Allagan_Tomestone_Of_Mendacity": "Mendacity",
    "Allagan_Tomestone_Of_Creation": "Creation",
    "Allagan_Tomestone_Of_Verity": "Verity",
    "Allagan_Tomestone_Of_Scripture": "Scripture",
    "Allagan_Tomestone_Of_Lore": "Lore",
    "Allagan_Tomestone_Of_Esoterics": "Esoterics",
    "Allagan_Tomestone_Of_Law": "Law",
    "Allagan_Tomestone_Of_Soldiery": "Soldiery",
    "Allagan_Tomestone_Of_Mythology": "Mythology",
    "Allagan_Tomestone_Of_Philosophy": "Philosophy",
    "Allagan_Tomestone_Of_Mnemosyne": "Mnemosyne",
    "Allagan_Tomestone_Of_Mathematics": "Mathematics",
    # Crystals - remove underscores
    "Fire_Shard": "Fire Shard", "Fire_Crystal": "Fire Crystal", "Fire_Cluster": "Fire Cluster",
    "Ice_Shard": "Ice Shard", "Ice_Crystal": "Ice Crystal", "Ice_Cluster": "Ice Cluster",
    "Wind_Shard": "Wind Shard", "Wind_Crystal": "Wind Crystal", "Wind_Cluster": "Wind Cluster",
    "Earth_Shard": "Earth Shard", "Earth_Crystal": "Earth Crystal", "Earth_Cluster": "Earth Cluster",
    "Lightning_Shard": "Lightning Shard", "Lightning_Crystal": "Lightning Crystal", "Lightning_Cluster": "Lightning Cluster",
    "Water_Shard": "Water Shard", "Water_Crystal": "Water Crystal", "Water_Cluster": "Water Cluster",
    # Common - clean up underscores
    "Bicolor_Gemstone": "Bicolor Gemstone",
    # Battle
    "Wolf_Mark": "Wolf Marks", "Trophy_Crystal": "Trophy Crystal", "Allied_Seal": "Allied Seals",
    "Centurio_Seal": "Centurio Seals", "Sack_Of_Nuts": "Sack of Nuts", "Faux_Leaf": "Faux Leaves",
    "Bozjan_Cluster": "Bozjan Clusters", "Flame_Seal": "Flame Seals", "Serpent_Seal": "Serpent Seals",
    "Storm_Seal": "Storm Seals", "Achievement_Certificate": "Achievement Cert",
    # Societies
    "Fae_Fancy": "Fae Fancy", "Hammered_Frogment": "Hammered Frogment", "Carved_Kupo_Nut": "Carved Kupo Nut",
    "Loporrit_Carat": "Loporrit Carat", "Omicron_Omnitoken": "Omicron Omnitoken",
    "Seafarer's_Cowrie": "Seafarer's Cowrie", "Ananta_Dreamstaff": "Ananta Dreamstaff",
    "Arkasodara_Pana": "Arkasodara Pana", "Black_Copper_Gil": "Black Copper Gil",
    "Kojin_Sango": "Kojin Sango", "Namazu_Koban": "Namazu Koban", "Pixie_Locket": "Pixie Locket",
    "Qitari_Compliment": "Qitari Compliment", "Steel_Amalj'ok": "Steel Amalj'ok",
    "Sylphic_Goldleaf": "Sylphic Goldleaf", "Titan_Cobaltpiece": "Titan Cobaltpiece",
    "Tribal_Quest_Allowance": "Tribal Allowance",
}


def get_currency_display_name(currency_name):
    """Get shortened display name for a currency"""
    if currency_name in CURRENCY_SHORT_NAMES:
        return CURRENCY_SHORT_NAMES[currency_name]
    # Fallback: replace underscores with spaces
    return currency_name.replace("_", " ")


def categorize_currencies(currencies_dict):
    """
    Categorize currencies into groups for display.
    Returns dict with:
      - 'crystal_grid': dict of element -> {'Shard': val, 'Crystal': val, 'Cluster': val}
      - 'categories': dict of category -> [(display_name, value), ...]
    """
    # Crystal elements in display order
    CRYSTAL_ELEMENTS = ["Fire", "Ice", "Wind", "Earth", "Lightning", "Water"]
    
    # Build crystal grid: element -> {type: value}
    crystal_grid = {elem: {"Shard": 0, "Crystal": 0, "Cluster": 0} for elem in CRYSTAL_ELEMENTS}
    
    # Other categories
    categorized = {
        "Common": [],
        "Tomestones": [],
        "Battle": [],
        "Societies": [],
        "Other": [],
    }
    
    for curr_name, curr_value in currencies_dict.items():
        # Check if it's a crystal
        is_crystal = False
        for elem in CRYSTAL_ELEMENTS:
            if curr_name.startswith(elem + "_"):
                is_crystal = True
                if curr_name.endswith("_Shard"):
                    crystal_grid[elem]["Shard"] = curr_value
                elif curr_name.endswith("_Crystal"):
                    crystal_grid[elem]["Crystal"] = curr_value
                elif curr_name.endswith("_Cluster"):
                    crystal_grid[elem]["Cluster"] = curr_value
                break
        
        if is_crystal:
            continue
        
        # Check other categories
        display_name = get_currency_display_name(curr_name)
        found_category = False
        
        for cat_name, cat_currencies in CURRENCY_CATEGORIES.items():
            if cat_name == "Crystals":
                continue  # Already handled
            if curr_name in cat_currencies:
                categorized[cat_name].append((display_name, curr_value))
                found_category = True
                break
        
        if not found_category:
            categorized["Other"].append((display_name, curr_value))
    
    # Sort each category alphabetically by display name
    for cat_name in categorized:
        categorized[cat_name].sort(key=lambda x: x[0])
    
    # Check if character has any crystals
    has_crystals = any(
        crystal_grid[elem][t] > 0 
        for elem in CRYSTAL_ELEMENTS 
        for t in ["Shard", "Crystal", "Cluster"]
    )
    
    return {
        "crystal_grid": crystal_grid if has_crystals else None,
        "crystal_elements": CRYSTAL_ELEMENTS,
        "categories": {k: v for k, v in categorized.items() if v}
    }


# ===============================================
# Residential District Mapping (Lifestream)
# ===============================================
RESIDENTIAL_DISTRICTS = {
    8: "Mist",
    9: "Goblet",
    2: "Lavender Beds",
    70: "Empyreum",
    111: "Shirogane"
}

DISTRICT_ABBREV = {
    "Mist": "Mist",
    "Goblet": "Goblet",
    "Lavender Beds": "LB",
    "Empyreum": "Empyreum",
    "Shirogane": "Shirogane"
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
                if cid not in housing_map:
                    housing_map[cid] = {'private': None, 'fc': None}
                
                ward = entry.get('Ward')
                plot = entry.get('Plot')
                if ward is not None:
                    ward = ward + 1
                if plot is not None:
                    plot = plot + 1
                
                district_id = entry.get('ResidentialDistrict')
                district_name = RESIDENTIAL_DISTRICTS.get(district_id, "")
                district_abbrev = DISTRICT_ABBREV.get(district_name, "")
                
                is_private = entry.get('IsPrivate', False)
                
                if is_private:
                    housing_map[cid]['private'] = {'ward': ward, 'plot': plot, 'district': district_abbrev}
                else:
                    housing_map[cid]['fc'] = {'ward': ward, 'plot': plot, 'district': district_abbrev}
        
        return housing_map
    except Exception as e:
        print(f"[WARNING] Failed to load Lifestream data from '{lifestream_path}': {e}")
        return {}


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

@app.template_filter('sp_compact')
def sp_compact_filter(value):
    """Compact number: 404288500 -> 404.2m, 1155110 -> 1,155k, 32000 -> 32k, 1500 -> 1.5k, 872 -> 872"""
    try:
        n = int(value)
    except (TypeError, ValueError):
        return str(value)
    if n >= 1_000_000_000:
        b = n / 1_000_000_000
        return f"{b:,.1f}b".replace('.0b', 'b')
    elif n >= 1_000_000:
        m = n / 1_000_000
        return f"{m:,.1f}m".replace('.0m', 'm')
    elif n >= 10000:
        return f"{n // 1000:,}k"
    elif n >= 1000:
        k = n / 1000
        return f"{k:.1f}k".replace('.0k', 'k')
    return str(n)

# ===============================================
# Data Parsing Functions
# ===============================================
def load_external_config():
    """Load external config file if it exists"""
    global HOST, PORT, DEBUG, AUTO_REFRESH, account_locations
    global submarine_plans, retainer_plans, item_values
    global SHOW_CLASSES, SHOW_CURRENCIES, SHOW_MSQ_PROGRESSION, DEFAULT_THEME
    global HIGHLIGHT_IDLE_RETAINERS, HIGHLIGHT_IDLE_SUBS, HIGHLIGHT_READY_ITEMS, HIGHLIGHT_MAX_MB, HIGHLIGHT_POTENTIAL_RETAINER, HIGHLIGHT_POTENTIAL_SUBS
    global HONOR_AR_EXCLUSIONS
    global HIGHLIGHT_COLOR_IDLE_RETAINERS, HIGHLIGHT_COLOR_IDLE_SUBS, HIGHLIGHT_COLOR_MAX_MB, HIGHLIGHT_COLOR_POTENTIAL_RETAINER, HIGHLIGHT_COLOR_POTENTIAL_SUBS
    global BUILD_GIL_RATES, BUILD_CONSUMPTION_RATES
    global CERULEUM_TANK_COST, REPAIR_KIT_COST
    
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
        SHOW_CLASSES = config.get("SHOW_CLASSES", SHOW_CLASSES)
        SHOW_CURRENCIES = config.get("SHOW_CURRENCIES", SHOW_CURRENCIES)
        SHOW_MSQ_PROGRESSION = config.get("SHOW_MSQ_PROGRESSION", SHOW_MSQ_PROGRESSION)
        DEFAULT_THEME = config.get("DEFAULT_THEME", DEFAULT_THEME)
        HIGHLIGHT_IDLE_RETAINERS = config.get("HIGHLIGHT_IDLE_RETAINERS", HIGHLIGHT_IDLE_RETAINERS)
        HIGHLIGHT_IDLE_SUBS = config.get("HIGHLIGHT_IDLE_SUBS", HIGHLIGHT_IDLE_SUBS)
        HIGHLIGHT_READY_ITEMS = config.get("HIGHLIGHT_READY_ITEMS", HIGHLIGHT_READY_ITEMS)
        HIGHLIGHT_MAX_MB = config.get("HIGHLIGHT_MAX_MB", HIGHLIGHT_MAX_MB)
        HIGHLIGHT_POTENTIAL_RETAINER = config.get("HIGHLIGHT_POTENTIAL_RETAINER", HIGHLIGHT_POTENTIAL_RETAINER)
        HIGHLIGHT_POTENTIAL_SUBS = config.get("HIGHLIGHT_POTENTIAL_SUBS", HIGHLIGHT_POTENTIAL_SUBS)
        HONOR_AR_EXCLUSIONS = config.get("HONOR_AR_EXCLUSIONS", HONOR_AR_EXCLUSIONS)
        
        # Load custom highlight colors
        HIGHLIGHT_COLOR_IDLE_RETAINERS = config.get("HIGHLIGHT_COLOR_IDLE_RETAINERS", HIGHLIGHT_COLOR_IDLE_RETAINERS)
        HIGHLIGHT_COLOR_IDLE_SUBS = config.get("HIGHLIGHT_COLOR_IDLE_SUBS", HIGHLIGHT_COLOR_IDLE_SUBS)
        HIGHLIGHT_COLOR_MAX_MB = config.get("HIGHLIGHT_COLOR_MAX_MB", HIGHLIGHT_COLOR_MAX_MB)
        HIGHLIGHT_COLOR_POTENTIAL_RETAINER = config.get("HIGHLIGHT_COLOR_POTENTIAL_RETAINER", HIGHLIGHT_COLOR_POTENTIAL_RETAINER)
        HIGHLIGHT_COLOR_POTENTIAL_SUBS = config.get("HIGHLIGHT_COLOR_POTENTIAL_SUBS", HIGHLIGHT_COLOR_POTENTIAL_SUBS)
        
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
        
        # Load custom build rates (optional - merges with built-in rates)
        if "build_gil_rates" in config:
            BUILD_GIL_RATES.update(config["build_gil_rates"])
            print(f"[CONFIG] Loaded {len(config['build_gil_rates'])} custom build gil rates")
        if "build_consumption_rates" in config:
            BUILD_CONSUMPTION_RATES.update(config["build_consumption_rates"])
            print(f"[CONFIG] Loaded {len(config['build_consumption_rates'])} custom build consumption rates")
        
        # Load supply cost overrides (optional)
        if "ceruleum_tank_cost" in config:
            CERULEUM_TANK_COST = config["ceruleum_tank_cost"]
        if "repair_kit_cost" in config:
            REPAIR_KIT_COST = config["repair_kit_cost"]
        
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


# ===============================================
# MSQ Quest Tracking - Chronological Quest List with Names
# ===============================================
# Complete MSQ quest data in CHRONOLOGICAL ORDER (955 trackable quests)
# Format: (quest_id, quest_name) tuples
# Progress is calculated by finding the HIGHEST position MSQ quest the character has
# This approach works even if Altoholic only tracks partial quest history
#
# https://raw.githubusercontent.com/Sohtoren/Altoholic/refs/heads/main/Altoholic/Models/QuestIds.cs
# Note: ~40 quests from quests.txt are not in quest_cache.json and cannot be tracked
# Total expected MSQ: ~993 | Trackable: 955 (938 base + 17 patch 7.x)
#
# Covers: ARR -> Seventh Astral Era -> Heavensward -> Dragonsong War ->
#         Stormblood -> Post-Ala Mhigan -> Shadowbringers -> Endwalker ->
#         Newfound Adventure -> Dawntrail -> Crossroads -> Into the Mist
MSQ_QUEST_DATA = [
    (66060, "The Ultimate Weapon"),
    (66729, "Build on the Stone"),
    (66899, "Through the Maelstrom"),
    (66996, "Brave New Companions"),
    (65625, "Let Us Cling Together"),
    (65965, "In Memory of Moenbryda"),
    (65964, "Before the Dawn"),
    (67205, "Heavensward"),
    (67699, "As Goes Light, So Goes Darkness"),
    (67777, "Causes and Costs"),
    (67783, "Litany of Peace"),
    (67886, "An Ending to Mark a New Beginning"),
    (67891, "Louisoix's Finest Student"),
    (67895, "The Far Edge of Fate"),
    (68089, "Stormblood"),
    (68508, "Return of the Bull"),
    (68565, "Rise of a New Sun"),
    (68612, "Emissary of the Dawn"),
    (68685, "Prelude in Violet"),
    (68719, "The Face of War"),
    (68721, "A Requiem for Heroes"),
    (69190, "Shadowbringers"),
    (69218, "Vows of Virtue, Deeds of Cruelty"),
    (69306, "Echoes of a Fallen Star"),
    (69318, "Reflections in Crystal"),
    (69552, "Futures Rewritten"),
    (69599, "When the Dust Settles"),
    (69602, "Death Unto Dawn"),
    (70000, "Endwalker"),
    (70062, "A Satrap's Duty"),
    (70136, "Buried Memory"),
    (70214, "Gods Revel, Lands Tremble"),
    (70279, "The Dark Throne"),
    (70286, "Growing Light"),
    (70289, "The Coming Dawn"),
    (70495, "Dawntrail"),
    (70786, "Crossroads"),
    (70842, "Seekers of Eternity"),
    (70909, "The Promise of Tomorrow"),
    (70970, "The Mist"),
]
# Total: 40 MSQ milestone quests (ARR through Patch 7.x)

# Build lookup maps for O(1) access
MSQ_POSITION_MAP = {qid: pos for pos, (qid, name) in enumerate(MSQ_QUEST_DATA, 1)}
MSQ_NAME_MAP = {qid: name for qid, name in MSQ_QUEST_DATA}

# Load quest level requirements from cache (for validation)
MSQ_LEVEL_MAP = {}
try:
    import json as _json
    _cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quest_cache.json')
    if os.path.exists(_cache_path):
        with open(_cache_path, 'r', encoding='utf-8') as _f:
            _cache = _json.load(_f)
            for qid, _ in MSQ_QUEST_DATA:
                _quest = _cache.get(str(qid), {})
                MSQ_LEVEL_MAP[qid] = _quest.get('class_level', 0)
except Exception:
    pass


def calculate_msq_progress(quest_ids, max_job_level=100):
    """
    Calculate MSQ progress by finding the HIGHEST chronological position
    of any MSQ quest the character has tracked.
    
    This works even if Altoholic only tracks partial quest history -
    we just need ONE MSQ quest to determine where they are in the story.
    
    Args:
        quest_ids: List of completed quest IDs
        max_job_level: Character's highest job level (for validation)
    
    Returns: (percentage, highest_position, total_count, quest_name)
    """
    if not quest_ids:
        return 0, 0, 0, ""
    
    total_msq = len(MSQ_QUEST_DATA)
    if total_msq == 0:
        return 0, 0, 0, ""
    
    # Find the highest MSQ position from the character's quests
    # Only count quests where character's level meets the requirement
    highest_pos = 0
    highest_name = ""
    for qid in quest_ids:
        pos = MSQ_POSITION_MAP.get(qid, 0)
        if pos > 0:
            # Validate: character must be high enough level for this quest
            required_level = MSQ_LEVEL_MAP.get(qid, 0)
            if required_level > 0 and max_job_level < required_level:
                continue  # Skip - character can't have done this quest
            if pos > highest_pos:
                highest_pos = pos
                highest_name = MSQ_NAME_MAP.get(qid, "Unknown")
    
    if highest_pos == 0:
        return 0, 0, total_msq, ""
    
    percentage = round((highest_pos / total_msq) * 100, 1)
    return percentage, highest_pos, total_msq, highest_name


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
            "SELECT CharacterId, Inventory, Saddle, ArmoryInventory, Retainers, Jobs, Currencies, Quests, LastJob, LastJobLevel FROM characters"
        ).fetchall()
        
        for char_id, inv_json, saddle_json, armory_json, retainers_json, jobs_json, currencies_json, quests_json, last_job_id, last_job_level in rows:
            treasure_value = 0
            coffer_dye_value = 0
            coffer_count = 0
            dye_count = 0
            dye_pure_white = 0
            dye_jet_black = 0
            dye_pastel_pink = 0
            mb_dye_count = 0  # Dyes on marketboard
            venture_coins = 0
            
            def consume(items, is_marketboard=False):
                nonlocal treasure_value, coffer_dye_value, coffer_count, dye_count, dye_pure_white, dye_jet_black, dye_pastel_pink, mb_dye_count
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
                            dye_pure_white += qty
                            if is_marketboard:
                                mb_dye_count += qty
                        elif iid == 13115:  # Jet Black Dye
                            coffer_dye_value += qty * item_values.get("jet_black_dye", COFFER_DYE_VALUES[iid])
                            dye_count += qty
                            dye_jet_black += qty
                            if is_marketboard:
                                mb_dye_count += qty
                        elif iid == 13708:  # Pastel Pink Dye
                            coffer_dye_value += qty * item_values.get("pastel_pink_dye", COFFER_DYE_VALUES[iid])
                            dye_count += qty
                            dye_pastel_pink += qty
                            if is_marketboard:
                                mb_dye_count += qty
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
            
            # Process Retainers inventories (both Inventory and MarketInventory)
            retainers = _safe_json_load(retainers_json)
            if isinstance(retainers, list):
                for retainer in retainers:
                    if isinstance(retainer, dict):
                        ret_inv = retainer.get("Inventory", [])
                        if isinstance(ret_inv, list):
                            consume(ret_inv)
                        # Also check MarketInventory (items listed on marketboard)
                        ret_market_inv = retainer.get("MarketInventory", [])
                        if isinstance(ret_market_inv, list):
                            consume(ret_market_inv, is_marketboard=True)
            
            # Use LastJob and LastJobLevel for current class (last played job)
            current_job = CLASSJOB_ID_TO_ABBR.get(last_job_id, "") if last_job_id else ""
            current_level = int(last_job_level) if last_job_level else 0
            
            # Parse Jobs to find highest/lowest level jobs and all job levels
            highest_job = ""
            highest_level = 0
            lowest_job = ""
            lowest_level = 999  # Start high to find minimum
            all_jobs = {}  # Store all job levels
            jobs = _safe_json_load(jobs_json)
            if isinstance(jobs, dict):
                for job_name, job_data in jobs.items():
                    if isinstance(job_data, dict):
                        level = job_data.get("Level", 0)
                        if isinstance(level, int) and level > 0:
                            all_jobs[job_name] = level
                            # Track lowest level job (must be > 0)
                            if level < lowest_level:
                                lowest_level = level
                                lowest_job = JOB_ABBREVIATIONS.get(job_name, job_name[:3].upper())
                        if level > highest_level:
                            highest_level = level
                            highest_job = JOB_ABBREVIATIONS.get(job_name, job_name[:3].upper())
            # Reset lowest if no jobs found
            if lowest_level == 999:
                lowest_level = 0
                lowest_job = ""
            
            # Parse Currencies to get Venture coins and all currencies
            all_currencies = {}
            currencies = _safe_json_load(currencies_json)
            if isinstance(currencies, dict):
                venture_coins = currencies.get("Venture", 0)
                if not isinstance(venture_coins, int):
                    try:
                        venture_coins = int(venture_coins)
                    except Exception:
                        venture_coins = 0
                # Capture all currencies with values > 0
                for curr_name, curr_value in currencies.items():
                    if isinstance(curr_value, int) and curr_value > 0:
                        all_currencies[curr_name] = curr_value
                    elif curr_value:
                        try:
                            val = int(curr_value)
                            if val > 0:
                                all_currencies[curr_name] = val
                        except Exception:
                            pass
            
            # Parse Quests to get completed quest IDs
            completed_quests = []
            quests = _safe_json_load(quests_json)
            if isinstance(quests, list):
                completed_quests = [int(q) for q in quests if isinstance(q, (int, str))]
            
            result[int(char_id)] = {
                "treasure_value": int(treasure_value),
                "coffer_dye_value": int(coffer_dye_value),
                "coffer_count": int(coffer_count),
                "dye_count": int(dye_count),
                "dye_pure_white": int(dye_pure_white),
                "dye_jet_black": int(dye_jet_black),
                "dye_pastel_pink": int(dye_pastel_pink),
                "mb_dye_count": int(mb_dye_count),
                "venture_coins": int(venture_coins),
                "current_job": current_job,
                "current_level": current_level,
                "highest_job": highest_job,
                "highest_level": highest_level,
                "lowest_job": lowest_job,
                "lowest_level": lowest_level,
                "all_jobs": all_jobs,
                "all_currencies": all_currencies,
                "completed_quests": completed_quests,
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
    total_mb_dye_count = 0
    total_venture_coins = 0
    total_fc_points = 0
    total_subs_leveling = 0
    total_subs_farming = 0
    total_idle_subs = 0
    total_retainers_leveling = 0
    total_retainers_farming = 0
    total_idle_retainers = 0
    total_excluded_retainers = 0
    total_excluded_subs = 0
    total_sleeping_retainers = 0
    total_sleeping_subs = 0
    total_potential_subs = 0  # Characters with potential subs (lv 25+ not in FC)
    total_enabled_retainers = 0  # Enabled retainers (not excluded, not sleeping)
    total_enabled_subs = 0  # Enabled subs (not excluded, not sleeping)
    total_all_max_mb = 0  # Characters with ALL retainers maxed
    min_restock_days = None  # Track lowest restock days across all accounts (excluding 0)
    
    # Character stats tracking
    total_chars_lv25_plus = 0
    total_chars_lv100 = 0
    unique_personal_plots = set()  # Track unique plots by world+district+ward+plot
    unique_fc_plots = set()  # Track unique FC plots by world+district+ward+plot
    
    # MSQ Progress tracking
    total_characters_with_msq = 0
    msq_100_count = 0  # Characters at 100% MSQ
    msq_90_count = 0   # Characters at 90%+ MSQ
    msq_50_count = 0   # Characters at 50%+ MSQ
    total_msq_percent = 0  # For calculating average
    
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
            "total_mb_dye_count": 0,
            "total_venture_coins": 0,
            "total_fc_points": 0,
            "subs_leveling": 0,
            "subs_farming": 0,
            "idle_subs": 0,
            "has_idle_sub": False,
            "retainers_leveling": 0,
            "retainers_farming": 0,
            "idle_retainers": 0,
            "has_idle_retainer": False,
            "msq_100_count": 0,
            "msq_90_count": 0,
            "msq_50_count": 0,
            "characters_with_msq": 0,
            "has_max_mb_retainer": False,  # Track if any character has ALL retainers with 20 MB items
            "max_mb_retainer_count": 0,  # Count of retainers with 20 MB items
            "all_max_mb_count": 0,  # Count of characters with ALL retainers maxed
            "excluded_retainers": 0,  # Count of excluded retainers
            "excluded_subs": 0,  # Count of excluded submarines
            "sleeping_retainers": 0,  # Count of sleeping (disabled) retainers
            "sleeping_subs": 0,  # Count of sleeping (disabled) submarines
            "has_sleeping_retainer": False,
            "has_sleeping_sub": False,
            "potential_subs_count": 0,  # Count of characters with potential subs (lv 25+ not in FC)
            "enabled_retainers": 0,  # Count of enabled retainers (not excluded, not sleeping)
            "enabled_subs": 0,  # Count of enabled subs (not excluded, not sleeping)
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
        
        # Load Lifestream housing data
        housing_map = {}
        lfstrm_path = account.get("lfstrm_path", "")
        if lfstrm_path:
            housing_map = load_lifestream_data(lfstrm_path)
        
        for char in characters:
            cid = char.get("CID", 0)
            char_gil = char.get("Gil", 0)
            
            # Check AR exclusion settings for this character
            exclude_retainer = char.get("ExcludeRetainer", False) if HONOR_AR_EXCLUSIONS else False
            exclude_workshop = char.get("ExcludeWorkshop", False) if HONOR_AR_EXCLUSIONS else False
            
            # Check AR enabled/disabled (sleeping) settings for this character
            # Enabled=false means retainers are sleeping (not rotating)
            # WorkshopEnabled=false means subs are sleeping (not rotating)
            retainers_sleeping = not char.get("Enabled", True)  # Default True = enabled
            subs_sleeping = not char.get("WorkshopEnabled", True)  # Default True = enabled
            
            # Parse submarines (always parse, but hide in display if excluded)
            submarines = parse_submarine_data(char)
            sub_daily_income = sum(s["daily_gil"] for s in submarines) if not exclude_workshop else 0
            sub_daily_cost = sum(s["daily_cost"] for s in submarines) if not exclude_workshop else 0
            
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
            
            # Count idle submarines (no plan, not leveling, not farming)
            char_idle_subs = sum(1 for s in submarines if not s.get("plan_name") and not s.get("is_farming", False) and not s.get("is_leveling", False))
            # Idle sub = has idle subs AND not excluded AND not sleeping (must be enabled)
            has_idle_sub = char_idle_subs > 0 and not exclude_workshop and not subs_sleeping
            
            # Parse retainers (always parse, but hide in display if excluded)
            retainers = parse_retainer_data(char)
            retainer_gil = sum(r["gil"] for r in retainers) if not exclude_retainer else 0
            mb_items = sum(r["mb_items"] for r in retainers) if not exclude_retainer else 0
            # Override max MB highlight if excluded
            # Only highlight if ALL retainers have max MB items (20)
            has_max_mb_retainer = len(retainers) > 0 and all(r["mb_items"] >= 20 for r in retainers) and not exclude_retainer
            # Count retainers with max MB items (for summary)
            char_max_mb_count = sum(1 for r in retainers if r["mb_items"] >= 20) if not exclude_retainer else 0
            
            # Count leveling vs farming retainers (< 100 = leveling, 100 = farming)
            char_retainers_leveling = sum(1 for r in retainers if r["level"] < 100)
            char_retainers_farming = sum(1 for r in retainers if r["level"] >= 100)
            
            # Count idle retainers (no venture assigned)
            char_idle_retainers = sum(1 for r in retainers if not r["has_venture"])
            # Idle retainer = has idle retainers AND not excluded AND not sleeping (must be enabled)
            has_idle_retainer = char_idle_retainers > 0 and not exclude_retainer and not retainers_sleeping
            
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
            dye_pure_white = 0
            dye_jet_black = 0
            dye_pastel_pink = 0
            mb_dye_count = 0
            venture_coins = 0
            current_job = ""
            current_level = 0
            highest_job = ""
            highest_level = 0
            lowest_job = ""
            lowest_level = 0
            all_jobs = {}
            all_currencies = {}
            completed_quests = []
            if cid in alto_map:
                treasure_value = alto_map[cid].get("treasure_value", 0)
                coffer_dye_value = alto_map[cid].get("coffer_dye_value", 0)
                coffer_count = alto_map[cid].get("coffer_count", 0)
                dye_count = alto_map[cid].get("dye_count", 0)
                dye_pure_white = alto_map[cid].get("dye_pure_white", 0)
                dye_jet_black = alto_map[cid].get("dye_jet_black", 0)
                dye_pastel_pink = alto_map[cid].get("dye_pastel_pink", 0)
                mb_dye_count = alto_map[cid].get("mb_dye_count", 0)
                venture_coins = alto_map[cid].get("venture_coins", 0)
                current_job = alto_map[cid].get("current_job", "")
                current_level = alto_map[cid].get("current_level", 0)
                highest_job = alto_map[cid].get("highest_job", "")
                highest_level = alto_map[cid].get("highest_level", 0)
                lowest_job = alto_map[cid].get("lowest_job", "")
                lowest_level = alto_map[cid].get("lowest_level", 0)
                all_jobs = alto_map[cid].get("all_jobs", {})
                all_currencies = alto_map[cid].get("all_currencies", {})
                completed_quests = alto_map[cid].get("completed_quests", [])
            
            # Get venture coffers from AutoRetainer if Altoholic doesn't have it
            venture_coffers_ar = char.get("VentureCoffers", 0)
            if coffer_count == 0 and venture_coffers_ar > 0:
                coffer_count = venture_coffers_ar
                coffer_dye_value += venture_coffers_ar * COFFER_DYE_VALUES.get(32161, 18000)
            
            # Get housing data from Lifestream
            private_house = None
            fc_house = None
            if cid in housing_map:
                private_data = housing_map[cid].get('private')
                fc_data_house = housing_map[cid].get('fc')
                if private_data:
                    private_house = f"{private_data['district']} W{private_data['ward']} P{private_data['plot']}"
                if fc_data_house:
                    fc_house = f"{fc_data_house['district']} W{fc_data_house['ward']} P{fc_data_house['plot']}"
            
            char_data = {
                "cid": cid,
                "name": char.get("Name", "Unknown"),
                "world": char.get("World", "Unknown"),
                "region": region_from_world(char.get("World", "")),
                "gil": char_gil,
                "retainer_gil": retainer_gil,
                "total_gil": char_gil + retainer_gil,
                "treasure_value": treasure_value,
                "coffer_dye_value": coffer_dye_value,
                "coffer_count": coffer_count,
                "dye_count": dye_count,
                "dye_pure_white": dye_pure_white,
                "dye_jet_black": dye_jet_black,
                "dye_pastel_pink": dye_pastel_pink,
                "mb_dye_count": mb_dye_count,
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
                "idle_subs": char_idle_subs,
                "has_idle_sub": has_idle_sub,
                "retainers_leveling": char_retainers_leveling,
                "retainers_farming": char_retainers_farming,
                "idle_retainers": char_idle_retainers,
                "has_idle_retainer": has_idle_retainer,
                "days_until_restock": days_until_restock,
                "private_house": private_house,
                "fc_house": fc_house,
                "all_jobs": all_jobs,
                "all_currencies": all_currencies,
                "categorized_currencies": categorize_currencies(all_currencies) if all_currencies else {},
            }
            
            # Add highest/lowest job (already extracted from alto_map)
            char_data["highest_job"] = highest_job
            char_data["highest_level"] = highest_level
            char_data["lowest_job"] = lowest_job
            char_data["lowest_level"] = lowest_level
            
            # Calculate MSQ progress (returns percentage, position, total, quest_name)
            # Get max COMBAT job level for validation (MSQ requires combat jobs, not crafters)
            max_combat_level = max((lv for job, lv in all_jobs.items() if job in COMBAT_JOBS), default=0) if all_jobs else 0
            # Fallback to current_level only if it's a combat job
            if max_combat_level == 0 and current_job in COMBAT_JOBS:
                max_combat_level = current_level
            msq_pct, msq_pos, msq_total, msq_quest_name = calculate_msq_progress(completed_quests, max_combat_level)
            char_data["msq_percent"] = msq_pct
            char_data["msq_completed"] = msq_pos
            char_data["msq_total"] = msq_total
            char_data["msq_quest_name"] = msq_quest_name
            
            # Count ready submarines and retainers
            char_ready_subs = sum(1 for s in submarines if s["is_ready"])
            char_ready_retainers = sum(1 for r in retainers if r["is_ready"])
            
            # Get max levels for sorting
            max_retainer_level = max((r["level"] for r in retainers), default=0)
            max_sub_level = max((s["level"] for s in submarines), default=0)
            # Get min levels for sorting (lowest level sub/retainer)
            min_retainer_level = min((r["level"] for r in retainers), default=0)
            min_sub_level = min((s["level"] for s in submarines), default=0)
            
            # Get minimum return time in seconds for sorting (soonest return first)
            # For ready items, use 0 (already ready). For non-ready, use seconds until return.
            # VentureEndsAt and ReturnTime are Unix timestamps (integers)
            now_ts = datetime.datetime.now().timestamp()
            retainer_return_times = []
            for r in retainers:
                if r["is_ready"]:
                    retainer_return_times.append(0)
                elif r["venture_ends"] and r["venture_ends"] > 0:
                    # venture_ends is Unix timestamp, subtract current timestamp
                    delta = r["venture_ends"] - now_ts
                    retainer_return_times.append(max(0, delta))
                else:
                    retainer_return_times.append(999999)  # No venture = sort last
            min_retainer_return = min(retainer_return_times) if retainer_return_times else 999999
            
            sub_return_times = []
            for s in submarines:
                if s["is_ready"]:
                    sub_return_times.append(0)
                elif s["return_time"] and s["return_time"] > 0:
                    # return_time is Unix timestamp, subtract current timestamp
                    delta = s["return_time"] - now_ts
                    sub_return_times.append(max(0, delta))
                else:
                    sub_return_times.append(999999)  # No voyage = sort last
            min_sub_return = min(sub_return_times) if sub_return_times else 999999
            
            # Add ready counts and max levels to character data
            char_data["ready_subs"] = char_ready_subs
            char_data["total_subs"] = len(submarines)
            char_data["ready_retainers"] = char_ready_retainers
            char_data["total_retainers"] = len(retainers)
            char_data["max_retainer_level"] = max_retainer_level
            char_data["max_sub_level"] = max_sub_level
            char_data["min_retainer_level"] = min_retainer_level
            char_data["min_sub_level"] = min_sub_level
            char_data["min_retainer_return"] = int(min_retainer_return)
            char_data["min_sub_return"] = int(min_sub_return)
            char_data["has_max_mb_retainer"] = has_max_mb_retainer
            
            # Add exclusion flags for template display
            char_data["exclude_retainer"] = exclude_retainer
            char_data["exclude_workshop"] = exclude_workshop
            
            # Add sleeping flags for template display
            char_data["retainers_sleeping"] = retainers_sleeping
            char_data["subs_sleeping"] = subs_sleeping
            # Add processing flag - character is processing if Enabled=true OR WorkshopEnabled=true
            char_data["is_processing"] = not retainers_sleeping or not subs_sleeping
            # Count sleeping retainers/subs for this character
            char_sleeping_retainers = len(retainers) if retainers_sleeping else 0
            char_sleeping_subs = len(submarines) if subs_sleeping else 0
            char_data["sleeping_retainer_count"] = char_sleeping_retainers
            char_data["sleeping_sub_count"] = char_sleeping_subs
            
            # Check if character has potential for retainers (MSQ 66060 completed but 0 retainers)
            # Override if retainers are excluded
            # Only set if SHOW_MSQ_PROGRESSION is enabled (otherwise we can't determine MSQ status)
            char_data["has_potential_retainer"] = SHOW_MSQ_PROGRESSION and (66060 in completed_quests) and (len(retainers) == 0) and not exclude_retainer
            
            # Check if character has potential for subs (Lv 25+ but not in FC)
            # Use highest_level to check if any job is 25+
            char_data["has_potential_subs"] = highest_level >= 25 and not fc_name
            
            # Track max MB count for this character
            char_data["max_mb_count"] = char_max_mb_count
            
            # Track idle flags for asterisk descriptions
            char_data["has_idle_retainer"] = has_idle_retainer
            char_data["has_idle_sub"] = has_idle_sub
            
            account_data["characters"].append(char_data)
            account_data["total_gil"] += char_data["total_gil"]
            # Don't count excluded subs/retainers in account totals
            account_data["total_subs"] += len(submarines) if not exclude_workshop else 0
            account_data["total_retainers"] += len(retainers) if not exclude_retainer else 0
            # Don't count sleeping or excluded subs/retainers as ready
            account_data["ready_subs"] += char_ready_subs if not exclude_workshop and not subs_sleeping else 0
            account_data["ready_retainers"] += char_ready_retainers if not exclude_retainer and not retainers_sleeping else 0
            # Track excluded counts
            if exclude_retainer and len(retainers) > 0:
                account_data["excluded_retainers"] += len(retainers)
            if exclude_workshop and len(submarines) > 0:
                account_data["excluded_subs"] += len(submarines)
            # Track sleeping counts (Enabled=false or WorkshopEnabled=false)
            # Don't count excluded retainers/subs in sleeping totals
            if char_sleeping_retainers > 0 and not exclude_retainer:
                account_data["sleeping_retainers"] += char_sleeping_retainers
                account_data["has_sleeping_retainer"] = True
            if char_sleeping_subs > 0 and not exclude_workshop:
                account_data["sleeping_subs"] += char_sleeping_subs
                account_data["has_sleeping_sub"] = True
            account_data["total_mb_items"] += mb_items
            account_data["total_treasure"] += treasure_value
            account_data["total_coffer_dye_value"] += coffer_dye_value
            account_data["total_coffer_count"] += coffer_count
            account_data["total_dye_count"] += dye_count
            account_data["total_mb_dye_count"] += mb_dye_count
            account_data["total_venture_coins"] += venture_coins
            account_data["total_fc_points"] += fc_points
            
            # Track minimum restock days (excluding 0 and None)
            if days_until_restock is not None and days_until_restock > 0:
                if min_restock_days is None or days_until_restock < min_restock_days:
                    min_restock_days = days_until_restock
            
            account_data["subs_leveling"] += char_subs_leveling
            account_data["subs_farming"] += char_subs_farming
            # Only count idle subs if not excluded AND not sleeping (must be enabled)
            if not exclude_workshop and not subs_sleeping:
                account_data["idle_subs"] += char_idle_subs
            if has_idle_sub:
                account_data["has_idle_sub"] = True
            account_data["retainers_leveling"] += char_retainers_leveling
            account_data["retainers_farming"] += char_retainers_farming
            # Only count idle retainers if not excluded AND not sleeping (must be enabled)
            if not exclude_retainer and not retainers_sleeping:
                account_data["idle_retainers"] += char_idle_retainers
            if has_idle_retainer:
                account_data["has_idle_retainer"] = True
            
            # Track max MB retainers (only when ALL retainers are maxed)
            if has_max_mb_retainer:
                account_data["has_max_mb_retainer"] = True
                account_data["all_max_mb_count"] += 1  # Count characters with ALL retainers maxed
            # Count individual retainers at max MB (for summary)
            account_data["max_mb_retainer_count"] += char_max_mb_count
            
            # Track potential subs (lv 25+ not in FC)
            if char_data["has_potential_subs"]:
                account_data["potential_subs_count"] += 1
            
            # Track enabled retainers/subs (not excluded, not sleeping)
            if not exclude_retainer and not retainers_sleeping:
                account_data["enabled_retainers"] += len(retainers)
            if not exclude_workshop and not subs_sleeping:
                account_data["enabled_subs"] += len(submarines)
            
            # Track MSQ progress stats
            if char_data["msq_percent"] > 0:
                account_data["characters_with_msq"] += 1
                total_characters_with_msq += 1
                total_msq_percent += char_data["msq_percent"]
                if char_data["msq_percent"] >= 100:
                    account_data["msq_100_count"] += 1
                    msq_100_count += 1
                if char_data["msq_percent"] >= 90:
                    account_data["msq_90_count"] += 1
                    msq_90_count += 1
                if char_data["msq_percent"] >= 50:
                    account_data["msq_50_count"] += 1
                    msq_50_count += 1
            
            # Track character level stats and housing plots
            if highest_level >= 25:
                total_chars_lv25_plus += 1
            if highest_level >= 100:
                total_chars_lv100 += 1
            # Track unique plots (world+location to avoid counting shared houses)
            char_world = char.get("World", "")
            if cid in housing_map:
                private_data = housing_map[cid].get('private')
                fc_data_house = housing_map[cid].get('fc')
                if private_data:
                    plot_key = f"{char_world}_{private_data['district']}_W{private_data['ward']}_P{private_data['plot']}"
                    unique_personal_plots.add(plot_key)
                if fc_data_house:
                    plot_key = f"{char_world}_{fc_data_house['district']}_W{fc_data_house['ward']}_P{fc_data_house['plot']}"
                    unique_fc_plots.add(plot_key)
            
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
        total_mb_dye_count += account_data["total_mb_dye_count"]
        total_venture_coins += account_data["total_venture_coins"]
        total_fc_points += account_data["total_fc_points"]
        total_subs_leveling += account_data["subs_leveling"]
        total_subs_farming += account_data["subs_farming"]
        total_idle_subs += account_data["idle_subs"]
        total_retainers_leveling += account_data["retainers_leveling"]
        total_retainers_farming += account_data["retainers_farming"]
        total_idle_retainers += account_data["idle_retainers"]
        total_excluded_retainers += account_data["excluded_retainers"]
        total_excluded_subs += account_data["excluded_subs"]
        total_sleeping_retainers += account_data["sleeping_retainers"]
        total_sleeping_subs += account_data["sleeping_subs"]
        total_potential_subs += account_data["potential_subs_count"]
        total_enabled_retainers += account_data["enabled_retainers"]
        total_enabled_subs += account_data["enabled_subs"]
        total_all_max_mb += account_data["all_max_mb_count"]
        
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
            "total_mb_dye_count": total_mb_dye_count,
            "total_venture_coins": total_venture_coins,
            "total_fc_points": total_fc_points,
            "subs_leveling": total_subs_leveling,
            "subs_farming": total_subs_farming,
            "idle_subs": total_idle_subs,
            "retainers_leveling": total_retainers_leveling,
            "retainers_farming": total_retainers_farming,
            "idle_retainers": total_idle_retainers,
            "excluded_retainers": total_excluded_retainers,
            "excluded_subs": total_excluded_subs,
            "sleeping_retainers": total_sleeping_retainers,
            "sleeping_subs": total_sleeping_subs,
            "potential_subs_count": total_potential_subs,
            "enabled_retainers": total_enabled_retainers,
            "enabled_subs": total_enabled_subs,
            "all_max_mb_count": total_all_max_mb,
            "daily_income": total_daily_income,
            "monthly_income": total_daily_income * 30,
            "annual_income": total_daily_income * 365,
            "daily_cost": total_daily_cost,
            "monthly_cost": total_daily_cost * 30,
            "daily_profit": total_daily_income - total_daily_cost,
            "monthly_profit": (total_daily_income - total_daily_cost) * 30,
            "annual_profit": (total_daily_income - total_daily_cost) * 365,
            "min_restock_days": min_restock_days,
            # MSQ Progress stats
            "msq_100_count": msq_100_count,
            "msq_90_count": msq_90_count,
            "msq_50_count": msq_50_count,
            "characters_with_msq": total_characters_with_msq,
            "msq_avg_percent": round(total_msq_percent / total_characters_with_msq, 1) if total_characters_with_msq > 0 else 0,
            "msq_total_quests": len(MSQ_QUEST_DATA),
            "total_characters": sum(len(acc.get("characters", [])) for acc in all_accounts),
            # Character stats
            "chars_lv25_plus": total_chars_lv25_plus,
            "chars_lv100": total_chars_lv100,
            "personal_plots": len(unique_personal_plots),
            "fc_plots": len(unique_fc_plots),
            # Max MB retainer tracking
            "max_mb_retainer_count": sum(acc.get("max_mb_retainer_count", 0) for acc in all_accounts),
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
    <title>AutoRetainer Dashboard</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚓</text></svg>">
    <style>
        :root, [data-theme="default"] {
            --bg-primary: #1a1a2e;
            --bg-secondary: #16213e;
            --bg-card: #0f3460;
            --bg-hover: #1a4a7a;
            --text-primary: #e8e8e8;
            --text-secondary: #a0a0a0;
            --accent: #3a7aaa;
            --accent-light: #4a9aca;
            --accent-highlight: #e94560;
            --success: #00d26a;
            --warning: #ffc107;
            --border: #2a2a4a;
            --gold: #ffd700;
            --theme-btn: #3a7aaa;
        }
        
        [data-theme="dark-gray"] {
            --bg-primary: #1a1a1a;
            --bg-secondary: #252525;
            --bg-card: #2d2d2d;
            --bg-hover: #3a3a3a;
            --text-primary: #e8e8e8;
            --text-secondary: #a0a0a0;
            --accent: #808080;
            --accent-light: #a0a0a0;
            --success: #00d26a;
            --warning: #ffc107;
            --border: #404040;
            --gold: #ffd700;
            --theme-btn: #606060;
        }
        
        [data-theme="ocean-blue"] {
            --bg-primary: #0a1628;
            --bg-secondary: #0d1f3c;
            --bg-card: #132744;
            --bg-hover: #1a3a5c;
            --text-primary: #e8f4fc;
            --text-secondary: #8eb8d8;
            --accent: #00b4d8;
            --accent-light: #48cae4;
            --success: #00d26a;
            --warning: #ffc107;
            --border: #1e4976;
            --gold: #ffd700;
            --theme-btn: #0077b6;
        }
        
        [data-theme="forest-green"] {
            --bg-primary: #0d1f0d;
            --bg-secondary: #142814;
            --bg-card: #1a3a1a;
            --bg-hover: #2d5a2d;
            --text-primary: #e8f5e8;
            --text-secondary: #a0c8a0;
            --accent: #2ecc71;
            --accent-light: #58d68d;
            --success: #00d26a;
            --warning: #ffc107;
            --border: #2d5a2d;
            --gold: #ffd700;
            --theme-btn: #27ae60;
        }
        
        [data-theme="crimson-red"] {
            --bg-primary: #1a0a0a;
            --bg-secondary: #2d1414;
            --bg-card: #3d1a1a;
            --bg-hover: #5a2d2d;
            --text-primary: #f5e8e8;
            --text-secondary: #c8a0a0;
            --accent: #dc3545;
            --accent-light: #e74c5c;
            --success: #00d26a;
            --warning: #ffc107;
            --border: #5a2d2d;
            --gold: #ffd700;
            --theme-btn: #c82333;
        }
        
        [data-theme="purple-haze"] {
            --bg-primary: #1a0a2e;
            --bg-secondary: #251440;
            --bg-card: #2d1a4a;
            --bg-hover: #3d2a5a;
            --text-primary: #f0e8f8;
            --text-secondary: #b8a0d0;
            --accent: #9b59b6;
            --accent-light: #bb77d6;
            --success: #00d26a;
            --warning: #ffc107;
            --border: #4a2d6a;
            --gold: #ffd700;
            --theme-btn: #8e44ad;
        }
        
        [data-theme="dark-orange"] {
            --bg-primary: #1a1008;
            --bg-secondary: #2a1a0a;
            --bg-card: #3a2510;
            --bg-hover: #4a3520;
            --text-primary: #f8f0e8;
            --text-secondary: #d0b8a0;
            --accent: #e67e22;
            --accent-light: #f39c12;
            --success: #00d26a;
            --warning: #ffc107;
            --border: #5a4020;
            --gold: #ffd700;
            --theme-btn: #d35400;
        }
        
        [data-theme="pastel-pink"] {
            --bg-primary: #2e1a2a;
            --bg-secondary: #3d2538;
            --bg-card: #4a2d42;
            --bg-hover: #5a3d52;
            --text-primary: #fff0f5;
            --text-secondary: #e8c0d0;
            --accent: #ff69b4;
            --accent-light: #ffb6c1;
            --success: #00d26a;
            --warning: #ffc107;
            --border: #6a4d5a;
            --gold: #ffd700;
            --theme-btn: #ff1493;
        }
        
        [data-theme="brown"] {
            --bg-primary: #1a1410;
            --bg-secondary: #2a2018;
            --bg-card: #3a2d20;
            --bg-hover: #4a3d30;
            --text-primary: #f5f0e8;
            --text-secondary: #c8b8a0;
            --accent: #8b4513;
            --accent-light: #a0522d;
            --success: #00d26a;
            --warning: #ffc107;
            --border: #5a4a38;
            --gold: #ffd700;
            --theme-btn: #6b3410;
        }
        
        [data-theme="ultra-dark"] {
            --bg-primary: #0a0a0a;
            --bg-secondary: #0f0f0f;
            --bg-card: #141414;
            --bg-hover: #1a1a1a;
            --text-primary: #c0c0c0;
            --text-secondary: #808080;
            --accent: #404040;
            --accent-light: #505050;
            --success: #00d26a;
            --warning: #ffc107;
            --border: #252525;
            --gold: #ffd700;
            --theme-btn: #303030;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Sticky top section wrapper - height ~125px */
        .sticky-top-section {
            position: sticky;
            top: 0;
            z-index: 500;
            background: var(--bg-primary);
            padding-bottom: 8px;
            margin: -20px -20px 10px -20px;
            padding: 15px 20px 8px 20px;
        }
        
        header {
            background: var(--bg-card);
            padding: 12px 20px;
            border-radius: 10px;
            margin-bottom: 8px;
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
        
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .header-left {
            flex: 1;
        }
        
        .header-right {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 5px;
        }
        
        .search-container {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }
        
        .search-error {
            color: var(--danger);
            font-size: 0.85em;
            margin-bottom: 5px;
            display: none;
        }
        
        .search-error.visible {
            display: block;
        }
        
        .search-input {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 8px 12px;
            color: var(--text-primary);
            font-size: 0.9em;
            width: 200px;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        
        .search-input:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 8px rgba(0, 180, 216, 0.3);
        }
        
        .search-input::placeholder {
            color: var(--text-secondary);
        }
        
        .search-hidden {
            display: none !important;
        }
        
        /* Theme selector */
        .theme-selector {
            display: flex;
            gap: 4px;
            margin-top: 8px;
        }
        
        .global-filters {
            display: flex;
            gap: 4px;
            margin-top: 6px;
        }
        
        .theme-btn {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 2px solid transparent;
            cursor: pointer;
            transition: transform 0.2s, border-color 0.2s;
            font-size: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            line-height: 1;
        }
        
        .theme-btn:hover {
            transform: scale(1.15);
        }
        
        .theme-btn.active {
            /* No visual indicator for active theme */
        }
        
        .theme-btn[data-theme="default"] { background: linear-gradient(135deg, #1a1a2e, #3a7aaa); }
        .theme-btn[data-theme="ultra-dark"] { background: linear-gradient(135deg, #0a0a0a, #303030); }
        .theme-btn[data-theme="dark-gray"] { background: linear-gradient(135deg, #1a1a1a, #606060); }
        .theme-btn[data-theme="ocean-blue"] { background: linear-gradient(135deg, #0a1628, #00b4d8); }
        .theme-btn[data-theme="forest-green"] { background: linear-gradient(135deg, #0d1f0d, #2ecc71); }
        .theme-btn[data-theme="crimson-red"] { background: linear-gradient(135deg, #1a0a0a, #dc3545); }
        .theme-btn[data-theme="purple-haze"] { background: linear-gradient(135deg, #1a0a2e, #9b59b6); }
        .theme-btn[data-theme="pastel-pink"] { background: linear-gradient(135deg, #2e1a2a, #ff69b4); }
        .theme-btn[data-theme="dark-orange"] { background: linear-gradient(135deg, #1a1008, #e67e22); }
        .theme-btn[data-theme="brown"] { background: linear-gradient(135deg, #1a1410, #8b4513); }
        
        /* Loading overlay */
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--bg-primary);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            transition: opacity 0.5s ease;
        }
        
        .loading-overlay.hidden {
            opacity: 0;
            pointer-events: none;
        }
        
        .loading-text {
            color: var(--accent);
            font-size: 1.5em;
            margin-bottom: 20px;
        }
        
        .loading-subtext {
            color: var(--text-secondary);
            font-size: 0.9em;
            margin-bottom: 30px;
        }
        
        .progress-container {
            width: 300px;
            height: 8px;
            background: var(--bg-secondary);
            border-radius: 4px;
            overflow: hidden;
            border: 1px solid var(--border);
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--accent), #00d4ff);
            border-radius: 4px;
            animation: loading 2s ease-in-out infinite;
            width: 30%;
        }
        
        @keyframes loading {
            0% { transform: translateX(-100%); }
            50% { transform: translateX(250%); }
            100% { transform: translateX(-100%); }
        }
        
        .loading-hint {
            color: var(--text-secondary);
            font-size: 0.8em;
            margin-top: 15px;
            font-style: italic;
        }
        
        .summary-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 0;
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
        }
        
        .account-header {
            background: linear-gradient(90deg, var(--bg-card) 0%, var(--accent) 100%);
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            user-select: none;
            transition: opacity 0.2s;
            position: sticky;
            top: 115px;
            z-index: 400;
            border-radius: 12px 12px 0 0;
            overflow: hidden;
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
        
        .account-header.collapsed {
            border-radius: 12px;
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
            padding: 8px;
            margin-top: 5px;
            background: var(--bg-secondary);
            border-radius: 8px;
            align-items: center;
            position: sticky;
            top: 164px;
            z-index: 300;
        }
        
        .sort-bar.collapsed {
            display: none;
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
        
        .filter-btn {
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            padding: 3px 3px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 0.75em;
            transition: all 0.2s;
        }
        
        .filter-btn:hover {
            background: var(--border);
            color: var(--text-primary);
        }
        
        .filter-btn.active {
            background: var(--warning);
            color: white;
            border-color: var(--warning);
        }
        
        .region-btn {
            font-weight: bold;
            min-width: 32px;
            text-align: center;
        }
        
        .region-btn.active {
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }
        
        .character-card.filtered-hidden {
            display: none;
        }
        
        .character-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
            gap: 20px;
            padding: 20px;
            align-items: start;
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
        
        {% if highlight_ready_items %}
        .character-header.has-available {
            background: rgba(233, 69, 96, 0.25);
        }
        
        .character-header.has-available:hover {
            background: rgba(233, 69, 96, 0.35);
        }
        {% endif %}
        
        .account-stats .stat-ready {
            color: #000000 !important;
        }
        
        /* Max MB listings indicators */
        .account-stats .mb-max,
        .account-stats .mb-max span {
            color: var(--danger) !important;
            font-weight: 600;
        }
        
        {% if highlight_max_mb %}
        .character-card.has-max-mb {
            outline: 4px solid {{ highlight_color_max_mb }};
            outline-offset: -4px;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.7), inset 0 0 10px rgba(255, 215, 0, 0.2);
        }
        {% endif %}
        
        {% if highlight_idle_retainers %}
        .character-card.has-idle-retainer {
            outline: 4px solid {{ highlight_color_idle_retainers }};
            outline-offset: -4px;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.7), inset 0 0 10px rgba(0, 255, 255, 0.2);
        }
        {% endif %}
        
        {% if highlight_idle_subs %}
        .character-card.has-idle-sub {
            outline: 4px solid {{ highlight_color_idle_subs }};
            outline-offset: -4px;
            box-shadow: 0 0 20px rgba(255, 182, 193, 0.7), inset 0 0 10px rgba(255, 182, 193, 0.2);
        }
        {% endif %}
        
        {% if highlight_potential_retainer %}
        .character-card.has-potential-retainer {
            outline: 4px solid {{ highlight_color_potential_retainer }};
            outline-offset: -4px;
            box-shadow: 0 0 20px rgba(139, 69, 19, 0.7), inset 0 0 10px rgba(139, 69, 19, 0.2);
        }
        {% endif %}
        
        {% if highlight_potential_subs %}
        .character-card.has-potential-subs {
            outline: 4px solid {{ highlight_color_potential_subs }};
            outline-offset: -4px;
            box-shadow: 0 0 20px rgba(26, 26, 26, 0.7), inset 0 0 10px rgba(26, 26, 26, 0.2);
        }
        {% endif %}
        
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
            padding: 10px 15px;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
            font-size: 0.85em;
        }
        
        .character-body.collapsed {
            max-height: 0 !important;
            padding: 0 20px;
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 1px 0;
            border-bottom: 1px solid var(--border);
            align-items: flex-start;
        }
        
        .info-row:last-child {
            border-bottom: none;
        }
        
        .info-label {
            color: var(--text-secondary);
            flex-shrink: 0;
            margin-right: 10px;
        }
        
        .info-value {
            font-weight: 500;
            text-align: right;
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
            margin: 8px 0 5px 0;
            padding-bottom: 3px;
            border-bottom: 1px solid var(--accent);
        }
        
        .sub-table, .ret-table {
            width: 100%;
            font-size: 0.85em;
        }
        
        .sub-table th, .ret-table th {
            text-align: left;
            color: var(--text-secondary);
            padding: 3px 8px;
            font-weight: normal;
        }
        
        .sub-table td, .ret-table td {
            padding: 1px 8px;
        }
        
        .sub-table tr:nth-child(even), .ret-table tr:nth-child(even) {
            background: rgba(255, 255, 255, 0.03);
        }
        
        .job-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 10px 0;
        }
        
        .job-column {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        
        .job-category-title {
            font-size: 0.85em;
            color: var(--text-secondary);
            padding: 4px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 4px;
        }
        
        .job-row {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 2px 0;
            font-size: 0.85em;
        }
        
        .job-level {
            min-width: 28px;
            text-align: right;
            color: var(--gold);
            font-weight: bold;
        }
        
        .job-level-zero {
            color: var(--text-secondary);
            font-weight: normal;
        }
        
        .job-name {
            color: var(--text-primary);
        }
        
        .currency-section {
            padding: 3px 0 20px 0;
        }
        
        .currency-row-group {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 6px;
            align-items: flex-start;
        }
        
        .currency-row-group:last-child {
            margin-bottom: 5px;
            padding-bottom: 3px;
        }
        
        .currency-category {
            flex: 1;
            min-width: 130px;
            max-width: 180px;
        }
        
        .currency-category-title {
            color: var(--accent);
            font-size: 0.75em;
            font-weight: bold;
            margin-bottom: 4px;
            padding-bottom: 2px;
            border-bottom: 1px solid var(--border);
        }
        
        .currency-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1px 0;
            font-size: 0.75em;
        }
        
        .currency-name {
            color: var(--text-secondary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 100px;
        }
        
        .currency-value {
            color: var(--gold);
            font-weight: bold;
            margin-left: 5px;
        }
        
        .currency-value-zero {
            color: var(--text-secondary);
            margin-left: 5px;
        }
        
        .crystal-container {
            width: fit-content;
            margin-bottom: 6px;
        }
        
        .crystal-container .currency-category-title {
            width: 100%;
        }
        
        .crystal-grid {
            display: grid;
            grid-template-columns: 60px repeat(3, 70px);
            gap: 1px 5px;
            font-size: 0.75em;
        }
        
        .crystal-header {
            color: var(--accent);
            font-weight: bold;
            text-align: right;
            padding: 2px 0;
        }
        
        .crystal-element {
            color: var(--text-secondary);
            padding: 1px 0;
        }
        
        .crystal-value {
            color: var(--gold);
            font-weight: bold;
            text-align: right;
            padding: 1px 0;
        }
        
        .crystal-value-zero {
            color: var(--text-secondary);
            text-align: right;
            padding: 1px 0;
        }
        
        .status-ready {
            color: var(--success);
            font-weight: bold;
        }
        
        .status-none {
            color: var(--danger) !important;
            font-weight: bold;
        }
        
        td.status-none {
            color: var(--danger) !important;
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
            max-height: 800px;
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
    <!-- Loading Overlay -->
    <div class="loading-overlay" id="loading-overlay">
        <div class="loading-text">⚓ AutoRetainer Dashboard</div>
        <div class="loading-subtext">Loading {{ data.summary.total_characters }} characters across {{ data.accounts|length }} account(s)...</div>
        <div class="progress-container">
            <div class="progress-bar"></div>
        </div>
        <div class="loading-hint">This may take a few seconds for large character counts</div>
    </div>
    
    <div class="container">
        <!-- Sticky Top Section: Header + Summary Cards -->
        <div class="sticky-top-section">
            <header>
                <div class="header-content">
                    <div class="header-left">
                        <h1>⚓ AutoRetainer Dashboard <a href="/fcdata/" style="font-size:0.7rem;color:var(--accent-light);text-decoration:none;padding:3px 10px;border:1px solid var(--border);border-radius:6px;margin-left:8px;vertical-align:middle;font-weight:400;">🏨 FC Data</a><a href="/data/" style="font-size:0.7rem;color:var(--accent-light);text-decoration:none;padding:3px 10px;border:1px solid var(--border);border-radius:6px;margin-left:6px;vertical-align:middle;font-weight:400;">📝 Data</a></h1>
                        <div class="subtitle">Last Updated: <span id="last-updated">{{ data.last_updated }}</span> | Auto-refresh: {{ auto_refresh }}s</div>
                    </div>
                    <div class="header-right">
                        <div class="search-container">
                            <div class="search-error" id="search-error">No results match your search...</div>
                            <input type="text" class="search-input" id="character-search" placeholder="🔍 Search character..." oninput="searchCharacters(this.value)">
                            <div class="theme-selector">
                                <button class="filter-btn region-btn" id="region-na-btn" onclick="toggleRegionFilter('NA')" title="Show NA characters only">NA</button>
                                <button class="filter-btn region-btn" id="region-eu-btn" onclick="toggleRegionFilter('EU')" title="Show EU characters only">EU</button>
                                <button class="filter-btn region-btn" id="region-jp-btn" onclick="toggleRegionFilter('JP')" title="Show JP characters only">JP</button>
                                <button class="filter-btn region-btn" id="region-oce-btn" onclick="toggleRegionFilter('OCE')" title="Show OCE characters only">OCE</button>
                                <button class="theme-btn" data-theme="default" title="Default (Blue)" onclick="setTheme('default')">♻️</button>
                                <button class="theme-btn" data-theme="ultra-dark" title="Ultra Dark" onclick="setTheme('ultra-dark')"></button>
                                <button class="theme-btn" data-theme="dark-gray" title="Dark Gray" onclick="setTheme('dark-gray')"></button>
                                <button class="theme-btn" data-theme="ocean-blue" title="Ocean Blue" onclick="setTheme('ocean-blue')"></button>
                                <button class="theme-btn" data-theme="forest-green" title="Forest Green" onclick="setTheme('forest-green')"></button>
                                <button class="theme-btn" data-theme="crimson-red" title="Crimson Red" onclick="setTheme('crimson-red')"></button>
                                <button class="theme-btn" data-theme="purple-haze" title="Purple Haze" onclick="setTheme('purple-haze')"></button>
                                <button class="theme-btn" data-theme="pastel-pink" title="Pastel Pink" onclick="setTheme('pastel-pink')"></button>
                                <button class="theme-btn" data-theme="dark-orange" title="Dark Orange" onclick="setTheme('dark-orange')"></button>
                                <button class="theme-btn" data-theme="brown" title="Brown" onclick="setTheme('brown')"></button>
                            </div>
                            <div class="global-filters">
                                <button class="filter-btn" id="global-accounts-btn" onclick="toggleAllAccounts()" title="Expand/Collapse All Accounts">▶</button>
                                <button class="filter-btn money-btn" id="global-money-btn" onclick="toggleHideMoneyGlobal()" title="Hide Money Stats">💰</button>
                                <button class="filter-btn anon-btn" id="global-anon-btn" onclick="toggleAnonymizeGlobal()" title="Anonymize (if sorting after using, you may have to refresh the page to recover names.)">🔒</button>
                                <button class="filter-btn" id="global-hide-stats-btn" onclick="toggleHidePlayerStatsGlobal()" title="Show Player Stats">✏️</button>
                                <button class="filter-btn" id="global-hide-subs-btn" onclick="toggleHideSubsGlobal()" title="Hide Submarines">🐋</button>
                                <button class="filter-btn" id="global-hide-retainers-btn" onclick="toggleHideRetainersGlobal()" title="Hide Retainers">🛎️</button>
                                {% if show_classes %}<button class="filter-btn" id="global-hide-classes-btn" onclick="toggleHideClassesGlobal()" title="Show DoW/DoM & DoH/DoL">📖</button>{% endif %}
                                {% if show_currencies %}<button class="filter-btn" id="global-hide-currencies-btn" onclick="toggleHideCurrenciesGlobal()" title="Show Currencies">🪶</button>{% endif %}
                                <button class="filter-btn" id="global-house-btn" onclick="toggleFilterGlobal('personal-house')" title="Show only characters with Personal House">🏠</button>
                                <button class="filter-btn" id="global-fc-btn" onclick="toggleFilterGlobal('fc-house')" title="Show only characters with FC House">🏨</button>
                                <button class="filter-btn" id="global-coffers-btn" onclick="toggleFilterGlobal('coffers')" title="Show only characters with Coffers">📦</button>
                                <button class="filter-btn" id="global-dyes-btn" onclick="toggleFilterGlobal('dyes')" title="Show only characters with Dyes">🎨</button>
                                <button class="filter-btn" id="global-mb-btn" onclick="toggleFilterGlobal('mb')" title="Show only characters with MB Items">🪧</button>
                                <button class="filter-btn" id="global-retainers-btn" onclick="toggleFilterGlobal('retainers')" title="Show only characters with Retainers">👤</button>
                                <button class="filter-btn" id="global-treasure-btn" onclick="toggleFilterGlobal('treasure')" title="Show only characters with Treasure">💎</button>
                                <button class="filter-btn" id="global-subs-btn" onclick="toggleFilterGlobal('subs')" title="Show only characters with Submarines">🚢</button>
                                {% if show_msq_progression %}<button class="filter-btn" id="global-msq-btn" onclick="toggleFilterGlobal('msq')" title="Hide characters with 0% MSQ">📜</button>{% endif %}
                                <button class="filter-btn" id="global-ready-btn" onclick="toggleFilterGlobal('ready')" title="Show only characters with Ready retainers/subs">🏁</button>
                                <button class="filter-btn" id="global-sleeping-btn" onclick="toggleFilterGlobal('sleeping')" title="Show only characters with disabled retainers/subs">😴</button>
                                {% if data.summary.idle_retainers > 0 or data.summary.idle_subs > 0 %}<button class="filter-btn" id="global-idle-btn" onclick="toggleFilterGlobal('idle')" title="Show only characters with idle retainers/subs">⌛</button>{% endif %}
                                {% if highlight_potential_subs %}<button class="filter-btn" id="global-potential-subs-btn" onclick="toggleFilterGlobal('potential_subs')" title="Show only characters Lv 25+ not in FC and characters that can hire retainers.">❓</button>{% endif %}
                                <button class="filter-btn" id="global-processing-btn" onclick="toggleFilterGlobal('processing')" title="Show only characters that are processing (Enabled or WorkshopEnabled)">✅</button>
                                <button class="filter-btn" id="global-excluded-btn" onclick="toggleFilterGlobal('excluded')" title="Show only characters with exclusions">❌</button>
                                <button class="filter-btn" id="global-expand-btn" onclick="expandAllCharsGlobal()" title="Expand All Characters">▼</button>
                                <button class="filter-btn" id="global-collapse-btn" onclick="collapseAllCharsGlobal()" title="Collapse All Characters">▲</button>
                            </div>
                        </div>
                    </div>
                </div>
            </header>
            
            <!-- Summary Cards -->
            <div class="summary-grid">
            <div class="summary-card">
                <div class="value" id="sum-total-chars">👥 {{ data.summary.total_characters }}</div>
                <div class="sublabel" id="sum-char-levels">{{ data.summary.chars_lv25_plus }} Lv 25+ | {{ data.summary.chars_lv100 }} Lv 100</div>
                <div class="sublabel" id="sum-plots">🏠 {{ data.summary.personal_plots }} | 🏨 {{ data.summary.fc_plots }}{% if highlight_potential_subs and data.summary.potential_subs_count > 0 %} | <span id="sum-potential-subs" style="color: #888;">❓ {{ data.summary.potential_subs_count }}</span>{% endif %}</div>
            </div>
            <div class="summary-card">
                <div class="value" id="sum-total-gil">{{ "{:,}".format(data.summary.total_gil) }}</div>
                <div class="label">💰 Total Gil</div>
                <div class="sublabel" id="sum-fc-points">🪙 {{ "{:,}".format(data.summary.total_fc_points) }} FC</div>
            </div>
            <div class="summary-card">
                <div class="value" id="sum-treasure">{{ "{:,}".format(data.summary.total_treasure) }}</div>
                <div class="label">💎 Treasure Value</div>
                <div class="sublabel">💰+💎= <span id="sum-with-treasure">{{ "{:,}".format(data.summary.total_with_treasure) }}</span></div>
            </div>
            <div class="summary-card">
                <div class="value" id="sum-coffer-dye">{{ "{:,}".format(data.summary.total_coffer_dye_value) }}</div>
                <div class="label">📦 Coffer + Dyes</div>
                <div class="sublabel" id="sum-coffer-dye-counts">📦 {{ data.summary.total_coffer_count }} 🎨 {{ data.summary.total_dye_count }}{% if data.summary.total_mb_dye_count > 0 %} <span id="sum-mb-dye-count" style="color: var(--warning);">🪧 {{ data.summary.total_mb_dye_count }}</span>{% endif %}</div>
            </div>
            <div class="summary-card">
                <div class="value">
                    <span id="sum-ready-subs">{{ data.summary.ready_subs }}</span>/<span id="sum-total-subs">{{ data.summary.enabled_subs }}</span>
                    <div id="sum-subs-stats" style="font-size: 0.7em; color: var(--text-secondary);">
                        <span style="color: var(--warning);">Lvl: {{ data.summary.subs_leveling }}</span> |
                        <span style="color: var(--success);">Farm: {{ data.summary.subs_farming }}</span>{% if data.summary.idle_subs > 0 %} |
                        <span style="color: #FFB6C1;">Idle: {{ data.summary.idle_subs }}</span>{% endif %}
                    </div>
                </div>
                <div class="label">🚢 Submarines{% if data.summary.excluded_subs > 0 %} <span id="sum-excluded-subs" style="color: var(--danger);">❌{{ data.summary.excluded_subs }}</span>{% endif %}{% if data.summary.sleeping_subs > 0 %} <span id="sum-sleeping-subs" style="color: #9370DB;">😴{{ data.summary.sleeping_subs }}</span>{% endif %}</div>
            </div>
            <div class="summary-card">
                <div class="value">
                    <span id="sum-ready-retainers">{{ data.summary.ready_retainers }}</span>/<span id="sum-total-retainers">{{ data.summary.enabled_retainers }}</span>
                    <div id="sum-retainers-stats" style="font-size: 0.7em; color: var(--text-secondary);">
                        <span style="color: var(--warning);">Lvl: {{ data.summary.retainers_leveling }}</span> |
                        <span style="color: var(--success);">Farm: {{ data.summary.retainers_farming }}</span>{% if data.summary.idle_retainers > 0 %} |
                        <span style="color: cyan;">Idle: {{ data.summary.idle_retainers }}</span>{% endif %}
                    </div>
                </div>
                <div class="label">👤 Retainers{% if data.summary.excluded_retainers > 0 %} <span id="sum-excluded-retainers" style="color: var(--danger);">❌{{ data.summary.excluded_retainers }}</span>{% endif %}{% if data.summary.sleeping_retainers > 0 %} <span id="sum-sleeping-retainers" style="color: #9370DB;">😴{{ data.summary.sleeping_retainers }}</span>{% endif %}</div>
            </div>
            <div class="summary-card">
                <div class="value"><span id="sum-total-mb">{{ data.summary.total_mb_items }}</span>/<span id="sum-max-mb">{{ "{:,}".format(data.summary.max_mb_items) }}</span></div>
                <div class="label">🪧 MB Items</div>
                {% if data.summary.all_max_mb_count > 0 %}
                <div class="sublabel" id="sum-mb-max" style="color: var(--danger);">{{ data.summary.all_max_mb_count }} Chars Max</div>
                {% endif %}
            </div>
            <div class="summary-card">
                <div class="value profit" id="sum-monthly-income">{{ "{:,}".format(data.summary.monthly_income|int) }}</div>
                <div class="label">📈 Monthly Income</div>
                <div class="sublabel" id="sum-daily-income">📅 {{ "{:,}".format((data.summary.monthly_income / 30)|int) }}/day</div>
            </div>
            <div class="summary-card">
                <div class="value cost" id="sum-monthly-cost">{{ "{:,}".format(data.summary.monthly_cost|int) }}</div>
                <div class="label">📉 Monthly Cost</div>
                <div class="sublabel" id="sum-restock" style="{% if data.summary.min_restock_days is not none and data.summary.min_restock_days < 7 %}color: var(--danger);{% elif data.summary.min_restock_days is not none and data.summary.min_restock_days < 14 %}color: var(--warning);{% endif %}">♻️ {% if data.summary.min_restock_days is not none %}{{ data.summary.min_restock_days }}d lowest{% else %}N/A{% endif %}</div>
            </div>
            <div class="summary-card">
                <div class="value profit" id="sum-annual-income">{{ "{:,}".format(data.summary.annual_income|int) }}</div>
                <div class="label">🏆 Annual Income</div>
                <div class="sublabel profit">💎 <span id="sum-annual-profit">{{ "{:,}".format(data.summary.annual_profit|int) }}</span> Profit</div>
            </div>
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
                    <span class="{% if account.has_max_mb_retainer %}mb-max{% endif %}">🪧 <span class="acc-mb">{{ account.total_mb_items }}</span>/<span class="acc-max-mb">{{ "{:,}".format(account.max_mb_items) }}</span> MB{% if account.has_max_mb_retainer %} (<span class="acc-max-mb-count">{{ account.max_mb_retainer_count }}</span>){% endif %}</span>
                    {% if show_msq_progression %}<span>📜 <span class="acc-msq-100">{{ account.msq_100_count }}</span>/<span class="acc-msq-tracked">{{ account.characters_with_msq }}</span> MSQ</span>{% endif %}
                </div>
            </div>
            
            {% if not account.error %}
            <div class="sort-bar collapsed">
                <span class="sort-label">Sort by:</span>
                <button class="sort-btn" data-sort="level" data-order="desc" onclick="sortCharacters(this)" title="Level">🎚️ ▼</button>
                {% if show_classes %}<button class="sort-btn" data-sort="classes" data-order="asc" onclick="sortCharacters(this)" title="Classes (Lowest → Highest)">📖 ▲</button>{% endif %}
                <button class="sort-btn" data-sort="gil" data-order="desc" onclick="sortCharacters(this)" title="Gil">💰 ▼</button>
                <button class="sort-btn" data-sort="treasure" data-order="desc" onclick="sortCharacters(this)" title="Treasure">💎 ▼</button>
                <button class="sort-btn" data-sort="fc_points" data-order="desc" onclick="sortCharacters(this)" title="FC Points">🪙 ▼</button>
                <button class="sort-btn" data-sort="venture_coins" data-order="desc" onclick="sortCharacters(this)" title="Ventures">🛒 ▼</button>
                <button class="sort-btn" data-sort="coffers" data-order="desc" onclick="sortCharacters(this)" title="Coffers">📦 ▼</button>
                <button class="sort-btn" data-sort="dyes" data-order="desc" onclick="sortCharacters(this)" title="Dyes">🎨 ▼</button>
                <button class="sort-btn" data-sort="tanks" data-order="desc" onclick="sortCharacters(this)" title="Ceruleum Tanks">⛽ ▼</button>
                <button class="sort-btn" data-sort="kits" data-order="desc" onclick="sortCharacters(this)" title="Repair Kits">🔧 ▼</button>
                <button class="sort-btn" data-sort="restock" data-order="asc" onclick="sortCharacters(this)" title="Restock Days">♻️ ▲</button>
                <button class="sort-btn" data-sort="inventory" data-order="desc" onclick="sortCharacters(this)" title="Inventory">🎒 ▼</button>
                <button class="sort-btn" data-sort="mb" data-order="desc" onclick="sortCharacters(this)" title="MB Items">🪧 ▼</button>
                <button class="sort-btn" data-sort="retainers" data-order="asc" onclick="sortCharacters(this)" title="Retainers (by return time)">👤 ▲</button>
                <button class="sort-btn" data-sort="retainer_level" data-order="desc" onclick="sortCharacters(this)" title="Retainer Level">👤 Lv ▼</button>
                <button class="sort-btn" data-sort="subs" data-order="asc" onclick="sortCharacters(this)" title="Submarines (by return time)">🚢 ▲</button>
                <button class="sort-btn" data-sort="sub_level" data-order="desc" onclick="sortCharacters(this)" title="Submarine Level">🚢 Lv ▼</button>
                {% if show_msq_progression %}<button class="sort-btn" data-sort="msq_percent" data-order="asc" onclick="sortCharacters(this)" title="MSQ Progress (least to most)">📜 ▲</button>{% endif %}
            </div>
            {% endif %}
            
            <div class="account-content collapsed">
            {% if account.error %}
            <div class="error-message">{{ account.error }}</div>
            {% else %}
            <div class="character-grid">
                {% for char in account.characters %}
                <div class="character-card{% if char.has_max_mb_retainer %} has-max-mb{% endif %}{% if char.has_idle_retainer and not char.retainers_sleeping %} has-idle-retainer{% endif %}{% if char.has_idle_sub and not char.subs_sleeping %} has-idle-sub{% endif %}{% if char.has_potential_retainer %} has-potential-retainer{% endif %}{% if char.has_potential_subs %} has-potential-subs{% endif %}" data-char="{{ char.cid }}" data-level="{{ char.current_level }}" data-lowest-level="{{ char.lowest_level }}" data-highest-level="{{ char.highest_level }}" data-gil="{{ char.total_gil }}" data-treasure="{{ char.treasure_value }}" data-fc-points="{{ char.fc_points }}" data-venture-coins="{{ char.venture_coins }}" data-coffers="{{ char.coffer_count }}" data-dyes="{{ char.dye_count }}" data-tanks="{{ char.ceruleum }}" data-kits="{{ char.repair_kits }}" data-restock="{{ char.days_until_restock if char.days_until_restock is not none else 9999 }}" data-retainers="{{ char.ready_retainers }}" data-total-retainers="{{ char.total_retainers }}" data-subs="{{ char.ready_subs }}" data-total-subs="{{ char.total_subs }}" data-inventory="{{ 140 - char.inventory_space }}" data-has-personal-house="{{ 'true' if char.private_house else 'false' }}" data-has-fc-house="{{ 'true' if char.fc_house else 'false' }}" data-retainer-level="{{ char.max_retainer_level }}" data-sub-level="{{ char.min_sub_level }}" data-retainer-return="{{ char.min_retainer_return }}" data-sub-return="{{ char.min_sub_return }}" data-msq-percent="{{ char.msq_percent }}" data-has-max-mb="{{ 'true' if char.has_max_mb_retainer else 'false' }}" data-mb="{{ char.mb_items }}" data-has-mb="{{ 'true' if char.mb_items > 0 else 'false' }}" data-has-coffers="{{ 'true' if char.coffer_count > 0 else 'false' }}" data-has-dyes="{{ 'true' if char.dye_count > 0 else 'false' }}" data-has-treasure="{{ 'true' if char.treasure_value > 0 else 'false' }}" data-region="{{ char.region }}" data-has-ready="{{ 'true' if (char.ready_retainers > 0 and not char.exclude_retainer and not char.retainers_sleeping) or (char.ready_subs > 0 and not char.exclude_workshop and not char.subs_sleeping) else 'false' }}" data-has-exclusion="{{ 'true' if char.exclude_retainer or char.exclude_workshop else 'false' }}" data-is-processing="{{ 'true' if char.is_processing else 'false' }}" data-has-sleeping="{{ 'true' if (char.retainers_sleeping and char.total_retainers > 0 and not char.exclude_retainer) or (char.subs_sleeping and char.total_subs > 0 and not char.exclude_workshop) else 'false' }}" data-has-idle="{{ 'true' if (char.has_idle_retainer and not char.retainers_sleeping) or (char.has_idle_sub and not char.subs_sleeping) else 'false' }}" data-has-potential-subs="{{ 'true' if char.has_potential_subs or char.has_potential_retainer else 'false' }}">
                    <div class="character-header collapsed {% if (char.ready_retainers > 0 and not char.exclude_retainer and not char.retainers_sleeping) or (char.ready_subs > 0 and not char.exclude_workshop and not char.subs_sleeping) %}has-available{% endif %}" onclick="toggleCharacter(this)">
                        <div class="char-header-row name-row">
                            <span class="character-name">{{ char.name }}{% if char.current_level > 0 %} <span style="font-size: 0.8em; color: var(--text-secondary);">(Lv {{ char.current_level }}, {{ char.current_job }})</span>{% endif %}{% if show_msq_progression and char.msq_completed > 0 %} <span style="font-size: 0.8em; {% if char.msq_percent >= 90 %}color: #4ade80;{% elif char.msq_percent >= 50 %}color: #fbbf24;{% else %}color: #94a3b8;{% endif %}" title="MSQ Progress: {{ char.msq_completed }}/{{ char.msq_total }}{% if char.msq_quest_name %} - {{ char.msq_quest_name }}{% endif %}">MSQ: {{ char.msq_percent }}%</span>{% endif %}{% if char.private_house %} <span style="font-size: 0.8em;" title="Personal House: {{ char.private_house }}">🏠</span>{% endif %}{% if char.fc_house %} <span style="font-size: 0.8em;" title="FC House: {{ char.fc_house }}">🏨</span>{% endif %}</span>
                            <span class="char-status {% if char.ready_retainers > 0 and not char.exclude_retainer and not char.retainers_sleeping %}available{% else %}all-sent{% endif %}">👤 {% if char.exclude_retainer %}null{% else %}{{ char.ready_retainers }}/{{ char.total_retainers }}{% endif %}{% if char.sleeping_retainer_count > 0 %} <span style="color: #9370DB;">😴{{ char.sleeping_retainer_count }}</span>{% endif %}</span>
                        </div>
                        <div class="char-header-row">
                            <span class="character-world">{{ char.world }}{% if char.fc_name %} • {{ char.fc_name }}{% endif %} • 🎒 {{ 140 - char.inventory_space }}/140</span>
                            <span class="char-status {% if char.ready_subs > 0 and not char.exclude_workshop and not char.subs_sleeping %}available{% else %}all-sent{% endif %}">🚢 {% if char.exclude_workshop %}null{% else %}{{ char.ready_subs }}/{{ char.total_subs }}{% endif %}{% if char.sleeping_sub_count > 0 %} <span style="color: #9370DB;">😴{{ char.sleeping_sub_count }}</span>{% endif %}</span>
                        </div>
                        <div class="char-header-row">
                            <span style="font-size: 0.8em; color: var(--text-secondary);">🪧 {{ char.mb_items }} | 📦 {{ char.coffer_count }} | 🎨 {{ char.dye_count }}{% if char.dye_count > 0 %} 🤍{{ char.dye_pure_white }} 🖤{{ char.dye_jet_black }} 🩷{{ char.dye_pastel_pink }}{% endif %}</span>
                            <span class="character-gil">{{ "{:,}".format(char.total_gil) }} gil</span>
                        </div>
                        <div class="char-header-row">
                            <span style="font-size: 0.8em; color: var(--text-secondary);">🪙 {{ "{:,}".format(char.fc_points) }} | 🛒 {{ "{:,}".format(char.venture_coins) }} | ⛽ {{ "{:,}".format(char.ceruleum) }} | 🔧 {{ "{:,}".format(char.repair_kits) }}{% if char.total_subs > 0 %} | <span style="{% if char.days_until_restock is not none and char.days_until_restock < 7 %}color: var(--danger);{% elif char.days_until_restock is not none and char.days_until_restock < 14 %}color: var(--warning);{% endif %}">♻️ {% if char.days_until_restock is not none %}{{ char.days_until_restock }}d{% else %}N/A{% endif %}</span>{% endif %}</span>
                            {% if char.total_subs > 0 %}<span style="font-size: 0.8em; color: var(--gold);">💎 {{ "{:,}".format(char.treasure_value) }}</span>{% endif %}
                        </div>
                    </div>
                    <div class="character-body collapsed">
                        {% if highlight_idle_retainers and char.has_idle_retainer and not char.retainers_sleeping %}
                        <div class="highlight-reason" style="font-size: 0.75em; color: cyan; padding: 5px 15px; background: rgba(0, 255, 255, 0.1);">* You have idle retainers, update your planner in game</div>
                        {% endif %}
                        {% if highlight_idle_subs and char.has_idle_sub and not char.subs_sleeping %}
                        <div class="highlight-reason" style="font-size: 0.75em; color: #FFB6C1; padding: 5px 15px; background: rgba(255, 182, 193, 0.1);">* You have idle subs, update your planner in game</div>
                        {% endif %}
                        {% if highlight_max_mb and char.has_max_mb_retainer %}
                        <div class="highlight-reason" style="font-size: 0.75em; color: #FFD700; padding: 5px 15px; background: rgba(255, 215, 0, 0.1);">* You have max marketboard items, go undercut or remove!</div>
                        {% endif %}
                        {% if highlight_potential_retainer and char.has_potential_retainer %}
                        <div class="highlight-reason" style="font-size: 0.75em; color: #8B4513; padding: 5px 15px; background: rgba(139, 69, 19, 0.1);">* You should hire retainers, you have progressed far enough in MSQ</div>
                        {% endif %}
                        {% if highlight_potential_subs and char.has_potential_subs %}
                        <div class="highlight-reason" style="font-size: 0.75em; color: #888; padding: 5px 15px; background: rgba(26, 26, 26, 0.3);">* You're lv 25+ and not in an FC, get to farming!<br>You may also just not have Lifestream registered, get on it!</div>
                        {% endif %}
                        {% if char.retainers_sleeping and char.total_retainers > 0 %}
                        <div class="highlight-reason" style="font-size: 0.75em; color: #9370DB; padding: 5px 15px; background: rgba(147, 112, 219, 0.1);">* Your retainers are not enabled in AutoRetainer</div>
                        {% endif %}
                        {% if char.subs_sleeping and char.total_subs > 0 %}
                        <div class="highlight-reason" style="font-size: 0.75em; color: #9370DB; padding: 5px 15px; background: rgba(147, 112, 219, 0.1);">* Your submarines are not enabled in AutoRetainer</div>
                        {% endif %}
                        <div class="section-title collapsible collapsed player-stats-header" onclick="toggleCollapse(this)">📊 Player Stats</div>
                        <div class="collapse-content collapsed player-stats-content">
                        <div class="info-row">
                            <span class="info-label">Player</span>
                            <span class="info-value player-name-world">{{ char.name }}@{{ char.world }}</span>
                        </div>
                        {% if char.current_level > 0 %}
                        <div class="info-row">
                            <span class="info-label">Current Class</span>
                            <span class="info-value">{{ char.current_job }} Lv {{ char.current_level }}</span>
                        </div>
                        {% endif %}
                        {% if char.lowest_level > 0 and char.lowest_level < char.current_level %}
                        <div class="info-row">
                            <span class="info-label">Lowest Class</span>
                            <span class="info-value">{{ char.lowest_job }} Lv {{ char.lowest_level }}</span>
                        </div>
                        {% endif %}
                        {% if char.highest_level > 0 and char.highest_level > char.current_level %}
                        <div class="info-row">
                            <span class="info-label">Highest Class</span>
                            <span class="info-value">{{ char.highest_job }} Lv {{ char.highest_level }}</span>
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
                        <div class="info-row">
                            <span class="info-label">Inventory 🎒</span>
                            <span class="info-value" style="{% if (140 - char.inventory_space) >= 130 %}color: var(--accent);{% elif (140 - char.inventory_space) >= 100 %}color: var(--warning);{% endif %}">{{ 140 - char.inventory_space }}/140</span>
                        </div>
                        {% if show_msq_progression and char.msq_completed > 0 %}
                        <div class="info-row">
                            <span class="info-label">MSQ Progress 📜</span>
                            <span class="info-value" style="{% if char.msq_percent >= 90 %}color: #4ade80;{% elif char.msq_percent >= 50 %}color: #fbbf24;{% else %}color: #94a3b8;{% endif %}">{{ char.msq_percent }}% ({{ char.msq_completed }}/{{ char.msq_total }}){% if char.msq_quest_name %} - {{ char.msq_quest_name }}{% endif %}</span>
                        </div>
                        {% endif %}
                        {% if char.private_house %}
                        <div class="info-row">
                            <span class="info-label">Personal House 🏠</span>
                            <span class="info-value">{{ char.private_house }}</span>
                        </div>
                        {% endif %}
                        {% if char.fc_house %}
                        <div class="info-row">
                            <span class="info-label">FC House 🏨</span>
                            <span class="info-value">{{ char.fc_house }}</span>
                        </div>
                        {% endif %}
                        <div class="info-row">
                            <span class="info-label">Ceruleum Tanks ⛽</span>
                            <span class="info-value">{{ "{:,}".format(char.ceruleum) }}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Repair Kits 🔧</span>
                            <span class="info-value">{{ "{:,}".format(char.repair_kits) }}</span>
                        </div>
                        {% if char.total_subs > 0 %}
                        <div class="info-row">
                            <span class="info-label">Days Until Restock ♻️</span>
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
                                    <td class="{% if not sub.plan_name and not sub.is_farming and not sub.is_leveling %}status-none{% endif %}" style="{% if sub.plan_name or sub.is_farming %}color: var(--success);{% elif sub.is_leveling %}color: var(--warning);{% endif %}">
                                        {% if sub.plan_name %}{{ sub.plan_name }}{% elif sub.is_farming %}Farm{% elif sub.is_leveling %}Lvl{% else %}None{% endif %}
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
                        <div class="section-title collapsible" onclick="toggleCollapse(this)">👤 Retainers ({{ char.retainers|length }}) - <span style="color: var(--warning);">Lvl: {{ char.retainers_leveling }}</span> | <span style="color: var(--success);">Farm: {{ char.retainers_farming }}</span></div>
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
                                    <td class="{% if ret.venture_formatted == 'Ready!' %}status-ready{% elif not ret.has_venture %}status-none{% else %}status-voyaging{% endif %}">
                                        {{ ret.venture_formatted if ret.has_venture else "None" }}
                                    </td>
                                </tr>
                                {% endfor %}
                            </table>
                        </div>
                        {% endif %}
                        
                        {% if show_classes and char.all_jobs %}
                        <div class="section-title collapsible collapsed" onclick="toggleCollapse(this)">⚔️ DoW/DoM</div>
                        <div class="collapse-content collapsed">
                            <div class="job-grid">
                                <div class="job-column">
                                    <div class="job-category-title">🛡️ Tank</div>
                                    {% for job in job_categories.Tank %}
                                    {% set job_level = char.all_jobs.get(job, 0) %}
                                    {% if job_level == 0 and job in job_base_class %}
                                    {% set job_level = char.all_jobs.get(job_base_class[job], 0) %}
                                    {% endif %}
                                    <div class="job-row">
                                        <span class="job-level {% if job_level == 0 %}job-level-zero{% endif %}">{{ job_level }}</span>
                                        <span class="job-name">{{ job_display_names.get(job, job) }}</span>
                                    </div>
                                    {% endfor %}
                                    <div class="job-category-title" style="margin-top: 10px;">⚔️ Melee DPS</div>
                                    {% for job in job_categories.MeleeDPS %}
                                    {% set job_level = char.all_jobs.get(job, 0) %}
                                    {% if job_level == 0 and job in job_base_class %}
                                    {% set job_level = char.all_jobs.get(job_base_class[job], 0) %}
                                    {% endif %}
                                    <div class="job-row">
                                        <span class="job-level {% if job_level == 0 %}job-level-zero{% endif %}">{{ job_level }}</span>
                                        <span class="job-name">{{ job_display_names.get(job, job) }}</span>
                                    </div>
                                    {% endfor %}
                                </div>
                                <div class="job-column">
                                    <div class="job-category-title">💚 Healer</div>
                                    {% for job in job_categories.Healer %}
                                    {% set job_level = char.all_jobs.get(job, 0) %}
                                    {% if job_level == 0 and job in job_base_class %}
                                    {% set job_level = char.all_jobs.get(job_base_class[job], 0) %}
                                    {% endif %}
                                    <div class="job-row">
                                        <span class="job-level {% if job_level == 0 %}job-level-zero{% endif %}">{{ job_level }}</span>
                                        <span class="job-name">{{ job_display_names.get(job, job) }}</span>
                                    </div>
                                    {% endfor %}
                                    <div class="job-category-title" style="margin-top: 10px;">🏹 Physical Ranged DPS</div>
                                    {% for job in job_categories.PhysRangedDPS %}
                                    {% set job_level = char.all_jobs.get(job, 0) %}
                                    {% if job_level == 0 and job in job_base_class %}
                                    {% set job_level = char.all_jobs.get(job_base_class[job], 0) %}
                                    {% endif %}
                                    <div class="job-row">
                                        <span class="job-level {% if job_level == 0 %}job-level-zero{% endif %}">{{ job_level }}</span>
                                        <span class="job-name">{{ job_display_names.get(job, job) }}</span>
                                    </div>
                                    {% endfor %}
                                    <div class="job-category-title" style="margin-top: 10px;">✨ Magical Ranged DPS</div>
                                    {% for job in job_categories.MagicRangedDPS %}
                                    {% set job_level = char.all_jobs.get(job, 0) %}
                                    {% if job_level == 0 and job in job_base_class %}
                                    {% set job_level = char.all_jobs.get(job_base_class[job], 0) %}
                                    {% endif %}
                                    <div class="job-row">
                                        <span class="job-level {% if job_level == 0 %}job-level-zero{% endif %}">{{ job_level }}</span>
                                        <span class="job-name">{{ job_display_names.get(job, job) }}</span>
                                    </div>
                                    {% endfor %}
                                </div>
                            </div>
                        </div>
                        
                        <div class="section-title collapsible collapsed" onclick="toggleCollapse(this)">🔨 DoH/DoL</div>
                        <div class="collapse-content collapsed">
                            <div class="job-grid">
                                <div class="job-column">
                                    <div class="job-category-title">🔨 Disciples of the Hand</div>
                                    {% for job in job_categories.DoH %}
                                    {% set job_level = char.all_jobs.get(job, 0) %}
                                    <div class="job-row">
                                        <span class="job-level {% if job_level == 0 %}job-level-zero{% endif %}">{{ job_level }}</span>
                                        <span class="job-name">{{ job_display_names.get(job, job) }}</span>
                                    </div>
                                    {% endfor %}
                                </div>
                                <div class="job-column">
                                    <div class="job-category-title">⛏️ Disciples of the Land</div>
                                    {% for job in job_categories.DoL %}
                                    {% set job_level = char.all_jobs.get(job, 0) %}
                                    <div class="job-row">
                                        <span class="job-level {% if job_level == 0 %}job-level-zero{% endif %}">{{ job_level }}</span>
                                        <span class="job-name">{{ job_display_names.get(job, job) }}</span>
                                    </div>
                                    {% endfor %}
                                </div>
                            </div>
                        </div>
                        {% endif %}
                        
                        {% if show_currencies and char.categorized_currencies %}
                        <div class="section-title collapsible collapsed" onclick="toggleCollapse(this)">💰 Currencies</div>
                        <div class="collapse-content collapsed">
                            <div class="currency-section">
                                {% if char.categorized_currencies.crystal_grid %}
                                <div class="crystal-container">
                                <div class="currency-category-title">💎 Crystals</div>
                                <div class="crystal-grid">
                                    <div></div>
                                    <div class="crystal-header">Shards</div>
                                    <div class="crystal-header">Crystals</div>
                                    <div class="crystal-header">Clusters</div>
                                    {% for elem in char.categorized_currencies.crystal_elements %}
                                    <div class="crystal-element">{{ elem }}</div>
                                    <div class="{% if char.categorized_currencies.crystal_grid[elem].Shard > 0 %}crystal-value{% else %}crystal-value-zero{% endif %}">{{ "{:,}".format(char.categorized_currencies.crystal_grid[elem].Shard) }}</div>
                                    <div class="{% if char.categorized_currencies.crystal_grid[elem].Crystal > 0 %}crystal-value{% else %}crystal-value-zero{% endif %}">{{ "{:,}".format(char.categorized_currencies.crystal_grid[elem].Crystal) }}</div>
                                    <div class="{% if char.categorized_currencies.crystal_grid[elem].Cluster > 0 %}crystal-value{% else %}crystal-value-zero{% endif %}">{{ "{:,}".format(char.categorized_currencies.crystal_grid[elem].Cluster) }}</div>
                                    {% endfor %}
                                </div>
                                </div>
                                {% endif %}
                                
                                {% if char.categorized_currencies.categories.Common or char.categorized_currencies.categories.Tomestones %}
                                <div class="currency-row-group">
                                    {% if char.categorized_currencies.categories.Common %}
                                    <div class="currency-category">
                                        <div class="currency-category-title">Common</div>
                                        {% for display_name, value in char.categorized_currencies.categories.Common %}
                                        <div class="currency-row">
                                            <span class="currency-name">{{ display_name }}</span>
                                            <span class="currency-value">{{ "{:,}".format(value) }}</span>
                                        </div>
                                        {% endfor %}
                                    </div>
                                    {% endif %}
                                    {% if char.categorized_currencies.categories.Tomestones %}
                                    <div class="currency-category">
                                        <div class="currency-category-title">Tomestones</div>
                                        {% for display_name, value in char.categorized_currencies.categories.Tomestones %}
                                        <div class="currency-row">
                                            <span class="currency-name">{{ display_name }}</span>
                                            <span class="currency-value">{{ "{:,}".format(value) }}</span>
                                        </div>
                                        {% endfor %}
                                    </div>
                                    {% endif %}
                                </div>
                                {% endif %}
                                
                                {% if char.categorized_currencies.categories.Battle or char.categorized_currencies.categories.Societies or char.categorized_currencies.categories.Other %}
                                <div class="currency-row-group">
                                    {% if char.categorized_currencies.categories.Battle %}
                                    <div class="currency-category">
                                        <div class="currency-category-title">Battle</div>
                                        {% for display_name, value in char.categorized_currencies.categories.Battle %}
                                        <div class="currency-row">
                                            <span class="currency-name">{{ display_name }}</span>
                                            <span class="currency-value">{{ "{:,}".format(value) }}</span>
                                        </div>
                                        {% endfor %}
                                    </div>
                                    {% endif %}
                                    {% if char.categorized_currencies.categories.Societies %}
                                    <div class="currency-category">
                                        <div class="currency-category-title">Societies</div>
                                        {% for display_name, value in char.categorized_currencies.categories.Societies %}
                                        <div class="currency-row">
                                            <span class="currency-name">{{ display_name }}</span>
                                            <span class="currency-value">{{ "{:,}".format(value) }}</span>
                                        </div>
                                        {% endfor %}
                                    </div>
                                    {% endif %}
                                    {% if char.categorized_currencies.categories.Other %}
                                    <div class="currency-category">
                                        <div class="currency-category-title">Other</div>
                                        {% for display_name, value in char.categorized_currencies.categories.Other %}
                                        <div class="currency-row">
                                            <span class="currency-name">{{ display_name }}</span>
                                            <span class="currency-value">{{ "{:,}".format(value) }}</span>
                                        </div>
                                        {% endfor %}
                                    </div>
                                    {% endif %}
                                </div>
                                {% endif %}
                            </div>
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
            Please wait for page to load, may take longer if importing hundreds of characters, disable classes and/or currencies to generate faster.<br>
            AutoRetainer Dashboard {{ version }} | Data sourced from AutoRetainer, Lifestream, & Altoholic<br>
            <a href="https://github.com/xa-io/ffxiv-tools/tree/main/AutoRetainer-Dashboard" target="_blank" style="color: var(--accent); text-decoration: none;">github.com/xa-io/ffxiv-tools</a>
        </div>
    </div>
    
    <script>
        const REFRESH_INTERVAL = {{ auto_refresh }} * 1000;
        const DEFAULT_THEME = '{{ default_theme }}';
        
        // Theme switching functionality
        function setTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('dashboard-theme', theme);
            updateThemeButtons(theme);
        }
        
        function updateThemeButtons(activeTheme) {
            document.querySelectorAll('.theme-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.theme === activeTheme);
            });
        }
        
        function initTheme() {
            const savedTheme = localStorage.getItem('dashboard-theme') || DEFAULT_THEME;
            setTheme(savedTheme);
        }
        
        // Initialize theme immediately (before page fully loads)
        initTheme();
        
        // Hide loading overlay when page is fully loaded
        window.addEventListener('load', function() {
            const loadingOverlay = document.getElementById('loading-overlay');
            if (loadingOverlay) {
                loadingOverlay.classList.add('hidden');
                // Remove from DOM after fade animation
                setTimeout(() => {
                    loadingOverlay.remove();
                }, 500);
            }
        });
        
        function formatNumber(num) {
            return num.toLocaleString('en-US');
        }
        
        // Character search functionality
        let currentSearchTerm = '';
        
        function searchCharacters(searchTerm) {
            currentSearchTerm = searchTerm.toLowerCase().trim();
            const searchError = document.getElementById('search-error');
            let totalMatches = 0;
            
            // Process all account sections
            document.querySelectorAll('.account-section').forEach(accountSection => {
                const accountHeader = accountSection.querySelector('.account-header');
                const sortBar = accountSection.querySelector('.sort-bar');
                const accountContent = accountSection.querySelector('.account-content');
                const grid = accountSection.querySelector('.character-grid');
                
                if (!grid) return;
                
                const cards = grid.querySelectorAll('.character-card');
                let accountMatches = 0;
                
                cards.forEach(card => {
                    const charName = card.querySelector('.character-name');
                    if (!charName) return;
                    
                    // Get the character name text (just the name part, not the level/job spans)
                    const nameText = charName.childNodes[0].textContent.toLowerCase().trim();
                    
                    if (currentSearchTerm === '' || nameText.includes(currentSearchTerm)) {
                        card.classList.remove('search-hidden');
                        if (currentSearchTerm !== '') {
                            accountMatches++;
                            totalMatches++;
                        }
                    } else {
                        card.classList.add('search-hidden');
                    }
                });
                
                // If searching and this account has matches, expand it
                if (currentSearchTerm !== '' && accountMatches > 0) {
                    accountHeader.classList.remove('collapsed');
                    if (sortBar) sortBar.classList.remove('collapsed');
                    if (accountContent) accountContent.classList.remove('collapsed');
                }
                
                // If searching and no matches in this account, collapse it
                if (currentSearchTerm !== '' && accountMatches === 0) {
                    accountHeader.classList.add('collapsed');
                    if (sortBar) sortBar.classList.add('collapsed');
                    if (accountContent) accountContent.classList.add('collapsed');
                }
                
                // If search cleared, restore original collapse state
                if (currentSearchTerm === '') {
                    const collapsedAccounts = JSON.parse(localStorage.getItem('collapsedAccounts') || '{}');
                    const accountName = accountSection.dataset.account;
                    const shouldBeCollapsed = collapsedAccounts[accountName] !== false;
                    accountHeader.classList.toggle('collapsed', shouldBeCollapsed);
                    if (sortBar) sortBar.classList.toggle('collapsed', shouldBeCollapsed);
                    if (accountContent) accountContent.classList.toggle('collapsed', shouldBeCollapsed);
                }
            });
            
            // Show/hide error message
            if (currentSearchTerm !== '' && totalMatches === 0) {
                searchError.classList.add('visible');
            } else {
                searchError.classList.remove('visible');
            }
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
            
            // Toggle sort-bar (sibling after header)
            const sortBar = accountSection.querySelector('.sort-bar');
            if (sortBar) {
                sortBar.classList.toggle('collapsed', isCollapsed);
            }
            
            // Toggle account-content
            const content = accountSection.querySelector('.account-content');
            if (content) {
                content.classList.toggle('collapsed', isCollapsed);
            }
            
            // Save state to localStorage
            const collapsedAccounts = JSON.parse(localStorage.getItem('collapsedAccounts') || '{}');
            collapsedAccounts[accountName] = isCollapsed;
            localStorage.setItem('collapsedAccounts', JSON.stringify(collapsedAccounts));
        }
        
        // Track global accounts expand/collapse state
        let allAccountsExpanded = false;
        
        function toggleAllAccounts() {
            const btn = document.getElementById('global-accounts-btn');
            const accountSections = document.querySelectorAll('.account-section');
            const collapsedAccounts = JSON.parse(localStorage.getItem('collapsedAccounts') || '{}');
            
            allAccountsExpanded = !allAccountsExpanded;
            
            accountSections.forEach(section => {
                const accountName = section.dataset.account;
                const header = section.querySelector('.account-header');
                const sortBar = section.querySelector('.sort-bar');
                const content = section.querySelector('.account-content');
                
                if (allAccountsExpanded) {
                    // Expand all
                    header.classList.remove('collapsed');
                    if (sortBar) sortBar.classList.remove('collapsed');
                    if (content) content.classList.remove('collapsed');
                    collapsedAccounts[accountName] = false;
                } else {
                    // Collapse all
                    header.classList.add('collapsed');
                    if (sortBar) sortBar.classList.add('collapsed');
                    if (content) content.classList.add('collapsed');
                    collapsedAccounts[accountName] = true;
                }
            });
            
            // Update button arrow
            btn.textContent = allAccountsExpanded ? '▼' : '▶';
            btn.title = allAccountsExpanded ? 'Collapse All Accounts' : 'Expand All Accounts';
            
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
            const accountSection = btn.closest('.account-section');
            const grid = accountSection.querySelector('.character-grid');
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
                'inventory': 'inventory',
                'retainers': 'retainer-return',
                'retainer_level': 'retainer-level',
                'subs': 'sub-return',
                'sub_level': 'sub-level',
                'mb': 'mb',
                'msq_percent': 'msq-percent'
            };
            
            // Sort cards
            if (sortKey === 'classes') {
                // Special sorting for classes: sort by lowest level, then by highest level
                cards.sort((a, b) => {
                    const aLowest = parseFloat(a.dataset.lowestLevel) || 0;
                    const bLowest = parseFloat(b.dataset.lowestLevel) || 0;
                    const aHighest = parseFloat(a.dataset.highestLevel) || 0;
                    const bHighest = parseFloat(b.dataset.highestLevel) || 0;
                    
                    // Primary sort by lowest level
                    let diff = aLowest - bLowest;
                    // Secondary sort by highest level if lowest is same
                    if (diff === 0) {
                        diff = aHighest - bHighest;
                    }
                    
                    return order === 'asc' ? diff : -diff;
                });
            } else {
                const attr = attrMap[sortKey];
                cards.sort((a, b) => {
                    const aVal = parseFloat(a.dataset[attr.replace(/-([a-z])/g, (g) => g[1].toUpperCase())]) || 0;
                    const bVal = parseFloat(b.dataset[attr.replace(/-([a-z])/g, (g) => g[1].toUpperCase())]) || 0;
                    
                    if (order === 'asc') {
                        return aVal - bVal;
                    } else {
                        return bVal - aVal;
                    }
                });
            }
            
            // Re-append in sorted order
            cards.forEach(card => grid.appendChild(card));
        }
        
        function toggleFilter(btn) {
            const accountSection = btn.closest('.account-section');
            const grid = accountSection.querySelector('.character-grid');
            const cards = grid.querySelectorAll('.character-card');
            const sortBar = btn.closest('.sort-bar');
            
            // Toggle active state
            btn.classList.toggle('active');
            
            // Get all filter states
            const retainersBtn = sortBar.querySelector('.filter-btn[data-filter="retainers"]');
            const subsBtn = sortBar.querySelector('.filter-btn[data-filter="subs"]');
            const personalHouseBtn = sortBar.querySelector('.filter-btn[data-filter="personal-house"]');
            const fcHouseBtn = sortBar.querySelector('.filter-btn[data-filter="fc-house"]');
            const msqBtn = sortBar.querySelector('.filter-btn[data-filter="msq"]');
            
            const hideNoRetainers = retainersBtn && retainersBtn.classList.contains('active');
            const hideNoSubs = subsBtn && subsBtn.classList.contains('active');
            const showOnlyPersonalHouse = personalHouseBtn && personalHouseBtn.classList.contains('active');
            const showOnlyFcHouse = fcHouseBtn && fcHouseBtn.classList.contains('active');
            const hideNoMsq = msqBtn && msqBtn.classList.contains('active');
            
            // Apply all filters
            cards.forEach(card => {
                const totalRetainers = parseInt(card.dataset.totalRetainers) || 0;
                const totalSubs = parseInt(card.dataset.totalSubs) || 0;
                const hasPersonalHouse = card.dataset.hasPersonalHouse === 'true';
                const hasFcHouse = card.dataset.hasFcHouse === 'true';
                const msqPercent = parseFloat(card.dataset.msqPercent) || 0;
                
                let shouldHide = false;
                
                // Hide filters (hide if condition not met)
                if (hideNoRetainers && totalRetainers === 0) shouldHide = true;
                if (hideNoSubs && totalSubs === 0) shouldHide = true;
                if (hideNoMsq && msqPercent === 0) shouldHide = true;
                
                // Show-only filters (hide if doesn't have the feature)
                if (showOnlyPersonalHouse && !hasPersonalHouse) shouldHide = true;
                if (showOnlyFcHouse && !hasFcHouse) shouldHide = true;
                
                card.classList.toggle('filtered-hidden', shouldHide);
            });
        }
        
        let isAnonymized = false;
        let isMoneyHidden = false;
        const originalData = new Map();
        const originalMoneyData = new Map();
        
        function toggleAnonymize(btn) {
            try {
                isAnonymized = !isAnonymized;
                btn.classList.toggle('active', isAnonymized);
                btn.textContent = isAnonymized ? '🔓' : '🔒';
                
                // Toggle all anonymize buttons across all accounts
                document.querySelectorAll('.anon-btn').forEach(b => {
                    b.classList.toggle('active', isAnonymized);
                    b.textContent = isAnonymized ? '🔓' : '🔒';
                });
                
                if (isAnonymized) {
                    anonymizeAll();
                } else {
                    restoreAll();
                }
            } catch (e) {
                console.error('Error in toggleAnonymize:', e);
            }
        }
        
        function anonymizeAll() {
            try {
            // Anonymize account headers
            document.querySelectorAll('.account-section').forEach((section, accIndex) => {
                const header = section.querySelector('.account-header h2');
                if (header) {
                    if (!originalData.has(header)) {
                        originalData.set(header, header.textContent);
                    }
                    header.textContent = 'Account ' + (accIndex + 1);
                }
            });
            
            // Anonymize character data
            document.querySelectorAll('.character-card').forEach((card, cardIndex) => {
                const charName = card.querySelector('.character-name');
                if (charName) {
                    if (!originalData.has(charName)) {
                        originalData.set(charName, charName.innerHTML);
                    }
                    // Keep all spans (level/job info AND housing emojis) but replace the name
                    const allSpans = charName.querySelectorAll('span');
                    let spansHtml = '';
                    allSpans.forEach(span => { spansHtml += ' ' + span.outerHTML; });
                    charName.innerHTML = 'Toon ' + (cardIndex + 1) + spansHtml;
                }
                
                const worldFC = card.querySelector('.character-world');
                if (worldFC) {
                    if (!originalData.has(worldFC)) {
                        originalData.set(worldFC, worldFC.textContent);
                    }
                    // Count bullet points: 2+ means FC + inventory, 1 means just inventory (no FC)
                    const bulletCount = (worldFC.textContent.match(/•/g) || []).length;
                    const hasFC = bulletCount >= 2;
                    // Extract actual inventory value to preserve it
                    const inventoryMatch = worldFC.textContent.match(/🎒 (\\d+\\/\\d+)/);
                    const inventoryText = inventoryMatch ? ' • 🎒 ' + inventoryMatch[1] : '';
                    worldFC.textContent = 'Eorzea' + (hasFC ? ' • FC Name' : '') + inventoryText;
                }
                
                // Anonymize retainer names in expanded content (table rows, first td is name)
                const retTable = card.querySelector('.ret-table');
                if (retTable) {
                    retTable.querySelectorAll('tr').forEach((row, rowIndex) => {
                        if (rowIndex === 0) return; // Skip header row
                        const nameCell = row.querySelector('td:first-child');
                        if (nameCell) {
                            if (!originalData.has(nameCell)) {
                                originalData.set(nameCell, nameCell.textContent);
                            }
                            nameCell.textContent = 'Retainer ' + rowIndex;
                        }
                    });
                }
                
                // Anonymize submarine names and plan names in expanded content
                const subTable = card.querySelector('.sub-table');
                if (subTable) {
                    subTable.querySelectorAll('tr').forEach((row, rowIndex) => {
                        if (rowIndex === 0) return; // Skip header row
                        const nameCell = row.querySelector('td:first-child');
                        if (nameCell) {
                            if (!originalData.has(nameCell)) {
                                originalData.set(nameCell, nameCell.textContent);
                            }
                            nameCell.textContent = 'Submarine ' + rowIndex;
                        }
                        // Anonymize plan name (4th column) with TOP SECRET in red
                        const planCell = row.querySelector('td:nth-child(4)');
                        if (planCell) {
                            if (!originalData.has(planCell)) {
                                originalData.set(planCell, { html: planCell.innerHTML, style: planCell.getAttribute('style') });
                            }
                            planCell.innerHTML = 'TOP SECRET';
                            planCell.style.color = 'var(--accent)';
                        }
                    });
                }
                
                // Anonymize housing info in expanded content
                card.querySelectorAll('.info-row').forEach(row => {
                    const label = row.querySelector('.info-label');
                    const value = row.querySelector('.info-value');
                    if (label && value) {
                        const labelText = label.textContent;
                        if (labelText.includes('Personal House') || labelText.includes('FC House')) {
                            if (!originalData.has(value)) {
                                originalData.set(value, { html: value.innerHTML, style: value.getAttribute('style') });
                            }
                            value.innerHTML = 'TOP SECRET';
                            value.style.color = 'var(--accent)';
                        }
                    }
                });
                
                // Anonymize Player Name @ World
                const playerNameWorld = card.querySelector('.player-name-world');
                if (playerNameWorld) {
                    if (!originalData.has(playerNameWorld)) {
                        originalData.set(playerNameWorld, { text: playerNameWorld.textContent });
                    }
                    playerNameWorld.textContent = 'Toon ' + (cardIndex + 1) + '@Eorzea';
                }
            });
            } catch (e) {
                console.error('Error in anonymizeAll:', e);
            }
        }
        
        function restoreAll() {
            originalData.forEach((value, element) => {
                try {
                    // Skip if element no longer exists in DOM
                    if (!element || !document.body.contains(element)) return;
                    
                    if (element.classList && element.classList.contains('character-name')) {
                        element.innerHTML = value;
                    } else if (typeof value === 'object' && value.html !== undefined) {
                        // Restore plan cells with original HTML and style
                        element.innerHTML = value.html;
                        if (value.style) {
                            element.setAttribute('style', value.style);
                        } else {
                            element.removeAttribute('style');
                        }
                    } else if (typeof value === 'object' && value.text !== undefined) {
                        // Restore player name with original text
                        element.textContent = value.text;
                    } else {
                        element.textContent = value;
                    }
                } catch (e) {
                    console.warn('Error restoring element:', e);
                }
            });
            originalData.clear();
        }
        
        function toggleHideMoney(btn) {
            isMoneyHidden = !isMoneyHidden;
            btn.classList.toggle('active', isMoneyHidden);
            btn.textContent = isMoneyHidden ? '💸' : '💰';
            
            // Toggle all money buttons across all accounts
            document.querySelectorAll('.money-btn').forEach(b => {
                b.classList.toggle('active', isMoneyHidden);
                b.textContent = isMoneyHidden ? '💸' : '💰';
            });
            
            if (isMoneyHidden) {
                hideMoneyAll();
            } else {
                restoreMoneyAll();
            }
        }
        
        function hideMoneyAll(forceRefresh = false) {
            const HIDDEN = '*****';
            
            // Hide Characters summary card (preserve labels, hide numbers only)
            const charTotal = document.querySelector('#sum-total-chars');
            if (charTotal && (forceRefresh || !originalMoneyData.has(charTotal))) {
                if (!forceRefresh) originalMoneyData.set(charTotal, charTotal.textContent);
                charTotal.textContent = '👥 ***';
            }
            const charLevels = document.querySelector('#sum-char-levels');
            if (charLevels && (forceRefresh || !originalMoneyData.has(charLevels))) {
                if (!forceRefresh) originalMoneyData.set(charLevels, charLevels.textContent);
                charLevels.textContent = '*** Lv 25+ | *** Lv 100';
            }
            const charPlots = document.querySelector('#sum-plots');
            if (charPlots && (forceRefresh || !originalMoneyData.has(charPlots))) {
                if (!forceRefresh) originalMoneyData.set(charPlots, { html: charPlots.innerHTML });
                // Preserve structure but hide numbers (including potential subs count if present)
                charPlots.innerHTML = '🏠 *** | 🏨 ***{% if highlight_potential_subs %} | <span id="sum-potential-subs" style="color: #888;">❓ ***</span>{% endif %}';
            }
            
            // Hide summary cards (top section)
            const summarySelectors = [
                '#sum-total-gil', '#sum-treasure', '#sum-with-treasure', '#sum-coffer-dye',
                '#sum-ready-subs', '#sum-total-subs', '#sum-ready-retainers', '#sum-total-retainers',
                '#sum-total-mb', '#sum-max-mb', '#sum-monthly-income', '#sum-monthly-cost',
                '#sum-monthly-profit', '#sum-annual-income', '#sum-annual-profit'
            ];
            summarySelectors.forEach(sel => {
                const el = document.querySelector(sel);
                if (el && (forceRefresh || !originalMoneyData.has(el))) {
                    if (!forceRefresh) originalMoneyData.set(el, el.textContent);
                    el.textContent = HIDDEN;
                }
            });
            
            // Hide summary card sublabels (preserve labels, hide numbers only)
            const fcPoints = document.querySelector('#sum-fc-points');
            if (fcPoints && (forceRefresh || !originalMoneyData.has(fcPoints))) {
                if (!forceRefresh) originalMoneyData.set(fcPoints, fcPoints.textContent);
                fcPoints.textContent = '🪙 *** FC';
            }
            const cofferDyeCounts = document.querySelector('#sum-coffer-dye-counts');
            if (cofferDyeCounts && (forceRefresh || !originalMoneyData.has(cofferDyeCounts))) {
                if (!forceRefresh) originalMoneyData.set(cofferDyeCounts, { html: cofferDyeCounts.innerHTML });
                cofferDyeCounts.innerHTML = '📦 *** 🎨 *** <span id="sum-mb-dye-count" style="color: var(--warning);">🪧 ***</span>';
            }
            const subsStats = document.querySelector('#sum-subs-stats');
            if (subsStats && (forceRefresh || !originalMoneyData.has(subsStats))) {
                if (!forceRefresh) originalMoneyData.set(subsStats, { html: subsStats.innerHTML });
                subsStats.innerHTML = '<span style="color: var(--warning);">Lvl: ***</span> | <span style="color: var(--success);">Farm: ***</span> | <span style="color: #FFB6C1;">Idle: ***</span>';
            }
            const retainersStats = document.querySelector('#sum-retainers-stats');
            if (retainersStats && (forceRefresh || !originalMoneyData.has(retainersStats))) {
                if (!forceRefresh) originalMoneyData.set(retainersStats, { html: retainersStats.innerHTML });
                retainersStats.innerHTML = '<span style="color: var(--warning);">Lvl: ***</span> | <span style="color: var(--success);">Farm: ***</span> | <span style="color: cyan;">Idle: ***</span>';
            }
            const mbMax = document.querySelector('#sum-mb-max');
            if (mbMax && (forceRefresh || !originalMoneyData.has(mbMax))) {
                if (!forceRefresh) originalMoneyData.set(mbMax, mbMax.textContent);
                mbMax.textContent = '*** Max';
            }
            const excludedSubs = document.querySelector('#sum-excluded-subs');
            if (excludedSubs && (forceRefresh || !originalMoneyData.has(excludedSubs))) {
                if (!forceRefresh) originalMoneyData.set(excludedSubs, excludedSubs.textContent);
                excludedSubs.textContent = '❌***';
            }
            const excludedRetainers = document.querySelector('#sum-excluded-retainers');
            if (excludedRetainers && (forceRefresh || !originalMoneyData.has(excludedRetainers))) {
                if (!forceRefresh) originalMoneyData.set(excludedRetainers, excludedRetainers.textContent);
                excludedRetainers.textContent = '❌***';
            }
            const sleepingSubs = document.querySelector('#sum-sleeping-subs');
            if (sleepingSubs && (forceRefresh || !originalMoneyData.has(sleepingSubs))) {
                if (!forceRefresh) originalMoneyData.set(sleepingSubs, sleepingSubs.textContent);
                sleepingSubs.textContent = '😴***';
            }
            const sleepingRetainers = document.querySelector('#sum-sleeping-retainers');
            if (sleepingRetainers && (forceRefresh || !originalMoneyData.has(sleepingRetainers))) {
                if (!forceRefresh) originalMoneyData.set(sleepingRetainers, sleepingRetainers.textContent);
                sleepingRetainers.textContent = '😴***';
            }
            const dailyIncome = document.querySelector('#sum-daily-income');
            if (dailyIncome && (forceRefresh || !originalMoneyData.has(dailyIncome))) {
                if (!forceRefresh) originalMoneyData.set(dailyIncome, dailyIncome.textContent);
                dailyIncome.textContent = '📅 *****/day';
            }
            const restock = document.querySelector('#sum-restock');
            if (restock && (forceRefresh || !originalMoneyData.has(restock))) {
                if (!forceRefresh) originalMoneyData.set(restock, restock.textContent);
                restock.textContent = '♻️ ***d lowest';
            }
            
            // Hide account tab stats
            document.querySelectorAll('.account-stats span').forEach(el => {
                const text = el.textContent;
                if (text.includes('💰') || text.includes('💎') || text.includes('🚢') || 
                    text.includes('👤') || text.includes('📦')) {
                    if (forceRefresh || !originalMoneyData.has(el)) {
                        if (!forceRefresh) originalMoneyData.set(el, { html: el.innerHTML });
                        // Keep emoji, hide values
                        const emoji = text.match(/^[^\\d]*/)[0].trim();
                        el.innerHTML = emoji + ' ' + HIDDEN;
                    }
                }
                // Hide MB items (🪧) for privacy
                if (text.includes('🪧') && text.includes('MB')) {
                    if (forceRefresh || !originalMoneyData.has(el)) {
                        if (!forceRefresh) originalMoneyData.set(el, { html: el.innerHTML });
                        el.innerHTML = '🪧 ' + HIDDEN + ' MB';
                    }
                }
                // Hide MSQ progress (📜) for privacy
                if (text.includes('📜') && text.includes('MSQ')) {
                    if (forceRefresh || !originalMoneyData.has(el)) {
                        if (!forceRefresh) originalMoneyData.set(el, { html: el.innerHTML });
                        el.innerHTML = '📜 ' + HIDDEN + ' MSQ';
                    }
                }
            });
            
            // Hide character card header stats
            document.querySelectorAll('.character-card').forEach(card => {
                // Character gil (in header) - use shorter ** for compact display
                const gilEl = card.querySelector('.character-gil');
                if (gilEl && (forceRefresh || !originalMoneyData.has(gilEl))) {
                    if (!forceRefresh) originalMoneyData.set(gilEl, gilEl.textContent);
                    gilEl.textContent = '** gil';
                }
                
                // Treasure value in header - use shorter ** for compact display
                card.querySelectorAll('.char-header-row span').forEach(span => {
                    const text = span.textContent;
                    if (span.style.color && span.style.color.includes('gold') && text.includes('💎')) {
                        if (forceRefresh || !originalMoneyData.has(span)) {
                            if (!forceRefresh) originalMoneyData.set(span, { html: span.innerHTML });
                            span.innerHTML = '💎 **';
                        }
                    }
                    // MB items, coffers, dyes row (including individual dye counts)
                    if (text.includes('🪧') && text.includes('📦') && text.includes('🎨') && !text.includes('🪙')) {
                        if (forceRefresh || !originalMoneyData.has(span)) {
                            if (!forceRefresh) originalMoneyData.set(span, { html: span.innerHTML });
                            // Use shorter ** for compact display in character cards
                            const SHORT = '**';
                            // Check if individual dyes are shown (🤍🖤🩷)
                            const hasIndividualDyes = text.includes('🤍') || text.includes('🖤') || text.includes('🩷');
                            if (hasIndividualDyes) {
                                span.innerHTML = '🪧 ' + SHORT + ' | 📦 ' + SHORT + ' | 🎨 ' + SHORT + ' 🤍' + SHORT + ' 🖤' + SHORT + ' 🩷' + SHORT;
                            } else {
                                span.innerHTML = '🪧 ' + SHORT + ' | 📦 ' + SHORT + ' | 🎨 ' + SHORT;
                            }
                        }
                    }
                    // FC points, venture coins, tanks, kits, restock row - use shorter ** for compact display
                    if (text.includes('🪙') && text.includes('🛒') && text.includes('⛽') && text.includes('🔧')) {
                        if (forceRefresh || !originalMoneyData.has(span)) {
                            if (!forceRefresh) originalMoneyData.set(span, { html: span.innerHTML });
                            const SHORT = '**';
                            span.innerHTML = '🪙 ' + SHORT + ' | 🛒 ' + SHORT + ' | ⛽ ' + SHORT + ' | 🔧 ' + SHORT + (text.includes('♻️') ? ' | ♻️ ' + SHORT : '');
                        }
                    }
                });
                
                // Expanded section info rows
                card.querySelectorAll('.info-row').forEach(row => {
                    const label = row.querySelector('.info-label');
                    const value = row.querySelector('.info-value');
                    if (label && value) {
                        const labelText = label.textContent;
                        const moneyLabels = [
                            'Character Gil', 'Retainer Gil', 'Treasure Value', 'Coffer + Dye Value',
                            'FC Points', 'Venture Coins', 'Coffers', 'Ceruleum Tanks', 'Repair Kits',
                            'Days Until Restock', 'Daily Income', 'Daily Cost'
                        ];
                        if (moneyLabels.some(ml => labelText.includes(ml))) {
                            if (forceRefresh || !originalMoneyData.has(value)) {
                                if (!forceRefresh) originalMoneyData.set(value, { html: value.innerHTML, style: value.getAttribute('style') });
                                value.innerHTML = HIDDEN;
                            }
                        }
                    }
                });
                
                // Retainer table - hide level, gil, and MB columns
                const retTable = card.querySelector('.ret-table');
                if (retTable) {
                    retTable.querySelectorAll('tr').forEach((row, rowIndex) => {
                        if (rowIndex === 0) return; // Skip header
                        // Level (2nd column)
                        const levelCell = row.querySelector('td:nth-child(2)');
                        if (levelCell && (forceRefresh || !originalMoneyData.has(levelCell))) {
                            if (!forceRefresh) originalMoneyData.set(levelCell, levelCell.textContent);
                            levelCell.textContent = HIDDEN;
                        }
                        // Gil (3rd column)
                        const gilCell = row.querySelector('td:nth-child(3)');
                        if (gilCell && (forceRefresh || !originalMoneyData.has(gilCell))) {
                            if (!forceRefresh) originalMoneyData.set(gilCell, gilCell.textContent);
                            gilCell.textContent = HIDDEN;
                        }
                        // MB items (4th column)
                        const mbCell = row.querySelector('td:nth-child(4)');
                        if (mbCell && (forceRefresh || !originalMoneyData.has(mbCell))) {
                            if (!forceRefresh) originalMoneyData.set(mbCell, mbCell.textContent);
                            mbCell.textContent = HIDDEN;
                        }
                    });
                }
                
                // Submarine table - hide level, build, and status columns
                const subTable = card.querySelector('.sub-table');
                if (subTable) {
                    subTable.querySelectorAll('tr').forEach((row, rowIndex) => {
                        if (rowIndex === 0) return; // Skip header
                        // Level (2nd column)
                        const levelCell = row.querySelector('td:nth-child(2)');
                        if (levelCell && (forceRefresh || !originalMoneyData.has(levelCell))) {
                            if (!forceRefresh) originalMoneyData.set(levelCell, levelCell.textContent);
                            levelCell.textContent = HIDDEN;
                        }
                        // Build (3rd column)
                        const buildCell = row.querySelector('td:nth-child(3)');
                        if (buildCell && (forceRefresh || !originalMoneyData.has(buildCell))) {
                            if (!forceRefresh) originalMoneyData.set(buildCell, buildCell.textContent);
                            buildCell.textContent = HIDDEN;
                        }
                        // Status (5th column)
                        const statusCell = row.querySelector('td:nth-child(5)');
                        if (statusCell && (forceRefresh || !originalMoneyData.has(statusCell))) {
                            if (!forceRefresh) originalMoneyData.set(statusCell, { html: statusCell.innerHTML, className: statusCell.className });
                            statusCell.textContent = HIDDEN;
                            statusCell.className = '';
                        }
                    });
                }
            });
        }
        
        function restoreMoneyAll() {
            originalMoneyData.forEach((value, element) => {
                if (typeof value === 'object' && value.html !== undefined) {
                    element.innerHTML = value.html;
                    if (value.style) {
                        element.setAttribute('style', value.style);
                    } else if (value.style === null) {
                        element.removeAttribute('style');
                    }
                    if (value.className !== undefined) {
                        element.className = value.className;
                    }
                } else {
                    element.textContent = value;
                }
            });
            originalMoneyData.clear();
        }
        
        function expandAllChars(btn) {
            const accountSection = btn.closest('.account-section');
            const cards = accountSection.querySelectorAll('.character-card');
            const collapsedChars = JSON.parse(localStorage.getItem('collapsedChars') || '{}');
            
            cards.forEach(card => {
                const charId = card.dataset.char;
                const header = card.querySelector('.character-header');
                const body = header.nextElementSibling;
                
                header.classList.remove('collapsed');
                body.classList.remove('collapsed');
                card.classList.add('expanded');
                collapsedChars[charId] = false;
            });
            
            localStorage.setItem('collapsedChars', JSON.stringify(collapsedChars));
        }
        
        function collapseAllChars(btn) {
            const accountSection = btn.closest('.account-section');
            const cards = accountSection.querySelectorAll('.character-card');
            const collapsedChars = JSON.parse(localStorage.getItem('collapsedChars') || '{}');
            
            cards.forEach(card => {
                const charId = card.dataset.char;
                const header = card.querySelector('.character-header');
                const body = header.nextElementSibling;
                
                header.classList.add('collapsed');
                body.classList.add('collapsed');
                card.classList.remove('expanded');
                collapsedChars[charId] = true;
            });
            
            localStorage.setItem('collapsedChars', JSON.stringify(collapsedChars));
        }
        
        // Global filter functions for header buttons
        function toggleHideMoneyGlobal() {
            isMoneyHidden = !isMoneyHidden;
            // Update all money buttons including global
            document.querySelectorAll('.money-btn').forEach(b => {
                b.classList.toggle('active', isMoneyHidden);
                b.textContent = isMoneyHidden ? '💸' : '💰';
            });
            if (isMoneyHidden) {
                hideMoneyAll();
            } else {
                restoreMoneyAll();
            }
        }
        
        function toggleAnonymizeGlobal() {
            try {
                isAnonymized = !isAnonymized;
                // Update all anon buttons including global
                document.querySelectorAll('.anon-btn').forEach(b => {
                    b.classList.toggle('active', isAnonymized);
                    b.textContent = isAnonymized ? '🔓' : '🔒';
                });
                if (isAnonymized) {
                    anonymizeAll();
                } else {
                    restoreAll();
                }
            } catch (e) {
                console.error('Error in toggleAnonymizeGlobal:', e);
            }
        }
        
        // Global show player stats - INVERTED: active = show, inactive = hide (default collapsed)
        let isPlayerStatsShown = false;
        
        function toggleHidePlayerStatsGlobal() {
            isPlayerStatsShown = !isPlayerStatsShown;
            const btn = document.getElementById('global-hide-stats-btn');
            if (btn) {
                btn.classList.toggle('active', isPlayerStatsShown);
            }
            
            // Toggle all player stats sections
            document.querySelectorAll('.player-stats-header').forEach(header => {
                if (isPlayerStatsShown) {
                    // Active = show (expand)
                    header.classList.remove('collapsed');
                    const content = header.nextElementSibling;
                    if (content) {
                        content.classList.remove('collapsed');
                    }
                } else {
                    // Inactive = hide (collapse)
                    if (!header.classList.contains('collapsed')) {
                        header.classList.add('collapsed');
                    }
                    const content = header.nextElementSibling;
                    if (content && !content.classList.contains('collapsed')) {
                        content.classList.add('collapsed');
                    }
                }
            });
        }
        
        // Global hide submarines
        let isSubsHidden = false;
        
        function toggleHideSubsGlobal() {
            isSubsHidden = !isSubsHidden;
            const btn = document.getElementById('global-hide-subs-btn');
            if (btn) {
                btn.classList.toggle('active', isSubsHidden);
            }
            
            // Toggle all submarine sections (find by content starting with 🚢)
            document.querySelectorAll('.section-title.collapsible').forEach(header => {
                if (header.textContent.includes('🚢 Submarines')) {
                    if (isSubsHidden) {
                        if (!header.classList.contains('collapsed')) {
                            header.classList.add('collapsed');
                        }
                        const content = header.nextElementSibling;
                        if (content && !content.classList.contains('collapsed')) {
                            content.classList.add('collapsed');
                        }
                    } else {
                        header.classList.remove('collapsed');
                        const content = header.nextElementSibling;
                        if (content) {
                            content.classList.remove('collapsed');
                        }
                    }
                }
            });
        }
        
        // Global hide retainers
        let isRetainersHidden = false;
        
        function toggleHideRetainersGlobal() {
            isRetainersHidden = !isRetainersHidden;
            const btn = document.getElementById('global-hide-retainers-btn');
            if (btn) {
                btn.classList.toggle('active', isRetainersHidden);
            }
            
            // Toggle all retainer sections (find by content starting with 👤)
            document.querySelectorAll('.section-title.collapsible').forEach(header => {
                if (header.textContent.includes('👤 Retainers')) {
                    if (isRetainersHidden) {
                        if (!header.classList.contains('collapsed')) {
                            header.classList.add('collapsed');
                        }
                        const content = header.nextElementSibling;
                        if (content && !content.classList.contains('collapsed')) {
                            content.classList.add('collapsed');
                        }
                    } else {
                        header.classList.remove('collapsed');
                        const content = header.nextElementSibling;
                        if (content) {
                            content.classList.remove('collapsed');
                        }
                    }
                }
            });
        }
        
        // Global show classes (DoW/DoM and DoH/DoL) - INVERTED: active = show, inactive = hide (default collapsed)
        let isClassesShown = false;
        
        function toggleHideClassesGlobal() {
            isClassesShown = !isClassesShown;
            const btn = document.getElementById('global-hide-classes-btn');
            if (btn) {
                btn.classList.toggle('active', isClassesShown);
            }
            
            // Toggle all DoW/DoM and DoH/DoL sections
            document.querySelectorAll('.section-title.collapsible').forEach(header => {
                if (header.textContent.includes('⚔️ DoW/DoM') || header.textContent.includes('🔨 DoH/DoL')) {
                    if (isClassesShown) {
                        // Active = show (expand)
                        header.classList.remove('collapsed');
                        const content = header.nextElementSibling;
                        if (content) {
                            content.classList.remove('collapsed');
                        }
                    } else {
                        // Inactive = hide (collapse)
                        if (!header.classList.contains('collapsed')) {
                            header.classList.add('collapsed');
                        }
                        const content = header.nextElementSibling;
                        if (content && !content.classList.contains('collapsed')) {
                            content.classList.add('collapsed');
                        }
                    }
                }
            });
        }
        
        // Global show currencies - INVERTED: active = show, inactive = hide (default collapsed)
        let isCurrenciesShown = false;
        
        function toggleHideCurrenciesGlobal() {
            isCurrenciesShown = !isCurrenciesShown;
            const btn = document.getElementById('global-hide-currencies-btn');
            if (btn) {
                btn.classList.toggle('active', isCurrenciesShown);
            }
            
            // Toggle all currencies sections
            document.querySelectorAll('.section-title.collapsible').forEach(header => {
                if (header.textContent.includes('💰 Currencies')) {
                    if (isCurrenciesShown) {
                        // Active = show (expand)
                        header.classList.remove('collapsed');
                        const content = header.nextElementSibling;
                        if (content) {
                            content.classList.remove('collapsed');
                        }
                    } else {
                        // Inactive = hide (collapse)
                        if (!header.classList.contains('collapsed')) {
                            header.classList.add('collapsed');
                        }
                        const content = header.nextElementSibling;
                        if (content && !content.classList.contains('collapsed')) {
                            content.classList.add('collapsed');
                        }
                    }
                }
            });
        }
        
        // Track global filter states
        let globalFilters = {
            'personal-house': false,
            'fc-house': false,
            'coffers': false,
            'dyes': false,
            'mb': false,
            'retainers': false,
            'treasure': false,
            'subs': false,
            'msq': false,
            'ready': false,
            'sleeping': false,
            'idle': false,
            'potential_subs': false,
            'processing': false,
            'excluded': false
        };
        
        // Track region filter (only one can be active at a time, or none)
        let activeRegion = null;
        
        function toggleRegionFilter(region) {
            // If clicking the same region, toggle it off
            if (activeRegion === region) {
                activeRegion = null;
            } else {
                activeRegion = region;
            }
            
            // Update button states (only one active at a time)
            ['NA', 'EU', 'JP', 'OCE'].forEach(r => {
                const btn = document.getElementById('region-' + r.toLowerCase() + '-btn');
                if (btn) btn.classList.toggle('active', activeRegion === r);
            });
            
            // Apply region filter to all accounts
            applyAllFilters();
        }
        
        function applyAllFilters() {
            document.querySelectorAll('.account-section').forEach(section => {
                const grid = section.querySelector('.character-grid');
                if (!grid) return;
                const cards = grid.querySelectorAll('.character-card');
                
                cards.forEach(card => {
                    let shouldShow = true;
                    
                    // Check region filter first
                    if (activeRegion && card.dataset.region !== activeRegion) shouldShow = false;
                    
                    // Check all active global filters
                    if (globalFilters['personal-house'] && card.dataset.hasPersonalHouse !== 'true') shouldShow = false;
                    if (globalFilters['fc-house'] && card.dataset.hasFcHouse !== 'true') shouldShow = false;
                    if (globalFilters['coffers'] && card.dataset.hasCoffers !== 'true') shouldShow = false;
                    if (globalFilters['dyes'] && card.dataset.hasDyes !== 'true') shouldShow = false;
                    if (globalFilters['mb'] && card.dataset.hasMb !== 'true') shouldShow = false;
                    if (globalFilters['retainers'] && parseInt(card.dataset.totalRetainers || 0) === 0) shouldShow = false;
                    if (globalFilters['treasure'] && card.dataset.hasTreasure !== 'true') shouldShow = false;
                    if (globalFilters['subs'] && parseInt(card.dataset.totalSubs || 0) === 0) shouldShow = false;
                    if (globalFilters['msq'] && parseInt(card.dataset.msqPercent || 0) === 0) shouldShow = false;
                    if (globalFilters['ready'] && card.dataset.hasReady !== 'true') shouldShow = false;
                    if (globalFilters['sleeping'] && card.dataset.hasSleeping !== 'true') shouldShow = false;
                    if (globalFilters['idle'] && card.dataset.hasIdle !== 'true') shouldShow = false;
                    if (globalFilters['potential_subs'] && card.dataset.hasPotentialSubs !== 'true') shouldShow = false;
                    if (globalFilters['processing'] && card.dataset.isProcessing !== 'true') shouldShow = false;
                    if (globalFilters['excluded'] && card.dataset.hasExclusion !== 'true') shouldShow = false;
                    
                    card.style.display = shouldShow ? '' : 'none';
                });
            });
        }
        
        function toggleFilterGlobal(filterType) {
            globalFilters[filterType] = !globalFilters[filterType];
            const isActive = globalFilters[filterType];
            
            // Update global button state
            const btnId = {
                'personal-house': 'global-house-btn',
                'fc-house': 'global-fc-btn',
                'coffers': 'global-coffers-btn',
                'dyes': 'global-dyes-btn',
                'mb': 'global-mb-btn',
                'retainers': 'global-retainers-btn',
                'treasure': 'global-treasure-btn',
                'subs': 'global-subs-btn',
                'msq': 'global-msq-btn',
                'ready': 'global-ready-btn',
                'sleeping': 'global-sleeping-btn',
                'idle': 'global-idle-btn',
                'potential_subs': 'global-potential-subs-btn',
                'processing': 'global-processing-btn',
                'excluded': 'global-excluded-btn'
            }[filterType];
            const globalBtn = document.getElementById(btnId);
            if (globalBtn) globalBtn.classList.toggle('active', isActive);
            
            // Apply all filters (including region filter)
            applyAllFilters();
        }
        
        function expandAllCharsGlobal() {
            const collapsedChars = JSON.parse(localStorage.getItem('collapsedChars') || '{}');
            document.querySelectorAll('.character-card').forEach(card => {
                const charId = card.dataset.char;
                const header = card.querySelector('.character-header');
                const body = header.nextElementSibling;
                header.classList.remove('collapsed');
                body.classList.remove('collapsed');
                card.classList.add('expanded');
                collapsedChars[charId] = false;
            });
            localStorage.setItem('collapsedChars', JSON.stringify(collapsedChars));
        }
        
        function collapseAllCharsGlobal() {
            const collapsedChars = JSON.parse(localStorage.getItem('collapsedChars') || '{}');
            document.querySelectorAll('.character-card').forEach(card => {
                const charId = card.dataset.char;
                const header = card.querySelector('.character-header');
                const body = header.nextElementSibling;
                header.classList.add('collapsed');
                body.classList.add('collapsed');
                card.classList.remove('expanded');
                collapsedChars[charId] = true;
            });
            localStorage.setItem('collapsedChars', JSON.stringify(collapsedChars));
        }
        
        function restoreCollapsedState() {
            const collapsedAccounts = JSON.parse(localStorage.getItem('collapsedAccounts') || '{}');
            document.querySelectorAll('.account-section').forEach(section => {
                const accountName = section.dataset.account;
                const header = section.querySelector('.account-header');
                const sortBar = section.querySelector('.sort-bar');
                const content = section.querySelector('.account-content');
                
                // Default to collapsed if not in localStorage
                const shouldBeCollapsed = collapsedAccounts[accountName] !== false;
                
                if (shouldBeCollapsed) {
                    header.classList.add('collapsed');
                    if (sortBar) sortBar.classList.add('collapsed');
                    content.classList.add('collapsed');
                } else {
                    header.classList.remove('collapsed');
                    if (sortBar) sortBar.classList.remove('collapsed');
                    content.classList.remove('collapsed');
                }
            });
            
            // Sync global accounts button state
            const accountSections = document.querySelectorAll('.account-section');
            let expandedCount = 0;
            accountSections.forEach(section => {
                const header = section.querySelector('.account-header');
                if (!header.classList.contains('collapsed')) expandedCount++;
            });
            allAccountsExpanded = expandedCount === accountSections.length;
            const accountsBtn = document.getElementById('global-accounts-btn');
            if (accountsBtn) {
                accountsBtn.textContent = allAccountsExpanded ? '▼' : '▶';
                accountsBtn.title = allAccountsExpanded ? 'Collapse All Accounts' : 'Expand All Accounts';
            }
            
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
                
                // Update timestamp always
                document.getElementById('last-updated').textContent = data.last_updated;
                
                // Only update summary cards and account stats if money is NOT hidden
                if (!isMoneyHidden) {
                    document.getElementById('sum-total-gil').textContent = formatNumber(data.summary.total_gil);
                    document.getElementById('sum-treasure').textContent = formatNumber(data.summary.total_treasure);
                    document.getElementById('sum-with-treasure').textContent = formatNumber(data.summary.total_with_treasure);
                    document.getElementById('sum-ready-subs').textContent = data.summary.ready_subs;
                    document.getElementById('sum-total-subs').textContent = data.summary.enabled_subs;
                    document.getElementById('sum-ready-retainers').textContent = data.summary.ready_retainers;
                    document.getElementById('sum-total-retainers').textContent = data.summary.enabled_retainers;
                    document.getElementById('sum-total-mb').textContent = data.summary.total_mb_items;
                    document.getElementById('sum-max-mb').textContent = formatNumber(data.summary.max_mb_items);
                    // Update max MB count if element exists
                    const maxMbCountEl = document.getElementById('sum-max-mb-count');
                    if (maxMbCountEl) maxMbCountEl.textContent = data.summary.max_mb_retainer_count;
                    document.getElementById('sum-monthly-income').textContent = formatNumber(Math.floor(data.summary.monthly_income));
                    document.getElementById('sum-monthly-cost').textContent = formatNumber(Math.floor(data.summary.monthly_cost));
                    document.getElementById('sum-annual-income').textContent = formatNumber(Math.floor(data.summary.annual_income));
                    document.getElementById('sum-annual-profit').textContent = formatNumber(Math.floor(data.summary.annual_profit));
                    
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
                            // Update max MB count if element exists
                            const accMaxMbCount = section.querySelector('.acc-max-mb-count');
                            if (accMaxMbCount) accMaxMbCount.textContent = account.max_mb_retainer_count;
                            // Update mb-max class on account stats span
                            const mbSpan = section.querySelector('.acc-mb').closest('span');
                            if (mbSpan) {
                                if (account.has_max_mb_retainer) {
                                    mbSpan.classList.add('mb-max');
                                } else {
                                    mbSpan.classList.remove('mb-max');
                                }
                            }
                        }
                    });
                    
                    // Update character card has-max-mb class
                    data.accounts.forEach(account => {
                        account.characters.forEach(char => {
                            const card = document.querySelector(`[data-char="${char.cid}"]`);
                            if (card) {
                                if (char.has_max_mb_retainer) {
                                    card.classList.add('has-max-mb');
                                } else {
                                    card.classList.remove('has-max-mb');
                                }
                            }
                        });
                    });
                }
                
                // Re-apply anonymize if active
                if (isAnonymized) {
                    originalData.clear();
                    anonymizeAll();
                }
                
                console.log('Data refreshed at', data.last_updated);
            } catch (error) {
                console.error('Failed to refresh data:', error);
            }
        }
        
        // Set dynamic sticky positions based on sticky-top-section height
        function updateStickyPositions() {
            const stickyTop = document.querySelector('.sticky-top-section');
            const firstAccountHeader = document.querySelector('.account-header');
            if (stickyTop) {
                const stickyHeight = stickyTop.offsetHeight;
                const accountHeaderHeight = firstAccountHeader ? firstAccountHeader.offsetHeight : 45;
                document.querySelectorAll('.account-header').forEach(el => {
                    el.style.top = stickyHeight + 'px';
                });
                document.querySelectorAll('.sort-bar').forEach(el => {
                    el.style.top = (stickyHeight + accountHeaderHeight) + 'px';
                });
            }
        }
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {
            restoreCollapsedState();
            updateStickyPositions();
            window.addEventListener('resize', updateStickyPositions);
            
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
# Map Page Data Collection
# ===============================================
# Region character limits per account
REGION_CHAR_LIMITS = {"NA": 40, "EU": 40, "JP": 40, "OCE": 39}
MAX_CHARS_PER_WORLD = 8
MAX_PLOTS_PER_WARD = 60
DISTRICT_ORDER = ["Goblet", "LB", "Mist", "Empyreum", "Shirogane"]


def get_map_data():
    """
    Collect all data needed for the /map/ page:
    - Plot locations by district/ward with character details
    - Characters not in FC grouped by account
    - Per-account, per-region, per-world character counts
    - Capacity calculations for FC planning
    """
    plot_list = []           # All individual plot entries
    district_ward_map = {}   # district -> ward -> [plot entries]
    seen_fc_plots = set()    # Deduplicate FC plots by world+district+ward+plot (same as main page)
    no_fc_chars = []         # Characters not in any FC
    account_summaries = []   # Per-account capacity info

    # First pass: build global FC manager map across ALL accounts
    # Maps fc_key -> {name, account} for the first char with active subs per FC
    global_fc_managers = {}
    for account in account_locations:
        auto_path = account["auto_path"]
        if not os.path.isfile(auto_path):
            continue
        try:
            with open(auto_path, 'r', encoding='utf-8-sig') as f:
                pre_data = json.load(f)
        except Exception:
            continue
        pre_fc_data = extract_fc_data(pre_data)
        pre_characters = collect_characters(pre_data, account["nickname"])
        pre_housing = {}
        lfstrm_path = account.get("lfstrm_path", "")
        if lfstrm_path:
            pre_housing = load_lifestream_data(lfstrm_path)
        for char in pre_characters:
            cid = char.get("CID", 0)
            if not bool(char.get("OfflineSubmarineData", [])):
                continue
            if char.get("ExcludeWorkshop", False) if HONOR_AR_EXCLUSIONS else False:
                continue
            world = char.get("World", "Unknown")
            name = char.get("Name", "Unknown")
            fc_name = pre_fc_data[cid].get("Name", "") if cid in pre_fc_data else ""
            has_fc_house = cid in pre_housing and pre_housing[cid].get('fc') is not None
            fc_key = None
            if has_fc_house:
                fcd = pre_housing[cid]['fc']
                fc_key = f"{world}_{fcd['district']}_W{fcd['ward']}_P{fcd['plot']}"
            elif fc_name:
                fc_key = f"{world}_{fc_name}"
            if fc_key and fc_key not in global_fc_managers:
                global_fc_managers[fc_key] = {"name": name, "account": account["nickname"]}

    sub_planner_accounts = []  # Per-account submarine planner data

    for account in account_locations:
        auto_path = account["auto_path"]
        if not os.path.isfile(auto_path):
            continue

        try:
            with open(auto_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
        except Exception:
            continue

        build_plan_name_lookup(data)
        fc_data = extract_fc_data(data)
        characters = collect_characters(data, account["nickname"])

        # Scan Altoholic for highest_level
        alto_map = {}
        alto_path = account.get("alto_path", "")
        if alto_path:
            alto_map = scan_altoholic_db(alto_path)

        # Load Lifestream housing
        housing_map = {}
        lfstrm_path = account.get("lfstrm_path", "")
        if lfstrm_path:
            housing_map = load_lifestream_data(lfstrm_path)

        # Track per-account stats
        acc_chars_total = 0
        acc_chars_in_fc = 0
        acc_chars_in_fc_no_subs = 0  # orange: FC house no subs OR duplicate FC (managed by alt)
        acc_chars_no_fc = 0
        acc_chars_excluded = 0
        acc_region_counts = {}   # region -> count of chars
        acc_world_counts = {}    # world -> count of chars
        acc_world_fc_counts = {} # world -> count of unique FCs with subs (green)
        acc_world_fc_nosubs_counts = {} # world -> count of managed-by-alt (orange)
        acc_world_excluded_counts = {} # world -> count of excluded chars
        acc_region_fc = {}       # region -> count of unique FCs with subs (green)
        acc_region_fc_nosubs = {} # region -> count of managed-by-alt (orange)
        acc_region_excluded = {} # region -> count of excluded chars
        acc_no_fc_list = []      # chars not in FC for this account
        seen_fc_keys = {}        # FC plot dedup: fc_key -> first char name that claimed it
        per_world_chars = {}     # world -> list of {name, status, fc_name} for clickable UI
        acc_sub_chars = []       # Characters with subs for Sub Planner

        for char in characters:
            cid = char.get("CID", 0)
            name = char.get("Name", "Unknown")
            world = char.get("World", "Unknown")
            region = region_from_world(world)

            # Get highest level from altoholic
            highest_level = 0
            if cid in alto_map:
                highest_level = alto_map[cid].get("highest_level", 0)

            # FC membership for capacity planner
            fc_name = ""
            if cid in fc_data:
                fc_name = fc_data[cid].get("Name", "")

            # Check AR exclusion settings for this character
            exclude_workshop = char.get("ExcludeWorkshop", False) if HONOR_AR_EXCLUSIONS else False
            is_excluded = exclude_workshop

            has_subs = bool(char.get("OfflineSubmarineData", []))
            has_fc_house = cid in housing_map and housing_map[cid].get('fc') is not None

            # Build FC key for dedup (same plot = same FC = same earnings)
            fc_key = None
            if has_fc_house:
                fcd = housing_map[cid]['fc']
                fc_key = f"{world}_{fcd['district']}_W{fcd['ward']}_P{fcd['plot']}"
            elif fc_name:
                fc_key = f"{world}_{fc_name}"

            # Classify character into 4 categories:
            # GREEN  (in_fc):         unique FC with active subs
            # ORANGE (in_fc_no_subs): managed by alt — FC house no subs, or duplicate FC with subs
            # GRAY   (excluded):      ExcludeWorkshop enabled
            # YELLOW (can_join):      not in any FC
            if is_excluded:
                char_status = "excluded"
            elif has_subs:
                if fc_key and fc_key in seen_fc_keys:
                    char_status = "fc_managed"  # duplicate FC — subs managed by another toon
                else:
                    char_status = "in_fc"  # unique FC with active subs
                    if fc_key:
                        seen_fc_keys[fc_key] = {"name": name, "account": account["nickname"]}
            elif has_fc_house:
                char_status = "fc_managed"  # has FC plot but no subs on this char
            else:
                char_status = "can_join"

            acc_chars_total += 1
            if char_status == "excluded":
                acc_chars_excluded += 1
            elif char_status == "in_fc":
                acc_chars_in_fc += 1
            elif char_status == "fc_managed":
                acc_chars_in_fc_no_subs += 1
            else:
                acc_chars_no_fc += 1

            # Region/world counts
            if region:
                acc_region_counts[region] = acc_region_counts.get(region, 0) + 1
                if char_status == "excluded":
                    acc_region_excluded[region] = acc_region_excluded.get(region, 0) + 1
                elif char_status == "in_fc":
                    acc_region_fc[region] = acc_region_fc.get(region, 0) + 1
                elif char_status == "fc_managed":
                    acc_region_fc_nosubs[region] = acc_region_fc_nosubs.get(region, 0) + 1
            if world:
                acc_world_counts[world] = acc_world_counts.get(world, 0) + 1
                if char_status == "excluded":
                    acc_world_excluded_counts[world] = acc_world_excluded_counts.get(world, 0) + 1
                elif char_status == "in_fc":
                    acc_world_fc_counts[world] = acc_world_fc_counts.get(world, 0) + 1
                elif char_status == "fc_managed":
                    acc_world_fc_nosubs_counts[world] = acc_world_fc_nosubs_counts.get(world, 0) + 1

            # Track character for clickable world UI
            if world not in per_world_chars:
                per_world_chars[world] = []
            char_info = {
                "name": name,
                "status": char_status,
                "fc_name": fc_name,
            }
            if char_status == "fc_managed" and fc_key and fc_key in global_fc_managers:
                mgr = global_fc_managers[fc_key]
                char_info["managed_by"] = mgr["name"]
                char_info["managed_by_account"] = mgr["account"]
            per_world_chars[world].append(char_info)

            # Characters not in FC (can_join or excluded — not green/orange)
            if char_status in ("can_join", "excluded"):
                char_entry = {
                    "name": name,
                    "world": world,
                    "region": region,
                    "highest_level": highest_level,
                    "account": account["nickname"],
                    "has_fc_house": False,
                    "has_private_house": False,
                    "is_excluded": is_excluded,
                }
                if cid in housing_map:
                    if housing_map[cid].get('fc'):
                        char_entry["has_fc_house"] = True
                    if housing_map[cid].get('private'):
                        char_entry["has_private_house"] = True
                        pd = housing_map[cid]['private']
                        char_entry["private_house"] = f"{pd['district']} W{pd['ward']} P{pd['plot']}"
                acc_no_fc_list.append(char_entry)
                no_fc_chars.append(char_entry)

            # Collect plot data from housing_map
            if cid in housing_map:
                for plot_type in ['private', 'fc']:
                    pd = housing_map[cid].get(plot_type)
                    if pd:
                        # Deduplicate FC plots by world+district+ward+plot (same as main page unique_fc_plots)
                        plot_key = f"{world}_{pd['district']}_W{pd['ward']}_P{pd['plot']}"
                        if plot_type == 'fc':
                            if plot_key in seen_fc_plots:
                                continue  # Skip duplicate FC plot (shared by multiple chars in same FC)
                            seen_fc_plots.add(plot_key)

                        entry = {
                            "type": plot_type,
                            "district": pd['district'],
                            "ward": pd['ward'],
                            "plot": pd['plot'],
                            "world": world,
                            "region": region,
                            "character": name,
                            "account": account["nickname"],
                            "fc_name": fc_name if plot_type == 'fc' else "",
                        }
                        plot_list.append(entry)

                        # Build district -> ward map
                        dist = pd['district']
                        if dist not in district_ward_map:
                            district_ward_map[dist] = {}
                        ward = pd['ward']
                        if ward not in district_ward_map[dist]:
                            district_ward_map[dist][ward] = []
                        district_ward_map[dist][ward].append(entry)

            # Collect submarine data for Sub Planner
            submarines = parse_submarine_data(char)
            if submarines:
                subs_sleeping = not char.get("WorkshopEnabled", True)
                sub_list = []
                for s in submarines:
                    # Compact ETA: "R" if ready, "Xh" or "Xm" or "XdYh"
                    eta = "R"
                    if not s.get("is_ready", False) and s.get("return_time"):
                        delta = datetime.datetime.fromtimestamp(s["return_time"]) - datetime.datetime.now()
                        secs = delta.total_seconds()
                        if secs > 0:
                            hrs = int(secs // 3600)
                            mins = int((secs % 3600) // 60)
                            if hrs >= 24:
                                eta = f"{hrs // 24}d{hrs % 24}h"
                            elif hrs > 0:
                                eta = f"{hrs}h"
                            else:
                                eta = f"{mins}m"
                    sub_list.append({
                        "name": s["name"],
                        "level": s["level"],
                        "build": s["build"],
                        "plan_name": s.get("plan_name", ""),
                        "is_farming": s.get("is_farming", False),
                        "is_leveling": s.get("is_leveling", False),
                        "eta": eta,
                    })

                # Character inventory stats
                ceruleum = char.get("Ceruleum", 0)
                repair_kits = char.get("RepairKits", 0)
                inventory_space = char.get("InventorySpace", 0)
                total_tanks_per_day = sum(s.get("tanks_per_day", 0) for s in submarines)
                total_kits_per_day = sum(s.get("kits_per_day", 0) for s in submarines)
                restock_days = None
                if total_tanks_per_day > 0 and total_kits_per_day > 0:
                    d_tanks = ceruleum / total_tanks_per_day if ceruleum > 0 else 0
                    d_kits = repair_kits / total_kits_per_day if repair_kits > 0 else 0
                    restock_days = int(min(d_tanks, d_kits))

                acc_sub_chars.append({
                    "name": name,
                    "world": world,
                    "region": region,
                    "fc_name": fc_name,
                    "excluded": is_excluded,
                    "sleeping": subs_sleeping,
                    "subs": sub_list,
                    "tanks": ceruleum,
                    "kits": repair_kits,
                    "restock_days": restock_days,
                    "inventory": inventory_space,
                })

        # Calculate capacity per region
        region_capacity = []
        for reg in ["NA", "EU", "JP", "OCE"]:
            limit = REGION_CHAR_LIMITS[reg]
            current = acc_region_counts.get(reg, 0)
            in_fc_count = acc_region_fc.get(reg, 0)
            in_fc_no_subs_count = acc_region_fc_nosubs.get(reg, 0)
            excluded_count = acc_region_excluded.get(reg, 0)
            not_in_fc = current - in_fc_count - in_fc_no_subs_count - excluded_count
            remaining = limit - current

            # Per-world breakdown for this region
            world_set = NA_WORLDS if reg == "NA" else EU_WORLDS if reg == "EU" else JP_WORLDS if reg == "JP" else OCE_WORLDS
            world_breakdown = []
            for w in sorted(world_set):
                w_title = w.title()
                count = acc_world_counts.get(w_title, 0)
                if count > 0:
                    w_in_fc = acc_world_fc_counts.get(w_title, 0)
                    w_in_fc_no_subs = acc_world_fc_nosubs_counts.get(w_title, 0)
                    w_excluded = acc_world_excluded_counts.get(w_title, 0)
                    w_not_in_fc = count - w_in_fc - w_in_fc_no_subs - w_excluded
                    world_breakdown.append({"world": w_title, "count": count, "in_fc": w_in_fc, "in_fc_no_subs": w_in_fc_no_subs, "not_in_fc": w_not_in_fc, "excluded": w_excluded, "max": MAX_CHARS_PER_WORLD, "remaining": MAX_CHARS_PER_WORLD - count, "chars": per_world_chars.get(w_title, [])})

            region_capacity.append({
                "region": reg,
                "limit": limit,
                "current": current,
                "in_fc": in_fc_count,
                "in_fc_no_subs": in_fc_no_subs_count,
                "not_in_fc": not_in_fc,
                "excluded": excluded_count,
                "remaining": remaining,
                "worlds": world_breakdown,
            })

        account_summaries.append({
            "nickname": account["nickname"],
            "total_chars": acc_chars_total,
            "in_fc": acc_chars_in_fc,
            "in_fc_no_subs": acc_chars_in_fc_no_subs,
            "not_in_fc": acc_chars_no_fc,
            "excluded": acc_chars_excluded,
            "no_fc_chars": acc_no_fc_list,
            "region_capacity": region_capacity,
        })

        if acc_sub_chars:
            sub_planner_accounts.append({
                "nickname": account["nickname"],
                "characters": acc_sub_chars,
                "total_subs": sum(len(c["subs"]) for c in acc_sub_chars),
                "total_chars": len(acc_sub_chars),
            })

    # Build district summary for visualization (ordered: Goblet, LB, Mist, Empyreum, Shirogane)
    district_summary = {}
    # Process in defined order, then any extras alphabetically
    ordered_districts = [d for d in DISTRICT_ORDER if d in district_ward_map]
    ordered_districts += sorted(d for d in district_ward_map if d not in DISTRICT_ORDER)
    for dist in ordered_districts:
        wards = district_ward_map[dist]
        ward_list = []
        for ward_num in sorted(wards.keys()):
            plots = sorted(wards[ward_num], key=lambda p: p['plot'])
            fc_count = sum(1 for p in plots if p['type'] == 'fc')
            personal_count = sum(1 for p in plots if p['type'] == 'private')
            ward_list.append({
                "ward": ward_num,
                "plots": plots,
                "fc_count": fc_count,
                "personal_count": personal_count,
                "total": len(plots),
            })
        district_summary[dist] = {
            "wards": ward_list,
            "total_plots": sum(w['total'] for w in ward_list),
            "total_fc": sum(w['fc_count'] for w in ward_list),
            "total_personal": sum(w['personal_count'] for w in ward_list),
            "ward_count": len(ward_list),
        }

    total_plots = sum(d['total_plots'] for d in district_summary.values())
    total_fc = sum(d['total_fc'] for d in district_summary.values())
    total_personal = sum(d['total_personal'] for d in district_summary.values())

    # Aggregate character counts across all accounts
    total_chars = sum(a["total_chars"] for a in account_summaries)
    total_in_fc = sum(a["in_fc"] for a in account_summaries)
    total_in_fc_no_subs = sum(a["in_fc_no_subs"] for a in account_summaries)
    total_not_in_fc = sum(a["not_in_fc"] for a in account_summaries)
    num_accounts = len(account_summaries)

    # Max capacity: sum of all region limits across all accounts
    max_capacity = 0
    for acc in account_summaries:
        for rc in acc["region_capacity"]:
            max_capacity += rc["limit"]

    # FC coverage percentage
    fc_coverage_pct = round(total_in_fc / total_chars * 100, 1) if total_chars > 0 else 0

    # Max ward total across all districts (for bar chart scaling)
    max_ward_total = 0
    for dist_data in district_summary.values():
        for w in dist_data["wards"]:
            if w["total"] > max_ward_total:
                max_ward_total = w["total"]

    return {
        "plots": plot_list,
        "district_summary": district_summary,
        "district_ward_map": district_ward_map,
        "no_fc_chars": no_fc_chars,
        "account_summaries": account_summaries,
        "total_plots": total_plots,
        "total_fc": total_fc,
        "total_personal": total_personal,
        "total_chars": total_chars,
        "total_in_fc": total_in_fc,
        "total_in_fc_no_subs": total_in_fc_no_subs,
        "total_not_in_fc": total_not_in_fc,
        "num_accounts": num_accounts,
        "max_capacity": max_capacity,
        "fc_coverage_pct": fc_coverage_pct,
        "max_ward_total": max_ward_total,
        "sub_planner_accounts": sub_planner_accounts,
        "plot_regions": sorted(set(p["region"] for p in plot_list if p.get("region"))),
        "plot_account_names": sorted(set(p["account"] for p in plot_list if p.get("account"))),
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# ===============================================
# Map Page HTML Template
# ===============================================
MAP_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plot Map - AutoRetainer Dashboard</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🗺️</text></svg>">
    <style>
        :root {
            --bg-primary: #1a1a2e;
            --bg-secondary: #16213e;
            --bg-card: #0f3460;
            --bg-hover: #1a4a7a;
            --text-primary: #e8e8e8;
            --text-secondary: #a0a0a0;
            --accent: #3a7aaa;
            --accent-light: #4a9aca;
            --accent-highlight: #e94560;
            --success: #00d26a;
            --warning: #ffc107;
            --border: #2a2a4a;
            --gold: #ffd700;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: var(--bg-primary); color: var(--text-primary); min-height: 100vh; }

        .top-bar {
            background: var(--bg-secondary);
            border-bottom: 2px solid var(--border);
            padding: 12px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .top-bar h1 { font-size: 1.3rem; color: var(--accent-light); }
        .top-bar h1 span { color: var(--text-secondary); font-weight: 400; font-size: 0.85rem; margin-left: 8px; }
        .top-bar a { color: var(--accent-light); text-decoration: none; font-size: 0.9rem; padding: 6px 14px; border: 1px solid var(--border); border-radius: 6px; transition: all 0.2s; }
        .top-bar a:hover { background: var(--bg-hover); border-color: var(--accent); }
        .top-bar a.active { background: var(--accent); color: #fff; border-color: var(--accent); }

        .container { max-width: 1700px; margin: 0 auto; padding: 20px; }

        /* Summary cards */
        .summary-row {
            display: flex;
            gap: 16px;
            margin-bottom: 24px;
            flex-wrap: wrap;
        }
        .summary-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px 24px;
            flex: 1;
            min-width: 160px;
            text-align: center;
        }
        .summary-card .value { font-size: 2rem; font-weight: 700; color: var(--accent-light); }
        .summary-card .label { font-size: 0.8rem; color: var(--text-secondary); margin-top: 2px; }
        .summary-card .sublabel { font-size: 0.7rem; color: var(--text-secondary); margin-top: 4px; }
        .summary-card.fc .value { color: var(--success); }
        .summary-card.personal .value { color: var(--gold); }
        .summary-card.warn .value { color: var(--warning); }
        .summary-card.accent .value { color: var(--accent-highlight); }

        .info-disclaimer {
            background: rgba(58, 122, 170, 0.1);
            border: 1px solid rgba(58, 122, 170, 0.3);
            border-radius: 8px;
            padding: 12px 16px;
            margin: 8px 0 16px 0;
            font-size: 0.78rem;
            color: var(--text-secondary);
            line-height: 1.5;
        }
        .info-disclaimer strong { color: var(--accent-light); }

        /* Section headers */
        .section-header {
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--accent-light);
            margin: 28px 0 14px 0;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* District visualization */
        .district-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 12px;
            margin-bottom: 24px;
        }
        .district-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            overflow: visible;
            transition: border-color 0.2s;
        }
        .district-card:hover { border-color: var(--accent); }
        .district-card-header {
            padding: 10px 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            border-radius: 10px 10px 0 0;
            background: var(--bg-card);
        }
        .district-name { font-weight: 700; font-size: 1.05rem; }
        .district-count {
            font-size: 0.8rem;
            color: var(--text-secondary);
            display: flex;
            gap: 10px;
        }
        .district-count .fc-tag { color: var(--success); }
        .district-count .personal-tag { color: var(--gold); }
        .district-body { padding: 10px 10px; border-radius: 0 0 10px 10px; background: var(--bg-card); }

        /* Ward rows */
        .ward-row {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 5px 0;
            border-bottom: 1px solid rgba(255,255,255,0.04);
        }
        .ward-row:last-child { border-bottom: none; }
        .ward-label {
            font-size: 0.75rem;
            color: var(--text-secondary);
            width: 30px;
            flex-shrink: 0;
            font-weight: 600;
        }
        .ward-plots { display: flex; gap: 3px; flex-wrap: wrap; flex: 1; }

        /* Plot dots */
        .plot-dot {
            width: 18px;
            height: 18px;
            border-radius: 3px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.48rem;
            font-weight: 700;
            cursor: default;
            position: relative;
            transition: transform 0.15s;
        }
        .plot-dot:hover { transform: scale(1.4); z-index: 50; }
        .plot-dot.fc { background: var(--success); color: #000; }
        .plot-dot.private { background: var(--gold); color: #000; }

        /* Tooltip */
        .plot-dot .tooltip {
            display: none;
            position: absolute;
            bottom: 130%;
            left: 50%;
            transform: translateX(-50%);
            background: #111;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 6px 10px;
            white-space: nowrap;
            font-size: 0.75rem;
            color: var(--text-primary);
            z-index: 50;
            pointer-events: none;
            font-weight: 400;
        }
        .plot-dot:hover .tooltip { display: block; }

        /* Ward bar chart */
        .ward-bar-container { margin-top: 10px; }
        .ward-bar-row {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 4px;
        }
        .ward-bar-label {
            font-size: 0.75rem;
            color: var(--text-secondary);
            width: 52px;
            flex-shrink: 0;
            text-align: right;
        }
        .ward-bar-track {
            flex: 1;
            height: 14px;
            background: rgba(255,255,255,0.05);
            border-radius: 3px;
            overflow: hidden;
            display: flex;
        }
        .ward-bar-fc {
            height: 100%;
            background: var(--success);
            transition: width 0.4s;
        }
        .ward-bar-personal {
            height: 100%;
            background: var(--gold);
            transition: width 0.4s;
        }
        .ward-bar-value {
            font-size: 0.7rem;
            color: var(--text-secondary);
            width: 40px;
            text-align: right;
            flex-shrink: 0;
        }

        /* View toggle */
        .view-toggle {
            display: flex;
            gap: 4px;
            background: var(--bg-secondary);
            border-radius: 8px;
            padding: 3px;
            border: 1px solid var(--border);
        }
        .view-toggle button {
            background: none;
            border: none;
            color: var(--text-secondary);
            padding: 5px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.2s;
        }
        .view-toggle button.active { background: var(--accent); color: #fff; }
        .view-toggle button:hover:not(.active) { color: var(--text-primary); }

        /* FC Planner section */
        .planner-controls {
            display: flex;
            gap: 12px;
            align-items: center;
            flex-wrap: wrap;
            margin-bottom: 16px;
        }
        .planner-controls label { font-size: 0.85rem; color: var(--text-secondary); }
        .planner-controls select {
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 0.85rem;
            cursor: pointer;
        }
        .planner-controls select:focus { outline: none; border-color: var(--accent); }

        /* Region cards */
        .region-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        .region-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
        }
        .region-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        .region-card-header h3 { font-size: 1.05rem; color: var(--accent-light); }
        .region-badge {
            font-size: 0.75rem;
            padding: 3px 10px;
            border-radius: 12px;
            font-weight: 600;
        }
        .region-badge.full { background: var(--accent-highlight); color: #fff; }
        .region-badge.available { background: var(--success); color: #000; }

        /* Capacity bar */
        .capacity-bar {
            height: 28px;
            background: rgba(255,255,255,0.05);
            border-radius: 6px;
            overflow: hidden;
            display: flex;
            margin: 8px 0;
            position: relative;
        }
        .capacity-bar .in-fc {
            height: 100%;
            background: var(--success);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            font-weight: 700;
            color: #000;
            min-width: 20px;
            transition: width 0.4s;
        }
        .capacity-bar .in-fc-no-subs {
            height: 100%;
            background: #e67e22;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            font-weight: 700;
            color: #000;
            min-width: 20px;
            transition: width 0.4s;
        }
        .capacity-bar .not-in-fc {
            height: 100%;
            background: var(--warning);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            font-weight: 700;
            color: #000;
            min-width: 20px;
            transition: width 0.4s;
        }
        .capacity-bar .excluded {
            height: 100%;
            background: rgba(255,255,255,0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            font-weight: 700;
            color: rgba(255,255,255,0.5);
            min-width: 20px;
            transition: width 0.4s;
        }
        .capacity-bar .remaining-space {
            height: 100%;
            flex: 1;
        }
        .capacity-legend {
            display: flex;
            gap: 16px;
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-top: 6px;
        }
        .capacity-legend span { display: flex; align-items: center; gap: 4px; cursor: default; }
        .legend-dot { width: 10px; height: 10px; border-radius: 3px; display: inline-block; }
        .legend-dot.fc-dot { background: var(--success); }
        .legend-dot.fc-nosubs-dot { background: #e67e22; }
        .legend-dot.nofc-dot { background: var(--warning); }
        .legend-dot.excluded-dot { background: rgba(255,255,255,0.15); }
        .legend-dot.empty-dot { background: rgba(255,255,255,0.1); }

        .capacity-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-top: 12px;
            text-align: center;
        }
        .cap-stat { background: rgba(255,255,255,0.03); border-radius: 6px; padding: 8px; }
        .cap-stat .cap-val { font-size: 1.1rem; font-weight: 700; }
        .cap-stat .cap-lbl { font-size: 0.7rem; color: var(--text-secondary); }
        .cap-stat.green .cap-val { color: var(--success); }
        .cap-stat.orange .cap-val { color: #e67e22; }
        .cap-stat.yellow .cap-val { color: var(--warning); }
        .cap-stat.gray .cap-val { color: rgba(255,255,255,0.5); }
        .cap-stat.blue .cap-val { color: var(--accent-light); }

        /* World breakdown */
        .world-breakdown { margin-top: 12px; }
        .world-row {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 4px 0;
            font-size: 0.8rem;
        }
        .world-name { width: 100px; color: var(--text-secondary); }
        .world-bar-track {
            flex: 1;
            height: 14px;
            background: rgba(255,255,255,0.05);
            border-radius: 3px;
            overflow: hidden;
            display: flex;
        }
        .world-bar-fc {
            height: 100%;
            background: var(--success);
            transition: width 0.3s;
        }
        .world-bar-fc-nosubs {
            height: 100%;
            background: #e67e22;
            transition: width 0.3s;
        }
        .world-bar-nofc {
            height: 100%;
            background: var(--warning);
            transition: width 0.3s;
        }
        .world-bar-excluded {
            height: 100%;
            background: rgba(255,255,255,0.15);
            transition: width 0.3s;
        }
        .world-count { width: 40px; text-align: right; font-size: 0.75rem; color: var(--text-secondary); }
        .world-row { cursor: pointer; border-radius: 4px; padding: 4px 6px !important; }
        .world-row:hover { background: rgba(255,255,255,0.05); }
        .world-chars {
            display: none;
            padding: 6px 8px 8px 108px;
            font-size: 0.75rem;
            line-height: 1.6;
        }
        .world-chars.open { display: block; }
        .world-chars .ch-name { margin-right: 6px; }
        .world-chars .ch-name.st-in_fc { color: var(--success); }
        .world-chars .ch-name.st-fc_managed { color: #e67e22; }
        .world-chars .ch-name.st-can_join { color: var(--warning); }
        .world-chars .ch-name.st-excluded { color: rgba(255,255,255,0.4); }
        .world-chars .ch-fc { font-size: 0.65rem; color: var(--text-secondary); }

        /* Sub Planner */
        .sub-planner-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 6px;
        }
        .sp-account {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 6px;
            overflow: hidden;
        }
        .sp-acc-header {
            background: rgba(255,255,255,0.04);
            padding: 4px 6px;
            font-size: 0.65rem;
            font-weight: 700;
            color: var(--accent-light);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .sp-acc-header .sp-count {
            font-weight: 400;
            color: var(--text-secondary);
            font-size: 0.55rem;
        }
        .sp-char {
            padding: 2px 5px;
            border-bottom: 1px solid rgba(255,255,255,0.04);
        }
        .sp-char:last-child { border-bottom: none; }
        .sp-char-name {
            font-size: 0.6rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .sp-char-name .sp-world {
            font-weight: 400;
            color: var(--text-secondary);
            font-size: 0.55rem;
        }
        .sp-sub-row {
            display: flex;
            align-items: center;
            gap: 3px;
            font-size: 0.58rem;
            line-height: 1.35;
            padding-left: 4px;
        }
        .sp-sub-lvl {
            min-width: 22px;
            font-weight: 600;
        }
        .sp-sub-lvl.farming { color: var(--success); }
        .sp-sub-lvl.leveling { color: var(--warning); }
        .sp-sub-build {
            color: var(--text-secondary);
            min-width: 34px;
            font-family: monospace;
            font-size: 0.55rem;
        }
        .sp-sub-eta {
            min-width: 22px;
            font-size: 0.55rem;
            color: var(--text-secondary);
            font-weight: 600;
            text-align: center;
        }
        .sp-sub-eta.ready { color: var(--success); }
        .sp-sub-plan {
            color: var(--text-secondary);
            font-size: 0.55rem;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            flex: 1;
        }
        .sp-inv-row {
            display: flex;
            gap: 4px;
            padding: 1px 4px 2px;
            font-size: 0.5rem;
            color: var(--text-secondary);
            border-top: 1px solid rgba(255,255,255,0.04);
            flex-wrap: wrap;
        }
        .sp-inv-row span { cursor: default; white-space: nowrap; }
        .sp-sort-bar {
            display: flex;
            align-items: center;
            gap: 4px;
            margin-bottom: 6px;
            flex-wrap: wrap;
        }
        .sp-sort-btn {
            background: rgba(255,255,255,0.06);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            font-size: 0.65rem;
            padding: 2px 7px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.15s;
        }
        .sp-sort-btn:hover { background: rgba(255,255,255,0.1); color: var(--text-primary); }
        .sp-sort-btn.active { background: var(--accent); color: #fff; border-color: var(--accent); }
        .sp-char.excluded { opacity: 0.35; }
        .sp-char.sleeping { opacity: 0.5; }

        /* No FC character table */
        .char-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
        }
        .char-table th {
            text-align: left;
            padding: 8px 12px;
            background: var(--bg-secondary);
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 2px solid var(--border);
        }
        .char-table td {
            padding: 6px 12px;
            border-bottom: 1px solid rgba(255,255,255,0.04);
        }
        .char-table tr:hover td { background: rgba(255,255,255,0.03); }
        .char-table .lv-high { color: var(--success); font-weight: 600; }
        .char-table .lv-mid { color: var(--warning); }
        .char-table .lv-low { color: var(--text-secondary); }
        .char-table .region-tag {
            font-size: 0.7rem;
            padding: 2px 6px;
            border-radius: 4px;
            background: rgba(255,255,255,0.08);
            font-weight: 600;
        }
        .char-table .house-icon { font-size: 0.85rem; }

        .no-data {
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
            font-size: 0.95rem;
        }

        .footer-note {
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.75rem;
            padding: 20px 0;
            border-top: 1px solid var(--border);
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <div class="top-bar">
        <h1>🗺️ Plot Map & FC Planner <span>{{ version }}</span></h1>
        <div style="display:flex;gap:8px;align-items:center;">
            <span style="font-size:0.75rem;color:var(--text-secondary);">Updated: {{ data.last_updated }}</span>
            <a href="/">📊 Dashboard</a>
            <a href="/fcdata/" class="active">🏨 FC Data</a>
            <a href="/data/">📝 Data</a>
        </div>
    </div>

    <div class="container">
        <!-- Summary cards -->
        <div class="summary-row">
            <div class="summary-card">
                <div class="value">{{ data.total_chars }}</div>
                <div class="label">👥 Total Characters</div>
                <div class="sublabel">{{ data.num_accounts }} accounts</div>
            </div>
            <div class="summary-card fc">
                <div class="value">{{ data.total_in_fc }}</div>
                <div class="label">✅ In FC</div>
                <div class="sublabel">{{ data.fc_coverage_pct }}% coverage</div>
            </div>
            <div class="summary-card warn">
                <div class="value">{{ data.total_not_in_fc }}</div>
                <div class="label">⚠️ Can Join FC</div>
                <div class="sublabel">of {{ data.max_capacity }} max capacity</div>
            </div>
            <div class="summary-card fc">
                <div class="value">{{ data.total_fc }}</div>
                <div class="label">🏨 FC Plots</div>
                <div class="sublabel">{{ data.total_plots }} total plots</div>
            </div>
            <div class="summary-card personal">
                <div class="value">{{ data.total_personal }}</div>
                <div class="label">🏡 Personal Plots</div>
                <div class="sublabel">{{ data.district_summary|length }} districts</div>
            </div>
        </div>

        <!-- Plot Visualization -->
        <div class="section-header">
            <span>🏘️ Housing Plot Overview</span>
            <div style="margin-left:auto;">
                <div class="view-toggle">
                    <button class="active" onclick="setView('dots', this)">Grid</button>
                    <button onclick="setView('bars', this)">Bars</button>
                </div>
            </div>
        </div>

        {% if data.district_summary %}
        <div class="plot-filters" style="display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-bottom:12px;font-size:0.8rem;">
            <span style="color:var(--text-secondary);font-weight:600;">Region:</span>
            <div class="view-toggle" id="region-plot-toggle">
                <button class="active" onclick="setPlotRegion('all', this)">All</button>
                {% for reg in data.plot_regions %}
                <button onclick="setPlotRegion('{{ reg }}', this)">{{ reg }}</button>
                {% endfor %}
            </div>
            <span style="color:var(--text-secondary);font-weight:600;margin-left:8px;">Accounts:</span>
            {% for acc_name in data.plot_account_names %}
            <label style="display:inline-flex;align-items:center;gap:4px;cursor:pointer;color:var(--text-secondary);">
                <input type="checkbox" checked onchange="filterPlots()" class="plot-acc-cb" value="{{ acc_name }}" style="cursor:pointer;"> {{ acc_name }}
            </label>
            {% endfor %}
        </div>
        <div class="district-grid">
            {% for dist_name, dist_data in data.district_summary.items() %}
            <div class="district-card">
                <div class="district-card-header">
                    <span class="district-name">
                        {% if dist_name == "Mist" %}🌊{% elif dist_name == "Goblet" %}🏜️{% elif dist_name == "LB" %}🌿{% elif dist_name == "Empyreum" %}⛰️{% elif dist_name == "Shirogane" %}🏯{% endif %}
                        {{ dist_name }}
                    </span>
                    <span class="district-count">
                        <span class="fc-tag">🏨 {{ dist_data.total_fc }}</span>
                        <span class="personal-tag">🏡 {{ dist_data.total_personal }}</span>
                    </span>
                </div>
                <div class="district-body">
                    <!-- Dot view -->
                    <div class="view-dots">
                        {% for ward_data in dist_data.wards %}
                        <div class="ward-row">
                            <span class="ward-label">W{{ ward_data.ward }}</span>
                            <div class="ward-plots">
                                {% for plot in ward_data.plots %}
                                <div class="plot-dot {{ plot.type }}" title="P{{ plot.plot }}" data-region="{{ plot.region }}" data-account="{{ plot.account }}">
                                    {{ plot.plot }}
                                    <div class="tooltip">
                                        <b>{{ plot.character }}</b><br>
                                        {{ dist_name }} W{{ ward_data.ward }} P{{ plot.plot }}<br>
                                        {{ "FC" if plot.type == "fc" else "Personal" }}{% if plot.fc_name %} - {{ plot.fc_name }}{% endif %}<br>
                                        <span style="color:var(--text-secondary)">{{ plot.world }} ({{ plot.account }})</span>
                                    </div>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    <!-- Bar view -->
                    <div class="view-bars" style="display:none;">
                        <div class="ward-bar-container">
                            {% for ward_data in dist_data.wards %}
                            <div class="ward-bar-row">
                                <span class="ward-bar-label">W{{ ward_data.ward }}</span>
                                <div class="ward-bar-track">
                                    <div class="ward-bar-fc" style="width:{{ (ward_data.fc_count / data.max_ward_total * 100)|round(1) if ward_data.fc_count > 0 else 0 }}%;{% if ward_data.fc_count == 0 %}display:none{% endif %}"></div>
                                    <div class="ward-bar-personal" style="width:{{ (ward_data.personal_count / data.max_ward_total * 100)|round(1) if ward_data.personal_count > 0 else 0 }}%;{% if ward_data.personal_count == 0 %}display:none{% endif %}"></div>
                                </div>
                                <span class="ward-bar-value">{{ ward_data.total }}</span>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        <div style="display:flex;gap:16px;justify-content:center;margin-bottom:24px;font-size:0.8rem;">
            <span style="display:flex;align-items:center;gap:5px;"><span class="legend-dot fc-dot"></span> FC Plot</span>
            <span style="display:flex;align-items:center;gap:5px;"><span class="legend-dot nofc-dot" style="background:var(--gold)"></span> Personal Plot</span>
        </div>
        {% else %}
        <div class="no-data">No housing plot data found. Ensure Lifestream DefaultConfig.json is configured.</div>
        {% endif %}

        <!-- FC Capacity Planner -->
        <div class="section-header">
            <span>📊 FC Capacity Planner</span>
        </div>

        <div class="info-disclaimer">
            <strong>ℹ️ How "In FC" is determined:</strong> A character counts as <span style="color:var(--success);font-weight:600;">In FC</span> (green) only if it has active submarines in a <em>unique</em> FC &mdash; multiple characters in the same FC are de-duplicated by plot location. Green characters may or may not show an FC name; what matters is they have active subs. <span style="color:#e67e22;font-weight:600;">Managed by Alt</span> (orange) means another character is already managing the subs for that FC &mdash; click on a world bar to see which character and account is handling it. <span style="color:var(--warning);font-weight:600;">Can Join FC</span> (yellow) characters are not in any FC for capacity purposes; they may still show an FC name if they're in an FC but have no plot or active subs. <span style="color:rgba(255,255,255,0.4);font-weight:600;">Excluded</span> (gray) characters have <code>ExcludeWorkshop</code> enabled in AutoRetainer.<br>
            <strong>⚠️ FC Name Data:</strong> AutoRetainer may not always have your FC name saved correctly. If a character shows an FC name but is no longer in that FC, open AutoRetainer settings in-game &rarr; Exclusions &rarr; search the character &rarr; click <em>"Remove FC Data"</em> to clear stale data. You can refresh sub data by interacting with the submersible console afterwards if needed.<br>
            <strong>📊 OCE Max Capacity:</strong> OCE shows 39 max per account by default, reserving 1 slot for DC travel from other regions. NA/EU/JP/OCE max is 40 per account, 8 max per world.
        </div>

        <div class="planner-controls">
            <label for="account-select">Account:</label>
            <select id="account-select" onchange="updatePlanner()">
                <option value="all">All Accounts</option>
                {% for acc in data.account_summaries %}
                <option value="{{ acc.nickname }}">{{ acc.nickname }} ({{ acc.total_chars }} chars)</option>
                {% endfor %}
            </select>

            <label for="region-select">Region:</label>
            <select id="region-select" onchange="updatePlanner()">
                <option value="all">All Regions</option>
                <option value="NA">NA (40 max)</option>
                <option value="EU">EU (40 max)</option>
                <option value="JP">JP (40 max)</option>
                <option value="OCE">OCE (39 max)</option>
            </select>
        </div>

        <div id="planner-content">
            <!-- Populated by JS -->
        </div>

        <!-- Sub Planners -->
        <div class="section-header">
            <span>🚢 Sub Planners</span>
            <span style="font-size:0.8rem;color:var(--text-secondary);margin-left:auto;">
                {{ data.sub_planner_accounts|sum(attribute='total_subs') }} subs across {{ data.sub_planner_accounts|sum(attribute='total_chars') }} characters
            </span>
        </div>

        {% if data.sub_planner_accounts %}
        <div class="sp-sort-bar">
            <span style="color:var(--text-secondary);font-size:0.7rem;margin-right:4px;">Sort:</span>
            <button class="sp-sort-btn active" onclick="sortSubPlanners('default',this)" title="Default order">Default</button>
            <button class="sp-sort-btn" onclick="sortSubPlanners('maxlvl',this)" data-key="maxlvl" data-dir="desc" title="Sort by sub level">🔱 Level ▼</button>
            <button class="sp-sort-btn" onclick="sortSubPlanners('tanks',this)" data-key="tanks" data-dir="desc" title="Sort by ceruleum tanks">⛽ Tanks ▼</button>
            <button class="sp-sort-btn" onclick="sortSubPlanners('kits',this)" data-key="kits" data-dir="desc" title="Sort by repair kits">🔧 Kits ▼</button>
            <button class="sp-sort-btn" onclick="sortSubPlanners('restock',this)" data-key="restock" data-dir="asc" title="Sort by restock days">♻️ Restock ▲</button>
            <button class="sp-sort-btn" onclick="sortSubPlanners('inv',this)" data-key="inv" data-dir="desc" title="Sort by inventory slots">🎒 Inventory ▼</button>
        </div>
        <div class="sub-planner-grid">
            {% for spa in data.sub_planner_accounts %}
            <div class="sp-account">
                <div class="sp-acc-header">
                    <span>{{ spa.nickname }}</span>
                    <span class="sp-count">{{ spa.total_subs }} subs / {{ spa.total_chars }} chars</span>
                </div>
                {% for ch in spa.characters %}
                <div class="sp-char{% if ch.excluded %} excluded{% endif %}{% if ch.sleeping %} sleeping{% endif %}" data-maxlvl="{{ ch.subs|map(attribute='level')|max }}" data-tanks="{{ ch.tanks }}" data-kits="{{ ch.kits }}" data-restock="{{ ch.restock_days if ch.restock_days is not none else 9999 }}" data-inv="{{ ch.inventory }}">
                    <div class="sp-char-name" title="{{ ch.name }}@{{ ch.world }} ({{ ch.region }}){% if ch.fc_name %} — {{ ch.fc_name }}{% endif %}{% if ch.excluded %} [EXCLUDED]{% endif %}{% if ch.sleeping %} [SLEEPING]{% endif %}">
                        {{ ch.name }}<span class="sp-world">@{{ ch.world }}</span>
                    </div>
                    {% for sub in ch.subs %}
                    <div class="sp-sub-row">
                        <span class="sp-sub-lvl {{ 'farming' if sub.is_farming else 'leveling' }}">{{ sub.level }}</span>
                        <span class="sp-sub-build">{{ sub.build }}</span>
                        <span class="sp-sub-eta{% if sub.eta == 'R' %} ready{% endif %}">{{ sub.eta }}</span>
                        <span class="sp-sub-plan" title="{{ sub.plan_name if sub.plan_name else 'No plan' }}">{{ sub.plan_name if sub.plan_name else '—' }}</span>
                    </div>
                    {% endfor %}
                    <div class="sp-inv-row">
                        <span title="Ceruleum Tanks: {{ '{:,}'.format(ch.tanks) }}">⛽{{ ch.tanks|sp_compact }}</span>
                        <span title="Repair Kits: {{ '{:,}'.format(ch.kits) }}">🔧{{ ch.kits|sp_compact }}</span>
                        <span title="Days until restock">♻️{{ ch.restock_days if ch.restock_days is not none else '?' }}</span>
                        <span title="Inventory slots remaining">🎒{{ ch.inventory }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endfor %}
        </div>

        <div style="display:flex;gap:16px;justify-content:center;margin:10px 0 20px;font-size:0.75rem;color:var(--text-secondary);">
            <span style="display:flex;align-items:center;gap:4px;"><span style="color:var(--success);font-weight:700;">Lv</span> Farming</span>
            <span style="display:flex;align-items:center;gap:4px;"><span style="color:var(--warning);font-weight:700;">Lv</span> Leveling</span>
        </div>
        {% else %}
        <div class="no-data">No submarine data found.</div>
        {% endif %}

        <!-- Characters Not in FC -->
        <div class="section-header">
            <span>👤 Characters Not in FC</span>
            <span style="font-size:0.8rem;color:var(--text-secondary);margin-left:auto;">{{ data.no_fc_chars|length }} characters</span>
        </div>

        {% if data.no_fc_chars %}
        <div style="margin-bottom:8px;">
            <label style="font-size:0.8rem;color:var(--text-secondary);cursor:pointer;display:inline-flex;align-items:center;gap:6px;">
                <input type="checkbox" id="hide-excluded" onchange="toggleExcluded()" style="cursor:pointer;" checked> Hide excluded toons
            </label>
        </div>
        <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;overflow:hidden;">
            <table class="char-table">
                <thead>
                    <tr>
                        <th>Character</th>
                        <th>World</th>
                        <th>Region</th>
                        <th>Level</th>
                        <th>Account</th>
                        <th>Housing</th>
                    </tr>
                </thead>
                <tbody>
                    {% for ch in data.no_fc_chars|sort(attribute='highest_level', reverse=true) %}
                    <tr{% if ch.get('is_excluded') %} data-excluded="1" style="opacity:0.4"{% endif %}>
                        <td style="color:{{ 'rgba(255,255,255,0.4)' if ch.get('is_excluded') else 'var(--warning)' }}">{{ ch.name }}{% if ch.get('is_excluded') %} 🚫{% endif %}</td>
                        <td>{{ ch.world }}</td>
                        <td><span class="region-tag">{{ ch.region }}</span></td>
                        <td class="{{ 'lv-high' if ch.highest_level >= 25 else ('lv-mid' if ch.highest_level >= 10 else 'lv-low') }}">
                            Lv {{ ch.highest_level }}
                        </td>
                        <td style="color:var(--text-secondary)">{{ ch.account }}</td>
                        <td>
                            {% if ch.has_private_house %}<span class="house-icon" title="{{ ch.get('private_house', '') }}">🏡</span>{% endif %}
                            {% if ch.has_fc_house %}<span class="house-icon">🏨 <span style="font-size:0.7rem;color:var(--text-secondary)">(no subs)</span></span>{% endif %}
                            {% if not ch.has_private_house and not ch.has_fc_house %}<span style="color:var(--text-secondary)">-</span>{% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <div class="no-data">All characters are in a Free Company!</div>
        {% endif %}

        <div class="footer-note">
            AutoRetainer Dashboard {{ version }} &bull; <a href="/" style="color:var(--accent-light);text-decoration:none;">Back to Dashboard</a>
        </div>
    </div>

    <script>
        function toggleExcluded() {
            const hide = document.getElementById('hide-excluded').checked;
            document.querySelectorAll('tr[data-excluded]').forEach(r => r.style.display = hide ? 'none' : '');
        }
        // Apply default hide on page load
        toggleExcluded();
        // Raw data from backend
        const accountData = {{ data.account_summaries | tojson }};
        const REGION_LIMITS = {"NA": 40, "EU": 40, "JP": 40, "OCE": 39};
        const MAX_PER_WORLD = 8;

        let currentPlotRegion = 'all';

        function setView(view, btn) {
            btn.parentElement.querySelectorAll('button').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.querySelectorAll('.view-dots').forEach(el => el.style.display = view === 'dots' ? '' : 'none');
            document.querySelectorAll('.view-bars').forEach(el => el.style.display = view === 'bars' ? '' : 'none');
        }

        function setPlotRegion(region, btn) {
            currentPlotRegion = region;
            const toggle = document.getElementById('region-plot-toggle');
            if (toggle) toggle.querySelectorAll('button').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            filterPlots();
        }

        function filterPlots() {
            const selRegion = currentPlotRegion;
            const checkedAccs = new Set();
            document.querySelectorAll('.plot-acc-cb:checked').forEach(cb => checkedAccs.add(cb.value));

            // Filter dots
            document.querySelectorAll('.plot-dot').forEach(dot => {
                const r = dot.getAttribute('data-region');
                const a = dot.getAttribute('data-account');
                const show = (selRegion === 'all' || r === selRegion) && checkedAccs.has(a);
                dot.style.display = show ? '' : 'none';
            });

            // Update district counts
            document.querySelectorAll('.district-card').forEach(card => {
                const dots = card.querySelectorAll('.plot-dot');
                let fcCount = 0, personalCount = 0;
                dots.forEach(d => {
                    if (d.style.display !== 'none') {
                        if (d.classList.contains('fc')) fcCount++;
                        else personalCount++;
                    }
                });
                const fcTag = card.querySelector('.fc-tag');
                const pTag = card.querySelector('.personal-tag');
                if (fcTag) fcTag.textContent = '🏨 ' + fcCount;
                if (pTag) pTag.textContent = '🏡 ' + personalCount;
            });

            // Update bar view: recalculate per-ward bars
            document.querySelectorAll('.district-card').forEach(card => {
                const wardRows = card.querySelectorAll('.view-dots .ward-row');
                const barRows = card.querySelectorAll('.ward-bar-row');
                let maxTotal = 0;
                const wardTotals = [];
                wardRows.forEach((wr, i) => {
                    const dots = wr.querySelectorAll('.plot-dot');
                    let fc = 0, personal = 0;
                    dots.forEach(d => {
                        if (d.style.display !== 'none') {
                            if (d.classList.contains('fc')) fc++;
                            else personal++;
                        }
                    });
                    const total = fc + personal;
                    if (total > maxTotal) maxTotal = total;
                    wardTotals.push({fc, personal, total});
                });
                barRows.forEach((br, i) => {
                    if (i >= wardTotals.length) return;
                    const wt = wardTotals[i];
                    const scale = maxTotal > 0 ? maxTotal : 1;
                    const fcBar = br.querySelector('.ward-bar-fc');
                    const pBar = br.querySelector('.ward-bar-personal');
                    const valSpan = br.querySelector('.ward-bar-value');
                    if (fcBar) {
                        fcBar.style.width = (wt.fc / scale * 100) + '%';
                        fcBar.style.display = wt.fc > 0 ? '' : 'none';
                    }
                    if (pBar) {
                        pBar.style.width = (wt.personal / scale * 100) + '%';
                        pBar.style.display = wt.personal > 0 ? '' : 'none';
                    }
                    if (valSpan) valSpan.textContent = wt.total;
                });
            });
        }

        // Sub Planner sorting — store original DOM order on first load
        (function() {
            document.querySelectorAll('.sp-account').forEach(acc => {
                const chars = Array.from(acc.querySelectorAll('.sp-char'));
                chars.forEach((ch, i) => ch.setAttribute('data-orig', i));
            });
        })();

        function sortSubPlanners(key, btn) {
            if (key === 'default') {
                document.querySelectorAll('.sp-sort-btn').forEach(b => b.classList.remove('active'));
                if (btn) btn.classList.add('active');
            } else {
                // If clicking the already-active button, flip direction
                const wasActive = btn && btn.classList.contains('active');
                if (wasActive) {
                    const cur = btn.dataset.dir;
                    btn.dataset.dir = cur === 'desc' ? 'asc' : 'desc';
                    const label = btn.textContent.replace(/[▲▼]/, btn.dataset.dir === 'desc' ? '▼' : '▲');
                    btn.textContent = label;
                } else {
                    document.querySelectorAll('.sp-sort-btn').forEach(b => b.classList.remove('active'));
                    if (btn) btn.classList.add('active');
                }
            }

            const dir = (btn && btn.dataset.dir === 'asc') ? 1 : -1;

            document.querySelectorAll('.sp-account').forEach(acc => {
                const chars = Array.from(acc.querySelectorAll('.sp-char'));
                chars.sort((a, b) => {
                    if (key === 'default') {
                        return parseInt(a.dataset.orig) - parseInt(b.dataset.orig);
                    }
                    const av = parseFloat(a.dataset[key]) || 0;
                    const bv = parseFloat(b.dataset[key]) || 0;
                    return (av - bv) * dir;
                });
                chars.forEach(ch => acc.appendChild(ch));
            });
        }

        function updatePlanner() {
            const accSel = document.getElementById('account-select').value;
            const regSel = document.getElementById('region-select').value;
            const container = document.getElementById('planner-content');

            // Filter accounts
            let accounts = accountData;
            if (accSel !== 'all') {
                accounts = accounts.filter(a => a.nickname === accSel);
            }

            let html = '';

            for (const acc of accounts) {
                const fcNS = acc.in_fc_no_subs || 0;
                html += `<h3 style="color:var(--accent-light);margin:16px 0 10px;font-size:1rem;display:flex;align-items:center;flex-wrap:wrap;gap:6px;">
                    <span>${acc.nickname}</span>
                    <span style="color:var(--text-secondary);font-weight:400;font-size:0.8rem;">${acc.total_chars} chars</span>
                    <span style="font-size:0.75rem;display:inline-flex;gap:4px;margin-left:4px;">
                        <span title="${acc.in_fc} character${acc.in_fc !== 1 ? 's' : ''} in FCs with active subs" style="background:var(--success);color:#000;padding:1px 6px;border-radius:4px;font-weight:600;cursor:default;">${acc.in_fc} 🟢</span>
                        ${fcNS > 0 ? `<span title="${fcNS} character${fcNS !== 1 ? 's' : ''} managed by another alt in the same FC" style="background:#e67e22;color:#000;padding:1px 6px;border-radius:4px;font-weight:600;cursor:default;">${fcNS} 🟠</span>` : ''}
                        <span title="${acc.not_in_fc} character${acc.not_in_fc !== 1 ? 's' : ''} not in any FC — available to join one" style="background:var(--warning);color:#000;padding:1px 6px;border-radius:4px;font-weight:600;cursor:default;">${acc.not_in_fc} 🟡</span>
                        ${acc.excluded > 0 ? `<span title="${acc.excluded} character${acc.excluded !== 1 ? 's' : ''} excluded via ExcludeWorkshop" style="background:rgba(255,255,255,0.2);color:#fff;padding:1px 6px;border-radius:4px;font-weight:600;cursor:default;">${acc.excluded} ⬜</span>` : ''}
                    </span>
                </h3>`;

                let regions = acc.region_capacity;
                if (regSel !== 'all') {
                    regions = regions.filter(r => r.region === regSel);
                }

                html += '<div class="region-grid">';
                for (const reg of regions) {
                    if (reg.current === 0 && regSel === 'all') continue; // skip empty regions in "all" view

                    const pctFc = reg.limit > 0 ? (reg.in_fc / reg.limit * 100) : 0;
                    const fcNoSubs = reg.in_fc_no_subs || 0;
                    const pctFcNoSubs = reg.limit > 0 ? (fcNoSubs / reg.limit * 100) : 0;
                    const pctNoFc = reg.limit > 0 ? (reg.not_in_fc / reg.limit * 100) : 0;
                    const pctExcl = reg.limit > 0 ? ((reg.excluded || 0) / reg.limit * 100) : 0;
                    const isFull = reg.remaining <= 0;
                    const hasExcluded = (reg.excluded || 0) > 0;
                    const hasFcNoSubs = fcNoSubs > 0;
                    const maxFcPotential = reg.in_fc + fcNoSubs + reg.not_in_fc; // only non-excluded chars
                    // Dynamic grid columns: base 3 + 1 for each optional category
                    const statCols = 3 + (hasFcNoSubs ? 1 : 0) + (hasExcluded ? 1 : 0);

                    html += `
                    <div class="region-card">
                        <div class="region-card-header">
                            <h3>${reg.region} Region</h3>
                            <span class="region-badge ${isFull ? 'full' : 'available'}">
                                ${isFull ? 'FULL' : reg.remaining + ' slots open'}
                            </span>
                        </div>

                        <div class="capacity-bar">
                            ${reg.in_fc > 0 ? `<div class="in-fc" style="width:${pctFc}%">${reg.in_fc}</div>` : ''}
                            ${hasFcNoSubs ? `<div class="in-fc-no-subs" style="width:${pctFcNoSubs}%">${fcNoSubs}</div>` : ''}
                            ${reg.not_in_fc > 0 ? `<div class="not-in-fc" style="width:${pctNoFc}%">${reg.not_in_fc}</div>` : ''}
                            ${hasExcluded ? `<div class="excluded" style="width:${pctExcl}%">${reg.excluded}</div>` : ''}
                            <div class="remaining-space"></div>
                        </div>

                        <div class="capacity-legend">
                            <span title="${reg.in_fc} character${reg.in_fc !== 1 ? 's' : ''} in FCs with active subs"><span class="legend-dot fc-dot"></span> ${reg.in_fc}</span>
                            ${hasFcNoSubs ? `<span title="${fcNoSubs} character${fcNoSubs !== 1 ? 's' : ''} managed by another alt in the same FC"><span class="legend-dot fc-nosubs-dot"></span> ${fcNoSubs}</span>` : ''}
                            <span title="${reg.not_in_fc} character${reg.not_in_fc !== 1 ? 's' : ''} not in any FC — available to join one"><span class="legend-dot nofc-dot"></span> ${reg.not_in_fc}</span>
                            ${hasExcluded ? `<span title="${reg.excluded} character${reg.excluded !== 1 ? 's' : ''} excluded via ExcludeWorkshop"><span class="legend-dot excluded-dot"></span> ${reg.excluded}</span>` : ''}
                            <span title="${reg.remaining > 0 ? reg.remaining : 0} open slot${reg.remaining !== 1 ? 's' : ''} remaining"><span class="legend-dot empty-dot"></span> ${reg.remaining > 0 ? reg.remaining : 0}</span>
                        </div>

                        ${reg.worlds.length > 0 ? `
                        <div class="world-breakdown">
                            <div style="font-size:0.75rem;color:var(--text-secondary);margin-top:12px;margin-bottom:6px;font-weight:600;">
                                Per-World (${MAX_PER_WORLD} max each)
                            </div>
                            ${reg.worlds.map((w, idx) => {
                                const wFcNoSubs = w.in_fc_no_subs || 0;
                                const wId = `wc_${acc.nickname}_${reg.region}_${idx}`;
                                const chars = w.chars || [];
                                const charHtml = chars.map(c => {
                                    const fcTag = c.fc_name ? `<span class="ch-fc">[${c.fc_name}]</span>` : '';
                                    const mgrTag = (c.status === 'fc_managed' && c.managed_by) ? `<span class="ch-fc"> &mdash; subs managed by ${c.managed_by} (${c.managed_by_account})</span>` : '';
                                    return `<span class="ch-name st-${c.status}">${c.name}</span>${fcTag}${mgrTag}`;
                                }).join('<br>');
                                return `
                            <div class="world-row" onclick="document.getElementById('${wId}').classList.toggle('open')">
                                <span class="world-name">${w.world}</span>
                                <div class="world-bar-track">
                                    ${w.in_fc > 0 ? `<div class="world-bar-fc" style="width:${w.in_fc / MAX_PER_WORLD * 100}%"></div>` : ''}
                                    ${wFcNoSubs > 0 ? `<div class="world-bar-fc-nosubs" style="width:${wFcNoSubs / MAX_PER_WORLD * 100}%"></div>` : ''}
                                    ${w.not_in_fc > 0 ? `<div class="world-bar-nofc" style="width:${w.not_in_fc / MAX_PER_WORLD * 100}%"></div>` : ''}
                                    ${(w.excluded || 0) > 0 ? `<div class="world-bar-excluded" style="width:${w.excluded / MAX_PER_WORLD * 100}%"></div>` : ''}
                                </div>
                                <span class="world-count">${w.count}/${MAX_PER_WORLD}</span>
                            </div>
                            <div class="world-chars" id="${wId}">${charHtml}</div>`;
                            }).join('')}
                        </div>
                        ` : ''}

                        <div style="margin-top:14px;padding-top:10px;border-top:1px solid var(--border);font-size:0.8rem;color:var(--text-secondary);">
                            Max FC earning potential: <b style="color:var(--accent-light)">${maxFcPotential}</b> characters
                            ${reg.not_in_fc > 0 ? ` (+${reg.not_in_fc} if all join FC)` : ''}
                            ${hasExcluded ? `<br><span style="color:rgba(255,255,255,0.4);font-size:0.75rem;">* ${reg.excluded} excluded character${reg.excluded !== 1 ? 's' : ''} not counted in above results</span>` : ''}
                        </div>
                    </div>`;
                }
                html += '</div>';
            }

            if (html === '') {
                html = '<div class="no-data">No character data found for the selected filters.</div>';
            }

            container.innerHTML = html;
        }

        // Initialize on load
        document.addEventListener('DOMContentLoaded', updatePlanner);
    </script>
</body>
</html>
'''


# ===============================================
# Submarine Master List Data
# ===============================================
def get_subs_data():
    """
    Collect all character data across all accounts for the /subs/ master list page.
    Returns one row per character with up to 4 submarine slots,
    plus character-level context like gil, ceruleum, kits, inventory, treasure.
    Characters with no FC, no subs, no tanks, no kits are flagged as 'unused'.
    """
    rows = []
    seen_fcs = {}  # Track unique FCs by (account, fc_name) to avoid double-counting points
    unique_fc_names = set()  # Track globally unique FC names
    
    totals = {
        "total_chars": 0,
        "total_subs": 0,
        "total_chars_with_subs": 0,
        "total_unused": 0,
        "total_farming": 0,
        "total_leveling": 0,
        "total_idle": 0,
        "total_ready": 0,
        "total_daily_income": 0,
        "total_daily_cost": 0,
        "total_ceruleum": 0,
        "total_kits": 0,
        "total_fc_points": 0,
    }
    
    for account in account_locations:
        auto_path = account["auto_path"]
        if not os.path.isfile(auto_path):
            continue
        
        try:
            with open(auto_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
        except Exception:
            continue
        
        build_plan_name_lookup(data)
        fc_data = extract_fc_data(data)
        characters = collect_characters(data, account["nickname"])
        
        # Scan Altoholic for treasure values
        alto_map = {}
        alto_path = account.get("alto_path", "")
        if alto_path:
            alto_map = scan_altoholic_db(alto_path)
        
        for char in characters:
            cid = char.get("CID", 0)
            submarines = parse_submarine_data(char)
            
            totals["total_chars"] += 1
            
            # Character-level data
            char_name = char.get("Name", "Unknown")
            world = char.get("World", "Unknown")
            region = region_from_world(world)
            char_gil = char.get("Gil", 0)
            ceruleum = char.get("Ceruleum", 0)
            repair_kits = char.get("RepairKits", 0)
            inventory_space = char.get("InventorySpace", 0)
            ventures = char.get("Ventures", 0)
            
            # Altoholic data
            treasure_value = 0
            highest_level = 0
            highest_job = ""
            if cid in alto_map:
                treasure_value = alto_map[cid].get("treasure_value", 0)
                highest_level = alto_map[cid].get("highest_level", 0)
                highest_job = alto_map[cid].get("highest_job", "")
            
            # FC info
            fc_name = ""
            fc_points = 0
            if cid in fc_data:
                fc_name = fc_data[cid].get("Name", "")
                fc_points = fc_data[cid].get("FCPoints", 0)
                # Only count FC points once per unique FC per account
                fc_key = (account["nickname"], fc_name)
                if fc_key not in seen_fcs and fc_name:
                    seen_fcs[fc_key] = fc_points
                if fc_name:
                    unique_fc_names.add(fc_name)
            
            # Exclusion / sleeping flags
            exclude_workshop = char.get("ExcludeWorkshop", False) if HONOR_AR_EXCLUSIONS else False
            subs_sleeping = not char.get("WorkshopEnabled", True)
            
            # Calculate days until restock
            total_tanks_per_day = sum(s.get("tanks_per_day", 0) for s in submarines)
            total_kits_per_day = sum(s.get("kits_per_day", 0) for s in submarines)
            days_until_restock = None
            if total_tanks_per_day > 0 and total_kits_per_day > 0:
                days_from_tanks = ceruleum / total_tanks_per_day if ceruleum > 0 else 0
                days_from_kits = repair_kits / total_kits_per_day if repair_kits > 0 else 0
                days_until_restock = int(min(days_from_tanks, days_from_kits))
            
            # Daily totals for this character
            daily_income = sum(s["daily_gil"] for s in submarines) if submarines else 0
            daily_cost = sum(s["daily_cost"] for s in submarines) if submarines else 0
            
            # Pad submarines to 4 slots
            sub_slots = []
            for i in range(4):
                if i < len(submarines):
                    s = submarines[i]
                    sub_slots.append({
                        "name": s["name"],
                        "level": s["level"],
                        "build": s["build"],
                        "plan_name": s["plan_name"] if s["plan_name"] else ("Farming" if s["is_farming"] else ("Leveling" if s["is_leveling"] else "None")),
                        "return_formatted": s["return_formatted"],
                        "return_time": s["return_time"] if s["return_time"] else 0,
                        "is_ready": s["is_ready"],
                        "is_farming": s["is_farming"],
                        "is_leveling": s["is_leveling"],
                        "daily_gil": s["daily_gil"],
                    })
                else:
                    sub_slots.append(None)
            
            # Determine if character is "unused" (no FC, no subs, no tanks, no kits)
            has_fc = bool(fc_name)
            has_subs = len(submarines) > 0
            has_tanks = ceruleum > 0
            has_kits = repair_kits > 0
            is_unused = not has_fc and not has_subs and not has_tanks and not has_kits
            
            # Accumulate totals
            if has_subs:
                totals["total_chars_with_subs"] += 1
                totals["total_subs"] += len(submarines)
                totals["total_farming"] += sum(1 for s in submarines if s["is_farming"])
                totals["total_leveling"] += sum(1 for s in submarines if s["is_leveling"])
                totals["total_idle"] += sum(1 for s in submarines if not s["plan_name"] and not s["is_farming"] and not s["is_leveling"])
                totals["total_ready"] += sum(1 for s in submarines if s["is_ready"])
                totals["total_daily_income"] += daily_income
                totals["total_daily_cost"] += daily_cost
            totals["total_ceruleum"] += ceruleum
            totals["total_kits"] += repair_kits
            if is_unused:
                totals["total_unused"] += 1
            
            rows.append({
                "account": account["nickname"],
                "char_name": char_name,
                "world": world,
                "region": region,
                "fc_name": fc_name,
                "char_level": highest_level,
                "char_job": highest_job,
                "gil": char_gil,
                "ceruleum": ceruleum,
                "repair_kits": repair_kits,
                "inventory_space": inventory_space,
                "ventures": ventures,
                "treasure_value": treasure_value,
                "days_until_restock": days_until_restock,
                "daily_income": daily_income,
                "daily_cost": daily_cost,
                "num_subs": len(submarines),
                "subs": sub_slots,
                "exclude_workshop": exclude_workshop,
                "subs_sleeping": subs_sleeping,
                "is_unused": is_unused,
            })
    
    totals["total_monthly_income"] = totals["total_daily_income"] * 30
    totals["total_monthly_cost"] = totals["total_daily_cost"] * 30
    totals["total_net_daily"] = totals["total_daily_income"] - totals["total_daily_cost"]
    totals["total_net_monthly"] = totals["total_net_daily"] * 30
    
    # FC points totals (deduplicated per unique FC)
    totals["total_fc_points"] = sum(seen_fcs.values())
    totals["total_fc_tanks"] = totals["total_fc_points"] // 100
    totals["total_fc_stacks"] = round(totals["total_fc_tanks"] / 999, 1)
    totals["total_fc_tank_value"] = totals["total_fc_tanks"] * CERULEUM_TANK_COST
    totals["unique_fc_count"] = len(unique_fc_names)
    
    return {
        "rows": rows,
        "totals": totals,
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# ===============================================
# Submarine Master List HTML Template
# ===============================================
SUBS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Master List - AutoRetainer Dashboard</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚓</text></svg>">
    <script src="https://cdn.sheetjs.com/xlsx-0.20.1/package/dist/xlsx.full.min.js"></script>
    <style>
        :root {
            --bg-primary: #0a0e17;
            --bg-card: #131a2b;
            --bg-header: #0d1320;
            --border: #1e2d44;
            --text-primary: #e0e6ed;
            --text-secondary: #7a8ba3;
            --accent: #3a7aaa;
            --accent-light: #5ba0d0;
            --accent-highlight: #7ec8e3;
            --success: #4caf50;
            --warning: #ff9800;
            --danger: #f44336;
            --gold: #ffd700;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { height: 100%; overflow: hidden; }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
        }

        /* Dark scrollbars */
        ::-webkit-scrollbar { width: 10px; height: 10px; }
        ::-webkit-scrollbar-track { background: var(--bg-primary); }
        ::-webkit-scrollbar-thumb { background: #2a3a52; border-radius: 5px; }
        ::-webkit-scrollbar-thumb:hover { background: #3a5070; }
        ::-webkit-scrollbar-corner { background: var(--bg-primary); }
        * { scrollbar-color: #2a3a52 var(--bg-primary); scrollbar-width: thin; }

        .container {
            display: flex;
            flex-direction: column;
            height: 100vh;
            max-width: 100%;
            padding: 12px 24px 0;
        }

        /* Navigation */
        .nav-bar {
            flex-shrink: 0;
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 10px;
            padding: 10px 16px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
        }
        .nav-bar a {
            color: var(--accent-light);
            text-decoration: none;
            font-size: 0.85rem;
            padding: 6px 12px;
            border-radius: 6px;
            transition: background 0.2s;
        }
        .nav-bar a:hover { background: rgba(58, 122, 170, 0.2); }
        .nav-bar a.active { background: var(--accent); color: #fff; }
        .nav-bar .title {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-right: auto;
        }

        /* Summary cards */
        .summary-row {
            flex-shrink: 0;
            display: flex;
            gap: 12px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }
        .summary-card {
            flex: 1;
            min-width: 100px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 8px 10px;
            text-align: center;
        }
        .summary-card .value { font-size: 1.1rem; font-weight: 700; color: var(--accent-highlight); }
        .summary-card .label { font-size: 0.68rem; color: var(--text-secondary); margin-top: 2px; }
        .summary-card .sublabel { font-size: 0.6rem; color: var(--text-secondary); margin-top: 2px; }
        .summary-card.fc .value { color: var(--success); }
        .summary-card.warn .value { color: var(--warning); }
        .summary-card.danger .value { color: var(--danger); }
        .summary-card.gold .value { color: var(--gold); }

        /* Table container */
        .table-wrapper {
            flex: 1;
            overflow: auto;
            min-height: 0;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
        }

        /* Master table */
        .sub-master-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            font-size: 0.78rem;
            white-space: nowrap;
        }
        .sub-master-table th {
            position: sticky;
            top: 0;
            z-index: 10;
            background: var(--bg-header);
            color: var(--accent-light);
            padding: 10px 8px;
            text-align: left;
            border-bottom: 2px solid var(--border);
            cursor: pointer;
            user-select: none;
            font-weight: 600;
            font-size: 0.72rem;
            transition: background 0.15s;
        }
        .sub-master-table th:hover { background: rgba(58, 122, 170, 0.2); }
        .sub-master-table th .sort-arrow { margin-left: 4px; font-size: 0.6rem; opacity: 0.5; }
        .sub-master-table th.sorted .sort-arrow { opacity: 1; color: var(--gold); }
        .sub-master-table td {
            padding: 7px 8px;
            border-bottom: 1px solid rgba(255,255,255,0.04);
            color: var(--text-primary);
        }
        .sub-master-table tbody tr:hover { background: rgba(58, 122, 170, 0.08); }

        /* Sub slot header groups */
        .sub-master-table th.sub-group-1 { border-top: 3px solid var(--success); }
        .sub-master-table th.sub-group-2 { border-top: 3px solid var(--accent); }
        .sub-master-table th.sub-group-3 { border-top: 3px solid var(--warning); }
        .sub-master-table th.sub-group-4 { border-top: 3px solid var(--danger); }

        /* Cell colors */
        .text-success { color: var(--success); }
        .text-warning { color: var(--warning); }
        .text-danger { color: var(--danger); }
        .text-gold { color: var(--gold); }
        .text-muted { color: var(--text-secondary); }
        .text-accent { color: var(--accent-light); }

        .cell-ready { color: var(--success); font-weight: 700; }
        .cell-returning { color: var(--warning); }
        .cell-empty { color: var(--text-secondary); opacity: 0.4; }
        .cell-sleeping { color: #666; font-style: italic; }

        .restock-critical { color: var(--danger); font-weight: 700; }
        .restock-warning { color: var(--warning); }
        .restock-ok { color: var(--success); }

        /* Footer */
        .footer {
            flex-shrink: 0;
            text-align: center;
            padding: 8px;
            color: var(--text-secondary);
            font-size: 0.7rem;
        }

        /* Filter bar */
        .sticky-filters {
            flex-shrink: 0;
            background: var(--bg-primary);
            padding: 6px 0 4px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 6px;
        }

        /* Search */
        .search-bar {
            margin-bottom: 8px;
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .search-bar input {
            flex: 1;
            max-width: 300px;
            padding: 8px 12px;
            background: var(--bg-header);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text-primary);
            font-size: 0.85rem;
            outline: none;
        }
        .search-bar input:focus { border-color: var(--accent); }
        .search-bar .count { font-size: 0.8rem; color: var(--text-secondary); }

        /* Filter buttons */
        .filter-row {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            margin-bottom: 12px;
        }
        .filter-btn {
            padding: 5px 10px;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: var(--bg-header);
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 0.75rem;
            transition: all 0.15s;
        }
        .filter-btn:hover { border-color: var(--accent); color: var(--text-primary); }
        .filter-btn.active { background: var(--accent); color: #fff; border-color: var(--accent); }

        /* Checkbox toggle */
        .toggle-row {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-left: 16px;
        }
        .toggle-row label {
            font-size: 0.8rem;
            color: var(--text-secondary);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .toggle-row input[type="checkbox"] {
            accent-color: var(--accent);
            cursor: pointer;
            width: 14px;
            height: 14px;
        }
        .toggle-row .unused-count {
            font-size: 0.72rem;
            color: var(--text-secondary);
            opacity: 0.7;
        }
        tr.row-unused { opacity: 0.5; }
    </style>
</head>
<body>
    <div class="container">
        <!-- Navigation -->
        <div class="nav-bar">
            <span class="title">📝 Data Master List</span>
            <a href="/">📊 Dashboard</a>
            <a href="/fcdata/">🏨 FC Data</a>
            <a href="/data/" class="active">📝 Data</a>
        </div>

        <!-- Summary cards -->
        <div class="summary-row">
            <div class="summary-card">
                <div class="value">{{ data.totals.total_subs }}</div>
                <div class="label">🚢 Total Subs</div>
                <div class="sublabel">{{ data.totals.total_chars_with_subs }} w/ subs · {{ data.totals.total_chars }} total</div>
            </div>
            <div class="summary-card fc">
                <div class="value">{{ data.totals.total_farming }}</div>
                <div class="label">🌾 Farming</div>
                <div class="sublabel">{{ data.totals.total_ready }} ready now</div>
            </div>
            <div class="summary-card warn">
                <div class="value">{{ data.totals.total_leveling }}</div>
                <div class="label">📈 Leveling</div>
                <div class="sublabel">{{ data.totals.total_idle }} idle</div>
            </div>
            <div class="summary-card gold">
                <div class="value">{{ "{:,}".format(data.totals.total_daily_income|int) }}</div>
                <div class="label">💰 Daily Income</div>
                <div class="sublabel">{{ "{:,}".format(data.totals.total_monthly_income|int) }}/mo</div>
            </div>
            <div class="summary-card danger">
                <div class="value">{{ "{:,}".format(data.totals.total_daily_cost|int) }}</div>
                <div class="label">🔧 Daily Cost</div>
                <div class="sublabel">{{ "{:,}".format(data.totals.total_monthly_cost|int) }}/mo</div>
            </div>
            <div class="summary-card fc">
                <div class="value">{{ "{:,}".format(data.totals.total_net_daily|int) }}</div>
                <div class="label">📊 Net Daily</div>
                <div class="sublabel">{{ "{:,}".format(data.totals.total_net_monthly|int) }}/mo</div>
            </div>
            <div class="summary-card">
                <div class="value">{{ "{:,}".format(data.totals.total_ceruleum) }}</div>
                <div class="label">⛽ Ceruleum</div>
                <div class="sublabel">{{ "{:,}".format(data.totals.total_kits) }} kits</div>
            </div>
            <div class="summary-card gold">
                <div class="value">{{ "{:,}".format(data.totals.total_fc_points) }}</div>
                <div class="label">🪙 FC Points</div>
                <div class="sublabel">{{ "{:,.1f}".format(data.totals.total_fc_stacks) }} stacks · {{ data.totals.total_fc_tank_value|sp_compact }} gil</div>
            </div>
            <div class="summary-card">
                <div class="value">{{ data.totals.unique_fc_count }}</div>
                <div class="label">🏠 Unique FCs</div>
                <div class="sublabel">across all accounts</div>
            </div>
        </div>

        <!-- Search and filters (sticky) -->
        <div class="sticky-filters">
            <div class="search-bar">
                <input type="text" id="searchInput" placeholder="Search characters, worlds, accounts..." oninput="filterTable()">
                <span class="count" id="rowCount">{{ data.rows|length }} characters</span>
                <div class="toggle-row">
                    <label><input type="checkbox" id="subsOnly" checked onchange="filterTable()"> Show only toons with subs</label>
                    <label><input type="checkbox" id="showUnused" onchange="filterTable()"> Show unused toons <span class="unused-count">({{ data.totals.total_unused }})</span></label>
                </div>
                <button onclick="exportToExcel()" style="margin-left:auto;padding:4px 12px;font-size:0.75rem;background:var(--accent);color:#fff;border:1px solid var(--accent);border-radius:6px;cursor:pointer;" title="Export visible rows to Excel">📥 Export Excel</button>
            </div>
            <div class="filter-row">
                <button class="filter-btn active" onclick="filterRegion(this, 'all')">All</button>
                <button class="filter-btn" onclick="filterRegion(this, 'NA')">NA</button>
                <button class="filter-btn" onclick="filterRegion(this, 'EU')">EU</button>
                <button class="filter-btn" onclick="filterRegion(this, 'JP')">JP</button>
                <button class="filter-btn" onclick="filterRegion(this, 'OCE')">OCE</button>
            </div>
        </div>

        <!-- Master table -->
        <div class="table-wrapper">
            <table class="sub-master-table" id="subsTable">
                <thead>
                    <tr>
                        <th onclick="sortTable(0, 'str')" data-col="0">Account <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(1, 'str')" data-col="1">Character <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(2, 'str')" data-col="2">World <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(3, 'str')" data-col="3">Region <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(4, 'num')" data-col="4">Lvl <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(5, 'num')" data-col="5">Gil <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(6, 'num')" data-col="6">⛽ Tanks <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(7, 'num')" data-col="7">🔧 Kits <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(8, 'num')" data-col="8">♻️ Restock <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(9, 'num')" data-col="9">📦 Inv <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(10, 'num')" data-col="10">💎 Treasure <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(11, 'num')" data-col="11" class="sub-group-1">S1 Lvl <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(12, 'str')" data-col="12" class="sub-group-1">S1 Build <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(13, 'str')" data-col="13" class="sub-group-1">S1 Plan <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(14, 'str')" data-col="14" class="sub-group-1">S1 Return <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(15, 'num')" data-col="15" class="sub-group-2">S2 Lvl <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(16, 'str')" data-col="16" class="sub-group-2">S2 Build <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(17, 'str')" data-col="17" class="sub-group-2">S2 Plan <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(18, 'str')" data-col="18" class="sub-group-2">S2 Return <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(19, 'num')" data-col="19" class="sub-group-3">S3 Lvl <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(20, 'str')" data-col="20" class="sub-group-3">S3 Build <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(21, 'str')" data-col="21" class="sub-group-3">S3 Plan <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(22, 'str')" data-col="22" class="sub-group-3">S3 Return <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(23, 'num')" data-col="23" class="sub-group-4">S4 Lvl <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(24, 'str')" data-col="24" class="sub-group-4">S4 Build <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(25, 'str')" data-col="25" class="sub-group-4">S4 Plan <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(26, 'str')" data-col="26" class="sub-group-4">S4 Return <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(27, 'num')" data-col="27">💰 Daily <span class="sort-arrow">▲▼</span></th>
                        <th onclick="sortTable(28, 'num')" data-col="28">🔧 Cost <span class="sort-arrow">▲▼</span></th>
                    </tr>
                </thead>
                <tbody>
                    {% for row in data.rows %}
                    <tr data-region="{{ row.region }}" data-unused="{{ 'true' if row.is_unused else 'false' }}" data-hassubs="{{ 'true' if row.num_subs > 0 else 'false' }}" data-search="{{ row.account|lower }} {{ row.char_name|lower }} {{ row.world|lower }} {{ row.region|lower }} {{ row.fc_name|lower }}"{% if row.num_subs == 0 %} style="display:none"{% endif %}{% if row.is_unused %} class="row-unused"{% endif %}>
                        <td>{{ row.account }}</td>
                        <td><strong>{{ row.char_name }}</strong>{% if row.subs_sleeping %} <span class="cell-sleeping">💤</span>{% endif %}{% if row.exclude_workshop %} <span class="text-muted">🚫</span>{% endif %}</td>
                        <td>{{ row.world }}</td>
                        <td>{{ row.region }}</td>
                        <td>{{ row.char_level }}</td>
                        <td class="text-gold">{{ "{:,}".format(row.gil) }}</td>
                        <td>{{ "{:,}".format(row.ceruleum) }}</td>
                        <td>{{ "{:,}".format(row.repair_kits) }}</td>
                        <td class="{% if row.days_until_restock is not none %}{% if row.days_until_restock < 7 %}restock-critical{% elif row.days_until_restock < 14 %}restock-warning{% else %}restock-ok{% endif %}{% endif %}">{% if row.days_until_restock is not none %}{{ row.days_until_restock }}d{% else %}-{% endif %}</td>
                        <td{% if row.inventory_space <= 10 %} class="text-danger"{% elif row.inventory_space <= 35 %} class="text-warning"{% endif %}>{{ row.inventory_space }}</td>
                        <td class="text-gold">{{ "{:,}".format(row.treasure_value) }}</td>
                        {% for i in range(4) %}
                        {% if row.subs[i] %}
                        <td class="{% if row.subs[i].is_ready %}cell-ready{% endif %}">{{ row.subs[i].level }}</td>
                        <td>{{ row.subs[i].build }}</td>
                        <td class="{% if row.subs[i].is_farming %}text-success{% elif row.subs[i].is_leveling %}text-warning{% else %}text-muted{% endif %}">{{ row.subs[i].plan_name }}</td>
                        <td class="{% if row.subs[i].is_ready %}cell-ready{% else %}cell-returning{% endif %}">{{ row.subs[i].return_formatted }}</td>
                        {% else %}
                        <td class="cell-empty">-</td>
                        <td class="cell-empty">-</td>
                        <td class="cell-empty">-</td>
                        <td class="cell-empty">-</td>
                        {% endif %}
                        {% endfor %}
                        <td class="text-success">{{ "{:,}".format(row.daily_income) }}</td>
                        <td class="text-warning">{{ "{:,}".format(row.daily_cost) }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <div class="footer">
            AutoRetainer Dashboard {{ version }} — Submarine Master List — Last updated: {{ data.last_updated }}
        </div>
    </div>

    <script>
        // Sort state
        let currentSortCol = -1;
        let currentSortDir = 'asc';

        function sortTable(colIdx, type) {
            const table = document.getElementById('subsTable');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const headers = table.querySelectorAll('th');

            // Toggle direction
            if (currentSortCol === colIdx) {
                currentSortDir = currentSortDir === 'asc' ? 'desc' : 'asc';
            } else {
                currentSortDir = 'asc';
                currentSortCol = colIdx;
            }

            // Clear sorted class
            headers.forEach(h => h.classList.remove('sorted'));
            headers[colIdx].classList.add('sorted');

            rows.sort((a, b) => {
                let aVal = a.cells[colIdx].textContent.trim();
                let bVal = b.cells[colIdx].textContent.trim();

                if (type === 'num') {
                    aVal = parseFloat(aVal.replace(/[^0-9.\\-]/g, '')) || 0;
                    bVal = parseFloat(bVal.replace(/[^0-9.\\-]/g, '')) || 0;
                    return currentSortDir === 'asc' ? aVal - bVal : bVal - aVal;
                } else {
                    aVal = aVal.toLowerCase();
                    bVal = bVal.toLowerCase();
                    if (aVal < bVal) return currentSortDir === 'asc' ? -1 : 1;
                    if (aVal > bVal) return currentSortDir === 'asc' ? 1 : -1;
                    return 0;
                }
            });

            rows.forEach(r => tbody.appendChild(r));
            updateArrows(colIdx);
        }

        function updateArrows(sortedCol) {
            document.querySelectorAll('.sub-master-table th').forEach((th, idx) => {
                const arrow = th.querySelector('.sort-arrow');
                if (!arrow) return;
                if (idx === sortedCol) {
                    arrow.textContent = currentSortDir === 'asc' ? '▲' : '▼';
                } else {
                    arrow.textContent = '▲▼';
                }
            });
        }

        // Search filter
        let activeRegion = 'all';

        function filterTable() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const subsOnly = document.getElementById('subsOnly').checked;
            const showUnused = document.getElementById('showUnused').checked;
            const rows = document.querySelectorAll('#subsTable tbody tr');
            let visible = 0;

            rows.forEach(row => {
                const searchData = row.getAttribute('data-search');
                const region = row.getAttribute('data-region');
                const isUnused = row.getAttribute('data-unused') === 'true';
                const hasSubs = row.getAttribute('data-hassubs') === 'true';
                const matchesSearch = !query || searchData.includes(query);
                const matchesRegion = activeRegion === 'all' || region === activeRegion;
                const matchesSubs = !subsOnly || hasSubs;
                const matchesUnused = showUnused || !isUnused;
                const show = matchesSearch && matchesRegion && matchesSubs && matchesUnused;
                row.style.display = show ? '' : 'none';
                if (show) visible++;
            });

            document.getElementById('rowCount').textContent = visible + ' characters';
        }

        function filterRegion(btn, region) {
            activeRegion = region;
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filterTable();
        }

        function exportToExcel() {
            const table = document.getElementById('subsTable');
            const headers = [];
            table.querySelectorAll('thead th').forEach(th => {
                headers.push(th.textContent.replace(/[▲▼]/g, '').trim());
            });

            const dataRows = [];
            table.querySelectorAll('tbody tr').forEach(row => {
                if (row.style.display === 'none') return;
                const cells = [];
                row.querySelectorAll('td').forEach(td => {
                    let val = td.textContent.trim();
                    // Try to parse as number (strip commas, gil suffix, etc.)
                    const num = parseFloat(val.replace(/[^0-9.\-]/g, ''));
                    cells.push(!isNaN(num) && val.match(/^[\d,.\-]+[dg]?$/) ? num : val);
                });
                dataRows.push(cells);
            });

            const wsData = [headers, ...dataRows];
            const ws = XLSX.utils.aoa_to_sheet(wsData);

            // Frozen row 1 (header)
            ws['!freeze'] = {xSplit: 0, ySplit: 1};
            // Auto-filter on all columns
            ws['!autofilter'] = {ref: XLSX.utils.encode_range({s:{r:0,c:0}, e:{r:dataRows.length, c:headers.length-1}})};
            // Column widths (auto-fit approximation)
            ws['!cols'] = headers.map((h, i) => {
                let maxLen = h.length;
                dataRows.forEach(r => {
                    const len = String(r[i] || '').length;
                    if (len > maxLen) maxLen = len;
                });
                return {wch: Math.min(maxLen + 2, 30)};
            });

            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, 'Data');

            // Set freeze pane via sheet views
            wb.Sheets['Data']['!views'] = [{state: 'frozen', ySplit: 1}];

            const now = new Date();
            const ts = now.getFullYear() + '-' + String(now.getMonth()+1).padStart(2,'0') + '-' + String(now.getDate()).padStart(2,'0');
            XLSX.writeFile(wb, 'AutoRetainer_Data_' + ts + '.xlsx');
        }

        // Update row count on page load to match default filter state
        document.addEventListener('DOMContentLoaded', filterTable);
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
    return render_template_string(HTML_TEMPLATE, data=data, auto_refresh=AUTO_REFRESH, 
                                  job_categories=JOB_CATEGORIES, job_display_names=JOB_DISPLAY_NAMES,
                                  job_base_class=JOB_BASE_CLASS, version=VERSION,
                                  show_classes=SHOW_CLASSES, show_currencies=SHOW_CURRENCIES,
                                  show_msq_progression=SHOW_MSQ_PROGRESSION, default_theme=DEFAULT_THEME,
                                  highlight_idle_retainers=HIGHLIGHT_IDLE_RETAINERS,
                                  highlight_idle_subs=HIGHLIGHT_IDLE_SUBS,
                                  highlight_ready_items=HIGHLIGHT_READY_ITEMS,
                                  highlight_max_mb=HIGHLIGHT_MAX_MB,
                                  highlight_potential_retainer=HIGHLIGHT_POTENTIAL_RETAINER,
                                  highlight_potential_subs=HIGHLIGHT_POTENTIAL_SUBS,
                                  highlight_color_idle_retainers=HIGHLIGHT_COLOR_IDLE_RETAINERS,
                                  highlight_color_idle_subs=HIGHLIGHT_COLOR_IDLE_SUBS,
                                  highlight_color_max_mb=HIGHLIGHT_COLOR_MAX_MB,
                                  highlight_color_potential_retainer=HIGHLIGHT_COLOR_POTENTIAL_RETAINER,
                                  highlight_color_potential_subs=HIGHLIGHT_COLOR_POTENTIAL_SUBS)


@app.route('/fcdata/')
@app.route('/fcdata')
def map_page():
    """Plot map and FC capacity planner page"""
    data = get_map_data()
    return render_template_string(MAP_TEMPLATE, data=data, version=VERSION)


@app.route('/data/')
@app.route('/data')
def subs_page():
    """Submarine master list page"""
    data = get_subs_data()
    return render_template_string(SUBS_TEMPLATE, data=data, version=VERSION)


@app.route('/api/subs-data')
def api_subs_data():
    """API endpoint for subs page JSON data"""
    data = get_subs_data()
    return jsonify(data)


@app.route('/api/map-data')
def api_map_data():
    """API endpoint for map page JSON data"""
    data = get_map_data()
    return jsonify(data)


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
# FC Detection Diagnostic
# ===============================================
def run_fc_diagnostic():
    """
    Compare FC detection methods across all accounts.
    Prints per-character breakdown showing which indicators triggered.
    """
    print("\n" + "=" * 100)
    print("  FC DETECTION DIAGNOSTIC — Comparing main page vs /map/ page logic")
    print("=" * 100)
    
    grand_total = {"chars": 0, "in_fc": 0, "fc_managed": 0, "excluded": 0, "not_in_fc": 0}
    
    for account in account_locations:
        auto_path = account["auto_path"]
        if not os.path.isfile(auto_path):
            continue
        try:
            with open(auto_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
        except Exception:
            continue
        
        fc_data = extract_fc_data(data)
        characters = collect_characters(data, account["nickname"])
        
        housing_map = {}
        lfstrm_path = account.get("lfstrm_path", "")
        if lfstrm_path:
            housing_map = load_lifestream_data(lfstrm_path)
        
        # Per-account counters
        acc = {"chars": 0, "in_fc": 0, "fc_managed": 0, "excluded": 0, "not_in_fc": 0}
        # Per-region counters
        region_counts = {}
        char_details = []
        seen_fc_keys = {}  # FC plot dedup
        
        for char in characters:
            cid = char.get("CID", 0)
            name = char.get("Name", "Unknown")
            world = char.get("World", "Unknown")
            region = region_from_world(world)
            
            # FC indicators
            fc_name = fc_data[cid].get("Name", "") if cid in fc_data else ""
            has_subs = bool(char.get("OfflineSubmarineData", []))
            has_fc_house = cid in housing_map and housing_map[cid].get('fc') is not None
            
            # Build FC key for dedup
            fc_key = None
            if has_fc_house:
                fcd = housing_map[cid]['fc']
                fc_key = f"{world}_{fcd['district']}_W{fcd['ward']}_P{fcd['plot']}"
            elif fc_name:
                fc_key = f"{world}_{fc_name}"
            
            # Exclusion flags (only ExcludeWorkshop affects FC capacity)
            excl_ret = char.get("ExcludeRetainer", False) if HONOR_AR_EXCLUSIONS else False
            excl_ws = char.get("ExcludeWorkshop", False) if HONOR_AR_EXCLUSIONS else False
            is_excluded = excl_ws
            
            # Classify with dedup (matches get_map_data logic)
            if is_excluded:
                status = "EXCLUDED"
            elif has_subs:
                if fc_key and fc_key in seen_fc_keys:
                    status = "FC_MANAGED"
                else:
                    status = "IN_FC"
                    if fc_key:
                        seen_fc_keys[fc_key] = name
            elif has_fc_house:
                status = "FC_MANAGED"
            else:
                status = "NOT_IN_FC"
            
            acc["chars"] += 1
            if status == "EXCLUDED":
                acc["excluded"] += 1
            elif status == "IN_FC":
                acc["in_fc"] += 1
            elif status == "FC_MANAGED":
                acc["fc_managed"] += 1
            else:
                acc["not_in_fc"] += 1
            
            # Track per region
            if region:
                if region not in region_counts:
                    region_counts[region] = {"chars": 0, "in_fc": 0, "fc_managed": 0, "excluded": 0, "not_in_fc": 0}
                rc = region_counts[region]
                rc["chars"] += 1
                if status == "EXCLUDED":
                    rc["excluded"] += 1
                elif status == "IN_FC":
                    rc["in_fc"] += 1
                elif status == "FC_MANAGED":
                    rc["fc_managed"] += 1
                else:
                    rc["not_in_fc"] += 1
            
            # Build indicators list for detail display
            indicators = []
            if has_subs: indicators.append("SUBS")
            if has_fc_house: indicators.append("FC_HOUSE")
            if fc_name: indicators.append(f"FC:{fc_name}")
            if excl_ret: indicators.append("EXCL_RET")
            if excl_ws: indicators.append("EXCL_WS")
            if fc_key and fc_key in seen_fc_keys and status == "FC_MANAGED": indicators.append("DEDUP")
            
            char_details.append({
                "name": name, "world": world, "region": region,
                "status": status, "indicators": indicators,
                "is_excluded": is_excluded
            })
        
        # Print account summary
        print(f"\n  [{account['nickname']}] {acc['chars']} chars — InFC: {acc['in_fc']}, ManagedByAlt: {acc['fc_managed']}, Excluded: {acc['excluded']}, CanJoin: {acc['not_in_fc']}")
        
        for reg in sorted(region_counts.keys()):
            rc = region_counts[reg]
            mg = rc['fc_managed']
            mg_str = f" | MgdByAlt: {mg:3d}" if mg > 0 else ""
            print(f"    {reg:4s}: {rc['chars']:3d} chars | InFC: {rc['in_fc']:3d}{mg_str} | Excluded: {rc['excluded']:3d} | CanJoin: {rc['not_in_fc']:3d}")
        
        # Show excluded characters with their indicators
        excluded_chars = [c for c in char_details if c["is_excluded"]]
        if excluded_chars:
            print(f"    --- Excluded Characters ({len(excluded_chars)}) ---")
            for c in excluded_chars:
                print(f"      {c['name']:24s} {c['world']:15s} {c['region']:4s} [{', '.join(c['indicators'])}]")
        
        # Show characters managed by alt (orange category)
        fc_managed_chars = [c for c in char_details if c["status"] == "FC_MANAGED"]
        if fc_managed_chars:
            print(f"    --- Managed by Alt ({len(fc_managed_chars)}) — shown as ORANGE ---")
            for c in fc_managed_chars:
                print(f"      {c['name']:24s} {c['world']:15s} {c['region']:4s} [{', '.join(c['indicators'])}]")
        
        grand_total["chars"] += acc["chars"]
        grand_total["in_fc"] += acc["in_fc"]
        grand_total["fc_managed"] += acc["fc_managed"]
        grand_total["excluded"] += acc["excluded"]
        grand_total["not_in_fc"] += acc["not_in_fc"]
    
    print(f"\n  GRAND TOTAL: {grand_total['chars']} chars")
    print(f"    In FC (unique):   {grand_total['in_fc']}")
    print(f"    Managed by Alt:   {grand_total['fc_managed']}")
    print(f"    Excluded:         {grand_total['excluded']}")
    print(f"    Can Join FC:      {grand_total['not_in_fc']}")
    print(f"    HONOR_AR_EXCLUSIONS: {HONOR_AR_EXCLUSIONS}")
    print(f"    FC Detection: unique subs=GREEN, dup FC or no subs=ORANGE(managed), else=CAN_JOIN")
    print(f"    Dedup: by FC plot (world+district+ward+plot) or fc_name+world")
    print("=" * 100 + "\n")


# ===============================================
# Main Entry Point
# ===============================================
def main():
    load_external_config()
    
    print("=" * 60)
    print(f"  AutoRetainer Dashboard {VERSION}")
    print("=" * 60)
    print(f"  Server: http://{HOST}:{PORT}")
    print(f"  FC Data: http://{HOST}:{PORT}/fcdata/")
    print(f"  Data:   http://{HOST}:{PORT}/data/")
    print(f"  Accounts: {len(account_locations)}")
    print(f"  Auto-refresh: {AUTO_REFRESH}s" if AUTO_REFRESH > 0 else "  Auto-refresh: Disabled")
    print("=" * 60)
    
    # Run FC detection diagnostic (only when DEBUG is enabled)
    if DEBUG:
        run_fc_diagnostic()
    
    app.run(host=HOST, port=PORT, debug=DEBUG)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        from datetime import datetime
        from pathlib import Path
        
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_msg = f"\n{'='*80}\n[CRITICAL ERROR] Script crashed with unhandled exception:\n{'='*80}\n"
        error_msg += f"Exception Type: {type(e).__name__}\n"
        error_msg += f"Exception Message: {e}\n"
        error_msg += f"\nFull Traceback:\n{traceback.format_exc()}"
        error_msg += f"{'='*80}\n"
        print(error_msg)
        
        # Save crash log to file
        crash_log_path = Path(__file__).parent / f"crash_log_{timestamp}.log"
        try:
            with open(crash_log_path, 'w', encoding='utf-8') as f:
                f.write(f"Crash Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(error_msg)
            print(f"[CRASH LOG SAVED] {crash_log_path}")
        except:
            print("[CRASH LOG] Failed to save crash log to file")
        
        # Keep window open for debugging
        print("\n[CRASH] Script has stopped. Window will remain open for debugging.")
        print("Press Enter to close this window...")
        input()
