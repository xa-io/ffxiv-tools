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

# Webhook info
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
MENTION_ROLE = os.getenv("MENTION_ROLE", "")

# Dalamud meta URL
URL = "https://kamori.goats.dev/Dalamud/Release/Meta"

# Local file to store last scan data
LAST_SCAN_FILE = "last_scan.json"

# Which top-level keys to watch for changes
WATCH_KEYS = ["api11", "api12", "net9", "stg"]  # Add or remove keys as needed


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


def build_changed_sections_message(changed_keys, current_data):
    """
    Given a list of changed keys and the current data,
    return a nicely formatted message showing each section’s relevant fields.
    """
    # If mention role is enabled and we have a role ID, mention it
    mention_text = f"<@&{MENTION_ROLE}> " if (ENABLE_MENTION_ROLE and MENTION_ROLE) else ""

    lines = [f"{mention_text}**Dalamud Update Detected**\n"]
    
    for k in changed_keys:
        section = current_data.get(k, {})
        # Potential fields to reference
        key_field = section.get("key", "N/A")
        track = section.get("track", "N/A")
        assembly_version = section.get("assemblyVersion", "N/A")
        supported_game_ver = section.get("supportedGameVer", "N/A")

        lines.append(f"**Section**: `{k}`")
        lines.append(f"- **Key**: {key_field}")
        lines.append(f"- **Track**: {track}")
        lines.append(f"- **AssemblyVersion**: {assembly_version}")
        lines.append(f"- **SupportedGameVer**: {supported_game_ver}")
        lines.append("")  # blank line for spacing

    return "\n".join(lines).strip()


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

                # If any sections changed, send a single combined message
                if changed_keys:
                    msg = build_changed_sections_message(changed_keys, current_data)
                    send_discord_notification(msg)
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Update(s) detected in {changed_keys}. Notification sent.")

                    # Update the local file
                    save_last_data(current_data)
                else:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] No changes made at this time.")

        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] Encountered an error: {e}")

        time.sleep(300)  # Wait 5min before next scan


if __name__ == "__main__":
    main()
