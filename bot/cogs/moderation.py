import discord
from discord import app_commands
from discord.ext import commands
from utils.permissions import is_moderator, is_admin
from datetime import timedelta
from dotenv import load_dotenv
import os

from main import GUILD_ID

GUILD = int(os.getenv("GUILD_ID"))

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

    #---------ban-----------------------------------
    @app_commands.command(name="ban", description="Ban a user from the server")
    @app_commands.guilds(GUILD)
    async def ban(self, interaction: discord.Interaction, user: discord.User, reason: str = "No reason provided"):
        if not is_admin(interaction.user):
            await interaction.response.send_message("You dont have permission to use this command", ephemeral=True)
            return

        await interaction.guild.ban(user, reason=reason)

    #-------timeout--------------------------------------
    @app_commands.command(name="timeout", description="Kick a member from the server")
    @app_commands.guilds(GUILD)
    async def timout(self, interaction: discord.Interaction, member: discord.Member,minutes: int, reason: str = "No reason provided"):
        if not is_moderator(interaction.user):
            await interaction.response.send_message("You dont have persmission to use this command", ephemeral=True)
            return
        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await interaction.response.send_message(f'{member} has been timed out for {minutes} minutes')


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))