import discord
from discord.ext import commands
import json

class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"นรสิงค์เข้ามาล้าวววว")
        else:
            await ctx.send("เข้าห้องพูดคุยก่อนเด้")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send(f"เออออกก็ได้พวกเฒ่า")
        else:
            await ctx.send("เข้าไม่ได้โว้ย")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setserver(self, ctx, guild_id: int):
        # Check if guild_id is already set in the config
        with open('config.json', 'r') as f:
            config = json.load(f)

        if str(guild_id) in config["guilds"]:
            await ctx.send("Server channel is already set.")
            return

        config["guilds"][str(guild_id)] = {}
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

        await ctx.send(f'Successfully set server channel.')

async def setup(client):
    await client.add_cog(Voice(client)) 