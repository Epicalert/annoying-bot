import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random

import ttsfbfe.tts

bot = commands.Bot(command_prefix='oi mate ')

def get_all_sendable_text_channels(self):
    outlist = []
    for server in self.guilds:
        for channel in server.channels:
            if channel.type == discord.ChannelType.text and channel.permissions_for(server.me).send_messages:
                outlist = outlist + [channel]
    return outlist

@bot.event
async def on_ready():
    print("ready lol")
    await bot.change_presence(activity=discord.Game('with your sanity'))

async def random_annoyance(self):
    await self.wait_until_ready()
    while not self.is_closed():
        availableTextChannels = get_all_sendable_text_channels(self)
        channel = availableTextChannels[random.randint(0, len(availableTextChannels) - 1)]
        
        await channel.send("@everyone hey im supposed to do some annoying thing but idk")

        waittime = random.randint(15, 1800)
        print("annoyance sent to " +channel.guild.name +"." +channel.name +"; next annoyance in " +str(waittime) +" seconds.")

        await asyncio.sleep(waittime)

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