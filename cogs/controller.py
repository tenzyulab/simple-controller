import discord
from discord.ext import commands


class Controller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.administrator

    @commands.command(aliases=["rn"])
    async def rename(self, ctx, name):
        """チャンネル名を変更します。"""
        await ctx.channel.edit(name=name)
        await ctx.send(f"{ctx.author.mention} チャンネル名を {ctx.channel.name} に変更しました。")

    @commands.command()
    async def nsfw(self, ctx):
        """チャンネルのNSFW設定を切り替えます。"""
        boolen = False
        state = "SFW"
        if not ctx.channel.is_nsfw():
            boolen = True
            state = "NSFW"
        await ctx.channel.edit(nsfw=boolen)
        await ctx.send(f"{ctx.author.mention} このチャンネルは {state} になりました。")

    @commands.command(aliases=["ro"])
    async def readonly(self, ctx):
        """@everyoneからのメッセージ送信を禁止します。"""
        everyone = discord.utils.get(ctx.guild.roles, name="@everyone")
        await ctx.channel.edit(sync_permissions=True)
        await ctx.channel.set_permissions(everyone, send_messages=False)
        await ctx.send("@everyoneからのメッセージ送信を禁止しました。")

    @commands.command(aliases=["sp"])
    async def sync_permissions(self, ctx):
        """チャンネルの権限をカテゴリーに同期します。"""
        await ctx.channel.edit(sync_permissions=True)
        await ctx.send("チャンネルの権限をカテゴリーに同期しました。")


def setup(bot):
    bot.add_cog(Controller(bot))
