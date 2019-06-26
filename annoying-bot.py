import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random

import ttsfbfe.tts

bot = commands.Bot(command_prefix='oi mate ')

@bot.event
async def on_ready():
    print("ready lol")
    await bot.change_presence(activity=discord.Game('with your sanity'))

async def random_annoyance(self):
    await self.wait_until_ready()
    channel = self.get_channel(0) # TODO: get random channel from list
    while not self.is_closed():
        await channel.send("@everyone hey im supposed to do some annoying thing but idk")
        await asyncio.sleep(random.randint(15, 10800))

class AnnoyingBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel"""

        channel = ctx.author.voice.channel

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def say(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        ttsfbfe.tts.runTTS(query)

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("output.wav"))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)


    @say.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

bot.add_cog(AnnoyingBot(bot))
bot.loop.create_task(random_annoyance(bot))
token = open("token.txt").read()
bot.run(token)