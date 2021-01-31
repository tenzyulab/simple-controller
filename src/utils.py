from asyncio import TimeoutError
from textwrap import dedent


class Confirm:
    @staticmethod
    async def dialog(ctx, what: str):
        message = dedent(
            f"""
            {ctx.author.mention} 本当に{what}しますか?
            実行する場合は20秒以内に `y` を送信してください。
            それ以外のメッセージを送信するとキャンセルできます。
            """
        )
        await ctx.send(message)

    @staticmethod
    async def get_response(ctx):
        try:
            response = await ctx.bot.wait_for(
                "message",
                timeout=20,
                check=lambda messages: messages.author.id == ctx.author.id,
            )
            return response
        except TimeoutError:
            return None
