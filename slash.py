# commands.py
import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="ping", description="เช็คค่า latency")
    async def ping(self, ctx):
        await ctx.respond(f' {round(self.client.latency * 1000)}ms')

async def setup(client):
    await client.add_cog(General(client))
