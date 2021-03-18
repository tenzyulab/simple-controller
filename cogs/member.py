from discord import Member
from discord.ext.commands import Bot, Cog, Context, command, group, has_permissions


class MemberCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @group(aliases=["me"])
    async def member(self, ctx):
        """help memberで詳細を表示"""
        if not ctx.invoked_subcommand:
            await ctx.send("サブコマンドを指定してください。")

    @member.command(aliases=["ki"])
    @has_permissions(kick_members=True)
    async def kick(self, ctx: Context, member: Member = None, *, reason: str = None):
        """メンバーをキックします。"""
        if member is None:
            await ctx.reply("キックするユーザーを指定してください。")
            return
        if reason is None:
            reason = "削除された理由は記載されていません。"
        await member.kick(reason=reason)
        await ctx.reply(f"{member.display_name} をキックしました。")


def setup(bot: Bot):
    bot.add_cog(MemberCog(bot))
