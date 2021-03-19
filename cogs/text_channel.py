from asyncio import TimeoutError
from textwrap import dedent

from discord import AllowedMentions, Embed, utils
from discord.errors import Forbidden
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

    @channel.command(aliases=["de", "del"])
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

    @channel.command(aliases=["pu"])
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

    @channel.command(aliases=["we"])
    @has_permissions(manage_webhooks=True)
    async def webhook(self, ctx: Context, *, name: str = None):
        """チャンネルの Webhook を作成します。"""
        if name is None:
            name = ctx.channel.name
        new_webhook = await ctx.channel.create_webhook(name=name)
        try:
            await ctx.author.send(
            f"{ctx.channel.mention} の Webhook を作成しました。\nURL: {new_webhook.url}"
        )
        except Forbidden:
            await ctx.send{f"{ctx.channel.mention} の Webhook を作成しました。"}

    @channel.command(aliases=["ua"])
    @has_permissions(manage_messages=True)
    async def unpinall(self, ctx: Context):
        """チャンネルのピン留めを全て外します。"""
        await Confirm.dialog(ctx, "チャンネルのピン留めを全て外")
        response = await Confirm.get_response(ctx)
        if response is None:
            await ctx.reply("タイムアウトしました。")
            return
        if not response.content in ["y", "Y", "ｙ", "Ｙ"]:
            await ctx.reply("キャンセルしました。")
            return
        pins = await ctx.channel.pins()
        [await pin.unpin() for pin in pins]
        await ctx.reply(f"{len(pins)} 件のピン留めを外しました。")

    @channel.command(aliases=["to"])
    @has_permissions(manage_channels=True)
    async def topic(self, ctx: Context, topic: str = None):
        """チャンネルのトピックを変更します。"""
        await ctx.channel.edit(topic=topic)
        await ctx.reply(
            f"チャンネルのトピックを {ctx.channel.topic} に変更しました。",
            allowed_mentions=AllowedMentions(everyone=False, users=False, roles=False),
        )


def setup(bot):
    bot.add_cog(TextChannel(bot))
