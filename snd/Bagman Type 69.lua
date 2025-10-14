-- ┌-----------------------------------------------------------------------------------------------------------------------
-- | 
-- |   ██╗  ██╗ █████╗     ██████╗  █████╗  ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗
-- |   ╚██╗██╔╝██╔══██╗    ██╔══██╗██╔══██╗██╔════╝ ████╗ ████║██╔══██╗████╗  ██║
-- |    ╚███╔╝ ███████║    ██████╔╝███████║██║  ███╗██╔████╔██║███████║██╔██╗ ██║
-- |    ██╔██╗ ██╔══██║    ██╔══██╗██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║
-- |   ██╔╝ ██╗██║  ██║    ██████╔╝██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║
-- |   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
-- |                                                                                                                         
-- | Automated FFXIV bagman script for collecting and distributing resources across multiple characters
-- | 
-- | This script automates the process of collecting gil, treasure maps, dyes, and valuable items from multiple 
-- | characters and delivering them to a designated "Tony" character. Features intelligent inventory management 
-- | with configurable minimum thresholds and automatic Lifestream integration for seamless world transfers.
-- | 
-- | Core Features:
-- | • Multi-character gil and resource collection with configurable keep amounts
-- | • Automated treasure map and dye transfer system
-- | • High-value item detection and transfer (materia, crafting materials, etc.)
-- | • Lifestream integration for automatic world transfers and FC pathing
-- | • Configurable fuel and repair material minimum thresholds
-- | • Dropbox-based trading system with automatic inventory management
-- | • Enhanced character availability detection with false positive prevention
-- | • Support for custom Tony coordinates and meeting locations
-- | 
-- | Important Note: All characters MUST have Lifestream configured with FC pathing AND Enter House as setup. 
-- |
-- | *** CHECK DROPBOX!! ***
-- | You'll want to have auto-accepting on Tony!
-- | This is required to setup manually, just open dropbox and checkmark auto trading!
-- | 
-- | Requires:
-- |  dfunc; can be found here: https://github.com/McVaxius/dhogsbreakfeast/blob/main/dfunc.lua
-- |  xafunc; can be found here: https://github.com/xa-io/ffxiv-tools/blob/main/snd/xafunc.lua
-- |   - Two setup processes, 1) SND > Add script, name dfunc and another xafunc paste the code.
-- |   - 2) SND > Add script name the same as before, add github url and save, can update through SND
-- | 
-- | It is to be assumed that you have read the original bagman notes and understand how to run things from this point on.
-- | 
-- | XA Bagman Type 69 v7.35.2
-- | Created by: https://github.com/xa-io
-- | Last Updated: 2025-10-14 10:30
-- | 
-- | ## Release Notes ##
-- | v7.35.2 - No actual script changes, just adding notes regarding Tony x/y/z coords.
-- | v7.35.1 - No longer need to worry about dropbox being open on franchise owners, OpenDropboxXA() has been improved
-- | v7.35 - Revamped codebase using new xafunc functions for better readability and maintainability
-- | v7.3.1 - Fixed CharacterSafeWait/PlayerAvailable false positives with new functions
-- | v7.3 - Initial release with integrated minimum fuel and repair materials keep functionality
-- | - This would be useful for any retainer farmers with a surpluss of supplies that can be used to balance out alts
-- | - Set this number to something like 9999999 if you don't want to use the minimum filter to ensure it doesn't filter out your supplies
-- | - Added support for Lifestream pathing to FC entrances
-- └-----------------------------------------------------------------------------------------------------------------------

-- DO NOT TOUCH THESE LINES BELOW
require("dfunc")
require("xafunc")
DisableARMultiXA()
PandoraSetFeatureState("Auto-Fill Numeric Dialogs", false)
rsrXA("off")
bagman_type = 69 -- That's one sexy bag of loot
tony_type = 420 -- We're meeting at public smoking spot
-- DO NOT TOUCH THESE LINES ABOVE

-- ---------------------------------------
-- -- Start of Configuration Parameters --
-- ---------------------------------------

-- Where are we meeting Tony
tonys_turf = "Sephirot"          -- Which server are we bringing treasure to?
tonys_spot = "Summerford Farms"  -- What is the Aetheryte name to teleport to?
tony_zoneID = 134                -- ZoneID Check for tony_spot

-- Inventory Management          -- This will also give you all dyes now.
bagmans_take = 50000             -- Keep this much Gil on alts, give the rest to Tony
min_fuel_keep = 999999           -- Keep this much Ceruleum Fuel on alts, give the rest to Tony
min_repair_mats_keep = 999999    -- Keep this much Magitek Repair Mats on alts, give the rest to Tony

-- Do not need to change the below coords unless you want all franchise_owners to run to a set coord and wait for tony to be within range
-- Use GetInverseBagmanCoordsXA() from xafunc if you want to set this
tony_x = 42069420
tony_y = 42069420
tony_z = 42069420
-- If you change the above coods, understand that Tony must be within 1.5 Yalms, so make sure Tony is within reach, or the alt will spam wait
-- Otherwise if you leave 42069420, the alts will auto-path to your "Tony Name" in franchise_owners list below

--[[
Field 1. Subfarmer Name@World
Field 2. Return Home 1 = yes 0 = no
Field 3. 69 = Let Lifestream handle pathing (XA release, do not change)
Field 4. Tonyfirst Lastname (No world name) [no comma on last line]
]]

-- Toon list (last toon should not have a comma at the end)
local franchise_owners = {
    {"Toon One@World", 1, 69,"Tony Name"},
    {"Toon Two@World", 1, 69,"Tony Name"},
    {"Toon Three@World", 1, 69,"Tony Name"}
}

-- -------------------------------------
-- -- End of Configuration Parameters --
-- -------------------------------------

-- ------------------------
-- -- Start of Functions --
-- ------------------------

local filled_bags = {
    {1,999999999},
    {2,999999999},
    {3,999999999}
}

DropboxSetItemQuantity(1,false,0)

for i=1, #filled_bags do
    filled_bags[i][3] = 1
end

function are_we_there_yet_jimmy()
    woah_bruv = 1
        for i=1, #filled_bags do
            if GetItemCount(filled_bags[i][1]) - filled_bags[i][2] > 0 then
                woah_bruv = 0
            end
        end
    return woah_bruv
end

fat_tony = "Firstname Lastname" -- Placeholder, do not change

local function distance(x1, y1, z1, x2, y2, z2)
    if type(x1) ~= "number" then x1 = 0 end
    if type(y1) ~= "number" then y1 = 0 end
    if type(z1) ~= "number" then z1 = 0 end
    if type(x2) ~= "number" then x2 = 0 end
    if type(y2) ~= "number" then y2 = 0 end
    if type(z2) ~= "number" then z2 = 0 end
    zoobz = math.sqrt((x2 - x1)^2 + (y2 - y1)^2 + (z2 - z1)^2)
        if type(zoobz) ~= "number" then
            zoobz = 0
        end
    return zoobz
end

local function approach_tony()
    local specific_tony = 0
    if tony_x ~= 42069420 and tony_y ~= 42069420 and tony_z ~= 42069420 then
        specific_tony = 1
    end
    if specific_tony == 0 then
        PathfindAndMoveTo(GetObjectRawXPos(fat_tony),GetObjectRawYPos(fat_tony),GetObjectRawZPos(fat_tony), false)
    end
    if specific_tony == 1 then
        PathfindAndMoveTo(tony_x,tony_y,tony_z, false)
    end
end

get_to_the_choppa = 0
horrible_counter_method = 0

local function shake_hands()
    get_to_the_choppa = 0
    horrible_counter_method = 0

    thebag = GetGil() - bagmans_take
        if thebag < 0 then
            thebag = GetGil()
        end

    fuel_to_deliver = GetItemCount(10155) - min_fuel_keep
        if fuel_to_deliver < 0 then
            fuel_to_deliver = 0
        end

    mats_to_deliver = GetItemCount(10373) - min_repair_mats_keep
        if mats_to_deliver < 0 then
            mats_to_deliver = 0
        end

    TargetXA(fat_tony)
    SleepXA(1.04)
    while string.len(GetTargetName()) == 0 do
        TargetXA(fat_tony)
        SleepXA(1.05)
    end

    while distance(EntityPlayerPositionX(), EntityPlayerPositionY(), EntityPlayerPositionZ(), GetObjectRawXPos(fat_tony),GetObjectRawYPos(fat_tony),GetObjectRawZPos(fat_tony)) > 1.5 do
        TargetXA(fat_tony)
        SleepXA(1.06)
    end

    while get_to_the_choppa == 0 do
        if (GetGil() < (bagmans_take + 1)) and (tony_type == 420) then
            get_to_the_choppa = 1
        end
        TargetXA(fat_tony)

        if bagman_type == 69 then
            snaccman = GetGil() - bagmans_take
            if snaccman < 0 then
                snaccman = 0
            end
            OpenDropboxXA()
            SleepXA(0.5)
            if snaccman > 0 then
                DropboxSetItemQuantity(1,false,snaccman) -- Gil
            end

            -- xfertreasure 
                DropboxSetItemQuantity(22500,false,999999) -- Salvaged Ring
                DropboxSetItemQuantity(22501,false,999999) -- Salvaged Bracelet
                DropboxSetItemQuantity(22502,false,999999) -- Salvaged Earring
                DropboxSetItemQuantity(22503,false,999999) -- Salvaged Necklace
                DropboxSetItemQuantity(22504,false,999999) -- Extravagant Salvaged Ring
                DropboxSetItemQuantity(22505,false,999999) -- Extravagant Salvaged Bracelet
                DropboxSetItemQuantity(22506,false,999999) -- Extravagant Salvaged Earring
                DropboxSetItemQuantity(22507,false,999999) -- Extravagant Salvaged Necklace

            -- xferdyes 
                DropboxSetItemQuantity(13114,false,999999) -- General-purpose Pure White Dye
                DropboxSetItemQuantity(13115,false,999999) -- General-purpose Jet Black Dye
                DropboxSetItemQuantity(13116,false,999999) -- General-purpose Metallic Silver Dye
                DropboxSetItemQuantity(13117,false,999999) -- General-purpose Metallic Gold Dye
                DropboxSetItemQuantity(13708,false,999999) -- General-purpose Pastel Pink Dye
                DropboxSetItemQuantity(13709,false,999999) -- General-purpose Dark Red Dye
                DropboxSetItemQuantity(13710,false,999999) -- General-purpose Dark Brown Dye
                DropboxSetItemQuantity(13711,false,999999) -- General-purpose Pastel Green Dye
                DropboxSetItemQuantity(13712,false,999999) -- General-purpose Dark Green Dye
                DropboxSetItemQuantity(13713,false,999999) -- General-purpose Pastel Blue Dye
                DropboxSetItemQuantity(13714,false,999999) -- General-purpose Dark Blue Dye
                DropboxSetItemQuantity(13715,false,999999) -- General-purpose Pastel Purple Dye
                DropboxSetItemQuantity(13716,false,999999) -- General-purpose Dark Purple Dye
                DropboxSetItemQuantity(13717,false,999999) -- General-purpose Metallic Red Dye
                DropboxSetItemQuantity(13718,false,999999) -- General-purpose Metallic Orange Dye
                DropboxSetItemQuantity(13719,false,999999) -- General-purpose Metallic Yellow Dye
                DropboxSetItemQuantity(13720,false,999999) -- General-purpose Metallic Green Dye
                DropboxSetItemQuantity(13721,false,999999) -- General-purpose Metallic Sky Blue Dye
                DropboxSetItemQuantity(13722,false,999999) -- General-purpose Metallic Blue Dye
                DropboxSetItemQuantity(13723,false,999999) -- General-purpose Metallic Purple Dye

            -- xferhighvaluables 
                DropboxSetItemQuantity(20476,false,999999) -- Ao Dai
                DropboxSetItemQuantity(36841,false,999999) -- Buttoned Varsity Jacket
                DropboxSetItemQuantity(40408,false,999999) -- Cactuar Pajama Eye Mask
                DropboxSetItemQuantity(40409,false,999999) -- Cactuar Pajama Shirt
                DropboxSetItemQuantity(40410,false,999999) -- Cactuar Pajama Bottoms
                DropboxSetItemQuantity(40411,false,999999) -- Cactuar Pajama Slippers
                DropboxSetItemQuantity(32798,false,999999) -- Calfskin Rider's Cap
                DropboxSetItemQuantity(32799,false,999999) -- Calfskin Rider's Jacket
                DropboxSetItemQuantity(32800,false,999999) -- Calfskin Rider's Gloves
                DropboxSetItemQuantity(32801,false,999999) -- Calfskin Rider's Bottoms
                DropboxSetItemQuantity(32802,false,999999) -- Calfskin Rider's Shoes
                DropboxSetItemQuantity(33027,false,999999) -- Calf Leather
                DropboxSetItemQuantity(40412,false,999999) -- Chocobo Pajama Eye Mask
                DropboxSetItemQuantity(40413,false,999999) -- Chocobo Pajama Shirt
                DropboxSetItemQuantity(40414,false,999999) -- Chocobo Pajama Bottoms
                DropboxSetItemQuantity(40415,false,999999) -- Chocobo Pajama Slippers
                DropboxSetItemQuantity(8554,false,999999) -- Coliseum Loincloth
                DropboxSetItemQuantity(8553,false,999999) -- Coliseum Gaskins
                DropboxSetItemQuantity(8555,false,999999) -- Coeurl Beach Tanga
                DropboxSetItemQuantity(8557,false,999999) -- Coeurl Beach Halter
                DropboxSetItemQuantity(8558,false,999999) -- Coeurl Beach Briefs
                DropboxSetItemQuantity(8559,false,999999) -- Coeurl Beach Maro
                DropboxSetItemQuantity(8560,false,999999) -- Coeurl Beach Pareo
                DropboxSetItemQuantity(8561,false,999999) -- Coeurl Beach Sarong
                DropboxSetItemQuantity(27977,false,999999) -- Coliseum Galerus Antiquated
                DropboxSetItemQuantity(14836,false,999999) -- Expeditioner's Overcoat
                DropboxSetItemQuantity(14835,false,999999) -- Expeditioner's Pantalettes
                DropboxSetItemQuantity(33660,false,999999) -- Frontier Dress
                DropboxSetItemQuantity(33656,false,999999) -- Frontier Jacket
                DropboxSetItemQuantity(33657,false,999999) -- Frontier Trousers
                DropboxSetItemQuantity(33659,false,999999) -- Frontier Ribbon
                DropboxSetItemQuantity(33662,false,999999) -- Frontier Pumps
                DropboxSetItemQuantity(33869,false,999999) -- Frontier Cloth
                DropboxSetItemQuantity(38244,false,999999) -- Lawless Enforcer's Jacket
                DropboxSetItemQuantity(38246,false,999999) -- Lawless Enforcer's Slacks
                DropboxSetItemQuantity(7546,false,999999) -- Light Steel Galerus
                DropboxSetItemQuantity(7032,false,999999) -- Lotus Leaf
                DropboxSetItemQuantity(41592,false,999999) -- Martial Artist's Vest
                DropboxSetItemQuantity(41593,false,999999) -- Martial Artist's Slops
                DropboxSetItemQuantity(41594,false,999999) -- Martial Artist's Pumps
                DropboxSetItemQuantity(41595,false,999999) -- Martial Artist's Sleeveless Vest
                DropboxSetItemQuantity(8026,false,999999) -- Matron's Favor (Upper La Noscea)
                DropboxSetItemQuantity(15925,false,999999) -- Odyssean Dress Shoes
                DropboxSetItemQuantity(15921,false,999999) -- Odyssean Dress Shirt
                DropboxSetItemQuantity(15927,false,999999) -- Odyssean Thighboots
                DropboxSetItemQuantity(15926,false,999999) -- Odyssean Skirt
                DropboxSetItemQuantity(20270,false,999999) -- Oriental Tea Set
                DropboxSetItemQuantity(20475,false,999999) -- Pantalettes of Eternal Devotion
                DropboxSetItemQuantity(36629,false,999999) -- Neon Hangar Sign
                DropboxSetItemQuantity(9289,false,999999) -- Peisteskin Map
                DropboxSetItemQuantity(40404,false,999999) -- Porxie Pajama Eye Mask
                DropboxSetItemQuantity(40405,false,999999) -- Porxie Pajama Shirt
                DropboxSetItemQuantity(40406,false,999999) -- Porxie Pajama Bottoms
                DropboxSetItemQuantity(40407,false,999999) -- Porxie Pajama Slippers
                DropboxSetItemQuantity(20477,false,999999) -- Qiqirn Earring
                DropboxSetItemQuantity(28827,false,999999) -- Raptor Skin
                DropboxSetItemQuantity(28824,false,999999) -- Raptor Leather
                DropboxSetItemQuantity(7537,false,999999) -- Sentinel Sarouel
                DropboxSetItemQuantity(7535,false,999999) -- Sentinel Galerus
                DropboxSetItemQuantity(7538,false,999999) -- Sentinel Sabatons
                DropboxSetItemQuantity(39313,false,999999) -- Thavnairian Bustier (Replica)
                DropboxSetItemQuantity(39315,false,999999) -- Thavnairian Sandals (Replica)
                DropboxSetItemQuantity(39309,false,999999) -- Thavnairian Turban (Replica)
                DropboxSetItemQuantity(39308,false,999999) -- Thavnairian Bustier (Replica)
                DropboxSetItemQuantity(44252,false,999999) -- Turali Formal Shirt
                DropboxSetItemQuantity(44254,false,999999) -- Turali Formal Shoes
                DropboxSetItemQuantity(44255,false,999999) -- Turali Formal Slacks
                DropboxSetItemQuantity(44253,false,999999) -- Turali Formal Vest
                DropboxSetItemQuantity(7540,false,999999) -- Vanya Robe
                DropboxSetItemQuantity(7542,false,999999) -- Vanya Hat
                DropboxSetItemQuantity(7541,false,999999) -- Vanya Slops
                DropboxSetItemQuantity(7548,false,999999) -- Vanya Gloves
                DropboxSetItemQuantity(20471,false,999999) -- Wreath of Roses
                DropboxSetItemQuantity(20473,false,999999) -- Wreath of Lilies
                DropboxSetItemQuantity(10394,false,999999) -- Thavnairian Armlets
                DropboxSetItemQuantity(10393,false,999999) -- Thavnairian Bustier
                DropboxSetItemQuantity(10392,false,999999) -- Thavnairian Headdress
                DropboxSetItemQuantity(10396,false,999999) -- Thavnairian Sandals
                DropboxSetItemQuantity(10390,false,999999) -- Thavnairian Sarouel
                DropboxSetItemQuantity(10395,false,999999) -- Thavnairian Tights
                DropboxSetItemQuantity(44132,false,999999) -- Timeless Turali Cloth
                DropboxSetItemQuantity(44246,false,999999) -- Turali Trader's Shirt
                DropboxSetItemQuantity(44247,false,999999) -- Turali Trader's Culottes
                DropboxSetItemQuantity(44248,false,999999) -- Turali Trader's Shoes
                DropboxSetItemQuantity(44249,false,999999) -- Turali Traveler's Shirt
                DropboxSetItemQuantity(44250,false,999999) -- Turali Traveler's Shoes
                DropboxSetItemQuantity(36839,false,999999) -- Varsity Bottoms
                DropboxSetItemQuantity(36837,false,999999) -- Varsity Flat Cap
                DropboxSetItemQuantity(36838,false,999999) -- Varsity Jacket
                DropboxSetItemQuantity(36842,false,999999) -- Varsity Skirt
                DropboxSetItemQuantity(36840,false,999999) -- Varsity Shoes
                DropboxSetItemQuantity(38566,false,999999) -- White Sweet Pea Necklace
                DropboxSetItemQuantity(35869,false,999999) -- Wristlet of Happiness

            if fuel_to_deliver > 0 then
                DropboxSetItemQuantity(10155,false,fuel_to_deliver) -- Ceruleum Tank
            end
            if mats_to_deliver > 0 then
                DropboxSetItemQuantity(10373,false,mats_to_deliver) -- Magitek Repair Materials
            end

            if GetItemCount(22500) == 0 and GetItemCount(22501) == 0 and GetItemCount(22502) == 0 and GetItemCount(22503) == 0 and GetItemCount(22504) == 0 and GetItemCount(22505) == 0 and GetItemCount(22506) == 0 and GetItemCount(22507) == 0 then
                if GetGil() == snaccman then
                    get_to_the_choppa = 1
                end
            end

            if GetGil() > bagmans_take then
                DropboxSetItemQuantity(1,false,thebag)
            end

            horrible_counter_method = horrible_counter_method + 1
                    EchoXA("Bagman type 2 processing....")
            if horrible_counter_method > 1 then
                get_to_the_choppa = 1
                    EchoXA("Moving towards exiting bagman type 2....")
            end
        end
    end
        SleepXA(0.99)
        FocusTargetXA()
        DropboxStart()
        OpenArmouryChestXA()
        floo = DropboxIsBusy()
        while floo == true do
            floo = DropboxIsBusy()
            SleepXA(1)
                EchoXA("Trading happening!")
        end

    SleepXA(5.01)
end

-- ----------------------
-- -- End of Functions --
-- ----------------------

-- ------------------------
-- -- Start of XA Bagman --
-- ------------------------

for i=1,#franchise_owners do
    fat_tony = franchise_owners[i][4]
        EchoXA("Loading bagman to deliver protection payments Fat Tony -> "..fat_tony..".  Bagman -> "..franchise_owners[i][1])
        EchoXA("Processing Bagman "..i.."/"..#franchise_owners)

    if GetCharacterName(true) ~= franchise_owners[i][1] then
        ARRelogXA(franchise_owners[i][1])
        EnableTextAdvanceXA()
        RemoveSproutXA()
    end
        EchoXA("Processing Bagman "..i.."/"..#franchise_owners)

    DropboxSetItemQuantity(1,false,0)
    if GetGil() < bagmans_take then
        SleepXA(5.02)
    end

    road_trip = 0
        EchoXA("GetGil() -> "..GetGil())
        EchoXA("bagmans_take -> "..bagmans_take)

    road_trip = 1
        LifestreamCmdXA(tonys_turf)
            EchoXA("Processing Bagman "..i.."/"..#franchise_owners)

    if tony_type == 420 then
        EchoXA(fat_tony.." is meeting us in the alleyways.. watch your back")
        while tony_zoneID ~= Svc.ClientState.TerritoryType do
            LifestreamCmdXA(tonys_spot)
        end
    end

    if tony_type == 420 then
        approach_tony()
        FullStopMovementXA()
    end

shake_hands()
zungazunga()

    if road_trip == 1 then
        if franchise_owners[i][2] == 0 then
                EchoXA("wait why can't i leave "..fat_tony.."?")
        end

        if franchise_owners[i][2] == 1 then
            EchoXA("See ya "..fat_tony..", a pleasure.")
            return_to_homeworldXA()

                if franchise_owners[i][3] == 69 then
                    SleepXA(5.04)
                    return_to_fcXA()
                    FreeCompanyCmdXA()
                end
        end
    end
end

EnableARMultiXA()

-- ----------------------
-- -- End of XA Bagman --
-- ----------------------
