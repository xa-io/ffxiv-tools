-- ┌-----------------------------------------------------------------------------------------------------------------------
-- | 
-- |   ██╗  ██╗ █████╗     ██╗███╗   ██╗██╗   ██╗███████╗██████╗ ███████╗███████╗          
-- |   ╚██╗██╔╝██╔══██╗    ██║████╗  ██║██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝          
-- |    ╚███╔╝ ███████║    ██║██╔██╗ ██║██║   ██║█████╗  ██████╔╝███████╗█████╗            
-- |    ██╔██╗ ██╔══██║    ██║██║╚██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝            
-- |   ██╔╝ ██╗██║  ██║    ██║██║ ╚████║ ╚████╔╝ ███████╗██║  ██║███████║███████╗          
-- |   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝          
-- |                                                                                     
-- |   ██████╗  █████╗  ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗    ██╗   ██╗███████╗ ██████╗ 
-- |   ██╔══██╗██╔══██╗██╔════╝ ████╗ ████║██╔══██╗████╗  ██║    ██║   ██║╚════██║ ╚════██╗
-- |   ██████╔╝███████║██║  ███╗██╔████╔██║███████║██╔██╗ ██║    ██║   ██║    ██╔╝  █████╔╝
-- |   ██╔══██╗██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║    ╚██╗ ██╔╝   ██╔╝   ╚═══██╗
-- |   ██████╔╝██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║     ╚████╔╝    ██║██╗██████╔╝
-- |   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝      ╚═══╝     ╚═╝╚═╝╚═════╝ 
-- | 
-- |  Automated inventory management system for FFXIV submarine operations.
-- | 
-- |  This script cycles through multiple characters to check their inventory status for submarine-related
-- |  materials and resources. It automatically logs into each character, teleports to Tony's location,
-- |  and reports needed items for efficient resource management across your submarine fleet.
-- | 
-- |  Core Features:
-- |  • Multi-character inventory scanning with automatic login rotation
-- |  • Submarine resource tracking (fuel, repair materials, parts, gil)
-- |  • Automated movement to Tony's location in Summerford Farms
-- |  • Configurable minimum thresholds for all tracked resources
-- |  • Real-time inventory status reporting via in-game chat
-- |  • Safe character switching with proper wait states and error handling
-- |  • Customizable item requirements for different submarine operations
-- |  • Automatic return to FC house after inventory checks
-- | 
-- |  Important Note: Requires SomethingNeedDoing plugin and proper character configuration. Ensure all
-- |  characters in the franchise_owners list have access to the required zones and permissions.
-- | 
-- | Requires:
-- |  dfunc; can be found here: https://github.com/McVaxius/dhogsbreakfeast/blob/main/dfunc.lua
-- |  xafunc; can be found here: https://github.com/xa-io/ffxiv-tools/blob/main/snd/xafunc.lua
-- |   - Two setup processes, 1) SND > Add script, name dfunc and another xafunc paste the code.
-- |   - 2) SND > Add script name the same as before, add github url and save, can update through SND
-- | 
-- |  Lifestream pathing to each FC door so on your next multi run it won't be stuck
-- |  Dropbox box auto accepting trades
-- | 
-- |  XA Inverse Bagman v7.3
-- |  Automated inventory management system for FFXIV submarine operations
-- |  Created by: https://github.com/xa-io
-- |  Last Updated: 2025-08-28 09:48:06
-- └-----------------------------------------------------------------------------------------------------------------------

-- ---------------------------------------
-- -- Start of Configuration Parameters --
-- ---------------------------------------

-- DO NOT TOUCH THESE LINES BELOW
    require("dfunc")
    require("xafunc")
    yield("/rotation Cancel")
-- DO NOT TOUCH THESE LINES ABOVE

-- Config Parameters
local TonyTurf = "Sophia"
local TonyZoneID = 134 -- Summerford Farms

-- Inventory Needs
local gil_buffer = 5000 -- Buffer to ignore missing gil if less than this amount
local min_gil_keep = 50000 -- Minimum amount of gil to keep
local min_fuel_keep = 0  -- The minimum amount of Ceruleum Fuel to keep
local min_repair_mats_keep = 0  -- The minimum amount of Magitek Repair Mats to keep
local min_shark_hull = 0
local min_shark_stern = 0
local min_shark_bow = 0
local min_shark_bridge = 0
local min_unkiu_bow = 0
local min_coelacanth_bridge = 0
local min_dive_credit = 0

-- Item IDs
local gil_id = 1 -- Gil
local fuel_id = 10155 -- Ceruleum Tank
local kits_id = 10373 -- Magitek Repair Materials
local shark_hull_id = 21794  -- Shark-class Pressure Hull
local shark_stern_id = 21795 -- Shark-class Stern
local shark_bow_id = 21792   -- Shark-class Bow
local shark_bridge_id = 21793 -- Shark-class Bridge
local unkiu_bow_id = 21796   -- Unkiu-class Bow
local coelacanth_bridge_id = 23904 -- Coelacanth-class Bridge
local dive_credit_id = 22317 -- Dive Credit

-- Tony's coordinates (set this manually so the alt runs to a set location)
local tony_x = 233.81164550781
local tony_y = 112.45678710938
local tony_z = -262.1672668457

-- Toon list (last toon should not have a comma at the end)
local franchise_owners = {
    {"Toon One@World"},
    {"Toon Two@World"},
    {"Toon Three@World"}
}

-- -------------------------------------
-- -- End of Configuration Parameters --
-- -------------------------------------

-- ------------------------
-- -- Start of Functions --
-- ------------------------

local function ipairs(t)
    local i = 0
    return function()
        i = i + 1
        local v = t[i]
        if v then
            return i, v
        end
    end
end

-- Function to calculate needed and excess items, then output them to chat
local function check_items()
    local gil_needed = min_gil_keep - GetGil()
    local fuel_needed = min_fuel_keep - GetItemCount(fuel_id)
    local mats_needed = min_repair_mats_keep - GetItemCount(kits_id)
    local items_needed = false
    local has_items_needed = false

    -- Output separator before items
    yield("/e -------------")
    yield("/e Items Needed:")

    -- Check for needed general items
    if gil_needed > gil_buffer then
        yield("/e Gil: " .. gil_needed)
        items_needed = true
        has_items_needed = true
    end
    if fuel_needed > 0 then
        yield("/e Fuel: " .. fuel_needed)
        items_needed = true
        has_items_needed = true
    end
    if mats_needed > 0 then
        yield("/e Kits: " .. mats_needed)
        items_needed = true
        has_items_needed = true
    end

    -- Check for needed parts (set minimum amounts)
    local parts = {
        { id = shark_hull_id, name = "Shark-class Pressure Hull", min = min_shark_hull },
        { id = shark_stern_id, name = "Shark-class Stern", min = min_shark_stern },
        { id = shark_bow_id, name = "Shark-class Bow", min = min_shark_bow },
        { id = shark_bridge_id, name = "Shark-class Bridge", min = min_shark_bridge },
        { id = unkiu_bow_id, name = "Unkiu-class Bow", min = min_unkiu_bow },
        { id = coelacanth_bridge_id, name = "Coelacanth-class Bridge", min = min_coelacanth_bridge },
        { id = dive_credit_id, name = "Dive Credit", min = min_dive_credit }
    }

    for _, part in ipairs(parts) do
        local count = GetItemCount(part.id)
        if count < part.min then
            yield("/e " .. part.name .. ": " .. (part.min - count))
            items_needed = true
            has_items_needed = true
        end
    end
    return has_items_needed
end

-- Function to move to Tony's location
local function approach_tony()
    PathfindAndMoveTo(tony_x, tony_y, tony_z, false)
    visland_stop_moving_xa()
end

-- Function to move to Tony's location, checking both world and zone
local function handle_tony_movement()
    -- Check if we are on the correct world
    yield("/li " .. TonyTurf)
    WaitForLifestream()
    yield("/wait 1.01")
    WaitForLifestream()
    yield("/wait 1.02")
    WaitForLifestream()
    yield("/wait 1.03")
    CharacterSafeWaitXA()
    
    -- Proceed with zone check
    yield("/echo Starting the process: Check if already in Summerford Farms...")
    if GetZoneID() == TonyZoneID then
        yield("/echo Already in Summerford Farms. Moving to Tony's location.")
        approach_tony()
    else
        yield("/echo Not in Summerford Farms. Teleporting now.")
        yield("/tp Summerford Farms")
        yield("/wait 12")
        CharacterSafeWaitXA()
        approach_tony()
    end
end

-- ----------------------
-- -- End of Functions --
-- ----------------------

-- --------------------------------
-- -- Start of XA Inverse Bagman --
-- --------------------------------

-- Function to cycle through characters and run inventory checks
local function cycle_characters()
    for _, owner in ipairs(franchise_owners) do
        -- Relog to the character in franchise_owners
        local character = owner[1]
        yield("/echo Logging in as " .. character)
        yield("/ays relog " .. character)
        yield("/wait 5")
        CharacterSafeWaitXA()
        yield("/at y")
        IsPlayerAvailableXA()
        handle_tony_movement()
        local items_status = check_items()

        -- Repeat check until all items are gathered
        while items_status do
            yield("/wait 3")
            items_status = check_items()
        end

        -- Return to the home location after checks
        return_to_fcXA()
    end
end

-- Execute the cycle_characters function to run the sequence
cycle_characters()

--[[
##################################
#### End of XA Inverse Bagman ####
##################################
]]
