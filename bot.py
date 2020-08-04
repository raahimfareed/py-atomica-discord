import discord
import os
import dotenv
from discord.ext import commands

dotenv.load_dotenv()

command_prefix = "."
bot = commands.Bot(command_prefix=command_prefix)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.run(os.environ.get("TOKEN"))
