import discord
from discord.ext import commands
from discord import app_commands
from utils.permissions import *
from datetime import datetime, timedelta, timezone
from utils.word_filter import contains_blocked_word
from utils.spam_filter import SpamFilter
from database.logging_db import log_moderation
import re


def contains_link(text):
    pattern = r"(?:https?://|www\.)[^\s]+|\b[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+\b"
    return bool(re.search(pattern, text, re.IGNORECASE))


class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

        self.word_filter_enabled = True
        self.word_filter_resume_at = None

        self.link_filter_enabled = True
        self.link_filter_resume_at = None

        self.spam_filter_enabled = True

        self.spam_filter = SpamFilter()
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        self.message_deleted = False
        if message.author.bot or message.guild is None:
            return


        if self.spam_filter_enabled:
            spam_type = self.spam_filter.check_spam(
                message.guild.id,
                message.author.id,
                message.content
            )

            if spam_type:
                await message.delete()

                print(
                    f"Spam detected from {message.author}: {spam_type}"
                )

                return

        # Check if the word filter should resume
        if self.word_filter_resume_at is not None:
            if datetime.now(timezone.utc) >= self.word_filter_resume_at:
                self.word_filter_enabled = True
                self.word_filter_resume_at = None

        if self.link_filter_resume_at is not None:
            if datetime.now(timezone.utc) >= self.link_filter_resume_at:
                self.link_filter_enabled = True
                self.link_filter_resume_at = None


        # Check message for blocked words
        if ((contains_blocked_word(message.content) and self.word_filter_enabled)):

            try:
                # Delete the offending message
                await message.delete()
                self.message_deleted = True

                # Notify the user
                await message.channel.send(
                    f"{message.author.mention}, your message was removed "
                    "for containing prohibited language.",
                    delete_after=5
                )

            except discord.Forbidden:
                print("AutoMod: Missing permissions.")

            except discord.HTTPException as e:
                print(f"AutoMod error: {e}")

        #check message for links
        if (contains_link(message.content) and self.link_filter_enabled and self.message_deleted == False):
            try:
                await message.delete()

                await message.channel.send(
                    f"{message.author.mention}, your message was removed for containing a link",
                    delete_after=5)

            except discord.Forbidden:
                print("Automod: Missing permissions.")
            except discord.HTTPException as e:
                print(f"Automod error: {e}")
        self.message_deleted = False

    
    @app_commands.command(name='disable_word_filter', description='disable word filtering for a set time or until its enableed again')
    @app_commands.guild_only
    async def disable_word_filter(self, interaction: discord.Interaction, time: int = 0):
        if not is_admin(interaction.user):
            await interaction.response.send_message("You dont have permission to use this command", ephemeral=True)
            return
        if time < 0:
            await interaction.response.send_message("Time must be greater than 0", ephemeral=True)
            return
        if time == 0:
            self.word_filter_enabled = False
            await interaction.response.send_message("Word filtering has been disabled, use /enablewordfilter, to turn it back on")

            log_moderation(
                guild_id=interaction.guild.id,
                moderator_id=interaction.user.id,
                action="Disabled the word filter"
            )
        else:
            self.word_filter_enabled = False
            # Disable for the specified number of minutes
            self.word_filter_resume_at = (
                datetime.now(timezone.utc) + timedelta(minutes=time)
            )

            await interaction.response.send_message(
                f"Word filtering has been disabled for {time} minute(s)."
            )
            log_moderation(
                guild_id=interaction.guild.id,
                moderator_id=interaction.user.id,
                action=f"Temporarily disabled word filter for {time} minutes"
            )
            
    @app_commands.command(
    name="enable_word_filter",
    description="Enable the word filter"
    )
    @app_commands.guild_only()
    async def enable_word_filter(self, interaction: discord.Interaction):
        if not is_admin(interaction.user):
            await interaction.response.send_message(
                "You don't have permission to use this command.",
                ephemeral=True
            )
            return

        self.word_filter_enabled = True
        self.word_filter_resume_at = None

        await interaction.response.send_message(
            "Word filtering has been enabled."
        )

    @app_commands.command(name='disable_link_filter', description='disable link filtering for a set time or until its enableed again')
    @app_commands.guild_only
    async def disable_link_filter(self, interaction: discord.Interaction, time: int = 0):
        if not is_admin(interaction.user):
            await interaction.response.send_message("You dont have permission to use this command", ephemeral=True)
            return
        if time < 0:
            await interaction.response.send_message("Time must be greater than 0", ephemeral=True)
            return
        if time == 0:
            self.link_filter_enabled = False
            await interaction.response.send_message("Link filtering has been disabled, use /enablelinkfilter, to turn it back on")
        else:
            self.link_filter_enabled = False
            # Disable for the specified number of minutes
            self.link_filter_resume_at = (
                datetime.now(timezone.utc) + timedelta(minutes=time)
            )

            await interaction.response.send_message(
                f"Word filtering has been disabled for {time} minute(s)."
            )
    @app_commands.command(
    name="enable_link_filter",
    description="Enable the link filter"
    )
    @app_commands.guild_only()
    async def enable_link_filter(self, interaction: discord.Interaction):
        if not is_admin(interaction.user):
            await interaction.response.send_message(
                "You don't have permission to use this command.",
                ephemeral=True
            )
            return

        self.link_filter_enabled = True
        self.link_filter_resume_at = None

        await interaction.response.send_message(
            "Link filtering has been enabled."
        )



async def setup(bot):
    await bot.add_cog(AutoMod(bot))