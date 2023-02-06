#Blibiotecas, comandos e libraries

import discord
from discord.ext.commands import Bot
from discord.ext import commands
import os

#TOKEN para acesso

TOKEN = 'MTA2NTAyMzMwOTI5ODgwNjc5NA.GndGbj.6Yz39Jg6WkPA-RJNiO0TPZWL_bQmvNHJ88MWns'

#Intenção, permissão e prefixo do BOT

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='.', intents=intents)
client = discord.Client(intents=intents)

#Mensagem no console quando estiver online

@client.event
async def on_ready():
    print('Estou online e funcionando!')

#Assim que marcado o BOT oferece ajuda

@client.event 
async def on_message(message):
    if client.user.mention in message.content:
        await message.channel.send('Olá meu amigo, você pode digitar ".help" para obter ajuda.')

client.run(TOKEN)    
