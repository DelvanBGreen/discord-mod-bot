import discord
from discord.ext import commands

from utils.word_filter import contains_blocked_word


class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        # Ignore bots and DMs
        if message.author.bot or message.guild is None:
            return

        # Check message for blocked words
        if contains_blocked_word(message.content):

            try:
                # Delete the offending message
                await message.delete()

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


async def setup(bot):
    await bot.add_cog(AutoMod(bot))