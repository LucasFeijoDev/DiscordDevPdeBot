import discord
from discord.ext.commands import Bot
from discord.ext import commands
import os

TOKEN = 'MTA2NTAyMzMwOTI5ODgwNjc5NA.GndGbj.6Yz39Jg6WkPA-RJNiO0TPZWL_bQmvNHJ88MWns'

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Estou online e funcionando!')

client.run(TOKEN)    