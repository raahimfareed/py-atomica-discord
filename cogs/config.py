import asyncio

import discord
from discord.ext import commands
from discord.utils import find

import sqlite3
import os
# from better_profanity import profanity

# profanity.load_censor_words()
# profanity.load_censor_words_from_file("./config/profanity_filter.txt")


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_id = os.environ.get("BOT_ID")
        self.owner_id = os.environ.get("OWNER_ID")
        db = sqlite3.connect("bot.db")
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wallet (
                Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                UserId INTEGER NOT NULL UNIQUE,
                Balance VARCHAR(255) NOT NULL DEFAULT 0
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guild_config (
                Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                GuildId INTEGER NOT NULL UNIQUE,
                LogChannel INTEGER,
                AnnouncementChannel INTEGER,
                BotChannel INTEGER
            );
        """)
        db.commit()
        cursor.close()
        db.close()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game("with you"))
        print("Atomica online!")

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.author.id != self.bot_id:
    #         if not isinstance(message.channel, discord.channel.DMChannel):
    #             guild_owner = message.guild.owner
    #             if profanity.contains_profanity(message.content):
    #                 await message.delete()
    #                 await message.channel.send(f"{message.author} has been warned!")
    #                 await guild_owner.send(f"User `{message.author}` wrote:`{message.content}`")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            bots_message = await ctx.send("You missed something in the command!")
            await asyncio.sleep(7)
            await ctx.message.delete()
            await bots_message.delete()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        general = find(lambda x: x.name == "general", guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            await general.send(f"Beep Boop. I've hopped on the server! "
                               "Say `.help` to know more about me!")
        # print(guild.id)
        db = sqlite3.connect("bot.db")
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        sql = "SELECT * FROM guild_config WHERE GuildId = ?"
        val = (guild.id,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        if result is None:
            sql = "INSERT INTO guild_config (GuildId) VALUES (?)"
            val = (guild.id,)
            cursor.execute(sql, val)
            db.commit()
        cursor.close()
        db.close()


def setup(bot):
    bot.add_cog(Config(bot))
