import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

import requests
import asyncio

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

    # Comando de ajuda
    @bot.command()
    async def ajuda(ctx):
        await ctx.send('Estou configurando certinho o comando de ajuda, mas em breve eu posso te ajudar.')

    #Comando de brincadeira Ping
    @bot.command()
    async def ping(ctx):
        await ctx.send('Pong!')

    #Comando de mandar mensagem
    @bot.command()
    async def falar(ctx, *, mensagem):
        mensagem_falada = f"{mensagem}"
        await ctx.send(mensagem_falada)
        await ctx.message.delete()

    # Resposta ao mencionar o bot
    @bot.event
    async def on_message(message):
        #Quando mencionado ele responde o usuário
        if bot.user.mentioned_in(message):
            await message.channel.send('Você pode digitar "p!ajuda" para obter mais informações.')

        await bot.process_commands(message)

    #Comentando sempre que tem algum commit no repositório
    DISCORD_CHANNEL_ID = 1133787510301003806
    GITHUB_OWNER = 'LucasFeijoDev'
    GITHUB_REPO = 'DiscordDevPdeBot'

    last_commit_sent = None

    def check_for_commits():
        url = f'https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/commits'
        response = requests.get(url)

        if response.status_code == 200:
            commits = response.json()
            last_commit = commits[0]['sha']
            return last_commit
        else:
            return None

    async def commit_checker():
        global last_commit_sent

        await bot.wait_until_ready()
        channel = bot.get_channel(DISCORD_CHANNEL_ID)

        while not bot.is_closed():
            last_commit = check_for_commits()

            if last_commit and last_commit != last_commit_sent:
                await channel.send(f'Novo commit no repositório {GITHUB_REPO}!')
                last_commit_sent = last_commit

            await asyncio.sleep(20)  # Verifica a cada 60 segundos
   
    # Falar para o console que o BOT está on
    @bot.event
    async def on_ready():
        print(f'Estou online e funcionando {bot.user}!')
        bot.loop.create_task(commit_checker())

    bot.run(TOKEN)