import random
from discord.ext import commands

class RandomNumber(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def สุ่ม(self, ctx, start: int, end: int):
        if start > end:
            await ctx.send("เลขแรกควรน้อยกว่าเลขที่สอง")
        else:
            number = random.randint(start, end)
            await ctx.send(f'{number}')

async def setup(client):
    await client.add_cog(RandomNumber(client))