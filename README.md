# AnnoyingBot
Your little brother but in bot form.

Originally made for [Discord Hack Week 2019.](https://blog.discordapp.com/discord-community-hack-week-build-and-create-alongside-us-6b2a7b7bba33)

## Description
Have you ever wanted someone to randomly @mention everyone in your server and scream at you in voice channels? Have you ever wanted to spam someone's DMs without having to do it yourself? Have you ever wanted someone to randomly send you unsolicited kangaroo pictures? Look no further, AnnoyingBot can do all of this for free!

## How To Use
Just add AnnoyingBot to your server and watch all hell break loose!

## User Targeting
Just say `oi mate target @user`, and @user will regret joining your server immediately! 

`Warning: has a 1 in 4 chance of backfiring and a 1 in 1024 chance of banning you or your target`

## Running The Bot
1. Put your Discord bot token in a file named `token.txt` in the same directory as the python script.
2. Install the dependencies listed below.
3. Run `annoying-bot.py` on Linux or MacOS*

*MacOS not tested, run on Linux to ensure the bot runs as intended.

## Dependencies
AnnoyingBot runs on [Python](https://www.python.org/) 3.5.3 or higher.

AnnoyingBot also depends on the following Python modules
- [discordpy](https://github.com/Rapptz/discord.py)
- [soundfile](https://github.com/bastibe/SoundFile)
- [numpy](https://www.numpy.org/)

## Configuration
You can disable certain features or change send intervals in the `config.ini` file. Additional information can be found in `config.ini`. You will need to restart the bot to apply any changes made to the configuration file.

## Custom Messages
You can add your own annoying messages to send in `annoyingPhrases.txt`, and add images in the `images` directory. Changes to these don't require a bot restart.

## Third Party Libraries
In addition to the python modules above, AnnoyingBot uses the following open source library:
- [TTS!!!!!](https://github.com/Epicalert/tts-followed-by-5-exclamation-marks)

## Contributors
- Amado Wilkins (@iiルビ#9624)
- Justin Mendoza (@iiShattered#9775)

---
Copyright 2019 Amado Wilkins & Justin Mendoza

Licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). See `LICENSE` for details.