from asyncio import TimeoutError
from textwrap import dedent

from discord import Embed
from discord.ext.commands import Cog, Context, command, group, has_permissions


class TextChannel(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def confirm_dialog(self, ctx, what: str):
        message = dedent(
            f"""
            {ctx.author.mention} 本当に{what}しますか?
            実行する場合は20秒以内に `y` を送信してください。
            それ以外のメッセージを送信するとキャンセルできます。
            """
        )
        await ctx.send(message)

    async def get_confirmation_response(self, ctx):
        try:
            response = await self.bot.wait_for(
                "message",
                timeout=20,
                check=lambda messages: messages.author.id == ctx.author.id,
            )
            return response
        except TimeoutError:
            return None

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
        await self.confirm_dialog(ctx, "チャンネルを削除")
        response = await self.get_confirmation_response(ctx)
        if response is None:
            await ctx.send("タイムアウトしました。")
            return
        if not response.content in ["y", "Y", "ｙ", "Ｙ"]:
            await ctx.send("キャンセルしました。")
            return
        await ctx.channel.delete(reason)

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
        await self.confirm_dialog(ctx, "全てのメッセージを削除")
        response = await self.get_confirmation_response(ctx)
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
