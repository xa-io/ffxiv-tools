import json
import xlsxwriter
import argparse
import os
import datetime
import sys
import getpass

# -----------------------------------------------
# pip install xlsxwriter
# -----------------------------------------------

# -----------------------------------------------
# Account locations + global data
# -----------------------------------------------
user = getpass.getuser()
account_locations = [
    ("Main", f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs\\AutoRetainer\\DefaultConfig.json"),
   # ("Alt1", f"C:\\Users\\{user}\\AltData\\alt1\\pluginConfigs\\AutoRetainer\\DefaultConfig.json"),
   # ("Alt2", f"C:\\Users\\{user}\\AltData\\alt2\\pluginConfigs\\AutoRetainer\\DefaultConfig.json"),
   # ("Alt3", f"C:\\Users\\{user}\\AltData\\alt3\\pluginConfigs\\AutoRetainer\\DefaultConfig.json"),
]
all_fc_data = {}
all_characters = []

# -----------------------------------------------
# Submarine Part Constants
# -----------------------------------------------
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

def extract_fc_data(full_data):
    """
    Recursively search the JSON for any dictionary containing "HolderChara".
    Store the info in fc_data, keyed by that HolderChara value.
    """
    fc_data = {}

    def recursive_search(obj):
        if isinstance(obj, dict):
            # If we see a HolderChara here, capture it
            if "HolderChara" in obj:
                holder_id = obj["HolderChara"]
                fc_data[holder_id] = {
                    "Name": obj.get("Name", "Unknown FC"),
                    "FCPoints": obj.get("FCPoints", 0)
                }
            # Continue searching deeper
            for v in obj.values():
                recursive_search(v)
        elif isinstance(obj, list):
            for item in obj:
                recursive_search(item)

    # Kick off the search
    recursive_search(full_data)
    return fc_data

def collect_characters(full_data, account_nickname):
    """
    Gather all character objects and assign an 'AccountNickname' for clarity.
    """
    all_characters = []

    def assign_nickname(chara):
        chara["AccountNickname"] = account_nickname
        return chara

    if isinstance(full_data, dict):
        if "OfflineData" in full_data and isinstance(full_data["OfflineData"], list):
            for c in full_data["OfflineData"]:
                if isinstance(c, dict) and "CID" in c:
                    all_characters.append(assign_nickname(c))
        else:
            for _, value in full_data.items():
                if isinstance(value, dict) and "CID" in value:
                    all_characters.append(assign_nickname(value))

    elif isinstance(full_data, list):
        for item in full_data:
            if isinstance(item, dict) and "CID" in item:
                all_characters.append(assign_nickname(item))

    return all_characters

def shorten_part_name(full_name: str) -> str:
    for prefix, code in CLASS_SHORTCUTS.items():
        if full_name.startswith(prefix):
            return code
    return "?"

def get_sub_parts_string(sub_data: dict) -> str:
    """
    Return a concatenated short code of submarine parts (e.g. "WSUC").
    """
    parts = []
    for key in ["Part1", "Part2", "Part3", "Part4"]:
        part_id = sub_data.get(key, 0)
        if part_id != 0:
            full_part_name = SUB_PARTS_LOOKUP.get(part_id, f"Unknown({part_id})")
            short_code = shorten_part_name(full_part_name)
            parts.append(short_code)
    return "".join(parts)

def build_char_summaries(all_characters, fc_data):
    """
    For each character, compute total gil and gather submarine parts + levels.
    Then cross-reference fc_data for FC name/points if CID matches a HolderChara.
    Also fill out retainer data, but preserve MBItems if it is already in the JSON.
    """
    char_summaries = []
    for char in all_characters:
        cid = char.get("CID", 0)
        char_name = char.get("Name", "Unknown")
        world = char.get("World", "Unknown")
        char_gil = char.get("Gil", 0)
        nickname = char.get("AccountNickname", "UnknownAcct")

        # Sum retainer gil and augment retainer info
        retainer_data = char.get("RetainerData", [])
        total_ret_gil = 0
        for ret in retainer_data:
            gil = ret.get("Gil", 0)
            total_ret_gil += gil

            # --- MBItems logic
            if "MBItems" not in ret:
                ret["MBItems"] = len(ret.get("MarketBoardItems", []))
            if isinstance(ret["MBItems"], bool):
                ret["MBItems"] = 1 if ret["MBItems"] else 0

            # --- HasVenture
            if "HasVenture" in ret:
                if isinstance(ret["HasVenture"], bool):
                    ret["HasVenture"] = 1 if ret["HasVenture"] else 0
            else:
                ret["HasVenture"] = 1 if ret.get("VentureID", 0) > 0 else 0

            # --- Level
            ret["Level"] = ret.get("Level", 0)

        # Submersible parts & levels
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

        # FC cross-reference
        fc_name = ""
        fc_points = 0
        if cid in fc_data:
            fc_name = fc_data[cid].get("Name", "")
            fc_points = fc_data[cid].get("FCPoints", 0)

        # Build the final dictionary for each character
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
            # Sub #1
            "sub1lvl": sub_data_map["Submersible-1"]["level"],
            "sub1parts": sub_data_map["Submersible-1"]["parts"],
            # Sub #2
            "sub2lvl": sub_data_map["Submersible-2"]["level"],
            "sub2parts": sub_data_map["Submersible-2"]["parts"],
            # Sub #3
            "sub3lvl": sub_data_map["Submersible-3"]["level"],
            "sub3parts": sub_data_map["Submersible-3"]["parts"],
            # Sub #4
            "sub4lvl": sub_data_map["Submersible-4"]["level"],
            "sub4parts": sub_data_map["Submersible-4"]["parts"],
        })
    return char_summaries

def write_excel(char_summaries, excel_output_path):
    """
    Takes the final list of character summaries and writes them to Excel.
    The output file name is always prepended with "yyyy-mm-dd-hh-mm - ".
    """
    # Sort by descending total gil
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

        # Headers for the Gil Summary sheet
        headers = [
            "CID",
            "Account Nickname",
            "Character Name",
            "World",
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
            "Overseer Name Formatting",
            "SND Name Formatting"
        ]
        for col_idx, head in enumerate(headers):
            worksheet.write(0, col_idx, head, header_format)

        row = 1
        for summary in char_summaries:
            cid = summary["cid"]
            nickname = summary["account_nickname"]
            char_name = summary["char_name"]
            world = summary["world"]
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

            # Overseer Name Formatting => "Character@World ",
            overseer_value = f"\"{char_name}@{world}\","  
            # SND Name Formatting => {"Character@World"},
            snd_value = f"{{\"{char_name}@{world}\"}},"  

            retainers = summary["retainers"]

            if not retainers:
                # Single line for a char with no retainers
                worksheet.write_string(row, 0, str(cid))                  # A
                worksheet.write(row, 1, nickname)                         # B
                worksheet.write(row, 2, char_name)                        # C
                worksheet.write(row, 3, world)                            # D
                worksheet.write_number(row, 4, char_gil, money_format)    # E
                worksheet.write(row, 5, "")                               # F (Retainer Name)
                worksheet.write_number(row, 6, 0, money_format)           # G (MBItems)
                worksheet.write_number(row, 7, 0, money_format)           # H (HasVenture)
                worksheet.write_number(row, 8, 0, money_format)           # I (Level)
                worksheet.write_number(row, 9, 0, money_format)           # J (Retainer Gil)
                worksheet.write_number(row, 10, total_gil, total_format)  # K (Total Gil)
                worksheet.write(row, 11, fc_name)                         # L (FC Name)
                worksheet.write_number(row, 12, fc_points, money_format)  # M (FC Points)
                worksheet.write_number(row, 13, sub1lvl)                  # N (Lvl #1)
                worksheet.write(row, 14, sub1parts)                       # O (#1)
                worksheet.write_number(row, 15, sub2lvl)                  # P (Lvl #2)
                worksheet.write(row, 16, sub2parts)                       # Q (#2)
                worksheet.write_number(row, 17, sub3lvl)                  # R (Lvl #3)
                worksheet.write(row, 18, sub3parts)                       # S (#3)
                worksheet.write_number(row, 19, sub4lvl)                  # T (Lvl #4)
                worksheet.write(row, 20, sub4parts)                       # U (#4)
                worksheet.write(row, 21, overseer_value)                  # V (Overseer)
                worksheet.write(row, 22, snd_value)                       # W (SND)
                row += 1
            else:
                # Multiple lines, one for each retainer
                for i, ret in enumerate(retainers):
                    ret_name = ret.get("Name", "Unknown")
                    ret_gil = ret.get("Gil", 0)
                    mb_items = ret.get("MBItems", 0)
                    has_venture = ret.get("HasVenture", 0)
                    ret_level = ret.get("Level", 0)

                    if i == 0:
                        # First line with character data
                        worksheet.write_string(row, 0, str(cid))               # A
                        worksheet.write(row, 1, nickname)                      # B
                        worksheet.write(row, 2, char_name, char_format)        # C
                        worksheet.write(row, 3, world)                         # D
                        worksheet.write_number(row, 4, char_gil, money_format) # E
                    else:
                        # Blank out these columns for subsequent retainers
                        worksheet.write(row, 0, "")
                        worksheet.write(row, 1, "")
                        worksheet.write(row, 2, "")
                        worksheet.write(row, 3, "")
                        worksheet.write(row, 4, "")

                    # Retainer-specific columns
                    worksheet.write(row, 5, ret_name)                         # F (Retainer Name)
                    worksheet.write_number(row, 6, mb_items, money_format)    # G (MBItems)
                    worksheet.write_number(row, 7, has_venture, money_format) # H (HasVenture)
                    worksheet.write_number(row, 8, ret_level, money_format)   # I (Level)
                    worksheet.write_number(row, 9, ret_gil, money_format)     # J (Retainer Gil)

                    if i == 0:
                        # Show totals on the first line
                        worksheet.write_number(row, 10, total_gil, total_format) # K (Total Gil)
                        worksheet.write(row, 11, fc_name)                        # L (FC Name)
                        worksheet.write_number(row, 12, fc_points, money_format) # M (FC Points)
                        worksheet.write_number(row, 13, sub1lvl)                  # N (Lvl #1)
                        worksheet.write(row, 14, sub1parts)                       # O (#1)
                        worksheet.write_number(row, 15, sub2lvl)                  # P (Lvl #2)
                        worksheet.write(row, 16, sub2parts)                       # Q (#2)
                        worksheet.write_number(row, 17, sub3lvl)                  # R (Lvl #3)
                        worksheet.write(row, 18, sub3parts)                       # S (#3)
                        worksheet.write_number(row, 19, sub4lvl)                  # T (Lvl #4)
                        worksheet.write(row, 20, sub4parts)                       # U (#4)
                        worksheet.write(row, 21, overseer_value)                  # V (Overseer)
                        worksheet.write(row, 22, snd_value)                       # W (SND)
                    else:
                        # Leave these columns blank on subsequent retainer rows
                        worksheet.write(row, 10, "")
                        worksheet.write(row, 11, "")
                        worksheet.write(row, 12, "")
                        worksheet.write(row, 13, "")
                        worksheet.write(row, 14, "")
                        worksheet.write(row, 15, "")
                        worksheet.write(row, 16, "")
                        worksheet.write(row, 17, "")
                        worksheet.write(row, 18, "")
                        worksheet.write(row, 19, "")
                        worksheet.write(row, 20, "")
                        worksheet.write(row, 21, "")
                        worksheet.write(row, 22, "")

                    row += 1

        #
        # Adjust column widths
        #
        worksheet.set_column("A:A", 22)  # CID
        worksheet.set_column("B:B", 20)  # Account Nickname
        worksheet.set_column("C:C", 25)  # Character Name
        worksheet.set_column("D:D", 15)  # World
        worksheet.set_column("E:E", 15)  # Character Gil
        worksheet.set_column("F:F", 25)  # Retainer Name
        worksheet.set_column("G:G", 10)  # MBItems
        worksheet.set_column("H:H", 10)  # HasVenture
        worksheet.set_column("I:I", 10)  # Retainer Level
        worksheet.set_column("J:J", 15)  # Retainer Gil
        worksheet.set_column("K:K", 15)  # Total Gil
        worksheet.set_column("L:L", 25)  # FC Name
        worksheet.set_column("M:M", 15)  # FC Points
        worksheet.set_column("N:N", 8)   # Lvl #1
        worksheet.set_column("O:O", 6)   # #1
        worksheet.set_column("P:P", 8)   # Lvl #2
        worksheet.set_column("Q:Q", 6)   # #2
        worksheet.set_column("R:R", 8)   # Lvl #3
        worksheet.set_column("S:S", 6)   # #3
        worksheet.set_column("T:T", 8)   # Lvl #4
        worksheet.set_column("U:U", 6)   # #4
        worksheet.set_column("V:V", 30)  # Overseer Name Formatting
        worksheet.set_column("W:W", 30)  # SND Name Formatting

        # Add autofilter and freeze the top row
        worksheet.autofilter(0, 0, 0, len(headers) - 1)
        worksheet.freeze_panes(1, 0)

        #
        # ================= Build Summary sheet =================
        #
        summary_headers = ["Metric", "Value"]
        for col_idx, head in enumerate(summary_headers):
            summary_sheet.write(0, col_idx, head, header_format)
        summary_sheet.set_column("A:A", 30)
        summary_sheet.set_column("B:B", 20)

        total_gil_all = sum(c["total_gil"] for c in char_summaries)
        total_chars = len(char_summaries)
        total_retainers = sum(c["retainer_count"] for c in char_summaries)

        # Count submersible builds
        sub_parts_count = {}
        for summary in char_summaries:
            for part_str in [
                summary["sub1parts"],
                summary["sub2parts"],
                summary["sub3parts"],
                summary["sub4parts"]
            ]:
                if part_str:
                    sub_parts_count[part_str] = sub_parts_count.get(part_str, 0) + 1

        sorted_parts = sorted(sub_parts_count.items(), key=lambda x: x[1], reverse=True)

        # Sum all FC points (for all characters)
        total_fc_points = sum(c["fc_points"] for c in char_summaries)

        # Count distinct FC names
        fc_names = set(c["fc_name"] for c in char_summaries if c["fc_name"])
        total_fc_count = len(fc_names)

        # Count how many FCs are actively "farming subs"
        fc_farming_subs = set(
            c["fc_name"] for c in char_summaries
            if c["fc_name"] and (
                c["sub1parts"] or c["sub2parts"] or c["sub3parts"] or c["sub4parts"]
            )
        )
        total_fc_farming_subs = len(fc_farming_subs)

        # Compute overall lowest/highest sub levels (ignoring zero-level subs)
        sub_levels = []
        for c in char_summaries:
            for i in [1, 2, 3, 4]:
                lvl = c.get(f"sub{i}lvl", 0)
                if lvl > 0:
                    sub_levels.append(lvl)
        lowest_sub_lvl = min(sub_levels) if sub_levels else 0
        highest_sub_lvl = max(sub_levels) if sub_levels else 0

        # Base summary rows
        summary_rows = [
            ["Total Characters", total_chars],
            ["Total Retainers", total_retainers],
            ["Total Gil (All Characters)", total_gil_all],
            [
                "Average Gil per Character",
                (total_gil_all / total_chars) if total_chars else 0
            ],
        ]

        if char_summaries:
            summary_rows.extend([
                ["Richest Character", char_summaries[0]["char_name"]],
                ["Richest Character Gil", char_summaries[0]["total_gil"]],
                ["Total FC's", total_fc_count],
                ["Total FC's Farming Subs", total_fc_farming_subs],
                ["Total FC Points", total_fc_points],
                # Insert the new rows here:
                ["Lowest Sub Level", lowest_sub_lvl],
                ["Highest Sub Level", highest_sub_lvl]
            ])

        # We continue building the summary after we've appended lowest/highest sub levels
        summary_rows.extend([
            ["Unique Submersible Parts", len(sub_parts_count)],
            ["Report Generated", datetime.datetime.now()],
        ])

        # Optionally insert submarine build usage details
        if sorted_parts:
            # Insert a label row to identify Submarine Builds
            summary_rows.insert(-1, ["Submarine Builds", ""])
            for i, (build, count) in enumerate(sorted_parts, 1):
                summary_rows.insert(-1, [f"Build #{i}", f"{build} ({count} uses)"])

        #
        # Example logic for "Gil Farmed Each Day" (optional usage)
        #
        gil_farmed_daily = 0
        for build, usage_count in sorted_parts:
            # Example: if certain builds are known to produce X gil daily, factor it here
            if build in ("WSUC", "SSUC"):
                gil_farmed_daily += 114454 * usage_count

        if gil_farmed_daily > 0:
            summary_rows.insert(-1, ["Gil Farmed Annually", gil_farmed_daily * 365])
            summary_rows.insert(-1, ["Gil Farmed Every 30 Days", gil_farmed_daily * 30])
            summary_rows.insert(-1, ["Gil Farmed Each Day", gil_farmed_daily])

        # Write all the summary rows
        r = 1
        for (label, value) in summary_rows:
            summary_sheet.write(r, 0, label)
            if isinstance(value, (int, float)):
                summary_sheet.write_number(
                    r, 1, value,
                    total_format if ("Gil" in label or "Points" in label) else None
                )
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

    parser = argparse.ArgumentParser(
        description='Load multiple accounts’ DefaultConfig.json, add account nicknames, and export to Excel.'
    )
    # We will ignore output file argument for a stable naming scheme:
    # "yyyy-mm-dd-hh-mm - ffxiv_gil_summary.xlsx"
    parser.add_argument(
        'output',
        nargs='?',
        default="unused_output_arg.xlsx",
        help='(Ignored) Name for the Excel output file.'
    )
    args = parser.parse_args()

    # Build the final file path with date-time prefix
    date_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    base_name = "ffxiv_gil_summary.xlsx"
    final_output_name = f"{date_str} - {base_name}"
    final_output_path = os.path.join(script_dir, final_output_name)

    # 1) Check each path, load data if found
    for (nickname, path) in account_locations:
        if os.path.isfile(path):
            print(f"[INFO] Found config for {nickname} at: {path}")
            try:
                with open(path, "r", encoding="utf-8-sig") as f:
                    data = json.load(f)
                # Extract FC data
                fc_part = extract_fc_data(data)
                for holder, fc_info in fc_part.items():
                    all_fc_data[holder] = fc_info
                # Extract characters (with nickname)
                chars_part = collect_characters(data, account_nickname=nickname)
                all_characters.extend(chars_part)
            except Exception as e:
                print(f"[ERROR] Could not parse JSON from {path}: {e}")
        else:
            print(f"[WARNING] No file found for {nickname} at {path}. Skipping.")

    if not all_characters:
        print("[FAIL] No character data loaded from any path.")
        sys.exit(1)

    # 2) Build summaries
    char_summaries = build_char_summaries(all_characters, all_fc_data)

    # 3) Write final Excel (with date in filename)
    result = write_excel(char_summaries, final_output_path)
    if result:
        print(f"[DONE] Wrote data to {result}")
        sys.exit(0)
    else:
        print("[FAIL] Could not process data.")
        sys.exit(1)

if __name__ == "__main__":
    main()
