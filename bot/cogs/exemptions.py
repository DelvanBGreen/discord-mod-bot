import discord
from discord import app_commands
from discord.ext import commands
from database.whitelist_db import *
from database.logging_db import log_moderation
from utils.permissions import *

FILTER_CHOICES = [
    app_commands.Choice(name="Word Filtering", value="word"),
    app_commands.Choice(name="Link Filtering", value="link"),
    app_commands.Choice(name="Spam Detection", value="spam"),
    app_commands.Choice(name="All Filters", value="all")
]


class Exemptions(commands.cog):
    exempt = app_commands.group(
        name = "exempt",
        description="Add Automod"
    )
    remove_exempt = app_commands.Group(
        name="remove_exempt",
        description="Remove AutoMod exemptions"
    )

    def __init__(self, bot):
        self.bot = bot

    
    
    @exempt.command(
        name="user",
        description="Exempt a user from AutoMod"
    )
    @app_commands.guild_only()
    @app_commands.choices(exempt_from=FILTER_CHOICES)
    async def exempt_user(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        exempt_from: app_commands.Choice[str]
    ):
        if not is_admin(interaction.user):
            await interaction.response.send_message("You dont have permission to use this command")
            return
        
        await exempt_user(
            interaction.guild.id,
            member.id,
            exempt_from.value
        )

        await log_moderation(
            guild_id=interaction.guild_id,
            user_id=member.id,
            moderator_id=interaction.user.id,
            action="exempt_user",
            reason=f'Exempted {member} from Automod {exempt_from} filtering'
        )

        await interaction.response.send_message(
            f"{member.mention} is now exempt from {exempt_from.value} filtering.",
            ephemeral=True
        )

    @exempt.command(
        name="role",
        description="Exempt a role from AutoMod"
    )
    @app_commands.guild_only()
    @app_commands.choices(exempt_from=FILTER_CHOICES)
    async def exempt_role(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        exempt_from: app_commands.Choice[str]
    ):
        if not is_admin(interaction.user):
            await interaction.response.send_message("You dont have permission to use this command")
            return
        
        await exempt_role(
            interaction.guild.id,
            role.id,
            exempt_from.value
        )

        await log_moderation(
            guild_id=interaction.guild_id,
            moderator_id=interaction.user.id,
            action="exempt_role",
            reason=f'Exempted {role} from Automod {exempt_from} filtering'
        )

        await interaction.response.send_message(
            f"{role} is now exempt from {exempt_from.value} filtering.",
            ephemeral=True
        )

    @exempt.command(
        name="channel",
        description="Exempt a channel from AutoMod"
    )
    @app_commands.guild_only()
    @app_commands.choices(exempt_from=FILTER_CHOICES)
    async def exempt_channel(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        exempt_from: app_commands.Choice[str]
    ):
        if not is_admin(interaction.user):
            await interaction.response.send_message("You dont have permission to use this command")
            return
        
        await exempt_channel(
            interaction.guild.id,
            channel.id,
            exempt_from.value
        )

        await log_moderation(
            guild_id=interaction.guild_id,
            moderator_id=interaction.user.id,
            action="exempt_channel",
            reason=f'Exempted {channel} from Automod {exempt_from} filtering'
        )

        await interaction.response.send_message(
            f"{channel} is now exempt from {exempt_from.value} filtering.",
            ephemeral=True
        )

    @remove_exempt.command(
        name="user",
        description="Un-Exempt a user from AutoMod"
    )
    @app_commands.guild_only()
    @app_commands.choices(exempt_from=FILTER_CHOICES)
    async def exempt_user(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        exempt_from: app_commands.Choice[str]
    ):
        if not is_admin(interaction.user):
            await interaction.response.send_message("You dont have permission to use this command")
            return
        
        await remove_user_exemption(
            interaction.guild.id,
            member.id,
            exempt_from.value
        )

        await log_moderation(
            guild_id=interaction.guild_id,
            user_id=member.id,
            moderator_id=interaction.user.id,
            action="un-exempt_user",
            reason=f'Removed {member} exemption from Automod {exempt_from} filtering'
        )

        await interaction.response.send_message(
            f"{member.mention} is no longer exempt from {exempt_from.value} filtering.",
            ephemeral=True
        )
    @remove_exempt.command(
        name="role",
        description="Un-Exempt a role from AutoMod"
    )
    @app_commands.guild_only()
    @app_commands.choices(exempt_from=FILTER_CHOICES)
    async def exempt_role(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        exempt_from: app_commands.Choice[str]
    ):
        if not is_admin(interaction.user):
            await interaction.response.send_message("You dont have permission to use this command")
            return
        
        await remove_role_exemption(
            interaction.guild.id,
            role.id,
            exempt_from.value
        )

        await log_moderation(
            guild_id=interaction.guild_id,
            moderator_id=interaction.user.id,
            action="un-exempt_role",
            reason=f'Removed {role} exemption from Automod {exempt_from} filtering'
        )

        await interaction.response.send_message(
            f"{role} is no longer exempt from {exempt_from.value} filtering.",
            ephemeral=True
        )
    @remove_exempt.command(
        name="channel",
        description="Un-Exempt a channel from AutoMod"
    )
    @app_commands.guild_only()
    @app_commands.choices(exempt_from=FILTER_CHOICES)
    async def exempt_channel(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        exempt_from: app_commands.Choice[str]
    ):
        if not is_admin(interaction.user):
            await interaction.response.send_message("You dont have permission to use this command")
            return
        
        await remove_channel_exemption(
            interaction.guild.id,
            channel.id,
            exempt_from.value
        )

        await log_moderation(
            guild_id=interaction.guild_id,
            moderator_id=interaction.user.id,
            action='un-exempt_channel',
            reason=f'Removed {channel} exemption from Automod {exempt_from} filtering'
        )

        await interaction.response.send_message(
            f"{channel} is no longer exempt from {exempt_from.value} filtering.",
            ephemeral=True
        )

    