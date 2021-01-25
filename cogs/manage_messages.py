from asyncio import TimeoutError

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
        await ctx.send(
            f"""{ctx.author.mention} 本当に全てのメッセージを一括削除しますか？\n
        実行する場合は20秒以内に `y` を送信してください。\n
        それ以外のメッセージを送信するとキャンセルできます。"""
        )
        try:
            response = await self.bot.wait_for(
                "message",
                timeout=20,
                check=lambda messages: messages.author.id == ctx.author.id,
            )
        except TimeoutError:
            await ctx.send("タイムアウトしました。")
            return
        if not response.content in ["y", "Y", "ｙ", "Ｙ"]:
            await ctx.send("キャンセルしました。")
            return
        await ctx.channel.purge(limit=None)
        embed = Embed(description="メッセージを全件削除しました。", colour=0x000000)
        embed.set_footer(text="このメッセージは10秒後に自動で削除されます。")
        await ctx.send(embed=embed, delete_after=10)


def setup(bot):
    bot.add_cog(ManageMessage(bot))
