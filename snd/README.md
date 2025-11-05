# FFXIV SomethingNeedDoing Tools

A comprehensive collection of automation scripts and function libraries for Final Fantasy XIV using the SomethingNeedDoing (SND) plugin. This repository provides robust tools for multi-character management, resource distribution, crafting automation, and various quality-of-life improvements.

Created by: [https://github.com/xa-io](https://github.com/xa-io)

---

## ⚠️ Important Disclaimer

**USE AT YOUR OWN RISK.** These scripts automate gameplay actions in Final Fantasy XIV and may violate the game's Terms of Service. The author is not responsible for any consequences including account suspension or ban. Use discretion and understand the risks before implementing these tools.

---

## 📋 Table of Contents

- [Required Plugins](#required-plugins)
- [Function Libraries](#function-libraries)
- [Main Automation Scripts](#main-automation-scripts)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Script Pairing & Workflows](#script-pairing--workflows)
- [Troubleshooting](#troubleshooting)

---

## 🔌 Required Plugins

All scripts require [FFXIVQuickLauncher/Dalamud](https://github.com/goatcorp/FFXIVQuickLauncher) with the following plugins:

### Core Dependencies
- **SomethingNeedDoing** - Script execution engine
- **vnavmesh** - Navigation and pathfinding
- **Lifestream** - World/datacenter travel automation
- **AutoRetainer** - Retainer management
- **Dropbox** - Player-to-player trading automation
- **TextAdvance** - Automatic dialogue progression
- **YesAlready** - Automatic confirmation dialogs

### Recommended Plugins
- **SimpleTweaks** - UI and QoL improvements
- **Artisan** - Crafting automation
- **BossMod Reborn** - Combat mechanics assistance
- **Rotation Solver Reborn** - Combat rotation automation
- **Questionable** - Quest automation

---

## 📚 Function Libraries

### xafunc.lua
**XA Function Library** - Comprehensive helper functions extending dfunc with additional automation utilities.

- **GitHub:** [https://github.com/xa-io/ffxiv-tools/blob/main/snd/xafunc.lua](https://github.com/xa-io/ffxiv-tools/blob/main/snd/xafunc.lua)
- **Version:** v2.0
- **Dependencies:** dfunc.lua

**Key Features:**
- Enhanced movement and navigation functions
- UI interaction utilities (Dropbox, Armoury Chest, etc.)
- Player management (targeting, focus, relogging)
- World interaction and teleportation
- Plugin integration (AutoRetainer, Artisan, Lifestream)
- Free Company management utilities
- Coordinate extraction and zone detection

**Setup:**
```lua
require("dfunc")
require("xafunc")
```

### dfunc.lua
**D's Function Library** - Base automation framework (external dependency)

- **GitHub:** [https://github.com/McVaxius/dhogsbreakfeast/blob/main/dfunc.lua](https://github.com/McVaxius/dhogsbreakfeast/blob/main/dfunc.lua)
- **Required by:** All scripts in this repository

---

## 🤖 Main Automation Scripts

### Resource Management

#### XA Inverse Bagman v2.0
Multi-character inventory threshold checker for automated submarine operations and resource distribution.

**Key Features:**
- Multi-character threshold monitoring with automatic login rotation
- Comprehensive submarine resource tracking (fuel, repair materials, parts, gil)
- Real-time inventory status reporting with ✓/✗ indicators
- Configurable thresholds for all tracked resources
- Safe character switching with proper wait states
- Homeworld return after threshold completion

**Companion Script:** XA Inverse Supplier v2.0

**Configuration Requirements:**
- Synchronize franchise_owners list with Inverse Supplier
- Configure item thresholds for all tracked resources
- Set supplier location coordinates (tony_x, tony_y, tony_z)
- Enable Dropbox Auto-Trading and Lifestream Paths

#### XA Inverse Supplier v2.0
Automated supplier script that distributes resources to franchise owners via dropbox trading.

**Key Features:**
- Automated nearby player scanning with configurable distance thresholds
- Franchise owner detection from synchronized character list
- Automatic dropbox trading using Bagman Type 69 methodology
- Resource threshold-based distribution system
- Trade completion tracking with visual status indicators
- Distance-based movement to approach franchise owners

**Companion Script:** XA Inverse Bagman v2.0

**Configuration Requirements:**
- Synchronize franchise_owners list with Inverse Bagman
- Match item thresholds and item IDs with Bagman
- Be logged into supplier character before starting

#### XA Bagman Type 69
Advanced multi-character resource distribution and inventory management system.

**Key Features:**
- Dropbox trading methodology for automated item distribution
- Multi-character queue management
- Threshold-based resource allocation
- Configurable item tracking and distribution rules

### Crafting Automation

#### XA Lazy Crafter v7.35.1
Automated FFXIV crafting leveling script for unlocking blacksmith and reaching level 25.

**Key Features:**
- Automatic teleportation to Limsa Lominsa Lower Decks and zone verification
- Gil and Fire Shards inventory checking with Tony trading integration
- Multi-vendor material purchasing (Engerrand, Sorcha, Iron Thunder, Syneyhil, Smydhaemr)
- Blacksmith Guild quest completion and class unlocking automation
- Two-stage crafting progression (levels 1-12 and 12-25) with Artisan integration
- Multi-position support for running up to 3 characters simultaneously
- Automatic gear changes and inventory management at level milestones
- Grand Company navigation and item discarding upon completion

**Requirements:**
- Armoury system unlocked
- Access to Limsa Lominsa
- Pre-configured Artisan crafting lists
- Specific YesAlready configurations for vendor interactions
- No prior BSM quest progress

### Utility Scripts

#### XA Monthly Relogger
Automated character login rotation for maintaining subscription status and retainer access.

**Key Features:**
- Scheduled character rotation
- AutoRetainer integration
- Configurable login intervals
- Multi-character support

---

## 🔧 Installation & Setup

### Method 1: Manual Script Addition

1. **Install dfunc.lua:**
   - Open SomethingNeedDoing
   - Click "Add Script"
   - Name: `dfunc`
   - Paste code from: [https://github.com/McVaxius/dhogsbreakfeast/blob/main/dfunc.lua](https://github.com/McVaxius/dhogsbreakfeast/blob/main/dfunc.lua)
   - Save

2. **Install xafunc.lua:**
   - Open SomethingNeedDoing
   - Click "Add Script"
   - Name: `xafunc`
   - Paste code from: [https://github.com/xa-io/ffxiv-tools/blob/main/snd/xafunc.lua](https://github.com/xa-io/ffxiv-tools/blob/main/snd/xafunc.lua)
   - Save

3. **Install Automation Scripts:**
   - Copy desired script content
   - Create new SND script with descriptive name
   - Paste script code
   - Save

### Method 2: GitHub Auto-Update (Recommended)

1. **Install dfunc.lua:**
   - Open SomethingNeedDoing
   - Click "Add Script"
   - Name: `dfunc`
   - Add GitHub URL: `https://github.com/McVaxius/dhogsbreakfeast/blob/main/dfunc.lua`
   - Save
   - Scripts will auto-update when GitHub repository changes

2. **Install xafunc.lua:**
   - Open SomethingNeedDoing
   - Click "Add Script"
   - Name: `xafunc`
   - Add GitHub URL: `https://github.com/xa-io/ffxiv-tools/blob/main/snd/xafunc.lua`
   - Save

3. **Install Automation Scripts:**
   - Add script with GitHub URL (if available)
   - Or manually add script content

### Required Plugin Configuration

#### YesAlready
Configure automatic confirmations for:
- Vendor purchases ("Nothing")
- Quest acceptances
- Teleport confirmations
- FC creation dialogs

#### SimpleTweaks
Enable recommended settings:
- FixTarget
- DisableTitleScreen
- Auto-advance dialogue options

#### Dropbox
- Enable Auto-Trading
- Configure trade acceptance settings
- Set appropriate distance thresholds

#### Lifestream
- Configure world/datacenter preferences
- Enable auto-navigation
- Set teleport retry attempts
- Set pathing to door for plot location

---

## ⚙️ Configuration

### General Script Structure

All scripts follow this initialization pattern:

```lua
-- DO NOT TOUCH THESE LINES BELOW
require("dfunc")
require("xafunc")
DisableARMultiXA()
rsrXA("off")
-- DO NOT TOUCH THESE LINES ABOVE

-- ---------------------------------------
-- -- Start of Configuration Parameters --
-- ---------------------------------------

-- [Your configuration here]
```

### Common Configuration Parameters

#### Character Lists
```lua
local franchise_owners = {
    {"Character One@World"},
    {"Character Two@World"},
    {"Character Three@World"}
    -- Last entry should NOT have comma
}
```

#### Item Thresholds (Inverse Bagman/Supplier)
```lua
local gil_threshold = 50000
local miniature_aetheryte_count = 10
local darksteel_nugget_count = 5
local growth_formula_gamma_count = 5
-- ... additional thresholds
```

#### Location Coordinates
```lua
-- Use GetInverseBagmanCoordsXA() from xafunc to get coordinates
local tony_x = 238.8885345459
local tony_y = 112.70601654053
local tony_z = -254.736328125
local TonyTurf = "Golem"
local TonySpot = "Summerford Farms"
local TonyZoneID = 134  -- Use GetZoneIDXA() from xafunc
```

### Getting Coordinates and Zone IDs

Use these xafunc functions for configuration:

```lua
-- Get coordinates for Inverse Bagman
GetInverseBagmanCoordsXA()

-- Get current zone ID
GetZoneIDXA()

-- Get general coordinates
GetSNDCoordsXA()
```

---

## 🔗 Script Pairing & Workflows

### Inverse Bagman + Inverse Supplier Workflow

**Purpose:** Automated multi-character resource distribution for submarine operations

**Setup:**
1. Configure **identical** franchise_owners lists in both scripts
2. Synchronize item thresholds and item IDs between scripts
3. Set supplier location coordinates in Bagman
4. Run Inverse Supplier on supplier character
5. Run Inverse Bagman on receiving characters

**Workflow:**
1. Supplier detects nearby franchise owners
2. Supplier opens dropbox and distributes configured resources
3. Bagman monitors inventory thresholds
4. Bagman waits until all thresholds are met
5. Bagman returns to homeworld and switches to next character
6. Process repeats for all characters in franchise_owners list

### Lazy Crafter Workflow

**Purpose:** Level fresh characters to BSM 25 for FC creation

**Setup:**
1. Ensure character has NOT started BSM quest line
2. Configure YesAlready for vendor "Nothing" responses
3. Prepare Artisan crafting lists (levels 1-12 and 12-25)
4. Ensure access to Limsa Lominsa
5. Configure multi-position if running multiple characters

**Workflow:**
1. Script teleports to Limsa Lominsa Lower Decks
2. Checks gil and Fire Shards inventory
3. Purchases materials from multiple vendors
4. Unlocks Blacksmith class and completes initial quest
5. Crafts items for levels 1-12 using Artisan
6. Changes gear and crafts items for levels 12-25
7. Navigates to Grand Company and discards items
8. Character ready for FC creation

---

## 🔍 Troubleshooting

### Common Issues

#### "Script failed to load dfunc/xafunc"
- Ensure dfunc and xafunc are installed in SomethingNeedDoing
- Check script names are exactly `dfunc` and `xafunc`
- Verify require statements at top of script

#### "Character stuck or not moving"
- Check vnavmesh is installed and enabled
- Verify navigation mesh is loaded for current zone
- Restart vnavmesh plugin
- Check for obstacles blocking pathing

#### "Trade not completing"
- Verify Dropbox plugin is installed and enabled
- Check Auto-Trading is enabled in Dropbox settings
- Ensure both characters are within trade range

#### "Lifestream not working"
- Check Lifestream plugin is enabled
- Verify character has teleport access to destination
- Ensure sufficient gil for teleport costs
- Check WaitForLifestreamXA() is called after travel commands

#### "Character won't relog"
- Verify AutoRetainer is installed and enabled
- Check character name format: "Character@World"
- Ensure AutoRetainer has character configured
- Check for pending retainer tasks blocking relog

### Debug Mode

Most scripts include debug logging. Enable with:

```lua
local debug_mode = true
```

Debug output shows:
- Function entry/exit points
- Variable states and values
- API call results
- Conditional branch decisions

---

**Last Updated:** 2025-11-05

**Repository:** [https://github.com/xa-io/ffxiv-tools](https://github.com/xa-io/ffxiv-tools)
