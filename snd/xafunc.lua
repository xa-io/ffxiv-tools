-- ┌-----------------------------------------------------------------------------------------------------------------------
-- |
-- |   ██╗  ██╗ █████╗     ███████╗██╗   ██╗███╗   ██╗ ██████╗    ██╗     ██╗██████╗ ██████╗  █████╗ ██████╗ ██╗   ██╗
-- |   ╚██╗██╔╝██╔══██╗    ██╔════╝██║   ██║████╗  ██║██╔════╝    ██║     ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝
-- |    ╚███╔╝ ███████║    █████╗  ██║   ██║██╔██╗ ██║██║         ██║     ██║██████╔╝██████╔╝███████║██████╔╝ ╚████╔╝ 
-- |    ██╔██╗ ██╔══██║    ██╔══╝  ██║   ██║██║╚██╗██║██║         ██║     ██║██╔══██╗██╔══██╗██╔══██║██╔══██╗  ╚██╔╝  
-- |   ██╔╝ ██╗██║  ██║    ██║     ╚██████╔╝██║ ╚████║╚██████╗    ███████╗██║██████╔╝██║  ██║██║  ██║██║  ██║   ██║   
-- |   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝    ╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
-- |
-- | Comprehensive Function Library for FFXIV SomethingNeedDoing Automation
-- |
-- | XA Func Library provides a robust collection of helper functions for automating FFXIV gameplay through
-- | SomethingNeedDoing scripts. This library extends dfunc with additional movement, UI, player management,
-- | and world interaction utilities designed for reliable multi-character automation workflows.
-- |
-- | Important Note: This library requires dfunc.lua to be loaded first in your scripts. Many functions build upon
-- | dfunc's base functionality. Always use require("dfunc") and require("xafunc") in your automation scripts.
-- |
-- | XA Func Library v2.4
-- | Created by: https://github.com/xa-io
-- | Last Updated: 2025-12-30 20:20:00
-- |
-- | ## Release Notes ##
-- | v2.4 - Added GetPartyMemberNameXA(), GetPartyMemberRawX/Y/ZPosXA(), PvpMoveToXA()
-- |        Fixed pathing in FreshLimsaToSummer() after Niniya as vnav gets stucks on the table after a recent update
-- | v2.3 - Added EnablePluginXA(), DisablePluginXA(), EnablePluginCollectionXA(), DisablePluginCollectionXA()
-- | v2.2 - Fixed EnterHousingWardFromMenu(), added FreshGridaniaToBentbranch(), FreshGridaniaToBeds(), 
-- |        BentbranchToBeds()
-- | v2.1 - Added DebugXA(), TradeDebugXA(), ListDebugXA(), CheckPluginInstalledXA(), CheckPluginEnabledXA(),
-- |        CheckAnyPluginInstalledXA(), CheckAnyPluginEnabledXA(), ListAllPluginsXA(), ApplyFCPermissionsXA()
-- | v2.0 - Added IsInFreeCompanyXA(), LeaveFreeCompanyXA(), OpenInventoryXA()
-- | v1.9 - Added GetInverseBagmanCoordsXA()
-- | v1.8 - Improved OpenDropboxXA() as Limiana has added [/dropbox OpenTradeTab] to ensure we're on the item tab
-- | v1.7 - Improved OpenArmouryChestXA() to use slashcommand instead of CTRL + I, Removed CharacterSafeWaitXA() from
-- |        being used within the InteractXA() function as there are menu's that will appear in some cases.
-- | v1.6 - Added StartArtisanListXA(list_id), vnavXA()
-- | v1.5 - Improved ARRelogXA() and LifestreamCmdXA() to include more WaitForLifestreamXA()/CharacterSafeWaitXA()
-- |        so they're not needed after each command is used within a script.
-- | v1.4 - Added vbmarXA(), Updated GetSNDCoordsXA()
-- | v1.3 - Added ARDiscardXA(), WaitForARToFinishXA(), ARRelogXA(), FreeCompanyCmdXA(), vbmaiXA(), bmraiXA(), adXA(),
-- |        callbackXA(), SelectYesnoXA()
-- | v1.2 - Added OpenArmouryChestXA(), TargetXA(targetname), FocusTargetXA(), EnableArtisanXA(), DisableArtisanXA(),
-- |        CloseCraftingWindowsXA(), OpenDropboxXA(), LifestreamCmdXA()
-- | v1.1 - Added DismountXA(), WaitForLifestreamXA(), EnableARMultiXA(), DisableARMultiXA(), QSTStartXA(), QSTStopXA(), 
-- |        QSTReloadXA(), BTBInviteXA(), BTBDisbandXA()
-- | v1.0 - Initial release
-- └-----------------------------------------------------------------------------------------------------------------------
-- ┌---------------------------------------------------------------------------
-- | QUICK REFERENCE GUIDE
-- |---------------------------------------------------------------------------
-- | 
-- | Usage: Add these lines at the start of your scripts:
-- |   require("dfunc")
-- |   require("xafunc")
-- |
-- | Dependencies:
-- |   - dfunc (required)   - https://github.com/McVaxius/dhogsbreakfeast/blob/main/dfunc.lua
-- |   - xafunc (this file) - https://github.com/xa-io/ffxiv-tools/blob/main/snd/xafunc.lua
-- |
-- | Can add the lua scripts manually in SND or use the github auto updating function.
-- | The SND scripts will just be named dfunc and xafunc
-- |
-- |---------------------------------------------------------------------------
-- | FUNCTION CATEGORIES
-- |---------------------------------------------------------------------------
-- | 
-- | Misc Things
-- |---------------------------------------------------------------------------
-- | EchoXA(text)                   -- Usage: EchoXA("Hello World In Echo Chat")
-- | DebugXA(message)               -- Usage: DebugXA("Debug message") - Requires debug_mode = true
-- | TradeDebugXA(message)          -- Usage: TradeDebugXA("Trade message") - Requires tradedebug_mode = true
-- | ListDebugXA(message)           -- Usage: ListDebugXA("List message") - Requires listdebug_mode = true
-- | SleepXA(time)                  -- Usage: SleepXA(5) -- Will use /wait 5
-- | TargetXA(targetname)           -- Usage: TargetXA("Player'or NPC-name")
-- | FocusTargetXA()                -- Usage: FocusTargetXA()
-- | vbmaiXA(text)                  -- Usage: vbmaiXA("on")
-- | vbmarXA()                      -- Usage: vbmarXA("disable")
-- | bmraiXA(text)                  -- Usage: bmraiXA("on")
-- | rsrXA(text)                    -- Usage: rsrXA("manual")
-- | adXA(text)                     -- Usage: adXA("stop")
-- | vnavXA(text)                   -- Usage: vnavXA("stop")
-- | gaXA(text)                     -- Usage: gaXA("Sprint")
-- | callbackXA(text)               -- Usage: callbackXA("SelectYesno true 0")
-- | SelectYesnoXA()                -- Selects Yes if there is a popup
-- | DidWeLoadcorrectlyXA()         -- Verification function to confirm xafunc loaded successfully
-- | 
-- | Plugin Things
-- |---------------------------------------------------------------------------
-- | IsEnabledXA(name)              -- Check if a plugin is installed AND enabled - Usage: if IsEnabledXA("RotationSolver") then ... end
-- | AutoRetainerIsBusyXA()         -- Check if AutoRetainer is currently processing
-- | WaitForARToFinishXA()          -- Wait for AutoRetainerIsBusyXA()
-- | CheckPluginInstalledXA()       -- ALL plugin(s) must be installed - Usage: if not CheckPluginInstalledXA({"P1", "P2", "P3"}) then return end
-- | CheckPluginEnabledXA()         -- ALL plugin(s) must be enabled - Usage: if not CheckPluginEnabledXA({"P1", "P2", "P3"}) then return end
-- | CheckAnyPluginInstalledXA()    -- At least ONE plugin must be installed - Usage: if not CheckAnyPluginInstalledXA({"P1", "P2"}) then return end
-- | CheckAnyPluginEnabledXA()      -- At least ONE plugin must be enabled - Usage: if not CheckAnyPluginEnabledXA({"P1", "P2"}) then return end
-- | ListAllPluginsXA()             -- List all installed plugins with [✓]/[✗] status
-- | EnableSimpleTweaksXA()         -- Enable recommended SimpleTweaks settings (FixTarget, DisableTitleScreen, etc.)
-- | WaitForLifestreamXA()          -- Wait for Lifestream to process
-- | ARRelogXA(name)                -- Runs /ays relog, Usage: ARRelogXA("Toon Name@World")
-- | EnableARMultiXA()              -- Enable AutoRetainer Multi Mode
-- | DisableARMultiXA()             -- Disable AutoRetainer Multi Mode
-- | ARDiscardXA()                  -- Discard items and wait for AR to finish
-- | LogoutXA()                     -- Logout with Yes confirmation
-- | QSTStartXA()                   -- Start Questionable
-- | QSTStopXA()                    -- Stop Questionable
-- | QSTReloadXA()                  -- Reload Questionable
-- | EnableTextAdvanceXA()          -- Enable TextAdvance
-- | DisableTextAdvanceXA()         -- Disable TextAdvance
-- | EnablePluginXA()               -- Enable a specific plugin - Usage: EnablePluginXA("Artisan")
-- | DisablePluginXA()              -- Disable a specific plugin - Usage: DisablePluginXA("Artisan")
-- | EnablePluginCollectionXA()     -- Enable a specific plugin collection - Usage: EnablePluginCollectionXA("Artisan")
-- | DisablePluginCollectionXA()    -- Disable a specific plugin collection - Usage: DisablePluginCollectionXA("Artisan")
-- | 
-- | World Info
-- |---------------------------------------------------------------------------
-- | GetSNDCoords()                 -- Gets the coords in two formats (space and comma separated)
-- | GetSNDCoordsXA()               -- Gets the coords with specificed usage listed above
-- | GetInverseBagmanCoordsXA()     -- Gets the coords for Inverse Bagman for easy copy paste
-- | RemoveSproutXA()               -- Remove New Adventurer Status
-- | GetLevelXA(pjob)               -- Get current job level - Usage: GetLevelXA() or GetLevelXA(9000)
-- | GetZoneIDXA()                  -- Get current Zone/Territory ID
-- | GetZoneNameXA()                -- Get current Zone/Territory Name
-- | GetWorldNameXA()               -- Get current World Name with ID
-- | GetPlayerNameXA()              -- Get Player Name
-- | GetPlayerNameAndWorldXA()      -- Get Player Name@World format
-- | FreeCompanyCmdXA()             -- Opens FC Window so AR can collect data
-- | IsInFreeCompanyXA()            -- Check if player is currently in a Free Company
-- | IsInFreeCompanyResultsXA()     -- Check FC status with detailed debug output
-- | ApplyFCPermissionsXA()         -- Apply Free Company member rank permissions (requires rank 6+)
-- | LeaveFreeCompanyXA()           -- Leave the current Free Company
-- |
-- | Party Commands
-- |---------------------------------------------------------------------------
-- | EnableBTBandInviteXA()         -- Enable BardToolbox, send mass party invite, then disable
-- | BTBInviteXA()                  -- Send out BardToolbox invite
-- | BTBDisbandXA()                 -- Send out BardToolbox disband and /leave to double check
-- | IsInPartyXA()                  -- Check if player is currently in a party
-- | PartyInviteXA(name)            -- Invite player to party by targeting them - Usage: PartyInviteXA("First Last")
-- | PartyInviteMenuXA(first,full)  -- Invite player via social menu - Usage: PartyInviteMenuXA("First", "First Last")
-- | PartyDisbandXA()               -- Disband current party
-- | PartyAcceptXA()                -- Accept party invitation
-- | PartyLeaveXA()                 -- Leave current party
-- | GetPartyMemberRawXPosXA(index) -- Get party member raw X position by index (0-7) - Usage: GetPartyMemberRawXPosXA(0)
-- | GetPartyMemberRawYPosXA(index) -- Get party member raw Y position by index (0-7) - Usage: GetPartyMemberRawYPosXA(0)
-- | GetPartyMemberRawZPosXA(index) -- Get party member raw Z position by index (0-7) - Usage: GetPartyMemberRawZPosXA(0)
-- | OpenInventoryXA()              -- Opens Inventory
-- | OpenArmouryChestXA()           -- Opens Armoury Chest
-- | OpenDropboxXA()                -- Opens Dropbox, then opens Item Trade Queue tab
-- | ClearDropboxXA()               -- Clears the Dropbox queue
-- | EnableSprintingInTownXA()      -- Enable auto-sprint in sanctuaries via Pandora
-- | DisableSprintingInTownXA()     -- Disable auto-sprint in sanctuaries via Pandora
-- | 
-- | Movement Commands
-- |---------------------------------------------------------------------------
-- | FullStopMovementXA()           -- Force stop all movement (visland, vnav, automove)
-- | WalkThroughDottedWallXA()      -- Hold W for 2 seconds to pass through dotted walls
-- | CharacterSafeWaitXA()          -- Comprehensive safewait using IsPlayerAvailableXA() & PlayerAndUIReadyXA() 
-- | DoNavFlySequenceXA()           -- Navigate to flag position with automatic fly/move selection
-- | MountUpXA()                    -- Automatic mounting with mount roulette when conditions allow
-- | DismountXA()                   -- Repeat casting /mount until dismounted and Svc.Condition[1] is met
-- | MovingCheaterXA()              -- Advanced movement using PlayerAndUIReadyXA() & MountUpXA() & DoNavFlySequenceXA()
-- | IsBusyXA()                     -- Check if player is busy with various activities
-- | IsPlayerCastingXA()            -- Check if player is currently casting
-- | IsPlayerAvailableXA()          -- Helper: Check if player is available (not casting, not zoning)
-- | PlayerAndUIReadyXA()           -- Helper: Check if NamePlate ready and player available
-- | GetPartyMemberNameXA(index)    -- Get party member name by index (0-7) - Usage: GetPartyMemberNameXA(0)
-- | WaitUntil(cond, timeout, step) -- Helper: Wait until condition is true or timeout - Usage: WaitUntil(function, 10, 0.2)
-- | return_to_fcXA()               -- Lifestream teleport to FC house with auto-entry
-- | return_to_homeXA()             -- Lifestream teleport to personal house with auto-entry
-- | return_to_autoXA()             -- Lifestream teleport to select using auto list configuration
-- | return_to_homeworldXA()        -- Lifestream teleport back to your homeworld
-- | RunToHomeGCXA()                -- Lifestream teleport to home Grand Company
-- | EnableDeliverooXA()            -- Enable Deliveroo plugin for GC turn-ins
-- | LifestreamCmdXA(name)          -- Replacement for yield("/li Limsa") - Usage: LifestreamCmdXA("Limsa")
-- | GetDistanceToPoint(x,y,z)      -- Calculate distance to target coordinates - Usage: GetDistanceToPoint(-12.123, 45.454, -18.5456)
-- | MoveToXA(x,y,z)                -- Fly/Run to coordinates with pathing - Usage: MoveToXA(-12.123, 45.454, -18.5456)
-- | PvpMoveToXA(x,y,z)             -- PvP-safe movement that waits for casting to finish - Usage: PvpMoveToXA(-12.123, 45.454, -18.5456)
-- | WalkToTargetXA(x,y,z,dist)     -- Walk (no mount) to coordinates, stop at distance - Usage: WalkToTargetXA(-12.123, 45.454, -18.5456, 3.0)
-- | get_coordinates(coords)        -- Helper: Extract coordinates from table
-- | log_coordinates(coords)        -- Helper: Log coordinates to echo chat
-- | move_to(coords)                -- Move to single coord or array of coords - Usage: move_to({x, y, z}) or move_to({{x1,y1,z1}, {x2,y2,z2}})
-- |
-- | Player Commands
-- |---------------------------------------------------------------------------
-- | InteractXA()                   -- Interact with selected target
-- | ResetCameraXA()                -- Reset camera position using END key
-- | EquipRecommendedGearXA()       -- Equip recommended gear via Character menu callbacks
-- | EquipRecommendedGearCmdXA()    -- Equip recommended gear via SimpleTweaks /equiprecommended command
-- | EnableArtisanXA()              -- Enable plugin collections named Artisan
-- | DisableArtisanXA()             -- Disable plugin collections named Artisan
-- | StartArtisanListXA(list_id)    -- Start's processing an Artisan List - Usage: StartArtisanListXA(1234)
-- | CloseCraftingWindowsXA()       -- Close all crafting windows
-- | MonitorJobLevelArtisanXA(lvl)  -- Monitor job level and stop Artisan when reached - Usage: MonitorJobLevelArtisanXA(25)
-- | 
-- | Braindead Functions
-- |---------------------------------------------------------------------------
-- | EnterHousingWardFromMenu()     -- Navigate housing ward selection menu
-- | SetNewbieCamera()              -- Set camera to comfortable position for new characters
-- | ImNotNewbStopWatching()        -- Remove sprout, enable text advance, set camera
-- | FreshLimsaToSummer()           -- Complete Limsa intro sequence and travel to Summerford Farms
-- | FreshLimsaToMist()             -- Complete Limsa intro sequence and travel to Summerford Farms, then to Mist housing district
-- | SummerToMist()                 -- Travel from Summerford Farms to Mist housing district
-- | FreshUldahToHorizon()          -- Complete Ul'dah intro sequence and travel to Horizon
-- | FreshUldahToGoblet()           -- Complete Ul'dah intro sequence and travel to Horizon, then Goblet housing district
-- | HorizonToGoblet()              -- Travel from Horizon to Goblet housing district
-- | FreshGridaniaToBentbranch()    -- Complete Gridania intro sequence and travel to Bentbranch Meadows
-- | FreshGridaniaToBeds()          -- Complete Gridania intro sequence and travel to Bentbranch Meadows, then Lavender Beds housing district
-- | BentbranchToBeds()             -- Travel from Bentbranch Meadows to Lavender Beds housing district
-- └---------------------------------------------------------------------------

-- ------------------------
-- Misc Things
-- ------------------------

function EchoXA(text) -- Usage: EchoXA("Hello World In Echo Chat")
    yield("/echo " .. tostring(text))
end

function DebugXA(message) -- Usage: DebugXA("Debug message")
    if debug_mode then
        EchoXA(string.format("[Debug] %s", tostring(message)))
    end
end

function TradeDebugXA(message) -- Usage: TradeDebugXA("Trade message")
    if tradedebug_mode then
        EchoXA(string.format("[Trade] %s", tostring(message)))
    end
end

function ListDebugXA(message) -- Usage: ListDebug("List message")
    if listdebug_mode then
        EchoXA(string.format("[List] %s", tostring(message)))
    end
end

function SleepXA(time) -- Usage: SleepXA(5) -- Will use /wait 5
    yield("/wait " .. tostring(time))
end

function TargetXA(targetname) -- Usage: TargetXA("Player'or NPC-name")
    yield("/target \"" .. tostring(targetname) .. "\"")
end

function FocusTargetXA() -- Usage: FocusTargetXA()
    yield("/focustarget")
    SleepXA(0.07)
end

function vbmaiXA(text) -- Usage: vbmaiXA("on")
    if IsEnabledXA("BossMod") then
        yield("/vbmai " .. tostring(text))
    end
end

function vbmarXA(text)  -- Usage: vbmarXA("disable")
    if IsEnabledXA("BossMod") then
        yield("/vbm ar " .. tostring(text))
    end
end

function bmraiXA(text) -- Usage: bmraiXA("on")
    if IsEnabledXA("BossModReborn") then
        yield("/bmrai " .. tostring(text))
    end
end

function rsrXA(text) -- Usage: rsrXA("manual")
    if IsEnabledXA("RotationSolver") then
        yield("/rsr " .. tostring(text))
    end
end

function adXA(text) -- Usage: adXA("stop")
    if IsEnabledXA("AutoDuty") then
        yield("/ad " .. tostring(text))
    end
end

function vnavXA(text) -- Usage: vnavXA("stop")
    if IsEnabledXA("vnavmesh") then
        yield("/vnav " .. tostring(text))
    end
end

function gaXA(text) -- Usage: gaXA("Sprint")
    yield("/gaction " .. tostring(text))
end

function callbackXA(text) -- Usage: callbackXA("SelectYesno true 0")
    yield("/callback " .. tostring(text))
end

function SelectYesnoXA()
    SleepXA(1.5)
    if IsAddonReady("SelectYesno") then callbackXA("SelectYesno true 0") end
end

function DidWeLoadcorrectlyXA()
	EchoXA("XA functions file read successfully!")
end

-- ------------------------
-- Plugin Things
-- ------------------------

function IsEnabledXA(name)
    -- Check if a plugin is installed AND enabled
    -- Usage: if IsEnabledXA("RotationSolver") then ... end
    for plugin in luanet.each(Svc.PluginInterface.InstalledPlugins) do
        if plugin.InternalName == name then
            return plugin.IsLoaded
        end
    end
    return false
end

function AutoRetainerIsBusyXA()
    return IPC.AutoRetainer.IsBusy()
end

function WaitForARToFinishXA()
    repeat
        SleepXA(1)
    until not AutoRetainerIsBusyXA()
end

function CheckPluginInstalledXA(nameOrList)
    -- Check if plugin(s) are installed - halts script if not installed
    -- Does NOT check if enabled - only installation status
    -- Usage: if not CheckPluginInstalledXA("Lifestream") then return end
    -- Usage: if not CheckPluginInstalledXA({"Lifestream", "AutoRetainer", "Dropbox"}) then return end

    -- Convert single string to table for uniform processing
    local pluginNames = type(nameOrList) == "table" and nameOrList or {nameOrList}

    -- Check each plugin
    for _, name in ipairs(pluginNames) do
        local isInstalled = false

        for plugin in luanet.each(Svc.PluginInterface.InstalledPlugins) do
            if plugin.InternalName == name then
                isInstalled = true
                break
            end
        end

        -- Halt script if plugin is not installed
        if not isInstalled then
            EchoXA("[✗] Plugin '" .. name .. "' is NOT INSTALLED")
            EchoXA("[✗] Script stopped - please install required plugin!")
            EchoXA("[ERROR] Missing plugin: " .. name)
            EchoXA("Plugin '" .. name .. "' not installed - script halted")
            return false
        end
    end

    -- All plugins are installed - silently continue (no spam)
    -- Uncomment below if you want confirmation messages:
    -- if #pluginNames == 1 then
    --     EchoXA("[✓] Plugin '" .. pluginNames[1] .. "' is installed")
    -- else
    --     EchoXA("[✓] All " .. #pluginNames .. " plugins are installed")
    -- end
    return true
end

function CheckPluginEnabledXA(nameOrList)
    -- Check if plugin(s) are installed AND enabled - halts script if not
    -- Usage: if not CheckPluginEnabledXA("Lifestream") then return end
    -- Usage: if not CheckPluginEnabledXA({"Lifestream", "AutoRetainer", "Dropbox"}) then return end

    -- Convert single string to table for uniform processing
    local pluginNames = type(nameOrList) == "table" and nameOrList or {nameOrList}

    -- Check each plugin
    for _, name in ipairs(pluginNames) do
        local isInstalled = false
        local isEnabled = false

        for plugin in luanet.each(Svc.PluginInterface.InstalledPlugins) do
            if plugin.InternalName == name then
                isInstalled = true
                -- Check if plugin is enabled (IsLoaded property indicates enabled status)
                if plugin.IsLoaded then
                    isEnabled = true
                end
                break
            end
        end

        -- Halt script if plugin is not installed or not enabled
        if not isInstalled then
            EchoXA("[✗] Plugin '" .. name .. "' is NOT INSTALLED")
            EchoXA("[✗] Script stopped - please install required plugin!")
            EchoXA("[ERROR] Missing plugin: " .. name)
            EchoXA("Plugin '" .. name .. "' not installed - script halted")
            return false
        end

        if not isEnabled then
            EchoXA("[✗] Plugin '" .. name .. "' is DISABLED")
            EchoXA("[✗] Script stopped - please enable required plugin!")
            EchoXA("[ERROR] Disabled plugin: " .. name)
            EchoXA("Plugin '" .. name .. "' not enabled - script halted")
            return false
        end
    end

    -- All plugins are ready - silently continue (no spam)
    -- Uncomment below if you want confirmation messages:
    -- if #pluginNames == 1 then
    --     EchoXA("[✓] Plugin '" .. pluginNames[1] .. "' is ready")
    -- else
    --     EchoXA("[✓] All " .. #pluginNames .. " plugins are ready")
    -- end
    return true
end

function CheckAnyPluginInstalledXA(pluginNames)
    -- Check if at least one plugin from list is installed
    -- Usage: if not CheckAnyPluginInstalledXA({"BossMod", "BossModReborn", "RotationSolver"}) then return end
    local foundAny = false
    local foundPlugins = {}

    for plugin in luanet.each(Svc.PluginInterface.InstalledPlugins) do
        for _, name in ipairs(pluginNames) do
            if plugin.InternalName == name then
                foundAny = true
                table.insert(foundPlugins, name)
            end
        end
    end

    if not foundAny then
        EchoXA("[✗] At least one of these plugins must be installed:")
        for _, name in ipairs(pluginNames) do
            EchoXA("    - " .. name)
        end
        EchoXA("[ERROR] No required plugins found - script halted")
        return false
    end

    -- Show which plugin(s) were found
    if #foundPlugins > 0 then
        EchoXA("[✓] Found plugin(s): " .. table.concat(foundPlugins, ", "))
    end

    return true
end

function CheckAnyPluginEnabledXA(pluginNames)
    -- Check if at least one plugin from list is installed AND enabled
    -- Usage: if not CheckAnyPluginEnabledXA({"BossMod", "BossModReborn", "RotationSolver"}) then return end
    local foundAny = false
    local foundPlugins = {}

    for plugin in luanet.each(Svc.PluginInterface.InstalledPlugins) do
        for _, name in ipairs(pluginNames) do
            if plugin.InternalName == name and plugin.IsLoaded then
                foundAny = true
                table.insert(foundPlugins, name)
            end
        end
    end

    if not foundAny then
        EchoXA("[✗] At least one of these plugins must be installed AND enabled:")
        for _, name in ipairs(pluginNames) do
            EchoXA("    - " .. name)
        end
        EchoXA("[ERROR] No required plugins are enabled - script halted")
        return false
    end

    -- Show which plugin(s) were found
    if #foundPlugins > 0 then
        EchoXA("[✓] Found enabled plugin(s): " .. table.concat(foundPlugins, ", "))
    end

    return true
end

function ListAllPluginsXA()
    -- List all installed plugins with enabled/disabled status
    -- Usage: ListAllPluginsXA()
    local pluginList = {}
    local enabledCount = 0
    local disabledCount = 0

    -- Collect all plugins
    for plugin in luanet.each(Svc.PluginInterface.InstalledPlugins) do
        local status = plugin.IsLoaded
        table.insert(pluginList, {
            name = plugin.InternalName,
            enabled = status
        })
        if status then
            enabledCount = enabledCount + 1
        else
            disabledCount = disabledCount + 1
        end
    end

    -- Sort alphabetically by name
    table.sort(pluginList, function(a, b) return a.name < b.name end)

    -- Display header
    EchoXA("==================================")
    EchoXA("ALL INSTALLED PLUGINS")
    EchoXA("==================================")

    -- Display each plugin
    for _, plugin in ipairs(pluginList) do
        if plugin.enabled then
            EchoXA("[✓] " .. plugin.name)
        else
            EchoXA("[✗] " .. plugin.name)
        end
    end

    -- Display summary
    EchoXA("==================================")
    EchoXA("Total: " .. #pluginList .. " plugins")
    EchoXA("Enabled: " .. enabledCount .. " | Disabled: " .. disabledCount)
    EchoXA("==================================")
end

function EnableSimpleTweaksXA()
    if IsEnabledXA("SimpleTweaksPlugin") then
        yield("/tweaks enable FixTarget")
        yield("/tweaks enable DisableTitleScreenMovie")
        yield("/tweaks enable EquipJobCommand")
        yield("/tweaks enable RecommendEquipCommand")
        EchoXA("SimpleTweaks has been adjusted.")
    else
        EchoXA("SimpleTweaksPlugin is not installed or enabled.")
    end
end

function WaitForLifestreamXA()
	xakonds = 0
    EchoXA("Waiting on lifestream")
	while IPC.Lifestream.IsBusy() do
		--DEBUG
		-- EchoXA("Waiting on lifestream -> "..sekonds)
		xakonds = xakonds + 1
		SleepXA(1)
	end
    EchoXA("Lifestream completed")
end

function ARRelogXA(name)
    local who = (type(name) == "string") and name:match('^%s*(.-)%s*$') or ""
    -- strip accidental wrapping quotes if caller included them
    who = who:gsub('^"(.*)"$', '%1'):gsub("^'(.*)'$", "%1")

    if who == "" then
        EchoXA("ARRelogXA: No character provided.")
        return false
    end

    EchoXA("Logging into " .. who)
    yield("/ays relog " .. who)
    SleepXA(1)
    WaitForARToFinishXA()
    CharacterSafeWaitXA()
    SleepXA(1.01)
    CharacterSafeWaitXA()
    SleepXA(1.02)
    CharacterSafeWaitXA()
    SleepXA(1.03)
    CharacterSafeWaitXA()
    SleepXA(1.04)
    return true
end

function LogoutXA()
    yield("/logout")
    SleepXA(1)
    SelectYesnoXA()
    SleepXA(1)
end

function EnableARMultiXA()
    if IsEnabledXA("AutoRetainer") then
        yield("/ays multi e")
    end
end

function DisableARMultiXA()
    if IsEnabledXA("AutoRetainer") then
        yield("/ays multi d")
    end
end

function ARDiscardXA()
    if IsEnabledXA("AutoRetainer") then
        yield("/ays discard")
        while AutoRetainerIsBusyXA() do
            SleepXA(1)
        end
        return true
    end
    return false
end

function QSTStartXA()
    if IsEnabledXA("Questionable") then
        SleepXA(1)
        yield("/qst start")
        SleepXA(2)
    end
end

function QSTStopXA()
    if IsEnabledXA("Questionable") then
        SleepXA(1)
        yield("/qst stop")
        SleepXA(2)
    end
end

function QSTReloadXA()
    if IsEnabledXA("Questionable") then
        SleepXA(1)
        yield("/qst reload")
        SleepXA(2)
    end
end

function EnableTextAdvanceXA()
    if IsEnabledXA("TextAdvance") then
        yield("/at y")
        EchoXA("Enabling Text Advance...")
    end
end

function DisableTextAdvanceXA()
    if IsEnabledXA("TextAdvance") then
        yield("/at n")
        EchoXA("Disabling Text Advance...")
    end
end

-- Usage: EnablePluginXA("Artisan")
function EnablePluginXA(plugin_name)
    yield("/xlenableplugin " .. plugin_name)
    EchoXA("Enabled Plugin " .. plugin_name)
    SleepXA(3)
end

-- Usage: DisablePluginXA("Artisan")
function DisablePluginXA(plugin_name)
    yield("/xldisableplugin " .. plugin_name)
    EchoXA("Disabled Plugin " .. plugin_name)
    SleepXA(3)
end

-- Usage: EnablePluginCollectionXA("Artisan")
function EnablePluginCollectionXA(collection_name)
    yield("/xlenableprofile " .. collection_name)
    EchoXA("Enabled Collection " .. collection_name)
    SleepXA(3)
end

-- Usage: DisablePluginCollectionXA("Artisan")
function DisablePluginCollectionXA(collection_name)
    yield("/xldisableprofile " .. collection_name)
    EchoXA("Disabled Collection " .. collection_name)
    SleepXA(3)
end

-- ------------------------
-- World Info
-- ------------------------

function GetSNDCoords()
    SleepXA(0.1)
    Engines.Native.Run ("/e " .. Entity.Player.Position.X .. " " .. Entity.Player.Position.Y .. " " .. Entity.Player.Position.Z)
    SleepXA(0.1)
    Engines.Native.Run ("/e " .. Entity.Player.Position.X .. ", " .. Entity.Player.Position.Y .. ", " .. Entity.Player.Position.Z)
    SleepXA(0.1)
end

function GetSNDCoordsXA()
    local p = Entity and Entity.Player and Entity.Player.Position
    if not p then
        EchoXA("Coords unavailable.")
        return
    end
    local x, y, z = tostring(p.X), tostring(p.Y), tostring(p.Z)

    SleepXA(0.1)
    EchoXA("/vnav moveto " .. x .. " " .. y .. " " .. z)
    SleepXA(0.1)
    EchoXA("MoveToXA(" .. x .. ", " .. y .. ", " .. z .. ")")
    SleepXA(0.1)
    EchoXA("local tony_x = " .. x)
    SleepXA(0.1)
    EchoXA("local tony_y = " .. y)
    SleepXA(0.1)
    EchoXA("local tony_z = " .. z)
    SleepXA(0.1)
end

function GetInverseBagmanCoordsXA()
    local p = Entity and Entity.Player and Entity.Player.Position
    if not p then
        EchoXA("Coords unavailable.")
        return
    end
    local x, y, z = tostring(p.X), tostring(p.Y), tostring(p.Z)

    SleepXA(0.1)
    EchoXA("local tony_x = " .. x)
    SleepXA(0.1)
    EchoXA("local tony_y = " .. y)
    SleepXA(0.1)
    EchoXA("local tony_z = " .. z)
    SleepXA(0.1)
end

function RemoveSproutXA()
    yield("/nastatus off")
    EchoXA("Removing New Adventurer Status...")
end

function GetLevelXA(pjob)
    pjob = pjob or 9000
    local lvl

    -- try your GetLevel() first
    if type(GetLevel) == "function" then
        local ok, v = pcall(GetLevel, pjob)
        if ok then lvl = v end
    end

    -- fallback if needed
    if lvl == nil then
        if pjob < 9000 and Player and Player.GetJob then
            local ok, v = pcall(function() return Player.GetJob(pjob + 1).Level end)
            if ok then lvl = v end
        elseif Player and Player.Job then
            lvl = Player.Job.Level
        end
    end

    lvl = tonumber(lvl) or "?"
    EchoXA("Level: " .. tostring(lvl))
    return lvl
end

function GetZoneIDXA()
    if Svc and Svc.ClientState and Svc.ClientState.TerritoryType then
        local zone_id = Svc.ClientState.TerritoryType
        EchoXA("Zone ID: " .. zone_id)
        return zone_id
    else
        EchoXA("Error: Zone data not available")
        return nil
    end
end

function GetZoneNameXA()
    local id = (Svc and Svc.ClientState and Svc.ClientState.TerritoryType) or nil
    local name

    if Excel and id then
        local row = Excel.GetRow("TerritoryType", id)
        if row then
            -- check with dot, call with colon
            local place = (row.GetProperty and row:GetProperty("PlaceName")) or nil
            name = place and (place.Name or place.Singular)
            if name and type(name) ~= "string" and name.ToString then
                name = name:ToString()
            end
        end
    end

    if not name or name == "" then name = tostring(id or "?") end
    EchoXA("Zone: " .. tostring(name) .. " [" .. tostring(id or "?") .. "]")
    return name, id
end

function GetWorldNameXA()
    local id = (Player and Player.Entity and Player.Entity.CurrentWorld) or nil
    local name = (homeworld_lookup and id and homeworld_lookup[id])
    if not name or name == "" then name = tostring(id or "?") end
    EchoXA("World: " .. name .. " [" .. tostring(id or "?") .. "]")
    return name, id
end

function GetPlayerNameXA()
    if Entity and Entity.Player and Entity.Player.Name then
        local player_name = Entity.Player.Name
        EchoXA(player_name)
        return player_name
    else
        EchoXA("Error: Player data not available")
        return nil
    end
end

function GetPlayerNameAndWorldXA()
    if Entity and Entity.Player and Entity.Player.Name and Entity.Player.HomeWorld then
        local player_name = Entity.Player.Name
        local world_id = Entity.Player.HomeWorld
        local world_name = homeworld_lookup[world_id] or "Unknown World"
        local full_name = player_name .. "@" .. world_name
        EchoXA(full_name)
        return full_name
    else
        EchoXA("Error: Player data not available")
        return nil
    end
end

function FreeCompanyCmdXA()
    yield("/freecompanycmd")
    SleepXA(1)
end

function IsInFreeCompanyXA()
    -- thx kryssx
    local fc_gc = Player.FreeCompany.GrandCompany
    local fc_name = Player.FreeCompany.Name
    local fc_rank = Player.FreeCompany.Rank

    if fc_gc == "None" or fc_gc == nil or fc_gc == "" then
        return false
    end

    if fc_name == nil or fc_name == "" then
        return false
    end

    if fc_rank == 0 then
        return false
    end

    return true
end

function IsInFreeCompanyResultsXA()
    -- thx kryssx
    local fc_gc = Player.FreeCompany.GrandCompany
    local fc_name = Player.FreeCompany.Name
    local fc_rank = Player.FreeCompany.Rank

    EchoXA("---- Free Company Check ----")
    EchoXA("Grand Company: " .. tostring(fc_gc or "nil"))
    EchoXA("FC Name: " .. tostring(fc_name or "nil"))
    EchoXA("FC Rank: " .. tostring(fc_rank or "nil"))

    if fc_gc == "None" or fc_gc == nil or fc_gc == "" then
        EchoXA("[✗] Not in a Grand Company (None or nil)")
        return false
    end

    if fc_name == nil or fc_name == "" then
        EchoXA("[✗] No Free Company name detected")
        return false
    end

    if fc_rank == 0 then
        EchoXA("[✗] Free Company rank is 0")
        return false
    end

    EchoXA("[✓] Player is in a Free Company!")
    EchoXA("------------------------------")
    return true
end

function ApplyFCPermissionsXA()
    zungazunga()
    FreeCompanyCmdXA()
    SleepXA(0.1)
    callbackXA("FreeCompany true 0 2")
    SleepXA(0.3)
    callbackXA("FreeCompanyRank true 2 2 Undefined Undefined Undefined")
    callbackXA("FreeCompanyRank true 4 3 1513 557 Undefined")
    callbackXA("FreeCompanyRank true 3 2 Undefined Undefined Undefined")
    SleepXA(0.1)
    callbackXA("ContextMenu true 0 0 0 Undefined Undefined")
    SleepXA(0.1)
    callbackXA("FreeCompanyMemberRankEdit true 0 Undefined 1 1 1 1 1 1 1 1 1 1 1 1 3 1 1 1 1 1 3 1 1 1 1 1 1 1 1 -1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 -1 1 1 1")
    SleepXA(0.5)
    EchoXA("FC permissions applied successfully")
    zungazunga()
end

function LeaveFreeCompanyXA()
    EchoXA("Opening Free Company menu to leave...")

    -- Open the FC menu
    yield("/freecompanycmd")
    SleepXA(2)

    -- Navigate to the Info tab
    callbackXA("FreeCompany false 0 5u")
    SleepXA(2)

    -- Click Leave FC button
    EchoXA("Leaving Free Company...")
    callbackXA("FreeCompanyStatus true 3")
    SleepXA(2)

    -- Confirm the leave action with SelectYesno
    EchoXA("Successfully left Free Company...")
    SelectYesnoXA()

    -- Leave the party as well
    yield("/leave")
    SleepXA(1)
    SelectYesnoXA()
end

-- ------------------------
-- Party Commands
-- ------------------------

function EnableBTBandInviteXA()
    yield("/xlenableprofile BTB")
    EchoXA("BTB collection enabled. Waiting 8 seconds.")
    SleepXA(8)
    BTBInviteXA()
    EchoXA("BTB Invite has been sent. Waiting 3 seconds.")
    SleepXA(3)
    yield("/xldisableprofile BTB")
    EchoXA("BTB collection disabled. Waiting 3 seconds.")
    SleepXA(3)
end

function BTBInviteXA()
    if IsEnabledXA("BardToolbox") then
        yield("/btb disband")
        SleepXA(2)
        yield("/btb invite")
        SleepXA(1)
    end
end

function BTBDisbandXA()
    if IsEnabledXA("BardToolbox") then
        yield("/btb disband")
        SleepXA(2)
        yield("/pcmd breakup")
        SleepXA(1)
        SelectYesnoXA()
        SleepXA(1)
        yield("/leave")
        SleepXA(1)
        SelectYesnoXA()
        SleepXA(1)
    end
end

function OpenInventoryXA()
    yield("/inventory")
    SleepXA(0.07)
end

function OpenArmouryChestXA()
    yield("/armourychest")
    SleepXA(0.07)
end

function OpenDropboxXA()
    if IsEnabledXA("Dropbox") then
        yield("/dropbox")
        SleepXA(0.5)
        yield("/dropbox OpenTradeTab")
        SleepXA(0.5)
    end
end

-- function AcceptDropboxTradesXA()
-- end

-- function RefuseDropboxTradesXA()
-- end

function ClearDropboxXA()
    if IsEnabledXA("KitchenSink") then
        SleepXA(0.2)
        yield("/dbq clear")
        SleepXA(0.3)
    end
end

function EnableSprintingInTownXA()
    PandoraSetFeatureState("Auto-Sprint in Sanctuaries",true)
end

function DisableSprintingInTownXA()
    PandoraSetFeatureState("Auto-Sprint in Sanctuaries",false)
end

function IsInPartyXA()
    return GetPartyMemberNameXA(0) ~= nil and GetPartyMemberNameXA(0) ~= "" and not GetCharacterCondition(45)
end

-- Usage: PartyInvite("First Last")
-- Will target and invite player to a party, and retrying if the invite timeout happens
-- Can only be used if target is in range
function PartyInviteXA(party_invite_name)
    local invite_timeout = 305   -- 300 Seconds is the invite timeout, adding 5 seconds for good measure
    local start_time = os.time() -- Stores the invite time

    while not IsInPartyXA() do
        repeat
            SleepXA(0.1)
        until IsPlayerAvailableXA() and not IsPlayerCastingXA() and not GetCharacterCondition(26)

        TargetXA(party_invite_name)
        yield("/invite")

        -- Wait for the target player to accept the invite or the timeout to expire
        while not IsInPartyXA() do
            SleepXA(0.1)

            -- Check if the invite has expired
            if os.time() - start_time >= invite_timeout then
                Echo("Invite expired. Reinviting " .. party_invite_name)
                start_time = os.time() -- Reset the start time for the new invite
                break                  -- Break the loop to resend the invite
            end
        end
    end
    -- stuff could go here
end

-- Usage: PartyInviteMenu("First", "First Last")
-- Will invite player to a party through the social menu, and retrying if the invite timeout happens
-- Can be used from anywhere
-- Semi broken at the moment
function PartyInviteMenuXA(party_invite_menu_first, party_invite_menu_full)
    local invite_timeout = 305   -- 300 Seconds is the invite timeout, adding 5 seconds for good measure
    local start_time = os.time() -- Stores the invite time

    while not IsInPartyXA() do
        repeat
            SleepXA(0.1)
        until IsPlayerAvailableXA() and not IsPlayerCastingXA() and not GetCharacterCondition(26)

        repeat
            yield('/search first "' .. party_invite_menu_first .. '" en jp de fr')
            SleepXA(0.5)
        until IsAddonVisible("SocialList")

        -- Probably needs the node scanner here to match the name, otherwise it will invite whoever was previously searched, will probably mess up for multiple matches too

        repeat
            if IsAddonReady("SocialList") then
                callbackXA("SocialList true 1 0 '" .. party_invite_menu_full .. "'")
            end
            SleepXA(0.5)
        until IsAddonVisible("ContextMenu")

        repeat
            if IsAddonReady("ContextMenu") then
                callbackXA("ContextMenu true 0 3 0")
            end
            SleepXA(0.1)
        until not IsAddonVisible("ContextMenu")

        repeat
            if IsAddonReady("Social") then
                callbackXA("Social true -1")
            end
            SleepXA(0.1)
        until not IsAddonVisible("Social")

        -- Wait for the target player to accept the invite or the timeout to expire
        while not IsInPartyXA() do
            SleepXA(0.1)

            -- Check if the invite has expired
            if os.time() - start_time >= invite_timeout then
                Echo("Invite expired. Reinviting " .. party_invite_menu_full)
                start_time = os.time() -- Reset the start time for the new invite
                break                  -- Break the loop to resend the invite
            end
        end
    end
    -- stuff could go here
end

-- Usage: PartyDisband()
-- Will check if player is in party and disband party
function PartyDisbandXA()
    if IsInPartyXA() then
        repeat
            SleepXA(0.1)
        until IsPlayerAvailableXA() and not IsPlayerCastingXA() and not GetCharacterCondition(26)

        yield("/partycmd disband")

        for i=1, 50 do
            SleepXA(0.1)
            if IsAddonVisible("SelectYesno") then
                break
            end
        end
        repeat
            if IsAddonReady("SelectYesno") then callbackXA("SelectYesno true 0") end
            SleepXA(0.1)
        until not IsAddonVisible("SelectYesno")
    end
end

-- Usage: PartyAccept()
-- Will accept party invite if not in party
-- NEEDS a name arg
function PartyAcceptXA()
    if not IsInPartyXA() then
        -- Wait until the player is available, not casting, and not in combat
        repeat
            SleepXA(0.1)
        until IsPlayerAvailableXA() and not IsPlayerCastingXA() and not GetCharacterCondition(26)

        -- Wait until the "SelectYesno" addon is ready
        repeat
            SleepXA(0.1)
        until IsAddonReady("SelectYesno")

        SleepXA(0.1)

        -- Accept the party invite
        callbackXA("SelectYesno true 0")

        -- Wait until the player is in a party
        repeat
            SleepXA(0.1)
        until IsInPartyXA()

        EchoXA("Party invitation accepted.")
    else
        EchoXA("Player is already in a party.")
    end
end

-- Usage: PartyLeaveXA()
-- Will leave party if in a party
function PartyLeaveXA()
    if IsInPartyXA() then
        repeat
            SleepXA(0.1)
        until IsPlayerAvailableXA() and not IsPlayerCastingXA() and not GetCharacterCondition(26)

        yield("/partycmd leave")

        repeat
            SleepXA(0.1)
        until IsAddonVisible("SelectYesno")

        SleepXA(0.1)

        repeat
            if IsAddonReady("SelectYesno") then callbackXA("SelectYesno true 0") end
            SleepXA(0.1)
        until not IsAddonVisible("SelectYesno")

        EchoXA("Party has been left.")
    else
        EchoXA("Player is not in a party.")
    end
end

-- ------------------------
-- Movement Commands
-- ------------------------

function FullStopMovementXA()
    muuv = 1
    muuvstop = 0
    muuvX = EntityPlayerPositionX()
    muuvY = EntityPlayerPositionY()
    muuvZ = EntityPlayerPositionZ()
    while muuv == 1 do
        SleepXA(1.01)
        muuvstop = muuvstop + 1
        if muuvX == EntityPlayerPositionX() and muuvY == EntityPlayerPositionY() and muuvZ == EntityPlayerPositionZ() then
            muuv = 0
        end
        muuvX = EntityPlayerPositionX()
        muuvY = EntityPlayerPositionY()
        muuvZ = EntityPlayerPositionZ()
        if muuvstop > 50 then
            if math.abs(muuvX - EntityPlayerPositionX()) < 2 and math.abs(muuvY - EntityPlayerPositionY()) < 2 and math.abs(muuvZ - EntityPlayerPositionZ()) < 2 then
                muuv = 0
            end
        end
    end
    SleepXA(1.02)
    yield("/visland stop")
    vnavXA("stop")
    yield("/automove off")
    SleepXA(1.03)
end

function WalkThroughDottedWallXA()
    ResetCameraXA()
	yield("/hold W")
	SleepXA(2)
	yield("/release W")
	SleepXA(3)
end

--- Check if player is busy with various activities
function IsBusyXA()
    return Player.IsBusy or GetCharacterCondition(6) or GetCharacterCondition(26) or GetCharacterCondition(27) or
        GetCharacterCondition(43) or GetCharacterCondition(45) or GetCharacterCondition(51) or GetCharacterCondition(32) or
        not (GetCharacterCondition(1) or GetCharacterCondition(4))
end

--- Check if player is currently casting
function IsPlayerCastingXA()
    return Player.IsCasting
end

function IsPlayerDeadXA()
    if Svc and Svc.Condition then
        if type(Svc.Condition.IsDeath) == "function" then
            local ok, res = pcall(Svc.Condition.IsDeath, Svc.Condition)
            if ok then return res end
        end
        return Svc.Condition[2] == true
    end
    return false
end

-- Get party member name by index (0-7)
function GetPartyMemberNameXA(index)
    if Entity == nil or Entity.GetPartyMember == nil then return nil end
    local member = Entity.GetPartyMember(index)
    if member == nil then return nil end
    return member.Name
end

--- Get party member position functions using two-step lookup: GetPartyMember for name, GetEntityByName for position
function GetPartyMemberRawXPosXA(index)
    if Entity == nil or Entity.GetPartyMember == nil then return nil end
    local member = Entity.GetPartyMember(index)
    if member == nil or member.Name == nil then return nil end
    local entity = Entity.GetEntityByName(member.Name)
    if entity == nil or entity.Position == nil then return nil end
    return entity.Position.X
end

function GetPartyMemberRawYPosXA(index)
    if Entity == nil or Entity.GetPartyMember == nil then return nil end
    local member = Entity.GetPartyMember(index)
    if member == nil or member.Name == nil then return nil end
    local entity = Entity.GetEntityByName(member.Name)
    if entity == nil or entity.Position == nil then return nil end
    return entity.Position.Y
end

function GetPartyMemberRawZPosXA(index)
    if Entity == nil or Entity.GetPartyMember == nil then return nil end
    local member = Entity.GetPartyMember(index)
    if member == nil or member.Name == nil then return nil end
    local entity = Entity.GetEntityByName(member.Name)
    if entity == nil or entity.Position == nil then return nil end
    return entity.Position.Z
end

function IsPlayerAvailableXA()
    if not Player or not Player.Available then return false end
    if Entity and Entity.Player and Entity.Player.IsCasting then return false end
    if Svc and Svc.Condition and not Svc.Condition[1] and not Svc.Condition[4] then return false end
    if Svc and Svc.Condition and Svc.Condition[45] then return false end  -- zoning
    return true
end

-- Helper: NamePlate + player + not zoning
function PlayerAndUIReadyXA()
    local not_zoning = not (Svc and Svc.Condition and Svc.Condition[45] and Svc.Condition[27] and Svc.Condition[26])
    return IsAddonReady("NamePlate")
        and IsAddonVisible("NamePlate")
        and IsPlayerAvailableXA()
        and not_zoning
end

function CharacterSafeWaitXA() -- Use this call for safewaits
	SleepXA(0.01)
    -- fast path: check once and return immediately if OK
    do
        local np = Addons and Addons.GetAddon and Addons.GetAddon("NamePlate")
        local ready, vis = np and np.Ready or false, np and np.Exists or false
        local avail = IsPlayerAvailableXA()
        if ready and vis and avail then
            return true
        end
    end

    -- otherwise, poll every 0.2s until conditions are met
    while true do
        local zoning = Svc and Svc.Condition and Svc.Condition[45]
        local np = Addons and Addons.GetAddon and Addons.GetAddon("NamePlate")
        local ready, vis = np and np.Ready or false, np and np.Exists or false
        local avail = IsPlayerAvailableXA()

        -- EchoXA(string.format("[NP %s/%s] [PLR %s] %s", tostring(ready), tostring(vis), tostring(avail), zoning and "(zoning)" or ""))

        if ready and vis and avail then
            EchoXA("All ready — stopping loop")
            return true
        end

        SleepXA(0.22)
    end
end

-- Helper: wait until a condition is true or timeout (seconds)
function WaitUntil(cond_fn, timeout_s, step_s)
    timeout_s = timeout_s or 10.0
    step_s = step_s or 0.2
    local waited = 0.0
    while not cond_fn() do
        SleepXA(step_s)
        waited = waited + step_s
        if waited >= timeout_s then return false end
    end
    return true
end

-- Simplified to wait if building map pathing
function DoNavFlySequenceXA()
    while not NavIsReady() do
        SleepXA(0.33)
    end

    if NavIsReady() then
        -- Choose flyflag vs moveflag based on Player.CanFly
        if Player and Player.CanFly then
            vnavXA("flyflag")
        else
            vnavXA("moveflag")
        end

        -- Stay paused while the path is active
        while PathIsRunning() or PathfindInProgress() do
            SleepXA(0.33)
        end

        -- Once path is done, dismount if you'd like
        -- yield("/mount")
        return true
    end

    return false
end

function MountUpXA()
    -- Only attempt to mount if mounting is allowed
    if not (Player and Player.CanMount) then
        return
    end

    while not Svc.Condition[4] do
        SleepXA(0.1)
        if Svc.Condition[27] then
            SleepXA(2)
        else
            gaXA("mount roulette")
            SleepXA(0.1)
        end
    end
end

function DismountXA()
    while Svc.Condition[4] do
        yield("/mount")
        SleepXA(2)
    end

    while not Svc.Condition[1] do
        SleepXA(0.1)
    end
end

function MovingCheaterXA()
    SleepXA(0.5)

    -- FAST PATH
    do
        if PlayerAndUIReadyXA() then
            MountUpXA()
            -- Reconfirm readiness after mount (avoids race)
            if WaitUntil(PlayerAndUIReadyXA, 3.0, 2) then
                DoNavFlySequenceXA()
                return true
            end
        end
    end

    -- POLL until ready, then go
    while true do
        if WaitUntil(PlayerAndUIReadyXA, 10.0, 2) then
            MountUpXA()
            -- Reconfirm after mount (e.g., if animation/zoning flickers)
            if WaitUntil(PlayerAndUIReadyXA, 3.0, 2) then
                DoNavFlySequenceXA()
                return true
            end
        end
        SleepXA(0.22)
    end
end

-- Setup pathing to door, and have Lifestream settings to Enter House
function return_to_fcXA()
    CharacterSafeWaitXA()
	yield("/li fc")
	SleepXA(1)
	WaitForLifestreamXA()
	SleepXA(2.01)
    CharacterSafeWaitXA()
	SleepXA(1.01)
end

function return_to_homeXA()
    CharacterSafeWaitXA()
	yield("/li home")
	SleepXA(1)
	WaitForLifestreamXA()
	SleepXA(2.02)
    CharacterSafeWaitXA()
	SleepXA(1.02)
end

function return_to_autoXA()
    CharacterSafeWaitXA()
	yield("/li auto")
	SleepXA(1)
	WaitForLifestreamXA()
	SleepXA(2.02)
    CharacterSafeWaitXA()
	SleepXA(1.02)
end

function return_to_homeworldXA()
    CharacterSafeWaitXA()
	yield("/li")
	SleepXA(1)
	WaitForLifestreamXA()
	SleepXA(2.02)
    CharacterSafeWaitXA()
	SleepXA(1.02)
end

function RunToHomeGCXA()
    CharacterSafeWaitXA()
	yield("/li hc")
	SleepXA(1)
	WaitForLifestreamXA()
	SleepXA(2.02)
    CharacterSafeWaitXA()
	SleepXA(1.02)
end

function EnableDeliverooXA()
    yield("/deliveroo enable")
end

function RestoreYesAlreadyXA()
    -- Restores YesAlready plugin when Deliveroo pauses or disables it
    -- Based on Deliveroo's ExternalPluginHandler.RestoreYesAlready() implementation
    -- which removes "Deliveroo" from YesAlready.StopRequests data
    if IPC and IPC.YesAlready then
        IPC.YesAlready.SetPluginEnabled(true)
        EchoXA("YesAlready restored after Deliveroo pause/disable")
    else
        EchoXA("Warning: YesAlready IPC not available")
    end
end

function GetYesAlreadyStateXA()
    -- Test function to check the current state of YesAlready plugin
    -- Returns and displays whether YesAlready is enabled or disabled
    EchoXA("=== YesAlready State Check ===")

    if not IPC then
        EchoXA("IPC not available")
        return nil
    end

    if not IPC.YesAlready then
        EchoXA("YesAlready IPC not available - plugin may not be installed")
        return nil
    end

    -- Try to get the enabled state
    local isEnabled = IPC.YesAlready.SetPluginEnabled()
    if isEnabled ~= nil then
        if isEnabled then
            EchoXA("YesAlready Status: ENABLED")
        else
            EchoXA("YesAlready Status: DISABLED")
        end
    else
        EchoXA("YesAlready Status: UNKNOWN (could not retrieve state)")
    end

    EchoXA("=========================")
    return isEnabled
end

function LifestreamCmdXA(name)
    local dest = (type(name) == "string") and name:match("^%s*(.-)%s*$") or ""
    if dest == "" then
        EchoXA("No Location Set.")
        return false
    end
    CharacterSafeWaitXA()
    SleepXA(1.01)
    EchoXA("Teleporting to " .. dest)
    yield("/li " .. dest)
    SleepXA(1)
    WaitForLifestreamXA()
    CharacterSafeWaitXA()
    SleepXA(1.02)
    CharacterSafeWaitXA()
    SleepXA(1.03)
    CharacterSafeWaitXA()
    SleepXA(1.04)
    CharacterSafeWaitXA()
    SleepXA(1.05)
    return true
end

function GetDistanceToPoint(target_x, target_y, target_z)
    local player_x = GetPlayerRawXPos()
    local player_y = GetPlayerRawYPos()
    local player_z = GetPlayerRawZPos()

    -- If only 2 coordinates provided, assume Z is same as player's Z
    if target_z == nil then
        target_z = player_z
    end

    local dx = player_x - target_x
    local dy = player_y - target_y
    local dz = player_z - target_z
    return math.sqrt(dx * dx + dy * dy + dz * dz)
end

function get_coordinates(coords)
    return coords[position]
end

function WalkToTargetXA(target_x, target_y, target_z, stop_dist)
    -- Walk to target without mounting, stop when within stop_dist
    local function GetCurrentDistance()
        local player_x = EntityPlayerPositionX()
        local player_y = EntityPlayerPositionY()
        local player_z = EntityPlayerPositionZ()
        local dx = target_x - player_x
        local dy = target_y - player_y
        local dz = target_z - player_z
        return math.sqrt(dx * dx + dy * dy + dz * dz)
    end

    local current_dist = GetCurrentDistance()

    -- If already within stop distance, don't move
    if current_dist <= stop_dist then
        EchoXA(string.format("[Walk] Already within %.1f yalms, no movement needed", stop_dist))
        return
    end

    -- Start walking (no flying/mounting)
    yield(string.format("/vnav moveto %.2f %.2f %.2f", target_x, target_y, target_z))
    SleepXA(0.5)

    -- Monitor distance and stop when close enough
    local max_iterations = 100
    local iterations = 0
    local stop_buffer = 1.5  -- Stop earlier to account for movement momentum

    while iterations < max_iterations do
        current_dist = GetCurrentDistance()

        -- Stop when within desired distance (with buffer for momentum)
        if current_dist <= (stop_dist + stop_buffer) then
            vnavXA("stop")
            SleepXA(0.3)
            local final_dist = GetCurrentDistance()
            EchoXA(string.format("[Walk] Stopped at %.1f yalms from target", final_dist))
            return
        end

        -- Check if pathfinding stopped (arrived or failed)
        if not PathfindInProgress() and not PathIsRunning() then
            vnavXA("stop")
            SleepXA(0.3)
            EchoXA(string.format("[Walk] Pathfinding completed at %.1f yalms", current_dist))
            return
        end

        SleepXA(0.3)
        iterations = iterations + 1
    end

    -- Timeout - stop movement
    vnavXA("stop")
    SleepXA(0.3)
    EchoXA("[Walk] Movement timeout - stopped")
end

-- Use GetSNDCoords() and then reference the long coords with the commas
-- MoveToXA(-12.123, 45.454, -18.5456) -- GOOD Usage
-- Will keep waiting SleepXA(0.507) while PathIsRunning/PathfindInProgress
function MoveToXA(valuex, valuey, valuez, stopdistance, FlyOrWalk)
    -- stopdistance and FlyOrWalk are optional (kept for backwards compatibility)
    SleepXA(0.1)

    MovingCheaterXA()

    -- Use flight if player can fly, otherwise walk
    PathfindAndMoveTo(valuex, valuey, valuez, Player and Player.CanFly or false)

    local countee = 0
    while (PathIsRunning() or PathfindInProgress()) do
        SleepXA(0.507)
        countee = countee + 1
        if gachi_jumpy == 1 and countee == 10 and Svc.ClientState.TerritoryType ~= 129 then
            gaXA("jump")
            countee = 0
            EchoXA("We are REALLY still pathfinding apparently.")
        end
    end

    EchoXA("[MoveToXA] Completed")
end

function log_coordinates(coords)
    local coord_str = table.concat(coords, ", ")
    EchoXA("[Coordinates] " .. coord_str)
end

function move_to(coords)
    if coords[1] and type(coords[1]) == "number" then
        log_coordinates(coords)
        MoveToXA(coords[1], coords[2], coords[3], 0.1, false)
        SleepXA(0.5)
    else
        for _, coord in ipairs(coords) do
            log_coordinates(coord)
            MoveToXA(coord[1], coord[2], coord[3], 0.1, false)
            SleepXA(0.5)
        end
    end
end

function PvpMoveToXA(x, y, z)
    -- Wait until player finishes casting before moving
    while GetCharacterCondition(27) do
        yield("/vnav stop")
        yield("/wait 0.1")
    end
    -- Execute vnavmesh moveto command with provided coordinates
    yield("/vnavmesh moveto "..x.." "..y.." "..z)
end

-- ------------------------
-- Player Commands
-- ------------------------

function InteractXA()
    SleepXA(0.5)
    yield("/interact")
    SleepXA(5)
end

function ResetCameraXA()
    yield("/send END")
    SleepXA(0.5)
end

function EquipRecommendedGearXA()
    CharacterSafeWaitXA()
    repeat
        yield("/character")
        SleepXA(0.1)
    until IsAddonVisible("Character")
    repeat
        if IsAddonReady("Character") then
            callbackXA("Character true 12")
        end
        SleepXA(0.1)
    until IsAddonVisible("RecommendEquip")
    repeat
        yield("/character")
        SleepXA(0.1)
    until not IsAddonVisible("Character")
    repeat
        if IsAddonReady("RecommendEquip") then
            callbackXA("RecommendEquip true 0")
        end
        SleepXA(0.1)
    until not IsAddonVisible("RecommendEquip")
end

function EquipRecommendedGearCmdXA()
    yield("/tweaks enable RecommendEquipCommand")
    SleepXA(1)
    yield("/equiprecommended")
    SleepXA(2)
end

function EnableArtisanXA()
    yield("/xlenableprofile Artisan")
    EchoXA("Enabled Artisan")
    SleepXA(3)
end

function DisableArtisanXA()
    yield("/xldisableprofile Artisan")
    EchoXA("Disabled Artisan")
    SleepXA(3)
end

function StartArtisanListXA(list_id)
    yield("/artisan lists " .. tostring(list_id) .. " start")
end

function CloseCraftingWindowsXA()
    callbackXA("Synthesis true -1") -- Cancel the current craft
    SleepXA(1) -- Shorter wait to retry frequently
    callbackXA("SynthesisSimple true -1") -- Cancel the current quick craft
    SleepXA(5) -- Shorter wait to retry frequently
    callbackXA("RecipeNote True -1") -- Close the crafting menu
    SleepXA(5) -- Brief wait to ensure the menu closes
end

-- MonitorJobLevelArtisanXA()      -- BAD Usage - script will not trigger if no level is mentioned
-- MonitorJobLevelArtisanXA(5)     -- GOOD Usage - monitors to reaching 5, then runs the stop/close/restart sequence
function MonitorJobLevelArtisanXA(target_level, pjob)
    if target_level == nil then
        EchoXA("No level has been set, no functionality being used.")
        return false
    end

    target_level = tonumber(target_level)
    if not target_level or target_level <= 0 then
        EchoXA("Invalid level provided, no functionality being used.")
        return false
    end

    local function _getlvl()
        return tonumber(GetLevelXA and GetLevelXA(pjob)) 
               or (Player and Player.Job and tonumber(Player.Job.Level)) 
               or 0
    end

    local characterLevel = _getlvl()

    if characterLevel < target_level then
        EchoXA("Level " .. target_level .. " not yet reached; we're level " .. characterLevel .. ". Waiting...")
        local lastAnnounced = characterLevel
        repeat
            SleepXA(5)
            characterLevel = _getlvl()
            -- Only echo when level changes to avoid spam
            if characterLevel ~= lastAnnounced and characterLevel < target_level then
                EchoXA("Level " .. target_level .. " not yet reached; we're level " .. characterLevel .. ".")
                lastAnnounced = characterLevel
            end
        until characterLevel >= target_level
    else
        EchoXA("Already level " .. characterLevel .. " (target " .. target_level .. ").")
    end

    EchoXA("Force stop crafting as we've reached level " .. target_level .. ".")

    DisableArtisanXA()
    SleepXA(8)

    -- Close crafting/recipe UIs until back to normal (minimal & safe)
    while not GetCharacterCondition(1) do
        CloseCraftingWindowsXA()
    end

    EnableArtisanXA()
    SleepXA(5)
    return true
end

-- ------------------------
-- Braindead Functions
-- ------------------------

function EnterHousingWardFromMenu()
    callbackXA("SelectString true 0")
    SleepXA(2)
    callbackXA("HousingSelectBlock true 0")
    SleepXA(3)
    SelectYesnoXA()
end

function SetNewbieCamera()
    yield("/hold UP")
    SleepXA(3)
    yield("/release UP")
    SleepXA(0.5)
    yield("/hold DOWN")
    SleepXA(0.5)
    yield("/release DOWN")
    SleepXA(0.5)
    yield("/hold NEXT")
    SleepXA(1)
    yield("/release NEXT")
    SleepXA(0.5)
    yield("/tiltcamera 60")
    SleepXA(1)
    yield("/hold CONTROL")
    SleepXA(0.5)
    yield("/send END")
    SleepXA(0.5)
    yield("/release CONTROL")
    SleepXA(0.5)
    yield("/send END")
end

function ImNotNewbStopWatching()
    SleepXA(1)
    EnableTextAdvanceXA()
    SleepXA(1)
    RemoveSproutXA()
    SleepXA(1)
    SetNewbieCamera()
    SleepXA(0.5)
end

function FreshLimsaToSummer()
    ImNotNewbStopWatching()

    -- Limsi Intro
    MoveToXA(-41.603382110596, 19.999998092651, -3.9526710510254)
    TargetXA("Ryssfloh")
    InteractXA()
    CharacterSafeWaitXA()

    -- Run to elevator
    MoveToXA(7.9892959594727, 20.99979019165, 11.781483650208)
    TargetXA("Grehfarr")
    InteractXA()
    SelectYesnoXA()
    CharacterSafeWaitXA()

    -- Run to bar
    MoveToXA(16.344181060791, 40.199962615967, -2.5296859741211)

    -- Complete MSQ Quest - Coming to Limsa Lominsa
    TargetXA("Baderon")
    InteractXA() -- I've been using /pyes for this, will setup sometime...
    -- callbackXA("SelectIconString true 1") -- Drowning Wench
    -- SleepXA(2)
    -- callbackXA("SelectYesno true 0") -- Proceed
    CharacterSafeWaitXA()

    -- Accept MSQ Quest - Close to Home
    TargetXA("Baderon")
    InteractXA()
    CharacterSafeWaitXA()
    TargetXA("Baderon") -- Double check
    InteractXA()
    CharacterSafeWaitXA()

    -- Talk to Niniya
    MoveToXA(7.4269256591797, 39.517566680908, -0.30605334043503)
    MoveToXA(7.8499450683594, 39.517566680908, 1.793778181076)
    ResetCameraXA()
    TargetXA("Niniya")
    InteractXA()
    CharacterSafeWaitXA()
    MoveToXA(5.2157278060913, 39.517566680908, 0.48788833618164)
    MoveToXA(3.6472775936127, 39.517570495605, 3.6093680858612)

    -- Run to elevator
    MoveToXA(6.0743732452393, 39.866470336914, 12.235060691833)
    TargetXA("Skaenrael")
    InteractXA()
    SelectYesnoXA()
    CharacterSafeWaitXA()

    -- Run to Aetheryte and attune
    MoveToXA(-76.502212524414, 18.800333023071, 2.2011289596558)
    grab_aetheryte()
    CharacterSafeWaitXA()

    -- Run to western town
    MoveToXA(62.093574523926, 19.999998092651, 0.20084396004677)
    WalkThroughDottedWallXA()
    CharacterSafeWaitXA()

    -- Run to Summerford
    gaXA("Sprint")
    MoveToXA(223.34646606445, 113.09998321533, -258.0676574707)
    grab_aetheryte()
    CharacterSafeWaitXA()
end

function FreshLimsaToMist()
    FreshLimsaToSummer()

    -- Run to southern door
    gaXA("Sprint")
    MoveToXA(188.85900878906, 65.238052368164, 285.26428222656)
    MoveToXA(208.56221008301, 65.483612060547, 286.01947021484)
    WalkThroughDottedWallXA()
    CharacterSafeWaitXA()

    -- Run to mist
    gaXA("Sprint")
    MoveToXA(597.07775878906, 61.533367156982, -108.43786621094)
    WalkThroughDottedWallXA()
    EnterHousingWardFromMenu()
end

function SummerToMist()
    -- Run to southern door
    gaXA("Sprint")
    MoveToXA(188.85900878906, 65.238052368164, 285.26428222656)
    MoveToXA(208.56221008301, 65.483612060547, 286.01947021484)
    WalkThroughDottedWallXA()
    CharacterSafeWaitXA()

    -- Run to mist
    gaXA("Sprint")
    MoveToXA(597.07775878906, 61.533367156982, -108.43786621094)
    WalkThroughDottedWallXA()
    EnterHousingWardFromMenu()
end

function FreshUldahToHorizon()
    ImNotNewbStopWatching()

    -- Uldah Intro
    MoveToXA(35.676815032959, 4.0, -151.50312805176)
    TargetXA("Wymond")
    InteractXA()
    CharacterSafeWaitXA()

    -- Run to bar
    MoveToXA(21.875730514526, 6.9999952316284, -81.64680480957)
    TargetXA("Momodi")
    InteractXA()
    CharacterSafeWaitXA()

    -- Complete MSQ Quest
    TargetXA("Momodi")
    InteractXA()
    CharacterSafeWaitXA()

    -- Confirm
    TargetXA("Momodi")
    InteractXA()
    CharacterSafeWaitXA()

    -- Run to uldah crystal
    MoveToXA(-140.84440612793, -3.1548881530762, -164.2811126709)
    grab_aetheryte()
    CharacterSafeWaitXA()

    -- Run to western thani
    MoveToXA(-178.24040222168, 14.049882888794, -16.344312667847)
    WalkThroughDottedWallXA()

    -- Run to horizon
    gaXA("Sprint")
    MoveToXA(69.638557434082, 46.244579315186, -224.87077331543)
    grab_aetheryte()
    CharacterSafeWaitXA()
end

function FreshUldahToGoblet()
    FreshUldahToHorizon()

    -- Run to Goblet
    gaXA("Sprint")
    MoveToXA(316.9354, 67.2082, 235.8752)
    WalkThroughDottedWallXA()
    EnterHousingWardFromMenu()
end

function HorizonToGoblet()
    -- Run to Goblet
    gaXA("Sprint")
    MoveToXA(316.9354, 67.2082, 235.8752)
    WalkThroughDottedWallXA()
    EnterHousingWardFromMenu()
end

function FreshGridaniaToBentbranch()
    ImNotNewbStopWatching()

    -- Gridania Intro
    MoveToXA(118.21111297607, -12.538880348206, 143.81802368164)
    TargetXA("Bertennant")
    InteractXA()
    CharacterSafeWaitXA()

    -- Run to bar
    MoveToXA(25.640754699707, -8.0, 114.60215759277)
    TargetXA("Mother Miounne")
    InteractXA()
    CharacterSafeWaitXA()

    -- Complete MSQ Quest
    TargetXA("Mother Miounne")
    InteractXA()
    CharacterSafeWaitXA()

    -- Confirm
    TargetXA("Mother Miounne")
    InteractXA()
    CharacterSafeWaitXA()

    -- Run to gridania crystal
    MoveToXA(34.434555053711, 2.2000005245209, 32.727458953857)
    grab_aetheryte()
    CharacterSafeWaitXA()

    -- Run to central shroud
    MoveToXA(118.21111297607, -12.538880348206, 143.81802368164)
    MoveToXA(152.84782409668, -12.851945877075, 157.20837402344)
    WalkThroughDottedWallXA()

    -- Run to Bentbranch
    gaXA("Sprint")
    MoveToXA(181.85122680664, -8.3421506881714, -39.37228012085)
    MoveToXA(87.608024597168, -6.2946090698242, 63.980049133301)
    MoveToXA(16.9049949646, -1.077308177948, 32.931064605713)
    grab_aetheryte()
    CharacterSafeWaitXA()
end

function FreshGridaniaToBeds()
    FreshGridaniaToBentbranch()

    -- Run to Beds
    gaXA("Sprint")
    MoveToXA(199.21711730957, -32.045715332031, 324.18838500977)
    TargetXA("Ferry Skipper")
    InteractXA()
    EnterHousingWardFromMenu()
end

function BentbranchToBeds()
    -- Run to Beds
    gaXA("Sprint")
    MoveToXA(199.21711730957, -32.045715332031, 324.18838500977)
    TargetXA("Ferry Skipper")
    InteractXA()
    EnterHousingWardFromMenu()
end
