import discord
from discord import app_commands
from discord.ext import commands
from utils.permissions import is_moderator, is_admin

from main import GUILD_ID

GUILD = discord.Object(id=GUILD_ID)

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        #---------kick--------------------------------
        @app_commands.command(name="kick", description="Kick a member from the server")
        @app_commands.guilds(GUILD)
        async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
            if not is_moderator(interaction.user):
                await interaction.response.send_message("You dont have persmission to use this command", ephemeral=True)
                return
            await member.kick(reason=reason)
