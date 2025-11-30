-- ┌-----------------------------------------------------------------------------------------------------------------------
-- | 
-- |   ██╗  ██╗ █████╗     ██╗███╗   ██╗██╗   ██╗███████╗██████╗ ███████╗███████╗    ███████╗██╗   ██╗██████╗ ██████╗ ██╗     ██╗███████╗██████╗ 
-- |   ╚██╗██╔╝██╔══██╗    ██║████╗  ██║██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔════╝██║   ██║██╔══██╗██╔══██╗██║     ██║██╔════╝██╔══██╗
-- |    ╚███╔╝ ███████║    ██║██╔██╗ ██║██║   ██║█████╗  ██████╔╝███████╗█████╗      ███████╗██║   ██║██████╔╝██████╔╝██║     ██║█████╗  ██████╔╝
-- |    ██╔██╗ ██╔══██║    ██║██║╚██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝      ╚════██║██║   ██║██╔═══╝ ██╔═══╝ ██║     ██║██╔══╝  ██╔══██╗
-- |   ██╔╝ ██╗██║  ██║    ██║██║ ╚████║ ╚████╔╝ ███████╗██║  ██║███████║███████╗    ███████║╚██████╔╝██║     ██║     ███████╗██║███████╗██║  ██║
-- |   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚══════╝ ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝╚══════╝╚═╝  ╚═╝
-- | 
-- |  Automated supplier script that distributes resources to franchise owners via dropbox trading system.
-- | 
-- |  This script scans for nearby franchise owners and automatically distributes configured resource thresholds using the
-- |  dropbox trading system. Works in tandem with XA Inverse Bagman to create a complete automated resource distribution
-- |  workflow for submarine operations and multi-character resource management.
-- | 
-- |  Core Features:
-- |  • Automated nearby player scanning with configurable distance thresholds
-- |  • Franchise owner detection from synchronized character list
-- |  • Automatic dropbox trading using Bagman Type 69 methodology
-- |  • Resource threshold-based distribution system
-- |  • Trade completion tracking with visual status indicators
-- |  • Distance-based movement to approach franchise owners
-- |  • Configurable scan intervals and trade delays
-- |  • Debug logging for troubleshooting
-- | 
-- |  Important Note: This script requires dfunc.lua and xafunc.lua dependencies. Configuration parameters (toon_list,
-- |  item thresholds, and item IDs) must be synchronized with XA Inverse Bagman for proper operation. The supplier
-- |  distributes items while Bagman waits for thresholds to be met on each character.
-- | 
-- |  Important Steps: Be logged into the Supplier toon before starting the script.
-- | 
-- | XA Inverse Supplier v2.14
-- | Automated resource distribution via dropbox trading
-- | Created by: https://github.com/xa-io
-- | Last Updated: 2025-11-30 16:50:00
-- | 
-- | ## Release Notes ##
-- | 
-- | v2.14
-- |   - Enhanced toon_list documentation with comprehensive format guide
-- |   - Added Smart Distribution (with AR Parser) section with detailed examples
-- |   - Added Manual Override section for custom threshold amounts
-- |   - Added Threshold-Based section for default behavior
-- |   - Added Workflow section explaining Bagman/Supplier interaction
-- |   - Improved documentation formatting consistency with Inverse Bagman
-- | 
-- | v2.13
-- |   - Fixed trade failure repositioning when player moves toward supplier
-- |   - When trade fails, supplier now repositions back to original location before retrying
-- |   - Added re-targeting and distance check after repositioning
-- |   - Prevents out-of-range trade failures when players approach supplier during initial movement
-- |   - Enhanced retry logic: supplies check → reposition → re-target → distance check → retry trade
-- | 
-- | v2.11
-- |   - Added smart inventory-based distribution logic
-- |   - Toon list now supports optional current inventory counts for Ceruleum Tanks and Repair Kits
-- |   - Format: {"Toon@World", current_fuel_count, current_kits_count} - inventory counts are optional
-- |   - Script calculates needed items: gives (threshold - current_count) instead of full threshold
-- |   - Backwards compatible: 0 values or missing values use original behavior (full threshold)
-- |   - Optimizes resource distribution by only giving what each character actually needs
-- | 
-- | v2.1
-- |   - Added required plugin checks (KitchenSink, Dropbox, Lifestream, vnavmesh, AutoRetainer, Pandora, TextAdvance)
-- |   - Script now validates all required plugins are installed and enabled before execution
-- |   - Detailed plugin status display via CheckPluginStatus() from xafunc
-- | 
-- | v2.0 
-- |   - Enhanced automated supplier with dropbox trading
-- |   - Automated franchise owner detection and targeting
-- |   - Threshold-based resource distribution from synchronized configuration
-- |   - Trade completion tracking with remaining character list
-- |   - Distance-based movement with configurable thresholds
-- |   - Dropbox trading integration using Bagman Type 69 methodology
-- |   - Configuration synchronization markers for Inverse Bagman pairing
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
-- |  Works with: XA Inverse Bagman
-- |  Configuration: Synchronize toon_list and item thresholds between both scripts
-- └-----------------------------------------------------------------------------------------------------------------------

-- DO NOT TOUCH THESE LINES BELOW
require("dfunc")
require("xafunc")
DisableARMultiXA()
rsrXA("off")
if not CheckPluginEnabledXA({"KitchenSink", "Dropbox", "Lifestream", "vnavmesh", "AutoRetainer", "PandorasBox", "TextAdvance"}) then return end
-- DO NOT TOUCH THESE LINES ABOVE

-- ---------------------------------------
-- -- Start of Configuration Parameters --
-- ---------------------------------------

debug_mode = false
tradedebug_mode = true
listdebug_mode = false

local scan_interval = 2                 -- Scan interval in seconds (how often to check for nearby players)
local max_scan_distance = 6             -- Maximum distance to scan for players (in yalms)
local move_distance_threshold = 4       -- Distance threshold to trigger movement (in yalms)
local stop_distance = 2                 -- Stop movement when within this distance (in yalms)
local trade_delay = 2                   -- Delay before initiating trade sequence (in seconds)

-- Supplier's coordinates (set this manually so the supplier stays at a set location)
-- Use GetInverseBagmanCoordsXA() from xafunc to get this. Required if changing TonySpot
local tony_x = 243.92610168457
local tony_y = 111.58336639404
local tony_z = -253.4475402832
-- The above location will walk slightly away from the actual afk placement so it will move and face the general direction
-- The targeting system in the script and functions will handle the movements needed and may even move sometimes slightly

-- -------------------------------------------------------
-- -- Inverse Supplier Toon List - Format Documentation --
-- -------------------------------------------------------
-- Format: {"Character@World", fuel_to_give, kits_to_give}
--
-- IMPORTANT: The numbers represent HOW MANY ITEMS TO GIVE (not current inventory)
--
-- -------------------------------------------------------
-- -- Smart Distribution (with AR Parser) - RECOMMENDED --
-- -------------------------------------------------------
--   The AR Parser calculates: items_to_give = threshold - current_inventory
--   This is the MOST COMMON use case for fuel and kits distribution
--
--   Example from AR Parser output in column (Inverse Supplier Formatting):
--     {"Toon One@World", 76, 1}
--       → Supplier gives 76 Ceruleum Tanks and 0 Repair Kits
--       → AR Parser calculated this:
--       → Has 24,924 tanks (needs 76 to reach 25,000)
--       → Has 3,999 kits (needs 1 to reach 4,000)
--       → Allows per-character control based on actual inventory levels
--
--       Example Thresholds used for Inverse Bagman & Inverse Supplier:
--       local fuel_threshold = 25000
--       local repair_mats_threshold = 4000
--
-- -----------------------------------------
-- -- Manual Override (without AR Parser) --
-- -----------------------------------------
--   You can specify custom amounts that OVERRIDE the thresholds below:
--
--   Example:
--     {"Toon One@World", 500, 200}
--       → Supplier gives 500 Ceruleum Tanks and 200 Repair Kits
--       → Even if fuel_threshold and repair_mats_threshold are set to different values
--       → Custom amounts always take priority over threshold settings
--
-- --------------------------------------------
-- -- Threshold-Based (no amounts specified) --
-- --------------------------------------------
--   When no custom amounts are provided, uses threshold values from configuration below:
--
--   Example:
--     {"Toon One@World"}
--       → Supplier gives fuel_threshold tanks and repair_mats_threshold kits
--
--   Example:
--     {"Toon One@World", 0, 0}
--       → Same as above (0 means "use threshold instead")
--
-- --------------
-- -- Workflow --
-- --------------
--   1. Inverse Bagman: Logs into each character → Requests full thresholds from Supplier
--   2. Inverse Supplier: Gives items → Uses custom amounts if specified, otherwise uses thresholds
--   3. Result: Characters get threshold amounts for most items, except fuel/kits which use AR Parser values (if specified)
--
-- ------------------------------------------------------------

-- Toon list (last toon should not have a comma at the end)
local toon_list = {
    {"Toon One@World"},
    {"Toon Two@World", 10, 20},
    {"Toon Three@World", 10, 20},
    {"Toon Four@World"},
    {"Toon Five@World"}
}

-- ------------------------------------------
-- Get the below lines from Inverse Bagman --
-- ------------------------------------------

-- Where is the supplier location
local TonyTurf = "Sophia"
local TonySpot = "Summerford Farms" -- Use the Aetheryte Name for this
local TonyZoneID = 134 -- Use GetZoneIDXA() from xafunc to get this

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

-- ------------------------------------------
-- Get the above lines from Inverse Bagman --
-- ------------------------------------------

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

-- Smart Distribution Functions (v2.11)
-- These functions implement inventory-aware distribution logic

local function GetToonInventoryData(target_name)
    -- Get the needed amounts from toon_list for a specific character
    -- These represent how much the character needs, calculated by AR Parser as (threshold - current_inventory)
    -- Returns: fuel_needed, kits_needed (or nil, nil if not found/not specified)
    for _, owner_data in ipairs(toon_list) do
        if owner_data[1] == target_name then
            local fuel_needed = owner_data[2] or 0
            local kits_needed = owner_data[3] or 0
            return fuel_needed, kits_needed
        end
    end
    return nil, nil
end

local function CalculateNeededAmount(needed_count, threshold)
    -- Calculate how many items to give based on needed amount
    -- If needed_count is 0 or nil, return full threshold (original behavior)
    -- Otherwise return the needed_count directly (already calculated by AR Parser)
    if not needed_count or needed_count == 0 then
        return threshold
    end
    
    -- Return the needed amount (AR Parser already calculated: threshold - current_inventory)
    -- Ensure it's not negative
    local needed = needed_count
    if needed < 0 then
        needed = 0
    end
    
    return needed
end

local function ShouldUseSmartDistribution(fuel_needed, kits_needed)
    -- Determine if we should use smart distribution logic
    -- Returns false if both values are nil/0 (use original behavior)
    -- Returns true if either value is greater than 0 (use smart distribution)
    if not fuel_needed and not kits_needed then
        return false
    end
    
    fuel_needed = fuel_needed or 0
    kits_needed = kits_needed or 0
    
    return (fuel_needed > 0 or kits_needed > 0)
end

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

-- Completed trades tracking
local completedTrades = {}           -- Table to track characters we've already traded with

-- Debug functions are now in xafunc.lua (DebugLogXA, TradeDebugXA, ListDebug)

function IsPlayerInList(player_name)
    for _, owner_data in ipairs(toon_list) do
        if player_name == owner_data[1] then
            return true
        end
    end
    return false
end

function IsTradeCompleted(player_name)
    return completedTrades[player_name] == true
end

function MarkTradeCompleted(player_name)
    completedTrades[player_name] = true
    TradeDebugXA(string.format("[Trade Complete] %s marked as completed", player_name))
end

function GetRemainingTradesList()
    local remaining = {}
    for _, owner_data in ipairs(toon_list) do
        local owner_name = owner_data[1]
        if not completedTrades[owner_name] then
            table.insert(remaining, owner_name)
        end
    end
    return remaining
end

function DisplayTradeStatus()
    local totalCount = #toon_list
    local completedCount = 0
    
    for _ in pairs(completedTrades) do
        completedCount = completedCount + 1
    end
    
    local remainingCount = totalCount - completedCount
    
    ListDebugXA("========================================")
    TradeDebugXA(string.format("[Trade Status] %d/%d completed | %d remaining", completedCount, totalCount, remainingCount))
    
    if completedCount > 0 then
        ListDebugXA("[Completed Trades]:")
        for owner_name, _ in pairs(completedTrades) do
            ListDebugXA(string.format("  ✓ %s", owner_name))
        end
    end
    
    if remainingCount > 0 then
        ListDebugXA("[Remaining Characters]:")
        local remaining = GetRemainingTradesList()
        for i, owner_name in ipairs(remaining) do
            ListDebugXA(string.format("  %d. %s", i, owner_name))
        end
    else
        TradeDebugXA("★★★ ALL TRADES COMPLETED! ★★★")
    end
    
    ListDebugXA("========================================")
end

function WhileSuppliesAreLow(items_to_send, target_name)
    -- Keep checking supplies every 20 seconds until we have enough
    EchoXA("========================================")
    EchoXA("[Supply Check] Waiting for supplies...")
    EchoXA("========================================")
    
    local all_supplies_met = false
    
    while not all_supplies_met do
        all_supplies_met = true
        
        EchoXA("-------------")
        EchoXA("Current Supply Status:")
        EchoXA(string.format("Target: %s", target_name))
        EchoXA("-------------")
        
        -- Show remaining characters to trade with
        local remaining = GetRemainingTradesList()
        if #remaining > 0 then
            ListDebugXA("[Characters Remaining]")
            for i, owner_name in ipairs(remaining) do
                local indicator = (owner_name == target_name) and ">>> " or "    "
                ListDebugXA(string.format("%s%d. %s", indicator, i, owner_name))
            end
            ListDebugXA("-------------")
        end
        
        -- Check each item we need to supply
        EchoXA("[Items Needed for Trade]")
        for _, item in ipairs(items_to_send) do
            local current_count = GetItemCount(item.id) or 0
            local status = current_count >= item.amount and "[✓]" or "[✗]"
            
            EchoXA(string.format("%s %s: %d / %d", status, item.name, current_count, item.amount))
            
            if current_count < item.amount then
                all_supplies_met = false
            end
        end
        
        if not all_supplies_met then
            EchoXA("-------------")
            EchoXA("[!!! Supplies Low !!!] Waiting 20 seconds...")
            EchoXA("<se.7> Inverse Supplier Attention Needed")
            EchoXA("========================================")
            SleepXA(20)
        else
            ListDebugXA("-------------")
            ListDebugXA("[✓ Supplies Ready] All items available!")
            ListDebugXA("========================================")
        end
    end
end

function CalculateItemsNeeded(target_name)
    -- Calculate how many of each item the target needs based on thresholds
    -- v2.11: Now supports smart distribution using needed amounts from toon_list
    
    DebugXA(string.format("[Calculating Items] Determining supplies needed for %s...", target_name))
    
    local items_to_send = {}
    
    -- Get needed amounts from toon_list (calculated by AR Parser as threshold - current_inventory)
    local fuel_needed, kits_needed = GetToonInventoryData(target_name)
    local use_smart_distribution = ShouldUseSmartDistribution(fuel_needed, kits_needed)
    
    if use_smart_distribution then
        DebugXA(string.format("[Smart Distribution] Using needed amounts for %s", target_name))
        DebugXA(string.format("  Ceruleum Tanks Needed: %d", fuel_needed or 0))
        DebugXA(string.format("  Repair Kits Needed: %d", kits_needed or 0))
    else
        DebugXA("[Standard Distribution] Using full threshold amounts (no needed data specified)")
    end
    
    -- Calculate amounts for Ceruleum Tanks and Repair Kits with smart distribution
    local fuel_amount = fuel_threshold
    local kits_amount = repair_mats_threshold
    
    if use_smart_distribution then
        fuel_amount = CalculateNeededAmount(fuel_needed, fuel_threshold)
        kits_amount = CalculateNeededAmount(kits_needed, repair_mats_threshold)
        
        if fuel_threshold > 0 then
            DebugXA(string.format("  Ceruleum Tanks: Giving %d (needed to reach threshold %d)", fuel_amount, fuel_threshold))
        end
        if repair_mats_threshold > 0 then
            DebugXA(string.format("  Repair Kits: Giving %d (needed to reach threshold %d)", kits_amount, repair_mats_threshold))
        end
    end
    
    -- Consolidated item definitions using table-driven approach
    local item_definitions = {
        {name = "Gil", id = gil_id, threshold = gil_threshold},
        {name = "Miniature Aetheryte", id = miniature_aetheryte_id, threshold = miniature_aetheryte_count},
        {name = "Ceruleum Tank", id = fuel_id, threshold = fuel_amount},  -- Uses smart amount
        {name = "Magitek Repair Materials", id = kits_id, threshold = kits_amount},  -- Uses smart amount
        {name = "Shark-class Pressure Hull", id = shark_hull_id, threshold = shark_hull_threshold},
        {name = "Shark-class Stern", id = shark_stern_id, threshold = shark_stern_threshold},
        {name = "Shark-class Bow", id = shark_bow_id, threshold = shark_bow_threshold},
        {name = "Shark-class Bridge", id = shark_bridge_id, threshold = shark_bridge_threshold},
        {name = "Unkiu-class Bow", id = unkiu_bow_id, threshold = unkiu_bow_threshold},
        {name = "Coelacanth-class Bridge", id = coelacanth_bridge_id, threshold = coelacanth_bridge_threshold},
        {name = "Dive Credit", id = dive_credit_id, threshold = dive_credit_threshold},
        {name = "Fire Shard", id = fire_shard_id, threshold = fire_shard_threshold}
    }
    
    -- Add items to send list if threshold > 0
    for _, item in ipairs(item_definitions) do
        if item.threshold > 0 then
            table.insert(items_to_send, {id = item.id, amount = item.threshold, name = item.name})
        end
    end
    
    return items_to_send
end

function SendItemsViaDropbox(target_name, items_to_send)
    local trade_successful = false
    local max_trade_attempts = 3
    local trade_attempt = 0
    
    while not trade_successful and trade_attempt < max_trade_attempts do
        trade_attempt = trade_attempt + 1
        DebugXA("========================================")
        DebugXA(string.format("[Trade Attempt %d/%d] for %s", trade_attempt, max_trade_attempts, target_name))
        DebugXA("========================================")
        
        -- Get BEFORE counts for all items we're about to trade
        local before_counts = {}
        DebugXA("[Pre-Trade Inventory Check]")
        for _, item in ipairs(items_to_send) do
            before_counts[item.id] = GetItemCount(item.id) or 0
            DebugXA(string.format("  %s: %d available (need to give %d)", item.name, before_counts[item.id], item.amount))
            
            -- Check if we have enough items BEFORE attempting trade
            if before_counts[item.id] < item.amount then
                EchoXA(string.format("[!!! INSUFFICIENT ITEMS !!!] %s: Have %d, Need %d", 
                    item.name, before_counts[item.id], item.amount))
                EchoXA("<se.7> Inverse Supplier Attention Needed")
                
                -- Show supply status and wait
                WhileSuppliesAreLow(items_to_send, target_name)
                -- After waiting, recheck counts
                before_counts[item.id] = GetItemCount(item.id) or 0
            end
        end
        
        -- Send calculated items via dropbox system (Bagman Type 69 methodology)
        DebugXA("[Trade Preparation] Opening dropbox...")
        OpenDropboxXA()
        ClearDropboxXA()
        SleepXA(0.5)
        
        -- Queue all items for trade
        for _, item in ipairs(items_to_send) do
            DebugXA(string.format("[Queueing] %s x%d (ID: %d)", item.name, item.amount, item.id))
            DropboxSetItemQuantity(item.id, false, item.amount)
        end
        
        -- Execute trade sequence from Bagman Type 69
        SleepXA(0.99)
        FocusTargetXA()
        DebugXA("[Starting Trade] Initiating DropboxStart...")
        DropboxStart()
        OpenArmouryChestXA()
        
        -- Wait for trade to complete
        floo = DropboxIsBusy()
        while floo == true do
            floo = DropboxIsBusy()
            SleepXA(1)
            DebugXA("Trading happening!")
        end
        
        DebugXA("[Trade Finished] DropboxStart sequence complete")
        ClearDropboxXA()
        SleepXA(2) -- Give time for inventory to update
        
        -- Get AFTER counts and validate trade completion
        DebugXA("========================================")
        DebugXA("[Post-Trade Inventory Validation]")
        trade_successful = true -- Assume success until proven otherwise
        
        for _, item in ipairs(items_to_send) do
            local after_count = GetItemCount(item.id) or 0
            local items_traded = before_counts[item.id] - after_count
            
            DebugXA(string.format("  %s:", item.name))
            DebugXA(string.format("    Before: %d | After: %d | Traded: %d | Expected: %d", 
                before_counts[item.id], after_count, items_traded, item.amount))
            
            -- Check if we traded the expected amount
            if items_traded < item.amount then
                DebugXA(string.format("    [✗ TRADE INCOMPLETE] Only traded %d out of %d needed!", items_traded, item.amount))
                trade_successful = false
            elseif items_traded == item.amount then
                EchoXA("    [✓ SUCCESS] Trade completed successfully!")
            else
                DebugXA(string.format("    [? WARNING] Traded more than expected: %d vs %d", items_traded, item.amount))
            end
        end
        
        if not trade_successful then
            if trade_attempt < max_trade_attempts then
                EchoXA("========================================")
                EchoXA("[Trade Failed] Will retry after repositioning...")
                EchoXA("<se.7> Inverse Supplier Attention Needed")
                EchoXA("========================================")
                
                -- Check supplies first
                WhileSuppliesAreLow(items_to_send, target_name)
                
                -- Reposition: Move back to original Tony location
                EchoXA("[Repositioning] Moving back to supplier location...")
                ApproachTonyXA()
                SleepXA(2)
                
                -- Strip world name from target_name to get searchable name
                local search_name = target_name
                local at_pos = string.find(target_name, "@")
                if at_pos then
                    search_name = string.sub(target_name, 1, at_pos - 1)
                end
                
                -- Re-target the player
                EchoXA(string.format("[Re-targeting] Targeting %s...", target_name))
                TargetXA(search_name)
                SleepXA(1)
                FocusTargetXA()
                SleepXA(1)
                
                -- Check distance and move closer if needed
                local obj_x = GetObjectRawXPos(search_name)
                local obj_y = GetObjectRawYPos(search_name)
                local obj_z = GetObjectRawZPos(search_name)
                
                if obj_x ~= 0 or obj_y ~= 0 or obj_z ~= 0 then
                    local player_x = EntityPlayerPositionX()
                    local player_y = EntityPlayerPositionY()
                    local player_z = EntityPlayerPositionZ()
                    
                    local dx = obj_x - player_x
                    local dy = obj_y - player_y
                    local dz = obj_z - player_z
                    local distance = math.sqrt(dx * dx + dy * dy + dz * dz)
                    
                    EchoXA(string.format("[Distance Check] %.1f yalms from target", distance))
                    
                    if distance > move_distance_threshold then
                        EchoXA(string.format("[Moving] Distance %.1f yalms > %d, moving closer...", distance, move_distance_threshold))
                        WalkToTargetXA(obj_x, obj_y, obj_z, stop_distance)
                        EchoXA("[Movement Complete] Ready to retry trade")
                    else
                        EchoXA("[Range OK] Target is within range")
                    end
                else
                    EchoXA("[Warning] Could not get target position, will attempt trade anyway")
                end
                
                SleepXA(2)
                EchoXA("[Retry Ready] Attempting trade again...")
            else
                EchoXA("========================================")
                EchoXA("[!!! MAX ATTEMPTS REACHED !!!]")
                EchoXA("<se.7> Inverse Supplier Attention Needed")
                EchoXA("========================================")
            end
        else
            EchoXA("========================================")
            EchoXA("[✓ TRADE VALIDATED] All items traded successfully!")
            EchoXA("========================================")
        end
    end
    
    return trade_successful
end

function ScanNearbyPlayers()
    DebugXA("Scanning for nearby toons...")
    
    local found_count = 0
    
    -- Check each toon in the list
    for _, owner_data in ipairs(toon_list) do
        local owner_name = owner_data[1]
        
        -- Strip world name if present (everything after @)
        local search_name = owner_name
        local at_pos = string.find(owner_name, "@")
        if at_pos then
            search_name = string.sub(owner_name, 1, at_pos - 1)
        end
        
        -- Check if this player exists nearby
        if Entity.GetEntityByName(search_name) ~= nil then
            local obj_x = GetObjectRawXPos(search_name)
            local obj_y = GetObjectRawYPos(search_name)
            local obj_z = GetObjectRawZPos(search_name)
            
            if obj_x ~= 0 or obj_y ~= 0 or obj_z ~= 0 then
                local player_x = EntityPlayerPositionX()
                local player_y = EntityPlayerPositionY()
                local player_z = EntityPlayerPositionZ()
                
                local dx = obj_x - player_x
                local dy = obj_y - player_y
                local dz = obj_z - player_z
                local distance = math.sqrt(dx * dx + dy * dy + dz * dz)
                
                -- Check if within scan range
                if distance <= max_scan_distance then
                    -- Check if already traded with this character
                    if IsTradeCompleted(owner_name) then
                        DebugXA(string.format("Skipping %s - trade already completed", owner_name))
                    else
                        DebugXA(string.format("Found player: %s (Distance: %.1f yalms)", owner_name, distance))
                        DebugXA(string.format("★ [Toon] %s ★", owner_name))
                        DebugXA(string.format("[Distance] %.1f yalms", distance))
                    
                        -- Target the toon
                        TargetXA(search_name)
                        SleepXA(1)
                        
                        found_count = found_count + 1
                        
                        -- Optional: Focus target them as well
                        FocusTargetXA()
                        SleepXA(trade_delay) -- Configurable delay before trade
                        
                        -- If distance is over threshold, move closer
                        if distance > move_distance_threshold then
                            DebugXA(string.format("[Moving] Distance %.1f yalms > %d, moving closer...", distance, move_distance_threshold))
                            WalkToTargetXA(obj_x, obj_y, obj_z, stop_distance)
                            DebugXA("[Completed]")
                        end
                        
                        -- ========================================
                        -- Inventory Management & Trade Sequence
                        -- ========================================
                        -- Calculate what items this character needs
                        local items_to_send = CalculateItemsNeeded(owner_name)
                        
                        -- Send items via dropbox (Bagman Type 69 methodology)
                        local trade_success = false
                        if #items_to_send > 0 then
                            trade_success = SendItemsViaDropbox(owner_name, items_to_send)
                        else
                            EchoXA("[No Items] No thresholds configured, skipping trade")
                            trade_success = true -- Consider it success if no items needed
                        end
                        -- ========================================
                        
                        -- Only mark as completed if trade was successful
                        if trade_success then
                            MarkTradeCompleted(owner_name)
                        else
                            EchoXA("[Trade Failed] Not marking as completed, will retry on next scan")
                            OpenDropboxXA()
                        end
                        
                        -- Display updated trade status
                        DisplayTradeStatus()
                        
                        -- Wait before continuing to next scan
                        SleepXA(10)
                        
                        return true, owner_name
                    end
                end
            end
        end
    end
    
    if found_count == 0 then
        DebugXA("No toons found nearby.")
    end
    
    return false, nil
end

-- ----------------------
-- -- End of Functions --
-- ----------------------

-- ----------------------------------
-- -- Start of XA Inverse Supplier --
-- ----------------------------------

EchoXA("========================================")
EchoXA("  XA Nearby Player Scanner - STARTED")
EchoXA("========================================")
DebugXA(string.format("[Monitoring] %d toons", #toon_list))
DebugXA(string.format("[Scan Range] %d yalms", max_scan_distance))
DebugXA(string.format("[Scan Interval] %.1f seconds", scan_interval))
DebugXA("========================================")

-- Display toon list
ListDebugXA("[Toon List]")
for i, owner_data in ipairs(toon_list) do
    ListDebugXA(string.format("  %d. %s", i, owner_data[1]))
end
ListDebugXA("========================================")

-- Display initial trade status
DisplayTradeStatus()

-- Move to Tony's location (ensure we're in the right world, zone, and spot)
DebugXA("========================================")
DebugXA("Ensuring supplier is at correct location...")
TonyMovementXA()
DebugXA("[Location Ready] Supplier positioned and ready to scan")
DebugXA("========================================")

-- Main scanning loop
while true do
    -- Wait for player to be available
    CharacterSafeWaitXA()
    
    -- Check if all trades are completed
    local completedCount = 0
    for _ in pairs(completedTrades) do
        completedCount = completedCount + 1
    end
    
    if completedCount >= #toon_list then
        EchoXA("========================================")
        EchoXA("★★★ ALL TRADES COMPLETED - SCRIPT ENDING ★★★")
        EchoXA("========================================")
        break
    end
    
    -- Perform scan
    ScanNearbyPlayers()
    
    -- Wait before next scan
    SleepXA(scan_interval)
end

EchoXA("Inverse Supplier has finished successfully!")

LogoutXA()
-- EnableARMultiXA()

-- --------------------------------
-- -- End of XA Inverse Supplier --
-- --------------------------------
