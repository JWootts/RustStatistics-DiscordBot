import os
import requests
import discord
import json
from collections import namedtuple
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
STEAM_KEY = os.getenv('STEAM_KEY')
client = discord.Client()
NEWLINE = " \n"
RUSTBOT_HELP = " **Rustbot Help**" + NEWLINE + \
                "- !rustbot playtime steamID" + NEWLINE + \
                "- !rustbot stats steamID"

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if str(message.content).lower().__contains__('!rustbot help'):
        await message.channel.send(RUSTBOT_HELP)
        return

    if str(message.content).lower().__contains__('!rustbot playtime'):
        steamID = str(message.content).replace("!rustbot playtime", "").strip()
        if steamID != "":
            data = requests.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' + STEAM_KEY + '&steamid=' + steamID + '&format=json')

            x = json.loads(data.content, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            if x.response.__len__() != 0:
                for gameStat in x.response.games:
                    if gameStat.appid == 252490:
                        timePlayed = float(gameStat.playtime_forever) / 60.0
                        await message.channel.send("RUST PLAYTIME - **%d** Hours Played" %timePlayed)
                        return
            else:
                await message.channel.send("Private Player Profile... Probably a Cheater POGU :))")

        else:
            await message.channel.send("Invalid request. Please use !rustbot help for more help.")

    elif str(message.content).lower().__contains__('!rustbot stats'):
        steamID = str(message.content).replace("!rustbot stats", "").strip()
        returnString = ""
        if steamID != "":
            data = requests.get('https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid=252490&key=' + STEAM_KEY + '&steamid=' + steamID)
            if data.ok:
                x = json.loads(data.content, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

                for playerStats in x.playerstats.stats:
                    returnString += str(playerStats.name).replace("_", " ") + ": " + str(playerStats.value) + NEWLINE

                await message.author.create_dm()
                await message.author.dm_channel.send("Playerstats for steamID: '**" + steamID + "**'\n \n" + returnString)
                await message.channel.send("Player Rust Results have been DM'd to you :)")
            else:
                await message.channel.send("Private Player Profile... Probably a Cheater POGU :))")
    else:
        await message.channel.send("Invalid request. Please use !rustbot help for more help.")

client.run(TOKEN)
