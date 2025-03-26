# Dalamud Meta Watcher

This Python script periodically checks for changes in specified sections of the Dalamud meta JSON hosted at:  
[https://kamori.goats.dev/Dalamud/Release/Meta](https://kamori.goats.dev/Dalamud/Release/Meta)

This script is running 24/7 here: https://discord.gg/g2NmYxPQCa

It:

1. Keeps a local reference of the last fetched data in a file (`last_scan.json`).
2. Compares new data from the site to that file.
3. If **any** sections have changed, it sends a **single** Discord notification (if enabled).
4. Updates `last_scan.json` with the new data when changes are detected.
5. Logs each check to the console.

---

## How It Works

1. **Initial Run**  
   - If `last_scan.json` does **not** exist, the script fetches the site data and **creates** `last_scan.json`, but **does not** send a notification.  
   - Logs: `Initial data fetched. No notification sent.`  

2. **Subsequent Runs**  
   - The script **loads** `last_scan.json` (the old data), then fetches the latest JSON from the site.  
   - For each **key** in `WATCH_KEYS` (e.g. `api11`, `net9`, `stg`), it checks if the data changed from the old file.  
   - If **any** keys differ, it sends **one** Discord message listing **all** changed sections, then writes the updated data into `last_scan.json`.  
   - If **no** keys differ, it logs: `No changes made at this time.`  

3. **Discord Notifications**  
   - If a Discord webhook is **enabled** and **configured**, the script sends a message.  
   - If `ENABLE_MENTION_ROLE` is also **true**, it will mention the provided role ID in the Discord message (e.g. `<@&1234567890>`).  

4. **Configuration**  
   - All configuration is done via a local `.env` file. If you leave out certain variables, the script can still run (it will simply skip notifications or role mentions).

---

## Requirements

- Python 3.7+  
- `requests` library  
- `python-dotenv` library  

Install the required libraries if you haven’t already:

`pip install requests python-dotenv`

---

## Setup

1. **Clone or download** this repository (containing `key_watcher.py` and a sample `.env`).
2. In the **same directory** as `key_watcher.py`, create a `.env` file. You can start with something like this:

   `
   # Enable or disable Discord webhook usage
   `ENABLE_WEBHOOK=true`

   # Your Discord Webhook URL (from Server Settings -> Integrations -> Webhooks)
   `DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/1234/abcdef`

   # Enable or disable pinging a specific role
   `ENABLE_MENTION_ROLE=true`

   # The numeric role ID to mention
   `MENTION_ROLE=123456789012345678`

3. **Configure** the script:
   - **`WATCH_KEYS`** in `key_watcher.py` is a list of the top-level JSON keys you want to compare for changes. By default:
     `WATCH_KEYS = ["api11", "net9", "stg"]`
     Add or remove items from this list as desired (e.g. `["release", "api11", "net9", "stg"]`).

4. **Run the Script**:
   `python key_watcher.py`
   - It will print logs to the console as it checks every 10 seconds by default.  
   - If `last_scan.json` is missing, the script creates it and does **not** send any notification this first time.  
   - On subsequent checks, if changes are detected in any of the watched sections, it will send a single Discord notification (if `ENABLE_WEBHOOK=true` and `DISCORD_WEBHOOK_URL` is set).

---

## Environment Variables Reference

- **`ENABLE_WEBHOOK`** (default `true` if omitted)  
  - Set to `false` to **disable** all Discord notifications.  
- **`DISCORD_WEBHOOK_URL`** (no default)  
  - The actual URL for the Discord webhook. If left blank or missing, notifications are skipped.  
- **`ENABLE_MENTION_ROLE`** (default `true` if omitted)  
  - Set to `false` to **disable** mentioning any role in Discord messages.  
- **`MENTION_ROLE`** (no default)  
  - The numeric ID of the role you’d like to ping. This is only used if `ENABLE_MENTION_ROLE=true`.

---

## Customizing

1. **Check Interval**  
   - By default, the script checks every 10 seconds (`time.sleep(10)` in the `while True:` loop). Adjust this to any interval you prefer.

2. **Changelog Parsing**  
   - If you want to show detailed changelogs or other fields from each section, you can expand the message-building logic.

3. **Manual Editing of `last_scan.json`**  
   - Because the script loads the file **on each loop**, you can manually edit `last_scan.json` for debugging. If your edits differ from the current site data, a notification will be triggered on the next check.

---

## Troubleshooting

1. **No Notifications**  
   - Check that `ENABLE_WEBHOOK=true` and `DISCORD_WEBHOOK_URL` is set to a valid webhook URL.  
   - Confirm your role mention settings if you’re not seeing pings.  

2. **File Errors**  
   - If `last_scan.json` is corrupt or partially written, the script will treat it as missing and recreate it.  

3. **Timeouts / Errors**  
   - The script uses a `timeout=10` seconds for the `requests.get(...)` call. If you’re on a slow or unreliable connection, you can increase the timeout.  
   - Errors are printed to the console as `[ERROR] Encountered an error: ...`.

---

**Enjoy monitoring Dalamud meta changes and receiving Discord updates automatically!**
