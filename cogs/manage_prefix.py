from textwrap import dedent
from typing import List, Tuple

from discord.ext.commands import Bot, Cog, Context, group, has_permissions
from src.custom_prefix import change_prefix, delete_prefix, get_prefix


class ManagePrefix(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @has_permissions(manage_nicknames=True)
    @group(invoke_without_command=True, aliases=["p"])
    async def prefix(self, ctx: Context) -> None:
        """help prefixで詳細を表示"""
        now_prefix: List[str] = get_prefix(self.bot, ctx.message)
        await ctx.send(f"現在のプレフィックスは {' と '.join(now_prefix[2:])} です。")

    @prefix.command(name="set", aliases=["s"])
    async def _set(self, ctx: Context, new_prefix: str) -> None:
        """プレフィックスを変更します。"""
        result: Tuple[str, str] = await change_prefix(ctx.guild.id, new_prefix)
        await ctx.send("プレフィックスを {} から {} に変更しました。".format(*result))

    @prefix.command(aliases=["r"])
    async def reset(self, ctx: Context) -> None:
        """カスタムプレフィックスを削除します。"""
        before_prefix: str = await delete_prefix(ctx.guild.id)
        message = dedent(
            f"""
            カスタムプレフィックス {before_prefix} を削除しました。
            ニックネームでプレフィックスを指定している場合はそちらが優先されます。
            """
        )
        await ctx.send(message)


def setup(bot: Bot) -> None:
    bot.add_cog(ManagePrefix(bot))
