# FFXIV Discord Monitor

A Python utility that monitors Final Fantasy XIV game processes and sends Discord notifications when a game client crashes or closes unexpectedly.

## Features

- Monitors the number of running FFXIV game client processes (`ffxiv_dx11.exe`)
- Plays an audio alert when a client crash is detected
- Sends Discord direct messages with crash information
- Intelligent process count tracking with multiple-check validation
- Automatic recovery detection

## Requirements

- Tested on Python 3.12.4
- Discord bot token with appropriate permissions
- Discord user ID to receive notifications
- The following Python packages:
  - discord.py
  - psutil
  - playsound
  - python-dotenv

## Setup

1. Install the required packages:
   ```
   pip install discord.py psutil playsound python-dotenv
   ```

2. Create a `.env` file in the same directory with the following variables:
   ```
   DISCORD_BOT_TOKEN=your_discord_bot_token
   DISCORD_USER_ID=your_discord_user_id
   ```

3. Configure the audio alert path in the script:
   ```python
   ALERT_AUDIO_PATH = r"path\to\your\alert\sound.wav"
   ```

4. Ensure your Discord bot:
   - Has the necessary intents enabled in the Discord Developer Portal
   - Shares a server with the user who will receive notifications
   - The user has allowed DMs from server members

## Usage

Run the script with Python:

```
python FFXIV_Discord_Monitor.py
```

The script will:
1. Connect to Discord using your bot token
2. Begin monitoring FFXIV processes
3. Establish a baseline count of running game clients
4. Send notifications and play alerts if the count decreases unexpectedly

## Configuration Options

You can modify these variables in the script to customize behavior:

- `PROCESS_NAME`: The executable name to monitor (default: `ffxiv_dx11.exe`)
- `SCAN_INTERVAL`: How often to check for process count changes in seconds (default: 15)
- `ALERT_AUDIO_PATH`: Path to the sound file that plays when a crash is detected

## How It Works

1. The script establishes a "stable count" of running FFXIV processes
2. It requires two consecutive higher counts before raising the stable count (to avoid false positives)
3. When the current count drops below the stable count, it:
   - Sends a Discord DM with crash details
   - Plays an audio alert until the process count recovers
   - Resets the stable count once recovery is detected

## Logging

The script logs all activities to both the console and a log file with timestamps, making it easy to track when crashes occurred.
