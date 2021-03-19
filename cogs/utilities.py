from time import monotonic

from discord import Permissions
from discord.ext.commands import Bot, Cog, Context, command
from discord.utils import oauth_url


class Utilities(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def ping(self, ctx):
        """接続と応答速度を確認できます。"""
        tmp = monotonic()
        msg = await ctx.send("計算中...")
        latency = (monotonic() - tmp) * 1000
        await msg.edit(content=f"Pong! 応答速度は **{int(latency)}** ms です。")

    @command(aliases=["in"])
    async def invite(self, ctx: Context):
        """この BOT の招待リンクを送ります。"""
        invite_url = oauth_url(self.bot.user.id, Permissions(administrator=True))
        await ctx.reply(f"<{invite_url}>")


def setup(bot: Bot):
    bot.add_cog(Utilities(bot))
