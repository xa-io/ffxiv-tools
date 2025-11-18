import os
import time
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configuration toggles
ENABLE_WEBHOOK = os.getenv("ENABLE_WEBHOOK", "true").lower() == "true"
ENABLE_MENTION_ROLE = os.getenv("ENABLE_MENTION_ROLE", "true").lower() == "true"
POST_ASSEMBLYVERSION = os.getenv("POST_ASSEMBLYVERSION", "false").lower() == "true"

# Webhook info
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
MENTION_ROLE = os.getenv("MENTION_ROLE", "")

# Dalamud meta URL
URL = "https://kamori.goats.dev/Dalamud/Release/Meta"

# Local file to store last scan data
LAST_SCAN_FILE = "last_scan.json"

# Which top-level keys to watch for changes
# Note: We are now adding "release" to the watcher list, but it has special handling.
WATCH_KEYS = ["api13", "api14", "api15", "net9", "stg", "imgui-bindings", "release"]

def get_current_release_data():
    """
    Fetch the JSON from the Dalamud meta endpoint and return it.
    """
    response = requests.get(URL, timeout=10)
    response.raise_for_status()  # Raise an exception for non-200 statuses
    return response.json()


def load_last_data(file_path=LAST_SCAN_FILE):
    """
    Load the last scan data from a local JSON file.
    Returns None if the file doesn't exist or is invalid.
    """
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None  # In case file is corrupt or unreadable


def save_last_data(data, file_path=LAST_SCAN_FILE):
    """
    Save the latest data to a local JSON file for future reference.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def send_discord_notification(message: str):
    """
    Sends a message to a Discord channel using a webhook, if enabled and configured.
    """
    # If webhook usage is disabled or no webhook URL is set, skip sending
    if not ENABLE_WEBHOOK or not DISCORD_WEBHOOK_URL:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Webhook disabled or not configured. Skipping notification.")
        return

    payload = {"content": message}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] Failed to send Discord notification: {e}")


def build_changed_sections_message(changed_keys, current_data, old_data):
    """
    Build a Discord message describing changes for the normal watchers (excluding special release handling).
    
    We'll only build messages for keys that are not 'release' or for 'release' if you
    want to handle it in the same style. However, since 'release' is special, we'll
    skip it in this function and handle it separately in the main loop.
    """
    # We'll rename 'beta_change_detected' to something more general:
    mention_triggered = False

    # Filter out 'release' since it's handled separately
    filtered_changed_keys = [k for k in changed_keys if k != 'release']

    # Filter out sections where only AssemblyVersion changed if POST_ASSEMBLYVERSION is False
    sections_to_post = []
    for k in filtered_changed_keys:
        new_section = current_data.get(k, {})
        old_section = old_data.get(k, {})

        new_key = new_section.get('key', 'N/A')
        old_key = old_section.get('key', 'N/A')
        new_kind = new_section.get('track', 'N/A')
        old_kind = old_section.get('track', 'N/A')
        new_gamever = new_section.get('supportedGameVer', 'N/A')
        old_gamever = old_section.get('supportedGameVer', 'N/A')
        new_assembly = new_section.get('assemblyVersion', 'N/A')
        old_assembly = old_section.get('assemblyVersion', 'N/A')

        # Check if only AssemblyVersion changed
        key_changed = new_key != old_key
        kind_changed = new_kind != old_kind
        gamever_changed = new_gamever != old_gamever
        assembly_changed = new_assembly != old_assembly

        # If POST_ASSEMBLYVERSION is False and only AssemblyVersion changed, skip this section
        if not POST_ASSEMBLYVERSION and assembly_changed and not (key_changed or kind_changed or gamever_changed):
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Skipping {k} - only AssemblyVersion changed (POST_ASSEMBLYVERSION=False)")
            continue

        sections_to_post.append(k)

        # Trigger a mention if any mention-worthy fields changed
        if key_changed or kind_changed or gamever_changed:
            mention_triggered = True

    # If no sections to post, return empty string
    if not sections_to_post:
        return ""

    # If mention is triggered AND mention role is enabled, prepend the mention
    if mention_triggered and ENABLE_MENTION_ROLE and MENTION_ROLE:
        mention_text = f"<@&{MENTION_ROLE}> "
    else:
        mention_text = ""

    lines = [f"{mention_text}**Dalamud Update Detected**\n"]

    # Now build the message of changed fields for the sections we're posting
    for k in sections_to_post:
        new_section = current_data.get(k, {})
        old_section = old_data.get(k, {})

        if k == 'stg':
            section_title = f"**Section**: `stg` (Beta)"
        elif k == 'imgui-bindings':
            section_title = "**Section**: `imgui-bindings` (Dev)"
        else:
            section_title = f"**Section**: `{k}`"
        lines.append(section_title)

        # DalamudBetaKey
        new_key = new_section.get('key', 'N/A')
        old_key = old_section.get('key', 'N/A')
        if new_key != old_key:
            lines.append(f"- **\"DalamudBetaKey\"**: \"{new_key}\" (old: \"{old_key}\"),")
        else:
            lines.append(f"- **\"DalamudBetaKey\"**: \"{new_key}\",")

        # DalamudBetaKind
        new_kind = new_section.get('track', 'N/A')
        old_kind = old_section.get('track', 'N/A')
        if new_kind != old_kind:
            lines.append(f"- **\"DalamudBetaKind\"**: \"{new_kind}\" (old: \"{old_kind}\"),")
        else:
            lines.append(f"- **\"DalamudBetaKind\"**: \"{new_kind}\",")

        # AssemblyVersion
        new_assembly = new_section.get('assemblyVersion', 'N/A')
        old_assembly = old_section.get('assemblyVersion', 'N/A')
        if new_assembly != old_assembly:
            lines.append(f"- **AssemblyVersion**: {new_assembly} (old: {old_assembly})")
        else:
            lines.append(f"- **AssemblyVersion**: {new_assembly}")

        # SupportedGameVer
        new_gamever = new_section.get('supportedGameVer', 'N/A')
        old_gamever = old_section.get('supportedGameVer', 'N/A')
        if new_gamever != old_gamever:
            lines.append(f"- **SupportedGameVer**: {new_gamever} (old: {old_gamever})")
        else:
            lines.append(f"- **SupportedGameVer**: {new_gamever}")

        lines.append("")  # Blank line for spacing

    # If no normal watchers changed, return an empty string (so we can skip sending a normal watchers message)
    # We'll rely on the caller to decide how to handle that scenario.
    if not filtered_changed_keys:
        return ""

    return "\n".join(lines).strip()


def build_release_change_message(current_release):
    """
    Build the special message for `release` key changes when
    isApplicableForCurrentGameVer transitions from False -> True.
    """
    # Insert mention if configured
    if ENABLE_MENTION_ROLE and MENTION_ROLE:
        mention_text = f"<@&{MENTION_ROLE}> "
    else:
        mention_text = ""

    assembly_version = current_release.get('assemblyVersion', 'N/A')
    supported_game_ver = current_release.get('supportedGameVer', 'N/A')

    lines = [
        f"{mention_text}**Dalamud Update Detected**",
        "",
        "**Section**: `release` (Stable)",
        f"- **\"DalamudBetaKey\"**: null,",
        f"- **\"DalamudBetaKind\"**: null,",
        f"- **AssemblyVersion**: {assembly_version}",
        f"- **SupportedGameVer**: {supported_game_ver}"
    ]

    return "\n".join(lines)


def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Dalamud meta watcher...")

    while True:
        try:
            # Load the last data from file
            last_data = load_last_data(LAST_SCAN_FILE)

            # If the file doesn't exist or is invalid, create it
            if last_data is None:
                current_data = get_current_release_data()
                save_last_data(current_data)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Initial data fetched. No notification sent.")
            else:
                # File exists: compare
                current_data = get_current_release_data()

                changed_keys = []
                for key in WATCH_KEYS:
                    old_section = last_data.get(key)
                    new_section = current_data.get(key)
                    if old_section != new_section:
                        changed_keys.append(key)

                # If nothing changed, do nothing
                if not changed_keys:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] No changes made at this time.")
                else:
                    # Handle release's special logic if 'release' is in changed_keys
                    if 'release' in changed_keys:
                        old_release = last_data.get('release', {})
                        new_release = current_data.get('release', {})

                        old_applicable = old_release.get('isApplicableForCurrentGameVer', False)
                        new_applicable = new_release.get('isApplicableForCurrentGameVer', False)

                        # Check the condition: from false -> true
                        if not old_applicable and new_applicable:
                            # Send the special "release" message
                            special_msg = build_release_change_message(new_release)
                            send_discord_notification(special_msg)
                            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Release changed from not-applicable to applicable. Notification sent.")

                        # Remove 'release' from normal changed_keys so it won't appear in normal watchers message
                        changed_keys.remove('release')

                    # Now build normal watchers message (excluding release) if anything remains
                    if changed_keys:  # if there are still other watchers that changed
                        msg = build_changed_sections_message(changed_keys, current_data, last_data)
                        if msg:  # If there's a real message to send
                            send_discord_notification(msg)
                            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Update(s) detected in {changed_keys}. Notification sent.")

                    # Update the local file
                    save_last_data(current_data)

        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] Encountered an error: {e}")

        time.sleep(300)  # Check every 5 minutes


if __name__ == "__main__":
    main()
