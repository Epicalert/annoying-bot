#    AnnoyingBot
#    https://github.com/Epicalert/annoying-bot
#
#    Copyright 2019 Amado Wilkins & Justin Mendoza
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import os
import soundfile as sf

import ttsfbfe.tts

bot = commands.Bot(command_prefix='oi mate ')
bot.remove_command("help")

@bot.command()
async def help(ctx):
    await ctx.channel.send("@everyone\nnoone can save you from me")
    await asyncio.sleep(5)
    await ctx.channel.send("@everyone\nyou can check out my github tho\nhttps://github.com/Epicalert/annoying-bot")

def get_all_sendable_text_channels(self):
    outlist = []
    for server in self.guilds:
        for channel in server.channels:
            if channel.type == discord.ChannelType.text and channel.permissions_for(server.me).send_messages:
                outlist = outlist + [channel]
    return outlist

def get_all_occupied_enterable_voice_channels(self):
    outlist = []
    for server in self.guilds:
        for channel in server.channels:
            if channel.type == discord.ChannelType.voice and channel.permissions_for(server.me).connect and channel.permissions_for(server.me).speak and len(channel.members) > 0:
                outlist = outlist + [channel]
    return outlist

def getRandomTextChannel(self):
    availableChannels = get_all_sendable_text_channels(self)
    return availableChannels[random.randint(0, len(availableChannels) - 1)]

def getRandomVoiceChannel(self):
    availableChannels = get_all_occupied_enterable_voice_channels(self)
    return availableChannels[random.randint(0, len(availableChannels) - 1)]

async def annoyingAction_text(self):
    channel = getRandomTextChannel(self)

    annoyingPhrasesFile = open("annoyingPhrases.txt")
    annoyingPhrases = annoyingPhrasesFile.readlines()
    annoyingPhrasesFile.close()
        
    await channel.send("@everyone " +annoyingPhrases[random.randint(0, len(annoyingPhrases) - 1)])

    return channel

async def annoyingAction_image(self):
    channel = getRandomTextChannel(self)

    imageNames = os.listdir("images")
    imageName = imageNames[random.randint(0, len(imageNames) - 1)]

    await channel.send("@everyone", file=discord.File("images/"+imageName))

    return channel

async def annoyingAction_voice(self):
    channel = getRandomVoiceChannel(self)

    await channel.connect()

    annoyingPhrasesFile = open("annoyingPhrases.txt")
    annoyingPhrases = annoyingPhrasesFile.readlines()
    annoyingPhrasesFile.close()
    phraseToSay = annoyingPhrases[random.randint(0, len(annoyingPhrases) - 1)]

    ttsfbfe.tts.runTTS(phraseToSay)

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("output.wav"))
    channel.guild.voice_client.play(source)

    outputsamples, outputrate = sf.read("output.wav")
    outputDuration = int(len(outputsamples)/outputrate)

    await asyncio.sleep(int(outputDuration) + 2) # REALLY hacky way do do it but meh

    await channel.guild.voice_client.disconnect()

    return channel

async def annoyingAction_voiceKick(self):
    channel = getRandomVoiceChannel(self)

    memberToKick = random.choice(channel.members)

    await memberToKick.edit(voice_channel=None)

    return channel

@bot.event
async def on_ready():
    print("ready lol")
    await bot.change_presence(activity=discord.Game('with your sanity'))

async def random_annoyance(self):
    await self.wait_until_ready()
    print("random annoyances will start in 10 seconds.")
    await asyncio.sleep(10)
    annoyanceNames = ["text phrase", "image", "voice phrase", "voice kick"]
    while not self.is_closed():
        seversJoined = len(self.guilds)

        action = random.randint(0,3)

        if action == 0:
            channel = await annoyingAction_text(self)
        elif action == 1:
            channel = await annoyingAction_image(self)
        elif action == 2:
            channel = await annoyingAction_voice(self)
        else:
            channel = await annoyingAction_voiceKick(self)

        waittime = random.randint(int(5/seversJoined), int(60/seversJoined))
        print(annoyanceNames[action] +" sent to " +channel.guild.name +"." +channel.name +"(" +str(channel.id) +"); next annoyance in " +str(waittime) +" seconds.")

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

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

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

#bot.add_cog(AnnoyingBot(bot))
bot.loop.create_task(random_annoyance(bot))
token = open("token.txt").read()
bot.run(token)