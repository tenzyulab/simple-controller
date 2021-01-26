import json
from re import compile
from typing import Dict

import aiofiles
import const
from discord import Message
from discord.ext.commands import Bot
from discord.ext.commands.bot import when_mentioned_or

NICKNAME_PATTERN = compile(r"\[(.+)\]")
with open("src/prefix.json", encoding='UTF-8') as f:
    prefix_dict: Dict[str, str] = json.loads(f.read())


def get_prefix(bot: Bot, message: Message):
    prefixes = []
    match_nickname = NICKNAME_PATTERN.match(message.guild.me.display_name)
    print(type(match_nickname))
    if match_nickname:
        prefixes.append(match_nickname.groups(1))
    if str(message.guild.id) in prefix_dict.keys():
        prefixes.append(prefix_dict)
    if not prefixes:
        prefixes = [const.BOT_PREFIX]
    return when_mentioned_or(*prefixes)(bot, message)


async def reload_prefix():
    async with aiofiles.open('prefix.json', 'w') as f:
        await f.write(json.dumps(prefix_dict, indent=4))


async def change_prefix(guild_id: int, new_prefix: str):
    before_prefix = prefix_dict[guild_id]
    prefix_dict[guild_id] = new_prefix
    await reload_prefix()
    return before_prefix, new_prefix


async def delete_prefix(guild_id: int):
    before_prefix = prefix_dict[guild_id]
    prefix_dict.remove(guild_id)
    await reload_prefix()
    return before_prefix
