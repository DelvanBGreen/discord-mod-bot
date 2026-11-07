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
        if member == interaction.user:
            await interaction.response.send_message("You cant kick yourself", ephemeral=True)
            return
        await member.kick(reason=reason)
        
        try:
            await member.send(
                f'You have been warn in **{interaction.guild.name}**.\n'
                f'**Reason:** {reason}'
            )
            dm_sent = True
        except (discord.Forbidden, discord.HTTPException):
                dm_sent =False

        await interaction.response.send_message(
                f"{member.name} has been banned for {reason}.\n"
                f"DM sent: {'Yes' if dm_sent else 'No'}", ephemeral=True
        )


    #---------ban-----------------------------------
    @app_commands.command(name="ban", description="Ban a user from the server")
    @app_commands.guilds(GUILD)
    async def ban(self, interaction: discord.Interaction, user: discord.User, reason: str = "No reason provided"):
        if not is_admin(interaction.user):
            await interaction.response.send_message("You dont have permission to use this command", ephemeral=True)
            return
        if user == interaction.user:
                    await interaction.response.send_message("You cant ban yourself", ephemeral=True)
                    return
        await interaction.guild.ban(user, reason=reason)

        try:
            await user.send(
                f'You have been warn in **{interaction.guild.name}**.\n'
                f'**Reason:** {reason}'
            )
            dm_sent = True
        except (discord.Forbidden, discord.HTTPException):
                dm_sent =False

        await interaction.response.send_message(
                f"{user.name} has been banned for {reason}.\n"
                f"DM sent: {'Yes' if dm_sent else 'No'}", ephemeral=True
        )
    
        

    #unban
    @app_commands.command(name="unban", description="Unban a user from the server")
    @app_commands.guilds(GUILD)
    async def unban(self, interaction: discord.Interaction, user: discord.User):
        if not is_admin(interaction.user):
            await interaction.response.send_message("You dont have permission to use this command", ephemeral=True)
            return
        if user == interaction.user:
            await interaction.response.send_message("Youre not banned gng", ephemeral=True)
            return

        try:
             await interaction.guild.fetch_ban(user)

             await interaction.guild.unban(user)
             await interaction.response.send_message(f'{user} has been unbanned')

        except discord.NotFound:
             await interaction.response.send_message('user is not banned', ephemeral=True)
        


    #-------timeout--------------------------------------
    @app_commands.command(name="timeout", description="Kick a member from the server")
    @app_commands.guilds(GUILD)
    async def timout(self, interaction: discord.Interaction, member: discord.Member,minutes: int, reason: str = "No reason provided"):
        if not is_moderator(interaction.user):
            await interaction.response.send_message("You dont have persmission to use this command", ephemeral=True)
            return
        if interaction.user == member:
             await interaction.response.send_message('You cant time yourself out', ephemeral=True)

        if member.is_timed_out():
             await interaction.response.send_message(f'{member} is already timed out', ephemeral=True)

        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await interaction.response.send_message(f'{member} has been timed out for {minutes} minutes')


    #------purge------------------------------------------
    @app_commands.command(name="purge", description="Delete multiple messages")
    @app_commands.guilds(GUILD)
    async def purge(
        self,
        interaction: discord.Interaction,
        amount: int
    ):
        if not is_moderator(interaction.user):
            await interaction.response.send_message(
                "You don't have permission to use this command.",
                ephemeral=True
            )
            return

        if amount < 1 or amount > 100:
            await interaction.response.send_message(
                "You must specify between 1 and 100 messages.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        deleted = await interaction.channel.purge(limit=amount)

        await interaction.followup.send(
            f"Successfully deleted {len(deleted)} messages.",
            ephemeral=True
        )

    #-----warn---------------------------------
    @app_commands.command(name="warn", description="Warn a member")
    @app_commands.guilds(GUILD)
    async def warn(self, interaction:discord.Interaction, member:discord.Member, reason:str):
        if not is_moderator(interaction.user):
            await interaction.response.send_message("You dont have permission to use this command", ephemeral=True)
            return
        if member==interaction.user:
             await interaction.response.send_message("You cant warn yourself", ephemeral=True)
             return

        try:
             await member.send(
                  f'You have been warn in **{interaction.guild.name}**.\n'
                  f'**Reason:** {reason}'
             )
             dm_sent = True
        except (discord.Forbidden, discord.HTTPException):
             dm_sent =False

        await interaction.response.send_message(
             f"{member.name} has been warned for {reason}.\n"
             f"DM sent: {'Yes' if dm_sent else 'No'}", ephemeral=True
        )
              

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))