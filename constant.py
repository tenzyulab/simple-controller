from os import getenv

from dotenv import load_dotenv

load_dotenv()

# get token from .env
DISCORD_BOT_TOKEN = getenv("DISCORD_BOT_TOKEN")


# setting
DISCORD_BOT_NAME = "BOT TEMPLATE"
DISCORD_BOT_PREFIX = "?"
