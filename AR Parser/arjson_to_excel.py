import json
import xlsxwriter
import argparse
import os
import datetime
import sys
from pathlib import Path
import getpass
import sqlite3

# ===============================================
# Account locations + global data
# ===============================================
user = getpass.getuser()

def acc(nickname, pluginconfigs_path, include_altoholic=True):  # Note: Default will use INCLUDE_ALTOHOLIC_BY_DEFAULT at runtime
    auto_path = os.path.join(pluginconfigs_path, "AutoRetainer", "DefaultConfig.json")
    alto_path = os.path.join(pluginconfigs_path, "Altoholic", "altoholic.db")
    
    return {
        "nickname": nickname,
        "auto_path": auto_path,
        "alto_path": alto_path,
        "include_altoholic": bool(include_altoholic),
    }

account_locations = [
     acc("Main",   f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs"),
   # acc("Acc1",   f"C:\\Users\\{user}\\AltData\\Acc1\\pluginConfigs"),
   # acc("Acc2",   f"C:\\Users\\{user}\\AltData\\Acc2\\pluginConfigs"),
   # acc("Acc3",   f"C:\\Users\\{user}\\AltData\\Acc3\\pluginConfigs"),
]

all_fc_data = {}
all_characters = []

# ===============================================
# CONFIG: Altoholic integration
# ===============================================
INCLUDE_ALTOHOLIC_BY_DEFAULT = True

# Item IDs to aggregate
TANK_ITEM_ID = 10155   # "Tanks"
KITS_ITEM_ID = 10373   # "Kits"

# Treasure values (gil) per item id
TREASURE_VALUES = {
    22500: 8000,   # Salvaged Ring
    22501: 9000,   # Salvaged Bracelet
    22502: 10000,  # Salvaged Earring
    22503: 13000,  # Salvaged Necklace
    22504: 27000,  # Extravagant Salvaged Ring
    22505: 28500,  # Extravagant Salvaged Bracelet
    22506: 30000,  # Extravagant Salvaged Earring
    22507: 34500,  # Extravagant Salvaged Necklace
}
TREASURE_IDS = set(TREASURE_VALUES.keys())

# ===============================================
# Region mapping by world
# ===============================================
NA_WORLDS = {
    "adamantoise","cactuar","faerie","gilgamesh","jenova","midgardsormr","sargatanas","siren",
    "balmung","brynhildr","coeurl","diabolos","goblin","malboro","mateus","zalera",
    "behemoth","excalibur","exodus","famfrit","hyperion","lamia","leviathan","ultros",
    "cuchulainn","golem","halicarnassus","kraken","maduin","marilith","rafflesia","seraph"
}
EU_WORLDS = {
    "cerberus","louisoix","moogle","omega","phantom","ragnarok","sagittarius","spriggan",
    "alpha","lich","odin","phoenix","raiden","shiva","twintania","zodiark"
}
OCE_WORLDS = {"bismarck","ravana","sephirot","sophia","zurvan"}
JP_WORLDS = {
    "aegis","atomos","carbuncle","garuda","gungnir","kujata","tonberry","typhon",
    "alexander","bahamut","durandal","fenrir","ifrit","ridill","tiamat","ultima",
    "anima","asura","chocobo","hades","ixion","masamune","pandaemonium","titan",
    "belias","mandragora","ramuh","shinryu","unicorn","valefor","yojimbo","zeromus"
}

def region_from_world(world: str) -> str:
    if not world:
        return ""
    w = str(world).strip().lower()
    if w in NA_WORLDS: return "NA"
    if w in EU_WORLDS: return "EU"
    if w in OCE_WORLDS: return "OCE"
    if w in JP_WORLDS: return "JP"
    return ""  # unknown/uncategorized

# ===============================================
# Submarine Part Constants
# ===============================================
SUB_PARTS_LOOKUP = {
    21792: "Shark-class Bow",
    21793: "Shark-class Bridge",
    21794: "Shark-class Pressure Hull",
    21795: "Shark-class Stern",
    21796: "Unkiu-class Bow",
    21797: "Unkiu-class Bridge",
    21798: "Unkiu-class Pressure Hull",
    21799: "Unkiu-class Stern",
    22526: "Whale-class Bow",
    22527: "Whale-class Bridge",
    22528: "Whale-class Pressure Hull",
    22529: "Whale-class Stern",
    23903: "Coelacanth-class Bow",
    23904: "Coelacanth-class Bridge",
    23905: "Coelacanth-class Pressure Hull",
    23906: "Coelacanth-class Stern",
    24344: "Syldra-class Bow",
    24345: "Syldra-class Bridge",
    24346: "Syldra-class Pressure Hull",
    24347: "Syldra-class Stern",
    24348: "Modified Shark-class Bow",
    24349: "Modified Shark-class Bridge",
    24350: "Modified Shark-class Pressure Hull",
    24351: "Modified Shark-class Stern",
    24352: "Modified Unkiu-class Bow",
    24353: "Modified Unkiu-class Bridge",
    24354: "Modified Unkiu-class Pressure Hull",
    24355: "Modified Unkiu-class Stern",
    24356: "Modified Whale-class Bow",
    24357: "Modified Whale-class Bridge",
    24358: "Modified Whale-class Pressure Hull",
    24359: "Modified Whale-class Stern",
    24360: "Modified Coelacanth-class Bow",
    24361: "Modified Coelacanth-class Bridge",
    24362: "Modified Coelacanth-class Pressure Hull",
    24363: "Modified Coelacanth-class Stern",
    24364: "Modified Syldra-class Bow",
    24365: "Modified Syldra-class Bridge",
    24366: "Modified Syldra-class Pressure Hull",
    24367: "Modified Syldra-class Stern"
}

CLASS_SHORTCUTS = {
    "Shark-class": "S",
    "Unkiu-class": "U",
    "Whale-class": "W",
    "Coelacanth-class": "C",
    "Syldra-class": "Y",
    "Modified Shark-class": "S+",
    "Modified Unkiu-class": "U+",
    "Modified Whale-class": "W+",
    "Modified Coelacanth-class": "C+",
    "Modified Syldra-class": "Y+"
}

# ===============================================
# Altoholic scanning helpers
# ===============================================
def _safe_json_load(s):
    if not s or s == "null":
        return None
    try:
        return json.loads(s)
    except Exception:
        return None

def scan_altoholic_db(db_path):
    """
    Scan a single Altoholic DB and return a mapping:
      { CharacterId: {"tank": int, "kits": int, "treasure_value": int} }
    (Region is now derived from World, not the DB.)
    """
    result = {}
    if not os.path.isfile(db_path):
        return result

    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        rows = cur.execute("SELECT CharacterId, Inventory, Saddle FROM characters").fetchall()
        for char_id, inv_json, saddle_json in rows:
            tank = 0
            kits = 0
            treasure_value = 0

            def consume(items):
                nonlocal tank, kits, treasure_value
                if not items:
                    return
                for it in items:
                    iid = it.get("ItemId", 0)
                    qty = it.get("Quantity", 1)
                    if not isinstance(qty, int):
                        try:
                            qty = int(qty)
                        except Exception:
                            qty = 1
                    if iid == TANK_ITEM_ID:
                        tank += qty
                    elif iid == KITS_ITEM_ID:
                        kits += qty
                    if iid in TREASURE_IDS:
                        treasure_value += qty * TREASURE_VALUES[iid]

            inv = _safe_json_load(inv_json)
            if isinstance(inv, list):
                consume(inv)
            sad = _safe_json_load(saddle_json)
            if isinstance(sad, list):
                consume(sad)

            if tank or kits or treasure_value:
                result[int(char_id)] = {
                    "tank": int(tank),
                    "kits": int(kits),
                    "treasure_value": int(treasure_value),
                }
        con.close()
    except Exception as e:
        print(f"[WARNING] Failed to scan Altoholic DB '{db_path}': {e}")
    return result

# ===============================================
# Existing helpers
# ===============================================
def extract_fc_data(full_data):
    fc_data = {}
    def recursive_search(obj):
        if isinstance(obj, dict):
            if "HolderChara" in obj:
                holder_id = obj["HolderChara"]
                fc_data[holder_id] = {
                    "Name": obj.get("Name", "Unknown FC"),
                    "FCPoints": obj.get("FCPoints", 0)
                }
            for v in obj.values():
                recursive_search(v)
        elif isinstance(obj, list):
            for item in obj:
                recursive_search(item)
    recursive_search(full_data)
    return fc_data

def collect_characters(full_data, account_nickname):
    all_chars = []
    def assign_nickname(chara):
        chara["AccountNickname"] = account_nickname
        return chara

    if isinstance(full_data, dict):
        if "OfflineData" in full_data and isinstance(full_data["OfflineData"], list):
            for c in full_data["OfflineData"]:
                if isinstance(c, dict) and "CID" in c:
                    all_chars.append(assign_nickname(c))
        else:
            for _, value in full_data.items():
                if isinstance(value, dict) and "CID" in value:
                    all_chars.append(assign_nickname(value))
    elif isinstance(full_data, list):
        for item in full_data:
            if isinstance(item, dict) and "CID" in item:
                all_chars.append(assign_nickname(item))
    return all_chars

def shorten_part_name(full_name: str) -> str:
    for prefix, code in CLASS_SHORTCUTS.items():
        if full_name.startswith(prefix):
            return code
    return "?"

def get_sub_parts_string(sub_data: dict) -> str:
    parts = []
    for key in ["Part1", "Part2", "Part3", "Part4"]:
        part_id = sub_data.get(key, 0)
        if part_id != 0:
            full_part_name = SUB_PARTS_LOOKUP.get(part_id, f"Unknown({part_id})")
            short_code = shorten_part_name(full_part_name)
            parts.append(short_code)
    return "".join(parts)

def build_char_summaries(all_characters, fc_data, alto_map):
    char_summaries = []
    for char in all_characters:
        cid = char.get("CID", 0)
        char_name = char.get("Name", "Unknown")
        world = char.get("World", "Unknown")
        char_gil = char.get("Gil", 0)
        nickname = char.get("AccountNickname", "UnknownAcct")

        retainer_data = char.get("RetainerData", [])
        total_ret_gil = 0
        for ret in retainer_data:
            gil = ret.get("Gil", 0)
            total_ret_gil += gil

            if "MBItems" not in ret:
                ret["MBItems"] = len(ret.get("MarketBoardItems", []))
            if isinstance(ret["MBItems"], bool):
                ret["MBItems"] = 1 if ret["MBItems"] else 0

            if "HasVenture" in ret:
                if isinstance(ret["HasVenture"], bool):
                    ret["HasVenture"] = 1 if ret["HasVenture"] else 0
            else:
                ret["HasVenture"] = 1 if ret.get("VentureID", 0) > 0 else 0

            ret["Level"] = ret.get("Level", 0)

        sub_info = char.get("AdditionalSubmarineData", {})
        sub_data_map = {
            "Submersible-1": {"level": 0, "parts": ""},
            "Submersible-2": {"level": 0, "parts": ""},
            "Submersible-3": {"level": 0, "parts": ""},
            "Submersible-4": {"level": 0, "parts": ""},
        }
        for sub_key, sub_dict in sub_info.items():
            if sub_key in sub_data_map:
                sub_data_map[sub_key]["level"] = sub_dict.get("Level", 0)
                sub_data_map[sub_key]["parts"] = get_sub_parts_string(sub_dict)

        fc_name = ""
        fc_points = 0
        if cid in fc_data:
            fc_name = fc_data[cid].get("Name", "")
            fc_points = fc_data[cid].get("FCPoints", 0)

        # Altoholic fields (no region here)
        tank = 0
        kits = 0
        treasure_value = 0
        if isinstance(cid, int) and cid in alto_map:
            tank = alto_map[cid].get("tank", 0)
            kits = alto_map[cid].get("kits", 0)
            treasure_value = alto_map[cid].get("treasure_value", 0)

        # Region is always derived from World
        region = region_from_world(world)

        char_summaries.append({
            "cid": cid,
            "account_nickname": nickname,
            "char_name": char_name,
            "world": world,
            "char_gil": char_gil,
            "retainers": retainer_data,
            "retainer_count": len(retainer_data),
            "total_gil": char_gil + total_ret_gil,
            "fc_name": fc_name,
            "fc_points": fc_points,
            "sub1lvl": sub_data_map["Submersible-1"]["level"],
            "sub1parts": sub_data_map["Submersible-1"]["parts"],
            "sub2lvl": sub_data_map["Submersible-2"]["level"],
            "sub2parts": sub_data_map["Submersible-2"]["parts"],
            "sub3lvl": sub_data_map["Submersible-3"]["level"],
            "sub3parts": sub_data_map["Submersible-3"]["parts"],
            "sub4lvl": sub_data_map["Submersible-4"]["level"],
            "sub4parts": sub_data_map["Submersible-4"]["parts"],
            "tank": tank,
            "kits": kits,
            "treasure_value": treasure_value,
            "region": region,
        })
    return char_summaries

def write_excel(char_summaries, excel_output_path):
    char_summaries.sort(key=lambda x: x["total_gil"], reverse=True)

    try:
        workbook = xlsxwriter.Workbook(excel_output_path)
        worksheet = workbook.add_worksheet("FFXIV Gil Summary")
        summary_sheet = workbook.add_worksheet("Summary")

        header_format = workbook.add_format({
            "bold": True,
            "bg_color": "#CFCFCF",
            "border": 1,
            "align": "left",
            "valign": "vcenter"
        })
        money_format = workbook.add_format({"num_format": "#,##0", "align": "right"})
        total_format = workbook.add_format({
            "num_format": "#,##0",
            "bold": True,
            "align": "right",
            "bg_color": "#E6F2FF"
        })
        char_format = workbook.add_format({"bg_color": "#F2F2F2"})
        date_format = workbook.add_format({"num_format": "yyyy-mm-dd hh:mm:ss"})

        headers = [
            "CID",
            "Account Nickname",
            "Character Name",
            "World",
            "Region",
            "Character Gil",
            "Retainer Name",
            "MBItems",
            "HasVenture",
            "Level",
            "Retainer Gil",
            "Total Gil",
            "FC Name",
            "FC Points",
            "Lvl #1",
            "#1",
            "Lvl #2",
            "#2",
            "Lvl #3",
            "#3",
            "Lvl #4",
            "#4",
            "Tanks",
            "Kits",
            "Treasure Value",
            "Plain Name",
            "List Formatting",
            "SND Formatting",
            "Bagman Formatting"
        ]
        for col_idx, head in enumerate(headers):
            worksheet.write(0, col_idx, head, header_format)

        TANK_COL = headers.index("Tanks")
        KITS_COL = headers.index("Kits")
        TREAS_COL = headers.index("Treasure Value")

        row = 1
        for summary in char_summaries:
            cid = summary["cid"]
            nickname = summary["account_nickname"]
            char_name = summary["char_name"]
            world = summary["world"]
            region = summary.get("region", "")
            char_gil = summary["char_gil"]
            total_gil = summary["total_gil"]
            fc_name = summary["fc_name"]
            fc_points = summary["fc_points"]

            sub1lvl = summary["sub1lvl"]
            sub1parts = summary["sub1parts"]
            sub2lvl = summary["sub2lvl"]
            sub2parts = summary["sub2parts"]
            sub3lvl = summary["sub3lvl"]
            sub3parts = summary["sub3parts"]
            sub4lvl = summary["sub4lvl"]
            sub4parts = summary["sub4parts"]

            tank = summary.get("tank", 0)
            kits = summary.get("kits", 0)
            treasure_value = summary.get("treasure_value", 0)

            plain_nameworld = f"{char_name}@{world}"
            list_nameworld = f"\"{char_name}@{world}\","
            snd_nameworld = f"{{\"{char_name}@{world}\"}},' "
            bagman_nameworld_tony = f"{{\"{char_name}@{world}\", 1, 69,\"Tony Name\"}},"

            retainers = summary["retainers"]

            if not retainers:
                worksheet.write_string(row, 0, str(cid))
                worksheet.write(row, 1, nickname)
                worksheet.write(row, 2, char_name)
                worksheet.write(row, 3, world)
                worksheet.write(row, 4, region)
                worksheet.write_number(row, 5, char_gil, money_format)
                worksheet.write(row, 6, "")
                worksheet.write_number(row, 7, 0, money_format)
                worksheet.write_number(row, 8, 0, money_format)
                worksheet.write_number(row, 9, 0, money_format)
                worksheet.write_number(row, 10, 0, money_format)
                worksheet.write_number(row, 11, total_gil, total_format)
                worksheet.write(row, 12, fc_name)
                worksheet.write_number(row, 13, fc_points, money_format)
                worksheet.write_number(row, 14, sub1lvl)
                worksheet.write(row, 15, sub1parts)
                worksheet.write_number(row, 16, sub2lvl)
                worksheet.write(row, 17, sub2parts)
                worksheet.write_number(row, 18, sub3lvl)
                worksheet.write(row, 19, sub3parts)
                worksheet.write_number(row, 20, sub4lvl)
                worksheet.write(row, 21, sub4parts)
                worksheet.write_number(row, TANK_COL, tank, money_format)
                worksheet.write_number(row, KITS_COL, kits, money_format)
                worksheet.write_number(row, TREAS_COL, treasure_value, total_format if treasure_value else money_format)
                worksheet.write(row, 25, plain_nameworld)
                worksheet.write(row, 26, list_nameworld)
                worksheet.write(row, 27, snd_nameworld)
                worksheet.write(row, 28, bagman_nameworld_tony)
                row += 1
            else:
                for i, ret in enumerate(retainers):
                    ret_name = ret.get("Name", "Unknown")
                    ret_gil = ret.get("Gil", 0)
                    mb_items = ret.get("MBItems", 0)
                    has_venture = ret.get("HasVenture", 0)
                    ret_level = ret.get("Level", 0)

                    if i == 0:
                        worksheet.write_string(row, 0, str(cid))
                        worksheet.write(row, 1, nickname)
                        worksheet.write(row, 2, char_name, char_format)
                        worksheet.write(row, 3, world)
                        worksheet.write(row, 4, region)
                        worksheet.write_number(row, 5, char_gil, money_format)
                    else:
                        worksheet.write(row, 0, "")
                        worksheet.write(row, 1, "")
                        worksheet.write(row, 2, "")
                        worksheet.write(row, 3, "")
                        worksheet.write(row, 4, "")
                        worksheet.write(row, 5, "")

                    worksheet.write(row, 6, ret_name)
                    worksheet.write_number(row, 7, mb_items, money_format)
                    worksheet.write_number(row, 8, has_venture, money_format)
                    worksheet.write_number(row, 9, ret_level, money_format)
                    worksheet.write_number(row, 10, ret_gil, money_format)

                    if i == 0:
                        worksheet.write_number(row, 11, total_gil, total_format)
                        worksheet.write(row, 12, fc_name)
                        worksheet.write_number(row, 13, fc_points, money_format)
                        worksheet.write_number(row, 14, sub1lvl)
                        worksheet.write(row, 15, sub1parts)
                        worksheet.write_number(row, 16, sub2lvl)
                        worksheet.write(row, 17, sub2parts)
                        worksheet.write_number(row, 18, sub3lvl)
                        worksheet.write(row, 19, sub3parts)
                        worksheet.write_number(row, 20, sub4lvl)
                        worksheet.write(row, 21, sub4parts)
                        worksheet.write_number(row, TANK_COL, tank, money_format)
                        worksheet.write_number(row, KITS_COL, kits, money_format)
                        worksheet.write_number(row, TREAS_COL, treasure_value, total_format if treasure_value else money_format)
                        worksheet.write(row, 25, plain_nameworld)
                        worksheet.write(row, 26, list_nameworld)
                        worksheet.write(row, 27, snd_nameworld)
                        worksheet.write(row, 28, bagman_nameworld_tony)
                    else:
                        for c in (11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, TANK_COL, KITS_COL, TREAS_COL, 25, 26, 27, 28):
                            worksheet.write(row, c, "")

                    row += 1

        worksheet.set_column("A:A", 22)  # CID
        worksheet.set_column("B:B", 20)  # Account Nickname
        worksheet.set_column("C:C", 25)  # Character Name
        worksheet.set_column("D:D", 15)  # World
        worksheet.set_column("E:E", 8)   # Region
        worksheet.set_column("F:F", 15)  # Character Gil
        worksheet.set_column("G:G", 25)  # Retainer Name
        worksheet.set_column("H:H", 10)  # MBItems
        worksheet.set_column("I:I", 10)  # HasVenture
        worksheet.set_column("J:J", 10)  # Retainer Level
        worksheet.set_column("K:K", 15)  # Retainer Gil
        worksheet.set_column("L:L", 15)  # Total Gil
        worksheet.set_column("M:M", 25)  # FC Name
        worksheet.set_column("N:N", 15)  # FC Points
        worksheet.set_column("O:O", 8)   # Lvl #1
        worksheet.set_column("P:P", 6)   # #1
        worksheet.set_column("Q:Q", 8)   # Lvl #2
        worksheet.set_column("R:R", 6)   # #2
        worksheet.set_column("S:S", 8)   # Lvl #3
        worksheet.set_column("T:T", 6)   # #3
        worksheet.set_column("U:U", 8)   # Lvl #4
        worksheet.set_column("V:V", 6)   # #4
        worksheet.set_column(TANK_COL, TANK_COL, 10)   # Tanks
        worksheet.set_column(KITS_COL, KITS_COL, 9)   # Kits
        worksheet.set_column(TREAS_COL, TREAS_COL, 18) # Treasure Value
        worksheet.set_column(25, 25, 30)  # Plain Name
        worksheet.set_column(26, 26, 38)  # List Formatting
        worksheet.set_column(27, 27, 40)  # SND Formatting
        worksheet.set_column(28, 28, 55)  # Bagman Formatting

        worksheet.autofilter(0, 0, 0, len(headers) - 1)
        worksheet.freeze_panes(1, 0)

        summary_headers = ["Metric", "Value"]
        for col_idx, head in enumerate(summary_headers):
            summary_sheet.write(0, col_idx, head, header_format)
        summary_sheet.set_column("A:A", 30)
        summary_sheet.set_column("B:B", 20)

        total_gil_all = sum(c["total_gil"] for c in char_summaries)
        total_chars = len(char_summaries)
        total_retainers = sum(c["retainer_count"] for c in char_summaries)

        sub_parts_count = {}
        for summary in char_summaries:
            for part_str in [summary["sub1parts"], summary["sub2parts"], summary["sub3parts"], summary["sub4parts"]]:
                if part_str:
                    sub_parts_count[part_str] = sub_parts_count.get(part_str, 0) + 1
        sorted_parts = sorted(sub_parts_count.items(), key=lambda x: x[1], reverse=True)

        total_fc_points = sum(c["fc_points"] for c in char_summaries)
        fc_names = set(c["fc_name"] for c in char_summaries if c["fc_name"])
        total_fc_count = len(fc_names)
        fc_farming_subs = set(
            c["fc_name"] for c in char_summaries
            if c["fc_name"] and (
                c["sub1parts"] or c["sub2parts"] or c["sub3parts"] or c["sub4parts"]
            )
        )
        total_fc_farming_subs = len(fc_farming_subs)

        sub_levels = []
        for c in char_summaries:
            for i in [1, 2, 3, 4]:
                lvl = c.get(f"sub{i}lvl", 0)
                if lvl > 0:
                    sub_levels.append(lvl)
        lowest_sub_lvl = min(sub_levels) if sub_levels else 0
        highest_sub_lvl = max(sub_levels) if sub_levels else 0

        total_tanks = sum(c.get("tank", 0) for c in char_summaries)
        total_kits = sum(c.get("kits", 0) for c in char_summaries)
        total_treasure_value = sum(c.get("treasure_value", 0) for c in char_summaries)

        total_gil_value = total_gil_all + total_treasure_value

        summary_rows = [
            ["Total Characters", total_chars],
            ["Total Retainers", total_retainers],
            ["Total Gil (All Characters)", total_gil_all],
            ["Average Gil per Character", (total_gil_all / total_chars) if total_chars else 0],
            ["Total Tanks", total_tanks],
            ["Total Kits", total_kits],
            ["Total Treasure Value", total_treasure_value],
            ["Total Gil Value", total_gil_value],
        ]

        if char_summaries:
            summary_rows.extend([
                ["Richest Character", char_summaries[0]["char_name"]],
                ["Richest Character Gil", char_summaries[0]["total_gil"]],
                ["Total FC's", total_fc_count],
                ["Total FC's Farming Subs", total_fc_farming_subs],
                ["Total FC Points", total_fc_points],
                ["Lowest Sub Level", lowest_sub_lvl],
                ["Highest Sub Level", highest_sub_lvl]
            ])

        summary_rows.extend([
            ["Unique Submersible Parts", len(sub_parts_count)],
            ["Report Generated", datetime.datetime.now()],
        ])

        if sorted_parts:
            summary_rows.insert(-1, ["Submarine Builds", ""])
            for i, (build, count) in enumerate(sorted_parts, 1):
                summary_rows.insert(-1, [f"Build #{i}", f"{build} ({count} uses)"])

        #
        # Calculate Gil Farmed from submarine builds
        #
        gil_farmed_daily = 0
        for build, usage_count in sorted_parts:
            # Known builds that produce gil daily
            if build in ("WSUC", "SSUC"):
                gil_farmed_daily += 118661 * usage_count

        if gil_farmed_daily > 0:
            summary_rows.insert(-1, ["Gil Farmed Annually", gil_farmed_daily * 365])
            summary_rows.insert(-1, ["Gil Farmed Every 30 Days", gil_farmed_daily * 30])
            summary_rows.insert(-1, ["Gil Farmed Each Day", gil_farmed_daily])

        r = 1
        for (label, value) in summary_rows:
            summary_sheet.write(r, 0, label)
            if isinstance(value, (int, float)):
                fmt = total_format if ("Gil" in label or "Points" in label or "Value" in label or "Tanks" in label or "Kits" in label) else None
                summary_sheet.write_number(r, 1, value, fmt)
            elif isinstance(value, datetime.datetime):
                summary_sheet.write_datetime(r, 1, value, date_format)
            else:
                summary_sheet.write(r, 1, value)
            r += 1

        workbook.close()
        print(f"[SUCCESS] Excel file created at: {os.path.abspath(excel_output_path)}")
        return excel_output_path

    except PermissionError:
        print(f"[ERROR] Permission denied writing '{excel_output_path}'. Is it open?")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to create Excel file: {e}")
        return None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description="Export FFXIV gil report with Regions by World and Altoholic inventory.")
    parser.add_argument("--no-altoholic", action="store_true", help="Disable Altoholic scanning for all accounts.")
    parser.add_argument("output", nargs="?", default="unused.xlsx", help="(Ignored) Legacy positional.")
    args = parser.parse_args()

    date_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    final_output_path = os.path.join(script_dir, f"{date_str} - ffxiv_gil_summary.xlsx")

    for entry in account_locations:
        nickname = entry["nickname"]
        auto_path = entry["auto_path"]
        if os.path.isfile(auto_path):
            print(f"[INFO] Found config for {nickname} at: {auto_path}")
            try:
                with open(auto_path, "r", encoding="utf-8-sig") as f:
                    data = json.load(f)
                fc_part = extract_fc_data(data)
                for holder, fc_info in fc_part.items():
                    all_fc_data[holder] = fc_info
                chars_part = collect_characters(data, account_nickname=nickname)
                all_characters.extend(chars_part)
            except Exception as e:
                print(f"[ERROR] Could not parse JSON from {auto_path}: {e}")
        else:
            print(f"[WARNING] No file found for {nickname} at {auto_path}. Skipping.")

    if not all_characters:
        print("[FAIL] No character data loaded from any path.]")
        sys.exit(1)

    alto_map_global = {}
    if not args.no_altoholic:
        for entry in account_locations:
            if not entry.get("include_altoholic", True):
                continue
            alto_path = entry.get("alto_path", "")
            if alto_path and os.path.isfile(alto_path):
                print(f"[INFO] Scanning Altoholic DB for {entry['nickname']}: {alto_path}")
                partial = scan_altoholic_db(alto_path)
                alto_map_global.update(partial)
            else:
                print(f"[INFO] Altoholic DB not found or disabled for {entry['nickname']}: {alto_path}")

    char_summaries = build_char_summaries(all_characters, all_fc_data, alto_map_global)
    result = write_excel(char_summaries, final_output_path)
    if result:
        print(f"[DONE] Wrote data to {result}")
        sys.exit(0)
    else:
        print("[FAIL] Could not process data.")
        sys.exit(1)

if __name__ == "__main__":
    main()
