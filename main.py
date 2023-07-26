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

    # Função para enviar mensagem no chat do Discord
    async def send_message(channel_id, message):
        channel = bot.get_channel(channel_id)
        await channel.send(message)

    # Função que verifica e envia as mensagens
    async def check_github_activity():
        while True:
            # Verifique aqui as atividades do GitHub usando a API do GitHub
            url = f'https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/events'
            response = requests.get(url)
            
            if response.status_code == 200:
                events = response.json()
                
                for event in events:
                    # Verificar o tipo de evento (commit, merge, etc.)
                    if event['type'] == 'PushEvent':
                        commit_msg = event['payload']['commits'][0]['message']
                        await send_message(DISCORD_CHANNEL_ID, f'Commit no GitHub: {commit_msg}')
                    elif event['type'] == 'PullRequestEvent':
                        action = event['payload']['action']
                        pr_title = event['payload']['pull_request']['title']
                        await send_message(DISCORD_CHANNEL_ID, f'Pull Request {action}: {pr_title}')
                    # Adicione mais verificações de eventos conforme necessário
            
            # Aguarde 1 minuto antes de verificar novamente
            await asyncio.sleep(60)
           
    # Falar para o console que o BOT está on
    @bot.event
    async def on_ready():
        print(f'Estou online e funcionando como {bot.user}!')
        
    bot.run(TOKEN)