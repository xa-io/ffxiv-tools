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
-- | XA Func Library v2.0
-- | Created by: https://github.com/xa-io
-- | Last Updated: 2025-11-01 21:10
-- |
-- | ## Release Notes ##
-- | v2.0 - Added IsInFreeCompany(), LeaveFreeCompany()
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
-- | SleepXA(time)                  -- Usage: SleepXA(5) -- Will use /wait 5
-- | TargetXA(targetname)           -- Usage: TargetXA("Player'or NPC-name")
-- | FocusTargetXA()                -- Usage: FocusTargetXA()
-- | vbmaiXA(text)                  -- Usage: vbmaiXA("on")
-- | vbmarXA()                      -- Usage: vbmarXA("disable")
-- | bmraiXA(text)                  -- Usage: bmraiXA("on")
-- | rsrXA(text)                    -- Usage: rsrXA("manual")
-- | adXA(text)                     -- Usage: adXA("stop")
-- | vnavXA(text)                   -- Usage: vnavXA("stop")
-- | callbackXA(text)               -- Usage: callbackXA("SelectYesno true 0")
-- | SelectYesnoXA()                -- Selects Yes if there is a popup
-- | 
-- | Plugin Things
-- |---------------------------------------------------------------------------
-- | AutoRetainerIsBusy()           -- Check if AutoRetainer is currently processing
-- | WaitForARToFinishXA()          -- Wait for AutoRetainerIsBusy()
-- | EnableSimpleTweaksXA()         -- Enable recommended SimpleTweaks settings (FixTarget, DisableTitleScreen, etc.)
-- | WaitForLifestreamXA()          -- Wait for Lifestream to process
-- | ARRelogXA(name)                -- Runs /ays relog, Usage: ARRelogXA("Toon Name@World")
-- | EnableARMultiXA()              -- Enable AutoRetainer Multi Mode
-- | DisableARMultiXA()             -- Disable AutoRetainer Multi Mode
-- | ARDiscardXA()                  -- Discard items and wait for AR to finish
-- | QSTStartXA()                   -- Start Questionable
-- | QSTStopXA()                    -- Stop Questionable
-- | QSTReloadXA()                  -- Reload Questionable
-- | EnableTextAdvanceXA()          -- Enable TextAdvance
-- | DisableTextAdvanceXA()         -- Disable TextAdvance
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
-- | IsInFreeCompany()              -- Check if player is currently in a Free Company
-- | LeaveFreeCompany()             -- Leave the current Free Company
-- |
-- | Party Commands
-- |---------------------------------------------------------------------------
-- | EnableBTBandInviteXA()         -- Enable BardToolbox, send mass party invite, then disable
-- | BTBInviteXA()                  -- Send out BardToolbox invite
-- | BTBDisbandXA()                 -- Send out BardToolbox disband and /leave to double check
-- | OpenArmouryChestXA()           -- Opens Armoury Chest
-- | OpenDropboxXA()                -- Opens Dropbox, then opens Item Trade Queue tab
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
-- | return_to_fcXA()               -- Lifestream teleport to FC house with auto-entry
-- | return_to_homeXA()             -- Lifestream teleport to personal house with auto-entry
-- | return_to_autoXA()             -- Lifestream teleport to select using auto list configuration
-- | return_to_homeworldXA()        -- Lifestream teleport back to your homeworld
-- | LifestreamCmdXA(name)          -- Replacement for yield("/li Limsa") - Usage: LifestreamCmdXA("Limsa")
-- | MoveToXA(x,y,z)                -- Fly/Run to coordinates with pathing - Usage: MoveToXA(-12.123, 45.454, -18.5456)
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
-- | FreshLimsaToMist()             -- Travel from Limsa to Mist housing district
-- | FreshSummerToMist()            -- Travel from Summerford Farms to Mist housing district
-- | FreshUldahToHorizon()          -- Complete Ul'dah intro sequence and travel to Horizon
-- └---------------------------------------------------------------------------

-- ------------------------
-- Misc Things
-- ------------------------

function EchoXA(text) -- Usage: EchoXA("Hello World In Echo Chat")
    yield("/echo " .. tostring(text))
end

function SleepXA(time) -- Usage: SleepXA(5) -- Will use /wait 5
    yield("/wait " .. tostring(time))
end

function TargetXA(targetname) -- Usage: TargetXA("Player'or NPC-name")
    yield('/target "' .. tostring(targetname) .. '"')
end

function FocusTargetXA() -- Usage: FocusTargetXA()
    yield("/focustarget")
    SleepXA(0.07)
end

function vbmaiXA(text) -- Usage: vbmaiXA("on")
    yield("/vbmai " .. tostring(text))
end

function vbmarXA(text)  -- Usage: vbmarXA("disable")
    yield("/vbm ar " .. tostring(text))
end

function bmraiXA(text) -- Usage: bmraiXA("on")
    yield("/bmrai " .. tostring(text))
end

function rsrXA(text) -- Usage: rsrXA("manual")
    yield("/rsr " .. tostring(text))
end

function adXA(text) -- Usage: adXA("stop")
    yield("/ad " .. tostring(text))
end

function vnavXA(text) -- Usage: vnavXA("stop")
    yield("/vnav " .. tostring(text))
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

function AutoRetainerIsBusy()
    return IPC.AutoRetainer.IsBusy()
end

function WaitForARToFinishXA()
    repeat
        SleepXA(1)
    until not IPC.AutoRetainer.IsBusy()
end

function EnableSimpleTweaksXA()
    if HasPlugin("SimpleTweaksPlugin") then
        yield("/tweaks enable FixTarget")
        yield("/tweaks enable DisableTitleScreenMovie")
        yield("/tweaks enable EquipJobCommand")
        yield("/tweaks enable RecommendEquipCommand")
        EchoXA("SimpleTweaks has been adjusted.")
    else
        EchoXA("SimpleTweaksPlugin is not installed.")
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
    EchoXA("Sending CharacterSafeWaitXA 1/4")
    CharacterSafeWaitXA()
    SleepXA(1.01)
    EchoXA("Sending CharacterSafeWaitXA 2/4")
    CharacterSafeWaitXA()
    SleepXA(1.02)
    EchoXA("Sending CharacterSafeWaitXA 3/4")
    CharacterSafeWaitXA()
    SleepXA(1.03)
    EchoXA("Sending CharacterSafeWaitXA 4/4")
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
    yield("/ays multi e")
end

function DisableARMultiXA()
    yield("/ays multi d")
end

function ARDiscardXA()
    yield("/ays discard")
    while AutoRetainerIsBusy() do
        SleepXA(1)
    end
    return true
end

function QSTStartXA()
    SleepXA(1)
    yield("/qst start")
    SleepXA(2)
end

function QSTStopXA()
    SleepXA(1)
    yield("/qst stop")
    SleepXA(2)
end

function QSTReloadXA()
    SleepXA(1)
    yield("/qst reload")
    SleepXA(2)
end

function EnableTextAdvanceXA()
    yield("/at y")
    EchoXA("Enabling Text Advance...")
end

function DisableTextAdvanceXA()
    yield("/at n")
    EchoXA("Disabling Text Advance...")
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

function GetWorldNameXAA()
    local id = (Svc and Svc.ClientState and Svc.ClientState.World) or nil
    local name

    if Excel and id then
        local row = Excel.GetRow("World", id)
        if row then
            -- check with dot, call with colon
            local place = (row.GetProperty and row:GetProperty("Name")) or nil
            name = place and (place.Name or place.Singular)
            if name and type(name) ~= "string" and name.ToString then
                name = name:ToString()
            end
        end
    end

    if not name or name == "" then name = tostring(id or "?") end
    EchoXA("World: " .. tostring(name) .. " [" .. tostring(id or "?") .. "]")
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

function IsInFreeCompany()
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

function LeaveFreeCompany()
    EchoXA("[Floater Assist] Opening Free Company menu to leave...")
    
    -- Open the FC menu
    yield("/freecompanycmd")
    SleepXA(2)
    
    -- Navigate to the Info tab
    yield("/callback FreeCompany false 0 5u")
    SleepXA(2)
    
    -- Click Leave FC button
    EchoXA("[Floater Assist] Leaving Free Company...")
    yield("/callback FreeCompanyStatus true 3")
    SleepXA(2)
    
    -- Confirm the leave action with SelectYesno
    if IsSelectYesnoVisible() then
        yield("/callback SelectYesno true 0")
        EchoXA("[Floater Assist] Successfully left Free Company")
    end

    yield("/leave")
    SleepXA(2)
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
    yield("/btb disband")
    SleepXA(2)
    yield("/btb invite")
    SleepXA(1)
end

function BTBDisbandXA()
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

function OpenArmouryChestXA()
    yield("/armourychest")
    SleepXA(0.07)
end

function OpenDropboxXA()
    yield("/dropbox")
    SleepXA(0.5)
    yield("/dropbox OpenTradeTab")
    SleepXA(0.5)
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
    yield("/vnavmesh stop")
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

        EchoXA(string.format("[NP %s/%s] [PLR %s] %s",
            tostring(ready), tostring(vis), tostring(avail), zoning and "(zoning)" or ""))

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
            yield("/vnav flyflag")
        else
            yield("/vnav moveflag")
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
            yield('/gaction "mount roulette"')
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

function LifestreamCmdXA(name)
    local dest = (type(name) == "string") and name:match("^%s*(.-)%s*$") or ""
    if dest == "" then
        EchoXA("No Location Set.")
        return false
    end

    EchoXA("Sending CharacterSafeWaitXA 1/5")
    CharacterSafeWaitXA()
    SleepXA(1.01)
    EchoXA("Teleporting to " .. dest)
    yield("/li " .. dest)
    SleepXA(1)
    WaitForLifestreamXA()
    EchoXA("Sending CharacterSafeWaitXA 2/5")
    CharacterSafeWaitXA()
    SleepXA(1.02)
    EchoXA("Sending CharacterSafeWaitXA 3/5")
    CharacterSafeWaitXA()
    SleepXA(1.03)
    EchoXA("Sending CharacterSafeWaitXA 4/5")
    CharacterSafeWaitXA()
    SleepXA(1.04)
    EchoXA("Sending CharacterSafeWaitXA 5/5")
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
            yield("/gaction jump")
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
end

function DisableArtisanXA()
    yield("/xldisableprofile Artisan")
    EchoXA("Disabled Artisan")
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

    -- Run to elevator
    MoveToXA(6.0743732452393, 39.866470336914, 12.235060691833)
    TargetXA("Skaenrael")
    InteractXA()
    callbackXA("SelectIconString true 1") -- Bulwark Hall
    SleepXA(2)
    callbackXA("SelectYesno true 0") -- Proceed
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

function FreshSummerToMist()
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

    -- Run horizon
    gaXA("Sprint")
    MoveToXA(69.638557434082, 46.244579315186, -224.87077331543)
    grab_aetheryte()
    CharacterSafeWaitXA()

    -- Run to Goblet
    gaXA("Sprint")
    MoveToXA(316.9354, 67.2082, 235.8752)
    WalkThroughDottedWallXA()
    EnterHousingWardFromMenu()
end
