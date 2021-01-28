import json
from re import compile
from typing import Dict, List, Tuple

import aiofiles
import const
from discord import Message
from discord.ext.commands import Bot
from discord.ext.commands.bot import when_mentioned_or

NICKNAME_PATTERN = compile(r"\[(.+)\]")

with open("database/prefix.json", encoding="UTF-8") as f:
    prefix_dict: Dict[str, str] = json.loads(f.read())


def get_prefix(bot: Bot, message: Message) -> List[str]:
    prefixes = []
    match_nickname = NICKNAME_PATTERN.match(message.guild.me.display_name)
    if match_nickname:
        prefixes.append(match_nickname.group(1))
    if str(message.guild.id) in prefix_dict.keys():
        prefixes.append(prefix_dict[str(message.guild.id)])
    if not prefixes:
        prefixes = [const.BOT_PREFIX]
    return when_mentioned_or(*prefixes)(bot, message)


async def change_prefix(guild_id: int, new_prefix: str) -> Tuple[str]:
    before_prefix: str = prefix_dict[str(guild_id)]
    prefix_dict[str(guild_id)] = new_prefix
    await reload_prefix()
    return before_prefix, new_prefix


async def delete_prefix(guild_id: int) -> None:
    before_prefix = prefix_dict[str(guild_id)]
    del prefix_dict[str(guild_id)]
    await reload_prefix()
    return before_prefix


async def reload_prefix() -> None:
    async with aiofiles.open("database/prefix.json", "w") as f:
        await f.write(json.dumps(prefix_dict, indent=4))
