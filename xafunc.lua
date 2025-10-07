------------------------------------------------------------------------------
-- Parts of this script pulls commands from dfunc, ensure you have dfunc before xafunc in your script
-- dfunc; can be found here: https://github.com/McVaxius/dhogsbreakfeast/blob/main/dfunc.lua
-- xafunc; can be found here: https://github.com/xa-io/ffxiv-tools/blob/main/xafunc.lua
--
-- To use these functions in your scripts use the following commands at the start of your scripts
-- require("dfunc")
-- require("xafunc")
------------------------------------------------------------------------------

--------------------------
-- Misc Things
--------------------------
-- SND GetCoords: 
-- Engines.Native.Run ("/e " .. Entity.Player.Position.X .. ", " .. Entity.Player.Position.Y .. ", " .. Entity.Player.Position.Z)

--------------------------
-- Party Commands
--------------------------

-- soon™

--------------------------
-- Movement Commands
--------------------------

function visland_stop_moving_xa()
    muuv = 1
    muuvstop = 0
    muuvX = EntityPlayerPositionX()
    muuvY = EntityPlayerPositionY()
    muuvZ = EntityPlayerPositionZ()
    while muuv == 1 do
        yield("/wait 1.01")
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
    yield("/wait 1.02")
    yield("/visland stop")
    yield("/vnavmesh stop")
    yield("/automove off")
    yield("/wait 1.03")
end

function WalkThroughDottedWallXA()
	yield("/hold W")
	yield("/wait 2")
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
	yield("/wait 0.01")
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

        yield(string.format("/echo [NP %s/%s] [PLR %s] %s",
            tostring(ready), tostring(vis), tostring(avail), zoning and "(zoning)" or ""))

        if ready and vis and avail then
            yield("/echo All ready — stopping loop")
            return true
        end

        yield("/wait 0.22")
    end
end

-- Helper: wait until a condition is true or timeout (seconds)
function WaitUntil(cond_fn, timeout_s, step_s)
    timeout_s = timeout_s or 10.0
    step_s = step_s or 0.2
    local waited = 0.0
    while not cond_fn() do
        yield(string.format("/wait %.2f", step_s))
        waited = waited + step_s
        if waited >= timeout_s then return false end
    end
    return true
end

-- Simplified to wait if building map pathing
function DoNavFlySequenceXA()
    while not NavIsReady() do
        yield("/wait 0.33")
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
            yield("/wait 0.33")
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
        yield("/wait 0.1")
        if Svc.Condition[27] then
            yield("/wait 2")
        else
            yield('/gaction "mount roulette"')
            yield("/wait 0.1")
        end
    end
end

function MovingCheaterXA()
    yield("/wait 0.5")

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
        yield("/wait 0.22")
    end
end

-- Setup pathing to door, and have Lifestream settings to Enter House
function return_to_fcXA()
	yield("/li fc")
	WaitForLifestream()
	yield("/wait 4")
    CharacterSafeWaitXA()
	yield("/wait 2")
end

function return_to_homeXA()
	yield("/li home")
	WaitForLifestream()
	yield("/wait 4")
    CharacterSafeWaitXA()
	yield("/wait 2")
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

--------------------------
-- IPC Commands
--------------------------

function AutoRetainerIsBusy()
    return IPC.AutoRetainer.IsBusy()
end
