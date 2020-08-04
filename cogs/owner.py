import discord
from discord.ext import commands

import asyncio
import sqlite3
import os


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = os.environ.get("OWNER_ID")

    @commands.command()
    async def give(self, ctx, mention: discord.Member, amount: int):
        if ctx.author.id != self.owner_id and ctx.author != self.bot.user:
            bots_message = await ctx.send("Wat?")
            await asyncio.sleep(7)
            await ctx.message.delete()
            await bots_message.delete()
        else:
            db = sqlite3.connect("bot.db")
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            sql = "SELECT * FROM wallet WHERE UserId = ?"
            val = (mention.id,)
            cursor.execute(sql, val)
            result = cursor.fetchone()
            new_balance = amount
            if result is None:
                sql = "INSERT INTO wallet (UserId, Balance) VALUES (?, ?)"
                val = (int(mention.id), new_balance)
            elif result is not None:
                balance = int(result["Balance"]) + amount
                sql = "UPDATE wallet SET Balance = ? WHERE UserId = ?"
                val = (balance, int(mention.id))

            try:
                cursor.execute(sql, val)
            except Exception as e:
                print(e)
            await ctx.send(f"{ctx.author} have given {mention.mention} {str(amount)} coins.\n"
                           f"Their balance is now {balance} coins")
            db.commit()
            cursor.close()
            db.close()


def setup(bot):
    bot.add_cog(Owner(bot))
