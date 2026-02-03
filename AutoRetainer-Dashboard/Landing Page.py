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
# Landing Page v1.25
# AutoRetainer Dashboard
# Created by: https://github.com/xa-io
# Last Updated: 2026-02-03 09:54:00
#
# ## Release Notes ##
#
# v1.25 - Bug fixes and filter improvements:
#         Brown MSQ highlight only shows when SHOW_MSQ_PROGRESSION is enabled
#         ❓ filter includes characters without FC and with potential retainer alerts
#         🏁 Ready filter excludes disabled/excluded retainers and submarines
#         Added explanations in expanded dropdowns for any marked character
#         Added ⌛ Idle filter button to show only characters with idle retainers/subs
#         ⌛ button only appears when idle count > 0
#         ✅ shows characters actively processing retainers/subs (regardless of exclusion settings)
#         Player Stats now collapsed by default, ✏️ button shows instead of hides
#         Fixed idle detection: now requires Enabled=true (excluded chars don't count as idle)
#         Non-expanded cards no longer stretch vertically when others in same row are expanded
# v1.24 - Added HONOR_AR_EXCLUSIONS config option:
#         When enabled, respects AutoRetainer's ExcludeRetainer and ExcludeWorkshop settings
#         ExcludeRetainer: Hides retainers for that character (but shows submarines)
#         ExcludeWorkshop: Hides submarines for that character (but shows retainers)
#         Useful for ensuring dashboard accurately reflects AR automation settings
# v1.23 - Added highlight toggle configuration options:
#         HIGHLIGHT_POTENTIAL_RETAINER: Toggle brown outline for chars with MSQ 66060 done but 0 retainers
#         Added version number in display options
# v1.22 - Added highlight toggle configuration options:
#         HIGHLIGHT_IDLE_RETAINERS: Toggle cyan outline for idle retainers (default: true)
#         HIGHLIGHT_IDLE_SUBS: Toggle pink outline for idle submarines (default: true)
#         HIGHLIGHT_READY_ITEMS: Toggle red background for ready items (default: true)
#         HIGHLIGHT_MAX_MB: Toggle gold outline for max MB listings (default: true)
#         When all false, character boxes display in theme color with no highlighting
# v1.21 - Fixed javascript regex syntax issue
# v1.20 - Major UI/UX enhancement release
#         STICKY HEADER & GLOBAL CONTROLS:
#         • Sticky header with summary cards fixed at top when scrolling
#         • Global filter buttons in header: hide money, anonymize, houses, retainers, subs, MSQ
#         • Expand/collapse all accounts button (▶/▼) for quick navigation
#         • Mass hide buttons: ✏️ Player Stats, 🐋 Submarines, 🛎️ Retainers, 📖 Classes, 🪶 Currencies
#         NEW SUMMARY CARDS & TRACKING:
#         • Characters summary card showing total chars, Lv 25+, Lv 100, personal/FC plots
#         • Consolidated summary cards (Treasure shows combined total, Annual Income shows profit)
#         • Max MB listings indicator with gold outline highlight
#         • Idle retainer tracking with cyan highlight, idle submarine tracking with pink highlight
#         ENHANCED FILTERING:
#         • Region filter buttons (NA, EU, JP, OCE) to filter by data center region
#         • New filter buttons: 📦 Coffers, 🎨 Dyes, 💎 Treasure, 🪧 MB items
#         • Changed MB icon from 📦 to 🪧 (placard) for clarity
#         UI IMPROVEMENTS:
#         • Collapsible Player Stats section (📊) with comprehensive character data
#         • "None" in Venture/Plan columns shows bold for visibility
#         • Fixed rounded corners on account tabs (collapsed and sticky states)
#         • Hide Money mode preserves labels with asterisks for privacy screenshots
#         CONFIG ENHANCEMENTS:
#         • Custom build gil rates and consumption rates via config.json
#         • Supply cost overrides (ceruleum_tank_cost, repair_kit_cost)
#         • SHOW_MSQ_PROGRESSION toggle (disabled until Altoholic tracking fixed)
#         BUG FIXES:
#         • Fixed plot counting to avoid duplicates from shared houses
#         • Fixed dye/coffer scanning to include retainer MarketInventory
#         • Fixed anonymize toggle with proper error handling
# v1.15 - Added 10 color theme presets with theme selector buttons under search bar
#         Themes: Default (Blue), Ultra Dark, Dark Gray, Ocean Blue, Forest Green,
#                 Crimson Red, Purple Haze, Pastel Pink, Dark Orange, Brown
#         DEFAULT_THEME config option in script and config.json
# v1.14 - Added character search bar in header (filters characters by name across all accounts)
#         Added loading overlay with animated progress bar for large character counts
#         Added anchor emoji favicon for browser tab
# v1.13 - Fixed Current Class to show last played job (using LastJob/LastJobLevel from Altoholic)
#         Added Lowest/Highest Class fields, "Classes" sort button, individual dye counts
# v1.12 - Added Hide Money Stats button to privatize earnings for screenshots
# v1.11 - Improved Currencies display with categories and shortened names
# v1.10 - Added MSQ progression percentage display with color coding
# v1.09 - Added Player Name@World, DoW/DoM, DoH/DoL, and Currencies collapsible sections
# v1.08 - Added housing filters, level sorting, anonymization improvements
# v1.07 - Added Housing information from Lifestream DefaultConfig.json
# v1.06 - Added Inventory Space tracking with color coding
# v1.05 - Added Anonymize mode and Expand/Collapse All buttons
# v1.04 - Added character filtering (hide no retainers/submarines)
# v1.03 - Major Altoholic integration: submarine plans, FC Points, Coffers, class/level display
# v1.02 - UI color refinements: blue account headers, red highlights for ready items
# v1.01 - Fixed stale submarine display bug
# v1.00 - Initial release with Flask web server, AutoRetainer parsing, dark-themed UI
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
VERSION = "v1.25"       # Version number shown in footer and startup
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
                        <h1>⚓ AutoRetainer Dashboard</h1>
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
    print(f"  AutoRetainer Dashboard {VERSION}")
    print("=" * 60)
    print(f"  Server: http://{HOST}:{PORT}")
    print(f"  Accounts: {len(account_locations)}")
    print(f"  Auto-refresh: {AUTO_REFRESH}s" if AUTO_REFRESH > 0 else "  Auto-refresh: Disabled")
    print("=" * 60)
    print()
    
    app.run(host=HOST, port=PORT, debug=DEBUG)
