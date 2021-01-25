from discord import Embed
from discord.ext.commands import Cog, command


class ManageMessage(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.author.permissions_in(ctx.channel).manage_messages:
            return True
        await ctx.send("あなたにはメッセージの管理権限がありません。")
        return False

    @command(name="purge", aliases=["p"])
    async def purge_messages(self, ctx, number: int):
        """!purge <number> で指定された数のメッセージを一括削除します。"""
        await ctx.channel.purge(limit=num + 1)
        embed = Embed(description=f"メッセージを{number}件削除しました。", colour=0x000000)
        embed.set_footer(text="このメッセージは10秒後に自動で削除されます。")
        await ctx.send(embed=embed, delete_after=10)

    @command(name="purgeall", aliases=["pa"])
    async def purge_all_messages(self, ctx):
        """全てのメッセージを一括削除します。"""
        await ctx.channel.purge(limit=None)
        embed = Embed(description="メッセージを全件削除しました。", colour=0x000000)
        embed.set_footer(text="このメッセージは10秒後に自動で削除されます。")
        await ctx.send(embed=embed, delete_after=10)


def setup(bot):
    bot.add_cog(ManageMessage(bot))
