import discord
from custom_prefix import change_prefix, delete_prefix, now_prefix, prefix_dict
from discord.ext.commands import Cog, command, group


class ManagePrefix(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.prefix_dict = prefix_dict

    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.administrator

    @group()
    async def prefix(self, ctx):
        await ctx.send(f"現在のプレフィックスは{now_prefix(ctx.guild.id)}です")


def setup(bot):
    bot.add_cog(ManagePrefix(bot))
