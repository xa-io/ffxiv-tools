-- ┌-----------------------------------------------------------------------------------------------------------------------
-- | 
-- |   ██╗  ██╗ █████╗     ██████╗ ███████╗██╗      ██████╗  ██████╗  ██████╗ ███████╗██████╗ 
-- |   ╚██╗██╔╝██╔══██╗    ██╔══██╗██╔════╝██║     ██╔═══██╗██╔════╝ ██╔════╝ ██╔════╝██╔══██╗
-- |    ╚███╔╝ ███████║    ██████╔╝█████╗  ██║     ██║   ██║██║  ███╗██║  ███╗█████╗  ██████╔╝
-- |    ██╔██╗ ██╔══██║    ██╔══██╗██╔══╝  ██║     ██║   ██║██║   ██║██║   ██║██╔══╝  ██╔══██╗
-- |   ██╔╝ ██╗██║  ██║    ██║  ██║███████╗███████╗╚██████╔╝╚██████╔╝╚██████╔╝███████╗██║  ██║
-- |   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
-- | 
-- | XA Relogger — Franchise owner login loop (no travel, no trading)
-- | - Logs into each character from a simple list ("Name@World")
-- | - Waits for CharacterSafeWaitXA() after each login
-- | - Immediately proceeds to the next character using /ays relog
-- | 
-- | - Use for FC Owners that do not log in often. Used to prevent transfer of ownership due to inactivity.
-- | 
-- | Requires:
-- |  dfunc; can be found here: https://github.com/McVaxius/dhogsbreakfeast/blob/main/dfunc.lua
-- |  xafunc; can be found here: https://github.com/xa-io/ffxiv-tools/blob/main/snd/xafunc.lua
-- |   - Two setup processes, 1) SND > Add script, name dfunc and another xafunc paste the code.
-- |   - 2) SND > Add script name the same as before, add github url and save, can update through SND
-- └-----------------------------------------------------------------------------------------------------------------------

-- DO NOT TOUCH THESE LINES BELOW
    require("dfunc")
    require("xafunc")
    PandoraSetFeatureState("Auto-Fill Numeric Dialogs", false)
    yield("/rotation Cancel")
-- DO NOT TOUCH THESE LINES ABOVE

-- ---------------------------------------
-- -- Start of Configuration Parameters --
-- ---------------------------------------

-- Toon list (last toon should not have a comma at the end)
local franchise_owners = {
    {"Toon One@World"},
    {"Toon Two@World"},
    {"Toon Three@World"}
}

-- -------------------------------------
-- -- End of Configuration Parameters --
-- -------------------------------------

-- --------------------------
-- -- Start of XA Relogger --
-- --------------------------

yield("/ays multi d")

for i = 1, #franchise_owners do
    local who = franchise_owners[i][1]
    local current = GetCharacterName(true)  -- includes @World

    EchoXA(string.format("[Relog %d/%d] -> %s", i, #franchise_owners, tostring(who)))

    -- Relog if we're not already on the target character
    if current ~= who then
        yield("/ays relog " .. who)
        SleepXA(2)
    else
        EchoXA("Already logged in as " .. who)
    end

    -- Run sequence for each toon
    CharacterSafeWaitXA()
    EnableTextAdvanceXA()
    RemoveSproutXA()
    return_to_homeXA()
    return_to_fcXA()
end

EchoXA("All characters processed. Relog-only run complete.")

yield("/ays multi e")

-- ------------------------
-- -- End of XA Relogger --
-- ------------------------
