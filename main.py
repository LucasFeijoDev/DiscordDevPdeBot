import discord
from discord.ext import commands
from discord import app_commands

import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = 'p!', intents = intents)

load_dotenv()
print(os.getenv('TOKEN'))

TOKEN = os.getenv('TOKEN')

if TOKEN is None:
    print("O token do bot não foi configurado corretamente nas variáveis de ambiente.")
else:
    #Falar para o console que o BOT está on
    @bot.event
    async def on_ready():
        print('Estou online e funcionando!')
        try: 
            synced = await bot.tree.sync()
            print(f'{len(synced)} comando(s) sincronizados.')
        except Exception as e:
            print(e)

    #Comando de ajuda
    @bot.event
    async def on_message(message):
        if message.content == 'p!ajuda':
            await message.channel.send('Estou configurando certinho o comando de ajuda, mas em breve eu posso te ajudar.')

    bot.run(TOKEN)    
