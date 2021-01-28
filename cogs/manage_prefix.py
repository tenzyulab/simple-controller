from typing import List, Tuple

from discord.ext.commands import Bot, Cog, Context, group
from src.custom_prefix import change_prefix, delete_prefix, get_prefix


class ManagePrefix(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        return ctx.author.guild_permissions.manage_nicknames

    @group(invoke_without_command=True, aliases=["p"])
    async def prefix(self, ctx: Context) -> None:
        now_prefix: List[str] = get_prefix(self.bot, ctx.message)
        await ctx.send(f"現在のプレフィックスは {' と '.join(now_prefix[2:])} です。")

    @prefix.command(aliases=["s"])
    async def set(self, ctx: Context, new_prefix: str) -> None:
        result: Tuple[str] = await change_prefix(ctx.guild.id, new_prefix)
        await ctx.send("プレフィックスを {} から {} に変更しました。".format(*result))

    @prefix.command(alias=["r"])
    async def reset(self, ctx: Context) -> None:
        before_prefix: str = await delete_prefix(ctx.guild.id)
        await ctx.send(
            f"カスタムプレフィックス {before_prefix} を削除しました。\nニックネームでプレフィックスを指定している場合はそちらが優先されます。"
        )


def setup(bot: Bot) -> None:
    bot.add_cog(ManagePrefix(bot))
