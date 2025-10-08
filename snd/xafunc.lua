-- ----------------------------------------------------------------------------
-- Parts of this script pulls commands from dfunc, ensure you have dfunc before xafunc in your script
-- dfunc; can be found here: https://github.com/McVaxius/dhogsbreakfeast/blob/main/dfunc.lua
-- xafunc; can be found here: https://github.com/xa-io/ffxiv-tools/blob/main/snd/xafunc.lua
--
-- To use these functions in your scripts use the following commands at the start of your scripts
-- require("dfunc")
-- require("xafunc")
-- ----------------------------------------------------------------------------

-- ------------------------
-- Misc Things
-- ------------------------

function GetSNDCoords()
    Engines.Native.Run ("/e " .. Entity.Player.Position.X .. " " .. Entity.Player.Position.Y .. " " .. Entity.Player.Position.Z)
    Engines.Native.Run ("/e " .. Entity.Player.Position.X .. ", " .. Entity.Player.Position.Y .. ", " .. Entity.Player.Position.Z)
end

function EchoXA(text)
    yield("/echo " .. tostring(text))
end

function SleepXA(time)
    yield("/wait " .. tostring(time))
end

-- ------------------------
-- Plugin Things
-- ------------------------

function AutoRetainerIsBusy()
    return IPC.AutoRetainer.IsBusy()
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

--------------------------
-- World Info
--------------------------

function EnableTextAdvanceXA()
    yield("/at y")
    EchoXA("Enabling Text Advance...")
end
function DisableTextAdvanceXA()
    yield("/at n")
    EchoXA("Disabling Text Advance...")
end

function RemoveSproutXA()
    yield("/nastatus off")
    EchoXA("Removing New Adventurer Status...")
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
    if type(EchoXA) == "function" then
        EchoXA("Level: " .. tostring(lvl))
    else
        yield("/echo Level: " .. tostring(lvl))
    end
    return lvl
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
    yield("/xldisableprofile Artisan")
    EchoXA("Disabled Artisan")
    SleepXA(8)

    -- Close crafting/recipe UIs until back to normal (minimal & safe)
    while type(GetCharacterCondition) == "function" and not GetCharacterCondition(1) do
        yield("/callback Synthesis true -1")
        SleepXA(1)
        yield("/callback SynthesisSimple true -1")
        SleepXA(5)
        yield("/callback RecipeNote True -1")
        SleepXA(5)
    end

    yield("/xlenableprofile Artisan")
    EchoXA("Enabled Artisan")
    SleepXA(5)
    return true
end

-- ------------------------
-- Party Commands
-- ------------------------

function EnableBTBandInvite()
    yield("/xlenableprofile BTB")
    SleepXA(3)
    yield("/btb invite")
    SleepXA(3)
    yield("/xldisableprofile BTB")
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
	yield("/hold W")
	SleepXA(2)
	yield("/release W")
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
	yield("/li fc")
	WaitForLifestream()
	SleepXA(2.01)
    CharacterSafeWaitXA()
	SleepXA(1.01)
end

function return_to_homeXA()
	yield("/li home")
	WaitForLifestream()
	SleepXA(2.02)
    CharacterSafeWaitXA()
	SleepXA(1.02)
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

    EchoXA("[MoveTo] Completed")
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

function InteractXA()
    SleepXA(0.5)
    yield("/interact")
    SleepXA(2)
end

function ResetCameraXA()
    yield("/send END")
    SleepXA(0.5)
end

--------------------------
-- Player Commands
--------------------------

function EquipRecommendedGearXA()
    CharacterSafeWaitXA()
    repeat
        yield("/character")
        SleepXA(0.1)
    until IsAddonVisible("Character")
    repeat
        if IsAddonReady("Character") then
            yield("/callback Character true 12")
        end
        SleepXA(0.1)
    until IsAddonVisible("RecommendEquip")
    repeat
        yield("/character")
        SleepXA(0.1)
    until not IsAddonVisible("Character")
    repeat
        if IsAddonReady("RecommendEquip") then
            yield("/callback RecommendEquip true 0")
        end
        SleepXA(0.1)
    until not IsAddonVisible("RecommendEquip")
end

function EquipRecommendedGearCmdXA()
    yield("/equiprecommended")
end

--------------------------
-- Braindead Functions
--------------------------

function EnterHousingWardFromMenu()
    SleepXA(3)
    yield("/callback SelectString true 0")
    SleepXA(2)
    yield("/callback HousingSelectBlock true 0")
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
    yield("/target Ryssfloh")
    InteractXA()
    CharacterSafeWaitXA()

    -- Run to elevator
    MoveToXA(7.9892959594727, 20.99979019165, 11.781483650208)
    yield("/target Grehfarr")
    InteractXA()
    CharacterSafeWaitXA()

    -- Run to bar
    MoveToXA(16.344181060791, 40.199962615967, -2.5296859741211)

    -- Complete MSQ Quest - Coming to Limsa Lominsa
    yield("/target Baderon")
    InteractXA()
    -- yield("/callback SelectIconString true 1") -- Drowning Wench
    -- SleepXA(2)
    -- yield("/callback SelectYesno true 0") -- Proceed
    CharacterSafeWaitXA()

    -- Accept MSQ Quest - Close to Home
    yield("/target Baderon")
    InteractXA()
    CharacterSafeWaitXA()
    yield("/target Baderon") -- Double check
    InteractXA()
    CharacterSafeWaitXA()

    -- Talk to Niniya
    MoveToXA(7.4269256591797, 39.517566680908, -0.30605334043503)
    MoveToXA(7.8499450683594, 39.517566680908, 1.793778181076)
    ResetCameraXA()
    yield("/target Niniya")
    InteractXA()
    CharacterSafeWaitXA()

    -- Run to elevator
    MoveToXA(6.0743732452393, 39.866470336914, 12.235060691833)
    yield("/target Skaenrael")
    InteractXA()
    yield("/callback SelectIconString true 1") -- Bulwark Hall
    SleepXA(2)
    yield("/callback SelectYesno true 0") -- Proceed
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
    MoveToXA(223.34646606445, 113.09998321533, -258.0676574707)
    grab_aetheryte()
end

function FreshLimsaToMist()
    -- Run to southern door
    MoveToXA(188.85900878906, 65.238052368164, 285.26428222656)
    MoveToXA(208.56221008301, 65.483612060547, 286.01947021484)
    WalkThroughDottedWallXA()
    CharacterSafeWaitXA()

    -- Run to mist
    MoveToXA(597.07775878906, 61.533367156982, -108.43786621094)
    WalkThroughDottedWallXA()
    EnterHousingWardFromMenu()
end

function FreshSummerToMist()
    -- Run to southern door
    MoveToXA(188.85900878906, 65.238052368164, 285.26428222656)
    MoveToXA(208.56221008301, 65.483612060547, 286.01947021484)
    WalkThroughDottedWallXA()
    CharacterSafeWaitXA()

    -- Run to mist
    MoveToXA(597.07775878906, 61.533367156982, -108.43786621094)
    WalkThroughDottedWallXA()
    EnterHousingWardFromMenu()
end

function FreshUldahToHorizon()
    ImNotNewbStopWatching()

    -- Uldah Intro
    MoveToXA(35.676815032959, 4.0, -151.50312805176)
    yield("/target Wymond")
    InteractXA()
    CharacterSafeWaitXA()

    -- Run to bar
    MoveToXA(21.875730514526, 6.9999952316284, -81.64680480957)
    yield("/target Momodi")
    InteractXA()
    CharacterSafeWaitXA()

    -- Complete MSQ Quest
    yield("/target Momodi")
    InteractXA()
    CharacterSafeWaitXA()

    -- Confirm
    yield("/target Momodi")
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
    MoveToXA(69.638557434082, 46.244579315186, -224.87077331543)
    grab_aetheryte()
    CharacterSafeWaitXA()

    -- Run to Goblet
    MoveToXA(316.9354, 67.2082, 235.8752)
    WalkThroughDottedWallXA()
    EnterHousingWardFromMenu()
end
