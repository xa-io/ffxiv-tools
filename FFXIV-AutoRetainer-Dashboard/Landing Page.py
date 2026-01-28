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
# A comprehensive web dashboard that displays FFXIV character data from AutoRetainer, Altoholic, and Lifestream.
# Provides a modern, dark-themed UI accessible via browser showing characters, submarines, retainers,
# housing locations, marketboard items, gil totals, inventory tracking, MSQ progression, job levels,
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
# • Configurable display options (MINIMUM_MSQ_QUESTS, SHOW_CLASSES, SHOW_CURRENCIES)
# • Monthly income and daily repair cost calculations
# • Modern, responsive dark-themed UI with multi-account support
#
# Landing Page v1.15
# FFXIV AutoRetainer Dashboard
# Created by: https://github.com/xa-io
# Last Updated: 2026-01-27 17:00:00
#
# ## Release Notes ##
#
# v1.15 - Added 10 color theme presets with theme selector buttons under search bar
#         Themes: Default (Blue), Ultra Dark, Dark Gray, Ocean Blue, Forest Green,
#                 Crimson Red, Purple Haze, Pastel Pink, Dark Orange, Brown
#         DEFAULT_THEME config option in script and config.json
# v1.14 - Added character search bar in header (filters characters by name across all accounts)
#         Added loading overlay with animated progress bar for large character counts
#         Added anchor emoji favicon for browser tab
#         Shows "No results match your search..." error when no characters found
#         Auto-expands accounts with matching characters during search
# v1.13 - Fixed Current Class to show last played job (using LastJob/LastJobLevel from Altoholic)
#         Added Lowest/Highest Class fields - only show when level differs from Current
#         Added "Classes" sort button - requires SHOW_CLASSES=true
#         Added individual dye counts (Pure White, Jet Black, Pastel Pink)
# v1.12 - Added Hide Money Stats button to privatize earnings for screenshots
#         Hides: gil, treasure, FC points, venture coins, coffers, dyes, subs, retainers, MB items
#         Hides: monthly/annual income/cost/profit, retainer levels/gil, submarine levels/builds
#         Displays asterisks (*****) in place of hidden values, currencies section unaffected
# v1.11 - Improved Currencies display with categories and shortened names
#         Categories: Crystals, Common, Tomestones, Battle, Societies, Other
#         Shortened verbose names (e.g., "Allagan_Tomestone_Of_Poetics" → "Poetics")
#         Compact flexbox layout prevents overflow and saves space
# v1.10 - Added MSQ (Main Scenario Quest) progression percentage display
#         Shows "MSQ: X%" after Lv/Class, before housing icons
#         Color coded: green (≥90%), yellow (≥50%), gray (<50%)
#         Tooltip shows completed/total quest count
#         Quest data fetched from XIVAPI and cached locally
#         Extracts completed quests from Altoholic database
# v1.09 - Added Player Name@World row in expanded section for easy copy/paste
#         Added DoW/DoM collapsible section showing all combat job levels (final jobs only)
#         Added DoH/DoL collapsible section showing all crafter/gatherer levels
#         Added Currencies collapsible section showing all currencies character has
# v1.08 - Added Personal House and FC House filter buttons (show only characters with houses)
#         Added Retainer Lv and Submarine Lv sort buttons for min/max levels
#         Renamed sort buttons to emojis for compact display
#         Anonymize now hides housing addresses with TOP SECRET in expanded section
# v1.07 - Added Housing information from Lifestream DefaultConfig.json
#         Added Personal House and FC House display after Lv/Class in character header
#         Format: "Mist W1 P15" for Ward 1, Plot 15 in Mist district
# v1.06 - Added Inventory Space tracking from AutoRetainer DefaultConfig.json
#         Added Inventory row in character expanded breakdown with color coding (red >= 130, yellow >= 100)
#         Added Inventory sort button to sort characters by inventory usage
# v1.05 - Added Anonymize button to hide personal data for screenshots (names, worlds, FCs, retainers, subs)
#         Added Expand All / Collapse All buttons for character cards
# v1.04 - Added character filtering options to hide characters without submarines or retainers
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

# Display options
MINIMUM_MSQ_QUESTS = 5  # Minimum MSQ quests to show MSQ progress (0 to always show)
SHOW_CLASSES = True     # Show DoW/DoM and DoH/DoL job sections, disable to speed up page load
SHOW_CURRENCIES = True  # Show currencies section, disable to speed up page load
DEFAULT_THEME = "default"  # Theme preset for dashboard
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

# ===============================================
# Data Parsing Functions
# ===============================================
def load_external_config():
    """Load external config file if it exists"""
    global HOST, PORT, DEBUG, AUTO_REFRESH, account_locations
    global submarine_plans, retainer_plans, item_values
    global MINIMUM_MSQ_QUESTS, SHOW_CLASSES, SHOW_CURRENCIES, DEFAULT_THEME
    
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
        MINIMUM_MSQ_QUESTS = config.get("MINIMUM_MSQ_QUESTS", MINIMUM_MSQ_QUESTS)
        SHOW_CLASSES = config.get("SHOW_CLASSES", SHOW_CLASSES)
        SHOW_CURRENCIES = config.get("SHOW_CURRENCIES", SHOW_CURRENCIES)
        DEFAULT_THEME = config.get("DEFAULT_THEME", DEFAULT_THEME)
        
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


# ===============================================
# MSQ Quest Tracking - Chronological Quest List with Names
# ===============================================
# Complete MSQ quest data in CHRONOLOGICAL ORDER (955 trackable quests)
# Format: (quest_id, quest_name) tuples
# Progress is calculated by finding the HIGHEST position MSQ quest the character has
# This approach works even if Altoholic only tracks partial quest history
#
# Note: ~40 quests from quests.txt are not in quest_cache.json and cannot be tracked
# Total expected MSQ: ~993 | Trackable: 955 (938 base + 17 patch 7.x)
#
# Covers: ARR -> Seventh Astral Era -> Heavensward -> Dragonsong War ->
#         Stormblood -> Post-Ala Mhigan -> Shadowbringers -> Endwalker ->
#         Newfound Adventure -> Dawntrail -> Crossroads -> Into the Mist
MSQ_QUEST_DATA = [
    (65564, "To the Bannock"),  # 1
    (65621, "Close to Home"),  # 2
    (65644, "Close to Home"),  # 3
    (65645, "Close to Home"),  # 4
    (65659, "Close to Home"),  # 5
    (65660, "Close to Home"),  # 6
    (65665, "Spirithold Broken"),  # 7
    (65697, "Leia's Legacy"),  # 8
    (65711, "Surveying the Damage"),  # 9
    (65712, "On to Bentbranch"),  # 10
    (65737, "Passing Muster"),  # 11
    (65781, "It's Probably Pirates"),  # 12
    (65808, "Life, Materia and Everything"),  # 13
    (65839, "Step Nine"),  # 14
    (65843, "Out of House and Home"),  # 15
    (65856, "Way Down in the Hole"),  # 16
    (65864, "Supply and Demands"),  # 17
    (65865, "The Perfect Swarm"),  # 18
    (65866, "Last Letter to Lost Hope"),  # 19
    (65868, "Passing the Blade"),  # 20
    (65869, "Following Footfalls"),  # 21
    (65870, "Storms on the Horizon"),  # 22
    (65872, "Oh Captain, My Captain"),  # 23
    (65879, "Lord of the Inferno"),  # 24
    (65912, "You Shall Not Trespass"),  # 25
    (65913, "Don't Look Down"),  # 26
    (65915, "In the Grim Darkness of the Forest"),  # 27
    (65916, "Threat Level Elevated"),  # 28
    (65917, "Migrant Marauders"),  # 29
    (65920, "A Hearer Is Often Late"),  # 30
    (65923, "Salvaging the Scene"),  # 31
    (65933, "Sky-high"),  # 32
    (65938, "Thanks a Million"),  # 33
    (65939, "Relighting the Torch"),  # 34
    (65942, "On to the Drydocks"),  # 35
    (65948, "Without a Doubt"),  # 36
    (65949, "Do Angry Pirates Dream"),  # 37
    (65950, "Victory in Peril"),  # 38
    (65951, "Righting the Shipwright"),  # 39
    (65981, "Chasing Shadows"),  # 40
    (65982, "Dread Is in the Air"),  # 41
    (65983, "To Guard a Guardian"),  # 42
    (65984, "Festive Endeavors"),  # 43
    (65985, "Renewing the Covenant"),  # 44
    (65998, "On to Summerford"),  # 45
    (65999, "Dressed to Call"),  # 46
    (66001, "Washed Up"),  # 47
    (66002, "Double Dealing"),  # 48
    (66003, "Loam Maintenance"),  # 49
    (66004, "Plowshares to Swords"),  # 50
    (66005, "Just Deserts"),  # 51
    (66039, "Give It to Me Raw"),  # 52
    (66043, "The Gridanian Envoy"),  # 53
    (66045, "The Scions of the Seventh Dawn"),  # 54
    (66046, "A Wild Rose by Any Other Name"),  # 55
    (66047, "A Hero in the Making"),  # 56
    (66049, "Sylph-management"),  # 57
    (66050, "Into the Beast's Maw"),  # 58
    (66052, "Wrath of the Titan"),  # 59
    (66053, "All Good Things"),  # 60
    (66054, "Eyes on Me"),  # 61
    (66055, "Lady of the Vortex"),  # 62
    (66056, "Reclamation"),  # 63
    (66057, "Escape from Castrum Centri"),  # 64
    (66058, "The Black Wolf's Ultimatum"),  # 65
    (66064, "The Ul'dahn Envoy"),  # 66
    (66079, "Lurkers in the Grotto"),  # 67
    (66080, "Feint and Strike"),  # 68
    (66081, "A Mizzenmast Repast"),  # 69
    (66082, "The Lominsan Envoy"),  # 70
    (66086, "Underneath the Sultantree"),  # 71
    (66087, "Duty, Honor, Country"),  # 72
    (66088, "A Royal Reception"),  # 73
    (66104, "Close to Home"),  # 74
    (66105, "Close to Home"),  # 75
    (66106, "Close to Home"),  # 76
    (66110, "Dressed to Deceive"),  # 77
    (66131, "We Must Rebuild"),  # 78
    (66154, "Unsolved Mystery"),  # 79
    (66155, "What Poor People Think"),  # 80
    (66156, "A Proper Burial"),  # 81
    (66157, "For the Children"),  # 82
    (66158, "Amalj'aa Wrong Places"),  # 83
    (66159, "Takin' What They're Givin'"),  # 84
    (66164, "Secrets and Lies"),  # 85
    (66177, "A Matter of Tradition"),  # 86
    (66196, "Into a Copper Hell"),  # 87
    (66207, "Nothing to See Here"),  # 88
    (66209, "Call of the Sea"),  # 89
    (66210, "Call of the Sea"),  # 90
    (66212, "Call of the Forest"),  # 91
    (66213, "Fire in the Gloom"),  # 92
    (66214, "Call of the Desert"),  # 93
    (66216, "The Company You Keep (Twin Adder)"),  # 94
    (66217, "The Company You Keep (Maelstrom)"),  # 95
    (66218, "The Company You Keep (Immortal Flames)"),  # 96
    (66219, "Wood's Will Be Done"),  # 97
    (66220, "Till Sea Swallows All"),  # 98
    (66221, "For Coin and Country"),  # 99
    (66225, "Men of the Blue Tattoos"),  # 100
    (66226, "High Society"),  # 101
    (66245, "Sylphic Studies"),  # 102
    (66246, "First Impressions"),  # 103
    (66251, "First Contact"),  # 104
    (66255, "Presence of the Enemy"),  # 105
    (66260, "Brotherly Love"),  # 106
    (66261, "Spirited Away"),  # 107
    (66273, "Like Fine Wine"),  # 108
    (66274, "Sylphish Concerns"),  # 109
    (66279, "A Simple Gift"),  # 110
    (66280, "Believe in Your Sylph"),  # 111
    (66282, "Back from the Wood"),  # 112
    (66283, "Shadow of Darkness"),  # 113
    (66284, "Highbridge Times"),  # 114
    (66292, "Where There Is Smoke"),  # 115
    (66293, "On to Little Ala Mhigo"),  # 116
    (66297, "Tea for Three"),  # 117
    (66298, "Foot in the Door"),  # 118
    (66299, "Meeting with the Resistance"),  # 119
    (66301, "Killing Him Softly"),  # 120
    (66310, "Helping Horn"),  # 121
    (66311, "He Ain't Heavy"),  # 122
    (66312, "Come Highly Recommended"),  # 123
    (66313, "The Bear and the Young'uns' Cares"),  # 124
    (66314, "Wilred Wants You"),  # 125
    (66318, "Big Trouble in Little Ala Mhigo"),  # 126
    (66319, "Back to Square One"),  # 127
    (66322, "Seeing Eye to Winged Eye"),  # 128
    (66323, "Rock of Rancor"),  # 129
    (66335, "Power of Deduction"),  # 130
    (66336, "Secret of the White Lily"),  # 131
    (66337, "Skeletons in Her Closet"),  # 132
    (66345, "Tales from the Tidus Slayer"),  # 133
    (66346, "Hungry Hungry Goobbues"),  # 134
    (66347, "The Lominsan Way"),  # 135
    (66348, "Nix That"),  # 136
    (66350, "A Modest Proposal"),  # 137
    (66357, "The Perfect Prey"),  # 138
    (66358, "When the Worm Turns"),  # 139
    (66367, "There and Back Again"),  # 140
    (66368, "The Things We Do for Cheese"),  # 141
    (66376, "An Offer You Can Refuse"),  # 142
    (66379, "It Won't Work"),  # 143
    (66381, "Give a Man a Drink"),  # 144
    (66382, "That Weight"),  # 145
    (66384, "Battle Scars"),  # 146
    (66386, "It Was a Very Good Year"),  # 147
    (66391, "In the Company of Heroes"),  # 148
    (66392, "As You Wish"),  # 149
    (66393, "Lord of Crags"),  # 150
    (66412, "Bringing out the Dead"),  # 151
    (66414, "Bury Me Not on the Lone Prairie"),  # 152
    (66419, "He Who Waited Behind"),  # 153
    (66420, "Cold Reception"),  # 154
    (66422, "The Unending War"),  # 155
    (66423, "Men of Honor"),  # 156
    (66425, "Three for Three"),  # 157
    (66426, "The Rose and the Unicorn"),  # 158
    (66433, "The Talk of Coerthas"),  # 159
    (66446, "Road to Redemption"),  # 160
    (66447, "Following the Evidence"),  # 161
    (66448, "In the Eyes of Gods and Men"),  # 162
    (66460, "Ye of Little Faith"),  # 163
    (66463, "Factual Folklore"),  # 164
    (66474, "Influencing Inquisitors"),  # 165
    (66475, "By the Lights of Ishgard"),  # 166
    (66476, "Blood for Blood"),  # 167
    (66477, "The Heretic among Us"),  # 168
    (66488, "In Pursuit of the Past"),  # 169
    (66489, "Into the Eye of the Storm"),  # 170
    (66491, "Sealed with Science"),  # 171
    (66492, "With the Utmost Care"),  # 172
    (66495, "A Promising Prospect"),  # 173
    (66496, "It's Probably Not Pirates"),  # 174
    (66497, "Representing the Representative"),  # 175
    (66498, "The Reluctant Researcher"),  # 176
    (66499, "Sweet Somethings"),  # 177
    (66503, "History Repeating"),  # 178
    (66511, "Better Late than Never"),  # 179
    (66514, "Casing the Castrum"),  # 180
    (66516, "Eyes on the Empire"),  # 181
    (66517, "Footprints in the Snow"),  # 182
    (66518, "Monumental Hopes"),  # 183
    (66519, "Notorious Biggs"),  # 184
    (66520, "Come-Into-My-Castrum"),  # 185
    (66522, "Getting Even with Garlemald"),  # 186
    (66537, "Drowning Out the Voices"),  # 187
    (66538, "Acting the Part"),  # 188
    (66540, "Fool Me Twice"),  # 189
    (66541, "Every Little Thing She Does Is Magitek"),  # 190
    (66573, "A Hero in Need"),  # 191
    (69388, "Prudence at This Junction"),  # 192
    (69389, "Heir Today, Gone Tomorrow"),  # 193
    (69390, "Eggs over Queasy"),  # 194
    (69391, "A Soldier's Breakfast"),  # 195
    (69392, "We Come in Peace"),  # 196
    (69393, "Dance Dance Diplomacy"),  # 197
    (69394, "Forest Friend"),  # 198
    (69395, "Druthers House Rules"),  # 199
    (69396, "Never Forget"),  # 200
    (69397, "Microbrewing"),  # 201
    (69398, "Nouveau Riche"),  # 202
    (69399, "Terror at Fallgourd"),  # 203
    (69400, "Ziz Is So Ridiculous"),  # 204
    (69401, "Trial by Turtle"),  # 205
    (69402, "What Do You Mean You Forgot the Wine"),  # 206
    (69403, "You Can't Take It with You"),  # 207
    (69404, "The Final Flight of the Enterprise"),  # 208
    (69405, "The Best Inventions"),  # 209
    (69406, "The Curious Case of Giggity"),  # 210
    (69407, "Dressed for Conquest"),  # 211
    (69408, "Hearts on Fire"),  # 212
    (69409, "Rock the Castrum"),  # 213
    (70057, "Operation Archon"),  # 214
    (70058, "The Ultimate Weapon"),  # 215
    (65588, "Traitor in the Midst"),  # 216
    (65589, "Back and Fourth"),  # 217
    (65590, "Coming to Terms"),  # 218
    (65593, "The Intercession of Saints"),  # 219
    (65598, "Strength in Unity"),  # 220
    (65605, "Dark Words, Dark Deeds"),  # 221
    (65610, "First Blood"),  # 222
    (65611, "The Path of the Righteous"),  # 223
    (65613, "For the Greater Good"),  # 224
    (65614, "Tendrils of Intrigue"),  # 225
    (65618, "A Simple Plan"),  # 226
    (65620, "The Instruments of Our Deliverance"),  # 227
    (65622, "The Road Less Traveled"),  # 228
    (65623, "Eyes Unclouded"),  # 229
    (65624, "The Reason Roaille"),  # 230
    (65625, "Let Us Cling Together"),  # 231
    (65899, "Good Intentions"),  # 232
    (65900, "Bait and Switch"),  # 233
    (65901, "Best Laid Schemes"),  # 234
    (65902, "The Rising Chorus"),  # 235
    (65904, "On the Counteroffensive"),  # 236
    (65905, "An Uninvited Ascian"),  # 237
    (65906, "Mask of Grief"),  # 238
    (65907, "Defenders for Ishgard"),  # 239
    (65908, "The Wyrm's Roar"),  # 240
    (65909, "Committed to the Cause"),  # 241
    (65927, "Volunteer Dragonslayers"),  # 242
    (65954, "An Allied Perspective"),  # 243
    (65956, "Administrative Decision"),  # 244
    (65957, "An Unexpected Ambition"),  # 245
    (65958, "Ancient Ways, Timeless Wants"),  # 246
    (65959, "Where We Are Needed"),  # 247
    (65960, "The Least among Us"),  # 248
    (65961, "A Time to Every Purpose"),  # 249
    (65962, "Come, but Not Gone"),  # 250
    (65963, "The Parting Glass"),  # 251
    (65964, "Before the Dawn"),  # 252
    (65965, "In Memory of Moenbryda"),  # 253
    (66711, "The Price of Principles"),  # 254
    (66725, "Hail to the King, Kupo"),  # 255
    (66726, "You Have Selected Regicide"),  # 256
    (66727, "On the Properties of Primals"),  # 257
    (66728, "The Gifted"),  # 258
    (66882, "A Final Temptation"),  # 259
    (66883, "The Mother of Exiles"),  # 260
    (66888, "Why We Adventure"),  # 261
    (66892, "The Sea Rises"),  # 262
    (66894, "Scouts in Distress"),  # 263
    (66895, "The Gift of Eternity"),  # 264
    (66896, "Into the Heart of the Whorl"),  # 265
    (66897, "Lord of the Whorl"),  # 266
    (66898, "When Yugiri Met the Fraternity"),  # 267
    (66899, "Through the Maelstrom"),  # 268
    (66978, "The Great Divide"),  # 269
    (66979, "Desperate Times"),  # 270
    (66982, "Revolution"),  # 271
    (66983, "Stories We Tell"),  # 272
    (66984, "Lord of Levin"),  # 273
    (66989, "What Little Gods Are Made Of"),  # 274
    (66992, "Guardian of Eorzea"),  # 275
    (66993, "Recruiting the Realm"),  # 276
    (66994, "Heretical Harassment"),  # 277
    (66995, "When the Cold Sets In"),  # 278
    (66996, "Brave New Companions"),  # 279
    (69410, "Moving On"),  # 280
    (69411, "All Things in Time"),  # 281
    (69412, "Laying the Foundation"),  # 282
    (69413, "It's Possibly a Primal"),  # 283
    (69414, "Build on the Stone"),  # 284
    (69415, "Still Waters"),  # 285
    (69416, "Promises to Keep"),  # 286
    (69417, "Yugiri's Game"),  # 287
    (69418, "All Due Respect"),  # 288
    (69419, "Shock and Awe"),  # 289
    (69420, "Reap the Whirlwind"),  # 290
    (69421, "Levin an Impression"),  # 291
    (69422, "Chasing Ivy"),  # 292
    (69423, "In Flagrante Delicto"),  # 293
    (69424, "Aether on Demand"),  # 294
    (70127, "The Steps of Faith"),  # 295
    (67116, "Coming to Ishgard"),  # 296
    (67117, "Taking in the Sights"),  # 297
    (67118, "The Better Half"),  # 298
    (67119, "Over the Wall"),  # 299
    (67120, "Work in Progress"),  # 300
    (67121, "The First and Foremost"),  # 301
    (67122, "From on High"),  # 302
    (67123, "Reconnaissance Lost"),  # 303
    (67124, "At the End of Our Hope"),  # 304
    (67125, "Knights Be Not Proud"),  # 305
    (67126, "Onwards and Upwards"),  # 306
    (67127, "An Indispensable Ally"),  # 307
    (67128, "Meeting the Neighbors"),  # 308
    (67129, "Sense of Urgency"),  # 309
    (67130, "Hope Springs Eternal"),  # 310
    (67131, "A Series of Unfortunate Events"),  # 311
    (67132, "A Reward Long in Coming"),  # 312
    (67133, "Divine Intervention"),  # 313
    (67134, "Disclosure"),  # 314
    (67135, "Flame General Affairs"),  # 315
    (67136, "In Search of Raubahn"),  # 316
    (67137, "Keeping the Flame Alive"),  # 317
    (67138, "To Siege or Not to Siege"),  # 318
    (67139, "Alphinaud's Way"),  # 319
    (67140, "In Search of Iceheart"),  # 320
    (67141, "From One Heretic to Another"),  # 321
    (67142, "Sounding Out the Amphitheatre"),  # 322
    (67143, "Camp of the Convictors"),  # 323
    (67144, "Purple Flame, Purple Flame"),  # 324
    (67145, "Where the Chocobos Roam"),  # 325
    (67146, "Worse than Dragons"),  # 326
    (67147, "The Trine Towers"),  # 327
    (67148, "Gifts for the Outcasts"),  # 328
    (67149, "The Nonmind"),  # 329
    (67150, "A Gnathic Deity"),  # 330
    (67151, "Breaking into Hives"),  # 331
    (67152, "Lord of the Hive"),  # 332
    (67153, "Mourn in Passing"),  # 333
    (67154, "Beyond the Clouds"),  # 334
    (67155, "Mountaintop Diplomacy"),  # 335
    (67156, "Moghan's Trial"),  # 336
    (67157, "Mogmug's Trial"),  # 337
    (67158, "Mogwin's Trial"),  # 338
    (67159, "Moglin's Judgment"),  # 339
    (67160, "Leaving Moghome"),  # 340
    (67161, "The Road to Zenith"),  # 341
    (67162, "Waiting for the Wind to Change"),  # 342
    (67163, "Heart of Ice"),  # 343
    (67164, "The Wyrm's Lair"),  # 344
    (67165, "New Winds, Old Friends"),  # 345
    (67166, "A General Summons"),  # 346
    (67167, "Awakening in Ul'dah"),  # 347
    (67168, "A Brave Resolution"),  # 348
    (67169, "Ready to Fly"),  # 349
    (67170, "Into the Aery"),  # 350
    (67171, "The Song Begins"),  # 351
    (67172, "Unrest in Ishgard"),  # 352
    (67173, "He Who Would Not Be Denied"),  # 353
    (67174, "Ill-weather Friends"),  # 354
    (67175, "Fire and Blood"),  # 355
    (67176, "A Knight's Calling"),  # 356
    (67177, "The Sins of Antiquity"),  # 357
    (67178, "In Search of the Soleil"),  # 358
    (67179, "Into the Blue"),  # 359
    (67180, "Familiar Faces"),  # 360
    (67181, "Devourer of Worlds"),  # 361
    (67182, "Black and the White"),  # 362
    (67183, "Bolt, Chain, and Island"),  # 363
    (67184, "A Difference of Opinion"),  # 364
    (67185, "One Good Turn"),  # 365
    (67186, "An Engineering Enterprise"),  # 366
    (67187, "Aetherial Trail"),  # 367
    (67188, "Lost in the Lifestream"),  # 368
    (67189, "Tataru's Surprise"),  # 369
    (67190, "Onward to Sharlayan"),  # 370
    (67191, "A Great New Nation"),  # 371
    (67192, "Golems Begone"),  # 372
    (67193, "An Illuminati Incident"),  # 373
    (67194, "Leaving Idyllshire"),  # 374
    (67195, "Matoya's Cave"),  # 375
    (67196, "Forbidden Knowledge"),  # 376
    (67197, "An Eye for Aether"),  # 377
    (67198, "Hour of Departure"),  # 378
    (67199, "The First Flight of the Excelsior"),  # 379
    (67200, "Systematic Exploration"),  # 380
    (67201, "In Node We Trust"),  # 381
    (67202, "Chimerical Maintenance"),  # 382
    (67203, "Close Encounters of the VIth Kind"),  # 383
    (67204, "Fetters of Lament"),  # 384
    (67205, "Heavensward"),  # 385
    (67529, "The Spice of Life"),  # 386
    (67530, "Noble Indiscretions"),  # 387
    (67531, "A Child Apart"),  # 388
    (67532, "Bloodlines"),  # 389
    (67692, "An Uncertain Future"),  # 390
    (67693, "Breaking the Cycle"),  # 391
    (67694, "Another Time, Another Place"),  # 392
    (67695, "In the Eye of the Beholder"),  # 393
    (67696, "A Little Slow, a Little Late"),  # 394
    (67697, "Dreams of the Lost"),  # 395
    (67698, "Against the Dying of the Light"),  # 396
    (67699, "As Goes Light, So Goes Darkness"),  # 397
    (67767, "As It Once Was"),  # 398
    (67768, "The Word of the Mother"),  # 399
    (67769, "This War of Ours"),  # 400
    (67770, "Staunch Conviction"),  # 401
    (67771, "Once More, a Favor"),  # 402
    (67772, "For Those We Have Lost"),  # 403
    (67773, "Consequences"),  # 404
    (67774, "Choices"),  # 405
    (67775, "A Spectacle for the Ages"),  # 406
    (67776, "For Those We Can Yet Save"),  # 407
    (67777, "Causes and Costs"),  # 408
    (67778, "The Man Within"),  # 409
    (67779, "An Ally for Ishgard"),  # 410
    (67780, "Winning Over the Wyrm"),  # 411
    (67781, "An End to the Song"),  # 412
    (67782, "Heroes of the Hour"),  # 413
    (67783, "Litany of Peace"),  # 414
    (67877, "Promises Kept"),  # 415
    (67878, "Shadows of the First"),  # 416
    (67879, "Two Sides of a Coin"),  # 417
    (67880, "Unlikely Allies"),  # 418
    (67881, "The Beast That Mourned at the Heart of the Mountain"),  # 419
    (67882, "Beneath a Star-filled Sky"),  # 420
    (67883, "When We Were Free"),  # 421
    (67884, "Honorable Heroes"),  # 422
    (67885, "One Life for One World"),  # 423
    (67886, "An Ending to Mark a New Beginning"),  # 424
    (67887, "Tidings from Gyr Abania"),  # 425
    (67888, "An Envoy for Ishgard"),  # 426
    (67889, "An Allied Decision"),  # 427
    (67890, "Griffin, Griffin on the Wall"),  # 428
    (67891, "Louisoix's Finest Student"),  # 429
    (67892, "The Obvious Solution"),  # 430
    (67893, "The Greater Obeisance"),  # 431
    (67894, "Fly Free, My Pretty"),  # 432
    (67895, "The Far Edge of Fate"),  # 433
    (67982, "Beyond the Great Wall"),  # 434
    (67983, "Lyse Takes the Lead"),  # 435
    (67984, "The Promise of a New Beginning"),  # 436
    (67985, "A Haven for the Bold"),  # 437
    (67986, "A Bargain Struck"),  # 438
    (67987, "A Friend of a Friend in Need"),  # 439
    (67988, "Signed, Sealed, to Be Delivered"),  # 440
    (67989, "Best Served with Cold Steel"),  # 441
    (67990, "Let Fill Your Hearts with Pride"),  # 442
    (67991, "A Familiar Face Forgotten"),  # 443
    (67992, "The Prodigal Daughter"),  # 444
    (67993, "A Life More Ordinary"),  # 445
    (67994, "The Color of Angry Qiqirn"),  # 446
    (67995, "The Black Wolf's Pups"),  # 447
    (67996, "Homeward Bound"),  # 448
    (67997, "Where Men Go as One"),  # 449
    (67998, "Crossing the Velodyna"),  # 450
    (67999, "In Crimson It Began"),  # 451
    (68000, "The Fires Fade"),  # 452
    (68001, "Bereft of Hearth and Home"),  # 453
    (68002, "Divide and Conquer"),  # 454
    (68003, "Lies, Damn Lies, and Pirates"),  # 455
    (68004, "Tales from the Far East"),  # 456
    (68005, "Not without Incident"),  # 457
    (68006, "The Man from Ul'dah"),  # 458
    (68007, "Where the Streets Are Paved with Koban"),  # 459
    (68008, "By the Grace of Lord Lolorito"),  # 460
    (68009, "A Good Samurai Is Hard to Find"),  # 461
    (68010, "It's Probably a Trap"),  # 462
    (68011, "Making the Catfish Sing"),  # 463
    (68012, "Once More, to the Ruby Sea"),  # 464
    (68013, "Open Water"),  # 465
    (68014, "Boys with Boats"),  # 466
    (68015, "To Bend with the Wind"),  # 467
    (68016, "Confederate Consternation"),  # 468
    (68017, "Alisaie's Stones"),  # 469
    (68018, "Under the Sea"),  # 470
    (68019, "Of Kojin and Kami"),  # 471
    (68020, "In Soroban We Trust"),  # 472
    (68021, "Forever and Ever Apart"),  # 473
    (68022, "In Darkness the Magatama Dreams"),  # 474
    (68023, "The Whims of the Divine"),  # 475
    (68024, "Breaking and Delivering"),  # 476
    (68025, "The Lord of the Revel"),  # 477
    (68026, "Tide Goes in, Imperials Go Out"),  # 478
    (68027, "A Silence in Three Parts"),  # 479
    (68028, "Life after Doma"),  # 480
    (68029, "The Stubborn Remainder"),  # 481
    (68030, "The Ones We Leave Behind"),  # 482
    (68031, "A New Ruby Tithe"),  # 483
    (68032, "The Will to Live"),  # 484
    (68033, "Daughter of the Deep"),  # 485
    (68034, "The Time between the Seconds"),  # 486
    (68035, "All the Little Angels"),  # 487
    (68036, "The Search for Lord Hien"),  # 488
    (68037, "A Season for War"),  # 489
    (68038, "An Impossible Dream"),  # 490
    (68039, "Stars in the Dark"),  # 491
    (68040, "A Warrior's Welcome"),  # 492
    (68041, "The Heart of Nations"),  # 493
    (68042, "A Trial Before the Trial"),  # 494
    (68043, "In the Footsteps of Bardam the Brave"),  # 495
    (68044, "The Children of Azim"),  # 496
    (68045, "The Labors of Magnai"),  # 497
    (68046, "For Love of the Moon"),  # 498
    (68047, "Sworn Enemies of the Sun"),  # 499
    (68048, "The Undying Ones"),  # 500
    (68049, "A Final Peace"),  # 501
    (68050, "As the Gods Will"),  # 502
    (68051, "Naadam"),  # 503
    (68052, "Glory to the Khagan"),  # 504
    (68053, "In Crimson They Walked"),  # 505
    (68054, "The Hour of Reckoning"),  # 506
    (68055, "The Room Where It Happened"),  # 507
    (68056, "Seeds of Despair"),  # 508
    (68057, "The Limits of Our Endurance"),  # 509
    (68058, "The Doma Within"),  # 510
    (68059, "On the Eve of Destiny"),  # 511
    (68060, "The Die Is Cast"),  # 512
    (68061, "The World Turned Upside Down"),  # 513
    (68062, "A Swift and Secret Departure"),  # 514
    (68063, "While You Were Away"),  # 515
    (68064, "Rhalgr's Beacon"),  # 516
    (68065, "The Fortunes of War"),  # 517
    (68066, "Rising Fortunes, Rising Spirits"),  # 518
    (68067, "The Lure of the Dream"),  # 519
    (68068, "The Lady of Bliss"),  # 520
    (68069, "The Silence of the Gods"),  # 521
    (68070, "The First of Many"),  # 522
    (68071, "Strong and Unified"),  # 523
    (68072, "Hells Open"),  # 524
    (68073, "Heavens Weep"),  # 525
    (68074, "The Road Home"),  # 526
    (68075, "For the Living and the Dead"),  # 527
    (68076, "Above the Churning Waters"),  # 528
    (68077, "The Path Forward"),  # 529
    (68078, "With Tired Hands We Toil"),  # 530
    (68079, "Where Courage Endures"),  # 531
    (68080, "The Price of Freedom"),  # 532
    (68081, "Raubahn's Invitation"),  # 533
    (68082, "Liberty or Death"),  # 534
    (68083, "The Lady in Red"),  # 535
    (68084, "Upon the Great Loch's Shore"),  # 536
    (68085, "The Key to Victory"),  # 537
    (68086, "The Resonant"),  # 538
    (68087, "The Legacy of Our Fathers"),  # 539
    (68088, "The Measure of His Reach"),  # 540
    (68089, "Stormblood"),  # 541
    (68166, "Here There Be Xaela"),  # 542
    (68171, "Future Rust, Future Dust"),  # 543
    (68172, "A Dash of Green"),  # 544
    (68173, "Ye Wayward Brothers"),  # 545
    (68174, "Token of Faith"),  # 546
    (68215, "The Last Voyage"),  # 547
    (68217, "The Solace of the Sea"),  # 548
    (68470, "A Glimpse of Madness"),  # 549
    (68471, "Path of No Return"),  # 550
    (68482, "How Tataru Got Her Groove Back"),  # 551
    (68483, "Broken Steel, Broken Men"),  # 552
    (68489, "The Arrows of Misfortune"),  # 553
    (68490, "Hard Country"),  # 554
    (68491, "Death by a Thousand Rocks"),  # 555
    (68498, "Arenvald's Adventure"),  # 556
    (68499, "The Darkness Below"),  # 557
    (68500, "The Mad King's Trove"),  # 558
    (68501, "The Butcher's Blood"),  # 559
    (68502, "Echoes of an Echo"),  # 560
    (68503, "A Sultana's Strings"),  # 561
    (68504, "A Sultana's Duty"),  # 562
    (68505, "A Sultana's Resolve"),  # 563
    (68506, "Securing the Saltery"),  # 564
    (68507, "A Blissful Arrival"),  # 565
    (68508, "Return of the Bull"),  # 566
    (68558, "Tidings from the East"),  # 567
    (68559, "The Sword in the Store"),  # 568
    (68560, "Hope on the Waves"),  # 569
    (68561, "Elation and Trepidation"),  # 570
    (68562, "Storm on the Horizon"),  # 571
    (68563, "His Forgotten Home"),  # 572
    (68564, "A Guilty Conscience"),  # 573
    (68565, "Rise of a New Sun"),  # 574
    (68606, "Gosetsu and Tsuyu"),  # 575
    (68607, "Gone Like the Morning Dew"),  # 576
    (68608, "Fruits of Her Labor"),  # 577
    (68609, "Conscripts and Contingencies"),  # 578
    (68610, "The Primary Agreement"),  # 579
    (68611, "Under the Moonlight"),  # 580
    (68612, "Emissary of the Dawn"),  # 581
    (68679, "Sisterly Act"),  # 582
    (68680, "Feel the Burn"),  # 583
    (68681, "Shadows in the Empire"),  # 584
    (68682, "A Power in Slumber"),  # 585
    (68683, "The Will of the Moon"),  # 586
    (68684, "The Call"),  # 587
    (68685, "Prelude in Violet"),  # 588
    (68715, "Soul Searching"),  # 589
    (68716, "A Defector's Tidings"),  # 590
    (68717, "Seiryu's Wall"),  # 591
    (68718, "Parley on the Front Lines"),  # 592
    (68719, "The Face of War"),  # 593
    (68720, "A Brief Reprieve"),  # 594
    (68721, "A Requiem for Heroes"),  # 595
    (68815, "The Syrcus Trench"),  # 596
    (68816, "City of the First"),  # 597
    (68817, "Travelers of Norvrandt"),  # 598
    (68818, "In Search of Alphinaud"),  # 599
    (68819, "A Still Tide"),  # 600
    (68820, "Open Arms, Closed Gate"),  # 601
    (68821, "A Fickle Existence"),  # 602
    (68822, "City of Final Pleasures"),  # 603
    (68823, "Free to Sightsee"),  # 604
    (68824, "A Taste of Honey"),  # 605
    (68825, "A Blessed Instrument"),  # 606
    (68826, "Emergent Splendor"),  # 607
    (68827, "In Search of Alisaie"),  # 608
    (68828, "City of the Mord"),  # 609
    (68829, "Working Off the Meal"),  # 610
    (68830, "A Desert Crossing"),  # 611
    (68831, "Following in Her Footprints"),  # 612
    (68832, "Culling Their Ranks"),  # 613
    (68833, "A Purchase of Fruit"),  # 614
    (68834, "The Time Left to Us"),  # 615
    (68835, "Tears on the Sand"),  # 616
    (68836, "The Lightwardens"),  # 617
    (68837, "Warrior of Darkness"),  # 618
    (68838, "An Unwelcome Guest"),  # 619
    (68839, "The Crystarium's Resolve"),  # 620
    (68840, "Logistics of War"),  # 621
    (68841, "The Oracle of Light"),  # 622
    (68842, "Il Mheg, the Faerie Kingdom"),  # 623
    (68843, "Sul Uin's Request"),  # 624
    (68844, "Ys Iala's Errand"),  # 625
    (68845, "Oul Sigun's Plea"),  # 626
    (68846, "Unto the Truth"),  # 627
    (68847, "Courting Cooperation"),  # 628
    (68848, "The Key to the Castle"),  # 629
    (68849, "A Visit to the Nu Mou"),  # 630
    (68850, "A Fitting Payment"),  # 631
    (68851, "Spore Sweeper"),  # 632
    (68852, "The Lawless Ones"),  # 633
    (68853, "The Elder's Answer"),  # 634
    (68854, "A Resounding Roar"),  # 635
    (68855, "Memento of a Friend"),  # 636
    (68856, "Acht-la Ormh Inn"),  # 637
    (68857, "The Wheel Turns"),  # 638
    (68858, "A Party Soon Divided"),  # 639
    (68859, "A Little Faith"),  # 640
    (68860, "Into the Dark"),  # 641
    (68861, "A Day in the Neighborhood"),  # 642
    (68862, "A Helping Hand"),  # 643
    (68863, "Lost but Not Forgotten"),  # 644
    (68864, "Saying Good-bye"),  # 645
    (68865, "Stirring Up Trouble"),  # 646
    (68866, "A Beeautiful Plan"),  # 647
    (68867, "An Unwanted Proposal"),  # 648
    (68868, "Put to the Proof"),  # 649
    (68869, "Into the Wood"),  # 650
    (68870, "Top of the Tree"),  # 651
    (68871, "Look to the Stars"),  # 652
    (68872, "Mi Casa, Toupasa"),  # 653
    (68873, "Legend of the Not-so-hidden Temple"),  # 654
    (68874, "The Aftermath"),  # 655
    (68875, "In Good Faith"),  # 656
    (68876, "The Burden of Knowledge"),  # 657
    (68877, "Bearing with It"),  # 658
    (68878, "Out of the Wood"),  # 659
    (69142, "When It Rains"),  # 660
    (69143, "Word from On High"),  # 661
    (69144, "Small Favors"),  # 662
    (69145, "The Best Way Out"),  # 663
    (69146, "Free Trade"),  # 664
    (69147, "The Trolley Problem"),  # 665
    (69148, "Rust and Ruin"),  # 666
    (69149, "On Track"),  # 667
    (69150, "Down for Maintenance"),  # 668
    (69151, "The Truth Hurts"),  # 669
    (69152, "A Convenient Distraction"),  # 670
    (69153, "A Dirty Job"),  # 671
    (69154, "Have a Heart"),  # 672
    (69155, "Full Steam Ahead"),  # 673
    (69156, "Crossing Paths"),  # 674
    (69157, "A Fresh Start"),  # 675
    (69158, "More than a Hunch"),  # 676
    (69166, "Return to Eulmore"),  # 677
    (69167, "A Feast of Lies"),  # 678
    (69168, "Paradise Fallen"),  # 679
    (69169, "The Ladder"),  # 680
    (69170, "The View from Above"),  # 681
    (69171, "In Mt. Gulg's Shadow"),  # 682
    (69172, "A Gigantic Undertaking"),  # 683
    (69173, "Meet the Tholls"),  # 684
    (69174, "A-Digging We Will Go"),  # 685
    (69175, "The Duergar's Tewel"),  # 686
    (69176, "Rich Veins of Hope"),  # 687
    (69177, "That None Shall Ever Again"),  # 688
    (69178, "A Breath of Respite"),  # 689
    (69179, "Extinguishing the Last Light"),  # 690
    (69180, "Reassuring the Masses"),  # 691
    (69181, "In His Garden"),  # 692
    (69182, "The Unbroken Thread"),  # 693
    (69183, "To Storm-tossed Seas"),  # 694
    (69184, "Waiting in the Depths"),  # 695
    (69185, "City of the Ancients"),  # 696
    (69186, "The Light of Inspiration"),  # 697
    (69187, "The Illuminated Land"),  # 698
    (69188, "The End of a World"),  # 699
    (69189, "A Greater Purpose"),  # 700
    (69190, "Shadowbringers"),  # 701
    (69209, "Shaken Resolve"),  # 702
    (69210, "A Grand Adventure"),  # 703
    (69211, "A Welcome Guest"),  # 704
    (69212, "Good for the Soul"),  # 705
    (69213, "Nowhere to Turn"),  # 706
    (69214, "A Notable Absence"),  # 707
    (69215, "For the People"),  # 708
    (69216, "Finding Good Help"),  # 709
    (69217, "Moving Forward"),  # 710
    (69218, "Vows of Virtue, Deeds of Cruelty"),  # 711
    (69297, "Old Enemies, New Threats"),  # 712
    (69298, "The Way Home"),  # 713
    (69299, "Seeking Counsel"),  # 714
    (69300, "Facing the Truth"),  # 715
    (69301, "A Sleep Disturbed"),  # 716
    (69302, "An Old Friend"),  # 717
    (69303, "Deep Designs"),  # 718
    (69304, "A Whale's Tale"),  # 719
    (69305, "Beneath the Surface"),  # 720
    (69306, "Echoes of a Fallen Star"),  # 721
    (69307, "In the Name of the Light"),  # 722
    (69308, "Heroic Dreams"),  # 723
    (69309, "Fraying Threads"),  # 724
    (69310, "Food for the Soul"),  # 725
    (69311, "Faded Memories"),  # 726
    (69312, "Etched in the Stars"),  # 727
    (69313, "The Converging Light"),  # 728
    (69314, "Hope's Confluence"),  # 729
    (69315, "Nothing Unsaid"),  # 730
    (69316, "The Journey Continues"),  # 731
    (69317, "Unto the Morrow"),  # 732
    (69318, "Reflections in Crystal"),  # 733
    (69543, "Alisaie's Quest"),  # 734
    (69544, "The Wisdom of Allag"),  # 735
    (69545, "Reviving the Legacy"),  # 736
    (69546, "Forget Us Not"),  # 737
    (69547, "Like Master, Like Pupil"),  # 738
    (69548, "The Admiral's Resolve"),  # 739
    (69549, "The Search for Sicard"),  # 740
    (69550, "On Rough Seas"),  # 741
    (69551, "The Great Ship Vylbrand"),  # 742
    (69552, "Futures Rewritten"),  # 743
    (69594, "Unto the Breach"),  # 744
    (69595, "Here Be Dragons"),  # 745
    (69596, "Righteous Indignation"),  # 746
    (69597, "For Vengeance"),  # 747
    (69598, "The Flames of War"),  # 748
    (69599, "When the Dust Settles"),  # 749
    (69600, "The Company We Keep"),  # 750
    (69601, "On Official Business"),  # 751
    (69602, "Death Unto Dawn"),  # 752
    (69893, "The Next Ship to Sail"),  # 753
    (69894, "Old Sharlayan, New to You"),  # 754
    (69895, "Hitting the Books"),  # 755
    (69896, "A Seat at the Last Stand"),  # 756
    (69897, "A Labyrinthine Descent"),  # 757
    (69898, "Glorified Ratcatcher"),  # 758
    (69899, "Deeper into the Maze"),  # 759
    (69900, "The Medial Circuit"),  # 760
    (69901, "The Full Report, Warts and All"),  # 761
    (69902, "A Guide of Sorts"),  # 762
    (69903, "Estate Visitor"),  # 763
    (69904, "For Thavnair Bound"),  # 764
    (69905, "On Low Tide"),  # 765
    (69906, "A Fisherman's Friend"),  # 766
    (69907, "House of Divinities"),  # 767
    (69908, "The Great Work"),  # 768
    (69909, "Shadowed Footsteps"),  # 769
    (69910, "A Boy's Errand"),  # 770
    (69911, "Tipping the Scale"),  # 771
    (69912, "The Satrap of Radz-at-Han"),  # 772
    (69913, "In the Dark of the Tower"),  # 773
    (69914, "The Jewel of Thavnair"),  # 774
    (69915, "The Color of Joy"),  # 775
    (69916, "Sound the Bell, School's In"),  # 776
    (69917, "A Capital Idea"),  # 777
    (69918, "Best of the Best"),  # 778
    (69919, "A Frosty Reception"),  # 779
    (69920, "Tracks in the Snow"),  # 780
    (69921, "How the Mighty Are Fallen"),  # 781
    (69922, "At the End of the Trail"),  # 782
    (69923, "A Way Forward"),  # 783
    (69924, "The Last Bastion"),  # 784
    (69925, "Personae non Gratae"),  # 785
    (69926, "His Park Materials"),  # 786
    (69927, "No Good Deed"),  # 787
    (69928, "Alea Iacta Est"),  # 788
    (69929, "Strange Bedfellows"),  # 789
    (69930, "In from the Cold"),  # 790
    (69931, "Gateway of the Gods"),  # 791
    (69932, "A Trip to the Moon"),  # 792
    (69933, "Sea of Sorrow"),  # 793
    (69934, "The Martyr"),  # 794
    (69935, "In Shadow's Wake"),  # 795
    (69936, "Helping Hands"),  # 796
    (69937, "A Harey Situation"),  # 797
    (69938, "A Taste of the Moon"),  # 798
    (69939, "Styled a Hero"),  # 799
    (69940, "All's Vale That Endsvale"),  # 800
    (69941, "Back to Old Tricks"),  # 801
    (69942, "Setting Things Straight"),  # 802
    (69943, "Heart of the Matter"),  # 803
    (69944, "Returning Home"),  # 804
    (69945, "Skies Aflame"),  # 805
    (69946, "The Blasphemy Unmasked"),  # 806
    (69947, "Amidst the Apocalypse"),  # 807
    (69948, "Beyond the Depths of Despair"),  # 808
    (69949, "That We Might Live"),  # 809
    (69950, "When All Hope Seems Lost"),  # 810
    (69951, "Warm Hearts, Rekindled Hopes"),  # 811
    (69952, "Simple Pleasures"),  # 812
    (69953, "Under His Wing"),  # 813
    (69954, "At World's End"),  # 814
    (69955, "Return to the Crystarium"),  # 815
    (69956, "Hope Upon a Flower"),  # 816
    (69957, "Petalouda Hunt"),  # 817
    (69958, "In Search of Hermes"),  # 818
    (69959, "Ponder, Warrant, Cherish, Welcome"),  # 819
    (69960, "Lives Apart"),  # 820
    (69961, "Their Greatest Contribution"),  # 821
    (69962, "Aether to Aether"),  # 822
    (69963, "A Sentimental Gift"),  # 823
    (69964, "Verdict and Execution"),  # 824
    (69965, "Travelers at the Crossroads"),  # 825
    (69966, "A Past, Not Yet Come to Pass"),  # 826
    (69967, "Witness to the Spectacle"),  # 827
    (69968, "Worthy of His Back"),  # 828
    (69969, "A Flower upon Your Return"),  # 829
    (69970, "Hunger in the Garden"),  # 830
    (69971, "Words without Sound"),  # 831
    (69972, "Follow, Wander, Stumble, Listen"),  # 832
    (69973, "Caging the Messenger"),  # 833
    (69974, "Thou Must Live, Die, and Know"),  # 834
    (69975, "As the Heavens Burn"),  # 835
    (69976, "Outside Help"),  # 836
    (69977, "Going Underground"),  # 837
    (69978, "No Job Too Small"),  # 838
    (69979, "Wise Guides"),  # 839
    (69980, "Agriculture Shock"),  # 840
    (69981, "Sage Council"),  # 841
    (69982, "Hither and Yarns"),  # 842
    (69983, "Once Forged"),  # 843
    (69984, "Bonds of Adamant(ite)"),  # 844
    (69985, "Her Children, One and All"),  # 845
    (69986, "A Bold Decision"),  # 846
    (69987, "Friends Gathered"),  # 847
    (69988, "Unto the Heavens"),  # 848
    (69989, "A §trαnge New World"),  # 849
    (69990, "On Burdεned ωings"),  # 850
    (69991, "Α Test of Wιll"),  # 851
    (69992, "Roads Pαved││Sacri┣ice"),  # 852
    (69993, "F//εsh AbanΔon┨Δ"),  # 853
    (69994, "Where Kn∞wledge Leads"),  # 854
    (69995, "Vic┨οry  ̈ ̈ ̈╳, │̆││ε Lost"),  # 855
    (69996, "┣┨̈//̈ No┨ΦounΔ•••"),  # 856
    (69997, "Hello, World"),  # 857
    (69998, "Forge Ahead"),  # 858
    (69999, "You're Not Alone"),  # 859
    (70000, "Endwalker"),  # 860
    (70062, "Newfound Adventure"),  # 861
    (70063, "Bountiful Ruins"),  # 862
    (70064, "Friends for the Road"),  # 863
    (70065, "Alzadaal's Legacy"),  # 864
    (70066, "A Brother's Grief"),  # 865
    (70067, "Sharing the Wealth"),  # 866
    (70068, "Bridging the Rift"),  # 867
    (70069, "Restricted Reading"),  # 868
    (70070, "Void Theory"),  # 869
    (70071, "A Satrap's Duty"),  # 870
    (70128, "In Search of Azdaja"),  # 871
    (70129, "Shadowed Remnants"),  # 872
    (70130, "Where Everything Begins"),  # 873
    (70131, "Groping in the Dark"),  # 874
    (70132, "Nowhere to Run"),  # 875
    (70133, "The Wind Rises"),  # 876
    (70134, "Return from the Void"),  # 877
    (70135, "A World with Light and Life"),  # 878
    (70136, "Buried Memory"),  # 879
    (70206, "Once More unto the Void"),  # 880
    (70207, "A Cold Reunion"),  # 881
    (70208, "Kindled Spirit"),  # 882
    (70209, "An Unforeseen Bargain"),  # 883
    (70210, "King of the Mountain"),  # 884
    (70211, "A Dragon's Resolve"),  # 885
    (70212, "Paths Barred"),  # 886
    (70213, "Desires Untold"),  # 887
    (70214, "Gods Revel, Lands Tremble"),  # 888
    (70271, "Currying Flavor"),  # 889
    (70272, "Going Haam"),  # 890
    (70273, "Like Fear to Flame"),  # 891
    (70274, "The Fallen Empire"),  # 892
    (70275, "Bonds of Trust"),  # 893
    (70276, "Lunar Rendezvous"),  # 894
    (70277, "The Red Side of the Moon"),  # 895
    (70278, "Abyssal Dark"),  # 896
    (70279, "The Dark Throne"),  # 897
    (70280, "Seeking the Light"),  # 898
    (70281, "Appealing to the Masses"),  # 899
    (70282, "In Defiance of Fate"),  # 900
    (70283, "Back to Action"),  # 901
    (70284, "Down in the Dark"),  # 902
    (70285, "Reunited at Last"),  # 903
    (70286, "Growing Light"),  # 904
    (70287, "When One Door Closes..."),  # 905
    (70288, "The Game Is Afoot"),  # 906
    (70289, "The Coming Dawn"),  # 907
    (70396, "A New World to Explore"),  # 908
    (70397, "The Nation of Tuliyollal"),  # 909
    (70398, "A City of Stairs"),  # 910
    (70399, "A Saga in Stone"),  # 911
    (70400, "The Rite of Succession"),  # 912
    (70401, "To Kozama'uka"),  # 913
    (70402, "A Festive People"),  # 914
    (70403, "The Feat of Reeds"),  # 915
    (70404, "A Well-mannered Shipwright"),  # 916
    (70405, "The Lifting of Wings"),  # 917
    (70406, "Knowing the Hanuhanu"),  # 918
    (70407, "To Urqopacha"),  # 919
    (70408, "Traders of Happiness"),  # 920
    (70409, "The Feat of Gold"),  # 921
    (70410, "Mablu's Dream"),  # 922
    (70411, "A Premium Deal"),  # 923
    (70412, "Wuk Lamat in the Saddle"),  # 924
    (70413, "Knowing the Pelupelu"),  # 925
    (70414, "The Success of Others"),  # 926
    (70415, "For All Turali"),  # 927
    (70416, "A Leaking Workpot"),  # 928
    (70417, "Lending a Helphand"),  # 929
    (70418, "The Feat of Pots"),  # 930
    (70419, "A Father First"),  # 931
    (70420, "The Shape of Peace"),  # 932
    (70421, "Lost Promise"),  # 933
    (70422, "A Brother's Duty"),  # 934
    (70423, "Feeding the River"),  # 935
    (70424, "Sibling Rescue"),  # 936
    (70425, "History's Keepers"),  # 937
    (70426, "The Feat of Proof"),  # 938
    (70427, "The High Luminary"),  # 939
    (70428, "An Echo of Madness"),  # 940
    (70429, "Pointing the Way"),  # 941
    (70430, "The Skyruin"),  # 942
    (70431, "The Feat of Ice"),  # 943
    (70432, "The Promise of Peace"),  # 944
    (70433, "The Leap to Yak T'el"),  # 945
    (70434, "Village of the Hunt"),  # 946
    (70435, "A History of Violence"),  # 947
    (70436, "The Feat of Repast"),  # 948
    (70437, "A Father's Grief"),  # 949
    (70438, "Taking a Stand"),  # 950
    (70439, "Into the Traverse"),  # 951
    (70440, "City of Silence"),  # 952
    (70441, "Blessed Siblings"),  # 953
    (70442, "Scale of Trust"),  # 954
    (70443, "Mamook Speaks"),  # 955
    (70444, "The Feat of the Brotherhood"),  # 956
    (70445, "Road to the Golden City"),  # 957
    (70446, "Dawn of a New Tomorrow"),  # 958
    (70447, "Ever Greater, Ever Brighter"),  # 959
    (70448, "The Long Road to Xak Tural"),  # 960
    (70449, "Saddled Up"),  # 961
    (70450, "Braced for Trouble"),  # 962
    (70451, "Blowing Smoke"),  # 963
    (70452, "Law of the Land"),  # 964
    (70453, "On Track"),  # 965
    (70454, "One with Nature"),  # 966
    (70455, "And the Land Would Tremble"),  # 967
    (70456, "No Time for Tears"),  # 968
    (70457, "Pick up the Pieces"),  # 969
    (70458, "Together as One"),  # 970
    (70459, "In Yyasulani's Shadow"),  # 971
    (70460, "Putting Plans into Locomotion"),  # 972
    (70461, "A Hot Commodity"),  # 973
    (70462, "All Aboard"),  # 974
    (70463, "The Land of Levin"),  # 975
    (70464, "A Royal Welcome"),  # 976
    (70465, "A Day in the Life"),  # 977
    (70466, "On the Cloud"),  # 978
    (70467, "Gone and Forgotten"),  # 979
    (70468, "Embracing Oblivion"),  # 980
    (70469, "Solution Nine"),  # 981
    (70470, "The Queen's Tour"),  # 982
    (70471, "Her People, Her Family"),  # 983
    (70472, "Scales of Blue"),  # 984
    (70473, "Gives You Teeth"),  # 985
    (70474, "Little Footfalls"),  # 986
    (70475, "Drowned Vestiges"),  # 987
    (70476, "Memories of a Knight"),  # 988
    (70477, "At a Crossroads"),  # 989
    (70478, "The Protector and the Destroyer"),  # 990
    (70479, "A Comforting Hand"),  # 991
    (70480, "Unto the Summit"),  # 992
    (70481, "The Resilient Son"),  # 993
    (70482, "A New Family"),  # 994
    (70483, "In Pursuit of Sphene"),  # 995
    (70484, "Through the Gate of Gold"),  # 996
    (70485, "Those Who Live Forever"),  # 997
    (70486, "In Serenity and Sorrow"),  # 998
    (70487, "The Land of Dreams"),  # 999
    (70488, "A Knight of Alexandria"),  # 1000
    (70489, "The Sanctuary of the Strong"),  # 1001
    (70490, "The Taste of Family"),  # 1002
    (70491, "Leafing through the Past"),  # 1003
    (70492, "An Explorer's Delight"),  # 1004
    (70493, "In Search of Discovery"),  # 1005
    (70494, "A Journey Never-ending"),  # 1006
    (70495, "Dawntrail"),  # 1007
    (70780, "A Royal Invitation"),  # 1008
    (70781, "Alexandria Mourns"),  # 1009
    (70782, "In Search of the Past"),  # 1010
    (70783, "Among the Abandoned"),  # 1011
    (70784, "Guidance of the Hhetso"),  # 1012
    (70785, "The Warmth of Family"),  # 1013
    (70786, "Crossroads"),  # 1014
    (70835, "A Glimmer of the Past"),  # 1015
    (70836, "Memories of a Bygone Age"),  # 1016
    (70837, "In Search of Meaning"),  # 1017
    (70838, "A Jewel Shattered"),  # 1018
    (70839, "The Meeting"),  # 1019
    (70840, "Descent to the Foundation"),  # 1020
    (70841, "Shared Paths"),  # 1021
    (70842, "Seekers of Eternity"),  # 1022
    (70900, "Targeted Tragedy"),  # 1023
    (70901, "The Endless Choice"),  # 1024
    (70902, "My Memories and Yours"),  # 1025
    (70903, "A Darkness in the Heart"),  # 1026
    (70904, "Preservation Their Purpose"),  # 1027
    (70905, "A Calculated Evolution"),  # 1028
    (70906, "One of Our Own"),  # 1029
    (70907, "A Terminal Invitation"),  # 1030
    (70908, "Blades in Waiting"),  # 1031
    (70909, "The Promise of Tomorrow"),  # 1032
    (70962, "With the Winds"),  # 1033
    (70963, "Through the Thunder"),  # 1034
    (70964, "Beyond the Mountains"),  # 1035
    (70965, "Around the City"),  # 1036
    (70966, "To Work"),  # 1037
    (70967, "In Her Heart"),  # 1038
    (70968, "Toward Trouble"),  # 1039
    (70969, "Where We Call Home"),  # 1040
    (70970, "Into the Mist"),  # 1041
]
# Total: 1041 trackable MSQ quests (ARR through Patch 7.4)

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
            venture_coins = 0
            
            def consume(items):
                nonlocal treasure_value, coffer_dye_value, coffer_count, dye_count, dye_pure_white, dye_jet_black, dye_pastel_pink
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
                        elif iid == 13115:  # Jet Black Dye
                            coffer_dye_value += qty * item_values.get("jet_black_dye", COFFER_DYE_VALUES[iid])
                            dye_count += qty
                            dye_jet_black += qty
                        elif iid == 13708:  # Pastel Pink Dye
                            coffer_dye_value += qty * item_values.get("pastel_pink_dye", COFFER_DYE_VALUES[iid])
                            dye_count += qty
                            dye_pastel_pink += qty
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
    total_venture_coins = 0
    total_fc_points = 0
    total_subs_leveling = 0
    total_subs_farming = 0
    total_retainers_leveling = 0
    total_retainers_farming = 0
    min_restock_days = None  # Track lowest restock days across all accounts (excluding 0)
    
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
            "total_venture_coins": 0,
            "total_fc_points": 0,
            "subs_leveling": 0,
            "subs_farming": 0,
            "retainers_leveling": 0,
            "retainers_farming": 0,
            "msq_100_count": 0,
            "msq_90_count": 0,
            "msq_50_count": 0,
            "characters_with_msq": 0,
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
            dye_pure_white = 0
            dye_jet_black = 0
            dye_pastel_pink = 0
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
            
            # Add ready counts and max levels to character data
            char_data["ready_subs"] = char_ready_subs
            char_data["total_subs"] = len(submarines)
            char_data["ready_retainers"] = char_ready_retainers
            char_data["total_retainers"] = len(retainers)
            char_data["max_retainer_level"] = max_retainer_level
            char_data["max_sub_level"] = max_sub_level
            
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
            # MSQ Progress stats
            "msq_100_count": msq_100_count,
            "msq_90_count": msq_90_count,
            "msq_50_count": msq_50_count,
            "characters_with_msq": total_characters_with_msq,
            "msq_avg_percent": round(total_msq_percent / total_characters_with_msq, 1) if total_characters_with_msq > 0 else 0,
            "msq_total_quests": len(MSQ_QUEST_DATA),
            "total_characters": sum(len(acc.get("characters", [])) for acc in all_accounts),
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
            border-color: var(--text-primary);
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
        }
        
        .account-header {
            background: linear-gradient(90deg, var(--bg-card) 0%, var(--accent) 100%);
            padding: 15px 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            user-select: none;
            transition: opacity 0.2s;
            position: sticky;
            top: 0;
            z-index: 100;
            border-radius: 12px 12px 0 0;
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
            margin-top: 5px;
            background: var(--bg-secondary);
            border-radius: 8px;
            align-items: center;
            position: sticky;
            top: 59px;
            z-index: 99;
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
            padding: 4px 8px;
            border-radius: 4px;
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
        
        .character-card.filtered-hidden {
            display: none;
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
        <div class="loading-text">⚓ FFXIV AutoRetainer Dashboard</div>
        <div class="loading-subtext">Loading {{ data.summary.total_characters }} characters across {{ data.accounts|length }} account(s)...</div>
        <div class="progress-container">
            <div class="progress-bar"></div>
        </div>
        <div class="loading-hint">This may take a few seconds for large character counts</div>
    </div>
    
    <div class="container">
        <header>
            <div class="header-content">
                <div class="header-left">
                    <h1>⚓ FFXIV AutoRetainer Dashboard</h1>
                    <div class="subtitle">Last Updated: <span id="last-updated">{{ data.last_updated }}</span> | Auto-refresh: {{ auto_refresh }}s</div>
                </div>
                <div class="header-right">
                    <div class="search-container">
                        <div class="search-error" id="search-error">No results match your search...</div>
                        <input type="text" class="search-input" id="character-search" placeholder="🔍 Search character..." oninput="searchCharacters(this.value)">
                        <div class="theme-selector">
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
                    </div>
                </div>
            </div>
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
                    <span>📜 <span class="acc-msq-100">{{ account.msq_100_count }}</span>/<span class="acc-msq-tracked">{{ account.characters_with_msq }}</span> MSQ</span>
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
                <button class="sort-btn" data-sort="retainers" data-order="desc" onclick="sortCharacters(this)" title="Retainers">👤 ▼</button>
                <button class="sort-btn" data-sort="retainer_level" data-order="desc" onclick="sortCharacters(this)" title="Retainer Level">👤 Lv ▼</button>
                <button class="sort-btn" data-sort="subs" data-order="desc" onclick="sortCharacters(this)" title="Submarines">🚢 ▼</button>
                <button class="sort-btn" data-sort="sub_level" data-order="desc" onclick="sortCharacters(this)" title="Submarine Level">🚢 Lv ▼</button>
                <button class="sort-btn" data-sort="msq_percent" data-order="asc" onclick="sortCharacters(this)" title="MSQ Progress (least to most)">📜 ▲</button>
                <span style="flex-grow: 1;"></span>
                <button class="filter-btn money-btn" onclick="toggleHideMoney(this)" title="Hide Money Stats">💰</button>
                <button class="filter-btn anon-btn" onclick="toggleAnonymize(this)" title="Anonymize">🔒</button>
                <button class="filter-btn" data-filter="personal-house" onclick="toggleFilter(this)" title="Show only characters with Personal House">🏠</button>
                <button class="filter-btn" data-filter="fc-house" onclick="toggleFilter(this)" title="Show only characters with FC House">🏨</button>
                <button class="filter-btn" data-filter="retainers" onclick="toggleFilter(this)" title="Show only characters with Retainers">👤</button>
                <button class="filter-btn" data-filter="subs" onclick="toggleFilter(this)" title="Show only characters with Submarines">🚢</button>
                <button class="filter-btn" data-filter="msq" onclick="toggleFilter(this)" title="Hide characters with 0% MSQ">📜</button>
                <button class="filter-btn" onclick="expandAllChars(this)" title="Expand All">▼</button>
                <button class="filter-btn" onclick="collapseAllChars(this)" title="Collapse All">▲</button>
            </div>
            {% endif %}
            
            <div class="account-content collapsed">
            {% if account.error %}
            <div class="error-message">{{ account.error }}</div>
            {% else %}
            <div class="character-grid">
                {% for char in account.characters %}
                <div class="character-card" data-char="{{ char.cid }}" data-level="{{ char.current_level }}" data-lowest-level="{{ char.lowest_level }}" data-highest-level="{{ char.highest_level }}" data-gil="{{ char.total_gil }}" data-treasure="{{ char.treasure_value }}" data-fc-points="{{ char.fc_points }}" data-venture-coins="{{ char.venture_coins }}" data-coffers="{{ char.coffer_count }}" data-dyes="{{ char.dye_count }}" data-tanks="{{ char.ceruleum }}" data-kits="{{ char.repair_kits }}" data-restock="{{ char.days_until_restock if char.days_until_restock is not none else 9999 }}" data-retainers="{{ char.ready_retainers }}" data-total-retainers="{{ char.total_retainers }}" data-subs="{{ char.ready_subs }}" data-total-subs="{{ char.total_subs }}" data-inventory="{{ 140 - char.inventory_space }}" data-has-personal-house="{{ 'true' if char.private_house else 'false' }}" data-has-fc-house="{{ 'true' if char.fc_house else 'false' }}" data-retainer-level="{{ char.max_retainer_level }}" data-sub-level="{{ char.max_sub_level }}" data-msq-percent="{{ char.msq_percent }}">
                    <div class="character-header collapsed {% if char.ready_retainers > 0 or char.ready_subs > 0 %}has-available{% endif %}" onclick="toggleCharacter(this)">
                        <div class="char-header-row name-row">
                            <span class="character-name">{{ char.name }}{% if char.current_level > 0 %} <span style="font-size: 0.8em; color: var(--text-secondary);">(Lv {{ char.current_level }}, {{ char.current_job }})</span>{% endif %}{% if char.msq_completed >= min_msq_quests %} <span style="font-size: 0.8em; {% if char.msq_percent >= 90 %}color: #4ade80;{% elif char.msq_percent >= 50 %}color: #fbbf24;{% else %}color: #94a3b8;{% endif %}" title="MSQ Progress: {{ char.msq_completed }}/{{ char.msq_total }}{% if char.msq_quest_name %} - {{ char.msq_quest_name }}{% endif %}">MSQ: {{ char.msq_percent }}%</span>{% endif %}{% if char.private_house %} <span style="font-size: 0.8em;" title="Personal House: {{ char.private_house }}">🏠</span>{% endif %}{% if char.fc_house %} <span style="font-size: 0.8em;" title="FC House: {{ char.fc_house }}">🏨</span>{% endif %}</span>
                            <span class="char-status {% if char.ready_retainers > 0 %}available{% else %}all-sent{% endif %}">👤 {{ char.ready_retainers }}/{{ char.total_retainers }}</span>
                        </div>
                        <div class="char-header-row">
                            <span class="character-world">{{ char.world }}{% if char.fc_name %} • {{ char.fc_name }}{% endif %} • 🎒 {{ 140 - char.inventory_space }}/140</span>
                            <span class="char-status {% if char.ready_subs > 0 %}available{% else %}all-sent{% endif %}">🚢 {{ char.ready_subs }}/{{ char.total_subs }}</span>
                        </div>
                        <div class="char-header-row">
                            <span style="font-size: 0.8em; color: var(--text-secondary);">🪙 {{ "{:,}".format(char.fc_points) }} | 🛒 {{ char.venture_coins }} | 📦 {{ char.coffer_count }} | 🎨 {{ char.dye_count }}{% if char.dye_count > 0 %} 🤍{{ char.dye_pure_white }} 🖤{{ char.dye_jet_black }} 🩷{{ char.dye_pastel_pink }}{% endif %}</span>
                            <span class="character-gil">{{ "{:,}".format(char.total_gil) }} gil</span>
                        </div>
                        <div class="char-header-row">
                            <span style="font-size: 0.8em; color: var(--text-secondary);">⛽ {{ "{:,}".format(char.ceruleum) }} | 🔧 {{ "{:,}".format(char.repair_kits) }}{% if char.total_subs > 0 %} | <span style="{% if char.days_until_restock is not none and char.days_until_restock < 7 %}color: var(--danger);{% elif char.days_until_restock is not none and char.days_until_restock < 14 %}color: var(--warning);{% endif %}">🔄 {% if char.days_until_restock is not none %}{{ char.days_until_restock }}d{% else %}N/A{% endif %}</span>{% endif %}</span>
                            {% if char.total_subs > 0 %}<span style="font-size: 0.8em; color: var(--gold);">💎 {{ "{:,}".format(char.treasure_value) }}</span>{% endif %}
                        </div>
                    </div>
                    <div class="character-body collapsed">
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
                        {% if char.msq_completed >= min_msq_quests %}
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
                                    <td class="{% if ret.venture_formatted == 'Ready!' %}status-ready{% else %}status-voyaging{% endif %}">
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
            FFXIV AutoRetainer Dashboard v1.15 | Data sourced from AutoRetainer, Lifestream, & Altoholic<br>
            <a href="https://github.com/xa-io/ffxiv-tools/tree/main/FFXIV-AutoRetainer-Dashboard" target="_blank" style="color: var(--accent); text-decoration: none;">github.com/xa-io/ffxiv-tools</a>
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
                'retainers': 'retainers',
                'retainer_level': 'retainer-level',
                'subs': 'subs',
                'sub_level': 'sub-level',
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
        }
        
        function anonymizeAll() {
            // Anonymize account headers
            document.querySelectorAll('.account-section').forEach((section, accIndex) => {
                const header = section.querySelector('.account-header h2');
                if (header && !originalData.has(header)) {
                    originalData.set(header, header.textContent);
                }
                header.textContent = 'Account ' + (accIndex + 1);
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
                    const inventoryMatch = worldFC.textContent.match(/🎒 (\d+\/\d+)/);
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
        }
        
        function restoreAll() {
            originalData.forEach((value, element) => {
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
            
            // Hide summary cards (top section)
            const summarySelectors = [
                '#sum-total-gil', '#sum-treasure', '#sum-with-treasure', '#sum-coffer-dye',
                '#sum-ready-subs', '#sum-total-subs', '#sum-ready-retainers', '#sum-total-retainers',
                '#sum-total-mb', '#sum-max-mb', '#sum-monthly-income', '#sum-monthly-cost',
                '#sum-monthly-profit', '#sum-annual-income'
            ];
            summarySelectors.forEach(sel => {
                const el = document.querySelector(sel);
                if (el && (forceRefresh || !originalMoneyData.has(el))) {
                    if (!forceRefresh) originalMoneyData.set(el, el.textContent);
                    el.textContent = HIDDEN;
                }
            });
            
            // Hide FC Points sublabel and restock days sublabel in summary cards
            document.querySelectorAll('.summary-card .sublabel').forEach(el => {
                if (el.textContent.includes('FC') || el.textContent.includes('📦') || el.textContent.includes('🎨') || el.textContent.includes('lowest')) {
                    if (forceRefresh || !originalMoneyData.has(el)) {
                        if (!forceRefresh) originalMoneyData.set(el, { html: el.innerHTML });
                        el.innerHTML = HIDDEN;
                    }
                }
            });
            
            // Hide leveling/farming stats in summary cards
            document.querySelectorAll('.summary-card .value div').forEach(el => {
                if (el.textContent.includes('Lvl:') || el.textContent.includes('Farm:')) {
                    if (forceRefresh || !originalMoneyData.has(el)) {
                        if (!forceRefresh) originalMoneyData.set(el, { html: el.innerHTML });
                        el.innerHTML = HIDDEN;
                    }
                }
            });
            
            // Hide account tab stats
            document.querySelectorAll('.account-stats span').forEach(el => {
                const text = el.textContent;
                if (text.includes('💰') || text.includes('💎') || text.includes('🚢') || 
                    text.includes('👤') || text.includes('📦')) {
                    if (forceRefresh || !originalMoneyData.has(el)) {
                        if (!forceRefresh) originalMoneyData.set(el, { html: el.innerHTML });
                        // Keep emoji, hide values
                        const emoji = text.match(/^[^\d]*/)[0].trim();
                        el.innerHTML = emoji + ' ' + HIDDEN;
                    }
                }
            });
            
            // Hide character card header stats
            document.querySelectorAll('.character-card').forEach(card => {
                // Character gil (in header)
                const gilEl = card.querySelector('.character-gil');
                if (gilEl && (forceRefresh || !originalMoneyData.has(gilEl))) {
                    if (!forceRefresh) originalMoneyData.set(gilEl, gilEl.textContent);
                    gilEl.textContent = HIDDEN + ' gil';
                }
                
                // Treasure value in header
                card.querySelectorAll('.char-header-row span').forEach(span => {
                    const text = span.textContent;
                    if (span.style.color && span.style.color.includes('gold') && text.includes('💎')) {
                        if (forceRefresh || !originalMoneyData.has(span)) {
                            if (!forceRefresh) originalMoneyData.set(span, { html: span.innerHTML });
                            span.innerHTML = '💎 ' + HIDDEN;
                        }
                    }
                    // FC points, venture coins, coffers, dyes row (including individual dye counts)
                    if (text.includes('🪙') && text.includes('🛒') && text.includes('📦') && text.includes('🎨')) {
                        if (forceRefresh || !originalMoneyData.has(span)) {
                            if (!forceRefresh) originalMoneyData.set(span, { html: span.innerHTML });
                            // Check if individual dyes are shown (🤍🖤🩷)
                            const hasIndividualDyes = text.includes('🤍') || text.includes('🖤') || text.includes('🩷');
                            if (hasIndividualDyes) {
                                span.innerHTML = '🪙 ' + HIDDEN + ' | 🛒 ' + HIDDEN + ' | 📦 ' + HIDDEN + ' | 🎨 ' + HIDDEN + ' 🤍' + HIDDEN + ' 🖤' + HIDDEN + ' 🩷' + HIDDEN;
                            } else {
                                span.innerHTML = '🪙 ' + HIDDEN + ' | 🛒 ' + HIDDEN + ' | 📦 ' + HIDDEN + ' | 🎨 ' + HIDDEN;
                            }
                        }
                    }
                    // Tanks, kits, restock row
                    if (text.includes('⛽') && text.includes('🔧')) {
                        if (forceRefresh || !originalMoneyData.has(span)) {
                            if (!forceRefresh) originalMoneyData.set(span, { html: span.innerHTML });
                            span.innerHTML = '⛽ ' + HIDDEN + ' | 🔧 ' + HIDDEN + (text.includes('🔄') ? ' | 🔄 ' + HIDDEN : '');
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
    return render_template_string(HTML_TEMPLATE, data=data, auto_refresh=AUTO_REFRESH, 
                                  job_categories=JOB_CATEGORIES, job_display_names=JOB_DISPLAY_NAMES,
                                  job_base_class=JOB_BASE_CLASS, min_msq_quests=MINIMUM_MSQ_QUESTS,
                                  show_classes=SHOW_CLASSES, show_currencies=SHOW_CURRENCIES,
                                  default_theme=DEFAULT_THEME)


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
    print("  FFXIV AutoRetainer Dashboard v1.15")
    print("=" * 60)
    print(f"  Server: http://{HOST}:{PORT}")
    print(f"  Accounts: {len(account_locations)}")
    print(f"  Auto-refresh: {AUTO_REFRESH}s" if AUTO_REFRESH > 0 else "  Auto-refresh: Disabled")
    print("=" * 60)
    print()
    
    app.run(host=HOST, port=PORT, debug=DEBUG)
