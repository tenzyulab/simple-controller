from pathlib import Path
from traceback import print_exc

from discord import Game
from discord.ext.commands import Bot

import const
from src.custom_prefix import get_prefix


class MyBot(Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        print(f"{const.BOT_NAME} を起動します。")

        for cog in Path("cogs/").glob("*.py"):
            try:
                self.load_extension("cogs." + cog.stem)
                print(f"{cog.stem}.pyは正常にロードされました。")
            except Exception:
                print_exc()

    async def on_ready(self):
        print(f"{self.user} としてログインしました。")
        activity = Game(name="?help または @Simple Controller help")
        await self.change_presence(activity=activity)


if __name__ == "__main__":
    bot = MyBot(command_prefix=get_prefix)
    bot.run(const.DISCORD_BOT_TOKEN)
