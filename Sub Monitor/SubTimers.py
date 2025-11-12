import json
import os
import datetime
import sys
import getpass
import time
from pathlib import Path

# ===============================================
# Account locations
# ===============================================
user = getpass.getuser()

def acc(nickname, pluginconfigs_path, include_submarines=True):
    auto_path = os.path.join(pluginconfigs_path, "AutoRetainer", "DefaultConfig.json")
    return {
        "nickname": nickname,
        "auto_path": auto_path,
        "include_submarines": bool(include_submarines),
    }

# Account configuration - matches AR Parser order
account_locations = [
    acc("Main",   f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs", include_submarines=False),
    acc("Acc1",   f"C:\\Users\\{user}\\AltData\\Acc1\\pluginConfigs", include_submarines=True),
    acc("Acc2",   f"C:\\Users\\{user}\\AltData\\Acc2\\pluginConfigs", include_submarines=True),
    acc("Acc3",   f"C:\\Users\\{user}\\AltData\\Acc3\\pluginConfigs", include_submarines=True)
]

def collect_characters(full_data, account_nickname):
    """Extract characters from AutoRetainer JSON data"""
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

def get_submarine_timers_for_account(account_entry):
    """
    Get all submarine timers for a single account.
    Returns dict with account info and submarine data.
    """
    nickname = account_entry["nickname"]
    auto_path = account_entry["auto_path"]
    include_subs = account_entry.get("include_submarines", True)
    
    result = {
        "nickname": nickname,
        "include_submarines": include_subs,
        "total_subs": 0,
        "soonest_hours": None,
        "characters": []
    }
    
    if not include_subs:
        return result
    
    if not os.path.isfile(auto_path):
        return result
    
    try:
        with open(auto_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        
        chars = collect_characters(data, account_nickname=nickname)
        current_time = datetime.datetime.now().timestamp()
        
        all_return_times = []
        
        for char in chars:
            # Get submarine data from OfflineSubmarineData
            offline_sub_data = char.get("OfflineSubmarineData", [])
            
            for sub_dict in offline_sub_data:
                sub_name = sub_dict.get("Name", "")
                return_timestamp = sub_dict.get("ReturnTime", 0)
                
                if return_timestamp > 0:
                    # Convert to hours remaining (can be negative if already returned)
                    hours_remaining = (return_timestamp - current_time) / 3600
                    all_return_times.append(hours_remaining)
                    result["total_subs"] += 1
        
        # Find the soonest submarine (minimum time)
        if all_return_times:
            result["soonest_hours"] = min(all_return_times)
    
    except Exception as e:
        print(f"[ERROR] Failed to process {nickname}: {e}")
    
    return result

def format_hours(hours):
    """Format hours with + prefix for positive values"""
    if hours is None:
        return "N/A"
    if hours >= 0:
        return f"+{hours:.1f} hours"
    else:
        # Negative means already returned
        return f"{hours:.1f} hours (READY)"

def display_submarine_timers():
    """Display submarine timers for all accounts"""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=" * 60)
    print("FFXIV Submarine Timer Monitor")
    print("=" * 60)
    print(f"Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    account_data = []
    
    for account_entry in account_locations:
        timer_data = get_submarine_timers_for_account(account_entry)
        account_data.append(timer_data)
    
    # Display results
    for data in account_data:
        nickname = data["nickname"]
        total_subs = data["total_subs"]
        soonest_hours = data["soonest_hours"]
        
        if not data["include_submarines"]:
            print(f"{nickname:15s}: Submarines disabled")
        elif total_subs == 0:
            print(f"{nickname:15s}: No submarines found")
        else:
            hours_str = format_hours(soonest_hours)
            print(f"{nickname:15s}: {hours_str:20s} ({total_subs} subs)")
    
    print()
    print("=" * 60)
    print("Press Ctrl+C to exit")
    print("=" * 60)

def main():
    """Main loop - continuously update display"""
    try:
        while True:
            display_submarine_timers()
            # Update every 30 seconds
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n\nExiting submarine timer monitor...")
        sys.exit(0)

if __name__ == "__main__":
    main()
