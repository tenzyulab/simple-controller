from asyncio import TimeoutError

from discord import Embed
from discord.ext.commands import Cog, command, group, has_permissions


class TextChannel(Cog):
    def __init__(self, bot):
        self.bot = bot

    @group()
    async def channel(self, ctx):
        """help channelで詳細を表示"""
        if not ctx.invoked_subcommand:
            await ctx.send("サブコマンドを指定してください。")

    @channel.command()
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int):
        """purge <number> で指定された数のメッセージを一括削除します。"""
        await ctx.channel.purge(limit=number + 1)
        embed = Embed(description=f"メッセージを{number}件削除しました。", colour=0x000000)
        embed.set_footer(text="このメッセージは10秒後に自動で削除されます。")
        await ctx.send(embed=embed, delete_after=10)

    @channel.command()
    @has_permissions(manage_messages=True)
    async def purgeall(self, ctx):
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

    @command(aliases=["cp"])
    @has_permissions(manage_messages=True)
    async def _purge(self, ctx, number):
        await self.purge(ctx, number)

    @command(aliases=["cpa"])
    @has_permissions(manage_messages=True)
    async def _purgeall(self, ctx):
        await self.purgeall(ctx)


def setup(bot):
    bot.add_cog(TextChannel(bot))
