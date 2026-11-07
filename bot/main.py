import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

class Client(commands.Bot):
    async def setup_hook(self):
        # Load all cogs
        await self.load_extension("cogs.moderation")
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
            await message.channel.send(f'Hi there, {message.author.mention}. I am Greens\' Moderation Bot, a bot made by <@{746447461886853131}>')


        await self.process_commands(message)


        


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = Client(command_prefix="!", intents=intents)

# Start the bot
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing from .env")

if __name__ == "__main__":
    client.run(TOKEN)