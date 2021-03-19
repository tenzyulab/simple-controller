from asyncio import TimeoutError
from textwrap import dedent

from discord import CategoryChannel
from discord.errors import NotFound
from discord.ext.commands import Cog, Context, command, group, has_permissions
from src.utils import Confirm


class MyCategoryChannel(Cog):
    def __init__(self, bot):
        self.bot = bot

    @group(aliases=["ca"])
    async def category(self, ctx: Context):
        """help channelで詳細を表示"""
        if not ctx.invoked_subcommand:
            await ctx.send("サブコマンドを指定してください。")

    @category.command(aliases=["de"])
    @has_permissions(manage_channels=True)
    async def delete(
        self, ctx: Context, category: CategoryChannel = None, *, reason: str = None
    ):
        """チャンネルごとカテゴリーを削除します。"""
        if category is None:
            try:
                category = ctx.channel.category
            except AttributeError:
                await ctx.reply("カテゴリーを指定してください。")
        if reason is None:
            reason = "削除された理由は記載されていません。"
        await Confirm.dialog(ctx, "チャンネルごとカテゴリーを削除")
        response = await Confirm.get_response(ctx)
        if response is None:
            await ctx.send("タイムアウトしました。")
            return
        if not response.content in ["y", "Y", "ｙ", "Ｙ"]:
            await ctx.send("キャンセルしました。")
            return
        [await channel.delete(reason=reason) for channel in category.channels]
        await category.delete(reason=reason)
        try:
            await ctx.reply("カテゴリーを削除しました。")
        except NotFound:
            await ctx.author.send("カテゴリーを削除しました。")


def setup(bot):
    bot.add_cog(MyCategoryChannel(bot))
