import asyncio

import discord
from discord.ext import commands


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dm(self, ctx, mention: discord.Member = ""):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            if mention == "":
                await ctx.message.delete()
                await ctx.author.send("I have been summoned!")
            else:
                await ctx.message.delete()
                if ctx.author == ctx.message.guild.owner:
                    await ctx.mention.send(f"{ctx.author} has sent me here!")
                else:
                    bots_message = await ctx.send(f"{ctx.author} you don't have permissions!")
                    await asyncio.sleep(5)
                    await bots_message.delete()
        else:
            await ctx.send(f"I'm already here {ctx.author}")


def setup(bot):
    bot.add_cog(Staff(bot))
