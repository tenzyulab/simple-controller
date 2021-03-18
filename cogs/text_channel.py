from asyncio import TimeoutError
from textwrap import dedent

from discord import Embed, utils
from discord.ext.commands import Cog, Context, command, group, has_permissions
from src.utils import Confirm


class TextChannel(Cog):
    def __init__(self, bot):
        self.bot = bot

    @group(aliases=["ch"])
    async def channel(self, ctx):
        """help channelで詳細を表示"""
        if not ctx.invoked_subcommand:
            await ctx.send("サブコマンドを指定してください。")

    @channel.command(aliases=["del"])
    @has_permissions(manage_channels=True)
    async def delete(self, ctx: Context, *, reason: str = None):
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

    @channel.command(aliases=["p"])
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int):
        """purge <number> で指定された数のメッセージを一括削除します。"""
        await ctx.channel.purge(limit=number + 1)
        embed = Embed(description=f"メッセージを{number}件削除しました。", colour=0x000000)
        embed.set_footer(text="このメッセージは10秒後に自動で削除されます。")
        await ctx.send(embed=embed, delete_after=10)

    @channel.command(aliases=["pa"])
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

    @channel.command(aliases=["rn"])
    @has_permissions(manage_channels=True)
    async def rename(self, ctx, name):
        """チャンネル名を変更します。"""
        await ctx.channel.edit(name=name)
        await ctx.send(f"{ctx.author.mention} チャンネル名を {ctx.channel.name} に変更しました。")

    @channel.command(aliases=["ns"])
    @has_permissions(manage_channels=True)
    async def nsfw(self, ctx):
        """チャンネルのNSFW設定を切り替えます。"""
        boolen = False
        state = "SFW"
        if not ctx.channel.is_nsfw():
            boolen = True
            state = "NSFW"
        await ctx.channel.edit(nsfw=boolen)
        await ctx.send(f"{ctx.author.mention} このチャンネルは {state} になりました。")

    @channel.command(aliases=["ro"])
    @has_permissions(manage_roles=True)
    async def readonly(self, ctx):
        """@everyoneからのメッセージ送信を禁止します。"""
        everyone = utils.get(ctx.guild.roles, name="@everyone")
        await ctx.channel.edit(sync_permissions=True)
        await ctx.channel.set_permissions(everyone, send_messages=False)
        await ctx.send("everyoneからのメッセージ送信を禁止しました。")

    @channel.command(aliases=["sy"])
    @has_permissions(administrator=True)
    async def sync(self, ctx):
        """チャンネルの権限をカテゴリーに同期します。"""
        await ctx.channel.edit(sync_permissions=True)
        await ctx.send("チャンネルの権限をカテゴリーに同期しました。")


def setup(bot):
    bot.add_cog(TextChannel(bot))
