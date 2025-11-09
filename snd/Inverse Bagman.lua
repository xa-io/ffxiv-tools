-- ┌-----------------------------------------------------------------------------------------------------------------------
-- | 
-- |   ██╗  ██╗ █████╗     ██╗███╗   ██╗██╗   ██╗███████╗██████╗ ███████╗███████╗    ██████╗  █████╗  ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗
-- |   ╚██╗██╔╝██╔══██╗    ██║████╗  ██║██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔══██╗██╔══██╗██╔════╝ ████╗ ████║██╔══██╗████╗  ██║
-- |    ╚███╔╝ ███████║    ██║██╔██╗ ██║██║   ██║█████╗  ██████╔╝███████╗█████╗      ██████╔╝███████║██║  ███╗██╔████╔██║███████║██╔██╗ ██║
-- |    ██╔██╗ ██╔══██║    ██║██║╚██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝      ██╔══██╗██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║
-- |   ██╔╝ ██╗██║  ██║    ██║██║ ╚████║ ╚████╔╝ ███████╗██║  ██║███████║███████╗    ██████╔╝██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║
-- |   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
-- |                                                                                                                                            
-- |  Mass toon inventory threshold checker for automated submarine operations and resource distribution.
-- | 
-- |  This script cycles through multiple characters and waits until all inventory thresholds are met before moving to the
-- |  next character. Perfect for automated trading and resource distribution where you need to ensure each character receives
-- |  specific items before continuing to the next one in the sequence.
-- | 
-- |  Core Features:
-- |  • Multi-character threshold monitoring with automatic login rotation
-- |  • Comprehensive submarine resource tracking (fuel, repair materials, parts, gil, etc.)
-- |  • Real-time inventory status reporting with ✓/✗ indicators
-- |  • Configurable thresholds for all tracked resources
-- |  • Automated waiting until all thresholds are satisfied
-- |  • Safe character switching with proper wait states
-- |  • Custom pathing integration for supplier interaction
-- |  • Homeworld return after successful threshold completion using Lifesteam auto
-- | 
-- |  Important Note: This script requires dfunc.lua and xafunc.lua dependencies. These must be configured in SomethingNeedDoing
-- |  before running. The script will move characters to a supplier location and wait for inventory thresholds to be met before
-- |  proceeding to the next character. Works in tandem with XA Inverse Supplier for automated resource distribution.
-- | 
-- |  Important Steps: Enable Dropbox Auto-Trading, Lifesteam Paths
-- | 
-- |  XA Inverse Bagman v2.0
-- |  Mass toon inventory threshold checker for submarine operations
-- |  Created by: https://github.com/xa-io
-- |  Last Updated: 2025-11-5 13:20:00
-- | 
-- |  ## Release Notes ##
-- | 
-- |  v2.0
-- |    - Enhanced multi-character submarine resource management
-- |    - Comprehensive threshold checking for different resources
-- |    - Automated supplier pathing with custom location configuration
-- |    - Real-time status reporting with visual indicators
-- |    - Safe character switching with proper wait states
-- |    - Homeworld return functionality after threshold completion
-- | 
-- |  ## Dependencies ##
-- | 
-- |  Requires dfunc.lua: https://github.com/McVaxius/dhogsbreakfeast/blob/main/dfunc.lua
-- |  Requires xafunc.lua: https://github.com/xa-io/ffxiv-tools/blob/main/snd/xafunc.lua
-- | 
-- |  Setup Process:
-- |  1. SND > Add Script > Name: dfunc > Paste code from dfunc.lua URL
-- |  2. SND > Add Script > Name: xafunc > Paste code from xafunc.lua URL
-- |  3. Alternative: SND > Add Script > Name: dfunc/xafunc > Add GitHub URL > Save (enables auto-update)
-- | 
-- |  ## Companion Script ##
-- | 
-- |  Works with: XA Inverse Supplier v2.0
-- |  Configuration: Synchronize toon_list and item thresholds between both scripts
-- └-----------------------------------------------------------------------------------------------------------------------

-- DO NOT TOUCH THESE LINES BELOW
require("dfunc")
require("xafunc")
DisableARMultiXA()
rsrXA("off")
if not CheckPluginEnabledXA({"Dropbox", "Lifestream", "vnavmesh", "AutoRetainer", "PandorasBox", "TextAdvance"}) then return end
-- DO NOT TOUCH THESE LINES ABOVE

-- ---------------------------------------
-- -- Start of Configuration Parameters --
-- ---------------------------------------

debug_mode = false
tradedebug_mode = true
listdebug_mode = false

-- Tony's coordinates (set this manually so the alt runs to a set location)
-- Use GetInverseBagmanCoordsXA() from xafunc to get this. Required if changing TonySpot
local tony_x = 238.8885345459
local tony_y = 112.70601654053
local tony_z = -254.736328125
-- No auto pathing is setup within Inverse Bagman, so you cannot use 42069420 from Bagman type 69
-- This was done specifically because you'll likely have different supplier toons

-- ----------------------------------------------
-- Share the below lines with Inverse Supplier --
-- ----------------------------------------------

-- Where is the supplier location
local TonyTurf = "Golem"
local TonySpot = "Summerford Farms" -- Use the Aetheryte Name for this
local TonyZoneID = 134 -- Use GetZoneIDXA() from xafunc to get this

-- Toon list (last toon should not have a comma at the end)
local toon_list = {
    {"Toon One@World"},
    {"Toon Two@World"},
    {"Toon Three@World"}
}

-- Inventory Management Thresholds
local gil_threshold = 0
local miniature_aetheryte_count = 0
local fuel_threshold = 0
local repair_mats_threshold = 0
local shark_hull_threshold = 0
local shark_stern_threshold = 0
local shark_bow_threshold = 0
local shark_bridge_threshold = 0
local unkiu_bow_threshold = 0
local coelacanth_bridge_threshold = 0
local dive_credit_threshold = 0
local fire_shard_threshold = 0

-- ----------------------------------------------
-- Share the above lines with Inverse Supplier --
-- ----------------------------------------------

-- Item IDs
local gil_id = 1
local miniature_aetheryte_id = 6600
local fuel_id = 10155
local kits_id = 10373
local shark_hull_id = 21794
local shark_stern_id = 21795
local shark_bow_id = 21792
local shark_bridge_id = 21793
local unkiu_bow_id = 21796
local coelacanth_bridge_id = 23904
local dive_credit_id = 22317
local fire_shard_id = 2

-- -------------------------------------
-- -- End of Configuration Parameters --
-- -------------------------------------

-- ------------------------
-- -- Start of Functions --
-- ------------------------

-- Check all required plugins and stop if any are missing or disabled
if not CheckPluginsBagmanXA() then
    return -- Stop script execution if plugins are not ready
end

-- Function to move to Tony's location, checking both world and zone
local function ApproachTonyXA()
    PathfindAndMoveTo(tony_x, tony_y, tony_z, false)
    FullStopMovementXA()
end

local function TonyMovementXA()
    -- Check if we are on the correct world
    local current_world, _ = GetWorldNameXA()
    if current_world ~= TonyTurf then
        DebugXA("Not on " .. TonyTurf .. ". Traveling to world now.")
        LifestreamCmdXA(TonyTurf)
    else
        DebugXA("Already on " .. TonyTurf .. ".")
    end
    
    -- Proceed with zone check
    DebugXA("Starting the process: Check if already in " .. TonySpot .. ".")
    if GetZoneID() == TonyZoneID then
        DebugXA("Already in " .. TonySpot .. ". Moving to supplier location.")
        ApproachTonyXA()
    else
        DebugXA("Not in " .. TonySpot .. ". Teleporting now.")
        LifestreamCmdXA(TonySpot)
        ApproachTonyXA()
    end
end

-- ----------------------
-- -- End of Functions --
-- ----------------------

-- --------------------------
-- -- Start of XA Relogger --
-- --------------------------

function ProcessToonListXA()
    for i = 1, #toon_list do
        local who = toon_list[i][1]
        if who and who ~= "" then
            ProcessToonXA(i, #toon_list, who)
        end
    end
end

function CheckIfItemsNeeded()
    -- Check all item counts and determine if any items are needed
    local current_gil = GetGil() or 0
    local current_aetherytes = GetItemCount(miniature_aetheryte_id) or 0
    local current_fuel = GetItemCount(fuel_id) or 0
    local current_repair_mats = GetItemCount(kits_id) or 0
    local current_shark_hull = GetItemCount(shark_hull_id) or 0
    local current_shark_stern = GetItemCount(shark_stern_id) or 0
    local current_shark_bow = GetItemCount(shark_bow_id) or 0
    local current_shark_bridge = GetItemCount(shark_bridge_id) or 0
    local current_unkiu_bow = GetItemCount(unkiu_bow_id) or 0
    local current_coelacanth_bridge = GetItemCount(coelacanth_bridge_id) or 0
    local current_dive_credit = GetItemCount(dive_credit_id) or 0
    local current_fire_shard = GetItemCount(fire_shard_id) or 0
    
    -- Check if any thresholds are not met
    local items_needed = false
    
    if current_gil < gil_threshold or 
       current_aetherytes < miniature_aetheryte_count or
       current_fuel < fuel_threshold or
       current_repair_mats < repair_mats_threshold or
       current_shark_hull < shark_hull_threshold or
       current_shark_stern < shark_stern_threshold or
       current_shark_bow < shark_bow_threshold or
       current_shark_bridge < shark_bridge_threshold or
       current_unkiu_bow < unkiu_bow_threshold or
       current_coelacanth_bridge < coelacanth_bridge_threshold or
       current_dive_credit < dive_credit_threshold or
       current_fire_shard < fire_shard_threshold then
        items_needed = true
    end
    
    return items_needed, current_gil, current_aetherytes, current_fuel, current_repair_mats,
           current_shark_hull, current_shark_stern, current_shark_bow, current_shark_bridge,
           current_unkiu_bow, current_coelacanth_bridge, current_dive_credit, current_fire_shard
end

function ProcessToonXA(i, total, who)
    DebugXA(string.format("[Relog %d/%d] -> %s", i, total, who))

    if GetCharacterName(true) ~= who then
        ARRelogXA(who)
    else
        DebugXA("Already logged in as " .. who)
    end
    CharacterSafeWaitXA() -- Do not remove this checker
    
    -- Initial inventory check
    local items_needed, current_gil, current_aetherytes, current_fuel, current_repair_mats,
          current_shark_hull, current_shark_stern, current_shark_bow, current_shark_bridge,
          current_unkiu_bow, current_coelacanth_bridge, current_dive_credit, current_fire_shard = CheckIfItemsNeeded()
    
    -- If all thresholds are met, skip to next toon
    if not items_needed then
        TradeDebugXA("[✓] All thresholds already met! No items needed.")
        DebugXA("[✓] Moving to next character...")
        SleepXA(1)
        return
    end
    
    -- Items are needed - execute supplier pathing and wait for items
    TradeDebugXA("[!] Items needed detected. Executing supplier sequence...")
    
    -- Move to Tony's location for supplier interaction
    TonyMovementXA()
    
    -- Keep checking until all thresholds are reached
    while items_needed do
        
        EchoXA("-------------")
        EchoXA("Checking Thresholds:")
        
        -- Consolidated threshold checking using table-driven approach
        local item_checks = {
            {name = "Gil", current = current_gil, threshold = gil_threshold},
            {name = "Miniature Aetheryte", current = current_aetherytes, threshold = miniature_aetheryte_count},
            {name = "Ceruleum Tank", current = current_fuel, threshold = fuel_threshold},
            {name = "Magitek Repair Materials", current = current_repair_mats, threshold = repair_mats_threshold},
            {name = "Shark-class Pressure Hull", current = current_shark_hull, threshold = shark_hull_threshold},
            {name = "Shark-class Stern", current = current_shark_stern, threshold = shark_stern_threshold},
            {name = "Shark-class Bow", current = current_shark_bow, threshold = shark_bow_threshold},
            {name = "Shark-class Bridge", current = current_shark_bridge, threshold = shark_bridge_threshold},
            {name = "Unkiu-class Bow", current = current_unkiu_bow, threshold = unkiu_bow_threshold},
            {name = "Coelacanth-class Bridge", current = current_coelacanth_bridge, threshold = coelacanth_bridge_threshold},
            {name = "Dive Credit", current = current_dive_credit, threshold = dive_credit_threshold},
            {name = "Fire Shard", current = current_fire_shard, threshold = fire_shard_threshold}
        }
        
        for _, item in ipairs(item_checks) do
            local status = item.current >= item.threshold and "[✓]" or "[✗]"
            EchoXA(string.format("%s %s: %d / %d", status, item.name, item.current, item.threshold))
        end
        
        EchoXA("Waiting 5s...")
        SleepXA(5)
        
        -- Refresh all counts and check if items are still needed
        items_needed, current_gil, current_aetherytes, current_fuel, current_repair_mats,
        current_shark_hull, current_shark_stern, current_shark_bow, current_shark_bridge,
        current_unkiu_bow, current_coelacanth_bridge, current_dive_credit, current_fire_shard = CheckIfItemsNeeded()
    end
    
    TradeDebugXA("[✓] All thresholds met! Returning home.")
    return_to_autoXA()

    EchoXA("[✓] Moving to next character.")
    SleepXA(1)
end

ProcessToonListXA()
DebugXA("Inverse Bagman has finished successfully!")

LogoutXA()
-- EnableARMultiXA()

-- ------------------------
-- -- End of XA Relogger --
-- ------------------------
