from asyncio import TimeoutError
from textwrap import dedent

from discord import Embed
from discord.ext.commands import Cog, Context, command, group, has_permissions
from utils.confirm import Confirm


class TextChannel(Cog):
    def __init__(self, bot):
        self.bot = bot

    @group()
    async def channel(self, ctx):
        """help channelで詳細を表示"""
        if not ctx.invoked_subcommand:
            await ctx.send("サブコマンドを指定してください。")

    @channel.command(name="delete", aliases=["del"])
    @has_permissions(manage_channels=True)
    async def _delete(self, ctx: Context, *, reason: str = None):
        """チャンネルを削除します。"""
        if reason is None:
            reason = "削除された理由は記載されていません。"
        await Confirm.dialog(ctx, "チャンネルを削除")
        response = await Confirm.get_response(ctx)
        if response is None:
            await ctx.send("タイムアウトしました。")
            return
        if not response.content in ["y", "Y", "ｙ", "Ｙ"]:
            await ctx.send("キャンセルしました。")
            return
        await ctx.channel.delete(reason=reason)

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
        await Confirm.dialog(ctx, "全てのメッセージを削除")
        response = await Confirm.get_response(ctx)
        if response is None:
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
