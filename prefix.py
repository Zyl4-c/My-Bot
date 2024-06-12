import discord
from discord.ext import commands
import json

class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix):
        with open('config.json', 'r') as f:
            config = json.load(f)

        config['prefix'] = new_prefix

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

        embed = discord.Embed(
            title="Prefix Changed",
            description=f"เปลี่ยนเป็น `{new_prefix}`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

        # อัปเดตค่า prefix ใน bot
        self.client.command_prefix = new_prefix

# เชื่อมต่อ cog กับ client
async def setup(client):
    await client.add_cog(Prefix(client)) 