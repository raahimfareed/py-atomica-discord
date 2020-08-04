from distutils.command import check
import discord
from discord.ext import commands

import asyncio
import sqlite3
import os


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_id = bot.id
        self.owner_id = os.environ.get("OWNER_ID")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

    @commands.command()
    async def create(self, ctx, create_type):
        permissions = ctx.author.permissions_in(ctx.channel)
        create_type = create_type.lower()

        def check_message(m):
            return m.author != self.bot

        if permissions.manage_roles or permissions.manage_channels:
            if create_type == "role":
                pass
            elif create_type == "text":
                pass
            elif create_type == "voice":
                pass
        else:
            bots_message = await ctx.send("I think not")
            await asyncio.sleep(7)
            await ctx.message.delete()
            await bots_message.delete()

    @commands.command()
    @commands.has_permissions(manage_permissions=True)
    async def channel(self, ctx, channel_type, channel: discord.TextChannel):
        channel_type = channel_type.lower()
        guild_id = ctx.guild.id
        db = sqlite3.connect("bot.db")
        cursor = db.cursor()
        if channel_type == "log" or channel_type == "ann" or channel_type == "bot":
            if channel_type == "log":
                sql = "UPDATE guild_config SET LogChannel = ? WHERE GuildId = ?"
            elif channel_type == "ann":
                sql = "UPDATE guild_config SET AnnouncementChannel = ? WHERE GuildId = ?"
            elif channel_type == "bot":
                sql = "UPDATE guild_config SET BotChannel = ? WHERE GuildId = ?"

            val = (channel.id, guild_id)

            try:
                cursor.execute(sql, val)
                db.commit()
                await ctx.send(f"{channel.mention} set as {channel_type.lower()} channel")
                cursor.close()
                db.close()
            except Exception as e:
                print(e)

        else:
            bots_message = await ctx.send("Invalid channel type!\nSyntax: `.channel <type> <channel mention>`\n\n"
                                          "Channel Types:\n`log` - Log\n`ann` - Announcement\n`bot` - Bot Commands")
            await asyncio.sleep(10)
            await ctx.message.delete()
            await bots_message.delete()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def console(self, ctx, *, message):
        print(message)


def setup(bot):
    bot.add_cog(Staff(bot))
