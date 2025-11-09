-- ┌-----------------------------------------------------------------------------------------------------------------------
-- | 
-- |   ██╗  ██╗ █████╗     ██████╗ ███████╗██╗      ██████╗  ██████╗  ██████╗ ███████╗██████╗ 
-- |   ╚██╗██╔╝██╔══██╗    ██╔══██╗██╔════╝██║     ██╔═══██╗██╔════╝ ██╔════╝ ██╔════╝██╔══██╗
-- |    ╚███╔╝ ███████║    ██████╔╝█████╗  ██║     ██║   ██║██║  ███╗██║  ███╗█████╗  ██████╔╝
-- |    ██╔██╗ ██╔══██║    ██╔══██╗██╔══╝  ██║     ██║   ██║██║   ██║██║   ██║██╔══╝  ██╔══██╗
-- |   ██╔╝ ██╗██║  ██║    ██║  ██║███████╗███████╗╚██████╔╝╚██████╔╝╚██████╔╝███████╗██║  ██║
-- |   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
-- | 
-- | XA Relogger — Mass toon house tapping. Checks Personal plots and FC plots.
-- | 
-- | - Useful for toons that do not log in often. Used to prevent transfer of ownership and demo due to inactivity.
-- | - Can be used as a starter template for mass processing using the 'Run sequence for each toon' section.
-- | 
-- | Important Note: All characters MUST have Lifestream configured with FC pathing AND Enter House as setup. 
-- | 
-- | Requires:
-- |  dfunc; can be found here: https://github.com/McVaxius/dhogsbreakfeast/blob/main/dfunc.lua
-- |  xafunc; can be found here: https://github.com/xa-io/ffxiv-tools/blob/main/snd/xafunc.lua
-- |   - Two setup processes, 1) SND > Add script, name dfunc and another xafunc paste the code.
-- |   - 2) SND > Add script name the same as before, add github url and save, can update through SND
-- | 
-- | Refresh Owners v7.35
-- | Created by: https://github.com/xa-io
-- | Last Updated: 2025-10-10 00:00
-- |
-- | ## Release Notes ##
-- | v7.35 - Revamped codebase using new xafunc functions for better readability and maintainability
-- └-----------------------------------------------------------------------------------------------------------------------

-- DO NOT TOUCH THESE LINES BELOW
require("dfunc")
require("xafunc")
DisableARMultiXA()
rsrXA("off")
if not CheckPluginEnabledXA({"Lifestream", "vnavmesh", "AutoRetainer", "TextAdvance"}) then return end
-- DO NOT TOUCH THESE LINES ABOVE

-- ---------------------------------------
-- -- Start of Configuration Parameters --
-- ---------------------------------------

-- Toon list (last toon should not have a comma at the end)
local toon_list = {
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

function ProcessToonListXA()
    for i = 1, #toon_list do
        local who = toon_list[i][1]
        if who and who ~= "" then
            ProcessToonXA(i, #toon_list, who)
        end
    end
end

function ProcessToonXA(i, total, who)
    EchoXA(string.format("[Relog %d/%d] -> %s", i, total, who))

    if GetCharacterName(true) ~= who then
        ARRelogXA(who)
    else
        EchoXA("Already logged in as " .. who)
    end
    CharacterSafeWaitXA() -- Do not remove this checker

    -- Run sequence for each toon
    EnableTextAdvanceXA()
    RemoveSproutXA()
    return_to_homeXA()
    FreeCompanyCmdXA()
    return_to_fcXA()
end

ProcessToonListXA()
EnableARMultiXA()

-- ------------------------
-- -- End of XA Relogger --
-- ------------------------
