import discord
from discord.ext import commands

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = "YOUR_BOT_TOKEN"

# Replace this with the channel ID of your announcements (news) channel
ANNOUNCEMENT_CHANNEL_ID = 1354574259468501246

# The role ID and name (for reference)
MENTION_ROLE_ID = 1354574931064787114
MENTION_ROLE_NAME = "kamori"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}.")

@bot.event
async def on_message(message):
    # Avoid the bot reacting to its own messages
    if message.author.id == bot.user.id:
        return

    lines = message.content.splitlines()
    should_publish = False
    should_not_publish = False

    for line in lines:
        line_lower = line.lower()

        # Condition 1: Publish if the line contains 'DalamudBetaKey' OR 'DalamudBetaKind' OR 'SupportedGameVer'
        # AND the word 'old'
        if (
            ("dalamudbetakey" in line_lower or
             "dalamudbetakind" in line_lower or
             "supportedgamever" in line_lower)
            and ("old" in line_lower)
        ):
            should_publish = True

        # Condition 2: Do NOT publish if the line contains 'AssemblyVersion' AND 'old'
        if ("assemblyversion" in line_lower) and ("old" in line_lower):
            should_not_publish = True
            break

    # Condition 3: Check if the specific role was mentioned
    # (instead of requiring the literal text "MENTION_ROLE=<ID>")
    was_role_mentioned = any(role.id == MENTION_ROLE_ID for role in message.role_mentions)

    # Only attempt to publish if all conditions are met
    if should_publish and not should_not_publish and was_role_mentioned:
        # Check if the message is in the announcements channel
        if message.channel.id == ANNOUNCEMENT_CHANNEL_ID:
            try:
                await message.publish()
                print(f"Message '{message.id}' was published successfully.")
            except discord.Forbidden:
                print("Bot does not have permission to publish in this channel.")
            except discord.HTTPException as e:
                print(f"Publishing failed: {e}")

    # Since we're overriding on_message, manually process commands
    await bot.process_commands(message)

bot.run(TOKEN)
