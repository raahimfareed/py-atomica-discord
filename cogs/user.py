import discord
import random
from googletrans import Translator
from discord.ext import commands


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! 🏓\nLatency: {round(self.bot.latency * 1000, 2)}ms")

    @commands.command(aliases=["8ball", "8b", "ball8", "8_ball", "eightball"])
    async def _8ball(self, ctx, *, question=""):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say now.",
            "Outlook not so good.",
            "Very doubtful"
        ]
        if question == "":
            await ctx.send("Please provide a question!")
        else:
            await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

    @commands.command()
    async def nice(self, ctx):
        await ctx.send(69)

    @commands.command(aliases=["69", "sixtynine"])
    async def sixnine(self, ctx):
        await ctx.send("Nice")

    @commands.command(aliases=["googletrans", "gtranslate", "googletranslate", "trans", "tr"])
    async def translate(self, ctx, *, message=""):
        if message == "":
            await ctx.send("Syntax: `.translate`  `[from lang]`  `[to lang]`  "
                           "`<message>`\nExample: `.translate` `en` `es` `Hello World`  ->  `Hola Mundo`\n"
                           "Languages Available: https://bit.ly/32QIE0A")
        else:
            raw_message = message.split()
            current_language = raw_message[0]
            translate_language = raw_message[1]
            cleaned_message = " ".join(raw_message[2:])
            translated_sentence = Translator().translate(cleaned_message, src=current_language, dest=translate_language)
            # print(translated_sentence.text)
            await ctx.send(translated_sentence.text)


def setup(bot):
    bot.add_cog(User(bot))
