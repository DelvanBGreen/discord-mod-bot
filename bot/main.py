import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

class Client(commands.Bot):
    async def setup_hook(self):
        # Load all cogs
        
        # Sync slash commands to the guild
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        synced = await self.tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands to guild {GUILD_ID}")

    async def on_ready(self):
        print(f"Logged in as {self.user}!")

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if self.user in message.mentions:
            await message.channel.send(f'Hi there, {message.author.mention}. I am Greens\' Gambling Bot, a bot made by <@{746447461886853131}>')


        await self.process_commands(message)


        


intents = discord.Intents.default()
intents.message_content = True


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)



# Start the bot
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing from .env")

client.run(TOKEN)