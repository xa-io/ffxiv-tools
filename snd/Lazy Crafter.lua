-- ┌-----------------------------------------------------------------------------------------------------------------------
-- | 
-- |   ██╗  ██╗ █████╗     ██╗      █████╗ ███████╗██╗   ██╗     ██████╗██████╗  █████╗ ███████╗████████╗███████╗██████╗ 
-- |   ╚██╗██╔╝██╔══██╗    ██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝    ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
-- |    ╚███╔╝ ███████║    ██║     ███████║  ███╔╝  ╚████╔╝     ██║     ██████╔╝███████║█████╗     ██║   █████╗  ██████╔╝
-- |    ██╔██╗ ██╔══██║    ██║     ██╔══██║ ███╔╝    ╚██╔╝      ██║     ██╔══██╗██╔══██║██╔══╝     ██║   ██╔══╝  ██╔══██╗
-- |   ██╔╝ ██╗██║  ██║    ███████╗██║  ██║███████╗   ██║       ╚██████╗██║  ██║██║  ██║██║        ██║   ███████╗██║  ██║
-- |   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝        ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝
-- | 
-- | Automated FFXIV crafting leveling script for unlocking blacksmith and reaching level 25
-- | 
-- | This script automates the complete process of leveling a fresh character from level 1 to 25 in blacksmithing 
-- | to enable Free Company creation. Features automatic material purchasing, class unlocking, and intelligent 
-- | crafting progression with support for both boosted and non-boosted worlds.
-- | 
-- | Core Features:
-- | • Automatic teleportation to Limsa Lominsa Lower Decks and zone verification
-- | • Gil and Fire Shards inventory checking with Tony trading integration via Dropbox
-- | • Multi-vendor material purchasing from Engerrand, Sorcha, Iron Thunder, Syneyhil, and Smydhaemr
-- | • Blacksmith Guild quest completion and class unlocking automation
-- | • Two-stage crafting progression (levels 1-12 and 12-25) with Artisan integration
-- | • Multi-position support for running up to 3 characters simultaneously
-- | • Automatic gear changes and inventory management at level milestones
-- | • Grand Company navigation and item discarding upon completion
-- | 
-- | Important Note: Requires dfunc/xafunc, Dropbox plugin, TextAdvance, and pre-configured Artisan crafting lists. 
-- | Character must have armoury system unlocked, access to Limsa Lominsa and specific YesAlready configurations for vendor interactions.
-- | 
-- | Requires:
-- |  dfunc; can be found here: https://github.com/McVaxius/dhogsbreakfeast/blob/main/dfunc.lua
-- |  xafunc; can be found here: https://github.com/xa-io/ffxiv-tools/blob/main/snd/xafunc.lua
-- |   - Two setup processes, 1) SND > Add script, name dfunc and another xafunc paste the code.
-- |   - 2) SND > Add script name the same as before, add github url and save, can update through SND
-- | 
-- | XA Lazy Crafter v7.35.2
-- | Created by: https://github.com/xa-io
-- | Last Updated: 2025-12-30 08:00
-- | 
-- | ## Release Notes ##
-- | v7.35.2 - Imported EquipRecommendedGearXA() to be used instead of Send C, misc.
-- | v7.35.1 - Added CharacterSafeWaitXA() after speaking to each Randwulf and Brithael
-- | v7.35 - Revamped codebase using new xafunc functions for better readability and maintainability
-- └-----------------------------------------------------------------------------------------------------------------------
-- ┌-----------------------------------------------------------------------------------------------------------------------
-- | ********************************************************************************************************
-- | *** READ EVERYTHING BEFORE USING BECAUSE THERE IS A 95% CHANCE YOU'LL MISS SOMETHING AND HAVE ISSUES ***
-- | ********************************************************************************************************
-- | 
-- | You should have NOT touched any BSM quest lines or accepting the original quests.
-- | If you did, this will still check and attempt to accept the class and do the first quest.
-- | In addition, you'll need to go add YesAlready options for 'Nothing' for those NPC's.
-- | 
-- | When the script starts, if you're not in Limsa Lominsa Lower Decks, it will automatically
-- | teleport you there. Once in Lower Decks, the script checks your Gil and Fire Shards
-- | inventory. If you're missing any items, the script will wait in Limsa for Tony to trade 
-- | them to you using Dropbox, so ensure you have dropbox turned on for the low level toon.
-- | I recommend preloading 85k gil and 600 fire shards to avoid bottlenecks.
-- | 
-- | If no items are needed from Tony, the script will proceed to purchase the required materials
-- | from various vendors. After purchasing, it will head to the Blacksmith to complete the first
-- | quest, then move to the Mender to start crafting.
-- | 
-- | The crafting process begins with the 1-12 crafting list, which includes extra items to 
-- | ensure you reach level 12. At level 12, the script will force stop, make you stand up, change 
-- | gear and then continue crafting until you reach level 25. Once crafting is complete, the script 
-- | will force stop again, move you to the Grand Company, and discard all your items, your may want
-- | to make a list after the first toon is completed and before moving onto the next toons.
-- | 
-- | Thanks to everyone in Punish and SND community for some of the things I was able to use from the channel.
-- | 
-- | - ѪѦ
-- └-----------------------------------------------------------------------------------------------------------------------
-- ┌-----------------------------------------------------------------------------------------------------------------------
-- | *** Plugin Requirements & Configuration***
-- | 
-- | TextAdvance -> No configuration needed, the script will enable it for each toon while running
-- | 
-- | SND -> Make a new SND lua script and name it dfunc and another xafunc and create those properly
-- | 
-- | Simple Tweaks -> Fix '/target' command -> Check this box
-- | 
-- | CBT -> Commands -> /equip -> Check this box
-- | 
-- | AutoRetainer -> Inventory Management -> Inventory Cleanup -> Discard List -> Max stacks size to be discarded -> 200 or 999 -- (You'll Have To Make Your Own List On The First Go)
-- | 
-- | YesAlready -> YesNo -> Click Yes -> Message: Repair all displayed items for 
-- | YesAlready -> YesNo -> Click Yes -> Message: Complete trade?
-- | YesAlready -> YesNo -> Click Yes -> Message: Purchase 
-- | YesAlready -> YesNo -> Click Yes -> Message: Join the Blacksmiths' Guild?
-- | YesAlready -> YesNo -> Click Yes -> Message: Swing a hammer for ol' Brithael?
-- | YesAlready -> YesNo -> Click Yes -> Message: Replace it with a weathered cross-pein hammer?
-- | YesAlready -> YesNo -> Click Yes -> Message: You cannot currently equip this item. Proceed with the transaction?
-- | YesAlready -> List -> Target: Sorcha -> Message: Purchase Fieldcraft/Tradecraft Accessories
-- | YesAlready -> List -> Target: Iron Thunder -> Message: Purchase Disciple of the Hand/Land Gear
-- | YesAlready -> List -> Target: Iron Thunder -> Message: Purchase Gear (Lv. 10-19)
-- | YesAlready -> List -> Target: Syneyhil -> Message: Purchase Disciple of the Hand Tools
-- | YesAlready -> List -> Target: Syneyhil -> Message: Purchase Tools (Lv. 10-19)
-- | YesAlready -> List -> Target: Randwulf -> Message: Nothing -- This is if you've already accepted things, it will just cancel out instead of getting stuck
-- | YesAlready -> List -> Target: Brithael -> Message: Nothing -- This is if you've already accepted things, it will just cancel out instead of getting stuck
-- | 
-- | Artisan -> Settings -> Automatice Action Execution Mode -> Checkmark to enable
-- | Artisan -> Settings -> Standard Recipe Solver Settings -> Max Quality: 0%
-- | Artisan -> Inside each crafting list -> List Settings -> Automatic Repairs 50%
-- | Artisan -> Inside each crafting list -> List Settings -> Set new items added to list as quick synth
-- | 
-- | Artisan Crafting Lists: Copy the gibberish after the -> then click on 'Import List From Clipboard (Artisan Export)
-- | Import 1-12 -> {"SkipLiteral":false,"RepairPercent":50,"AddAsQuickSynth":true,"ID":888888,"Name":"1-12 Lazy Crafter","Recipes":[{"ID":2,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":3,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":4,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":5,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":6,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":7,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":9,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":8,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":2071,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":10,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":12,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":14,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":13,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":15,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":17,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":16,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":2072,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":19,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":21,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":2073,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":22,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":23,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":26,"Quantity":1,"ListItemOptions":{"NQOnly":false,"Skipping":false}},{"ID":24,"Quantity":1,"ListItemOptions":{"NQOnly":true,"Skipping":false}},{"ID":29,"Quantity":1,"ListItemOptions":{"NQOnly":true,"Skipping":false}},{"ID":31,"Quantity":1,"ListItemOptions":{"NQOnly":true,"Skipping":false}}],"ExpandedList":[2,3,4,5,6,7,9,8,2071,10,12,14,13,15,17,16,2072,19,21,2073,22,23,26],"SkipIfEnough":false,"Materia":false,"Repair":true}
-- | Import 12-24 -> {"SkipLiteral":false,"RepairPercent":50,"AddAsQuickSynth":true,"ID":999999,"Name":"12-25 Lazy Crafter","Recipes":[{"ID":27,"Quantity":1,"ListItemOptions":{"NQOnly":true,"Skipping":false}},{"ID":28,"Quantity":1,"ListItemOptions":{"NQOnly":true,"Skipping":false}},{"ID":34,"Quantity":1,"ListItemOptions":{"NQOnly":true,"Skipping":false}},{"ID":32,"Quantity":1,"ListItemOptions":{"NQOnly":true,"Skipping":false}},{"ID":33,"Quantity":1,"ListItemOptions":{"NQOnly":true,"Skipping":false}},{"ID":35,"Quantity":1,"ListItemOptions":{"NQOnly":true,"Skipping":false}},{"ID":37,"Quantity":1,"ListItemOptions":{"NQOnly":true,"Skipping":false}},{"ID":39,"Quantity":1,"ListItemOptions":{"NQOnly":true,"Skipping":false}},{"ID":2074,"Quantity":1,"ListItemOptions":{"NQOnly":true,"Skipping":false}},{"ID":42,"Quantity":1,"ListItemOptions":{"NQOnly":true,"Skipping":false}},{"ID":43,"Quantity":396,"ListItemOptions":{"NQOnly":true,"Skipping":false}},{"ID":51,"Quantity":99,"ListItemOptions":{"NQOnly":true,"Skipping":false}}],"ExpandedList":[24,29,31,27,28,34,32,33,35,37,39,2074,42,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51],"SkipIfEnough":false,"Materia":false,"Repair":true}
-- | 
-- | -- IMPORTANT NOTE: After importing crafting lists:
-- |   1. Item IDs will be different from the original lists you just copied
-- |   2. Verify in Artisan -> Craft Lists for the correct IDs before starting
-- |   3. Update local crafting_lists -> left/middle/right profiles (line 194) to match the new imported lists for each client
-- |   4. In each imported list, open the crafting list, list settings, make sure automatic repairs is enabled at 50% and set new items to list as quick synth
-- | 
-- | -- VERY IMPORTANT NOTE: Make a plugin collection just for Artisan:
-- |   1. You will want to have Artisan inside a plugins collection
-- |   2. /xlplugins -> Installed Plugins -> Plugin Collection -> + -> New Collection is added, click the Edit pencil -> Rename the collection up top -> Artisan -> Add a Plugin! -> Artisan
-- |   3. Do not have Artisan in any other plugin collection or the level monitoring will fail to force stop crafting
-- |   4. Enable the collection once you have this made, before starting the script
-- └-----------------------------------------------------------------------------------------------------------------------
-- ┌-----------------------------------------------------------------------------------------------------------------------
-- | Approx Time To Complete On World Boosted Server: 27 minutes
-- | Approx Time To Complete On Non-World Boosted Server: 39 minutes
-- | 
-- | Current Issues:
-- |  - If You're Missing Items In Upper Decks, It Teleports Back And Collects The Needed Items,
-- |  - But If The Missing Items Are In Upper Decks It Tries To Run In A Wild Non-Reachable
-- |  - Location, So I Need To Figure Out To To Force It To /li Aftcastle /wait 12 Instead
-- |  - If this happens, just throw something on the ground that is a cheap buy
-- | 
-- | To Do: But I'll Probably Never Do This So Help Yourself
-- |  - To Resolve The Above Issues, I Was Planning On Adding A Zone Id Checker So If We're In
-- |  - 129 (Lower) It Will Know Only Engerrand, Sorcha, Iron_Thunder, Syneyhil Are Here
-- |  - 128 (Upper) It Will Know Only Syneyhil, Soemrwyb Are Here
-- |  - This Way If The NPC Is Located In The Same Zone It Will Route To, If Not It Will Go
-- |  - To Lower Decks First, Then /li Aftcastle If Needed
-- |  - Could Also Figure A Way To Check Right After Purchasing Before Moving To The Next Step
-- └-----------------------------------------------------------------------------------------------------------------------
-- ┌-----------------------------------------------------------------------------------------------------------------------
-- | FAQ:
-- | Q: Can I Ignore The Left/Right/Middle Settings? Wtf Is All This Shit?
-- | A: This Is If You're Running Up To 3 Clients At The Same Time, If You're Only Running 1 toon, Just Leave local position = "left" And Update Your crafting_lists For left.
-- | 
-- | Q: I Don't Have A Tony, I Don't Have Another Game Client, What Should I Do?
-- | A: You Should Load Up Your Character Somehow With The Gil And Fire Shards You Need.
-- | 
-- | Q: What Happens If I Run Out Of Gil Or Fire Shards During Crafting?
-- | A: This Shouldn't Happen With The Current Crafting List, If You Make Another List, Check Your Requirements, And Probably Add Other NPCs As Well.
-- | 
-- | Q: What Do I Do If The Crafting Process Stops Early?
-- | A: Check If You’ve Reached The Required Crafting Level. The Script Is Designed To Stop Once You Hit Level 12 Or 25, And It Will Then Proceed With The Next Phase.
-- | 
-- | Q: I Received An Error Message About A Missing Item. What Should I Do?
-- | A: This Error Likely Means You’re Missing A Key Crafting Material. The Script Checks For Required Items, But If Something Is Missing, Ensure You Have Enough Materials To Craft All Items In Your List.
-- | 
-- | Q: Do I Need Auto Repairs Enabled For This Script?
-- | A: Yes, If You've Updated Your Artisan Import Settings It Should Have This Selected Already.
-- | 
-- | Q: Can I Customize The NPC Vendor Coordinates?
-- | A: Yes, You Can Edit The Vendor Coordinates Directly In The Script If You Find Your NPCs In Different Locations Or Playing On A Different Server.
-- |    SND -> Engines.Native.Run ("/e " .. Entity.Player.Position.X .. ", " .. Entity.Player.Position.Y .. ", " .. Entity.Player.Position.Z)
-- | 
-- | If you have any other questions just ping me.
-- | 
-- | @_xa_
-- └-----------------------------------------------------------------------------------------------------------------------

-- DO NOT TOUCH THESE LINES BELOW
require("dfunc")
require("xafunc")
DisableARMultiXA()
EnableArtisanXA() -- Artisan Collection
rsrXA("off")
DisableSprintingInTownXA()
if not CheckPluginEnabledXA({"Artisan", "Dropbox", "Lifestream", "vnavmesh", "AutoRetainer", "PandorasBox", "TextAdvance"}) then return end
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

local min_gil_keep = 85000 -- Minimum amount of gil to keep
local gil_buffer = 40000 -- Buffer to ignore missing gil if less than this amount
local min_fire_shards = 600 -- [400] for boosted world -- [600] for non-boosted world
local zone_id = 129 -- Zone ID for Limsa Lominsa Lower Decks
position = "left" -- Default position to change between "left", "middle", or "right" (must be global for get_coordinates function) 

local delay_lists = {left = 1, middle = 2, right = 3} -- Add custom delay so you're not all stacking if using multiple toons

local function get_delay()
    return delay_lists[position]
end

-- The ID's you are given in /artisan crafting lists screen will go here, if the numbers are wrong, nothing will happen
local crafting_lists = {
    left = {levels_1_12 = 888888, levels_12_25 = 999999},
    middle = {levels_1_12 = 888888, levels_12_25 = 999999},
    right = {levels_1_12 = 888888, levels_12_25 = 999999}
}

local min_bronze_ingot = 48
local min_bronze_rivets = 6
local min_maple_lumber = 16
local min_bone_chip = 3
local min_fish_oil = 4
local min_animal_glue = 1
local min_clove_oil = 1
local min_copper_ore = 2
local min_ragstone_whetstone = 5
local min_brass_ingot = 1
local min_bronze_plate = 1
local min_ash_lumber = 13
local min_hard_leather = 2
local min_jellyfish_humours = 1
local min_iron_ore = 1287
local min_leather = 2

-- -------------------------------------
-- -- End of Configuration Parameters --
-- -------------------------------------

-- ------------------------
-- -- Start of Functions --
-- ------------------------

local function get_crafting_list(level_range)
    local lists = crafting_lists[position]
    return lists[level_range]
end

local engerrand_items = {
    {menu_index = 14, item_id = 5056, name = "Bronze Ingot", min_count = min_bronze_ingot},
    {menu_index = 16, item_id = 5091, name = "Bronze Rivets", min_count = min_bronze_rivets},
    {menu_index = 17, item_id = 5361, name = "Maple Lumber", min_count = min_maple_lumber},
    {menu_index = 26, item_id = 5432, name = "Bone Chip", min_count = min_bone_chip},
    {menu_index = 29, item_id = 5482, name = "Fish Oil", min_count = min_fish_oil},
    {menu_index = 33, item_id = 5503, name = "Animal Glue", min_count = min_animal_glue}
}

local sorcha_items = {
    {menu_index = 0, item_id = 4204, name = "Fang Earrings", min_count = 1},
    {menu_index = 6, item_id = 4307, name = "Copper Choker", min_count = 1},
    {menu_index = 13, item_id = 4095, name = "Brass Wristlets of Crafting", min_count = 1},
    {menu_index = 17, item_id = 4431, name = "Brass Ring of Crafting", min_count = 1},
    {menu_index = 17, item_id = 4431, name = "Brass Ring of Crafting", min_count = 1}
}

local iron_thunder_items = {
    {menu_index = 1, item_id = 2660, name = "Amateur's Headgear", min_count = 1},
    {menu_index = 7, item_id = 3019, name = "Hempen Doublet Vest of Crafting", min_count = 1},
    {menu_index = 12, item_id = 3536, name = "Amateur's Smithing Gloves", min_count = 1},
    {menu_index = 17, item_id = 3317, name = "Hempen Bottoms", min_count = 1},
    {menu_index = 21, item_id = 3768, name = "Amateur's Thighboots", min_count = 1}
}

local syneyhil_items = {
    {menu_index = 4, item_id = 2342, name = "Amateur's Cross-Pein Hammer", min_count = 1},
    {menu_index = 7, item_id = 2356, name = "Bronze File", min_count = 1}
}

local smydhaemr_items = {
    {menu_index = 0, item_id = 4856, name = "Clove Oil", min_count = min_clove_oil},
    {menu_index = 1, item_id = 5106, name = "Copper Ore", min_count = min_copper_ore},
    {menu_index = 3, item_id = 5258, name = "Ragstone Whetstone", min_count = min_ragstone_whetstone},
    {menu_index = 4, item_id = 5063, name = "Brass Ingot", min_count = min_brass_ingot},
    {menu_index = 5, item_id = 5071, name = "Bronze Plate", min_count = min_bronze_plate},
    {menu_index = 7, item_id = 5364, name = "Ash Lumber", min_count = min_ash_lumber},
    {menu_index = 11, item_id = 5276, name = "Hard Leather", min_count = min_hard_leather},
    {menu_index = 15, item_id = 5483, name = "Jellyfish Humours", min_count = min_jellyfish_humours}
}

local soemrwyb_items = {
    {menu_index = 2, item_id = 5111, name = "Iron Ore", min_count = min_iron_ore},
    {menu_index = 8, item_id = 5275, name = "Leather", min_count = min_leather}
}

local tony_coords = {
    left = {-108.59882354736, 18.000156402588, 10.385614395142},
    middle = {-108.7314453125, 18.000156402588, 9.9278326034546},
    right = {-108.88091278076, 18.000152587891, 9.3883771896362}
}

local engerrand_coords = {
    left = {{-130.77789306641, 18.200000762939, 23.897005081177}, {-129.94384765625, 18.200000762939, 25.552606582642}},
    middle = {{-131.22825622559, 18.200000762939, 24.116233825684}, {-130.51734924316, 18.200000762939, 25.807521820068}},
    right = {{-132.09976196289, 18.200000762939, 24.492063522339}, {-131.42776489258, 18.200000762939, 26.096347808838}}
}

local sorcha_coords = {
    left = {{-135.98805236816, 18.200000762939, 15.266785621643}},
    middle = {{-135.02648925781, 18.200000762939, 14.921815872192}},
    right = {{-134.2891998291, 18.200000762939, 14.573122024536}}
}

local iron_thunder_coords = {
    left = {{-155.70422363281, 18.199998855591, 25.301961898804}, {-156.3777923584, 18.200000762939, 23.581928253174}},
    middle = {{-154.6499786377, 18.199998855591, 24.96280670166}, {-155.27685546875, 18.200000762939, 23.528774261475}},
    right = {{-153.9615020752, 18.200000762939, 24.517431259155}, {-154.67851257324, 18.200000762939, 22.850835800171}}
}

local syneyhil_coords = {
    left = {{-248.42317199707, 16.200000762939, 41.548633575439}, {-248.40689086914, 16.200000762939, 39.900135040283}},
    middle = {{-247.2622833252, 16.200000762939, 41.621208190918}, {-247.35678100586, 16.200000762939, 39.914356231689}},
    right = {{-246.11773681641, 16.200000762939, 41.621524810791}, {-246.13233947754, 16.200000762939, 39.888523101807}}
}

local aethernet_coords = {
    left = {{-215.34873962402, 15.999086380005, 49.07398223877}},
    middle = {{-215.86627197266, 15.999101638794, 49.499584197998}},
    right = {{-216.14912414551, 15.99910736084, 50.113075256348}}
}

local smydhaemr_coords = {
    left = {{-25.55884552002, 42.499382019043, 199.65979003906}, {-28.056787490845, 42.499488830566, 198.52388000488}},
    middle = {{-25.55884552002, 42.499382019043, 199.65979003906}, {-28.039258956909, 42.499488830566, 197.98785400391}},
    right = {{-25.55884552002, 42.499382019043, 199.65979003906}, {-27.486181259155, 42.499462127686, 197.45043945313}}
}

local blacksmith_guild_coords = {
    left = {{-46.788990020752, 42.799995422363, 197.74812316895}, {-50.63362121582, 42.799926757813, 195.18067932129}},
    middle = {{-46.788990020752, 42.799995422363, 197.74812316895}, {-50.108211517334, 42.79988861084, 194.6329498291}},
    right = {{-46.788990020752, 42.799995422363, 197.74812316895}, {-49.445617675781, 42.800003051758, 193.94955444336}}
}

local brithael_coords = {
    left = {{-32.89733505249, 44.499950408936, 182.41342163086}, {-31.523557662964, 44.499984741211, 184.62544250488}},
    middle = {{-33.803462982178, 44.674991607666, 183.28169250488}, {-31.920627593994, 44.571308135986, 184.92184448242}},
    right = {{-34.574157714844, 44.674995422363, 184.67687988281}, {-32.420417785645, 44.674995422363, 185.35282897949}}
}

local mender_coords = {
    left = {{19.8249168396, 44.667293548584, 161.3754119873}, {15.814970970154, 44.549350738525, 161.24325561523}},
    middle = {{19.813983917236, 44.667293548584, 160.63967895508}, {15.813989639282, 44.549350738525, 160.51599121094}},
    right = {{19.835163116455, 44.667293548584, 159.96101379395}, {15.86612701416, 44.549354553223, 159.93182373047}}
}

local aftcastle_coords = {
    left = {{92.254837036133, 40.275371551514, 68.429870605469}},
    middle = {{92.254837036133, 40.275371551514, 68.967956542969}},
    right = {{92.254837036133, 40.275371551514, 69.584114074707}}
}

local function MonitorJobLevel(target_level, next_step, pjob)
    local characterLevel = GetLevel(pjob)
    
    while characterLevel < target_level do
        SleepXA(5)
        characterLevel = GetLevel(pjob)
    end
    
    EchoXA("Force stop crafting as we've reached level " .. target_level .. ".")
    
    DisableArtisanXA() -- Stop the crafting
    SleepXA(5) -- Brief wait to let the profile stop
    
    while not GetCharacterCondition(1) do
        CloseCraftingWindowsXA()
    end
    
    EnableArtisanXA()
    SleepXA(5)
    
    next_step()
end

local function buy_in_batches(item_data, max_per_purchase)
    local item_count = GetItemCount(item_data.item_id)
    local needed = item_data.min_count - item_count
    
    if needed > 0 then
        local batches = math.ceil(needed / max_per_purchase)
        
        for i = 1, batches do
            local to_buy = math.min(max_per_purchase, needed)
            callbackXA("Shop True 0 " .. item_data.menu_index .. " " .. to_buy)
            SleepXA(2)
            needed = needed - to_buy -- Reduce the remaining amount needed
        end
    end
end

local function all_items_in_stock(items)
    for _, item_data in pairs(items) do
        local item_count = GetItemCount(item_data.item_id)
        if item_count < item_data.min_count then
            return false -- Missing items
        end
    end
    return true -- All items are stocked
end

local function buy_missing_items(vendor_name, items, coords)
    local missing_items = false

    for _, item_data in pairs(items) do
        local item_count = GetItemCount(item_data.item_id)
        if item_count < item_data.min_count then
            missing_items = true
            break
        end
    end -- This closes the for loop

    if missing_items then
        move_to(coords)
        SleepXA(1)
        ResetCameraXA()
        SleepXA(1)
        TargetXA(vendor_name)
        SleepXA(1)
        InteractXA()
        SleepXA(1)

        for _, item_data in pairs(items) do
            local item_count = GetItemCount(item_data.item_id)
            if item_count < item_data.min_count then
                buy_in_batches(item_data, 99) -- Assuming 99 is the maximum purchase limit
            end
        end -- This closes the inner for loop

        zungazunga()
		callbackXA("SystemMenu true -1") -- Close The Escape Menu If Still Open
        SleepXA(2.5)
    else
        EchoXA("Skipping " .. vendor_name .. ", all items in stock.")
    end
end -- Close buy_missing_items function

-- ----------------------
-- -- End of Functions --
-- ----------------------

-- ------------------------------
-- -- Start of XA Lazy Crafter --
-- ------------------------------

local function LazyCrafterXA()
    EnableTextAdvanceXA()
    RemoveSproutXA()
    EchoXA("Starting the process: Applying delay of " .. get_delay() .. " seconds.")

    if get_delay() > 0 then
        SleepXA(get_delay())
        EchoXA("Delay of " .. get_delay() .. " seconds completed.")
        EchoXA("Starting Lazy Crafter 1-25 process...")
    end

    EchoXA("Checking if already in Limsa Lominsa Lower Decks...")

    if GetZoneID() == zone_id then
        EchoXA("Already in Limsa Lominsa Lower Decks. Checking Fire Shards...")
    else
        EchoXA("Not in Limsa Lominsa Lower Decks. Teleporting now.")
        LifestreamCmdXA("Limsa Lominsa Lower Decks")
    end

    local function check_needed_items()
        local fire_shards_shortfall = min_fire_shards - GetItemCount(2)
        local gil_shortfall = min_gil_keep - GetItemCount(1)
        local items_needed = false

        if fire_shards_shortfall > 0 or gil_shortfall > gil_buffer then
            EchoXA("-------------")
            EchoXA("Items Needed:")
            items_needed = true
        end

        if fire_shards_shortfall > 0 then
            EchoXA("Fire Shards: " .. fire_shards_shortfall)
        end
        if gil_shortfall > gil_buffer then
            EchoXA("Gil: " .. gil_shortfall)
        end

        if items_needed then
            EchoXA("-------------")
        else
            EchoXA("All required items are in stock.")
        end

        return items_needed
    end

    if check_needed_items() then
        EchoXA("Moving to Tony's location for needed items.")
        EchoXA("-------------")
        coords = get_coordinates(tony_coords)
        move_to(coords)

        while GetItemCount(2) < min_fire_shards or GetItemCount(1) < min_gil_keep do
            local fire_shards_shortfall = min_fire_shards - GetItemCount(2)
            local gil_shortfall = min_gil_keep - GetItemCount(1)
            EchoXA("Items Needed:")
            if fire_shards_shortfall > 0 then
                EchoXA("Fire Shards: " .. fire_shards_shortfall)
            end
            if gil_shortfall > gil_buffer then
                EchoXA("Gil: " .. gil_shortfall)
            end
            EchoXA("-------------")
            SleepXA(3)
        end
        EchoXA("All items received, ready to begin!")
    else
        EchoXA("All required items already in stock. Skipping Tony.")
    end

    SleepXA(1)
    EchoXA("Checking inventory for missing items...")

    if not all_items_in_stock(engerrand_items) then
        coords = get_coordinates(engerrand_coords)
        move_to(coords)
        buy_missing_items("Engerrand", engerrand_items, engerrand_coords)
    else
        EchoXA("Skipping Engerrand, all items in stock.")
    end

    if not all_items_in_stock(sorcha_items) then
        coords = get_coordinates(sorcha_coords)
        move_to(coords)
        buy_missing_items("Sorcha", sorcha_items, sorcha_coords)
    else
        EchoXA("Skipping Sorcha, all items in stock.")
    end

    if not all_items_in_stock(iron_thunder_items) then
        coords = get_coordinates(iron_thunder_coords)
        move_to(coords)
        buy_missing_items("Iron Thunder", iron_thunder_items, iron_thunder_coords)
    else
        EchoXA("Skipping Iron Thunder, all items in stock.")
    end

    if not all_items_in_stock(syneyhil_items) then
        coords = get_coordinates(syneyhil_coords)
        move_to(coords)
        buy_missing_items("Syneyhil", syneyhil_items, syneyhil_coords)
    else
        EchoXA("Skipping Syneyhil, all items in stock.")
    end

    coords = get_coordinates(aethernet_coords)
    move_to(coords)

    LifestreamCmdXA("Aftcastle")

    if not all_items_in_stock(smydhaemr_items) then
        coords = get_coordinates(smydhaemr_coords)
        move_to(coords)
        buy_missing_items("Smydhaemr", smydhaemr_items, smydhaemr_coords)
    else
        EchoXA("Skipping Smydhaemr, all items in stock.")
    end

    if not all_items_in_stock(soemrwyb_items) then
        coords = get_coordinates(smydhaemr_coords) -- Assuming they use the same coordinates
        move_to(coords)
        buy_missing_items("Soemrwyb", soemrwyb_items, smydhaemr_coords)
    else
        EchoXA("Skipping Soemrwyb, all items in stock.")
    end

    EchoXA("Final confirmation of all items...")

    local missing_items = false

    if not all_items_in_stock(engerrand_items) then missing_items = true end
    if not all_items_in_stock(sorcha_items) then missing_items = true end
    if not all_items_in_stock(iron_thunder_items) then missing_items = true end
    if not all_items_in_stock(syneyhil_items) then missing_items = true end
    if not all_items_in_stock(smydhaemr_items) then missing_items = true end
    if not all_items_in_stock(soemrwyb_items) then missing_items = true end

    if missing_items then
        EchoXA("Missing items detected before crafting, teleporting back to Limsa Lominsa.")
        LifestreamCmdXA("Limsa Lominsa Lower Decks")
        
        if not all_items_in_stock(engerrand_items) then
            coords = get_coordinates(engerrand_coords)
            move_to(coords)
            buy_missing_items("Engerrand", engerrand_items, engerrand_coords)
        end
        if not all_items_in_stock(sorcha_items) then
            coords = get_coordinates(sorcha_coords)
            move_to(coords)
            buy_missing_items("Sorcha", sorcha_items, sorcha_coords)
        end
        if not all_items_in_stock(iron_thunder_items) then
            coords = get_coordinates(iron_thunder_coords)
            move_to(coords)
            buy_missing_items("Iron Thunder", iron_thunder_items, iron_thunder_coords)
        end
        if not all_items_in_stock(syneyhil_items) then
            coords = get_coordinates(syneyhil_coords)
            move_to(coords)
            buy_missing_items("Syneyhil", syneyhil_items, syneyhil_coords)
        end
        if not all_items_in_stock(smydhaemr_items) then
            coords = get_coordinates(smydhaemr_coords)
            move_to(coords)
            buy_missing_items("Smydhaemr", smydhaemr_items, smydhaemr_coords)
        end
        if not all_items_in_stock(soemrwyb_items) then
            coords = get_coordinates(smydhaemr_coords) -- Assuming they use the same coordinates
            move_to(coords)
            buy_missing_items("Soemrwyb", soemrwyb_items, smydhaemr_coords)
        end
        EchoXA("All missing items purchased, ready to unlock crafting.")
    else
        EchoXA("All items confirmed in stock, proceeding to unlock crafting.")
    end

    coords = get_coordinates(blacksmith_guild_coords)
    move_to(coords)

    SleepXA(1)
    ResetCameraXA()
    SleepXA(1)
    TargetXA("Randwulf")
    SleepXA(1)
    InteractXA()
    CharacterSafeWaitXA()
    TargetXA("Randwulf")
    SleepXA(1)
    InteractXA()
    CharacterSafeWaitXA()

    coords = get_coordinates(brithael_coords)
    move_to(coords)

    SleepXA(1)
    ResetCameraXA()
    SleepXA(1)
    TargetXA("Brithael")
    SleepXA(1)
    InteractXA()
    CharacterSafeWaitXA()

    coords = get_coordinates(mender_coords)
    move_to(coords)

    ResetCameraXA()
    SleepXA(1)

    local function is_near_mender(stop_distance)
        local playerX = GetPlayerRawXPos()
        local playerY = GetPlayerRawYPos()
        local playerZ = GetPlayerRawZPos()
        local menderX, menderY, menderZ = table.unpack(get_coordinates(mender_coords)[2])
        local distance = math.sqrt((playerX - menderX)^2 + (playerY - menderY)^2 + (playerZ - menderZ)^2)
        return distance <= stop_distance
    end

    if not is_near_mender(2) then
        EchoXA("Not near the mender. Moving to mender's location.")
        local mender_coords_temp = get_coordinates(mender_coords)
        move_to(mender_coords_temp[2])
    else
        EchoXA("Already near the mender, skipping movement.")
    end

    SleepXA(1)
    yield("/equip 2340")
    EchoXA("Attempting to equip hammer. CBT #1")
    SleepXA(1)
    yield("/equip 2340")
    EchoXA("Attempting to equip hammer. CBT #2")
    SleepXA(1)
    yield("/equip 2340")
    EchoXA("Attempting to equip hammer. CBT #3")
    SleepXA(1)
    EquipRecommendedGearXA()
    EchoXA("All items checked, ready to craft!")

    EchoXA("Starting crafting 1-12")
    local list_id = get_crafting_list("levels_1_12")
    yield("/artisan lists " .. list_id .. " start")
    SleepXA(60)
    MonitorJobLevel(12, function()
        yield("/send ESCAPE")
        SleepXA(0.5)
        EquipRecommendedGearXA()
        SleepXA(0.5)
        EchoXA("Starting crafting 12-25")
        list_id = get_crafting_list("levels_12_25")
        yield("/artisan lists " .. list_id .. " start")
        SleepXA(60)
        MonitorJobLevel(25, function()
            EchoXA("Crafting completed at level 25.")
            coords = get_coordinates(aftcastle_coords)
            SleepXA(2)
            yield("/ays discard")
            move_to(coords)
            while AutoRetainerIsBusyXA() do

                SleepXA(1)
            end
        end)
    end)
    SleepXA(2)
end

local function XALazyCrafter()
    for _, owner in ipairs(franchise_owners) do
        local character = owner[1]
        EchoXA("Logging in as " .. character)
        ARRelogXA(character)
        LazyCrafterXA()
    end
    LogoutXA()
    EnableARMultiXA()
end

XALazyCrafter()

-- ----------------------------
-- -- End of XA Lazy Crafter --
-- ----------------------------
