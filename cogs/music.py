import discord
from discord.ext import commands
import os
import youtube_dl


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['j', 'jn'])
    async def join(self, ctx):
        if ctx.message.author.voice:
            channel = ctx.message.author.voice.channel
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                await channel.connect()

            await ctx.send(f"Joined {channel}")
        else:
            await ctx.send("You're not in a voice channel!")

    @commands.command(aliases=["l", "lv"])
    async def leave(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        print(voice)
        if voice is None:
            await ctx.send("I've been bamboozled! I'm not in a voice channel")
        elif not ctx.message.author.voice:
            await ctx.send("You're not in my voice channel!")
        else:
            channel = ctx.message.author.voice.channel
            if voice and voice.is_connected():
                if self.bot.user in channel.members:
                    await voice.disconnect()
                    await ctx.send(f"Left {channel}")
                else:
                    await ctx.send("You're not in my voice channel!")
            else:
                await ctx.send("I've been bamboozled! I'm not in a voice channel")

    @commands.command(aliases=["p", "pl"])
    async def play(self, ctx, url: str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")
        except Exception as e:
            print(e)
            # return
        except PermissionError as perm_error:
            print("Song being used: ", perm_error)
            await ctx.send("`Error: A song is already playing!`")
            return

        bots_message = await ctx.send("Getting everything ready...")

        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        ydl_options = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                }
            ],
        }

        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            print("Downloading song now")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                os.rename(file, "song.mp3")
                print(f"Renamed File: {file}")

        voice.play(discord.FFmpegOpusAudio("song.mp3"), after=lambda e: print(f"{e} has finished playing"))
        # voice.source = discord.PCMVolumeTransformer(voice.source)
        # voice.source.volume = 0.07
        discord.PCMVolumeTransformer(voice.source, 0.07)

        new_name = name.rsplit("-", 2)
        await ctx.send(f"Playing: {new_name}")
        print("Playing")


def setup(bot):
    bot.add_cog(Music(bot))
