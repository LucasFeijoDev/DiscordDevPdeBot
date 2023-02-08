#Blibiotecas, comandos e libraries

import discord 
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = 'p!', intents = intents)

TOKEN = 'TOKEN AQUI'

#Falar para o console que o BOT está on
@client.event
async def on_ready():
    print('Estou online e funcionando!')
    try: 
        synced = await client.tree.sync()
        print(f'{len(synced)} comando(s) sincronizados.')
    except Exception as e:
        print(e)


#Quando alguém marcar o BOT dar uma mensagem
@client.event
async def on_message(message):
    if message.mentions and client.user in message.mentions:
        await message.channel.send('Olá meu amigo, você pode digitar "p!ajuda" para ver oque eu tenho pra você.')


#Comando de ajuda
@client.event
async def on_message(message):
    if message.content == 'p!ajuda':
        await message.channel.send('Estou configurando certinho o comando de ajuda, mas em breve eu posso te ajudar.')


#Comando de apresentação
@client.tree.command(name='ola')
async def ola(interaction: discord.Interaction):
    await interaction.response.send_message(f'Olá {interaction.user.mention}! eu sou o PDEBOT.')
    

#Comando de falar por você
@client.tree.command(name='falar')
@app_commands.describe(palavra_frase = 'Oque eu deveria falar por você?')
async def say(interaction: discord.Interaction, palavra_frase: str):
    await interaction.response.send_message(f'{interaction.user.name} falou: {palavra_frase}')


client.run(TOKEN)
