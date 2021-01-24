import constant
import discord
from discord.ext import commands


class Controller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.administrator

    @commands.command(aliases=["rn"])
    async def rename(self, ctx, name):
        """Rename Channel Name"""
        await ctx.channel.edit(name=name)
        await ctx.send(f"{ctx.author.mention} renamed {ctx.channel.name}.")

    @commands.command()
    async def nsfw(self, ctx):
        """Toggle Channel NSFW"""
        boolen = False
        state = "SFW"
        if not ctx.channel.is_nsfw():
            boolen = True
            state = "NSFW"
        await ctx.channel.edit(nsfw=boolen)
        await ctx.send(f"{ctx.author.mention} this channel is now {state}")

    @commands.command(aliases=["ro"])
    async def readonly(self, ctx):
        """Disable sending messages by everyone"""
        everyone = discord.utils.get(ctx.guild.roles, name="@everyone")
        await ctx.channel.edit(sync_permissions=True)
        await ctx.channel.set_permissions(everyone, send_messages=False)
        await ctx.send("Disabled sending messages by everyone")

    @commands.command(aliases=["sp"])
    async def sync_permissions(self, ctx):
        """Sync Channel Permissions"""
        await ctx.channel.edit(sync_permissions=True)
        await ctx.send("Synced channel permissions with category.")


def setup(bot):
    bot.add_cog(Controller(bot))
