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
import time
import configparser

import ttsfbfe.tts

conf = configparser.ConfigParser()
conf.read("config.ini")

bot = commands.Bot(command_prefix='oi mate ')
bot.remove_command("help")

@bot.command()
async def help(ctx):
    await ctx.channel.send("@everyone\nnoone can save you from me")
    await asyncio.sleep(5)
    await ctx.channel.send("@everyone\nyou can check out my github tho\nhttps://github.com/Epicalert/annoying-bot")
    await asyncio.sleep(5)
    await ctx.channel.send("@everyone\n or target someone e.g. `oi mate target @someone`")

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

async def annoyingAction_text(self, channel=None, mentionString="@everyone"):
    if channel == None:
        channel = getRandomTextChannel(self)

    annoyingPhrasesFile = open("annoyingPhrases.txt")
    annoyingPhrases = annoyingPhrasesFile.readlines()
    annoyingPhrasesFile.close()
        
    await channel.send(mentionString +" " +annoyingPhrases[random.randint(0, len(annoyingPhrases) - 1)])

    return channel

async def annoyingAction_image(self, channel=None, mentionString="@everyone"):
    if channel == None:
        channel = getRandomTextChannel(self)

    imageNames = os.listdir("images")
    imageName = imageNames[random.randint(0, len(imageNames) - 1)]

    await channel.send(mentionString, file=discord.File("images/"+imageName))

    return channel

async def annoyingAction_voice(self, channel=None):
    if channel == None:
        channel = getRandomVoiceChannel(self)

    if conf["features"]["voice_tts"] != "true":
        return channel

    if channel.guild.voice_client != None:
        return channel

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
    VOICE_ACTIONS_START = 2 #set to first index of annoyanceNames that contains a voice channel action
    #NOTE: ALL VOICE ACTIONS SHOULD COME AFTER TEXT CHANNEL ACTIONS
    while not self.is_closed():
        seversJoined = len(self.guilds)

        if get_all_occupied_enterable_voice_channels(self) == []:
            action = random.randint(0,VOICE_ACTIONS_START - 1)
        else:
            action = random.randint(0,len(annoyanceNames) - 1)


        if action == 0:
            channel = await annoyingAction_text(self)
        elif action == 1:
            channel = await annoyingAction_image(self)
        elif action == 2:
            channel = await annoyingAction_voice(self)
        else:
            channel = await annoyingAction_voiceKick(self)

        waittime = random.randint(int(int(conf["random"]["interval_min"])/seversJoined), int(int(conf["random"]["interval_max"])/seversJoined))
        print(annoyanceNames[action] +" sent to " +channel.guild.name +"." +channel.name +"(" +str(channel.id) +"); next annoyance in " +str(waittime) +" seconds.")

        await asyncio.sleep(waittime)

async def targeted_annoyance(self, target, actions):
    await self.wait_until_ready()

    if target.dm_channel == None:
        await target.create_dm()

    for i in range(actions):
        maxAction = 3
        if target.voice == None:
            maxAction = 2
            

        action = random.randint(0, maxAction)

        if action == 0:
            await target.dm_channel.send(target.mention)
        elif action == 1:
            await annoyingAction_text(self, target.dm_channel, target.mention)
        elif action == 2:
            await annoyingAction_image(self, target.dm_channel, target.mention)
        else:
            await annoyingAction_voice(self, target.voice.channel)

        
        await asyncio.sleep(random.randint(int(conf["targeted"]["interval_min"]), int(conf["targeted"]["interval_max"])))


class AnnoyingBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def target(self, ctx):
        if conf["features"]["targeted"] != "true":
            await ctx.channel.send(ctx.message.author.mention +" sorry dat disabled ¯\_(ツ)_/¯")
            return

        if conf["features"]["ban_roulette"] == "true":
            roulette = random.randint(0, 1024)
        else:
            roulette = 0

        if ctx.message.mention_everyone or ctx.message.mentions[0].id == self.bot.user.id:
            await ctx.channel.send("no u")
            target = ctx.message.author
        elif len(ctx.message.mentions) == 0:
            await ctx.channel.send("oi " +ctx.message.author.mention +" u didnt mention anyone >:c")
            return
        else:
            target = ctx.message.mentions[0]

        if roulette > 768 and roulette < 1023:
            await ctx.channel.send(file=discord.File("nou.png"))
            target = ctx.message.author
        elif roulette == 1023:
            if ctx.author.permissions_in(ctx.channel).administrator:
                return
            
            await ctx.channel.send(ctx.author.mention +" https://www.youtube.com/watch?v=Xrne2-gOoqU")
            await ctx.channel.send(ctx.author.mention +"you're gettin banned >:D")
            await asyncio.sleep(5)
            await ctx.guild.ban(ctx.message.author, reason="bc why not *dab*")
            return
        else:
            if target.permissions_in(ctx.channel).administrator:
                return
            await ctx.channel.send(ctx.author.mention +" :regional_indicator_b: :regional_indicator_a: :regional_indicator_n: :hammer: ")
            await asyncio.sleep(10)
            await ctx.guild.ban(target, reason="bc why not *dab*")
            return

        actions = random.randint(1,50)

        await ctx.channel.send("annoying " +target.mention +" " +str(actions) +" times.")

        self.bot.loop.create_task(targeted_annoyance(self.bot, target, actions))


bot.add_cog(AnnoyingBot(bot))
if conf["features"]["random"] == "true":
    bot.loop.create_task(random_annoyance(bot))
token = open("token.txt").read()
bot.run(token)