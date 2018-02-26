import discord
import asyncio
import pymysql.cursors
from time import sleep
from custom_function import logtext
from custom_function import print_message
from custom_function import get_summoner_stats
from custom_function import get_summoner_id
from custom_function import post_latest_game
from custom_function import get_champion_name
from custom_function import get_queue_name
from datetime import datetime
from discord.ext import commands


client = discord.Client()

async def my_background_task():
    await client.wait_until_ready()
    while True:
        channels  = client.get_all_channels()
        for channel in channels:
            if 'J0b3n' in str(channel.guild):
                 if 'Text' in str(channel.category):
                    results_list = post_latest_game()
                    for matche in results_list:
                        matche = results_list[matche]
                        
                        champion_name = get_champion_name(matche.champion)
                        queue = get_queue_name(int(matche.queue))

                        if int(matche.win) is 1:
                            resultat = 'WIN'
                            embed = discord.Embed(title='[+] {} WIN:'.format(matche.summoner_name), description="", color=65280)

                        else:
                            resultat = 'LOSSE'
                            embed = discord.Embed(title='[+] {} LOSSE:'.format(matche.summoner_name), description="", color=16711680)
                    
                        embed.add_field(name="Champion:", value= champion_name)
                        embed.add_field(name="Lane:", value= matche.lane)
                        embed.add_field(name="Queue:", value= queue)

                        embed.add_field(name="KDA:", value= '{}/{}/{}'.format(matche.kills, matche.deaths, matche.assists))
                        embed.add_field(name="Gold Earned/Spent:", value= '{}/{}'.format(matche.goldEarned, matche.goldSpent))
                        embed.add_field(name="Total Damage dealt:", value= matche.totalDamageDealt)
                        embed.add_field(name="Minions Killed:", value= matche.totalMinionsKilled)

                        await channel.send(embed = embed)

                    await asyncio.sleep(60) # task runs every 60 seconds


async def lol_info(message, summoner_pseudo):
    summoner_id, accountId = get_summoner_id(summoner_pseudo)
    summoner = get_summoner_stats(summoner_id, summoner_pseudo)


    embed = discord.Embed(title='[+] {} Infos'.format(summoner.summoner_name), description="", color=0xeee657)
    embed.add_field(name="Summoner Name:", value= summoner.summoner_name)
    embed.add_field(name="Level:", value=summoner.summonerLevel)
    embed.add_field(name="Rank:", value='{} {}'.format(summoner.tier, summoner.rank))
    embed.add_field(name="Streak:", value=summoner.hotStreak)
    embed.add_field(name="Wins:", value=summoner.wins)
    embed.add_field(name="Losses:", value=summoner.losses)
    embed.add_field(name="League Name:", value=summoner.leagueName)
    embed.add_field(name="League Points:", value=summoner.leaguePoints)
    await message.channel.send(embed = embed)



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$lol_info'):
        summoner_pseudo = message.content.split('"')[1].replace('"','')
        await lol_info(message, summoner_pseudo)
    
    logtext(message)


client.loop.create_task(my_background_task())

client.run('')