import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

import requests
import asyncio

from flask import Flask, request, jsonify

intents = discord.Intents.default()
intents.typing = True                
intents.messages = True              
intents.reactions = True           
intents.guilds = True               
intents.message_content = True

bot = commands.Bot(command_prefix='p!', intents=intents)
app = Flask(__name__)

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

    @app.route("/github-webhook", methods=["POST"])
    async def github_webhook(request):
        data = await request.json()
        if "commits" in data:
            for commit in data["commits"]:
                message = f"Novo commit de {commit['author']['name']}: {commit['message']}"
                channel_id = DISCORD_CHANNEL_ID  # Substitua pelo ID do canal do Discord desejado
                channel = bot.get_channel(channel_id)
                await channel.send(message)
        return jsonify({"message": "OK"})  # Respondendo ao webhook do GitHub
        
           
    # Falar para o console que o BOT está on
    @bot.event
    async def on_ready():
        print(f'Estou online e funcionando como {bot.user}!')
    if __name__ == "__main__":
        bot.run(TOKEN)