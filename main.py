import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.typing = True                
intents.messages = True              
intents.reactions = True           
intents.guilds = True               
intents.message_content = True

bot = commands.Bot(command_prefix='p!', intents=intents)

load_dotenv()

TOKEN = os.getenv('TOKEN')

if TOKEN is None:
    print("O token do bot não foi configurado corretamente nas variáveis de ambiente.")
else:
    # Falar para o console que o BOT está on
    @bot.event
    async def on_ready():
        print('Estou online e funcionando!')

    # Comando de ajuda
    @bot.command()
    async def ajuda(ctx):
        await ctx.send('Estou configurando certinho o comando de ajuda, mas em breve eu posso te ajudar.')

    # Resposta ao mencionar o bot
    @bot.event
    async def on_message(message):
        #Quando mencionado ele responde o usuário
        if bot.user.mentioned_in(message):
            await message.channel.send('Você pode digitar "p!ajuda" para obter mais informações.')

        await bot.process_commands(message)

    bot.run(TOKEN)