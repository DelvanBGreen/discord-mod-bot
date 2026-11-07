import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# Configure the bot
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

# Start the bot
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing from .env")

client.run(TOKEN)