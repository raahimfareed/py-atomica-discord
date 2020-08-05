import discord
from discord.ext import commands

import asyncio
import sqlite3
import os


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_id = os.environ.get("BOT_ID")
        self.owner_id = os.environ.get("OWNER_ID")

    @commands.group()
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx):
        pass

    @role.command(name="create")
    async def _create(self, ctx, name):
        await ctx.guild.create_role(name=name)
        bots_message = await ctx.send(f"Role `{name}` created.")
        await asyncio.sleep(5)
        await ctx.message.delete()
        await bots_message.delete()

    @role.command(name="delete")
    async def _delete(self, ctx, role: discord.Role, *, reason=""):
        bots_question = await ctx.send("Are you sure you want to delete this role? Y/N")

        msg = await self.bot.wait_for("message", check=lambda x: x.author == ctx.message.author)

        if msg and msg is not None:
            if msg.content.lower() == "y" or msg.content.lower() == "yes":
                await role.delete(reason=reason)
                bots_reply = await ctx.send(f"{role.name} deleted.")
            elif msg.content.lower() == "n" or msg.content.lower() == "no":
                bots_reply = await ctx.send(f"{role.name} not deleted.")
            else:
                bots_reply = await ctx.send("Invalid reply! Role not deleted.")

            await asyncio.sleep(5)
            await ctx.message.delete()
            await bots_question.delete()
            await msg.delete()
            await bots_reply.delete()

    @role.command(name="give")
    async def _give(self, ctx, mention: discord.Member, role: discord.Role):
        if role in mention.roles:
            await mention.remove_roles(role)
            await ctx.send(f"{role.name} removed from {mention.mention}")
        else:
            await mention.add_roles(role)
            await ctx.send(f"{mention.mention} assigned {role.name}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

    # Incomplete
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
