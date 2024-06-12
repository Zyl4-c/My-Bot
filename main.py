import discord
import os
import json
from myserver import server_on
from discord.ext import commands
#from dotenv import load_dotenv

# Load .env variables
#load_dotenv()

intents = discord.Intents.all()

def get_prefix(client, message):
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config['prefix']

client = commands.Bot(command_prefix=get_prefix, intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} (ID: {client.user.id})')
    print('------')

    extensions = ['rdnumber', 'command', 'chatbox', 'music', 'welcome', 'leave', 'prefix', 'dm_mb', 'remind' ]

    for extension in extensions:
        try:
            await client.load_extension(extension)
            print(f'Loaded extension: {extension}')
        except Exception as e:
            print(f'Failed to load extension {extension}: {e}')

server_on()

client.run(os.getenv('TOKEN'))