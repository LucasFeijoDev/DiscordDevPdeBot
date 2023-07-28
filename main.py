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

    last_commit_datetime = None

    async def check_github_commits():
        global last_commit_datetime

        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/commits"
        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            commits_data = response.json()

            commits_data = commits_data[::-1]

            for commit in commits_data:
                commit_datetime = commit['commit']['author']['date']
                if last_commit_datetime is None or commit_datetime > last_commit_datetime:
                    message = f"Novo commit de {commit['commit']['author']['name']}: {commit['commit']['message']}"
                    channel = bot.get_channel(DISCORD_CHANNEL_ID)
                    await channel.send(message)

            if commits_data:
                last_commit_datetime = commits_data[0]['commit']['author']['date']

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição ao GitHub: {e}")

    async def background_task():
        await bot.wait_until_ready()
        while not bot.is_closed():
            await check_github_commits()
            await asyncio.sleep(10)

    # Falar para o console que o BOT está on
    @bot.event
    async def on_ready():
        print(f'Estou online e funcionando como {bot.user}!')
        bot.loop.create_task(background_task())

    if __name__ == "__main__":
        bot.run(TOKEN)