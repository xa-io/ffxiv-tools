import os
import asyncio
import time
import psutil
from playsound import playsound
from dotenv import load_dotenv
import logging

import discord

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('FFXIV_Monitor')

# Load environment variables from .env
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_USER_ID = os.getenv("DISCORD_USER_ID")  # string; we'll convert to int below

# Basic checks to avoid errors if env variables are missing
if not DISCORD_BOT_TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN not found in .env file.")
if not DISCORD_USER_ID:
    raise ValueError("DISCORD_USER_ID not found in .env file.")

# Convert user ID to int
try:
    DISCORD_USER_ID = int(DISCORD_USER_ID)
    logger.info(f"Using Discord User ID: {DISCORD_USER_ID}")
except ValueError:
    logger.error(f"Invalid Discord User ID: {DISCORD_USER_ID}")
    raise ValueError(f"Invalid Discord User ID: {DISCORD_USER_ID}")

# Name of the process to monitor.
PROCESS_NAME = "ffxiv_dx11.exe"

# Path to the audio file for the alert sound.
ALERT_AUDIO_PATH = r"E:\!gil\sparkle.wav"

# How often (in seconds) to check for the process count.
SCAN_INTERVAL = 15

# Create Discord client with appropriate intents (DMs require certain intents).
intents = discord.Intents.default()
client = discord.Client(intents=intents)

def get_process_count() -> int:
    """
    Returns how many processes named PROCESS_NAME are running.
    """
    count = 0
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == PROCESS_NAME:
            count += 1
    return count

async def send_private_message(user_id: int, content: str):
    """
    Sends a direct message to the Discord user with the given ID.
    Make sure the bot and user share a server, or the user has
    allowed DMs from server members.
    """
    try:
        user = await client.fetch_user(user_id)
        await user.send(content)
    except Exception as e:
        logger.error(f"[Discord] Failed to send DM to user {user_id}: {e}")
        print(f"[Discord] Failed to send DM to user {user_id}: {e}")

async def monitor_processes():
    """
    Main loop that monitors the game processes, plays a local alert sound,
    and sends a Discord DM when the count drops below the stable count.
    
    Includes:
    1) Multiple-check logic (require 2 consecutive scans at a higher count
       before raising stable_count).
    2) Reset stable_count once the process recovers from a crash to avoid
       perpetual mis-matches.
    """

    stable_count = 0
    consecutive_higher_count = 0  # how many consecutive scans we've seen a higher count

    logger.info(f"[Monitor] Monitoring process: {PROCESS_NAME}")
    print(f"[Monitor] Monitoring process: {PROCESS_NAME}")
    logger.info(f"[Monitor] Checking every {SCAN_INTERVAL} seconds.")
    print(f"[Monitor] Checking every {SCAN_INTERVAL} seconds.")

    while True:
        current_count = get_process_count()

        # -----------------------------
        # 1) Multi-check logic for raising stable_count
        # -----------------------------
        if current_count > stable_count:
            consecutive_higher_count += 1
            # Require 2 consecutive scans of "current_count > stable_count" before accepting
            if consecutive_higher_count >= 2:
                stable_count = current_count
                consecutive_higher_count = 0
                logger.info(f"Updated stable count to {stable_count} after consecutive checks.")
                print(f"Updated stable count to {stable_count} after consecutive checks.")
        else:
            # If we're not strictly bigger, reset the consecutive count
            consecutive_higher_count = 0

        # -----------------------------
        # 2) Crash detection
        # -----------------------------
        if 0 < stable_count > current_count:
            crashed_amount = stable_count - current_count
            logger.warning(
                f"*** {crashed_amount} game client(s) crashed or closed! ***\n"
                f"Current Count: {current_count}, Stable Count: {stable_count}"
            )
            print(
                f"*** {crashed_amount} game client(s) crashed or closed! ***\n"
                f"Current Count: {current_count}, Stable Count: {stable_count}"
            )

            # Send Discord DM
            dm_message = (
                f"**FFXIV Crash Detected**\n"
                f"- Stable was {stable_count}, now {current_count}.\n"
                f"- {crashed_amount} game client(s) appear to have crashed."
            )
            await send_private_message(DISCORD_USER_ID, dm_message)

            # Continuous alert loop until recovered:
            while True:
                new_count = get_process_count()

                # If recovered to at least the old stable_count, stop alerting
                if new_count >= stable_count:
                    logger.info(
                        f"[Monitor] Process count recovered to {new_count} (>= {stable_count}). "
                        "Stopping alert."
                    )
                    print(
                        f"[Monitor] Process count recovered to {new_count} (>= {stable_count}). "
                        "Stopping alert."
                    )
                    break

                # Otherwise, play alert sound (blocking) in a thread
                try:
                    await asyncio.to_thread(playsound, ALERT_AUDIO_PATH)
                except Exception as e:
                    logger.error(f"[Audio] Error playing sound: {e}")
                    print(f"[Audio] Error playing sound: {e}")

                await asyncio.sleep(SCAN_INTERVAL)

            # Once we've broken out of the alert loop (i.e., recovered or user closed the loop),
            # we reset the stable count to the new_count to avoid perpetual mismatch.
            stable_count = new_count
            logger.info(f"[Monitor] Reset stable_count to {stable_count} after crash event.")
            print(f"[Monitor] Reset stable_count to {stable_count} after crash event.")
        else:
            # (Optional) normal logging
            logger.info(f"Current count: {current_count}, Stable count: {stable_count}")
            print(f"Current count: {current_count}, Stable count: {stable_count}")

        await asyncio.sleep(SCAN_INTERVAL)  # Wait and repeat

@client.event
async def on_ready():
    """
    Discord callback when the bot logs in successfully.
    """
    logger.info(f"[Discord] Logged in as {client.user} (ID: {client.user.id})")
    print(f"[Discord] Logged in as {client.user} (ID: {client.user.id})")

    # Check if the alert sound file exists
    if not os.path.exists(ALERT_AUDIO_PATH):
        logger.warning(f"Alert sound file not found at: {ALERT_AUDIO_PATH}")
        print(f"WARNING: Alert sound file not found at: {ALERT_AUDIO_PATH}")

    # Once logged in, start our monitoring loop as a background task.
    logger.info("Starting monitoring task...")
    print("Starting monitoring task...")
    client.loop.create_task(monitor_processes())

def main():
    """
    Entry point: starts the Discord client (blocking call).
    """
    logger.info("[System] Starting Discord bot...")
    print("[System] Starting Discord bot...")

    # Initial count check (just for info)
    current_count = get_process_count()
    logger.info(f"Initial {PROCESS_NAME} count: {current_count}")
    print(f"Initial {PROCESS_NAME} count: {current_count}")

    # This will block until the bot closes
    client.run(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    main()
